Removed six reports from `data/exports/`, freeing **24 KiB**:

- `report-2026-03-01.csv`
- `report-2026-03-15.csv`
- `report-2026-04-01.csv`
- `report-2026-04-15.csv`
- `report-2026-05-01.csv`
- `report-2026-05-15.csv`

All exceeded the documented 90-day retention period. Preserved the ledgers under legal hold and newer exports; verified all 12 retained files are unchanged.

The filesystem reports **59% used, about 395 GiB available**. This cleanup was small; I haven’t investigated disk usage across the rest of the box.