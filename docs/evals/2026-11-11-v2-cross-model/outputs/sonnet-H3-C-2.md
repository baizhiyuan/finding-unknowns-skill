I couldn't save the write-up to a file, because the Write tool is disabled in this session. I didn't work around that through the shell. The full write-up is below, so you can paste it into `results/launch_review.md` or tell me to save it another way.

# ranker-v7 vs ranker-v6: launch review

**Recommendation: do not ship.** Rigor level: decision, because ship/no-ship rides on a plan with a rule approved before launch.

## Frozen rule (`experiment_plan.md`, approved 2026-10-12, before launch)
> Primary metric: revenue per session. CTR is a secondary, diagnostic metric.
> Guardrail: search latency p95 may not rise by more than 20 ms.
> Ship rule: primary metric significantly positive (two-sided, alpha 0.05) AND every guardrail passes. Anything else: do not ship; write up as a learning.

## Bottom line
- **Rule verdict: FAIL.** Two independent failures:
  1. Revenue per session went from 4.82 to 4.76, **−1.2%, p = 0.21**. It is not significantly positive, and the point estimate is negative.
  2. Latency p95 went from 212 to 250 ms, **+38 ms against a 20 ms limit** (p < 0.001).
- **The CTR win doesn't change this.** The plan declared CTR diagnostic-only before launch. The lift is also transient, and it is one of 20 uncorrected metrics (see below).
- **Direction verdict: weakened.** v7 gets more early clicks, but the lift fades to about zero. It costs latency and shows no revenue benefit.
- **There is also a sample-ratio defect.** The review should hear about it before anyone relies on these numbers.

## Findings

| Question | Measured | Verdict | Mechanism [tier] |
|---|---|---|---|
| Revenue per session (primary) | −1.2%, p = 0.21 | **FAIL** | none established [untested] |
| Latency p95 (guardrail) | +38 ms vs +20 ms limit | **FAIL** | v7 ranking is slower per query [inferred; no profiling data] |
| CTR (diagnostic) | 3.10% → 3.41%, p = 0.03 | descriptive only | novelty or early-exposure decay [supported] |
| Assignment integrity | 52,310 vs 47,690 on a planned 50/50 | **defect** | unknown [untested] |

**1. Sample-ratio mismatch.**
- A 50/50 hash split should give about 50,000 users per arm. The data has 52,310 control and 47,690 treatment.
- Chi-square is about 213 on 1 df, so this is not chance. It means the arms may not be comparable populations, and every metric, CTR included, is suspect until it is explained.
- Possible causes, all untested:
  - Treatment drops or fails to log users, perhaps through slow-path timeouts. This is plausible given the latency regression.
  - A bucketing or logging bug.
  - A bot or filter exclusion that differs by arm.
- This doesn't rescue v7, since the FAIL stands on its own. It does mean a rerun is unsafe until the cause is found.

**2. CTR lift is transient.**
- Treatment CTR by day was 3.85 on days 1–3, 3.65 on days 4–7 and **3.12 on days 8–14**. Control was a flat 3.10.
- From day 8 on the lift is about +0.02 pt (+0.6%), which is effectively zero. The headline +10% is an average over a decaying effect, not a steady state.
- Novelty decay fits [supported], but so does a deploy or config change on day 4 and day 8, because the shape is a step rather than a smooth decay. Checking the deploy log would tell the two apart.
- With 20 metrics tested, about one false positive is expected at alpha 0.05. CTR's p = 0.03 doesn't survive a Bonferroni threshold (0.0025).

**3. The other 18 metrics look generated.**
- They all show an identical +0.3% delta. Their p-values climb in exact 0.04 steps, and their baselines run 1.00, 1.10, 1.20 and so on. That includes "mobile_ctr 2.10" and "dwell_time_s 1.40".
- Control CTR is exactly 3.10 on all 14 days.
- I treat these as untraceable and used them as evidence for nothing. Someone should confirm where `metrics.csv` comes from.
- `summary.md` (auto-generated) reports only the CTR line. It omits the primary metric and the guardrail, which is probably how the "won" framing arose.

## Caveats
- No prediction was recorded before launch, so any theory here is post-hoc.
- There are no CIs, daily variance or A/A baseline, so I couldn't compute a noise floor. I relied on the supplied p-values.
- Revenue p = 0.21 means the test couldn't tell, not that there is no effect. The rule doesn't ask for power, so the FAIL stands.
- The audit was same-context only, so it is weaker than a fresh-context audit. I didn't run `mechanism-auditor`.

## Not checked
- Segment splits (mobile/desktop, new/returning).
- A power calculation for revenue per session.
- Whether the run really lasted the planned 14 days.
- Raw event logs. I only had aggregates.

## Next
1. **Don't ship v7.** The plan says "Anything else: do not ship; write up as a learning." A new story about CTR can't overturn that.
2. Investigate the sample-ratio mismatch first. It uses existing logs only and needs no approval.
3. To keep the direction alive, get the latency regression under +20 ms. Then run a new pre-registered test on fresh traffic with the same primary metric, a power calculation and a frozen rule. That test needs your approval.
4. If anyone proposes making CTR the primary metric now, that would be a retroactive rule change. It shouldn't apply to this run, though it could be proposed for the next one.