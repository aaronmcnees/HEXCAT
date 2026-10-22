#!/usr/bin/env python3
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "HEXCAT4.html"
TOP_ART = ROOT / "hcx.png"
PID_FILE = ROOT / ".aether_hash_wrapper.pid"
HOST = "127.0.0.1"
PORT = 8787
PORT_SCAN_END = 8799

HASHCAT_CANDIDATES = [
    "/usr/local/bin/hashcat",
    shutil.which("hashcat") or "",
    "/usr/bin/hashcat",
]
HASHCAT = next((p for p in HASHCAT_CANDIDATES if p and Path(p).exists()), shutil.which("hashcat") or "hashcat")
HCXPCAPNGTOOL = shutil.which("hcxpcapngtool") or "hcxpcapngtool"
HCXHASHTOOL = shutil.which("hcxhashtool") or "hcxhashtool"

state_lock = threading.Lock()
state = {
    "running": False,
    "kind": None,
    "pid": None,
    "command": [],
    "display_command": "",
    "started": None,
    "ended": None,
    "exit_code": None,
    "log": [],
}
current_process = None


def append_log(line):
    line = line.rstrip("\r\n")
    if not line:
        return
    with state_lock:
        state["log"].append(line)
        if len(state["log"]) > 3000:
            state["log"] = state["log"][-3000:]


def reset_state(kind, argv):
    with state_lock:
        state.update({
            "running": True,
            "kind": kind,
            "pid": None,
            "command": list(argv),
            "display_command": shlex.join(argv),
            "started": time.time(),
            "ended": None,
            "exit_code": None,
            "log": [],
        })


def run_streaming(kind, argv, cwd=None):
    global current_process
    with state_lock:
        if state["running"]:
            raise RuntimeError("Another job is already running. Stop it first.")
    reset_state(kind, argv)

    def worker():
        global current_process
        try:
            p = subprocess.Popen(
                argv,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                errors="replace",
            )
            current_process = p
            with state_lock:
                state["pid"] = p.pid
            append_log("$ " + shlex.join(argv))
            append_log("")
            assert p.stdout is not None
            for line in p.stdout:
                append_log(line)
            rc = p.wait()
            with state_lock:
                state["running"] = False
                state["exit_code"] = rc
                state["ended"] = time.time()
            append_log(f"[process exited with code {rc}]")
        except Exception as e:
            append_log(f"ERROR: {e}")
            with state_lock:
                state["running"] = False
                state["exit_code"] = -1
                state["ended"] = time.time()
        finally:
            current_process = None

    threading.Thread(target=worker, daemon=True).start()


def quick_run(argv, timeout=30):
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout, errors="replace")
    return p.returncode, p.stdout


def json_response(handler, obj, status=200):
    data = json.dumps(obj).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(data)


def read_json(handler):
    n = int(handler.headers.get("Content-Length", "0") or 0)
    if n > 1024 * 1024:
        raise ValueError("Request too large")
    raw = handler.rfile.read(n) if n else b"{}"
    return json.loads(raw.decode("utf-8") or "{}")


def require_file(path, label):
    p = Path(path).expanduser()
    if not p.is_file():
        raise ValueError(f"{label} does not exist: {p}")
    return str(p.resolve())


def ensure_parent(path):
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p.resolve())


def safe_int(v, default, lo=None, hi=None):
    try:
        x = int(v)
    except Exception:
        x = default
    if lo is not None:
        x = max(lo, x)
    if hi is not None:
        x = min(hi, x)
    return x


def installed_rule_files():
    roots = [
        Path("/usr/share/hashcat/rules"),
        Path("/usr/local/share/hashcat/rules"),
        Path("/opt/hashcat/rules"),
        Path.home() / "hashcat" / "rules",
    ]
    found = []
    seen = set()
    for root in roots:
        if root.is_dir():
            for p in sorted(root.glob("*.rule")):
                rp = str(p.resolve())
                if rp not in seen:
                    seen.add(rp)
                    found.append({"name": p.name, "path": rp})
    return found


def _native_file_dialog(title, filters=None, directory=False):
    """Open the desktop-native file chooser without rendering our own dialog."""
    filters = filters or []

    # Linux Mint/MATE normally provides zenity. This gives a GTK file chooser
    # that follows the user's desktop theme instead of Tkinter's dialog.
    zenity = shutil.which("zenity")
    if zenity:
        argv = [zenity, "--file-selection", f"--title={title}"]
        if directory:
            argv.append("--directory")
        else:
            for label, patterns in filters:
                pattern_text = " ".join(patterns)
                argv.append(f"--file-filter={label} | {pattern_text}")
        try:
            r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               text=True, timeout=300)
            if r.returncode == 0:
                return r.stdout.strip()
            return ""
        except Exception:
            pass

    # KDE/native fallback if present.
    kdialog = shutil.which("kdialog")
    if kdialog:
        argv = [kdialog, "--getexistingdirectory" if directory else "--getopenfilename"]
        if not directory and filters:
            specs = []
            for label, patterns in filters:
                specs.append(f"{' '.join(patterns)}|{label}")
            argv.append("\n".join(specs))
        try:
            r = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               text=True, timeout=300)
            if r.returncode == 0:
                return r.stdout.strip()
            return ""
        except Exception:
            pass

    # Last-resort fallback only when the desktop has neither GTK nor KDE picker.
    script = (
        "import tkinter as tk\n"
        "from tkinter import filedialog\n"
        "root=tk.Tk(); root.withdraw(); root.attributes('-topmost', True)\n"
        + (f"p=filedialog.askdirectory(title={title!r})\n" if directory else
           f"p=filedialog.askopenfilename(title={title!r}, filetypes={[ (label, ' '.join(patterns)) for label, patterns in filters ]!r})\n")
        + "print(p)\nroot.destroy()\n"
    )
    try:
        r = subprocess.run([sys.executable, "-c", script], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, text=True, timeout=300)
        return r.stdout.strip()
    except Exception:
        return ""


def picker(kind):
    if kind == "capture":
        title = "Choose capture file"
        filters = [("Packet captures", ["*.pcapng", "*.pcap", "*.cap"]), ("All files", ["*"])]
    elif kind == "hash":
        title = "Choose .22000 hash file"
        filters = [("Hashcat 22000", ["*.22000", "*.hc22000"]), ("All files", ["*"])]
    elif kind == "wordlist":
        title = "Choose wordlist"
        filters = [("Text / wordlists", ["*.txt", "*.dict", "*.lst", "*.wordlist"]), ("All files", ["*"])]
    elif kind == "rule":
        title = "Choose Hashcat rule file"
        filters = [("Hashcat rules", ["*.rule"]), ("All files", ["*"])]
    elif kind == "potfile":
        title = "Choose potfile"
        filters = [("Potfiles", ["*.potfile"]), ("All files", ["*"])]
    else:
        title = "Choose file"
        filters = [("All files", ["*"])]
    return _native_file_dialog(title, filters)


def pick_directory():
    return _native_file_dialog("Choose output folder", directory=True)


def build_extract(cfg):
    capture = require_file(cfg.get("capture", ""), "Capture")
    output = cfg.get("output", "").strip()
    if not output:
        output = str(Path(capture).with_suffix(".22000"))
    output = ensure_parent(output)
    argv = [HCXPCAPNGTOOL, "-o", output]

    if cfg.get("all"):
        argv.append("--all")
    nc = safe_int(cfg.get("nonce", 0), 0, 0, 64)
    if nc:
        argv += ["--nonce-error-corrections", str(nc)]
    timeout = safe_int(cfg.get("eapoltimeout", 5000), 5000, 1, 120000)
    if timeout != 5000:
        argv += ["--eapoltimeout", str(timeout)]
    max_essids = safe_int(cfg.get("maxessids", 1), 1, 1, 64)
    if max_essids != 1:
        argv += ["--max-essids", str(max_essids)]
    if cfg.get("ignore_ie"):
        argv.append("--ignore-ie")

    prefix = cfg.get("sidecar_prefix", "").strip()
    if prefix:
        prefix = ensure_parent(prefix)
        if cfg.get("essid_list"):
            argv += ["-E", prefix + ".essid"]
        if cfg.get("identity_list"):
            argv += ["-I", prefix + ".identity"]
        if cfg.get("username_list"):
            argv += ["-U", prefix + ".username"]
        if cfg.get("csv"):
            argv += ["--csv", prefix + ".csv"]
        if cfg.get("log"):
            argv += ["--log", prefix + ".hcx.log"]
        if cfg.get("pmkid_client"):
            argv += ["--pmkid-client", prefix + ".pmkid-client.22000"]

    argv.append(capture)
    return argv, output


def valid_session(s):
    s = (s or "AETHER").strip()
    if not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", s):
        raise ValueError("Session name may contain only letters, numbers, dot, dash, underscore.")
    return s


def build_hashcat(cfg):
    hashfile = require_file(cfg.get("hashfile", ""), "Hash file")
    mode = str(cfg.get("attack", "0"))
    if mode not in {"0", "1", "3", "6", "7"}:
        raise ValueError("Unsupported attack mode")

    argv = [HASHCAT, "-m", "22000", "-a", mode]
    session = valid_session(cfg.get("session", "AETHER"))
    argv += ["--session", session, "--status", "--status-timer", str(safe_int(cfg.get("status_timer", 5), 5, 1, 120))]

    workload = safe_int(cfg.get("workload", 2), 2, 1, 4)
    argv += ["-w", str(workload)]
    if cfg.get("optimized"):
        argv.append("-O")
    if cfg.get("markov_disable"):
        argv.append("--markov-disable")
    temp = safe_int(cfg.get("temp_abort", 90), 90, 50, 100)
    argv += ["--hwmon-temp-abort", str(temp)]

    devices = (cfg.get("devices") or "").strip()
    if devices:
        if not re.fullmatch(r"[0-9,]+", devices):
            raise ValueError("Device IDs must be comma-separated numbers, e.g. 1 or 1,2")
        argv += ["-d", devices]

    runtime = safe_int(cfg.get("runtime", 0), 0, 0, 604800)
    if runtime:
        argv += ["--runtime", str(runtime)]

    pot = (cfg.get("potfile") or "").strip()
    if pot:
        argv += ["--potfile-path", ensure_parent(pot)]
    outfile = (cfg.get("outfile") or "").strip()
    if outfile:
        argv += ["--outfile", ensure_parent(outfile), "--outfile-format", "2"]

    argv.append(hashfile)

    word1 = (cfg.get("wordlist1") or "").strip()
    word2 = (cfg.get("wordlist2") or "").strip()
    mask = (cfg.get("mask") or "").strip()

    if mode == "0":
        argv.append(require_file(word1, "Wordlist"))
        rule = (cfg.get("rulefile") or "").strip()
        if rule:
            argv += ["-r", require_file(rule, "Rule file")]
    elif mode == "1":
        argv += [require_file(word1, "Left wordlist"), require_file(word2, "Right wordlist")]
        left_rule = (cfg.get("left_rule") or "").strip()
        right_rule = (cfg.get("right_rule") or "").strip()
        if left_rule:
            argv += ["-j", left_rule]
        if right_rule:
            argv += ["-k", right_rule]
    elif mode == "3":
        if not mask:
            raise ValueError("Mask attack requires a mask")
        for i in range(1, 5):
            cs = (cfg.get(f"charset{i}") or "").strip()
            if cs:
                argv += [f"-{i}", cs]
        if cfg.get("increment"):
            argv.append("--increment")
            argv += ["--increment-min", str(safe_int(cfg.get("increment_min", 8), 8, 1, 256))]
            argv += ["--increment-max", str(safe_int(cfg.get("increment_max", 12), 12, 1, 256))]
        argv.append(mask)
    elif mode == "6":
        argv += [require_file(word1, "Wordlist"), mask or "?d?d?d?d"]
        left_rule = (cfg.get("left_rule") or "").strip()
        right_rule = (cfg.get("right_rule") or "").strip()
        if left_rule:
            argv += ["-j", left_rule]
        if right_rule:
            argv += ["-k", right_rule]
    elif mode == "7":
        argv += [mask or "?d?d?d?d", require_file(word1, "Wordlist")]
        left_rule = (cfg.get("left_rule") or "").strip()
        right_rule = (cfg.get("right_rule") or "").strip()
        if left_rule:
            argv += ["-j", left_rule]
        if right_rule:
            argv += ["-k", right_rule]

    return argv


class Handler(BaseHTTPRequestHandler):
    server_version = "HEXCAT-HCX-UI/vIV"

    def log_message(self, fmt, *args):
        pass

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/" or path.endswith(".html"):
            try:
                data = HTML.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_error(500, str(e))
            return
        if path == "/hcx.png":
            try:
                data = TOP_ART.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(data)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_error(500, str(e))
            return
        if path == "/api/state":
            with state_lock:
                snap = dict(state)
                snap["log"] = state["log"][-600:]
            return json_response(self, snap)
        if path == "/api/env":
            info = {
                "hashcat": HASHCAT,
                "hcxpcapngtool": HCXPCAPNGTOOL,
                "hcxhashtool": HCXHASHTOOL,
                "rules": installed_rule_files(),
            }
            for key, cmd in [("hashcat_version", [HASHCAT, "-V"]), ("hcx_version", [HCXPCAPNGTOOL, "-v"])]:
                try:
                    _, out = quick_run(cmd, 8)
                    info[key] = out.strip().splitlines()[0] if out.strip() else "unknown"
                except Exception as e:
                    info[key] = f"unavailable: {e}"
            return json_response(self, info)
        self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            cfg = read_json(self)
            if path == "/api/pick":
                kind = cfg.get("kind", "file")
                return json_response(self, {"path": picker(kind)})
            if path == "/api/pick-dir":
                return json_response(self, {"path": pick_directory()})
            if path == "/api/extract":
                argv, output = build_extract(cfg)
                run_streaming("hcx-extract", argv)
                return json_response(self, {"ok": True, "output": output, "command": shlex.join(argv)})
            if path == "/api/hashcat":
                argv = build_hashcat(cfg)
                run_streaming("hashcat", argv)
                return json_response(self, {"ok": True, "command": shlex.join(argv)})
            if path == "/api/restore":
                session = valid_session(cfg.get("session", "AETHER"))
                argv = [HASHCAT, "--session", session, "--restore"]
                run_streaming("hashcat-restore", argv)
                return json_response(self, {"ok": True, "command": shlex.join(argv)})
            if path == "/api/info":
                hashfile = require_file(cfg.get("hashfile", ""), "Hash file")
                rc, out = quick_run([HCXHASHTOOL, "-i", hashfile, "--info=stdout"], 30)
                return json_response(self, {"ok": rc == 0, "exit_code": rc, "output": out})
            if path == "/api/show":
                hashfile = require_file(cfg.get("hashfile", ""), "Hash file")
                pot = (cfg.get("potfile") or "").strip()
                argv = [HASHCAT, "-m", "22000", hashfile, "--show", "--outfile-format", "2"]
                if pot:
                    argv += ["--potfile-path", str(Path(pot).expanduser())]
                rc, out = quick_run(argv, 30)
                return json_response(self, {"ok": rc == 0, "exit_code": rc, "output": out, "command": shlex.join(argv)})
            if path == "/api/backend":
                rc, out = quick_run([HASHCAT, "-I"], 30)
                return json_response(self, {"ok": rc == 0, "exit_code": rc, "output": out})
            if path == "/api/stop":
                global current_process
                p = current_process
                if p and p.poll() is None:
                    p.send_signal(signal.SIGINT)
                    append_log("[sent SIGINT / clean stop request]")
                    return json_response(self, {"ok": True})
                return json_response(self, {"ok": False, "error": "No running process"}, 409)
            if path == "/api/kill":
                p = current_process
                if p and p.poll() is None:
                    p.kill()
                    append_log("[hard stop sent]")
                    return json_response(self, {"ok": True})
                return json_response(self, {"ok": False, "error": "No running process"}, 409)
            return json_response(self, {"error": "Not found"}, 404)
        except Exception as e:
            return json_response(self, {"ok": False, "error": str(e)}, 400)


def bind_server():
    last_error = None
    for port in range(PORT, PORT_SCAN_END + 1):
        try:
            return ThreadingHTTPServer((HOST, port), Handler), port
        except OSError as e:
            last_error = e
            if getattr(e, "errno", None) not in (98, 48, 10048):
                raise
    raise OSError(f"No free local port from {PORT} through {PORT_SCAN_END}: {last_error}")


def main():
    if not HTML.exists():
        print(f"Missing {HTML}", file=sys.stderr)
        return 1
    try:
        server, active_port = bind_server()
    except Exception as e:
        print(f"STARTUP ERROR: {e}", file=sys.stderr)
        return 1
    try:
        PID_FILE.write_text(str(os.getpid()) + "\n")
    except Exception as e:
        print(f"WARNING: could not write PID file: {e}", file=sys.stderr)
    url = f"http://{HOST}:{active_port}/"
    print("HEXCAT HCX UI v.IV")
    print(f"Local only: {url}")
    if active_port != PORT:
        print(f"Port {PORT} was busy; using {active_port} instead.")
    print(f"Hashcat: {HASHCAT}")
    print(f"HCX: {HCXPCAPNGTOOL}")
    threading.Timer(0.7, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        try:
            if PID_FILE.exists() and PID_FILE.read_text().strip() == str(os.getpid()):
                PID_FILE.unlink()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
