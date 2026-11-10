# Architecture

This document describes the design of the finding-unknowns framework: its components, the
contracts between them, and the principles that decide where a responsibility lives. The
README is the landing page; this is the reference.

## Components

```
commands/            Entry points (slash commands) — thin dispatchers, no logic
skills/
  finding-unknowns/  Before/during work — routing, techniques, Cartographer mode, guardrails
    references/      cartographer.md (normative Cartographer protocol), workflows.md
  keep-the-reasoning/  The handoff — stakes triage, handoff packet
agents/              Specialists — isolated execution profiles the main context lacks
docs/                Reference documentation (this file)
```

### Layer 1 — Commands (entry)

Commands are deliberately logic-free. Each one reads the skill and jumps to a named entry
point, passing `$ARGUMENTS` as the task:

| Command | Entry point |
|---------|-------------|
| `/finding-unknowns` | Phase 0 (quadrant routing) |
| `/blindspot` | Technique 1 (blind-spot pass) |
| `/cartographer` | Phase C (Cartographer mode) |
| `/change-quiz` | Technique 8 (quiz) |
| `/keep-the-reasoning` | Step 0 of the `keep-the-reasoning` skill (stakes triage; Step 3 if the work is done) |

Keeping commands thin means each protocol has exactly one source of truth: its `SKILL.md`.
A command never restates procedure; it names the section to execute.

### Layer 2 — The skills (protocol)

There are two sibling skills. `finding-unknowns` covers the unknowns *before and during*
work. `keep-the-reasoning` covers the human's judgment *at acceptance*: stakes triage
(offload vs keep the reasoning), a hypothesis before asking, "verified" defined up front,
and a fixed-order handoff packet (evidence first; what each check proved and did NOT
prove; decisions and assumptions; prior vs result; a fresh-context counterargument; a
never-empty "not checked"; summary last). `finding-unknowns` Phase 3 and the Phase E back
end hand over to it.

`SKILL.md` is written as an executable protocol, not a description. Its structure:

- **Contract**: `Purpose`, `Use_When`, `Do_Not_Use_When`, `Why_This_Exists` — when to
  fire and when to route elsewhere.
- **Execution_Policy**: the non-negotiables (explore before asking; up to 3 independent
  questions per round via AskUserQuestion, dependent questions one at a time; gate on
  blast radius, not confidence; discovery ends at understanding).
- **Steps**: Phase 0 (blocking quadrant routing) → Phases 1–3 (eight techniques, each a
  When / Procedure / Stop-when / Guardrails block) → Phase C (Cartographer mode, as a summary).
- **Templates**: exact per-round report and question formats, so output is reproducible
  rather than improvised.
- **Examples**: Good/Bad pairs with rationale — the strongest behavioural steering.
- **Escalation_And_Stop_Conditions** and a two-lane **Final_Checklist**.
- **References**: `references/cartographer.md` — the full normative Cartographer protocol
  (C0–C3, Phase E, resume, threshold config, checklist), read on demand before entering
  the mode. `SKILL.md` holds only its summary; the two must stay consistent, and the
  reference wins on any conflict.
- **References**: `references/workflows.md` — dynamic-workflow (Workflow tool) scripts
  for the three fan-out-heavy operations: multi-lens sweep with pipelined per-finding
  adversarial verification, a perspective-diverse refutation panel for cost ≥ 4
  resolutions, and a UU loop-until-dry probe. Each template encodes the
  fan-out/verify/merge structure deterministically and returns schema-validated ledger
  rows; a fallback ladder (Workflow → parallel Agent calls → inline) keeps the logic
  normative even where the mechanism is unavailable.

### Layer 3 — Agents (specialists)

Each agent exists because it has an execution profile the main conversation cannot match.
The governing principle: **discovery, scoring, and examination must not be performed by
the same context that implements.**

| Agent | Model | Tools | Why isolated |
|-------|-------|-------|--------------|
| `blindspot-scout` | sonnet | read-only | Wide recon in its own context window; structurally cannot drift into implementing |
| `prototype-smith` | inherit | writes throwaway files only | Diverges into N directions in one pass; sandboxed away from the real application |
| `ledger-keeper` | inherit | ledger file only | Scoring and gate verdicts need consistency and independence — a bookkeeper that did not conduct the interview will not inflate its verdict |
| `quiz-master` | inherit | read-only + report | An examiner that did not author the diff probes what the author glosses over |

Model routing (v3.7.0) follows the cost/judgment split used by mature frameworks — OMC
(opus for judgment, sonnet for execution, haiku for breadth) and Deep Research (strongest
model at the synthesis centre, cheaper fan-out) — with one adaptation: the top tier is
**`inherit`, not a pinned model.** The judgment and creative agents (scoring/gate verdict,
divergent brainstorm, independent grading) inherit the session model so they run at the
user's chosen strength and are never downgraded (Fable stays Fable, Opus stays Opus).
`blindspot-scout` is the one deliberate cost tier — `sonnet` — because recon fans out in
parallel (multi-lens sweeps run 3–5 at once) to feed a strong synthesiser; it is
overridable to `inherit` for maximum-quality single-lens passes.

Every agent declares an explicit I/O contract (inputs it needs, artifact it returns) in
its frontmatter description and body. The skill relays agent reports; it does not re-run
their exploration.

## Data artifacts

| Artifact | Producer | Consumer | Lifetime |
|----------|----------|----------|----------|
| `unknowns-ledger.md` | ledger-keeper (or skill inline) | clearing loop, gate, quiz | whole task; IS the resume state (header: threshold, locked topology, per-round quadrant score history). Rows carry a prior and a `reversibility` value (reversible · wide · irreversible) |
| `unknowns-spec-{slug}.md` | Cartographer gate PASS | Phase E execution bridge | one task; pending-approval handoff artifact, including the verification contract (per criterion: failable check, artifact, what it proves, what it does NOT prove, lane) |
| `implementation-notes.md` | build phase | quiz-master, next attempt | one build |
| `prototypes/*.html` | prototype-smith | user reaction | throwaway |
| `change-report.html` | quiz-master | merge decision | one review |

Resume semantics: Cartographer sessions resume by re-reading the ledger — no separate
state store, no re-seeding.

## Design principles

1. **One source of truth.** Procedure lives only in each skill's `SKILL.md` (and, for
   Cartographer, in `references/cartographer.md`); commands dispatch, agents execute their
   contract, docs explain.
2. **Separation of judgment.** The verdict-giving roles (gate, quiz grade) belong to
   contexts that did not produce the work being judged.
3. **Graceful degradation.** Every technique works inline with no agents and no
   commands installed; each layer is an enhancement, not a dependency.
4. **Coverage over confidence — and clarity made visible.** Cartographer gates on two
   axes: whether the four quadrants were probed (coverage), and a per-quadrant clarity
   score rolled into a weighted ambiguity figure that must reach threshold (clarity,
   adapted from oh-my-claudecode's deep-interview). Coverage catches "we never looked
   there"; the score table shown every round catches "we looked, but the user can't tell
   how clear the map is" — the fuzzy-drift failure mode a field test surfaced.
5. **Regret-priced attention.** Questions are spent where cost-if-wrong × P(wrong) is
   high; everything else gets a logged conservative default.
6. **Route-typed clearing.** Regret decides which unknown to clear first; the row's route
   decides the instrument — interview (user's head), territory (verify in code/data),
   experiment (measure), or audit (review an external artifact). The Cartographer loop is
   a router, not an interview: territory rows are never asked of the user, and pending
   experiment/audit rows suspend the loop instead of spawning useless extra rounds.
   (Field-test finding: in a real quant×DL session, the three highest-regret rows all had
   non-interview routes.)
7. **Author never self-approves.** The crystallized spec ends in an approval-gated
   execution bridge: plans are cross-validated by an independent reviewer agent, and
   execution (inline or via the `fu-execute-verified` Workflow template) pairs every
   implementer with a refute-framed verifier from a different context. No context grades
   its own work. `keep-the-reasoning` extends this to the human side: the agent that did
   the work does not get to declare it accepted, so the handoff packet states what each
   check did NOT prove and what went unchecked, and leaves the acceptance to the human.
8. **Gate on blast radius, not confidence.** Regret contains P(wrong), which is a confidence
   estimate. For rows whose `reversibility` is irreversible, confidence never substitutes
   for the user: they are never silently defaulted under the regret bar and resolve only
   with recorded user confirmation (a seventh gate condition).
9. **Hypothesis before discovery.** Each row records a prior before evidence-based scoring;
   findings that contradict it surface as surprises (blindspot-scout reports a Surprises
   section when given a prior) rather than being absorbed quietly.
10. **Checks the implementer cannot edit.** The verification contract is locked against the
    implementer, since agents can also edit their own checks.

### Phase E execution rules

Normative text is in `references/cartographer.md`; the design intent is:

- The loop lives inside a task; the graph lives between tasks. The user approves the task
  graph (lanes, touched paths, checks, edges) before execution.
- Edges must name what crosses. Unnamed edges are dropped only from reversible upstreams
  and only after the user confirms; out of `wide`/`irreversible` tasks they are kept.
  Tasks with overlapping touched paths never run concurrently. Mechanical steps are code.
- Failures return the unit with its scope: `UNIT · VERDICT · REASON · EVIDENCE · SCOPE`;
  the retry's verifier sees the previous return.
- An attempt cap (default 3) turns a task into a plan-suspect ledger row.
- A learning edge feeds derived constraints to every task not yet started; constraints
  may only tighten the spec — a conflicting one halts the run.
- Every lane requires green contract checks from a separate check-runner context with
  check files unchanged against a pre-run baseline; `wide` also requires a dependents
  check; `irreversible` never closes in-run — its checks are dry-runs, the user executes,
  post-checks close it.
- The human sits at both ends (spec, contract and task graph at the front; irreversible
  lane and merge at the back), not in the middle. Exits from discovery never waive the
  irreversibility floor.

The Workflow template `fu-execute-verified` encodes these with argument validation that
fails closed, per-task scheduling (no wave barrier), path locks, code-compared check
results and hashes, and resume inputs (`closed`, `executed`). It states which guarantees
are enforced in code and which only by prompt.

## Relationship to upstream paradigms

- Technique content derives from Thariq Shihipar's essay (see README attribution).
- `keep-the-reasoning` and the verification contract draw on Addy Osmani's "Critical
  thinking when agents do the work" (https://x.com/addyosmani/status/2117512471930167377).
  The Phase E execution rules draw on Anthropic's "Building effective agents"
  (evaluator-optimizer, orchestrator-workers) and @hanakoxbt's "Loops and Graphs"
  (https://x.com/hanakoxbt/status/2091515787366306154).
- The protocol format (contract sections, phased steps, templates, Good/Bad examples,
  stop conditions, checklists) follows the skill paradigm of
  [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode); the layered
  command → skill → agent architecture and model-tier routing likewise. This project
  intentionally does not adopt OMC's runtime machinery (state stores, hooks, settings
  resolution) — the file-based ledger provides resumability without a framework
  dependency.

Sibling OMC skills (as of OMC 5.8.1) are deferred to when installed, not duplicated:
`deep-interview` (approval-gated; its `--frontier` mode is the closest analogue of batched
independent questions plus territory routing), `ask-navigator`, `interrogate`, `loft`,
`show-me-your-work`, `blast-radius`, `in-your-own-words` / `sharpen`, and `teach`. The
mapping table is the "Relationship to sibling tooling" section of `SKILL.md`.
