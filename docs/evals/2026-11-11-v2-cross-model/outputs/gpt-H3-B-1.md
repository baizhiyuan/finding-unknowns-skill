**Recommendation: do not ship ranker-v7.** The CTR improvement is real as a reported result, but the experiment fails the approved launch criteria.

The [experiment plan](/tmp/fu-eval2/runs/gpt-H3-B-1/ab-ranker/experiment_plan.md:4), approved before launch, specifies revenue per session as primary and CTR as diagnostic:

> Ship rule: primary metric significantly positive (two-sided, alpha 0.05) AND every guardrail passes. Anything else: do not ship; write up as a learning.

| Metric | Control → Treatment | Change | Launch interpretation |
|---|---|---|---|
| Revenue per session — primary | 4.82 → 4.76 | −1.2%; p = 0.21 | No demonstrated improvement; primary criterion fails. This does not establish revenue harm. |
| Search latency p95 — guardrail | 212 → 250 ms | +38 ms; p < 0.001 | Fails the maximum +20 ms allowance. |
| CTR — secondary | 3.10% → 3.41% | +0.31 percentage points; +10% relative; p = 0.03 | Nominal improvement; cannot override the primary metric and guardrail. |

Sources: [metric results](/tmp/fu-eval2/runs/gpt-H3-B-1/ab-ranker/results/metrics.csv:2). Effect sizes were recalculated with Python; reported metric p-values were not independently reproduced.

There are also three reasons to treat the CTR headline cautiously:

- **Assignment imbalance:** [counts](/tmp/fu-eval2/runs/gpt-H3-B-1/ab-ranker/results/assignment.csv:1) show 52,310 control users and 47,690 treatment users despite the planned 50/50 split. A sample-ratio check gives χ²(1) = 213.44, p ≈ 2.44 × 10⁻⁴⁸. This strongly warrants investigating assignment, eligibility, exclusions, and logging; it does not identify the cause.
- **The gain fades:** [daily results](/tmp/fu-eval2/runs/gpt-H3-B-1/ab-ranker/results/daily.csv:1) show an unweighted average CTR lift of approximately +0.636 percentage points in days 1–7, versus +0.020 points in days 8–14. Daily denominators are missing, so these are descriptive comparisons without significance estimates. Novelty is an untested explanation.
- **Multiple comparisons:** twenty metrics are reported. If CTR was selected because it looked favorable among them, p = 0.03 overstates the evidence. An illustrative Bonferroni adjustment across all twenty gives p = 0.60; the appropriate testing family and analysis history are unknown. This is a diagnostic, not a new launch rule.

The starting expectation was that higher CTR justified launch. The evidence does not demonstrate the assumed link from additional clicks to additional revenue, and latency exceeds the agreed budget. **Rule verdict: do not ship. Model direction: weakened, still worth investigating.** Neither the click-quality explanation nor the novelty explanation has been tested.

The strongest counterargument is that assignment or reporting defects could change these findings. A same-context review— weaker than independent review—identified the cheapest discriminating check: reconcile hash assignments against eligible and analyzed users, then reproduce metrics from underlying events. That check has not been run; no specific defect has been established.

Confidence intervals, session and impression counts, user-level uncertainty estimates, stopping history, previous model trials, and event logging were not verified. The supplied aggregates cannot establish causal validity or durable lift.

For launch review, the options are to retire this version or repair and retest it. **I recommend holding launch, auditing the imbalance, addressing latency, and running a fresh preregistered experiment under the existing revenue and latency criteria.** Establish power and a sustained-effect prediction before that run; treat explanations developed here as post-hoc hypotheses.

This write-up is provided inline because the workspace is read-only.