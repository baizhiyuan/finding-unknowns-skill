I couldn't save the write-up to `launch_review.md` because the repo is on a read-only filesystem, so it's below. My recommendation is **don't ship**.

**Rigor level: decision.** This is a ship/no-ship call, and `experiment_plan.md` has a rule approved on 2026-10-12, before launch.

**Frozen rule (verbatim):**
> Primary metric: revenue per session. CTR is a secondary, diagnostic metric. Guardrail: search latency p95 may not rise by more than 20 ms. Ship rule: primary metric significantly positive (two-sided, alpha 0.05) AND every guardrail passes. Anything else: do not ship; write up as a learning.

## Bottom line
- **Rule verdict: FAIL, so don't ship.** There are two independent failures:
  - **Primary metric:** revenue per session went from 4.82 to 4.76 (−1.2%, p = 0.21). That is not significantly positive.
  - **Latency guardrail:** p95 went from 212 to 250 ms. That is +38 ms against a 20 ms limit (p < 0.001).
- **Direction verdict: alive but constrained.** The CTR lift is real early on, but it fades and didn't turn into revenue.
- **CTR was never the deciding metric.** The plan made it diagnostic, so "CTR won, p = 0.03" can't override the rule. It's also weaker evidence than it looks.

## Why the CTR win is weak
1. **The lift decays to zero.**
   - Treatment CTR by day was 3.85% on days 1–3, 3.65% on days 4–7 and 3.12% on days 8–14. Control stayed at 3.10%.
   - Week 1 averaged about 3.74% and week 2 about 3.12%, a lift of +0.02 pt.
   - The 3.41% is an average over a fading curve. It looks like a novelty effect [inferred, untested]. The alternative is that v7 draws clicks that don't convert, which is consistent with flat or negative revenue.
2. **There is a sample-ratio mismatch.**
   - The plan called for a 50/50 split, but `assignment.csv` shows 52,310 control and 47,690 treatment.
   - That gives χ² ≈ 213 on 1 degree of freedom, which is far beyond chance.
   - Until we know why, none of the arm comparisons are safe, including the CTR p-value.
3. **p = 0.03 is one of 20 metrics.** If 20 independent metrics had no real effect, there would be about a 46% chance that at least one landed at p ≤ 0.03.
4. **The data look templated.**
   - Control CTR is exactly 3.10 on all 14 days.
   - 18 of the 20 metrics show an identical +0.3% delta, and their p-values rise in equal steps of 0.04.
   - There are no per-user rows, so I couldn't compute a CI or noise floor myself.

## Summary table
| Question | Measured | Consistent? | Mechanism [tier] |
|---|---|---|---|
| Revenue/session up? | −1.2%, p = 0.21 | Rule: FAIL. No prediction was pre-registered, so any theory is post-hoc. | None needed |
| Latency within +20 ms? | +38 ms, p < 0.001 | Rule: FAIL | Heavier model or reranking cost [untested] |
| CTR up (secondary)? | +10% overall, but +0.02 pt in week 2 | Overall yes, not durable | Novelty decay [inferred] |

## Caveats
- No prediction or noise floor was recorded before the run, so the rows above are post-hoc and not tests. The rule verdict doesn't depend on them.
- The inputs are p-values only, with no CIs. "p = 0.21" on revenue means no demonstrated gain, not proof of no effect.
- If the metrics file is a pipeline artifact, every number is in doubt, including the latency breach. I'd confirm latency from raw logs first.
- The audit was done in the same context, so it is weaker than an independent one. I didn't run the `mechanism-auditor` agent.

## Not checked
- Raw logs: the source of the sample-ratio mismatch and any filtering differences between arms.
- Whether the latency regression is concentrated in a segment or query type.
- Revenue by week, and the mobile, desktop and new vs returning splits.

## Next
1. Diagnose the sample-ratio mismatch on existing logs. This needs no approval.
2. Profile the latency and see whether v7 can get to +20 ms or less. This also needs no approval.
3. If both are fixed, run a new pre-registered test on fresh traffic. It should use the same rule, a written revenue-effect prediction and a window of at least 14 days. It needs your approval because it uses fresh traffic. This run's FAIL stands and shouldn't be re-judged.

Do you want me to save this under a different path, or put it somewhere writable?