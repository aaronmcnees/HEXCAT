# HEXCAT Short Manual

## Requirements

Linux, Bash, Python 3, Hashcat with a working compute driver/runtime, HCXTOOLS, Zenity, procps, and a browser. No pip packages are required.

Supply your own capture or `.22000` file and any required wordlists. **Wordlists are not included.**

## Basic operation

1. Start HEXCAT using `bash RUN.sh` from its folder.
2. Under **Capture → HCX Extract**, select a capture and output path, then click **Extract .22000**.
3. Select the hash file and click **Inspect Hashes**.
4. Choose an attack:
   - **Wordlist:** one wordlist; optionally a rule file.
   - **Combine:** two wordlists.
   - **Mask:** a candidate pattern.
   - **Word + Mask / Mask + Word:** one wordlist plus a pattern.
5. Review the command preview and click **Run Hashcat**.
6. Follow progress in **LIVE OUTPUT**.

**Clean Stop** requests a clean stop. **Hard Stop** forcibly ends the job. **Restore Session** resumes an existing saved session using its original name. **Show Recovered** displays recovered results. **GPU / Backend Info** lists compute devices.

Stop the active job before closing HEXCAT.
