# Cartographer Mode — Full Protocol

Loaded on demand by `SKILL.md` (Phase C summary). Read this file in full before entering
Cartographer mode; the summary in SKILL.md is a map, this is the territory. Every rule
here is normative. Workflow scripts referenced below live in `workflows.md`.

## Phase C: Cartographer mode (high-stakes escalation)

Gates on **coverage** (all four quadrants probed) AND **clarity** (per-quadrant ambiguity
scored every round, weighted total at or below threshold), persists across the **whole
lifecycle**, and orders work by **regret**. Two axes, two jobs: regret prices *rows*
(which unknown to clear next); ambiguity scores *quadrants* (whether the user can see how
clear the map actually is). The interactive loop is mandatory — scores are shown after
every round so the user can steer instead of discovering drift at the end.

**Resolve the clarity threshold first (blocking).** Read
`findingUnknowns.ambiguityThreshold` from `./.claude/settings.json` (project) then
`~/.claude/settings.json` (user); default **0.25**. Depth-flag presets: `--quick` 0.35 ·
`--standard` 0.25 · `--deep` 0.15. Precedence: **flag > project > user > default**. Announce on entry,
first line exactly:

> Clarity threshold: {X}% (source: {project settings | user settings | default | flag})
>
> Entering Cartographer mode. I will maintain unknowns-ledger.md, clear the highest-regret
> unknown each round by its route, score all four quadrants' clarity after every round, and
> will not proceed to implementation until the coverage gate passes AND weighted ambiguity
> is at or below {X}%.

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
| UK | taste/recognition criteria have been elicited — prototype reactions or reference extractions converted into explicit criteria |
| UU | blind-spot probes ran and are going dry; findings are tracked rows |

`ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)` — UU carries the most weight
because unprobed blind spots are the failure mode this skill exists to prevent. Scoring is
`ledger-keeper`'s SCORE-QUADRANTS operation when installed; inline otherwise. Consistency
beats flair: justify from ledger evidence, never from how productive the round felt.

### C0: Seed the ledger

Create `unknowns-ledger.md` (owned by `ledger-keeper` when installed). The file opens
with a header block — clarity threshold + source, the Round 0 locked topology (components,
statuses, deferral reasons), and a per-round quadrant score history table — followed by
the rows:

| id | quadrant | unknown | cost-if-wrong (1–5) | P(wrong) | regret | **route** | **reversibility** | status | phase | resolution / default |
|----|----------|---------|--------------------|----------|--------|-----------|-------------------|--------|-------|----------------------|

- Run Technique 1 (blind-spot pass) → seed UU rows. Naming a blind spot makes it trackable.
  For high-stakes tasks, prefer a **multi-lens sweep**: parallel scouts with distinct lenses
  (e.g. domain-risk / engineering / statistics) — diversity catches what one lens cannot.
  When the Workflow tool is available (and the user has opted into orchestration), run the
  sweep as the `fu-multi-lens-sweep` script in `workflows.md`: scouts fan out,
  each finding is adversarially verified as its lens completes (pipeline, no barrier), and
  the result is schema-validated ledger rows — no lens or verification step can be
  silently dropped. Without Workflow, follow the fallback ladder in that file.
- Run Technique 2/4 where taste is involved → seed UK rows.
- Write down KK; list KU.
- **Domain checklist hook**: after seeding, check the ledger against a domain checklist
  derived from the user's profile, and add any missing rows. Example (quant trading):
  funding/borrow costs · liquidation distance · capacity/liquidity · per-leg attribution ·
  fee/slippage realism · regime dependence. A checklist row you can immediately mark
  resolved costs one line; a missing one costs a blown-up backtest.
- **Prior first**: before a row is scored from evidence, record the prior — the user's
  stated hypothesis or the agent's best guess — in the resolution column as `prior: …`.
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
  confirmation, recorded like any other. A task's lane is the maximum lane of the
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
     clearing action, written as a `theory-vs-result` prediction card (saved with its
     `Written` line); the row stays `probing`. "What result clears the row" is a pass
     line, so it goes through that skill's threshold gate (explained in plain language and
     approved by the user) or the row can only clear descriptively.
     When results return, report them as `theory-vs-result` cards and append the card's
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
   - **Adversarial check**: before marking the row resolved, construct the strongest
     alternative explanation consistent with the SAME evidence. If a plausible refutation
     exists, the row stays `resolved-provisional` and the ledger records the one
     discriminating check that would separate the explanations. (Example: a strong
     backtest IC resolves "is the signal real?" only provisionally — leakage produces the
     same IC; the discriminating check is a pipeline audit.) With Workflow available, use
     the `fu-verify-panel` script (`workflows.md`): three refuters with distinct
     lenses (alternative-explanation / evidence-independence / reproduction); the
     resolution survives only if ≥2 fail to refute, and refuters' discriminating checks
     land in the ledger verbatim.
   - **Cross-reference rule**: a cost ≥ 4 resolution backed by a single evidence source is
     `resolved-provisional`, never `resolved`. Two independent sources (different
     instruments — e.g. an experiment AND an audit) are required for full resolution.
   - Record per resolution: the evidence, its source(s), and a confidence label
     (high/medium/low). Separate fact from inference explicitly.
3.8 **Score the quadrants** (every round, no exceptions): re-score all four quadrants per
   the clarity model in the Phase C header (`ledger-keeper` SCORE-QUADRANTS when
   installed). Append the scores to the ledger's score history. The next round's target
   is the highest-regret open row, tie-broken toward the weakest quadrant.
3.9 **Challenge modes** (each used exactly once, then back to normal clearing):
   - Round 4+, **Contrarian**: the next interview question challenges a core assumption —
     "what if the opposite were true / this constraint doesn't exist?"
   - Round 6+, **Simplifier**: probe removable complexity — "what's the simplest version
     that would still be valuable?"
   - Round 8+ if ambiguity still > 0.30, **Ontologist**: "what IS this, really — which
     component is the core and which are supporting views?" (may revise the Round 0
     topology; re-lock it if so)
4. **Report** after every round, in exactly this format:

```
Round {n} complete.

Ledger: {open} open | {probing} probing | {resolved} resolved | {deferred} deferred
Top regret: {id} ({regret}) — {unknown} [route: {route}]

| Quadrant | Score | Weight | Gap |
|----------|-------|--------|-----|
| KK | {s} | 0.20 | {gap or "clear"} |
| KU | {s} | 0.25 | {gap or "clear"} |
| UK | {s} | 0.25 | {gap or "clear"} |
| UU | {s} | 0.30 | {gap or "clear"} |
| **Ambiguity** | **{a}%** | threshold {X}% | {weakest quadrant × component + why it's next} |

Coverage gate:
[{x| }] KK locked          [{x| }] KU resolved/deferred
[{x| }] UK extracted       [{x| }] UU probed
[{x| }] no open row with regret ≥ 1.0
[{x| }] every irreversible row user-confirmed
[{x| }] ambiguity {a}% ≤ threshold {X}%

{gate passes ? "Gate PASSED — ready to build."
 : "Next target: {id} — {reason}"
 : when only probing rows with pending experiments/audits remain:
   "Gate BLOCKED on external work: {list of clearing actions}. No further rounds add
    value — execute the clearing actions, then resume (the ledger is the state)."}
```

### C2: Gate check (blocking, dual-axis)

Implementation may start only when ALL hold — coverage AND clarity:

- [ ] KK locked — knowns written down
- [ ] KU resolved or deferred-with-default
- [ ] UK extracted — at least one brainstorm/prototype/reference ran
- [ ] UU probed — at least one blind-spot pass ran; findings are tracked rows
- [ ] No open row has regret ≥ 1.0
- [ ] Every `irreversible` row is user-confirmed (resolved with recorded confirmation, or
      deferred with a conservative default the user accepted) — never agent-resolved
- [ ] Weighted ambiguity ≤ threshold (per-quadrant scores from the latest round)

The two axes catch different failures: coverage catches "we never looked there";
ambiguity catches "we looked, but the user still can't tell how clear it is". Passing one
does not imply the other. Round limits: soft warning at round 10 (show scores, offer
continue/proceed-with-risk), hard cap at round 20 (proceed noting the residual ambiguity).
Early exit from round 3+ is allowed — display the current score table and open gaps once,
transparently, then respect the exit. **Exits waive the coverage and ambiguity
conditions, never the irreversibility floor**: before proceeding through an early exit,
the round-20 cap, or a "just build it", list every open irreversible row and get each
confirmed or deferred-with-accepted-default — or force the work it guards into the
irreversible lane so it cannot run without the user.

If UU was never probed the gate FAILS — that is its entire point. When `ledger-keeper` is
installed its verdict is final; never pass the gate out of politeness.

**Completeness critic (final sub-step before declaring PASS)**: when all seven conditions
appear satisfied, run one explicit "what's missing?" pass before announcing PASS — a
domain-checklist re-scan plus three questions: which quadrant was probed most shallowly?
which resolution is single-source or provisional? what would an expert reviewer ask that
no row covers? Anything surfaced becomes a new row and the gate re-evaluates. A PASS
without the critic pass is invalid. If the critic names UU as the shallow quadrant and
Workflow is available, run `fu-uu-until-dry` (`workflows.md`): differently
angled probes loop until two consecutive rounds surface nothing new — bounded by
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

**Crystallized spec.** On gate PASS, also write `unknowns-spec-{slug}.md` next to the
ledger — the handoff artifact for Phase E: goal (one sentence, covering every active
topology component), constraints, non-goals, testable acceptance criteria, the final
quadrant clarity table (scores + ambiguity % + threshold + source), an assumptions
exposed → resolved table, the **verification contract** (below), and a ledger snapshot
reference. The spec is marked **pending approval** — writing it grants no execution
permission.

**Verification contract — define "verified" before anything is built.** Post-facto,
any outcome can be rationalized; so each acceptance criterion gets, in the spec:

| criterion | check (what runs) | artifact (test / screenshot / log / trace) | proves | does NOT prove | lane |
|-----------|-------------------|---------------------------------------------|--------|----------------|------|

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
  (`reversible` · `wide` · `irreversible`) and decides who may close it in Phase E.
- The user approves the contract together with the spec. This is the front end of the
  human's two touchpoints; the back end is the irreversible lane in Phase E.

### E: Cross-validated execution bridge (approval-gated)

Never auto-execute. After the spec, ask ONE question — "Spec ready (ambiguity {a}%).
How to proceed?" — with these options:

1. **Consensus-refine, then separate execution approval (recommended).** A planner-role
   agent drafts the implementation plan from spec + ledger; an INDEPENDENT reviewer-role
   agent (architect/critic framing: "find what breaks this plan against the spec and the
   ledger's deferred defaults") reviews it; loop until the reviewer approves, ≤3
   iterations. Then STOP with the consensus plan marked pending approval — execution is a
   separate explicit yes.
2. **Execute via Workflow orchestration** (requires the user's orchestration opt-in): run
   `fu-execute-verified` from `workflows.md` under the execution rules below — every task
   is a loop (implement → independent verify against the contract → correct), the tasks
   form a graph (only real dependencies wait), and lanes decide who closes a task.
   **First, the task graph is itself approved**: a planner-role context derives tasks
   from the spec (id, description, covered criteria, lane = max lane of those criteria,
   touched paths, checks and check files from the contract, post-checks for the
   irreversible lane, dependencies with what crosses); the user approves that graph
   before the run. The spec author does not approve its own decomposition.
   Fallback ladder: Workflow → parallel Agent calls → inline. On the inline rung the
   implementer and verifier would share a context, so no lane closes automatically —
   every task goes to the user with its check results.
3. **Refine further** — return to the C1 loop.

**Execution rules (normative on every rung of the fallback ladder).**

- **The loop lives inside a task; the graph lives between tasks.** A task is one bounded
  unit — one input, one output, its own context. Without a verifier that can fail it, a
  "loop" is just a scheduler; without a graph, a good loop runs the wrong steps in the
  wrong order.
- **Edges must name what crosses.** A dependency edge `A → B` is valid only if you can
  name the variable/artifact A produces that B consumes. "And then" is not an edge —
  unnamed edges are the most common source of needless waiting. But dropping one is a
  claim of independence, so it is shown to the user before the run; and an unnamed edge
  out of a `wide` or `irreversible` task is kept (fail closed), because running a
  consumer before an unconfirmed irreversible producer builds on a premise that is not
  yet true.
- **Code, not agents, for mechanical nodes.** If a step can be described without
  *judge / decide / assess / summarize* (merge, dedupe, rank, compare, format), it is a
  code node, not an agent call.
- **Never concurrent on the same paths.** Each task declares the paths it may touch
  (its SCOPE ceiling; no globs); tasks whose paths overlap are serialized, and edits
  outside every declared path stop the run. Tasks on disjoint paths still share one
  working tree, so keep each task's checks narrow to its own paths — attribution between
  concurrent tasks is prompted, not enforced.
- **Return the unit, never the batch.** When one task fails, only that task goes back,
  carrying `UNIT · VERDICT · REASON · EVIDENCE (expected vs got, file:line) · SCOPE (what
  the fix may touch)`. Re-running passed siblings produces different, not better, work.
  SCOPE stops a one-file fix from becoming a four-file diff. The verifier of a retry is
  shown the previous return and checks that defect and SCOPE first, so objections do not
  drift between attempts.
- **Attempt cap = plan signal.** After the cap (default 3 attempts per task), stop
  retrying: repeated failure means the plan or the territory map is wrong, not the
  implementer. The task becomes a new ledger row (`phase: during`, route as appropriate)
  and goes back to the user.
- **Two return edges.** The *correction edge* fixes this run (the failed unit, scoped).
  The *learning edge* fixes every later run: when a verdict — pass or fail — reveals a
  constraint the spec did not state ("adapters must preserve keyword args exactly"),
  append it to the spec's **Derived constraints** and the ledger, and feed it to every
  task not yet started. Derived constraints may only *tighten* the spec: one that
  contradicts the spec or its contract halts the run and becomes a ledger row for the
  user; tasks that closed before a constraint appeared are listed for re-check. A system
  that is fast but never gets smarter is missing this edge. In ledger terms: every
  failure is a discovered unknown.
- **Lanes close tasks by reversibility, not by confidence.**
  Every lane first requires the contract checks to run green — run by a context other
  than the implementer, with check files unchanged against a pre-run baseline (a
  tampered check stops the task outright).
  `reversible` → then closes on the independent verifier's pass.
  `wide` → additionally requires the verifier to have checked the dependents of the
  changed surface, with evidence (`oh-my-claudecode:blast-radius` when installed).
  `irreversible` → never closes in-run, whatever the scores. Contract checks for this
  lane must be safe dry-runs (plan output, `--sql`, diff of intended effect); anything
  that would perform the irreversible action is a *post-check*. The implementer prepares
  the change and the exact command and executes nothing irreversible; the user (or the
  main agent on the user's explicit yes for that command) executes it; then the
  post-checks run, and only then does the task close.
  Evidence order for every verdict: check-runner results → the commands actually
  executed and their output → the verifier's own reading → the implementer's summary,
  which is a claim, not evidence.
- **The human sits at both ends, not in the middle.** Front: approve the spec and its
  verification contract. Back: the irreversible lane and the final merge. A human in the
  middle of the graph becomes its slowest node; a human only at the end, reviewing an
  artifact they never framed, is rubber-stamping — pair the back-end review with the
  `keep-the-reasoning` handoff packet when that skill is installed.

Normative invariant (extends "separation of judgment"): **the context that authored a
spec or plan never self-approves its execution.** Author and approver are always
different contexts — a second agent, or the user.

### C3: During & close-out

- Keep the ledger open through the build: every mid-build discovery becomes a row
  (quadrant + regret + reversibility), conservative option chosen and logged (Technique 6
  feeds the ledger; learning-edge constraints from Phase E land here too).
- Post: build the quiz FROM the ledger — one question per resolved high-regret row and per
  named UU. Merge only when no open row has regret ≥ 1.0 and every irreversible row —
  including those discovered mid-build — is user-confirmed or deferred with an accepted
  default.

## Resume

The ledger IS the state. To resume an interrupted Cartographer session, re-read
`unknowns-ledger.md` (and `implementation-notes.md` if the build started), announce the
current gate status, and continue from the highest-regret open row. Do not re-seed.

## Threshold configuration

Optional, read at Cartographer entry (project overrides user; degrade silently to the
default — no OMC runtime required):

```json
{ "findingUnknowns": { "ambiguityThreshold": 0.25 } }
```

## Cartographer final checklist

- [ ] Ledger exists with quadrant, cost, P(wrong), regret, route, reversibility, status,
      phase per row; priors recorded before evidence-based scoring
- [ ] No `irreversible` row was defaulted silently or resolved without user confirmation
- [ ] The domain checklist hook ran at seeding; missing domain rows were added
- [ ] Every row was cleared via its route — no territory-answerable question was asked of
      the user, and no experiment/audit row blocked the loop with useless extra rounds
- [ ] Every round reported the ledger summary + gate checklist in the standard format
- [ ] Gate verdict came from ledger-keeper when installed; UU probe was not skipped
- [ ] Deferred rows all carry conservative defaults; no rows were deleted
- [ ] First announcement line stated the clarity threshold and its source
- [ ] Round 0 topology was confirmed by the user before any quadrant scoring
- [ ] Every round's report included the four-quadrant score table with weighted ambiguity
- [ ] Gate checked both axes: coverage conditions AND ambiguity ≤ threshold
- [ ] On PASS, unknowns-spec-{slug}.md was written and marked pending approval, with a
      verification contract whose every check can fail and states what it does NOT prove
- [ ] In execution: edges named what crosses; failures returned per unit with SCOPE;
      derived constraints fed forward; irreversible-lane tasks waited for the user
- [ ] Execution bridge asked before any execution; plan author ≠ plan approver throughout
- [ ] Quiz was generated from the ledger; merge recommendation followed the pass rule
