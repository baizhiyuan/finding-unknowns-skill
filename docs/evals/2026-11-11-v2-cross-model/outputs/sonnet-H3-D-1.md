I couldn't save the write-up to a file because the Write tool is disabled in this session, so it's below. I haven't committed anything.

# ranker-v7 vs ranker-v6: launch review

**Recommendation: do not ship.** Two of the criteria pre-registered in `experiment_plan.md` fail, and the CTR win doesn't hold up.

## Ship rule check

The plan says to ship only if the primary metric is significantly positive and every guardrail passes.

| Criterion | Requirement | Result | Pass? |
|---|---|---|---|
| Primary: revenue per session | Significantly positive (alpha 0.05) | 4.82 → 4.76 (−1.2%), p = 0.21 | **No.** Not significant, and the point estimate is negative. |
| Guardrail: search latency p95 | Rise ≤ 20 ms | 212 → 250 ms (+38 ms), p < 0.001 | **No.** The rise is nearly double the limit. |

For this outcome the plan says "do not ship; write up as a learning."

## Why the CTR result doesn't change this

CTR went from 3.10% to 3.41% (+10% relative, p = 0.03). The plan made CTR a secondary, diagnostic metric, and the evidence behind it is weak:

1. **The lift was a novelty effect that has faded to nothing.** Treatment CTR was 3.85% on days 1–3 and 3.65% on days 4–7. On days 8–14 it was 3.12% against 3.10% for control. The 3.41% average comes from the early days. The last-week gap is 0.02 points, so v7's steady-state CTR effect looks like zero.
2. **No multiple-comparison correction.** `metrics.csv` reports 20 metrics, and one p = 0.03 among 20 tests is about what chance produces. It wouldn't survive a Bonferroni or FDR correction.
3. **The extra clicks didn't turn into revenue.** Revenue per session is flat to slightly down, and latency is 38 ms worse.
4. **The data has integrity problems (next section).**

## Data-quality problems to resolve before trusting any of this

- **Sample ratio mismatch.**
  - The plan specifies a 50/50 split, but `assignment.csv` shows 52,310 control users and 47,690 treatment users.
  - Against an expected 50,000 each, chi-square is about 213 (1 df), p ≈ 1e-48. That is not noise.
  - Assignment, logging, or exposure filtering is broken for at least one arm, which can bias every metric. Find the cause first.
- **The metrics table looks templated.** Below the first three rows, baselines run 1.00, 1.10, 1.20 and so on. Every delta is exactly +0.3%, and the p-values rise in steady 0.04 steps. Values like `add_to_cart_rate` = 1.00 are implausible. I wouldn't cite those rows as evidence either way until the pipeline that produced them is checked.
- **Control CTR is exactly 3.10 on all 14 days.** Real daily data would vary, so this series looks smoothed or aggregated.
- **`summary.md` hides the verdict.** It is auto-generated and reports only the CTR line, leaving out the primary metric and the guardrail. That is how a secondary metric ended up as the headline.

## Proposed next steps

1. Don't ship v7 as it stands.
2. Investigate the sample ratio mismatch and the metrics pipeline.
3. Profile v7's latency. The +38 ms is the clearest effect in the data, and fixing it is the prerequisite for a re-test.
4. If you re-test, pre-specify the analysis window so novelty effects are excluded or tracked. In this run they covered roughly the first week.
5. Make the auto-generated summary lead with the primary metric and the guardrails.

## Caveats

- I only had the aggregate CSVs. I couldn't check per-user data or how the p-values were computed.
- Revenue p = 0.21 means no detectable effect, not proven harm. The ship decision doesn't depend on that, because the latency guardrail fails regardless.

If you want this saved as `launch_review.md`, I can write it once file writes are enabled. Alternatively, you can copy it from here.