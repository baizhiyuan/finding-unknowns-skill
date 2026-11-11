# Cartographer Mode — Full Protocol

Part of **structured mode** (`structured.md`), loaded only on request: `/fu-cartographer`,
"Cartographer mode", or structured mode at high stakes. Read this file in full before
entering; every rule here is normative. Restored from 4.3.2 for people who want the full
protocol, including with smaller models; Workflow execution (4.x Phase E2) is not part of
5.0.

**How it fits the task card.** The ledger lives beside the card
(`.finding-unknowns/unknowns-ledger.md`). The spec's priors become the card's
predictions; its acceptance criteria and verification contract become the card's
contract; the budget multiple is set in the Brief as usual. The card's Brief freezes on the user's approval of the spec; that approval, the § E1 choice and the card freeze are one ask before the build, and the build (with the turn-end rule) starts at the execution yes. Option 3 is not an approval; the card stays unfrozen. The four stop-points, the
build rule and the `/fu-debrief` grading apply unchanged; at merge, `/fu-debrief` uses the
full nine-section packet (`handoff-full.md`).

## Phase C: Cartographer mode (high-stakes escalation)

Gates on **coverage** (six conditions, C2: every quadrant probed — or, for UK only,
user-confirmed not applicable — no open high-regret row, every irreversible row
user-confirmed), persists across the **whole lifecycle**, and orders work by **regret**.
**Clarity is displayed, not gated**: per-quadrant clarity is scored every round and
summarized as a weighted ambiguity figure so the user can steer instead of discovering
drift at the end. Two signals, two jobs: regret prices *rows* (which unknown to clear
next); the clarity display scores *quadrants* (whether the user can see how clear the map
actually is). The interactive loop is mandatory — scores are shown after every round —
but the ambiguity figure is never a gate condition.

**Resolve the depth first (blocking).** Depth sets breadth, not a threshold:

| Depth | Seeding (C0) | Before the gate (C2) | Soft check |
|-------|--------------|----------------------|------------|
| `--quick` | single-lens blind-spot pass (one scout, one lens) | standard gate | round 5, then every 5 rounds |
| `--standard` (default) | one blind-spot pass (full report); escalates to a multi-lens sweep when the task spans more than one risk domain (e.g. money + data + infra) | standard gate | round 10, then every 10 rounds |
| `--deep` | always a multi-lens sweep (parallel scouts) | UU loop-until-dry (repeat angled passes until two add nothing) | round 10, then every 10 rounds |

Precedence: **flag > the user's stated request > default (`--standard`)**. The settings
key `findingUnknowns.ambiguityThreshold` is ignored since 4.2.0 (see § Settings).
Announce on entry, first line exactly:

> Depth: {quick | standard | deep} (source: {flag | user request | default})
>
> Entering Cartographer mode. I will maintain .finding-unknowns/unknowns-ledger.md, clear
> the highest-regret unknown each round by its route, show all four quadrants' clarity
> after every round, and will not proceed to implementation until the six-condition gate
> passes.

**Round 0 — topology gate (one question, before any scoring).** Enumerate the task's 1–6
top-level components (outcomes that can succeed or fail independently — not sub-features)
and confirm via one question: "I read this as N components: … Add, remove, merge, split,
or defer any?" Lock the confirmed list into the ledger header. Quadrant scores are then
tracked per component where components differ materially; the reported score for a
quadrant is its weakest active component's score — depth-first clarity on the
best-described component must not hide sibling fog. Deferrals need a user-confirmed
reason and are excluded from ambiguity math but stay listed.

**Quadrant clarity model.** Each quadrant scores 0.0–1.0 with a one-clause justification
and a named gap when below 0.9:

| Quadrant | Scores high when |
|----------|------------------|
| KK | stated knowns are written down, internally consistent, and confirmed against the territory |
| KU | known gaps are enumerated, each with a route and a resolution or logged default |
| UK | taste/recognition criteria have been elicited — prototype reactions or reference extractions converted into explicit criteria (a UK the user confirmed not applicable scores 1.0 with that justification) |
| UU | blind-spot probes ran and are going dry; findings are tracked rows |

`ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)` — UU carries the most weight
because unprobed blind spots are the failure mode this skill exists to prevent. The figure
is a **display**: it steers targeting and tells the user how clear the map is; it never
passes or fails the gate. Scoring is `ledger-keeper`'s SCORE-QUADRANTS operation when
installed; inline otherwise. Consistency beats flair: justify from ledger evidence, never
from how productive the round felt.

### C0: Seed the ledger

Create `.finding-unknowns/unknowns-ledger.md` at the project root (owned by
`ledger-keeper` when installed; the directory and its `.gitignore` rule are in `card.md`). The file opens with a header block — first line
`schema: 2` (the ledger format version; the fields below are schema 2), then depth +
source, the Round 0 locked topology (components, statuses, deferral reasons), the UK
status (in scope, or not applicable with the user's confirmation), and a per-round
quadrant score history table — followed by the rows:

| id | quadrant | unknown | cost-if-wrong (1–5) | P(wrong) | regret | **route** | **reversibility** | status | phase | resolution / default |
|----|----------|---------|--------------------|----------|--------|-----------|-------------------|--------|-------|----------------------|

- Run Technique 1 (blind-spot pass, full report) → seed UU rows. Naming a blind spot makes
  it trackable. Breadth follows the depth: `--quick` runs one scout with one lens;
  `--standard` runs one blind-spot pass, escalating to a **multi-lens sweep** when the
  task spans more than one risk domain (e.g. money + data + infra); `--deep` always runs
  a multi-lens sweep. A multi-lens sweep is parallel scouts with distinct lenses (e.g.
  domain-risk / engineering / statistics) — diversity catches what one lens cannot.
  Run the scouts as parallel `blindspot-scout` calls (inline, one lens at a time, when
  subagents are unavailable); verify each finding adversarially before it becomes a
  ledger row, and never drop a lens silently.
- Run Technique 2/4 where taste is involved → seed UK rows. When the task has no taste
  component (e.g. a backend migration), propose marking UK "not applicable" and record the
  user's confirmation in the ledger header; never mark it without that confirmation.
- Write down KK; list KU.
- **Domain checklist hook**: after seeding, check the ledger against a domain checklist
  derived from the user's profile, and add any missing rows. Example (quant trading):
  funding/borrow costs · liquidation distance · capacity/liquidity · per-leg attribution ·
  fee/slippage realism · regime dependence. A checklist row you can immediately mark
  resolved costs one line; a missing one costs a blown-up backtest. When the work runs
  on a remote device or service, the checklist always includes access: reachable from
  the working machine, and with which credentials.
- **Prior first**: before a row is scored from evidence, record the prior — the user's
  stated expectation or the agent's best guess — in the resolution column as `prior: …`
  (reuse a prior already captured in Phase 0 or by a sibling skill; never ask again).
  The column is append-only: a resolution extends it (`prior: X → resolved: Y
  [user-confirmed {date}]`), never overwrites it, so the prior stays comparable.
  Initial P(wrong) reflects how much evidence backs the prior; no evidence → P(wrong)
  starts high. When later evidence contradicts a prior, that surprise is itself a signal:
  re-examine sibling rows that rested on the same belief.
- `regret = cost-if-wrong × P(wrong)` — the prioritization signal for *ordering*.
- **`reversibility` — the gating signal** (`reversible` · `wide` · `irreversible`):
  `reversible` = contained and cheap to undo (a copy change, a test, an isolated
  function); `wide` = undoable but touches shared surface (a shared utility, a public
  interface, an additive backward-compatible schema change with a tested down-path);
  `irreversible` = hard or impossible to undo (migrations that rewrite or drop data,
  deletions, production data, money, external publication, commitments to people).
  **Classify upward when unsure.** Downgrading a row from `irreversible` requires user
  confirmation, recorded like any other. This value is the row's **lane** (the only
  meaning of "lane" across these skills); a task's lane is the maximum lane of the
  criteria it covers.
- **Irreversibility floor**: regret contains P(wrong), and P(wrong) is a confidence
  estimate — the one input most prone to optimism. So for `irreversible` rows,
  confidence never substitutes for the user: (a) the leave-open rule does not apply —
  an irreversible row is never silently defaulted, whatever its regret; (b) it can reach
  `resolved` only with explicit user confirmation recorded in the row, in addition to the
  evidence discipline of C1 step 3.5; (c) the other legitimate end state is `deferred`
  with a conservative default the user accepted. Whatever the route, the user sees it:
  for `territory`/`experiment`/`audit` rows, run the check first, then present the
  evidence for confirmation — that is a confirmation, not a discoverable question.
  Gate on blast radius, not on confidence.
- **`route` — HOW the row gets cleared** (regret decides order; route decides instrument):
  - `interview` — the answer exists only in the user's head (preferences, intent, context)
  - `territory` — verifiable by reading/checking code or data (assign to a scout or a check;
    NEVER ask the user — the no-discoverable-questions rule applies per row)
  - `experiment` — needs a backtest/prototype/measurement to settle
  - `audit` — needs review of an external artifact (a pipeline, a dependency, a document)
- `status ∈ {open, probing, resolved-provisional, resolved, deferred}`; deferred REQUIRES a
  conservative default; resolved-provisional (single-source or refutable evidence, cost ≥ 4)
  REQUIRES a named discriminating check. Rows are never deleted. `phase ∈ {pre, during,
  post}` records when the unknown surfaced.

### C1: Clearing loop

The engine is a **router, not an interview**: each round clears the highest-regret open row
by its route. Repeat until the gate passes or the user exits:

1. **Target**: the highest-regret open row (keeper picks when installed) — or, for the
   `interview` route, the top 1–3 *independent* rows to clear in one round. Leave-open rule:
   rows with regret < 1.0 get a conservative default logged and are not worth a round —
   except `irreversible` rows, which always reach the user (irreversibility floor, C0).
2. **Dispatch by route**:
   - `interview` → ask via AskUserQuestion, prefixed with the targeting rationale. Ask 1–3
     *independent* interview-route rows in one round (highest regret first); keep dependent
     rows for later rounds:

     ```
     Round {n} | Targets: {id(s)} {unknown(s)} | Regret: {r each} ({cost}×{p}) |
     Route: interview | Why now: {one sentence per target}

     {1–3 questions, each with 2–3 concrete options + recommendation}
     ```

   - `territory` → run the check now (Grep/Read/scout); report the evidence found.
   - `experiment` → do NOT block the loop: record the experiment spec as the row's
     clearing action, written as a prediction card (`results.md`) (saved with its
     `Written` line); the row stays `probing`. "What result clears the row" is a pass
     line, so it goes through the threshold gate in `results.md` (explained in plain language and
     approved by the user) or the row can only clear descriptively.
     When results return, report them as result cards (`results.md`) and append the card's
     verdict and tier to the row's resolution column (append-only). Mapping: `consistent`
     with tier `verified` may resolve the row, subject to step 3.5 (a single source at
     cost ≥ 4 stays `resolved-provisional`) and the irreversibility floor; `consistent` or
     `partly` with a lower tier → `resolved-provisional`, with the card's next check as the
     discriminating check; `inconsistent` → `resolved-provisional` with "prior contradicted:
     broken link = …" (the experiment answered the question; the answer is that the prior
     was wrong), the broken link becomes a new row, and sibling rows that rested on the same
     belief are re-examined; `can't tell`, `post-hoc fit` or `void` → the row stays `probing`. For
     cost ≥ 4 rows the `mechanism-auditor` audit can serve as step 3.5's adversarial check;
     it does not count as an independent second source.
   - `audit` → likewise: name the artifact, what to look for, and the expected effort;
     the row stays `probing` until the audit result arrives.
3. **Re-score** the row's P(wrong) from the answer/evidence; recompute regret. Answers may
   spawn NEW rows (quadrant + regret + route) — that chain is the ledger working correctly.
3.5 **Verify before resolving (evidence discipline, for rows with cost ≥ 4)**:
   - **Adversarial check** — a fresh-context refutation (the shared primitive: a context
     that did not produce the resolution tries to refute it from the same evidence; run in
     the same context, it is labelled `same-context — weaker` in the row's resolution /
     evidence cell). Before marking the row
     resolved, construct the strongest alternative explanation consistent with the SAME
     evidence. If a plausible refutation exists, the row stays `resolved-provisional` and
     the ledger records the one discriminating check that would separate the
     explanations. (Example: a strong backtest IC resolves "is the signal real?" only
     provisionally — leakage produces the same IC; the discriminating check is a pipeline
     audit.) When subagents are available, use
     three fresh-context refuters with distinct lenses (alternative-explanation / evidence-independence
     / reproduction); the resolution survives only if every refuter reports and none
     refutes it (one plausible refutation keeps the row `resolved-provisional`), and
     refuters' discriminating checks land in the ledger verbatim.
   - **Cross-reference rule**: a cost ≥ 4 resolution backed by a single evidence source is
     `resolved-provisional`, never `resolved`. Two independent sources (different
     instruments — e.g. an experiment AND an audit) are required for full resolution.
   - Record per resolution: the evidence, its source(s), and a confidence label
     (high/medium/low). Separate fact from inference explicitly.
3.8 **Score the quadrants** (every round, no exceptions; display only): re-score all four
   quadrants per the clarity model in the Phase C header (`ledger-keeper` SCORE-QUADRANTS
   when installed). Append the scores to the ledger's score history. The next round's
   target is the highest-regret open row, tie-broken toward the weakest quadrant.
4. **Report** after every round, in exactly this format:

```
Round {n} complete.

Ledger: {open} open | {probing} probing | {resolved} resolved | {deferred} deferred
Top regret: {id} ({regret}) — {unknown} [route: {route}]

| Quadrant | Score | Weight | Gap |
|----------|-------|--------|-----|
| KK | {s} | 0.20 | {gap or "clear"} |
| KU | {s} | 0.25 | {gap or "clear"} |
| UK | {s} | 0.25 | {gap, "clear", or "n/a (user-confirmed)"} |
| UU | {s} | 0.30 | {gap or "clear"} |
| **Ambiguity** (display) | **{a}%** | — | {weakest quadrant × component + why it's next} |

Gate:
[{x| }] KK written down    [{x| }] KU resolved/deferred-with-default
[{x| }] UK extracted or n/a (user-confirmed)
[{x| }] UU probed
[{x| }] no open row with regret ≥ 1.0
[{x| }] every irreversible row user-confirmed

{gate passes ? "Gate PASSED — writing the close-out report and spec (C2.5)."
 : "Next target: {id} — {reason}"
 : when only probing rows with pending experiments/audits remain:
   "Gate BLOCKED on external work: {list of clearing actions}. No further rounds add
    value — execute the clearing actions, then resume (the ledger is the state)."}
```

### C2: Gate check (blocking, six conditions)

Implementation may start only when ALL six hold:

- [ ] KK written down — knowns recorded in the ledger
- [ ] KU resolved or deferred-with-default
- [ ] UK extracted — at least one brainstorm/prototype/reference ran — OR marked "not
      applicable" with the user's confirmation recorded (e.g. a backend migration with no
      taste component)
- [ ] UU probed — at least one blind-spot pass ran; findings are tracked rows
- [ ] No open row has regret ≥ 1.0
- [ ] Every `irreversible` row is user-confirmed (resolved with recorded confirmation, or
      deferred with a conservative default the user accepted) — never agent-resolved

The clarity display is shown next to the gate but is not a condition: the gate rules on
checkable ledger facts (what was probed, what is still open, what the user confirmed),
never on whether a self-scored figure crossed a line.

**Soft check** at round 10 and every 10 rounds after (round 5 and every 5 after under
`--quick`) while the gate has not passed: show
the score table, surface the top-3 stuck rows by regret, and offer the user three ways
forward — resolve them now, defer them with a conservative default, or exit. There is no
hard round cap. Early exit from round 3+ is also allowed — display the current score table
and open gaps once, transparently, then respect the exit. **Exits waive the coverage
conditions, never the irreversibility floor**: before proceeding through an early exit,
the soft-check exit, or a "just build it", list every open irreversible row and get each
confirmed or deferred-with-accepted-default. A row left open stays under the build rule
in C2.5 ("Any build from this spec"): the work it guards is prepared but never executed
until the user runs it or says yes to that exact command.

If UU was never probed the gate FAILS — that is its entire point. When `ledger-keeper` is
installed its verdict is final; never pass the gate out of politeness.

**`--deep` only — UU loop-until-dry before the gate**: once the other conditions appear
satisfied, run differently angled blind-spot passes until two consecutive passes surface
nothing new, and add every new finding as a row before the gate is evaluated.

**Completeness critic (final sub-step before declaring PASS)**: when all six conditions
appear satisfied, run one explicit "what's missing?" pass before announcing PASS — a
domain-checklist re-scan plus three questions: which quadrant was probed most shallowly?
which resolution is single-source or provisional? what would an expert reviewer ask that
no row covers? Anything surfaced becomes a new row and the gate re-evaluates. A PASS
without the critic pass is invalid. If the critic names UU as the shallow quadrant, run
differently angled probes until two consecutive rounds surface nothing new — bounded by
information, not by a fixed count.

### C2.5: Close-out report (structured, Deep-Research style)

When the gate passes — or when suspending on external work — deliver a structured report,
not a prose summary:

```
# {task}: Unknowns Report
*Rounds: {n} | Rows: {total} ({resolved}/{provisional}/{deferred}/{open}) | Gate: {verdict}*

## Executive summary        — 3–5 sentences: what is now known, what still blocks
## Findings by row          — per high-regret row: evidence, source(s), confidence
##                            (high/med/low), fact vs inference labelled
## Gaps & provisional items — every resolved-provisional row with its discriminating
##                            check; every deferral with its conservative default
## Methodology              — which routes ran (interview/territory/experiment/audit),
##                            which agents/lenses, what was NOT examined
```

Acknowledging gaps is a deliverable, not an apology — an unlisted gap is an unlogged
deviation waiting to happen.

**Crystallized spec.** On gate PASS, also write
`.finding-unknowns/unknowns-spec-{slug}.md` next to the ledger — the handoff artifact:
goal (one sentence, covering every active topology component), constraints, non-goals,
testable acceptance criteria, the final quadrant clarity table (scores + ambiguity %,
display; depth), an assumptions exposed → resolved table, the **verification contract**
(below), and a ledger snapshot reference. The spec is marked **pending approval** —
writing it grants no execution permission.

**Default end of Cartographer: write the spec, then STOP.** On gate PASS, deliver the
close-out report and the spec with its verification contract, and stop. The next step
is the single ask in § E1 (the consensus-refine plan, option 1, recommended); the merge
runs `/fu-debrief`, noted as a line under Open. That merge debrief always uses the **full** packet (`handoff-full.md`):
Cartographer is high stakes by definition.

**Verification contract — define "verified" before anything is built.** Post-facto,
any outcome can be rationalized; so each acceptance criterion gets, in the spec:

| criterion | check (what runs) | artifact (test / screenshot / log / trace) | proves | does NOT prove | lane |
|-----------|-------------------|---------------------------------------------|--------|----------------|------|

- **Irreversible-lane criteria name their post-check** (what runs after the user executes
  the command, and what result closes the row) — the build rule below requires it on
  every execution path.
- **A check must be able to fail.** "Tests exit 0", "every claim carries a source line",
  "the diff touches only files listed in the plan" are checks. "Looks good", "the model
  is confident", "no errors were raised" are not — absence of an error is not evidence
  of correctness, and a model agreeing with a model is two optimists agreeing.
- **The "does NOT prove" column is mandatory.** A green check conveys one property. If you
  cannot say what a check would miss, the criterion needs a second, different check or a
  human review — not a quicker approval.
- **The contract is locked against its implementer.** Checks are authored (or at least
  approved) outside the implementing context, and the implementer may not edit check
  files; verifiers confirm the check files are untouched. A test written with the same
  mistake as the feature passes, and an agent that can edit its oracle can always go
  green.
- **`lane`** inherits the reversibility of the work the criterion guards
  (`reversible` · `wide` · `irreversible`) and decides who may close it (the build rule
  in C2.5/C3 for any build).
- The user approves the contract together with the spec. This is the front end of the
  human's two touchpoints; the back end is the irreversible work and the final merge.

**Any build from this spec — irreversible work stays with the user.** Whatever the
execution path (the user's own build, or a build from the consensus plan after a separate
yes), the implementer prepares each irreversible change and the exact
command, and executes nothing irreversible itself. The user runs the command, or gives an
explicit yes for that specific command; a general "go ahead" is not a per-command yes.
The post-checks run before the row (or task) closes. This is the card's first stop-point.

### E: After the spec — next step

The default end of Cartographer is the spec (C2.5). Never auto-execute.

#### E1 — Next step after the spec (default)

After the spec, ask ONE question — "Spec ready. How to proceed?" — offering options 1
and 3; the merge `/fu-debrief` (full packet) is a line under Open, not an offer. This
question, the approval of the spec and the freeze of the card are one ask, made before
the build; the build, and the rule that every turn ends with a completion report or a
stop-point request, start at the execution yes. (4.x option 2, Workflow execution, is
not part of 5.0.)

- **Option 1 — Consensus-refine, then separate execution approval (recommended).** A
  planner-role agent drafts the implementation plan from spec + ledger; an INDEPENDENT
  reviewer-role agent (architect/critic framing: "find what breaks this plan against the
  spec and the ledger's deferred defaults") reviews it; loop until the reviewer approves,
  ≤3 iterations. Then STOP with the consensus plan marked pending approval — execution
  is a separate explicit yes, and any build that follows is bound by the build rule in
  C2.5.
- **Option 3 — Refine further** — return to the C1 loop.

### C3: During & close-out

- Whoever builds, the build rule in C2.5 holds: irreversible steps are prepared, not
  executed; the user runs each one or gives a per-command yes; post-checks run before the
  row closes.
- Keep the ledger open through the build: every mid-build discovery becomes a row
  (quadrant + regret + reversibility), conservative option chosen and logged (the card's delta
  log feeds the ledger).
- Post: if the person wants a quiz, build it from the ledger — one question per resolved
  high-regret row and per named UU (Technique 8: inline; `quiz-master` only drafts). Merge only when no open row has regret ≥ 1.0 and every irreversible row —
  including those discovered mid-build — is user-confirmed or deferred with an accepted
  default. Hand over at merge with `/fu-debrief` and the full packet (Cartographer is
  high stakes by definition).

## Resume

The ledger IS the state. To resume an interrupted Cartographer session, re-read
`.finding-unknowns/unknowns-ledger.md` (and `.finding-unknowns/implementation-notes.md` if
the build started), announce the current gate status, and continue from the highest-regret
open row. After the build starts, interview-route rows are not asked; they go under Open unless they are one of the four stop-points. Do not re-seed.

- **Legacy location.** If `.finding-unknowns/unknowns-ledger.md` is absent but a
  root-level `unknowns-ledger.md` exists (pre-4.3), read it — and a root-level
  `implementation-notes.md` or `unknowns-spec-*.md` likewise — and offer in one line to
  move them into `.finding-unknowns/`. Never move them silently; until the user agrees,
  keep working on the root-level files. If the build has started, write the move offer under Open instead of asking.
- **Schema upgrade.** A ledger whose first line is not `schema: 2` is schema 1 (pre-4.3).
  Before the first round, `ledger-keeper` (its RESUME operation; inline otherwise) adds
  the missing header fields — depth + source, Round 0 topology, UK status, score
  history — reconstructed from the rows where they allow it and written as
  `{value} (reconstructed, legacy)`, otherwise marked `unknown (legacy)`; writes
  `schema: 2` as the first line; and reports what it added. A reconstructed or
  `unknown (legacy)` field never satisfies a gate condition until the user confirms it;
  on confirmation the marker is removed. So a reconstructed depth or topology counts only
  once confirmed, UK `unknown (legacy)` is not "not applicable", and a missing topology
  is re-confirmed with the user (Round 0). If the build has started, write the re-confirmation under Open instead of asking.

## Settings

None are required. `findingUnknowns.ambiguityThreshold` is ignored since 4.2.0 — the
ambiguity figure is display-only, so there is nothing for it to set. Depth comes from the
flag or the user's request (see the depth table at the top); a leftover key has no effect
and needs no announcement.

## Cartographer final checklist

- [ ] Ledger exists at `.finding-unknowns/unknowns-ledger.md` with `schema: 2` as its
      first line, and quadrant, cost, P(wrong), regret, route, reversibility, status,
      phase per row; priors recorded before evidence-based scoring
- [ ] No `irreversible` row was defaulted silently or resolved without user confirmation
- [ ] The domain checklist hook ran at seeding; missing domain rows were added
- [ ] Every row was cleared via its route — no territory-answerable question was asked of
      the user, and no experiment/audit row blocked the loop with useless extra rounds
- [ ] Every round reported the ledger summary + gate checklist in the standard format
- [ ] Gate verdict came from ledger-keeper when installed; UU probe was not skipped
- [ ] Deferred rows all carry conservative defaults; no rows were deleted
- [ ] First announcement line stated the depth and its source
- [ ] Round 0 topology was confirmed by the user before any quadrant scoring
- [ ] Every round's report included the four-quadrant score table with the weighted
      ambiguity figure, shown as a display and never used as a gate condition
- [ ] Gate checked all six conditions; UK was marked not applicable only with the user's
      confirmation recorded
- [ ] Depth honoured: `--quick` single-lens pass and soft check every 5 rounds;
      `--standard` one blind-spot pass, a multi-lens sweep when the task spans more than
      one risk domain; `--deep` multi-lens sweep at seeding and UU loop-until-dry before
      the gate
- [ ] On PASS, `.finding-unknowns/unknowns-spec-{slug}.md` was written and marked pending
      approval, with a verification contract whose every check can fail and states what
      it does NOT prove — and the run stopped there
- [ ] After the spec, only options 1 and 3 were offered (§ E1)
- [ ] In any build from the spec, irreversible steps were prepared, not executed; the user
      ran each one or gave a per-command yes; post-checks ran before the row closed
- [ ] Nothing executed without a separate yes; plan author ≠ plan approver throughout
- [ ] The merge debrief used the full packet (`handoff-full.md`)
- [ ] Quiz only if the person asked; then generated from the ledger, and the merge
      recommendation followed the pass rule
