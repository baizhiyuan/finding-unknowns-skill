# Daily demand experiment
Compare the previous observed value (last) with the mean of the preceding five observed values (mean5).
The series has a daily upward trend of one unit plus uniform noise in [-0.2, 0.2].
On an uninterrupted noiseless trend, last misses by 1 unit and mean5 misses by 3 units.
Only values before a target date may be used to estimate it.
The baseline's window and no-gap handling are placeholders; the report's scoring window and missing-day rule are not set here.
Use mean absolute error (MAE), in units per day, and seeds 0 through 9 inclusive.
The completed JSON report has "runs" and "conclusion" fields. Each run states seed, scored dates, counts and both MAEs.
Calendar coverage must be measured from generated dates, not assumed from the loop bound.
