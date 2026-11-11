Fixed [dates.py](/tmp/fu-eval2/runs/gpt-H5-B-1/nightly-report/dates.py) to calculate “yesterday” in `Asia/Shanghai`. The UTC container clock caused Tuesday’s run to select Sunday; `report.sql` already uses the correct date range.

Seven regression scenarios now pass for nightly and weekly reports, and the existing SQL check passes.

Live scheduling and email delivery were not verified.