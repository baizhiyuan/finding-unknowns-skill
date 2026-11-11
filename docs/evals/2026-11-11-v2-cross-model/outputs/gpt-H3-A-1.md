**Launch-review recommendation: do not ship ranker-v7.** CTR improved, but the experiment did not meet the [approved ship rule](experiment_plan.md): a statistically significant increase in revenue per session and passing every guardrail.

| Metric | Control → treatment | Result |
|---|---|---|
| **Primary: revenue per session** | 4.82 → 4.76 | −1.2%, p = 0.21; required improvement not demonstrated |
| **Guardrail: p95 search latency** | 212 → 250 ms | +38 ms; exceeds the +20 ms limit |
| Secondary: CTR | 3.10% → 3.41% | +0.31 percentage points (+10% relative), nominal p = 0.03 |

The revenue result does not establish a decline, but it also does not establish the benefit required for launch. The latency guardrail fails independently.

Two additional findings weaken the CTR claim:

- **Unexpected allocation imbalance.** The planned split was 50/50, but observed user counts were 52,310 control and 47,690 treatment. A sample-ratio-mismatch test gives χ² = 213.44, p ≈ 2.4 × 10⁻⁴⁸. This requires investigation of assignment, eligibility, exclusions, and logging before trusting causal estimates.
- **The lift fades over time.** Treatment CTR falls from 3.85% on days 1–3 to 3.12% on days 8–14, versus control at 3.10% throughout. This is consistent with a transient effect; daily denominators are unavailable to assess its uncertainty. CTR is also one of 20 reported metrics, so its nominal p-value should not be presented as confirmatory evidence of an overall win.

**Next steps:** retain ranker-v6, resolve the allocation discrepancy, address latency, and rerun under the original decision criteria with sufficient power for revenue per session. Record this experiment as a learning: the reported aggregate click gain did not establish business benefit or satisfy launch requirements.

Sources: [metrics](results/metrics.csv), [assignment counts](results/assignment.csv), [daily CTR](results/daily.csv).