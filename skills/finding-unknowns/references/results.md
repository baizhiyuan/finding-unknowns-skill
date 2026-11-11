# Results: Theory → Measured → Consistent? → Mechanism

*From the author's own empirical research practice. Theory lives inside engineering;
engineering is built on theory.*

A measured number on its own is not a finding. "accuracy 91 %", "p95 down 8 %", "loss went
up" tell the reader nothing until they know what was expected, whether the gap is bigger
than noise, and why it happened. Two failures follow from leaving that out, in opposite
directions. **Dismissal**: the theory was good, the result was bad, and the direction is
thrown out without anyone asking which assumption broke. **Rescue**: the result was bad,
a story is told afterwards, and the story quietly overturns a rule agreed before the run.
Every result is therefore reported as one four-part card, with facts, inferences and
untested explanations kept apart, and the verdict under the frozen rule kept apart from
the judgement about the direction.

Chinese labels: 理论预期 → 实测 → 是否一致 → 机理; 一致 · 部分一致 · 不一致 · 无法判断 ·
事后拟合; 已验证 · 有数据支持 · 推断 · 未检验; 仍成立 · 有条件成立 · 已削弱 · 已否定; 作废.

## How much to write

Decide silently; do not announce it.

| Level | When | Output |
|---|---|---|
| **Note** | one number, a prediction exists, nothing rides on it | one line: `[R#] expected {X}, measured {Y} → {verdict}; no action` |
| **Report** | someone will act on it; a mismatch; near a threshold | cards and a summary table |
| **Decision** | adopt or reject, ship or not, a pre-registered test, money or production | Report, plus the frozen rule quoted verbatim, and the rule verdict kept apart from the direction verdict. No frozen rule: propose one (threshold gate below) and stop; the decision is the person's. A rule approved after this result was seen does not apply to it; the result stays `descriptive only` |

A **reproducible, deterministic failure** (same input, same wrong output; a crash; a
failing test) takes the Debug path instead. A failure whose cause the error message
already names (a typo, a missing import, a stack trace pointing at one line): just fix
it.

## Debug path

The repro *is* the experiment: there is no noise floor and no data budget. Record six
things in order:

```
1. Repro        : `{exact command}` → {observed output, trimmed, not paraphrased}
2. Prior        : what you expected it to output
3. Explanations : at least two competing explanations, before touching the code
4. Checks       : one discriminating check per explanation, cheapest first, with its outcome
5. Fix          : what changed, by path
6. Re-run       : the same repro → the expected output; one neighbouring case that should
                  not change → unchanged
```

An explanation whose check was never run stays a guess; say so. Switch to a level when
the failure is flaky (a noise floor exists: Report) or a ship decision rides on the fix
(Decision).

## Before measuring: the prediction card

This is the Brief for a claim. Save it in `.finding-unknowns/predictions/{slug}.md`
before running anything, or before opening a result that already exists, and commit it
per `card.md`. Like a task card, the file starts with a header line
`Timing: frozen {date}, commit {hash} | self-reported`, written after the commit and
outside the frozen block. Timing:

- **commit:** the strongest evidence that the prediction came first;
- **self-reported:** graded as a prediction, but every verdict that rests on it carries
  the label `timing: self-reported`;
- **written after the result was opened,** or not saved before the run: `post-hoc`,
  whatever the Timing line says.

```
Claim under test   : {the belief, one sentence}
Mechanism chain    : A → B → C   (each link is an assumption that can fail on its own)
Your prediction    : direction + rough magnitude + where it shows up ({confidence})
Agent prediction   : the same, written after yours
Should not change  : where the effect should be absent, and the size that would matter
Noise floor        : measured how (≥ 3 reruns or an A/A comparison), and its size
Stopping rule      : how many seeds, runs or windows before any verdict
Falsifier          : the result that would show the claim is wrong
Decision rule      : the pre-agreed rule, quoted verbatim; else "descriptive only"
Data budget        : the data this run uses up (holdout, fresh traffic, forward period)
Trials so far      : raw configurations tried for this claim, and the effective number of
                     independent hypotheses among them (both cumulative across reports)
Terms              : definitions of any term that could shift meaning
Written            : {date; "before running" | "before opening <path>"}
```

1. **Scale the card.** At the Note level the prediction line alone is enough.
2. **The person's and the agent's predictions stay on separate lines.** Their
   disagreement is the most informative row.
3. **Locate the effect.** Most real mechanisms act on a subset: the tails of a ranking,
   cold caches, small accounts, peak hours. Say where it should appear and where it
   should not; the "should not" half is often the sharper test. When the magnitude
   cannot honestly be predicted, write "magnitude unknown; an effect ≥ X would matter".
4. **Name the chain.** When the result misses, the card must say which link broke.
5. **Measure the noise floor before freezing a rule.** At least three reruns or an A/A
   comparison. With fewer, the card says the floor itself is uncertain, and no verdict
   calls a difference signal on it. (A rule built on two runs once called +2.5 "signal";
   a third run reversed it.)
6. **Threshold gate.** A new or tighter pass/fail line is explained to the person in
   plain words first: what it protects against, why this number, what failing it means,
   what it might wrongly reject. It is frozen only after the person approves, applies
   only from then on, and never quietly turns a diagnostic into a gate.
7. **Result already in hand:** write the card anyway and mark it `post-hoc`. Its verdict
   is `post-hoc fit (not a test)`, its mechanism tier at most `inferred`, it never feeds a
   rule verdict, and the report includes a prediction card for a fresh run.
8. **No theory at all** (exploration that still feeds a decision): `exploratory`;
   Consistent? n/a; rule verdict `descriptive only`; include a prediction card for the
   next run.

## While results arrive: the run table

A claim outlives many runs. Keep an append-only table in the claim's file:

```
| date | run | config | what changed | result | cumulative trials | data spent |
```

- One line per run, plus a one-line Note card when it lands.
- Until the stopping rule is met, the state reads "3 of 5 seeds done, no verdict yet".
  Do not grade interim results; peeking at noisy interim numbers is research's version
  of an interruption.
- Failed and voided runs stay in the table. The latest success never replaces the
  history.
- The full Debrief runs at the declared stopping point.

## Measure fairly

Before trusting a difference, check each line; report the ones that failed or were
skipped as caveats, never silently.

| Check | Failure it prevents |
|---|---|
| Matched baseline: same data window, coverage, seeds/runs, population, evaluation pipeline | Crediting the change with what the sample did |
| One variable changed, or the confounds named | Crediting the architecture with what preprocessing did |
| Simplest baseline present | Complexity winning because nothing simple was tried |
| The same number of seeds or reruns on both sides (state N); independent batches reported separately | A lucky seed; a pooled result hiding a failed replication |
| All windows and segments reported, not the best ones | Cherry-picking |
| Metric = objective; proxies labelled as proxies | A metric improving while what you are paid for gets worse |
| Pipeline sanity: leakage, alignment, units, NaNs, numeric failures | A bug read as a product or economic result |
| Data budget respected: holdout read only when approved, then once | A "confirmation" tuned on the data it confirms |
| Trials reported raw and as effective independent hypotheses, cumulative | Best-of-N presented as one test |

Seed spread is not automatically a confidence interval, and overlapping or repeated
windows are not independent samples; use an analysis that fits the design.

## The card

```
[R#] {question}
Theory      : {the frozen prediction, quoted by ID, or "post-hoc"}
Measured    : {paired difference vs baseline in the objective's units, with its interval
               and n; both levels alongside}
Consistent? : consistent · partly · inconsistent · can't tell — which part held:
              direction / magnitude / location
Mechanism   : {why} [verified | supported | inferred | untested]
              if inconsistent: broken link = {assumption, or candidate links}; next check = {smallest test}
```

**Verdicts**

- **The interval governs.** Direction matches only when the interval (CI, or the spread
  across reruns) excludes 0; magnitude only when it excludes sizes that would contradict
  the prediction. An interval holding both 0 and the predicted size is `can't tell`. The
  noise floor informs how wide that interval is; it does not replace it.
- **consistent:** direction and magnitude both match, beyond the noise floor.
- **partly:** direction matches but magnitude or location does not, or some segments do
  and others don't. Say which.
- **inconsistent:** the result points the other way, or a predicted effect is absent with
  enough power to have seen it. This is where the information is, not a failure of the
  report.
- **can't tell:** inside the noise floor, or the comparison was unfair. Say what n or
  design would settle it.
- **A predicted null** is `consistent` when the interval excludes any effect large enough
  to matter. State that size; otherwise it is `can't tell`.
- **untraceable:** the number cannot be found in the artifacts; treat it as `can't tell`
  until traced.
- **post-hoc fit:** see the prediction card, item 7.
- **Falsifier:** if it fired, say so. A direction can be called `dead` only on a fired
  falsifier, or on independent failures that each name the same broken link.

**Mechanism tiers.** `verified`: a targeted test was run that would have come out
differently if the mechanism were false (an ablation, a counterfactual replay, a
decomposition whose parts were measured independently; an accounting identity always
sums and is not a test). `supported`: the data fits, but no discriminating test was run.
`inferred`: a plausible story with no check behind it. `untested`: named so it can be
tested. Never present an `inferred` mechanism untagged or as established.

**When theory and result disagree, walk this order**, cheapest first:

1. **Our pipeline:** bug, leakage, misalignment, unit error, numeric failure. A defect
   found after the result marks the run `void: pipeline defect`, only with evidence that
   the defect changes the headline number; the original verdict stays visible
   (`FAIL → void: {defect, evidence}`). A rerun on fresh data is a new run; on data
   already read it is `re-read, not confirmatory` and needs the person's approval. Check
   passing runs for the same defect too.
2. **Our comparison:** baseline mismatch, confound, too little power, wrong segment.
3. **Our metric:** the proxy moved and the objective did not, or the reverse.
4. **Our theory:** a specific link in the chain. Name it, or, when the evidence cannot
   separate candidates, name the candidates and the experiment that would.
5. **The environment** (regime, traffic mix, hardware), only with evidence.

Then answer: what would have to be true for the theory to still hold? What is the
smallest check that separates the candidate mechanisms? What adjustment would make the
idea work, and how would you verify it without reusing spent data?

## Reporting: two verdicts, never merged

Report and Decision levels deliver: (Decision only) the frozen rule, verbatim, with its
approval date · the bottom line in one to three lines · the summary table
`| Question | Theory | Measured | Consistent? | Mechanism [tier] |` · cards for rows that
need more than a cell · Facts / Inferences / To test, kept apart · caveats · not checked
(never empty) · next checks, each with the data it would consume and whether it needs
approval.

- **Rule verdict:** in the frozen rule's own labels (e.g. `PASS · FAIL · UNCERTAIN`), or
  `descriptive only`, or `void`. Computed mechanically on the rule's own metric as
  defined when it was frozen. An argument that the metric was a proxy feeds the direction
  verdict and the next rule proposal, never this verdict. A result exactly on a boundary
  the rule does not cover: say so and ask. Do not resolve it in your own favour.
- **Direction verdict:** `alive · alive-but-constrained · weakened · dead`, with the
  reason. **The agent proposes it; the person owns it.** When the person's hypothesis is
  under test, quote their words from the frozen card. `dead` needs a fired falsifier or
  independent failures naming the same broken link; otherwise `weakened` at most. A
  single failed run rarely makes a direction `dead`: one configuration failed; say which
  assumption the failure constrains.
- A good mechanism never turns a rule `FAIL` into a `PASS`; it only justifies a new,
  pre-registered test. A descriptive result is never upgraded into an adoption decision
  in the same report. A screen (a cheap pre-filter before the real test) can only
eliminate: passing it means "not eliminated", never PASS or confirmation. A pooled result never covers for a
  failed independent batch: report that batch first.

## Fresh-context audit

For Report and Decision levels, `mechanism-auditor` receives the cards, the saved
prediction card with its `Written` line, the frozen rule, and the artifact paths behind
every number. It downgrades any verdict or tier the evidence does not support, names an
alternative mechanism for every card (including `consistent` ones) and the cheapest
discriminating check. Downgrades take effect as given; where you disagree, keep its
reading and put yours under caveats. Without subagents, label the audit
`same-context — weaker`.

Examples and the anti-pattern table: `results-examples.md`.
