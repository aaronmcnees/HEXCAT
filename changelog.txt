# HEXCAT — CHANGELOG

## I → II → III

The first three HEXCAT generations established the project and evolved the original HCX/Hashcat wrapper concept into the standalone local control surface that became Version IV.

These early builds established the core direction:

- Local Linux operation.
- HCXTOOLS / `hcxpcapngtool` integration.
- Hashcat integration for `.22000` WPA/WPA2 material.
- Capture conversion and hash inspection.
- Browser-based control instead of requiring the entire workflow to be entered manually in a terminal.
- Native file selection.
- Attack construction from the UI.
- Live Hashcat command/output visibility.
- The project identity ultimately standardized as **HEXCAT**.

---

# IV

Version IV became the first mature standalone HEXCAT generation.

### HCX workflow

- PCAP / PCAPNG / CAP conversion to Hashcat `.22000`.
- HCX extraction controls.
- Hash inspection through HCXTOOLS.
- Output-path selection.
- Optional HCX sidecar outputs and extraction flags.

### Hashcat Attack Builder

Five primary attack modes were established:

- **WORDLIST**
- **COMBINE**
- **MASK**
- **WORD + MASK**
- **MASK + WORD**

### Rules and masks

- Hashcat `.rule` support for straight attacks.
- Inline `-j` and `-k` transformations for applicable combination/hybrid attacks.
- Four custom mask charsets.
- Incremental mask support.
- Markov control.
- Quick-mask presets.
- Workload selection.
- Optimized-kernel option.
- Temperature abort control.
- GPU/device selection.

### Sessions and recovery

- Named Hashcat sessions.
- Session restore.
- Potfile selection.
- Recovered-output file support.
- **Show Recovered** control.
- GPU/backend information.

### Runtime control

- Live Hashcat output.
- Full command preview.
- Clean Stop.
- Hard Stop.
- Clear View.
- Localhost-only browser interface.

Version IV established the architecture that the remaining IV revisions refined rather than replaced.

---

# IV.a

Version IV.a concentrated on **completion handling and output retention**.

- Fixed Hashcat completion handling.
- Normal Hashcat exit was no longer treated as an error or teardown condition.
- Preserved the final Hashcat status.
- Added permanent end-of-run information:
  - `FINAL STATUS`
  - `PROCESS EXIT CODE`
  - `OUTPUT RETAINED`
- Hashcat terminal output remained visible after completion or exhaustion.
- HEXCAT remained running after an attack completed.
- Output remained available until **Clear View** or another run replaced it.
- Existing potfile recoveries were correctly recognized as completed results.
- Added an experimental rule set for testing.
- Documentation and attribution were updated.
- Version identity advanced to **IV.a / 4.0.a**.

---

# IV.b → IV.j

These revisions formed the main **IV refinement cycle**.

The surviving development history does not preserve a trustworthy one-to-one mapping of every individual change to every letter from IV.b through IV.j, so the changes are recorded here as the chronological refinement cycle rather than assigning invented version numbers to individual edits.

### Custom mask files

- Added native custom `.hcmask` support.
- Added `.hcmask` file selection.
- Displayed the selected custom-mask filename.
- Displayed the selected mask's full path.
- Custom mask state was cleared appropriately when switching back to typed or preset masks.
- Selecting a custom mask made that mask file the active attack source.

### Rule handling

- Improved installed-rule selection.
- Improved custom `.rule` selection.
- Displayed custom rule filename and path.
- Clearly distinguished:
  - No rule
  - Installed rule
  - Custom rule
- Preserved Hashcat 7.1.2 straight-mode rule behavior.
- Preserved inline transformations for the attack modes that use them.

### Recovered-password handling

- Improved detection and presentation of recovered passwords.
- Added the dedicated cracked-password result display.
- Preserved the large high-visibility password presentation separately from raw terminal output.
- Successful results could be retrieved through the normal Hashcat potfile workflow without destroying the terminal record.

### Terminal controls

- Added terminal-output copy support.
- Preserved native Hashcat output rather than replacing it with a simplified display.
- Improved end-of-run behavior.
- Preserved exhausted, cracked, stopped and completed attack output.
- **Clear View** remained the explicit action for removing output from the display.

### HEXCAT LIVE STATUS

Added the simplified **HEXCAT LIVE STATUS** section beneath the real Hashcat terminal output.

The block reports:

- TARGET / ESSID
- AP BSSID
- STA / client MAC
- STATUS
- PROGRESS
- STAGE
- WORDLIST
- MASK
- RULE
- ETA
- SPEED
- RECOVERED
- CANDIDATES
- GPU temperature

### Progress presentation

- Added an ASCII progress bar.
- Added percentage display.
- Added attack-stage reporting.
- Added active wordlist reporting.
- Added active mask reporting.
- Added active rule reporting.
- Added speed and recovered-count parsing.
- Added candidate display.
- Added GPU-temperature reporting.

### Target intelligence

- Added ESSID / target extraction.
- Added AP MAC extraction.
- Added client / STA MAC extraction.
- Added fallback target parsing from HEXCAT capture/hash filenames.

### Parser hardening

Fixed real-world Hashcat parsing problems found during testing:

- TARGET / ESSID no longer appearing blank.
- AP and STA metadata parsing.
- `STAGE` failing to display.
- Single-stage attacks now correctly displaying `1 / 1 (100.00%)`.
- Long Hashcat ETA values preserved correctly.
- `Next Big Bang` no longer being mangled into a bogus clock value.
- Multi-day/hour/minute/second ETA handling improved.

### Terminal scrolling

- Fixed live polling constantly dragging the terminal back to the bottom.
- Automatic following continues while the user is already near the bottom.
- Scrolling upward now allows earlier Hashcat output to be inspected without fighting the UI.
- Reduced unnecessary blank lines in the live display.

Throughout these revisions the original five attack modes and the core IV workflow remained intact.

---

# IV.k

IV.k is the final refinement of the Version IV generation.

### Quick masks

Retained the existing quick-mask collection and added:

- **10 digits**
- `?d?d?d?d?d?d?d?d?d?d`

The existing:

- **8 digits**
- **8 lower**
- **Capital + 5 lower + 2 digits**
- **8 alnum**
- **10 lower+digits**

presets remain available.

For the WPA/WPA2 `.22000` workflow, mask work remains focused on valid password lengths of **8 characters or greater**.

### Final footer

The footer was expanded to include the authorized-use warning, creator acknowledgments, HEXCAT ownership information and the complete project-version lineage.

**With gratitude to Jens Steube (atom), creator of Hashcat, and ZerBea, creator of hcxtools / hcxpcapngtool**

**HEXCAT by Aethercat / CoyoteLabs · © 2026 Aethercat / CoyoteLabs**

**I → II → III → IV → IV.a → IV.b → IV.c → IV.d → IV.e → IV.f → IV.g → IV.h → IV.i → IV.j → IV.k**

### Final IV architecture

HEXCAT IV.k therefore closes the Version IV line with:

- HCX capture conversion.
- Hash inspection.
- Five Hashcat attack modes.
- Wordlists.
- Combination attacks.
- Masks.
- Hybrid attacks.
- `.rule` support.
- `.hcmask` support.
- Custom charsets.
- Sessions and restore.
- Potfile recovery.
- GPU/backend controls.
- Raw Hashcat output.
- Persistent final output.
- Dedicated cracked-password presentation.
- Copyable terminal output.
- HEXCAT LIVE STATUS.
- Target/AP/STA identification.
- ASCII progress reporting.
- Stage, ETA, speed, candidate and GPU monitoring.
- Quick-mask presets.
- Localhost-only control.
- Authorized-use warning and creator attribution.

**THIS IS THE FINAL VERSION FOR IV, VERSION V WILL USE HASHCAT 8.X**
