# HEXCAT

HEXCAT is a simplified local browser interface for HCXTOOLS and Hashcat to make password auditing easier, especially for beginners. Point and click, no long syntax typed strings required. It converts Wi-Fi captures to `.22000` hashes, inspects hashes, configures attacks, restores sessions, and displays live output. 

Build: IV.

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

See **MANUAL.md** for basic operation. Use only with captures and networks you are authorized to test.
If you enjoyed using HEXCAT, please star this repository, thanks!
buymeacoffee.com/aethercat
