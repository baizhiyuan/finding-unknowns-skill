# Structured mode

The 4.x protocol, restored as an **opt-in** layer on top of the task card. Load this file
only when the person asks for it: "structured mode", `/fu-brief --structured`, or
`/fu-cartographer` (which also loads `cartographer.md`). The default flow in SKILL.md does
not load it.

**Why it exists.** In three evaluations, current frontier models gained nothing measurable
from the full protocol on single-turn tasks; they were already near the ceiling. Smaller
models (for example 27–38B open-weight models) may benefit from explicit steps, numbered
techniques and a ledger. That is a hypothesis under test, not a finding.

**What changes in structured mode.**
- Phase 0 classifies the gap on the quadrant map and announces the routing, and the
  numbered techniques below replace the short instrument list in `brief.md`. Phase 0 and
  Techniques 1–5 run inside the Brief, after the person's prediction; Technique 5's
  Definition of verified becomes the card's contract. The card records `Structured: yes`.
- High-stakes work can escalate to Cartographer (`cartographer.md`): ledger, regret
  ordering, clarity display, six-condition gate, spec with verification contract.
- The debrief uses the full nine-section packet (`handoff-full.md`).
- Everything in SKILL.md still holds: the card, the person predicts first, the four
  stop-points, the build rule, fresh-context grading.

## Phase 0: Locate the unknown (blocking prerequisite)

Before any technique, classify where the gap lives and announce the routing:

| | User is aware of it | User is not aware of it |
|---|---|---|
| **User knows it** | **KK — Known Knowns**: in the prompt. Write them down; implicit knowns drift. | **UK — Unknown Knowns**: know-it-when-I-see-it criteria. → Technique 2, 4 |
| **User doesn't know it** | **KU — Known Unknowns**: nameable gaps. → Technique 3, 5 | **UU — Unknown Unknowns**: blind spots. → Technique 1, 8 |

Capture the prior in one line — what the user expects the answer or outcome to be (ask
only if it is not inferable; "no idea yet" is a valid prior and itself routes to UU). A
prior is any expectation recorded before the result; one already recorded in this session
on the task card (the user's prediction) or in a prediction card (`results.md`) is reused,
never asked again.

Then choose the mode and say so:

> **Routing:** {quadrant(s) identified} → {technique(s) or Cartographer mode} — {one-line reason}

Mode selection:
- Low/medium stakes, one dominant quadrant → run the matching technique(s) from Phase 1–3
- High stakes (hard to reverse, wide blast radius, unfamiliar territory + long horizon) →
  offer Cartographer mode explicitly; do not silently escalate. Before entering, read
  `cartographer.md` in full; on entering, change the card's flag to
  `Structured: cartographer`

**Default deliverable (lightweight mode):** analysis outputs — the Phase 0 routing
analysis, the Technique 1 blind-spot pass, and Technique 4 reference extraction — end in
a short report: the 3 most consequential findings, each with its evidence, and 1
recommended next action. Fewer findings when fewer matter ("no significant unknowns" is
a valid report).

- **Surprises are never capped.** Every finding that contradicts the prior is listed,
  on top of the 3 findings.
- **No double compression.** When Technique 1 runs, its compact report IS the short
  report; do not compress it again.
- **Full output** (e.g. the five-section blind-spot report) on request ("full report")
  or at high stakes.
- **Always delivered in full**, never cut down to a short report: prototypes, interview
  questions, plans (Technique 5, including its Definition of verified), implementation
  notes, pitches (Technique 7), and quizzes. A short report may frame them.

## Phase 1: Pre-implementation techniques

### Technique 1 — Blind-spot pass (UU)

Delegate to `blindspot-scout` when a real codebase/domain sweep is involved; inline for
small conversational cases.

1. Establish goal + experience level (inferred conservatively if unstated) + the prior
   from Phase 0.
2. Explore the territory first: module, tests, git history, conventions, prior art; for
   external domains, what practitioners consider table stakes.
3. Report **compact by default** — this is the lightweight mode's short report (Phase 0),
   not something to compress again: **Surprises** when a prior was given, the **top 3
   findings** ranked by blast radius (each cited; fewer when fewer matter), and the
   **Rewritten request** (the user's request, upgraded by what you found; it serves as
   the next action). ≤ ~25 lines, not counting Surprises, which are never capped:
   **Surprises** lists every finding that contradicts the prior, or says "prior
   consistent with the territory".
4. **Full report** on request or when the case is high stakes (Cartographer seeding
   always uses it) — five sections, preceded by **Surprises** when a prior was given:
   **Landmines** (typical newcomer mistakes + repo-specific potholes, cited), **Hidden
   context** (constraining decisions and invariants, with evidence), **What good looks
   like** (2–3 real examples), **Questions you should be asking** (3–5 expert questions
   with best-guess answers + confidence), **Rewritten request**.

Stop when the report is delivered. Guardrail: prioritize architecture-changing findings;
cite evidence for every non-obvious claim.

### Technique 2 — Brainstorm & prototype (UK)

Delegate to `prototype-smith` for multi-direction artifacts. When the goal is already
clear and the user only needs options generated, a brainstorming skill (when installed)
serves instead.

1. Gather raw material (data samples, constraints, references) so options are concrete.
2. Produce N genuinely different directions (default 4) — different hierarchies, framings,
   interaction models. Variations on one idea are a failure mode.
3. One self-contained HTML artifact (`.finding-unknowns/prototypes/{slug}.html`); each
   direction labelled with a one-sentence thesis plus what it optimizes for and sacrifices.
4. Close with a reaction guide: 3–5 questions helping the user articulate what they like.

Stop when the user has reacted; convert reactions into explicit criteria before real code.
Guardrails: fake every backend; never modify the real application while prototyping.

### Technique 3 — Interview (KU)

For high-stakes cases use Cartographer mode instead — it adds regret targeting and a gate.

1. Read everything already established; never ask what is answered or discoverable.
2. Privately sort open ambiguities by blast radius: architecture-changers first (data
   model, interfaces, approach), then behavior definers (edge cases, failure modes,
   defaults), polish last — usually propose-and-move-on.
3. Ask via AskUserQuestion — up to 3 independent questions per round, each with context
   that makes it matter, 2–3 concrete options, and your recommendation. Bundle only
   questions whose answers do not depend on each other; ask a dependent follow-up in the
   next round. Accept "you decide" as an answer you then own.
4. Every few questions, checkpoint: restate all decisions in one tight list.

Stop when remaining unknowns are cheaper to discover during implementation than to ask
about — and say so. End with the final decision list. Guardrail: if an answer contradicts
an earlier decision, flag the conflict immediately.

### Technique 4 — References (UK)

1. Have the user point at the reference (path, repo, URL) and name the property they want:
   semantics, structure, feel. `blindspot-scout` can do large reads.
2. Read the underlying implementation, not a screenshot or summary.
3. Extract the transferable essence — behavior, invariants, structure — and state what
   will NOT transfer (language idioms, deps, scale assumptions).
4. Confirm the extraction before reimplementing.

Stop when the user confirms the extracted semantics. Guardrail: when the reference
conflicts with host-codebase conventions, surface the conflict; don't silently pick a side.

### Technique 5 — Implementation plan (KU)

The plan's job is to put expensive-to-change decisions in front of the user while changing
them is free — not to prove thoroughness. Markdown by default; `prototype-smith` can
render HTML on request.

1. Three-line opener: what is being built, chosen approach, single riskiest assumption.
2. **Decisions likely to change** first: data model, interfaces, API shapes, anything
   user-facing — each with the choice, one alternative, and the cost of changing later.
3. **Known unknowns and their defaults**: the default to be taken and the signal that
   would trigger a pivot.
3.5 **Definition of verified**: for each acceptance criterion, the check that will prove
   it (a test, screenshot, log or trace — something that can fail), and one line on what
   that check does NOT prove. Written now, because after the build any outcome can be
   rationalized. Checks the implementer must not edit are named here.
4. **Mechanical work** last, compressed.
5. End with the 2–4 decisions needing a yes/no or a pick.

Stop when the user rules on the flagged decisions. Guardrails: reviewable in minutes;
leave room for improvisation; present mid-planning pivots as their own decision.

## Phase 2: During implementation

### Technique 6 — Implementation notes

1. The card's delta log is the implementation notes: every entry is a delta
   (`deviation | surprise | decided-for-you`). If you also want the 4.x file, create
   `.finding-unknowns/implementation-notes.md` with headings **Deviations**, **Discovered
   edge cases**, **Questions for review**, and keep both in step.
2. When reality forces an unplanned choice: pick the conservative option (conservative =
   most reversible, not simplest), log what the plan said / what was done / why / cost to
   revisit — and keep going. Don't block the user on reversible decisions.
3. Log edge cases even when handled cleanly.
4. Irreversible or scope-changing choices are stop-points: stop at a safe checkpoint
   (SKILL.md, Building).
5. End with a five-line summary; reference the file in the handoff or PR.

Guardrails: entries 2–3 lines; an unlogged deviation is worse than no notes — the file
claims completeness.

## Phase 3: Post-implementation

### Technique 7 — Pitch & explainer

Package prototype + spec/plan + implementation notes into one document. Lead with the
demo; follow with decisions taken and the failure points an expert reviewer would probe
(pulled from Deviations). Reviewers' objections are predictable from the unknowns already
logged — answer them preemptively.

### Technique 8 — Quiz (UU, post-hoc)

The quiz runs inline: the main context writes the report, asks the questions and grades
the answers. `quiz-master` only drafts questions, from the diff, the card and the ledger
(a context that didn't write the change probes what its author glosses over); it never
grades. In 5.0 this quiz is opt-in; it is a merge gate only if the person asks for one.

1. Report first (Markdown, `.finding-unknowns/change-report.md`, by default; HTML on
   request): **Context**, **What changed** (grouped by intent, not file), **How it
   interacts** (existing paths that now behave differently, including files the diff
   doesn't show), **Decisions & assumptions**
   (defaults chosen, scope cut, requirements reinterpreted — the places a
   structurally-clean diff hides judgment), **Intuition** (2–3 mental-model updates).
2. Then 5–8 questions weighted toward deviations, edge cases, interaction effects; mix
   recall and prediction. Never trivia about names.
3. Grade honestly; for each miss give the answer AND classify it — gap in the user's
   model, or change too clever. Say which.

Stop when the user passes, or after two failed rounds → recommend simplifying or
splitting the change, not re-quizzing. Guardrail: never mark correct out of politeness; an
unexplained diff hunk absent from notes/ledger is an **unlogged deviation** — flag it.
