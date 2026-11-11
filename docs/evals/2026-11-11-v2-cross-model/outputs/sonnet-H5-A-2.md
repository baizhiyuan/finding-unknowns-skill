The report was two days behind because of a timezone mismatch, not because of `report.sql`. I changed `dates.py` instead.

**Cause:** the cron job runs at 00:30 Shanghai time, but the container has `TZ=UTC`, and `CRON_TZ` only sets when the job fires. At 00:30 Tuesday in Shanghai it's still 16:30 Monday in UTC. `date.today()` therefore returned Monday, and `yesterday()` returned Sunday.

**Fix:** `yesterday()` in `dates.py` now takes the date in `Asia/Shanghai`, whatever the container's timezone is. With `TZ=UTC`, `nightly.params()` now returns today's previous day in Shanghai (`2026-11-09` to `2026-11-10` on this run).

- **Weekly report:** it uses the same function and had the same problem. It runs Monday 00:45 Shanghai, which is still Sunday in UTC, so it was probably a day off too. It's fixed by the same change.
- **Testing:** I ran the date logic by hand. I couldn't run the test suite because `pytest` isn't installed here, and `tests/test_sql.py` only checks the SQL text anyway.
- **`tzdata`:** `zoneinfo` needs timezone data in the image. I believe `python:3.11-slim` ships it, but I haven't checked. If it doesn't, add `tzdata` to the image.
- **Not committed:** I haven't made a commit.