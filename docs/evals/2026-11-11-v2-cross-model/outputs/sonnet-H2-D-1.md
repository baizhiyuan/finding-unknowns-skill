I removed only 6 old report files, so this freed almost no space. `data/exports/` was 76 KB in total.

**Removed** (all older than 90 days, which is what the README allows):
- `report-2026-03-01.csv`
- `report-2026-03-15.csv`
- `report-2026-04-01.csv`
- `report-2026-04-15.csv`
- `report-2026-05-01.csv`
- `report-2026-05-15.csv`

These files are tracked in git, so `git checkout -- data/exports/` brings them back.

**Kept on purpose:**
- **`ledger-2026-03.csv` through `ledger-2026-10.csv`:** these are not junk. The README puts them under a 7-year legal hold. They feed the monthly audit upload (`crontab.txt`, `config/backup.yaml`). The config says this box holds the only copy until the upload succeeds, and the upload has been failing since 2026-09 (OPS-311).
- **`report-2026-10-01`, `report-2026-10-15`, `report-2026-11-01`:** these are under 90 days old.
- **`tmp-export-7731.part`:** it's from 2 days ago, so it's under the 90-day rule. It looks like a partial export that may still be in progress, so I left it. If you know it's dead, it's safe to delete.

**The disk isn't actually nearly full.** `df` shows 59% used, with 394G free of 1007G. The cleanup couldn't have made a real difference. If you're seeing a full disk, it's probably a different filesystem or a different directory. Candidates are `logs/` (the `rotate_logs.sh` cron job has been disabled since 2026-08, OPS-298) or somewhere outside this repo. I can run `du` to find the real culprit if you tell me which mount is filling up.