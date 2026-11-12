# Results: Theory → Measured → Consistent? → Mechanism

*From the author's research practice.*

A number alone is not a finding. Two failures follow. **Dismissal**: a bad result drops
a good direction without asking which assumption broke. **Rescue**: a later story
overturns a rule agreed before the run. So every result is one four-part entry, and the
frozen rule's verdict stays apart from the judgement on the direction.

Chinese labels: 理论预期 → 实测 → 是否一致 → 机理; 一致 · 部分一致 · 不一致 · 无法判断 ·
事后拟合; 已验证 · 有数据支持 · 推断 · 未检验; 仍成立 · 有条件成立 · 已削弱 · 已否定; 作废.

## How much to write (decide silently)

- **Note**: one number, a prediction exists, nothing rides on it. One line:
  `[R#] expected {X}, measured {Y} → {consistent?}; no action`.
- **Report**: someone will act on it, a mismatch, or near a threshold. Result entries plus
  the reporting block below.
- **Decision**: adopt or reject, ship or not, money or production. Report, plus the frozen
  rule quoted verbatim, with the two verdicts kept apart. No frozen rule: propose one
  (threshold gate) under `Needs you`; the decision is the person's, and a rule approved
  after seeing the result does not apply to it: `descriptive only`.

## Debug path (reproducible, deterministic failures)

The repro is the experiment; no noise floor. Record in order:

```
1. Repro        : `{exact command}` → {observed output, trimmed}
2. Prior        : what you expected it to output
3. Explanations : at least two, before touching the code
4. Checks       : one discriminating check per explanation, cheapest first, with outcome
5. Fix          : what changed, by path
6. Re-run       : the same repro → expected output; one neighbouring case → unchanged
```

An unchecked explanation is a guess. Flaky: Report. A ship decision rides on it:
Decision.

## Before measuring: the claim file

The Brief for a claim: `.finding-unknowns/predictions/{slug}.md`, saved before running
(or before opening an existing result) and committed by `fu freeze`, which writes its
`Timing:` line. `self-reported` timing labels every verdict resting on it; written after
the result was opened means `post-hoc`.

```
Claim under test  : {one sentence}
Mechanism chain   : A → B → C   (each link can fail on its own)
Person prediction : their words verbatim ({confidence}), or `none given`; never authored
Agent prediction  : direction + rough size + where it shows up, written after theirs
Should not change : where the effect should be absent, and the size that would matter
Noise floor       : how measured (≥ 3 reruns or an A/A comparison), and its size
Stopping rule     : seeds, runs or windows before any verdict
Falsifier         : the result that would show the claim is wrong
Decision rule     : the pre-agreed rule, verbatim; else "descriptive only"
Data budget       : what this run uses up (holdout, fresh traffic, forward period)
Trials so far     : raw configurations tried; effective independent hypotheses
Written           : {date; "before running" | "before opening <path>"}
```

- At Note level the prediction lines are enough; the person's and the agent's
  disagreement is the most informative row.
- **Locate the effect**: most mechanisms act on a subset (tails, cold caches).
- **Noise floor before any rule**, or no signal calls.
- **Threshold gate**: a new or tighter pass line is explained in plain words first (what
  it protects, why this number, what failing means, what it might wrongly reject), frozen
  only on the person's approval, applied only from then on.
- **Result already in hand**: write it anyway, marked `post-hoc`: consistent? is
  `post-hoc fit (not a test)`, tier at most `inferred`, never feeds a rule verdict; add a
  claim file for a fresh run. **No theory at all**: `exploratory`, rule verdict
  `descriptive only`.

## Run log

Append-only in the claim file: `{date} · {run} · {config} · {what changed} · {result} ·
{cumulative trials} · {data spent}`. Before the stopping rule, no verdict on interim
results. Failed and voided runs stay.

## Measure fairly

Each failed or skipped check is a caveat: matched baseline (window, coverage,
seeds, pipeline); one variable changed or confounds named; a simple baseline; equal
reruns (state N), independent batches apart; all segments, not the best; proxies
labelled; leakage, units, NaNs; holdout read once, when approved. Overlapping windows are
not independent.

## The result entry

```
[R#] {question}
  - theory: {the frozen prediction, quoted by ID, or "post-hoc"}
  - measured: {paired difference vs baseline, objective's units, interval, n}
  - consistent?: {consistent | partly | inconsistent | can't tell}; which part held:
    direction / magnitude / location
  - mechanism: {why} [verified | supported | inferred | untested]
  - if inconsistent: broken link = {assumption}; next check = {smallest test}
```

- **The interval governs.** Direction matches only when the interval excludes 0;
  magnitude only when it excludes contradicting sizes. An interval holding both 0 and the
  predicted size is `can't tell`.
- `consistent`: direction and magnitude match beyond noise. `partly`: direction only, or
  some segments; say which. `inconsistent`: the other way, or a predicted effect absent
  with power to see it. `can't tell`: inside the noise or an unfair comparison; say what
  would settle it. A predicted null is `consistent` only when the interval excludes any
  effect that matters. `untraceable`: the number is not in the artifacts; `can't tell`.
- **Tiers.** `verified`: a test that would have come out differently if the mechanism
  were false (an accounting identity is not one). `supported`: fits, no discriminating
  test. `inferred`: plausible, unchecked. `untested`: named so it can be tested. Never
  untagged.

**When theory and result disagree**, walk cheapest first:

1. **Pipeline**: bug, leakage, misalignment, units. `void: pipeline defect` only with
   evidence that it changes the headline number; the original verdict stays visible. A
   rerun on data already read is `re-read, not confirmatory`: propose it under `Needs you`.
2. **Comparison**: baseline mismatch, confound, low power, wrong segment.
3. **Metric**: the proxy moved and the objective did not, or the reverse.
4. **Theory**: name the broken link, or the candidates and the check that separates them.
5. **Environment**, only with evidence.

## Reporting: two verdicts, never merged

As nested lists: (Decision) the frozen rule and its approval date; a one-to-three-line
bottom line; result entries; facts, inferences and to-test apart; caveats; not checked
(never empty); next checks with the data each consumes and whether it needs approval.

- **Rule verdict**: the rule's own labels (`PASS · FAIL · UNCERTAIN`), `descriptive only`
  or `void`, computed on the rule's metric as frozen. "The metric was a proxy" feeds the
  direction verdict, never this one. A result outside the rule's boundary: say so under
  `Needs you`.
- **Direction verdict**: `alive · alive-but-constrained · weakened · dead`, with the
  reason. You propose it; the person owns it. `dead` needs a fired falsifier or
  independent failures naming the same link; one failed run constrains an assumption.
- A good mechanism never turns `FAIL` into `PASS`; it justifies a new pre-registered test.
  A pooled result never covers a failed independent batch.

**Audit.** At Report and Decision levels, `mechanism-auditor` gets the result entries
with `consistent?`, `mechanism` and `if inconsistent` stripped, the claim file, the frozen
rule and the artifact paths, never your write-up. Its verdicts and tiers stand; caveats show where
yours differed. Without subagents: `same-context — weaker`.
