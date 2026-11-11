**Recommendation: do not ship ranker-v7.** CTR improved, but the experiment failed the approved launch criteria and shows an allocation imbalance that needs investigation.

The [experiment plan](/tmp/fu-eval2/runs/gpt-H3-A-2/ab-ranker/experiment_plan.md) requires a statistically significant increase in **revenue per session** and a p95 search latency increase of no more than 20 ms. CTR is a secondary diagnostic metric.

| Metric | Control | Treatment | Change | Reported p-value | Assessment |
|---|---:|---:|---:|---:|---|
| Revenue per session | 4.82 | 4.76 | −1.2% | 0.21 | Primary criterion not met |
| Search latency, p95 | 212 ms | 250 ms | +38 ms | <0.001 | Guardrail breached |
| CTR | 3.10% | 3.41% | +0.31 percentage points; +10% relative | 0.03 | Secondary improvement |

Source: [metrics](/tmp/fu-eval2/runs/gpt-H3-A-2/ab-ranker/results/metrics.csv). The revenue result does not establish a decline, but it provides no evidence of the significant improvement required to ship. The latency increase exceeds the allowed limit by 18 ms.

Three findings further limit confidence in declaring a win:

- **Allocation imbalance:** [User counts](/tmp/fu-eval2/runs/gpt-H3-A-2/ab-ranker/results/assignment.csv) are 52,310 control versus 47,690 treatment despite the planned 50/50 split. A sample-ratio mismatch test gives χ² = 213.44, p ≈ 2.4 × 10⁻⁴⁸. Investigate assignment, exposure logging, and exclusions before trusting causal estimates.
- **The CTR lift fades:** [Daily results](/tmp/fu-eval2/runs/gpt-H3-A-2/ab-ranker/results/daily.csv) show treatment CTR falling from 3.85% on days 1–3 to 3.12% on days 8–14, versus 3.10% control throughout. This raises concerns about durability; daily denominators are unavailable to quantify uncertainty.
- **CTR significance is nominal:** Twenty metrics are reported, with no multiplicity procedure documented. An illustrative Bonferroni correction across all 20 gives CTR an adjusted p-value of 0.60. Regardless of correction, CTR cannot replace the prespecified primary metric.

Keep ranker-v6 in production. Investigate the allocation mismatch, address the latency regression, and diagnose why additional clicks did not improve revenue. Then rerun a prespecified experiment using the original revenue and latency launch criteria. Record this test as a learning, rather than a launch win.