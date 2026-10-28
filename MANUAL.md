# HEXCAT Short Manual

Version: IV.k — final Version IV release.

**THIS IS THE FINAL VERSION OF HEXCAT IV. HEXCAT V IS COMING SOON.**

**Use HEXCAT only on systems and networks you own or have explicit permission to audit. Do not use it to recover passwords or access systems without authorization.**

## Requirements

Linux, Bash, Python 3, Hashcat with a working compute driver/runtime, HCXTOOLS, and a browser. No pip packages are required.

Native file selection uses Zenity, KDialog, or Python's Tkinter fallback.

Supply your own capture or `.22000` file and any required wordlists. **Wordlists are not included.**

## Basic operation

1. Start HEXCAT using `bash RUN.sh` from its folder, or launch directly with `python3 HEXCAT4b.py`. Keep the Python file, matching HTML file, and `hcx.png` together.
2. Under **Capture → HCX Extract**, select a capture and output path, then click **Extract .22000**.
3. Select the hash file and click **Inspect Hashes**.
4. Choose an attack:
   - **Wordlist:** one wordlist; optionally a rule file.
   - **Combine:** two wordlists.
   - **Mask:** a typed candidate pattern, quick-mask preset, or custom `.hcmask` file.
   - **Word + Mask / Mask + Word:** one wordlist plus a pattern.
5. Review the command preview and click **Run Hashcat**.
6. Follow native Hashcat output in **LIVE OUTPUT** and the parsed summary in **HEXCAT LIVE STATUS**.

**Clean Stop** requests a clean stop. **Hard Stop** forcibly ends the job. **Restore Session** resumes an existing saved session using its original name. **Show Recovered** displays recovered results. **GPU / Backend Info** lists compute devices.

The supplied experimental `COYOTEBLUE.rule` can be selected with **Custom** in Wordlist mode.

## Rules and masks

In **Wordlist** mode, choose **No rule**, select an installed rule, or use **Custom** to select a `.rule` file. The selected custom rule's filename and path are displayed. Combine and hybrid modes provide optional inline `-j` and `-k` transformations.

In **Mask** mode, type a pattern, select a quick-mask preset, or use **Browse** under **Custom mask file** to select a `.hcmask` file. Its filename and full path are displayed, and it becomes the active mask source. Selecting a quick-mask preset clears the custom-mask selection.

Quick masks include **8 digits**, **10 digits**, **8 lower**, **Capital + 5 lower + 2 digits**, **8 alnum**, and **10 lower+digits**. For the WPA/WPA2 `.22000` workflow, use password lengths of 8 characters or greater.

Advanced mask controls provide four custom character sets, incremental lengths, and a **Disable Markov** option. Review the command preview before starting.

## Sessions, recovery, and devices

Use a named session when you intend to restore a run later. **Restore Session** uses the original session name. Optional fields let you choose a potfile and a recovered-output file. **Show Recovered** retrieves results through Hashcat's potfile workflow, and recovered passwords have a dedicated display.

Use **GPU / Backend Info** to inspect available compute devices. The attack builder also provides device selection, workload, optimized-kernel, temperature-abort, and runtime controls.

## Live status and output

**HEXCAT LIVE STATUS** reports target ESSID, AP BSSID, STA/client MAC, status, progress, attack stage, active wordlist, mask and rule, ETA, speed, recovered counts, candidates, and GPU temperature when available from the current hash material and Hashcat output. Progress includes an ASCII bar and percentage.

Use **COPY** to copy the terminal display. Automatic scrolling follows new output while you are near the bottom; scroll upward to inspect earlier output without being pulled back down.

After a run, the console retains its final status, exit code, and output for review. Use **Clear View** when finished reviewing.

Stop the active job before closing HEXCAT.

See [CHANGES.md](CHANGES.md) for the full project history through IV.k and [README.md](README.md) for the project overview.

## Thanks

Thanks to **Jens Steube (atom)**, creator of **Hashcat**, and **ZerBea**, creator of **hcxtools**, along with both projects' maintainers and contributors. Their work makes HEXCAT possible.
