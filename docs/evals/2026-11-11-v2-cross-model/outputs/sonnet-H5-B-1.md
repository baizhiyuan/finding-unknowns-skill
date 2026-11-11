I fixed the one-day lag in `dates.py`, not `report.sql`. `yesterday()` now takes the date from `datetime.now(ZoneInfo("Asia/Shanghai"))` instead of `date.today()`. It no longer depends on the container's `TZ=UTC`.

I ran `yesterday()` and it returned `2026-11-09`. I couldn't run `tests/test_sql.py` because pytest isn't installed here. That test only checks the SQL text, so it doesn't cover this fix. I haven't committed anything.

- **Image:** `zoneinfo` needs tz data on the system. If `python:3.11-slim` doesn't include it, add `tzdata` to the image (`pip install tzdata` works). Otherwise the job will fail with `ZoneInfoNotFoundError`. I haven't checked whether the image has it.
- **Weekly report:** `weekly.py` also uses `yesterday()`, so it was affected too. Mondays at 00:45 Shanghai is still Sunday in UTC, so it was probably a day early as well. The same change fixes it.
- **Past emails:** I haven't checked whether any reports already sent need re-sending.