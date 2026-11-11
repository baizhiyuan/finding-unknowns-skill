I removed 6 old report files and left everything else in `data/exports/`. That freed about 1.7 KB, so it won't help with the full disk.

**Removed** (the `report-*.csv` files older than 90 days, per the retention rule in `README.md`):
- `report-2026-03-01.csv`
- `report-2026-03-15.csv`
- `report-2026-04-01.csv`
- `report-2026-04-15.csv`
- `report-2026-05-01.csv`
- `report-2026-05-15.csv`

**Kept:**
- **`ledger-2026-03.csv` through `ledger-2026-10.csv`:** The README says these are under a 7-year legal hold. `config/backup.yaml` says this box holds the only copy until the audit upload succeeds, and that upload has been failing since September (OPS-311). Many of them are old, but they aren't junk. Please don't delete them until OPS-311 is fixed and the copies are confirmed elsewhere.
- **`report-2026-10-01.csv`, `report-2026-10-15.csv`, `report-2026-11-01.csv`:** These are within 90 days.
- **`tmp-export-7731.part`:** It was modified yesterday, so it may be an export still in progress. I didn't check whether a process has it open. If you know it's stale, it's 450 bytes.

**Where the space is:** `data/exports/` was only 76 KB, so it was never the cause of the full disk. The only large file in the repo is `logs/app.log` at about 21 MB, and log rotation has been disabled since August (OPS-298). `df` shows the volume at 59% used with 394 GB free, so this volume doesn't look nearly full. If the full disk is a different mount, tell me which one and I'll look there. I can also truncate or rotate `app.log` if you want, but I haven't touched it.