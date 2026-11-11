I couldn't save the write-up because the repo is mounted read-only, so I've put it below. I didn't try to remount it. If you want it saved, make the directory writable or tell me another path, and I'll write it there.

# ranker-v7 launch review: recommendation is not to ship

v7 fails the ship rule in `experiment_plan.md` on two separate counts. That plan was approved on 2026-10-12, before launch. The rule is that the primary metric must be significantly positive and every guardrail must pass.

| Criterion | Result | Pass? |
|---|---|---|
| Primary: revenue per session | 4.82 → 4.76 (−1.2%), p = 0.21 | No. It isn't significant, and the point estimate is negative. |
| Guardrail: p95 latency, at most +20 ms | 212 → 250 ms (+38 ms), p < 0.001 | No. The increase is almost double the allowed limit. |

CTR (3.10% → 3.41%, p = 0.03) is a secondary diagnostic metric in the plan. It can't trigger a ship decision.

## Why the CTR win isn't a real win
- **It was a novelty effect that has faded.**
  - Treatment CTR was 3.85% on days 1–3, 3.65% on days 4–7 and 3.12% on days 8–14. Control stayed at 3.10%.
  - The 3.41% is the 14-day average of a declining curve. The last 7 days show about +0.6%, which is effectively nothing.
- **Multiple comparisons.** `metrics.csv` has 20 metrics, so there's about a 64% chance that at least one shows p < 0.05 by luck. With a Bonferroni correction the threshold is 0.0025, and CTR at p = 0.03 doesn't meet it.
- **Revenue didn't follow clicks.** More clicks with no revenue gain fits curiosity clicks rather than better relevance.

## Data problems to fix before trusting any number
- **Sample ratio mismatch.**
  - The plan said 50/50, but the split is 52,310 control and 47,690 treatment (chi-square 213, p ≈ 1e-48).
  - That points to a bug in assignment or logging, such as differential dropout or bot filtering. Every comparison is suspect until it's explained.
- **Control CTR is exactly 3.10 on all 14 days.** Real daily data would vary. This looks like a pasted constant.
- **Most of `metrics.csv` looks like placeholder data.**
  - Control values run 1.00, 1.10, 1.20 and so on, every delta is +0.3%, and the p-values rise by exactly 0.04 per row.
  - I wouldn't cite those 18 rows until they're regenerated from raw logs.

## What I didn't check
I only had the aggregate CSVs. I haven't seen raw logs, the assignment code, confidence intervals or the revenue standard errors. I also couldn't confirm that the analysis used all 14 days, since the summary is dated 10-28.

The revenue result is inconclusive rather than proof that v7 hurts. We can't rule out a small gain or a small loss.

## Next steps
1. Find the cause of the sample ratio mismatch before re-analysing anything.
2. Profile the +38 ms latency regression. It blocks shipping on its own.
3. If v7 is still worth pursuing, re-run with revenue per session adequately powered. Run it long enough for the novelty effect to settle, which looks like about 8 days.