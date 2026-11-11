Fixed the cause in [dates.py](/tmp/fu-eval2/runs/gpt-H5-A-2/nightly-report/dates.py): it now calculates yesterday in Shanghai time. At Tuesday’s 00:30 run, UTC was still Monday, causing Sunday to be selected.

Added container timezone data and regression tests. Nightly, weekly, calendar-boundary, and SQL-bound checks pass.

Rebuild and redeploy the container to apply the fix.