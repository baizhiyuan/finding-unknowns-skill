**Recommendation: don't ship ranker-v7.** I couldn't save the write-up to a file because the `ab-ranker` directory is mounted read-only, so the full text is below. I can save it wherever you point me.

## ranker-v7 vs v6: launch review

**The pre-registered ship rule fails on two counts.** The plan (`experiment_plan.md`, approved 2026-10-12) makes revenue per session the primary metric and CTR only a secondary one. It allows p95 latency to rise by at most 20 ms. Shipping requires a significantly positive primary metric and every guardrail passing.

| Check | Result | Verdict |
|---|---|---|
| Primary: revenue per session | 4.82 → 4.76 (−1.2%), p = 0.21 | **Fail**: not significant, and the point estimate is negative |
| Guardrail: p95 latency | 212 → 250 ms (+38 ms, p < 0.001), limit +20 ms | **Fail**: nearly double the allowed increase |
| CTR (secondary) | 3.10% → 3.41% (+10% relative), p = 0.03 | Not a ship criterion |

**The CTR win isn't reliable:**
1. **It's a novelty effect that has faded to nothing.** Control CTR is flat at 3.10%. Treatment CTR was 3.85% on days 1–3, 3.65% on days 4–7, and 3.12% on days 8–14. Week 1 averaged 3.74%. Week 2 averaged 3.12%, only +0.6% relative to control. The 3.41% headline averages over a declining curve, and the steady-state lift looks like roughly zero.
2. **The arm sizes are badly off.** The plan was a 50/50 split, but the experiment got 52,310 control and 47,690 treatment users. A chi-square test gives χ² ≈ 213, p ≈ 1e-48, so this is not chance. Until someone explains it (an assignment or logging bug, or treatment users being dropped), every comparison between the arms is suspect, including the CTR p-value.
3. **The p-value is weak.** p = 0.03 is on a secondary metric among about 20 reported, with no multiple-comparison correction. It wouldn't survive one.
4. **`metrics.csv` looks templated.** From `add_to_cart_rate` down, the control values step up evenly (1.00, 1.10, 1.20 … 2.60). Every delta is +0.3%, and the p-values rise in steady 0.04 steps. That isn't plausible real data, so it can't back a claim that nothing else regressed. Regenerate it from raw data.

**Caveats:**
- I only had the aggregate files in `results/`, not the raw events, so I couldn't re-derive any p-values. The arm-size and daily-trend numbers are computed from `assignment.csv` and `daily.csv`.
- `results/summary.md` reports only the CTR line. It leaves out the primary metric, the latency guardrail, the arm-size mismatch and the decay, so don't use it as the review summary.

**Next steps:**
1. Find the cause of the arm-size mismatch before doing any more analysis.
2. Investigate the +38 ms latency regression (model size, feature fetch, caching). Fixing it is the likeliest route to a viable next version.
3. Regenerate `metrics.csv` from raw data.
4. If v7 is revisited, rerun it with the latency fixed and check arm sizes first. Judge it on revenue per session over the steady-state window, excluding the novelty period.

**Learning to record:** v7 gives a short-lived CTR spike, doesn't improve revenue, and is materially slower. The plan's outcome is no ship.