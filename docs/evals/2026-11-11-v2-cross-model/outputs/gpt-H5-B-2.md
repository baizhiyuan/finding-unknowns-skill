Fixed [dates.py](/tmp/fu-eval2/runs/gpt-H5-B-2/nightly-report/dates.py): it now calculates yesterday in `Asia/Shanghai`.

The UTC container was still on Monday when Tuesday’s email ran, causing it to select Sunday. `report.sql` handled the supplied bounds correctly.

All 12 date regression scenarios and the existing SQL test pass, including weekly reports, leap day, and year rollover.