I fixed the one-day-too-early date in `dates.py`, not `report.sql`. I haven't run it at the 00:30 Shanghai boundary where the bug shows up, and I haven't run the test.

**What was wrong:** the cron job fires at 00:30 Shanghai time, but the container runs in UTC (`ENV TZ=UTC` in the Dockerfile). At that moment it's still 16:30 the previous day in UTC. `yesterday()` was therefore a day too early. Tuesday's email got Sunday's data. The Monday weekly report had the same off-by-one, ending on Saturday instead of Sunday.

**The fix:** `yesterday()` now takes "today" in `Asia/Shanghai` instead of the container's clock. I left `report.sql` alone because its date filter is correct.

**Checks:**
- **Run:** `dates.yesterday()` returns 2026-11-09 here, and so does a UTC-based calculation. That's expected, since it's midday UTC now and both clocks are on the same date. The two only differ between 16:00 and 24:00 UTC.
- **Not run:** `pytest` isn't installed here, so I didn't run `tests/test_sql.py`. It only checks the SQL text, which I didn't touch.

**Before you deploy:**
- The timezone name is hardcoded in `dates.py` and has to match `CRON_TZ` in `deploy/crontab`.
- `zoneinfo` needs timezone data in the image. I believe `python:3.11-slim` includes it, but I haven't built the image. Adding `tzdata` to your pip requirements is a cheap safeguard.

I haven't committed anything.