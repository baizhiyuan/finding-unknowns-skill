---
name: theory-vs-result
description: "Report empirical results as Theory → Measured → Consistent? → Mechanism, so a number never arrives without the prediction it tests and the reason it came out that way. Use when STARTING a measurement (write the prediction, noise floor and decision rule first) and when REPORTING one (backtest, benchmark, A/B test, ablation, training run, load test, debugging hypothesis). Triggers: 'theory vs result', '理论 → 实测 → 机理', 'why did this come out like this', 'is this consistent', 'does this pass', experiment/backtest/benchmark reports. Not for results with no prediction at stake (a lookup, a status check)."
aliases: [theory-measured-mechanism, predict-measure-explain]
metadata:
  credits:
    source: "Distilled from a long-running empirical research practice, generalized for any measured claim"
    sibling: "finding-unknowns (unknowns before work) and keep-the-reasoning (the handoff) — this repository"
---

# Theory vs Result

*Theory lives inside engineering; engineering is built on theory.*

<Purpose>
A measured number on its own is not a finding. "accuracy 91%", "p95 down 8%", "loss went
up" tell the reader nothing until they know what was expected, whether the gap is bigger
than noise, and why it happened. Two failure modes follow from leaving that out, and they
point in opposite directions. **Dismissal**: the theory was good, the result was bad, and
the direction gets thrown out ("didn't pass") without anyone asking which assumption broke.
**Rescue**: the result was bad, a story gets told afterwards, and the story quietly
overturns a rule that was agreed before the run. This skill blocks both. Every result is
reported as a fixed four-part card: **Theory → Measured → Consistent? → Mechanism**. Facts,
inferences and untested explanations stay visibly separate, and the verdict under the frozen
rule stays separate from the judgment about the direction.
</Purpose>

<Use_When>
- Reporting any result that was measured to test a belief: backtests, benchmarks, A/B
  tests, ablations, training runs, load tests, profiling, a bug-fix hypothesis
- Before running such a measurement: write the prediction and decision rule first
- The user asks "why", "is this consistent", "does it pass", "should we drop this"
- A result contradicts the expectation, or sits close to a threshold
- A `finding-unknowns` ledger row with route `experiment` comes back with data
- `keep-the-reasoning` packet section 4 (Prior vs result) concerns a measured claim
</Use_When>

<Do_Not_Use_When>
- Nothing was predicted and nothing is decided (a lookup, a status read, a log grep)
- The work is building, not measuring. Use `finding-unknowns` before it and
  `keep-the-reasoning` at the handoff
- A one-off sanity number with no decision attached. One sentence is enough: "measured X,
  expected roughly X, no action"
</Do_Not_Use_When>

<Execution_Policy>
- **Theory before data.** Write the prediction before looking at the result. A theory
  written afterwards is labelled `post-hoc` and counts as weaker evidence
- **Predict magnitude and location, not just sign.** "Faster" cannot fail. "~2× on cold
  reads, ~0 on warm" can
- **Noise floor first.** No consistency verdict until you know how big a difference
  noise produces (seeds, reruns, windows, bootstrap). A difference inside it gets
  "can't tell", not "consistent"
- **Fair comparison or no comparison.** Same data, same coverage, same seeds/runs, same
  metric definition, same evaluation pipeline (how outputs become actions). Change one variable at a time, or say the
  change was confounded
- **The metric must be the objective.** Report the metric that is actually shipped,
  paid for or decided on. A convenient proxy is supporting evidence only
- **Mechanism has an evidence tier.** Every explanation carries one of
  `verified · supported · inferred · untested`. Never present an inference as a mechanism
- **A mismatch names the broken assumption.** Say which link in the theory's chain failed,
  give the smallest check that would tell the candidate explanations apart, and say what
  adjustment would let the idea hold
- **Two verdicts, never merged.** The *rule verdict* (what the pre-agreed rule says) is
  final for this run. The *direction verdict* (is the idea alive) is a judgment. A
  mechanism can keep a direction alive, but it cannot overturn a rule verdict
- **Rules are explained before they are frozen.** Any new or tightened threshold is
  explained in plain language and approved by the user before it applies (Step 1.4)
- **Report in the user's language.** Chinese labels: 理论预期 → 实测 → 是否一致 → 机理
</Execution_Policy>

<Steps>

## Step 0: Triage (blocking)

| Lane | Signals | Output |
|------|---------|--------|
| **Note** | one number, low stakes, no decision rides on it | one-line card |
| **Report** | a result someone will act on; a mismatch; near a threshold | full cards + summary table (Step 4) |
| **Decision** | adopt/reject, ship/no-ship, a pre-registered test, money or production | Report, plus the frozen rule quoted verbatim and the rule verdict separated from the direction verdict. No frozen rule → propose one via Step 1.4 and stop; the decision is the user's |

Announce: `Result lane: {note | report | decision} — {one-line reason}`.

## Step 1: Before measuring, write the theory (prediction card)

Write this down before you run anything, or before you open a result that already exists:

```
Claim under test : {the belief, one sentence}
Mechanism chain  : A → B → C   (each link is an assumption that can fail on its own)
Prediction       : direction + rough magnitude + where it shows up
                   (which subset, regime, tail, segment, load level)
Noise floor      : how big a difference noise makes, and how you know
                   (seed spread, rerun variance, CI width, prior runs)
Falsifier        : the result that would show the claim is wrong
Decision rule    : the pre-agreed rule if one exists, quoted verbatim; else "descriptive only"
Data budget      : which data this run uses up (holdout / fresh traffic / forward period), if any
Trials so far    : how many configs/hypotheses were already tried for this claim
Terms            : definitions of any term that could shift meaning ("accuracy", "return", "rare")
```

1. **Scale the card to the stakes.** In the Note lane the Prediction line alone is enough.
2. **Locate the effect.** Most real mechanisms act on a subset: the tails of a ranking, cold
   caches, small accounts, peak hours. Say where the effect should appear and
   where it should *not*. The "should not" half is often the sharper test.
3. **Name the chain.** "Feature X carries information → the model learns it → the
   decisions that act on it change → the outcome metric improves" has four links. When the result
   misses, Step 3 has to say which link broke.
4. **Threshold gate.** If you are proposing a new or tighter pass/fail line, stop. Explain
   to the user in plain words: **what it protects against, why this number, what failing it
   means, and what it might wrongly reject.** Freeze it only after the user approves, and
   record the approval. Until then it stays a diagnostic. A diagnostic never quietly turns
   into a gate, and a rule applies only from its approval onward, never retroactively.
5. **If the result is already in hand**, write the card anyway and mark it
   `post-hoc theory — weaker`. Do not "predict" what you have already seen. A result that
   exists but has not been opened can still get a genuine prediction.
6. **No theory at all** (pure exploration that still feeds a decision): label it
   `exploratory`; Consistent? = n/a; rule verdict = descriptive only. The deliverable
   includes a prediction card for the next, pre-registered run.

## Step 2: Measure fairly

Before trusting a difference, check:

| Check | Failure it prevents |
|-------|---------------------|
| Matched baseline: same data window, coverage, seeds/runs, population, evaluation pipeline (how outputs become actions) | Crediting the change with what the sample did |
| One variable changed, or the confounds named | Crediting the architecture with what the loss or preprocessing did |
| Simplest baseline present | Complexity winning only because nothing simple was tried |
| Same ≥N seeds/reruns on both sides; independent batches reported separately | A lucky seed; a pooled result hiding a failed replication |
| All windows/segments reported, not the best ones | Cherry-picking periods, seeds or regimes |
| Metric = objective; proxies labelled as proxies | A metric that improves while what you are paid for gets worse |
| Pipeline sanity: leakage, alignment, units, NaNs, numeric failures | A bug read as an economic or product result |
| Data budget respected: holdout read only when approved, then once | A "confirmation" tuned on the very data it claims to confirm |
| Trials counted by independent hypothesis, and reported | Best-of-N presented as a single test |

Report checks that failed or were skipped as caveats. Never drop them silently.

## Step 3: Reconcile, one card per result

```
[R#] {question}
Theory      : {prediction from Step 1, or "post-hoc"}
Measured    : {paired difference vs baseline in the objective's units (ms, %, $),
               with its interval and n; both levels alongside}
Consistent? : consistent · partly · inconsistent · can't tell (within noise)
              — say which part held: direction / magnitude / location
Mechanism   : {why} [verified | supported | inferred | untested]
              if inconsistent: broken link = {which assumption}; next check = {smallest test}
```

**Verdict rules**
- **consistent**: direction and magnitude both match, beyond the noise floor.
- **partly**: direction matches but magnitude or location does not, or some segments match
  and others don't. Say which.
- **inconsistent**: the result points the other way, or a predicted effect is absent with
  enough power to have seen it. Being inconsistent is not a failure of the report; it is
  where the information is.
- **can't tell**: the difference is inside the noise floor, or the comparison was unfair.
  Say what n or what design would settle it.
- **A predicted null** ("writes should not change") is **consistent** when the interval
  excludes any effect large enough to matter. State that size; otherwise it is can't tell.
- **untraceable** (used by the auditor): the number cannot be found in the artifacts →
  treat as can't tell until it is traced.

**Mechanism evidence tiers**
- `verified`: a targeted test was run that would have come out differently if the
  mechanism were false (an ablation, a counterfactual replay, a decomposition that adds up).
- `supported`: the data fits the mechanism, but no discriminating test was run.
- `inferred`: a plausible story with no check behind it.
- `untested`: named only so it can be tested later.

**When theory and result disagree, walk this order.** It goes from the cheapest
explanation to the most expensive:
1. **Our pipeline.** Bug, leakage, misalignment, unit/scale error, numeric failure
   (saturation, overflow, NaN masking). A numeric failure gets fixed first. It is not
   evidence against the idea.
2. **Our comparison.** Baseline mismatch, confound, power too low, wrong segment.
3. **Our metric.** The proxy moved and the objective did not, or the other way round.
4. **Our theory.** A specific link in the chain is wrong. Name it.
5. **The environment** (market regime, traffic mix, hardware), and only with evidence.
   "The market changed" and "the users are different" are hypotheses to test, not
   conclusions.

**Then answer three questions.** What would have to be true for the theory to still hold?
What is the smallest check that tells the candidate mechanisms apart? What adjustment would
make the idea work, and how would you verify it without reusing data you have already
spent?

## Step 4: Report

Report and Decision lanes deliver in this order (Note lane: the one-line card only):

```
Result lane: {lane} — {reason}

1. Bottom line       — 1–3 lines. The rule verdict (if any) and the direction verdict,
                       stated separately.
2. Summary table     — | Question | Theory | Measured | Consistent? | Mechanism [tier] |
3. Cards             — Step 3 cards for the rows that need more than one table cell
4. Facts / Inferences / To test
                     — three short lists, kept apart
5. Caveats           — failed or skipped Step 2 checks; post-hoc theories; proxy metrics
6. Not checked       — at least one item. Never empty
7. Next              — the smallest discriminating checks, each with the data it would
                       consume and whether it needs approval
```

**Rule verdict vs direction verdict**
- Rule verdict: in the frozen rule's own labels (e.g. `PASS · FAIL · UNCERTAIN`), or
  `descriptive only`. If the result lands exactly on a boundary the rule does not cover, say so
  and ask. Do not resolve it in your own favour.
- Direction verdict: `alive · alive-but-constrained · weakened · dead`, with the reason.
  A single failed run rarely makes a direction `dead`. One configuration failed;
  say which assumption the failure constrains. A good mechanism, in turn, does not turn a
  rule `FAIL` into a `PASS`. It only justifies a new, pre-registered test.
- A descriptive result is never upgraded into an adoption decision in the same report.
- A screen can only eliminate. Passing a screen means "not eliminated", never PASS or
  confirmation.
- A pooled result never covers for a failed independent batch. Report the batch
  that failed by itself first.

</Steps>

<Anti_Patterns>
Each of these came up in real research and cost a decision:

| Pattern | What it looks like | Instead |
|---------|-------------------|---------|
| Verdict without theory | "Didn't pass, dropping it" | Name the broken link and the next check |
| Story-fitting | A mechanism invented after the result, stated as fact | Tag it `inferred`; propose the discriminating test |
| Rescue by mechanism | "It failed, but the mechanism is sound, so it passes" | Rule verdict stands; direction can stay alive |
| Proxy drift | Average accuracy improves while the cases that drive the decision (top-ranked items, slowest requests) get worse | Report the decision-relevant metric first |
| Blunting to hit a cost metric | Delaying or averaging the output lowers a cost metric and also lowers accuracy and timeliness | Fix cost where it arises; don't degrade the core output |
| Unequal comparison | 3 runs vs 5; different date ranges; different populations | Match both sides, or say "can't tell" |
| Best-window reporting | The 3 good weeks out of 10; the best region | Report all of them |
| Pooled masking | The pooled result passes while the replication batch alone fails | Lead with the failed batch |
| Silent gate | A diagnostic gets used as a rejection line | Step 1.4: explain, get approval, apply going forward only |
| Retroactive rule | A new threshold re-judges old results | Rules apply from their approval onward |
| Blame the world | "Regime change" with no evidence | Check pipeline → comparison → metric → theory first |
| Numeric failure as idea failure | A NaN-masked loss or an overflowed counter reported as "approach X doesn't work" | Fix the numerics, then rerun |
| Undefined terms | "Rare event", "accuracy", "return" used in shifting senses | Define each term before measuring |
</Anti_Patterns>

<Examples>
<Good>
```
Result lane: decision — ship/no-ship for a shorter checkout form, pre-registered rule.
Frozen rule (verbatim): "Ship if the conversion-lift 95% CI lower bound > 0 and the
refund-rate increase is < 0.3 pt."

Bottom line: rule verdict FAIL (lower bound −0.1 pt). Direction: alive-but-constrained.
The lift is where the theory said it would be (mobile) and absent where it said it would
be absent (desktop), which dilutes the overall number.
Noise floor: last month's A/A test, ±0.4 pt on conversion.

| Question | Theory | Measured | Consistent? | Mechanism [tier] |
|---|---|---|---|---|
| Overall conversion lift? | Fewer fields → fewer abandons → about +1.0 pt | +0.5 pt [−0.1, +1.1], n = 48k per arm | partly: direction yes, size half | Diluted by desktop (next row) [supported] |
| Where does it show up? | Mobile about +1.5 pt (typing is costly); desktop ≈ 0 (a gain ≥ 1 pt would matter) | Mobile +1.3 [+0.4, +2.2]; desktop −0.1 [−0.9, +0.7] | consistent, including the predicted null | Typing cost on small screens [verified: per-field abandon events fell on mobile only, which a design-wide effect would not produce] |
| Refunds unchanged? | No mechanism links form length to refunds | +0.1 pt [−0.2, +0.4] | can't tell: upper bound crosses 0.3 | none proposed [untested] |

Facts: mobile lift; desktop null; overall CI crosses 0.
Inferences: none beyond the tiers above.
To test: refund effect at a larger n.
Not checked: novelty effect after week 2.
Next: pre-register a mobile-only test under the same rule. It uses fresh traffic and
needs your approval. This run's FAIL stands.
```
Why good: each prediction has a size and a location, including where the effect should
not appear. The predicted null is judged against a stated size that matters. The mechanism
earns `verified` from a split that could have come out the other way. The rule verdict
stays FAIL while the direction stays alive, and the next step is a new pre-registered test,
not a reinterpretation of this one.
</Good>

<Good>
```
[R1] Does the read-through cache cut API p95?
Theory      : 80% of reads repeat within 60s → hit rate ~0.8 → p95 roughly halves.
              Writes should not change.
Measured    : read p95 −41 ms (412 → 371, −10%), 5 reruns, spread ±15 ms; hit rate 0.31;
              write p95 +2 ms ±8 (a regression ≥20 ms would matter).
Consistent? : partly — direction yes, magnitude no; writes flat as predicted.
Mechanism   : broken link = "80% repeat". The cache key includes the session ID, so
              repeats from different sessions miss [supported: the key format explains
              a 0.31 hit rate].
              Next check: replay one hour of logs with a session-free key; the predicted
              hit rate is ≥0.7.
```
Why good: the magnitude miss is traced to one link. The writes-flat half shows the
change did no damage. The next check is cheap and can fail.
</Good>

<Bad>
```
New ranking model: NDCG 0.412 vs baseline 0.418. Doesn't pass, dropping this direction.
```
Why bad: no theory, no noise floor (is 0.006 within run-to-run spread?), no check that the
runs and query sets matched, no broken link named. A direction got discarded on one confounded number.
</Bad>

<Bad>
```
It failed the pre-registered latency guard in one region, but that is clearly traffic
noise and the design is sound, so we treat it as passing.
```
Why bad: the rule verdict was rewritten by an untested environmental story. The correct
report is "rule verdict FAIL; direction alive-but-constrained because …; next
pre-registered test …".
</Bad>
</Examples>

<Fresh_Context_Check>
The context that wrote the theory and ran the measurement is the one most likely to
believe its own mechanism. For Report and Decision lanes, hand the cards (not your
conclusion) to the `mechanism-auditor` agent when it is available, or to any fresh
subagent. Ask it to downgrade any tier the evidence does not support, to name an
alternative mechanism that fits the same numbers, and to propose the cheapest
discriminating check. Without subagents, do it yourself and label it
`same-context audit — weaker`.
</Fresh_Context_Check>

<Final_Checklist>
- [ ] Lane announced; Decision lane quotes the frozen rule verbatim
- [ ] Theory written before the result, or marked `post-hoc`
- [ ] Prediction states direction, magnitude and location; noise floor stated
- [ ] Comparison matched (data, coverage, seeds, metric, mapping), or confounds named
- [ ] Objective metric reported first; proxies labelled
- [ ] Every result has all four parts; every mechanism has a tier
- [ ] Every mismatch names the broken link and the smallest next check
- [ ] Rule verdict and direction verdict kept separate; no rescue, no dismissal
- [ ] No new or tightened threshold applied without plain-language explanation and approval
- [ ] Facts / inferences / to-test kept apart; "Not checked" non-empty
- [ ] Next checks state the data they would consume and whether approval is needed
</Final_Checklist>

<Relationship_To_Sibling_Tooling>
- `finding-unknowns`: Phase 0 captures the prior and Cartographer's `experiment` route
  defines what to run. When the measurement returns, report it here and write the
  ledger row's resolution from the card.
- `keep-the-reasoning`: when the handoff concerns measured claims, packet section 4
  (Prior vs result) *is* this skill's summary table, and section 7 (Not checked) is
  shared. Don't write it twice.
- `mechanism-auditor` (this repository): the fresh-context tier audit described above.
- `oh-my-claudecode:verify` proves a behaviour works. This skill explains a measured
  effect and its size. `oh-my-claudecode:trace` is a stronger competing-hypothesis
  tool for the Step 3 disagreement walk when installed.
</Relationship_To_Sibling_Tooling>
