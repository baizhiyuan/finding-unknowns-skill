---
name: finding-unknowns
description: "Surface the user's unknowns before, during, and after implementation — quadrant routing into eight cheap techniques (blind-spot pass, prototype, interview, references, plan, notes, pitch, quiz), escalating to Cartographer mode (coverage-gated, regret-ordered unknowns ledger with an approval-gated execution bridge) for high-stakes work. For ambiguous or unfamiliar tasks; not for concrete specs or trivial fixes."
aliases: []
metadata:
  credits:
    techniques: "Thariq Shihipar — A Field Guide to Fable: Finding Your Unknowns"
    url: "https://x.com/trq212/status/2073100352921215386"
    ambiguity-gating: "oh-my-claudecode deep-interview (Ouroboros-inspired)"
    verification-contract: "Addy Osmani — Critical thinking when agents do the work"
    execution-rules: "evaluator-optimizer / orchestrator-workers (Anthropic, Building effective agents); return-the-unit and edge heuristics from @hanakoxbt, Loops and Graphs"
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
- The user wants ontology/entity-convergence tracking, OMC state persistence, or
  OMC-native handoff into ralplan/autopilot/ralph/team — use
  `oh-my-claudecode:deep-interview` instead (see Relationship to sibling tooling)
- The work is done and the risk is the *handoff* — the user accepting agent output
  without engaging — use the sibling skill `keep-the-reasoning`
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
- Hypothesis before discovery: record what the user (or you) expects *before* a scout,
  interview, or prototype runs. Findings that contradict the prior are the most valuable
  output — surface them as surprises, never quietly absorb them
- Establish the user's starting point — where they are in their thinking, their experience
  with this problem and codebase. The same task needs different probing for an expert than
  for a first-timer
- Discovery ends at understanding. No discovery technique slides into implementation
- Never ask the user a question the territory can answer — explore the codebase first
- Interview via AskUserQuestion (clickable options). Up to 3 *independent* questions per
  round, ordered by blast-radius/regret; never bundle *dependent* questions — where one
  answer would change the next question's framing, ask those one at a time
- Architecture-changing unknowns outrank trivia, always
- Gate on blast radius, not confidence: an unknown guarding an irreversible step
  (migration, deletion, production data, money, publication) always reaches the user,
  however confident the evidence looks
- "You have no significant unknowns here" is a valid and valuable result — say it plainly
  rather than manufacturing concerns
- Deviations get logged, not buried. Comprehension is the merge gate, not a green diff
- Prefer single-file self-contained HTML artifacts for anything the user must react to or
  review (prototypes, plans, quiz reports); markdown fallback for pure-terminal flows
- Delegate to companion agents when installed and the case is non-trivial; run inline
  otherwise. Every technique works standalone. Where an installed sibling skill already
  owns a mechanism (see Relationship to sibling tooling), prefer it over re-implementing
</Execution_Policy>

<Steps>

## Phase 0: Locate the unknown (blocking prerequisite)

Before any technique, classify where the gap lives and announce the routing:

| | User is aware of it | User is not aware of it |
|---|---|---|
| **User knows it** | **KK — Known Knowns**: in the prompt. Write them down; implicit knowns drift. | **UK — Unknown Knowns**: know-it-when-I-see-it criteria. → Technique 2, 4 |
| **User doesn't know it** | **KU — Known Unknowns**: nameable gaps. → Technique 3, 5 | **UU — Unknown Unknowns**: blind spots. → Technique 1, 8 |

Capture the prior in one line — what the user expects the answer or outcome to be (ask
only if it is not inferable; "no idea yet" is a valid prior and itself routes to UU).

Then choose the lane and say so:

> **Routing:** {quadrant(s) identified} → {technique(s) or Cartographer mode} — {one-line reason}

Lane selection:
- Low/medium stakes, one dominant quadrant → run the matching technique(s) from Phase 1–3
- High stakes (hard to reverse, wide blast radius, unfamiliar territory + long horizon) →
  offer Cartographer mode explicitly; do not silently escalate. Before entering, read
  `references/cartographer.md`

## Phase 1: Pre-implementation techniques

### Technique 1 — Blind-spot pass (UU)

Delegate to `blindspot-scout` when a real codebase/domain sweep is involved; inline for
small conversational cases.

1. Establish goal + experience level (inferred conservatively if unstated) + the prior
   from Phase 0.
2. Explore the territory first: module, tests, git history, conventions, prior art; for
   external domains, what practitioners consider table stakes.
3. Report in five sections — preceded by **Surprises** when a prior was given:
   **Landmines** (typical newcomer mistakes + repo-specific
   potholes, cited), **Hidden context** (constraining decisions and invariants, with
   evidence), **What good looks like** (2–3 real examples), **Questions you should be
   asking** (3–5 expert questions with best-guess answers + confidence), **Rewritten
   request** (the user's request, upgraded by what you found). **Surprises** lists every
   finding that contradicts the prior, or says "prior consistent with the territory"

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
them is free — not to prove thoroughness. `prototype-smith` can render HTML.

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
claims completeness. When `oh-my-claudecode:show-me-your-work` is installed and the run is
long or autonomous, its append-only decision trail may serve as the Deviations log —
reference its path from the notes rather than duplicating entries.

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
   doesn't show), **Decisions & assumptions** (defaults chosen, scope cut, requirements
   reinterpreted — the places a structurally-clean diff hides judgment), **Intuition**
   (2–3 mental-model updates).
2. Then 5–8 questions weighted toward deviations, edge cases, interaction effects; mix
   recall and prediction. Never trivia about names.
3. Grade honestly; for each miss give the answer AND classify it — gap in the user's
   model, or change too clever. Say which.

Stop when the user passes, or after two failed rounds → recommend simplifying or
splitting the change, not re-quizzing. Guardrail: never mark correct out of politeness; an
unexplained diff hunk absent from notes/ledger is an **unlogged deviation** — flag it.

## Phase C: Cartographer mode (high-stakes escalation) — summary

**Blocking: read `references/cartographer.md` in full before entering.** This section is
the map; that file is the normative protocol (ledger schema, round template, gate,
close-out report, spec, verification contract, execution rules).

What it is: a coverage-gated, clarity-scored, regret-ordered discovery loop backed by
`unknowns-ledger.md`, persisting from pre-build through review. Its shape:

1. **Announce the clarity threshold** (first line; flag > project > user > default 0.25) and
   confirm the **Round 0 topology** (1–6 independently-failing components).
2. **C0 Seed** the ledger from all four quadrants — blind-spot pass (UU), prototypes or
   references (UK), knowns (KK), named gaps (KU) — plus a domain checklist. Each row
   carries a prior, `regret = cost × P(wrong)`, a **route** (interview · territory ·
   experiment · audit), and a **reversibility** (reversible · wide · irreversible).
3. **C1 Clearing loop** — a router, not an interview: clear the highest-regret row by its
   route; adversarially verify cost ≥ 4 resolutions; re-score all four quadrants every
   round and show the score table so the user can steer.
4. **C2 Dual gate** — coverage (all quadrants probed) AND clarity (weighted ambiguity ≤
   threshold), plus the **irreversibility floor**: no irreversible row is ever defaulted
   silently or resolved without the user. Completeness critic before any PASS.
5. **C2.5 Close-out** — structured unknowns report + crystallized spec with a
   **verification contract** ("verified" defined before building; every check can fail
   and states what it does NOT prove; checks locked against the implementer).
6. **E Execution bridge** — approval-gated. Execution runs tasks as loops inside a graph:
   edges must name what crosses, failures return per unit with SCOPE, derived
   constraints flow forward (learning edge), and lanes close tasks by reversibility —
   the irreversible lane always waits for the user. The author never self-approves.
7. **C3** — the ledger stays open through the build; the quiz is generated from it.

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
- Trivial cases stay inline; agent overhead needs a payoff. Cost anchors: a codebase
  blind-spot pass typically costs ~50–100k subagent tokens and a few minutes — worth it
  when a wrong assumption forces a redesign; not worth it for a one-file question.
- For cost ≥ 4 verification of a *diff or design* (rather than a ledger claim),
  `oh-my-claudecode:interrogate` — three reviewers on different models, findings only
  with a reproducing run — is a stronger instrument than a same-model refuter panel; use
  it when installed.
- For high-stakes tasks, `blindspot-scout` may be run as a multi-lens sweep: several
  parallel scouts, each with ONE named lens (e.g. domain-risk / engineering / statistics)
  stated in its prompt. Merge their findings into the ledger; duplicate findings across
  lenses are confirmation, not waste.
- **Workflow orchestration (preferred at Cartographer stakes when available)**: the three
  fan-out-heavy operations — multi-lens sweep, cost ≥ 4 verification panel, UU
  loop-until-dry — have ready-to-run Workflow scripts in `references/workflows.md`, with
  structured (schema-validated) outputs that feed the ledger mechanically; a fourth,
  `fu-execute-verified`, runs approved execution under Phase E's rules. Workflow use
  requires the user's orchestration opt-in; the file's fallback ladder covers plain-Agent
  and fully-inline environments. The logic is normative; the mechanism is not.

### Model routing

Route by role, the way OMC does (opus for judgment/reasoning, sonnet for execution, haiku
for cheap breadth) and Deep Research does (the strongest model synthesises at the centre;
cheaper sub-agents fan out). The twist: the top tier is **`inherit`, not a pinned model** —
respect the model the session is already running (Fable / Opus / Sonnet) and never downgrade
its reasoning strength.

| Role | Agent | Model | Why |
|------|-------|-------|-----|
| Orchestrator / task centre | (the main conversation) | the session model | your chosen strength runs the interview, routing, and synthesis |
| Judgment — scoring & gate verdict | `ledger-keeper` | `inherit` | the verdict must be as strong as the session, not capped at opus |
| Creative — divergent brainstorm | `prototype-smith` | `inherit` | idea quality is the skill's core value |
| Judgment — independent grading | `quiz-master` | `inherit` | examination is judgment work |
| Breadth — reconnaissance | `blindspot-scout` | `sonnet` (overridable to `inherit`) | fans out in parallel (multi-lens sweep = 3–5 instances); cheap breadth feeding a strong synthesiser |

`inherit` uses Claude Code's native subagent model-selection: a `[1m]` session resolves to
its base tier for subagents — reasoning strength preserved, the 1M context (which subagents
do not need) is not. In Workflow scripts the same rule holds: scout stages carry
`agentType: 'blindspot-scout'` (→ sonnet); scoring and verification stages omit `model` so
they inherit the session's strength.
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
Coverage gate: [x] KK [x] KU [x] UK [ ] UU [x] regret [x] irreversible [x] ambiguity
Gate FAILED — no blind-spot pass has run. Clarity on the questions we thought to ask is
not coverage of the ones we didn't. Run the scout before building.
```
Why good: refuses to conflate "all known questions answered" with "territory mapped" —
the exact failure mode this mode exists to prevent.
</Good>

<Good>
Irreversibility floor overriding a low regret score:
```
U7 "backfill rewrites historical rows in place" | cost 5 × P(wrong) 0.15 = regret 0.75 |
reversibility: irreversible → below the 1.0 bar, but NOT defaulted. Asking:
The backfill overwrites 2.1M rows with no snapshot. Proceed how?
  a) Snapshot first, then backfill (recommended — makes the step reversible)
  b) Backfill in place (accept the risk)
```
Why good: regret alone would have silently defaulted this row because the agent felt
confident; the floor routes it to the user, and the recommended option converts an
irreversible step into a reversible one — the cheapest risk reduction there is.
</Good>

<Bad>
Bundling dependent questions in one prose blob:
```
"What's the target audience? And given that, which tech stack, and given the stack, how
should auth work, and where does that deploy?"
```
Why bad: each answer changes the next question's framing, so asking them together forces
shallow answers and makes regret re-scoring meaningless. Independent questions are fine to
batch (up to 3) via AskUserQuestion's clickable options — chained ones are not.
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
  proceed. Respect the exit; make the risk visible once, not repeatedly. The one thing an
  exit never waives: an unknown guarding an irreversible step gets its own one-line
  confirmation (or its step waits for the user) before that step runs.
- **Interview stalls** (answers stop changing any row's regret): stop interviewing; the
  remaining unknowns are cheaper to discover during implementation. Say so.
- **Two failed quiz rounds**: recommend simplifying or splitting the change. Do not keep
  quizzing.
- **Scout finds nothing significant**: report "no significant blindspots" and end — do not
  pad the report.
- **Cartographer round 10 without gate progress**: surface the top-3 stuck rows and ask
  the user to resolve, defer-with-default, or exit to lightweight techniques.
- **Interview question times out / user is away**: the row stays `open` (no re-score
  without an answer), mark it "re-askable", report the round with the gate suspended, and
  deliver whatever territory/experiment routes can proceed without the user. Never invent
  an answer on the user's behalf.
- **Only probing rows with pending experiments/audits remain**: stop looping — further
  rounds add no information. State the clearing actions and suspend; resume from the
  ledger when results arrive.
- **Any technique asked to mutate product code**: refuse within the technique; discovery
  is read-only except for its own artifacts (prototypes/, notes, ledger, reports).
</Escalation_And_Stop_Conditions>

<Final_Checklist>
Lightweight lane:
- [ ] Phase 0 routing was announced (quadrant → technique) before any technique ran
- [ ] The prior was captured before discovery; contradicting findings surfaced as surprises
- [ ] No discovery technique mutated product code
- [ ] Interview questions were blast-radius-ordered, non-discoverable, ≤3 per round, and
      never bundled when dependent
- [ ] Artifacts delivered in reactable form (HTML default) with a reaction guide
- [ ] Plans defined "verified" up front: a failable check per criterion + what it misses
- [ ] Deviations logged at decision time, not reconstructed afterwards

Cartographer lane: additionally run the checklist at the end of
`references/cartographer.md`.
</Final_Checklist>

<Advanced>
## Resume

The ledger IS the state — see `references/cartographer.md` § Resume. Do not re-seed.

## Defaults (override by telling the skill)

| Knob | Default | Meaning |
|------|---------|---------|
| Prototype directions N | 4 | genuinely different directions per brainstorm |
| Regret question bar | 1.0 | rows below this get defaults, not questions — never applies to irreversible rows |
| Quiz size | 5–8 | questions per round |
| Quiz rounds | 2 | before recommending simplify/split |
| Cartographer soft cap | 10 rounds | then surface stuck rows / show scores |
| Cartographer hard cap | 20 rounds | proceed, noting residual ambiguity |
| Ambiguity threshold | 0.25 | settings `findingUnknowns.ambiguityThreshold`, or --quick 0.35 / --deep 0.15 |
| Consensus iterations | 3 | planner↔reviewer loops in Phase E option 1 |
| Execution attempt cap | 3 per task | then the task becomes a plan-suspect ledger row |
| Questions per round | ≤3 independent | interview-route rows batched per round (dependent ones one at a time) |

## Relationship to sibling tooling

Prefer an installed sibling when it owns the mechanism; this skill owns the *unknowns
lens* — quadrant routing, regret-priced rows, route-typed clearing, the reversibility
floor, and lifecycle persistence from discovery through review.

| Need | Sibling (when installed) | Relationship |
|------|--------------------------|--------------|
| Accepting agent output without surrendering judgment | `keep-the-reasoning` (this repo) | the handoff half — Phase 3 and Phase E's back end hand over to it |
| Ontology tracking, OMC state, ralplan/autopilot handoff | `oh-my-claudecode:deep-interview` | Cartographer's ambiguity gating, topology gate and challenge modes are adapted from it; its `--frontier` mode is the closest analogue of batched independent questions + territory routing. Both are approval-gated. Use it when you want the OMC runtime |
| Fog test + decision tickets on a tracker | `oh-my-claudecode:ask-navigator` | ticket types map onto routes (research ≈ territory, loft ≈ experiment, grilling ≈ interview); use it when decisions must live in an issue tracker rather than a ledger file |
| Adversarial review of a diff/design | `oh-my-claudecode:interrogate` | stronger than a same-model panel for cost ≥ 4 code claims (C1 step 3.5) |
| Throwaway prototype to settle a design | `oh-my-claudecode:loft` | an alternative backend for Technique 2 |
| Decision trail for autonomous work | `oh-my-claudecode:show-me-your-work` | may serve as Technique 6's Deviations log |
| Prove a change's blast radius | `oh-my-claudecode:blast-radius` | runs the checks; this skill only ranks by blast radius |
| Restate the brief before starting | `oh-my-claudecode:in-your-own-words` / `sharpen` | lighter than Technique 1 when the gap is wording, not territory |
| Learner-paced explanation | `oh-my-claudecode:teach` | Technique 8 grades and gates merge; teach only paces |

Divergent option generation as a discipline → `superpowers:brainstorming`. Rigorous
written plans → `superpowers:writing-plans` / `oh-my-claudecode:plan`. Spec already
concrete → skip discovery and execute.
</Advanced>
