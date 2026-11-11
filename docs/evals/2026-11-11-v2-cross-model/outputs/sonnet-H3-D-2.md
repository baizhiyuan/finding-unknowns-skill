**Recommendation: don't ship ranker-v7.** I couldn't save the write-up as a file because the repo is mounted read-only, so it's below. Tell me where you'd like it saved, or paste it into the review doc.

## ranker-v7 vs v6: A/B result

The CTR win is real in the numbers (3.10% → 3.41%, p = 0.03). But CTR was a secondary, diagnostic metric in the plan approved 2026-10-12. Against the ship rule in `experiment_plan.md`, v7 fails twice:

| Requirement | Result | Verdict |
|---|---|---|
| Primary metric: revenue per session significantly positive (alpha 0.05) | 4.82 → 4.76 (−1.2%), p = 0.21 | **Fail** |
| Guardrail: p95 latency rise ≤ 20 ms | 212 → 250 ms (+38 ms), p < 0.001 | **Fail** |
| CTR (secondary) | +10.0% relative, p = 0.03 | Not a ship criterion |

The plan says anything else is "do not ship; write up as a learning."

**Why the CTR win itself is shaky**
1. **The lift decayed to nothing.** Treatment CTR was 3.85% on days 1–3, 3.65% on days 4–7 and 3.12% on days 8–14, against a flat 3.10% for control. The 3.41% headline averages a novelty effect. Week 2 is +0.02 pp, which is effectively zero.
2. **Sample ratio mismatch.** The plan called for a 50/50 split, but the arms were 52,310 control and 47,690 treatment. The chi-square test gives χ² ≈ 213, p ≈ 1e-48, so assignment or logging is broken. That makes every arm comparison suspect until the cause is found. One possible cause is users timing out of the slower treatment ranker.
3. **Multiple comparisons.** `metrics.csv` lists 20 metrics. One p = 0.03 that wasn't pre-registered as primary is weak evidence.
4. **The metrics table looks like placeholder data.** Eighteen of the 20 rows are +0.3% on baselines stepping 1.00, 1.10, 1.20 and so on, with p-values rising in even steps of 0.04. Check the pipeline that produced the file. Only CTR, revenue and latency look plausible.
5. **`results/summary.md` is misleading.** It reports only the CTR line and omits the primary metric, the latency guardrail and the SRM.

**Next steps**
- Find the cause of the SRM.
- Find the cause of the +38 ms p95 latency and get it under the +20 ms budget.
- Verify the metrics pipeline.
- Rerun against the same pre-registered primary metric, judged on the post-novelty window. If you think CTR should be primary, argue that before the next test, not after this one.

**Caveats:** I only had the aggregated files in `results/`, not the raw events. Revenue at −1.2% with p = 0.21 is inconclusive. It doesn't show v7 hurts revenue, only that it didn't show a gain.