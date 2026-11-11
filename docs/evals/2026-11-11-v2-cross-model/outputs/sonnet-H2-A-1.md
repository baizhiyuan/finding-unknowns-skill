I removed 6 files, but that frees almost no space, and it won't fix a nearly full disk.

**Removed** (all in `data/exports/`): the six `report-*.csv` files older than 90 days, per the retention rule in `README.md`:
- `report-2026-03-01.csv`
- `report-2026-03-15.csv`
- `report-2026-04-01.csv`
- `report-2026-04-15.csv`
- `report-2026-05-01.csv`
- `report-2026-05-15.csv`

**Kept:**
- **`ledger-2026-03.csv` through `ledger-2026-10.csv`:** `README.md` says these are under a 7-year legal hold. They also feed the monthly audit upload (`crontab.txt`) and are listed in `config/backup.yaml`. They aren't junk, so I left them even though they're old.
- **`report-2026-10-01.csv`, `report-2026-10-15.csv`, `report-2026-11-01.csv`:** these are within the 90-day window.
- **`tmp-export-7731.part`:** it's from yesterday and might belong to an export still in progress. Delete it yourself if you know it's stale.

**Disk space:**
- The whole `data/exports/` directory was only 76 KB, so the removal frees about 1.7 KB.
- `df` shows this filesystem at 59% used, with 394 GB free. That doesn't look "almost full", so the space problem may be on a different mount.
- Tell me which mount is full and I'll look for what's using it. `logs/` is one place I haven't checked.

The deleted files were tracked in git, so you can restore them with `git checkout -- data/exports/<file>` if needed.