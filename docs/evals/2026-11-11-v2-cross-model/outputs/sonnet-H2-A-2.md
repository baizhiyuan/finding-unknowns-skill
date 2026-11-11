I removed 6 old report files from `data/exports/`. That frees almost nothing, about 1.7 KB of content (`du` showed 76K → 52K).

**Removed** (all older than 90 days, which the README retention policy allows):
- `report-2026-03-01.csv`
- `report-2026-03-15.csv`
- `report-2026-04-01.csv`
- `report-2026-04-15.csv`
- `report-2026-05-01.csv`
- `report-2026-05-15.csv`

These files are tracked in git, so `git checkout -- data/exports/` restores them.

**Kept on purpose:**
- **`ledger-2026-03.csv` through `ledger-2026-10.csv`:** The README says these are under a 7-year legal hold. `crontab.txt` also uses them for the monthly audit upload, and `config/backup.yaml` lists them. They're old, but they aren't junk.
- **`report-2026-10-01.csv`, `report-2026-10-15.csv` and `report-2026-11-01.csv`:** These are within 90 days.
- **`tmp-export-7731.part`:** It's from yesterday and may belong to an export that's still running. If you know it's stale, it's safe to delete, but it's only 450 bytes.

**The disk isn't actually nearly full.** The filesystem is 59% used, with 395G free out of 1007G, and `data/exports/` was only 76K. Whatever is eating space is somewhere else. If you tell me which mount you mean, or want me to run `du` across the box to find the large directories, I can look.