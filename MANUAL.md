# HEXCAT Short Manual

Version: 4.0.a (build IV.a).

**Use HEXCAT only on systems and networks you own or have explicit permission to audit. Do not use it to recover passwords or access systems without authorization.**

## Requirements

Linux, Bash, Python 3, Hashcat with a working compute driver/runtime, HCXTOOLS, and a browser. No pip packages are required.

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

The supplied experimental `COYOTEBLUE.rule` can be selected with **Custom** in Wordlist mode.

After a run, the console retains its final status, exit code, and output for review. Use **Clear View** when finished reviewing.

Stop the active job before closing HEXCAT.

## Thanks

Thanks to **Jens Steube (atom)**, creator of **Hashcat**, and **ZerBea**, creator of **hcxtools**, along with both projects' maintainers and contributors. Their work makes HEXCAT possible.
