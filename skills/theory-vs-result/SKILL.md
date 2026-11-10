---
name: theory-vs-result
description: "Use when a benchmark, backtest, A/B test, training or load-test result is planned or comes back, a failing test or crash whose cause isn't obvious, or the user asks 'is this consistent', 'why did this happen', 'does it pass', '理论 → 实测 → 机理'. Reports Theory → Measured → Consistent? → Mechanism, prediction first. Not for results nothing rides on."
aliases: [theory-measured-mechanism, predict-measure-explain]
metadata:
  credits:
    source: "Distilled from the author's own empirical research practice (baizhiyuan), generalized for any measured claim"
    sibling: "finding-unknowns (unknowns before work) and keep-the-reasoning (the handoff) — this repository"
    related-practice: "pre-registration; equivalence testing with a smallest effect of interest; multiple-testing and effective-trial corrections"
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
  tests, ablations, training runs, load tests, profiling, a bug fix's measured effect
- A reproducible failure whose cause isn't obvious — a failing test, a crash, the same wrong
  output for the same input every time → the Debug path (Step 0)
- Before running such a measurement: write the prediction and decision rule first
- The user asks "why", "is this consistent", "does it pass", "should we drop this"
- A result contradicts the expectation, or sits close to a threshold
- A `finding-unknowns` ledger row with route `experiment` comes back with data
- The Prior vs result section of a `keep-the-reasoning` packet concerns a measured claim
</Use_When>

<Do_Not_Use_When>
- Nothing was predicted and nothing is decided (a lookup, a status read, a log grep).
  If a prediction exists but little rides on it, use the Note level instead
- The work is building, not measuring. Use `finding-unknowns` before it and
  `keep-the-reasoning` at the handoff
- A one-off sanity number with no decision attached. One sentence is enough: "measured X,
  expected roughly X, no action"
- A failure whose cause the error message already names (a typo, a missing import, a
  stack trace pointing at one line): just fix it
</Do_Not_Use_When>

<Execution_Policy>
- **Theory before data.** Write the prediction before looking at the result, and record
  when it was written. The Theory is the measured-claim form of a *prior* (the
  expectation recorded before the result; see Step 1). A theory written afterwards is
  labelled `post-hoc`: it can only produce a *post-hoc fit*, never a test (Step 3)
- **Predict magnitude and location, not just sign.** "Faster" cannot fail. "~2× on cold
  reads, ~0 on warm" can
- **Noise floor first.** No consistency verdict until you know how big a difference
  noise produces (seeds, reruns, windows, bootstrap). A difference inside it gets
  "can't tell", not "consistent". When the data holds reruns, compute that spread and an
  interval for the difference before any headline; the headline is the verdict
- **Fair comparison or no comparison.** Same data, same coverage, same seeds/runs, same
  metric definition, same evaluation pipeline (how outputs become actions). Change one
  variable at a time, or say the change was confounded
- **The metric must be the objective.** Report the metric that is actually shipped,
  paid for or decided on. A convenient proxy is supporting evidence only
- **Mechanism has an evidence tier.** Every explanation carries one of
  `verified · supported · inferred · untested`. Never present an `inferred` mechanism
  untagged or as established
- **A mismatch names the broken assumption.** Say which link in the theory's chain failed,
  give the smallest check that would tell the candidate explanations apart, and say what
  adjustment would let the idea hold
- **Two verdicts, never merged.** The *rule verdict* (what the pre-agreed rule says) is
  final for this run. The *direction verdict* (is the idea alive) is a judgment. A
  mechanism can keep a direction alive, but it cannot overturn a rule verdict, and
  neither can a rerun or a claim that the rule's metric was "only a proxy"
- **Rules are explained before they are frozen.** Any new or tightened threshold is
  explained in plain language and approved by the user before it applies (Step 1.4)
- **Deterministic failures take the Debug path.** A failure that reproduces the same way
  every time has no noise floor and needs no frozen rule; record it on the Debug path
  (Step 0) and escalate to a rigor level only when it is flaky or a ship/no-ship rides
  on it
- **Report in the user's language.** Chinese labels: 理论预期 → 实测 → 是否一致 → 机理;
  一致 · 部分一致 · 不一致 · 无法判断 · 事后拟合; 已验证 · 有数据支持 · 推断 · 未检验;
  仍成立 · 有条件成立 · 已削弱 · 已否定; 作废
</Execution_Policy>

<Steps>

## Step 0: Triage (blocking)

First ask: is the "result" a **reproducible, deterministic failure** — same input → same
wrong output, a crash, a failing test? Then take the **Debug path** below, not a rigor
level. Otherwise choose the rigor level:

| Rigor level | Signals | Output |
|-------------|---------|--------|
| **Note** | one number, a prediction exists, low stakes, no decision rides on it | one-line card: `[R#] expected {X}, measured {Y} → {verdict}; no action` |
| **Report** | a result someone will act on; a mismatch; near a threshold | full cards + summary table (Step 4) |
| **Decision** | adopt/reject, ship/no-ship, a pre-registered test, money or production | Report, plus the frozen rule quoted verbatim and the rule verdict separated from the direction verdict. No frozen rule → propose one via Step 1.4 and stop; the decision is the user's. A rule approved after this result was seen does not apply to it: this result stays `descriptive only` |

Announce: `Rigor level: {note | report | decision} — {one-line reason}`, or
`Debug path — {one-line reason}`.

### Debug path (reproducible, deterministic failures)

When the failure comes back the same way every run, the repro *is* the experiment: there
is no noise floor to estimate and no data budget to spend. Record six things, in order:

```
Debug path — {one-line reason}
1. Repro        : `{exact command}` → {observed output, trimmed, not paraphrased}
2. Prior        : what you expected it to output
3. Explanations : the competing explanations, at least two, before touching the code
4. Checks       : one discriminating check per explanation, cheapest first, each with
                  its outcome (a print, a minimal input, a bisect, one variable changed)
5. Fix          : what changed, by path
6. Re-run       : the same repro → the expected output; plus one neighbouring case that
                  should not change → unchanged
```

No frozen rule, no pre-registration, no fresh-run requirement beyond re-running the repro.
An explanation whose check was never run stays a guess; say so. **Escalate to a rigor
level** when the failure is flaky or statistical (it does not reproduce every run, so a
noise floor exists: Report) or when the fix decision is a ship/no-ship (Decision).
`superpowers:systematic-debugging`, when installed, can drive the investigation (items
3–5); this path records the result.

## Step 1: Before measuring, write the theory (prediction card)

The prediction card is the measured-claim form of a **prior** — the expectation recorded
before the result, as `finding-unknowns` and `keep-the-reasoning` call it: Theory = prior +
mechanism chain. A prior already recorded in this session by either sibling (a Phase 0
prior, a ledger row's `prior:`, a handoff's Step 1 prior) is reused as the card's starting
point, never asked again; sharpen it into direction, magnitude and location.

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
Trials so far    : raw configurations tried for this claim, and the effective number of
                   independent hypotheses among them (both, cumulative across reports)
Terms            : definitions of any term that could shift meaning ("accuracy", "return", "rare")
Written          : {timestamp | commit | "before opening <path>"}
```

At the Report and Decision levels, save the card before measuring (default
`.finding-unknowns/predictions/{slug}.md` at the project root, or the Cartographer ledger
row it belongs to). An unsaved card whose timing cannot be shown counts as `post-hoc`.
A pre-4.3 card at root `predictions/{slug}.md` is read in place (its `Written` line
stands); offer the move into `.finding-unknowns/predictions/`, never move silently.
`.finding-unknowns/` is working state and usually gitignored; a gitignored card cannot
use a commit as its `Written` line, so give a timestamp, or commit the card when its
timing must survive review (`git add -f` the card, since the directory is ignored).

1. **Scale the card to the stakes.** At the Note level the Prediction line alone is enough.
2. **Locate the effect.** Most real mechanisms act on a subset: the tails of a ranking, cold
   caches, small accounts, peak hours. Say where the effect should appear and
   where it should *not*. The "should not" half is often the sharper test.
3. **Name the chain.** "Feature X carries information → the model learns it → the
   decisions that act on it change → the outcome metric improves" has four links. When the
   result misses, Step 3 has to say which link broke.
4. **Threshold gate.** If you are proposing a new or tighter pass/fail line, stop. Explain
   to the user in plain words: **what it protects against, why this number, what failing it
   means, and what it might wrongly reject.** Freeze it only after the user approves, and
   record the approval. Until then it stays a diagnostic. A diagnostic never quietly turns
   into a gate, and a rule applies only from its approval onward, never retroactively.
5. **If the result is already in hand**, write the card anyway and mark it `post-hoc`.
   Do not "predict" what you have already seen. A post-hoc card is limited (Step 3): its
   verdict is `post-hoc fit`, its mechanism tier is at most `inferred`, it never feeds a
   rule verdict, and the report must include a prediction card for a fresh run. A result
   that exists but has not been opened can still get a genuine prediction, if the card's
   `Written` line shows it.
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
| The same number of seeds/reruns on both sides (state N); independent batches reported separately | A lucky seed; a pooled result hiding a failed replication |
| All windows/segments reported, not the best ones | Cherry-picking periods, seeds or regimes |
| Metric = objective; proxies labelled as proxies | A metric that improves while what you are paid for gets worse |
| Pipeline sanity: leakage, alignment, units, NaNs, numeric failures | A bug read as an economic or product result |
| Data budget respected: holdout read only when approved, then once; budget carried forward across reports on the same claim | A "confirmation" tuned on the very data it claims to confirm |
| Trials reported as raw configurations and as effective independent hypotheses, cumulative across reports | Best-of-N presented as a single test |

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
- **The interval governs.** Direction counts as matched only when the interval (CI, or the
  spread across reruns) excludes 0; magnitude only when it excludes sizes that would
  contradict the prediction. An interval that contains both 0 and the predicted size is
  `can't tell`. The noise floor informs how wide that interval is; it does not replace it.
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
- **post-hoc fit**: the card's theory was written after the result was seen. It is not a
  test. Report it as `post-hoc fit (not a test)`, cap the mechanism tier at `inferred`
  unless a later, separately predicted test was run, keep it out of any rule verdict, and
  add a prediction card for a fresh run.
- **Falsifier.** If the Step 1 falsifier fired, say so on the card. A direction can be
  called `dead` only on a fired falsifier, or on independent failures that each name the
  same broken link.

**Mechanism evidence tiers** (the tier `verified` grades a *mechanism*; it is not a claim
"verified" under a `keep-the-reasoning` or Cartographer verification contract, which means
its contract checks ran and could have failed)
- `verified`: a targeted test was run that would have come out differently if the
  mechanism were false (an ablation, a counterfactual replay, a decomposition whose parts
  were measured independently and could have failed to sum to the total; an accounting
  identity always sums and is not a test).
- `supported`: the data fits the mechanism, but no discriminating test was run.
- `inferred`: a plausible story with no check behind it.
- `untested`: named only so it can be tested later.

**When theory and result disagree, walk this order.** It goes from the cheapest
explanation to the most expensive:
1. **Our pipeline.** Bug, leakage, misalignment, unit/scale error, numeric failure
   (saturation, overflow, NaN masking). A defect found after the result does not convert
   the result: the run is marked `void: pipeline defect` and its rule verdict is `void`.
   A void must name the defect with evidence and show that it changes the headline
   number; otherwise the original verdict stands. The original verdict stays visible
   (`FAIL → void: {defect, evidence}`), and the auditor checks the claim.
   A rerun after the fix is a new run. On fresh data it can be confirmatory; on data
   already read (holdout, forward period) it is labelled `re-read, not confirmatory` and
   needs the user's approval before it runs. Check runs that passed for the same defect
   class too: bugs found only after failures are a one-sided search.
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

Report and Decision levels deliver in this order (Note level: the one-line card only):

```
Rigor level: {level} — {reason}

0. Frozen rule        — Decision level only: quoted verbatim, with its approval date
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
  `descriptive only`, or `void` (pipeline defect, Step 3). It is computed on the rule's
  own metric as defined when the rule was frozen. An argument that this metric was a proxy
  feeds the direction verdict and the next rule proposal, never this verdict. If the
  result lands exactly on a boundary the rule does not cover, say so and ask. Do not
  resolve it in your own favour.
- Direction verdict: `alive · alive-but-constrained · weakened · dead`, with the reason.
  `dead` needs a fired falsifier or independent failures naming the same broken link;
  otherwise `weakened` at most. A single failed run rarely makes a direction `dead`. One
  configuration failed; say which assumption the failure constrains. A good mechanism, in
  turn, does not turn a rule `FAIL` into a `PASS`. It only justifies a new, pre-registered
  test.
- A descriptive result is never upgraded into an adoption decision in the same report.
- A screen (a cheap pre-filter run before the real test) can only eliminate. Passing a
  screen means "not eliminated", never PASS or confirmation.
- A pooled result never covers for a failed independent batch. Report the batch
  that failed by itself first.

</Steps>

<Anti_Patterns>
Recurring failures in empirical work. Each costs a decision when it goes unnoticed:

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
| Numeric failure as idea failure | A NaN-masked loss or an overflowed counter reported as "approach X doesn't work" | Mark the run `void`, fix the numerics, rerun on fresh data (or a re-read with approval) |
| Void-and-rerun rescue | A failed run is voided for a bug, rerun on the same holdout, and the new PASS reported as confirmation | A re-read is `not confirmatory`; audit passing runs for the same bug |
| Post-hoc as prediction | A theory written after seeing the result, reported as `consistent [supported]` | `post-hoc fit (not a test)`, tier ≤ `inferred`, plus a prediction card for a fresh run |
| Undefined terms | "Rare event", "accuracy", "return" used in shifting senses | Define each term before measuring |
</Anti_Patterns>

<Examples>
<Good>
```
Rigor level: decision — ship/no-ship for a shorter checkout form, pre-registered rule.
Frozen rule (verbatim, approved before launch): "Ship if the conversion-lift 95% CI lower
bound > 0 and the refund-rate increase is < 0.3 pt."

Bottom line: rule verdict FAIL (lower bound −0.1 pt). Direction: alive-but-constrained.
The overall effect cannot be told apart from zero, but the lift is where the theory said
it would be (mobile) and absent where it said it would be absent (desktop).
Noise floor: last month's A/A test, ±0.4 pt on conversion.

| Question | Theory | Measured | Consistent? | Mechanism [tier] |
|---|---|---|---|---|
| Overall conversion lift? | Fewer fields → fewer abandons → about +1.0 pt | +0.5 pt [−0.1, +1.1], n = 48k per arm | can't tell: the CI spans both 0 and the predicted +1.0 | Diluted by desktop (next row) [supported] |
| Where does it show up? | Mobile about +1.5 pt (typing is costly); desktop ≈ 0 (a gain ≥ 1 pt would matter) | Mobile +1.3 [+0.4, +2.2]; desktop −0.1 [−0.9, +0.7] | consistent, including the predicted null | Typing cost on small screens [verified: abandon events fell only at the three typing-heavy fields and only on mobile; a design-wide or scroll-length effect would also have moved the non-typing fields, and it did not] |
| Refunds unchanged? | No mechanism links form length to refunds | +0.1 pt [−0.2, +0.4] | can't tell: upper bound crosses 0.3 | no mechanism named (no tier) |

Facts: mobile lift; desktop null; overall CI crosses 0.
Inferences: none beyond the tiers above.
To test: refund effect at a larger n.
Caveats: none of the Step 2 checks failed; the prediction card was saved before launch.
Not checked: novelty effect after week 2.
Next: pre-register a mobile-only test under the same rule. It uses fresh traffic and
needs your approval. This run's FAIL stands.
``` Why good: each prediction has a size and a location, including where the effect should
not appear. The overall row is `can't tell`, not "partly", because its interval holds both
0 and the prediction. The predicted null is judged against a stated size that matters. The
mechanism earns `verified` from a split that could have come out the other way. The rule
verdict stays FAIL while the direction stays alive, and the next step is a new
pre-registered test, not a reinterpretation of this one.
</Good>

<Good>
```
[R1] Does the read-through cache cut API p95?
Theory      : 80% of reads repeat within 60s → hit rate ~0.8 → p95 roughly halves.
              Writes should not change.
Measured    : read p95 −41 ms (412 → 371, −10%), 5 reruns, spread ±15 ms; hit rate 0.31;
              write p95 +2 ms ±8 (a regression ≥20 ms would matter).
Consistent? : partly — direction yes, magnitude no; writes flat as predicted.
Mechanism   : broken link = "a repeat is a cache hit". Reads do repeat, but the cache
              key includes the session ID, so repeats from different sessions miss
              [supported: the key format explains a 0.31 hit rate].
              Next check: replay one hour of logs with a session-free key; the predicted
              hit rate is ≥0.7.
```
Why good: the magnitude miss is traced to one link. The writes-flat half shows the
change did no damage. The next check is cheap and can fail.
</Good>

<Bad>
```
New ranking model: NDCG 0.412 vs baseline 0.418. Doesn't pass, dropping this direction.
``` Why bad: no theory, no noise floor (is 0.006 within run-to-run spread?), no check that
the runs and query sets matched, no broken link named. A direction got discarded on one
confounded number.
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
This is the **fresh-context refutation** primitive (shared across these skills; defined
in `keep-the-reasoning`): a context that did not produce the claim tries to refute it from
the same evidence and returns the strongest alternative explanation plus the cheapest
discriminating check. Here it runs per card, with verdict and tier downgrades on top.

The context that wrote the theory and ran the measurement is the one most likely to
believe its own mechanism. For the Report and Decision levels, hand the auditor the
inputs, not your conclusion: the cards, the saved prediction card with its `Written`
line, the frozen rule quoted verbatim, and the paths of the artifacts behind every number
(without paths, every card comes back `untraceable`). Use the `mechanism-auditor` agent
when it is available, or any fresh subagent. Ask it to downgrade any verdict or tier the
evidence does not support, to name an alternative mechanism that fits the same numbers
for every card (including `consistent` ones), and to propose the cheapest discriminating
check.

Apply the audit: downgrades take effect as given; where you disagree, keep the audit's
reading and put yours in Caveats; the alternative mechanisms and checks go into Next, and
into the `keep-the-reasoning` packet when a handoff follows (Strongest counterargument
and Did I miss anything? in the full packet; under Not checked in the compact one).
Without subagents, do the audit yourself and label it `same-context — weaker`.
</Fresh_Context_Check>

<Final_Checklist>
- [ ] Rigor level or Debug path announced; the Decision level quotes the frozen rule
      verbatim
- [ ] Debug path: repro + observed output, prior, competing explanations, a check for each
      (cheapest first), fix, the same repro re-run plus one unchanged neighbour; escalated
      to a rigor level if flaky or ship/no-ship. The items below apply to rigor levels
- [ ] Theory written before the result with its `Written` line, or marked `post-hoc`
      (then: `post-hoc fit`, tier ≤ `inferred`, no rule verdict, prediction card for a fresh run)
- [ ] Every verdict reads the interval: one that holds both 0 and the prediction is `can't tell`
- [ ] Defects found after the result void the run; any re-read of spent data is labelled and approved
- [ ] Prediction states direction, magnitude and location; noise floor stated
- [ ] Comparison matched (data, coverage, seeds, metric, evaluation pipeline), or confounds named
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
- `keep-the-reasoning`: when the handoff concerns measured claims, the packet's Prior vs
  result section (a line in the compact packet) *is* this skill's summary table, and its
  Not checked section is shared. Don't write it twice.
- `mechanism-auditor` (this repository): the fresh-context tier audit described above.
- `oh-my-claudecode:verify` proves a behaviour works. This skill explains a measured
  effect and its size. `oh-my-claudecode:trace` is a stronger competing-hypothesis
  tool for the Step 3 disagreement walk when installed.
- `superpowers:systematic-debugging` can drive a deterministic-failure investigation
  when installed; the Debug path (Step 0) records its result.
</Relationship_To_Sibling_Tooling>
