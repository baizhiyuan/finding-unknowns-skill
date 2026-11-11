I couldn't save the write-up to a file because the Write tool is disabled in this session, so it's below. I recommend we don't ship.

# ranker-v7 vs ranker-v6: launch review

CTR rose from 3.10% to 3.41% (+10.0% relative, p = 0.03). The plan approved on 2026-10-12 made CTR a secondary, diagnostic metric, not the ship criterion. The plan's ship rule fails on two counts.

| Requirement | Result | Pass? |
|---|---|---|
| Primary metric (revenue per session) significantly positive at alpha 0.05 | 4.82 → 4.76 (−1.2%), p = 0.21 | **No** |
| Guardrail: p95 latency rises by at most 20 ms | 212 → 250 ms (+38 ms), p < 0.001 | **No** |

The plan says that anything else means don't ship and write it up as a learning.

## Why the CTR win shouldn't be trusted

1. **The lift fades to about zero.** Treatment CTR was 3.85% on days 1–3, 3.65% on days 4–7 and 3.12% on days 8–14. Control stayed at 3.10% throughout. The 3.41% figure is a 14-day average weighted toward the early days. By the last week the lift is about +0.02 points, which looks like a novelty effect. The steady-state gain is probably about 0, and revenue didn't move either.
2. **The sample ratio is wrong.** The plan specifies a 50/50 split, but assignment was 52,310 control to 47,690 treatment. That gives a chi-square of about 213 on 1 degree of freedom, so p is effectively 0. This is not chance. Assignment or logging is broken somewhere, possibly differential drop-out in treatment tied to the latency regression. Until that's explained, none of the treatment-vs-control comparisons are reliable, including the CTR p-value.
3. **There are many comparisons.** `metrics.csv` lists 20 metrics. One p = 0.03 among them, uncorrected, is weak evidence. A Bonferroni correction across 20 would need p < 0.0025.
4. **Much of `metrics.csv` looks like filler.** From `add_to_cart_rate` down, control values step 1.00, 1.10, 1.20, …, treatment is control + 0.003, and the p-values rise in steps of 0.04. Control CTR is also exactly 3.10 on all 14 days. Those rows should be regenerated before anyone cites them.

## Recommendation

- **Don't ship ranker-v7 as is.**
- **Find the cause of the sample ratio mismatch first.** It's a validity problem that could change every result.
- **Look at the +38 ms p95 latency.** If it can be fixed, a re-test may be worth it.
- **Agree on the success metric before the next run.** If CTR is what we care about, decide that up front. Use a longer window or a holdout so a novelty effect can be separated from the steady-state effect.
- **Report a confidence interval for revenue.** At −1.2% (p = 0.21), the test can't rule out a real revenue loss.

## Caveats

- I only had the summary files in `results/`, not the raw event data. I didn't recompute any p-values. The chi-square is my own calculation from `assignment.csv`.
- `results/summary.md` (auto-generated 2026-10-28) reports only the CTR result. It leaves out the primary metric and the latency guardrail, which is probably why this looked like a win.

If you want this saved as `launch_review.md`, tell me and I'll write it once file writing is available.