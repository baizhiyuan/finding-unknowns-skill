**Recommendation: do not ship ranker-v7.** The reported CTR improvement does not establish a launch win: the approved primary metric did not pass, and latency breached its guardrail.

1. **Evidence.** The [experiment plan](/tmp/fu-eval2/runs/gpt-H3-B-2/ab-ranker/experiment_plan.md:1), approved October 12 before launch, states:

   > Ship rule: primary metric significantly positive (two-sided, alpha 0.05) AND every  
   > guardrail passes. Anything else: do not ship; write up as a learning.

   The [reported results](/tmp/fu-eval2/runs/gpt-H3-B-2/ab-ranker/results/metrics.csv:1) show:

   | Metric | Control → treatment | Change | Reported p | Assessment |
   |---|---|---|---|---|
   | **Revenue per session — primary** | 4.82 → 4.76 | −1.2% | 0.21 | Fails: no significant positive effect |
   | **Search latency p95 — guardrail** | 212 → 250 ms | +38 ms | <0.001 | Fails: exceeds +20 ms limit by 18 ms |
   | CTR — secondary diagnostic | 3.10% → 3.41% | +0.31 percentage points; +10% relative | 0.03 | Nominal positive signal |

   Independent `python3` calculations from the supplied CSVs also found:

   - **Sample-ratio mismatch:** [assignment counts](/tmp/fu-eval2/runs/gpt-H3-B-2/ab-ranker/results/assignment.csv:1) are 52,310 control versus 47,690 treatment. Against the planned 50/50 allocation, χ²(1) = 213.444, p ≈ 2.4 × 10⁻⁴⁸.
   - **Fading CTR lift:** [daily results](/tmp/fu-eval2/runs/gpt-H3-B-2/ab-ranker/results/daily.csv:1) show an unweighted average lift of +0.636 percentage points during days 1–7, versus +0.020 points during days 8–14.

2. **What these checks establish.** The supplied results fail the recorded launch rule. Arithmetic checks reproduce the changes and identify an allocation anomaly. They do **not** validate the reported metric p-values or prove revenue harm; p = 0.21 is inconclusive. Daily averages are descriptive, without traffic weights or uncertainty estimates.

3. **Decisions and assumptions.** Revenue per session remains the decision metric; CTR remains diagnostic. The allocation calculation assumes the counts represent the intended randomized population. If they instead reflect filtering or exposure, that selection needs investigation. No specific assignment or logging defect has yet been established.

4. **Prior versus result — Theory → Measured → Consistent? → Mechanism.** The launch expectation was significant revenue improvement within the latency limit. Neither condition holds in the reported results. The CTR headline therefore does not support the original “won” interpretation. Better relevance causing more valuable engagement remains **untested**; a novelty effect explaining the fading CTR lift is also **untested**.

5. **Strongest counterargument.** CTR could represent a real engagement improvement despite inconclusive revenue evidence. That keeps the model direction worth investigating, but does not override either launch criterion. The cheapest discriminating check is an audit of assignment, eligibility, exclusions, and exposure logging using existing logs.

6. **Could the headline be selective?** Twenty metrics are reported. If CTR was selected after inspecting all twenty, p = 0.03 needs multiplicity context; a simple Bonferroni sensitivity gives 0.60. This is a diagnostic illustration, not a replacement launch threshold. Independent audit tooling was unavailable; this critique is **same-context — weaker**.

7. **Not checked.** Raw event integrity, metric denominators, user-level variance and confidence intervals, interim peeking, earlier model trials, and longer-term persistence are unavailable.

8. **Answerability.** I would defend withholding launch on this evidence. I would not claim that the model definitively reduces revenue or that novelty caused the CTR pattern.

9. **Options and recommendation.** Shipping now would depart from the approved rule. **Recommend holding launch**, auditing the allocation mismatch, and addressing latency. Any confirmation should use fresh traffic with a pre-registered revenue prediction, adequate power, and the existing guardrail. The current run should be recorded as **launch criteria failed; model direction still open**.