I fixed the one-day lag in `dates.py`, not `report.sql`. I haven't run it under the production cron setup. The `yesterday()` call returns the right date locally, but pytest isn't installed here, so the test suite didn't run. The one test only checks that `report.sql` has the `>= :start` and `< :end` clauses, so it doesn't exercise this fix.

**Cause:** `report.sql` has the right half-open date filter. The dates handed to it were wrong. `deploy/crontab` sets `CRON_TZ=Asia/Shanghai`, which only controls when the job fires. The Docker image sets `TZ=UTC`, so `date.today()` in `dates.py` used UTC. At 00:30 Tuesday in Shanghai it is still Monday 16:30 UTC, so `yesterday()` returned Sunday.

**Fix:** `yesterday()` now takes today's date in `Asia/Shanghai` explicitly instead of the container's local time. I added a comment saying it must match `CRON_TZ`. The check above returned `2026-11-09`, which is correct for the current Shanghai date.

**Weekly report:** `weekly.py` also calls `yesterday()`, so the Monday report was probably a day behind too, and this change fixes it.

**Docker image:** `zoneinfo` needs tz data in the image. I believe `python:3.11-slim` ships it, but I haven't confirmed that. If the container raises a `ZoneInfoNotFoundError`, add `tzdata` to the image's pip dependencies.

I haven't committed anything.