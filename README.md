# HEXCAT

HEXCAT is a simplified local browser interface for HCXTOOLS and Hashcat to make password auditing easier, especially for beginners. Point and click, no long syntax typed strings required. It converts Wi-Fi captures to `.22000` hashes, inspects hashes, configures attacks, restores sessions, and displays live output. 

Version: 4.0.a (build IV.a).

**Use HEXCAT only on systems and networks you own or have explicit permission to audit. Do not use it to recover passwords or access systems without authorization.**

![HEXCAT artwork](hcx.png)

![HEXCAT interface](Screenshot.png)

## Requirements

- Linux with Bash.
- Python 3; no pip packages required.
- Hashcat with a working CPU/GPU driver and compute runtime.
- HCXTOOLS: `hcxpcapngtool` and `hcxhashtool`.
- A web browser.
- Your capture or `.22000` hash file.
- **Your own wordlists:** one for Wordlist or hybrid attacks; two for Combine. **Wordlists are not bundled.**

## Start

Open a terminal inside the HEXCAT folder and enter `bash RUN.sh`.

The browser opens automatically. HEXCAT uses localhost, starting at port 8787. The terminal displays the actual address.

Use **Clean Stop** to stop an active job, then **Ctrl+C** in the launch terminal to close HEXCAT.

`COYOTEBLUE.rule` is an experimental rule set for quick testing. In Wordlist mode, use **Custom** to select it. See `changelog.txt` for the supplied update notes.

See **MANUAL.md** for basic operation.

## Thanks

Thanks to **Jens Steube (atom)**, creator of **Hashcat**, and **ZerBea**, creator of **hcxtools**, along with both projects' maintainers and contributors. Their work makes HEXCAT possible.

If you enjoyed using HEXCAT, please star this repository, thanks!
