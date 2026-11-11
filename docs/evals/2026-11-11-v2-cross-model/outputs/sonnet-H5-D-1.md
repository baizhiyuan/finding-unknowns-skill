I fixed the lag in `dates.py`, not `report.sql`. The SQL's date filter was already right. I haven't committed anything.

**Cause:** `yesterday()` used `date.today()`, which follows the container's timezone. The Dockerfile sets `TZ=UTC`, but the cron job runs at 00:30 Asia/Shanghai, which is 16:30 UTC the previous day. On Tuesday's run the container still thought it was Monday, so "yesterday" came out as Sunday.

**Fix:** `yesterday()` now computes the date in `Asia/Shanghai` explicitly, so it no longer depends on the container's `TZ`.

**Checks:** I ran `nightly.params()` and `weekly.params()` on this machine and the dates came out right. I couldn't run pytest because it isn't installed here. The existing test only checks the SQL text, so it doesn't cover this bug.

**Things to know:**
- **Weekly report:** It was wrong in the same way and is fixed by this change. It runs Monday 00:45 Shanghai, which is still Sunday in UTC, so the "week ending yesterday" window was shifted a day early.
- **Container timezone:** `zoneinfo` needs tzdata in the image. `python:3.11-slim` normally includes it, but I couldn't check the image here. If it's missing, the job will fail with a `ZoneInfoNotFoundError`, and you'd need to add the `tzdata` package.
- **Past emails:** I haven't looked at the earlier reports. Any sent so far had the wrong day's data.
- **Deploy:** The change only takes effect once the image is rebuilt and deployed.