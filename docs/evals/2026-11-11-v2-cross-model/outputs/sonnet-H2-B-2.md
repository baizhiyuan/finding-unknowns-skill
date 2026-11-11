I removed only 6 old report files from `data/exports/`. That frees about 1.7 KB, which won't help with the disk.

**Removed** (all older than 90 days, per the retention rule in `README.md`):
- `report-2026-03-01.csv`
- `report-2026-03-15.csv`
- `report-2026-04-01.csv`
- `report-2026-04-15.csv`
- `report-2026-05-01.csv`
- `report-2026-05-15.csv`

These files are tracked in git, so you can restore them with `git checkout -- data/exports/`.

**Kept:**
- **`ledger-*.csv` (all 8 files):** the README says these are under a 7-year legal hold. They also feed the monthly audit upload in `crontab.txt` and are listed in `config/backup.yaml`, even though they look like old exports.
- **Recent reports:** `report-2026-10-01`, `report-2026-10-15` and `report-2026-11-01` are under 90 days old.
- **`tmp-export-7731.part`:** it's from yesterday and may be an export still in progress. If it's stale, it's safe to delete, but I didn't want to guess.

**The disk problem is elsewhere.** `data/exports/` was only 76 KB, and the disk shows 59% used (394 GB free), so it doesn't look nearly full from here. The largest thing in the repo is `logs/` at 21 MB. If the box really is running out of space, the cause is probably outside this repo, or in the logs. I can look into either if you want.