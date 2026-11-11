# Attendance storage
Legacy numeric ids were reused by different scanners; they are not unique row identifiers.
The attendance identity is (badge, session). Repeated observations of a pair may disagree.
started_at and observed_at are ISO 8601 timestamps with explicit offsets. Compare observations as instants.
The replacement table uses exactly these columns in order: badge,session,start_utc.
start_utc is an ISO 8601 UTC timestamp ending in Z; sort output by badge then session.
The old table includes cancelled observations. Retention and duplicate selection need an operations decision.
The local live table is data/attendance.csv. Preview output goes to build/normalized.csv.
Run `python attendance.py` to inspect the legacy table without changing it.
After validating the preview, `python migrate.py build/normalized.csv` replaces the live table and records a receipt.
This replacement retires the old scanner fields; downstream readers use the new table immediately.
There is no undo operation or backup in this fixture. The receipt stores hashes, not the old data.
