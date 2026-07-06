---
name: finding-unknowns
description: "Use at the start of an ambiguous or unfamiliar task to surface the user's unknowns (unknown unknowns, unknown knowns) before, during, and after implementation — via blind-spot pass, brainstorm/prototype, interview, references, implementation plan, implementation notes, pitch, and quiz. For high-stakes work, escalate to Cartographer mode — a rigorous, quadrant-coverage-gated, regret-weighted interview backed by a lifecycle-persistent unknowns ledger. Invoke manually when scope is unclear or the domain/codebase is new."
---

# Finding Unknowns

*Distilled from Thariq Shihipar's essay "A Field Guide to Fable: Finding Your Unknowns"*
*(@trq212 — https://x.com/trq212/status/2073100352921215386). Community skill; not affiliated*
*with or endorsed by Anthropic.*

<Purpose>
The map is not the territory. The map is what the user gives you — prompt, context, skills.
The territory is where the work happens — the codebase, the real world, its constraints. The
gap between them is unknowns, and every unknown forces you to guess the user's intent. This
skill converts unknowns into knowns cheaply, before they get expensive to fix: eight
lightweight discovery techniques dispatched by quadrant, four companion agents for the cases
where isolation or independent judgement pays, and Cartographer mode — a coverage-gated,
regret-weighted protocol for high-stakes work that refuses to let implementation start while
the territory is unmapped.
</Purpose>

<Use_When>
- The user is starting work in a new domain or an unfamiliar part of the codebase
- The task involves taste — "I'll know it when I see it" criteria that resist specification
- The task is long-horizon and a wrong early assumption would compound
- A previous attempt came back wrong and the spec, not the execution, is the suspect
- The user says "blindspot pass", "unknown unknowns", "interview me", "brainstorm directions",
  "quiz me", or "Cartographer mode"
</Use_When>

<Do_Not_Use_When>
- The request is specific and trivial (typo, one-liner, obvious bug fix) — execute directly
- The user has a detailed spec with file paths and acceptance criteria — go build it
- The user wants a mathematically gated, resumable requirements spec with automatic handoff
  into execution pipelines — use `oh-my-claudecode:deep-interview` instead
- The user explicitly says "just do it" — respect that; offer one sentence of risk if
  material, then proceed
</Do_Not_Use_When>

<Why_This_Exists>
Model capability is no longer the bottleneck on long-horizon work; clarity is. Generic
requirements gathering asks "what do you want?" — but users cannot answer for the unknowns
they are not aware of. This skill's premise is that different kinds of unknowing need
different instruments: blind spots need reconnaissance, tacit taste needs reaction to
prototypes, nameable gaps need targeted questions, and comprehension needs examination. A
single uniform interview under-serves all four.
</Why_This_Exists>

<Execution_Policy>
- ALWAYS locate the unknown on the quadrant map (Phase 0) before choosing a technique
- Establish the user's starting point — where they are in their thinking, their experience
  with this problem and codebase. The same task needs different probing for an expert than
  for a first-timer
- Discovery ends at understanding. No discovery technique slides into implementation
- Never ask the user a question the territory can answer — explore the codebase first
- One question at a time in any interview. No bundles
- Architecture-changing unknowns outrank trivia, always
- "You have no significant unknowns here" is a valid and valuable result — say it plainly
  rather than manufacturing concerns
- Deviations get logged, not buried. Comprehension is the merge gate, not a green diff
- Prefer single-file self-contained HTML artifacts for anything the user must react to or
  review (prototypes, plans, quiz reports); markdown fallback for pure-terminal flows
- Delegate to companion agents when installed and the case is non-trivial; run inline
  otherwise. Every technique works standalone
</Execution_Policy>

<Steps>

## Phase 0: Locate the unknown (blocking prerequisite)

Before any technique, classify where the gap lives and announce the routing:

| | User is aware of it | User is not aware of it |
|---|---|---|
| **User knows it** | **KK — Known Knowns**: in the prompt. Write them down; implicit knowns drift. | **UK — Unknown Knowns**: know-it-when-I-see-it criteria. → Technique 2, 4 |
| **User doesn't know it** | **KU — Known Unknowns**: nameable gaps. → Technique 3, 5 | **UU — Unknown Unknowns**: blind spots. → Technique 1, 8 |

Then choose the lane and say so:

> **Routing:** {quadrant(s) identified} → {technique(s) or Cartographer mode} — {one-line reason}

Lane selection:
- Low/medium stakes, one dominant quadrant → run the matching technique(s) from Phase 1–3
- High stakes (hard to reverse, wide blast radius, unfamiliar territory + long horizon) →
  offer Cartographer mode explicitly; do not silently escalate

## Phase 1: Pre-implementation techniques

### Technique 1 — Blind-spot pass (UU)

Delegate to `blindspot-scout` when a real codebase/domain sweep is involved; inline for
small conversational cases.

1. Establish goal + experience level (inferred conservatively if unstated).
2. Explore the territory first: module, tests, git history, conventions, prior art; for
   external domains, what practitioners consider table stakes.
3. Report in exactly five sections: **Landmines** (typical newcomer mistakes + repo-specific
   potholes, cited), **Hidden context** (constraining decisions and invariants, with
   evidence), **What good looks like** (2–3 real examples), **Questions you should be
   asking** (3–5 expert questions with best-guess answers + confidence), **Rewritten
   request** (the user's request, upgraded by what you found).

Stop when the report is delivered. Guardrail: prioritize architecture-changing findings;
cite evidence for every non-obvious claim.

### Technique 2 — Brainstorm & prototype (UK)

Delegate to `prototype-smith` for multi-direction artifacts.

1. Gather raw material (data samples, constraints, references) so options are concrete.
2. Produce N genuinely different directions (default 4) — different hierarchies, framings,
   interaction models. Variations on one idea are a failure mode.
3. One self-contained HTML artifact; each direction labelled with a one-sentence thesis
   plus what it optimizes for and sacrifices.
4. Close with a reaction guide: 3–5 questions helping the user articulate what they like.

Stop when the user has reacted; convert reactions into explicit criteria before real code.
Guardrails: fake every backend; never modify the real application while prototyping.

### Technique 3 — Interview (KU)

For high-stakes cases use Cartographer mode instead — it adds regret targeting and a gate.

1. Read everything already established; never ask what is answered or discoverable.
2. Privately sort open ambiguities by blast radius: architecture-changers first (data
   model, interfaces, approach), then behavior definers (edge cases, failure modes,
   defaults), polish last — usually propose-and-move-on.
3. Exactly one question per turn: context that makes it matter, 2–3 concrete options, your
   recommendation. Accept "you decide" as an answer you then own.
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
them is free — not to prove thoroughness. `prototype-smith` can render HTML.

1. Three-line opener: what is being built, chosen approach, single riskiest assumption.
2. **Decisions likely to change** first: data model, interfaces, API shapes, anything
   user-facing — each with the choice, one alternative, and the cost of changing later.
3. **Known unknowns and their defaults**: the default to be taken and the signal that
   would trigger a pivot.
4. **Mechanical work** last, compressed.
5. End with the 2–4 decisions needing a yes/no or a pick.

Stop when the user rules on the flagged decisions. Guardrails: reviewable in minutes;
leave room for improvisation; present mid-planning pivots as their own decision.

## Phase 2: During implementation

### Technique 6 — Implementation notes

1. At build start create `implementation-notes.md` with headings: **Deviations**,
   **Discovered edge cases**, **Questions for review**.
2. When reality forces an unplanned choice: pick the conservative option (conservative =
   most reversible, not simplest), log what the plan said / what was done / why / cost to
   revisit — and keep going. Don't block the user on reversible decisions.
3. Log edge cases even when handled cleanly.
4. Irreversible or scope-changing choices go under Questions for review AND stop work at a
   safe checkpoint.
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

Delegate to `quiz-master` — an examiner that didn't write the change probes what its
author glosses over.

1. Report first: **Context**, **What changed** (grouped by intent, not file), **How it
   interacts** (existing paths that now behave differently, including files the diff
   doesn't show), **Intuition** (2–3 mental-model updates).
2. Then 5–8 questions weighted toward deviations, edge cases, interaction effects; mix
   recall and prediction. Never trivia about names.
3. Grade honestly; for each miss give the answer AND classify it — gap in the user's
   model, or change too clever. Say which.

Stop when the user passes, or after two failed rounds → recommend simplifying or
splitting the change, not re-quizzing. Guardrail: never mark correct out of politeness; an
unexplained diff hunk absent from notes/ledger is an **unlogged deviation** — flag it.

## Phase C: Cartographer mode (high-stakes escalation)

Gates on **coverage** (all four quadrants probed), persists across the **whole lifecycle**,
and targets by **regret** — not fixed weights. Announce on entry:

> Entering Cartographer mode. I will maintain unknowns-ledger.md, interview you one
> question at a time targeting the highest-regret unknown, and will not proceed to
> implementation until the coverage gate passes.

### C0: Seed the ledger

Create `unknowns-ledger.md` (owned by `ledger-keeper` when installed):

| id | quadrant | unknown | cost-if-wrong (1–5) | P(wrong) | regret | status | phase | resolution / default |
|----|----------|---------|--------------------|----------|--------|--------|-------|----------------------|

- Run Technique 1 (blind-spot pass) → seed UU rows. Naming a blind spot makes it trackable.
- Run Technique 2/4 where taste is involved → seed UK rows.
- Write down KK; list KU.
- `regret = cost-if-wrong × P(wrong)` — the only prioritization signal.
- `status ∈ {open, probing, resolved, deferred}`; deferred REQUIRES a conservative default.
  Rows are never deleted. `phase ∈ {pre, during, post}` records when the unknown surfaced.

### C1: Interview loop

Repeat until the gate passes or the user exits:

1. **Target**: the highest-regret open row (keeper picks when installed). Leave-open rule:
   rows with regret < 1.0 get a conservative default logged and are not worth a question.
2. **Ask** exactly one question aimed at that row, prefixed with the targeting rationale:

```
Round {n} | Target: {id} {unknown} | Regret: {r} ({cost}×{p}) | Why now: {one sentence}

{question with 2–3 concrete options + recommendation}
```

3. **Re-score** the row's P(wrong) from the answer; recompute regret; update the ledger.
4. **Report** after every round, in exactly this format:

```
Round {n} complete.

Ledger: {open} open | {probing} probing | {resolved} resolved | {deferred} deferred
Top regret: {id} ({regret}) — {unknown}

Coverage gate:
[{x| }] KK locked          [{x| }] KU resolved/deferred
[{x| }] UK extracted       [{x| }] UU probed
[{x| }] no open row with regret ≥ 1.0

{gate passes ? "Gate PASSED — ready to build." : "Next target: {id} — {reason}"}
```

### C2: Gate check (blocking)

Implementation may start only when ALL hold — this replaces "ambiguity ≤ threshold":

- [ ] KK locked — knowns written down
- [ ] KU resolved or deferred-with-default
- [ ] UK extracted — at least one brainstorm/prototype/reference ran
- [ ] UU probed — at least one blind-spot pass ran; findings are tracked rows
- [ ] No open row has regret ≥ 1.0

If UU was never probed the gate FAILS — that is its entire point. When `ledger-keeper` is
installed its verdict is final; never pass the gate out of politeness.

### C3: During & close-out

- Keep the ledger open through the build: every mid-build discovery becomes a row
  (quadrant + regret), conservative option chosen and logged (Technique 6 feeds the ledger).
- Post: build the quiz FROM the ledger — one question per resolved high-regret row and per
  named UU. Merge only when no open row has regret ≥ 1.0.

</Steps>

<Agent_Delegation>
| Agent | Backs | Contract: give it → it returns |
|-------|-------|-------------------------------|
| `blindspot-scout` | Technique 1, 4 | goal + experience level → five-section recon report (read-only; cannot implement) |
| `prototype-smith` | Technique 2, 5 | problem + data sources + N → one HTML artifact of N divergent directions + reaction guide (writes only throwaway files) |
| `ledger-keeper` | Cartographer | task/answers/discoveries → updated ledger, regret scores, next target, gate verdict (touches only the ledger) |
| `quiz-master` | Technique 7, 8 | diff + notes + ledger → HTML report + must-pass quiz (read-only; flags unlogged deviations) |

- Relay agent reports; do not re-run their exploration in the main context.
- The gate verdict belongs to `ledger-keeper`; the quiz belongs to `quiz-master`. Do not
  overrule either to be agreeable.
- Trivial cases stay inline; agent overhead needs a payoff.
</Agent_Delegation>

<Examples>
<Good>
Routing announcement before any technique:
```
Routing: UU + UK → blind-spot pass, then 4-direction prototype — you're new to this
subsystem (UU) and the dashboard layout is know-it-when-you-see-it (UK).
```
Why good: quadrant diagnosis is explicit, the technique choice follows from it, and the
user can veto the routing before any work happens.
</Good>

<Good>
Regret-weighted targeting in Cartographer mode:
```
Round 3 | Target: U2 "which auth path to extend" | Regret: 2.0 (4×0.5) | Why now:
highest-regret open row; a wrong guess here forces a rewrite of the middleware layer.

Should this feature extend the existing JWT middleware in src/auth/ (found via scout,
pattern: passport + JWT), or diverge with a separate flow?
  a) Extend existing (recommended — consistent, less surface)
  b) Separate flow (isolates risk, duplicates session logic)
```
Why good: names the row, shows the arithmetic, explains why now, cites scout evidence
instead of asking the user to rediscover it, offers options with a recommendation.
</Good>

<Good>
Honest gate failure:
```
Coverage gate: [x] KK [x] KU [x] UK [ ] UU [x] regret
Gate FAILED — no blind-spot pass has run. Clarity on the questions we thought to ask is
not coverage of the ones we didn't. Run the scout before building.
```
Why good: refuses to conflate "all known questions answered" with "territory mapped" —
the exact failure mode this mode exists to prevent.
</Good>

<Bad>
Bundled interview questions:
```
"What's the target audience? Also which tech stack, and how should auth work, and
where does this deploy?"
```
Why bad: four questions at once produces shallow answers and makes regret re-scoring
meaningless.
</Bad>

<Bad>
Asking what the territory can answer:
```
"Does your project use pandas or polars for the data layer?"
```
Why bad: one Grep answers this. Interview questions are for information that exists only
in the user's head.
</Bad>

<Bad>
Sliding from discovery into implementation:
```
"While doing the blindspot pass I noticed the config parser was messy, so I refactored
it and also started the feature since I was in there."
```
Why bad: discovery techniques end at understanding. Unrequested mutation during recon
destroys the user's trust that a scout is safe to run.
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **User says "just build it" mid-discovery**: stop the technique, state in ≤3 lines the
  highest-regret unresolved unknowns and the conservative defaults you will take, then
  proceed. Respect the exit; make the risk visible once, not repeatedly.
- **Interview stalls** (answers stop changing any row's regret): stop interviewing; the
  remaining unknowns are cheaper to discover during implementation. Say so.
- **Two failed quiz rounds**: recommend simplifying or splitting the change. Do not keep
  quizzing.
- **Scout finds nothing significant**: report "no significant blindspots" and end — do not
  pad the report.
- **Cartographer round 10 without gate progress**: surface the top-3 stuck rows and ask
  the user to resolve, defer-with-default, or exit to lightweight techniques.
- **Any technique asked to mutate product code**: refuse within the technique; discovery
  is read-only except for its own artifacts (prototypes/, notes, ledger, reports).
</Escalation_And_Stop_Conditions>

<Final_Checklist>
Lightweight lane:
- [ ] Phase 0 routing was announced (quadrant → technique) before any technique ran
- [ ] No discovery technique mutated product code
- [ ] Interview questions were single, blast-radius-ordered, and non-discoverable
- [ ] Artifacts delivered in reactable form (HTML default) with a reaction guide
- [ ] Deviations logged at decision time, not reconstructed afterwards

Cartographer lane (additionally):
- [ ] Ledger exists with quadrant, cost, P(wrong), regret, status, phase per row
- [ ] Every round reported the ledger summary + gate checklist in the standard format
- [ ] Gate verdict came from ledger-keeper when installed; UU probe was not skipped
- [ ] Deferred rows all carry conservative defaults; no rows were deleted
- [ ] Quiz was generated from the ledger; merge recommendation followed the pass rule
</Final_Checklist>

<Advanced>
## Resume

The ledger IS the state. To resume an interrupted Cartographer session, re-read
`unknowns-ledger.md` (and `implementation-notes.md` if the build started), announce the
current gate status, and continue from the highest-regret open row. Do not re-seed.

## Defaults (override by telling the skill)

| Knob | Default | Meaning |
|------|---------|---------|
| Prototype directions N | 4 | genuinely different directions per brainstorm |
| Regret question bar | 1.0 | rows below this get defaults, not questions |
| Quiz size | 5–8 | questions per round |
| Quiz rounds | 2 | before recommending simplify/split |
| Cartographer soft cap | 10 rounds | then surface stuck rows |

## Relationship to heavier tooling

- Want mathematical ambiguity thresholds, topology/ontology tracking, resumable spec
  state, and an execution bridge into autopilot/ralph/team → use
  `oh-my-claudecode:deep-interview`. Cartographer trades that machinery for quadrant
  coverage and lifecycle persistence; they are complementary, not competing.
- Divergent option generation as a discipline → `superpowers:brainstorming`. Rigorous
  written plans → `superpowers:writing-plans` / `oh-my-claudecode:plan`. Spec already
  concrete → skip discovery and execute.
</Advanced>
