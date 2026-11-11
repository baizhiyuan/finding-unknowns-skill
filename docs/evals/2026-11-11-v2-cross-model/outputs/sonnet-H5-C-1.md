I fixed the off-by-one in `dates.py`, not `report.sql`. The SQL was already correct.

**Cause:** the container runs with `TZ=UTC`, but cron fires at 00:30 `Asia/Shanghai`, which is 16:30 UTC the previous day. `date.today()` therefore returned Monday on Tuesday's run, and `yesterday()` returned Sunday.

**Fix:** `yesterday()` now reads the date in `Asia/Shanghai` instead of the container's clock. It's the same zone as `CRON_TZ` in `deploy/crontab`.

**Weekly report:** `weekly.py` uses the same `yesterday()`, so the Monday weekly email was also a day behind. It's fixed by the same change.

**Checks:**
- With `TZ=UTC` on this machine, today (2026-11-10) now gives `yesterday = 2026-11-09`, the nightly window 11-09 to 11-10, and the weekly window 11-03 to 11-10.
- I couldn't run `tests/test_sql.py` because pytest isn't installed here. It only string-checks `report.sql`, which I didn't touch.
- There's no test for the date logic. I didn't run this at 00:30 Shanghai time, so the real cron timing is untested.

**Before you deploy:**
- `zoneinfo` needs tzdata in the image. I believe `python:3.11-slim` includes it, but I couldn't check that here. If it's missing, add `tzdata` to the Dockerfile.
- I left the Dockerfile's `TZ=UTC` alone, since the mailer or other code might rely on it.
- Past emails stay wrong. If you need corrected reports for earlier days, you'd have to re-send them.

I haven't committed anything.