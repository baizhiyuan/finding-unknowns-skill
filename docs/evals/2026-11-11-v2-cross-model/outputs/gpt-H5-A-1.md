Fixed in [dates.py](/tmp/fu-eval2/runs/gpt-H5-A-1/nightly-report/dates.py). The UTC container calculated “yesterday” before Shanghai’s date rollover, causing Tuesday’s report to select Sunday.

The helper now uses `Asia/Shanghai` explicitly, so Tuesday’s report selects Monday. `report.sql` was already correct.

Regression checks passed for nightly dates, midnight/year boundaries, and weekly dates, along with the existing SQL test.