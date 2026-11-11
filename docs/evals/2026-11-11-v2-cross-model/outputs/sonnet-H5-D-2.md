The fix is in `dates.py`, not `report.sql`. I haven't run the repo's test because pytest isn't installed here. That test only checks the SQL text, which I didn't change.

`yesterday()` now computes the date in `Asia/Shanghai` instead of using the container's clock. I checked it with a UTC time of 16:30 on Nov 10, which is 00:30 on Nov 11 in Shanghai. It returns Nov 10, the day that just ended. Before, it would have returned Nov 9.

`weekly.py` also calls `yesterday()`, so the Monday report had the same problem and is fixed by this change. It was probably covering the week ending Saturday instead of Sunday.

I didn't touch the Dockerfile or crontab. Debian's default cron may ignore `CRON_TZ`, and I didn't check the cron setup in the image. If it does ignore it, the job would fire at 00:30 UTC, which is 08:30 Shanghai. The date logic would still be correct, but the email would arrive later than intended.

I also couldn't invoke the `finding-unknowns` skill from your CLAUDE.md, because it isn't installed in this environment. I haven't committed anything.