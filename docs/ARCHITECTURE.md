# Architecture

This document describes the design of the finding-unknowns framework: its components, the
contracts between them, and the principles that decide where a responsibility lives. The
README is the landing page; this is the reference. Terms (lane, rigor level, packet size,
mode, prior, fresh-context refutation, schema) are defined once in the
[Glossary](GLOSSARY.md); the [5-minute tutorial](TUTORIAL.md) is the hands-on entry.

## Components

```
commands/            Entry points (/blindspot, /cartographer, /change-quiz) — thin dispatchers, no logic
skills/
  finding-unknowns/  Before/during work — routing, techniques, Cartographer mode, guardrails
    references/      cartographer.md (normative Cartographer protocol), workflows.md
  keep-the-reasoning/  The handoff — stakes triage, handoff packet
  theory-vs-result/  Measured results — prediction card, Theory → Measured → Consistent? → Mechanism cards
agents/              Specialists — isolated execution profiles the main context lacks
docs/                Reference documentation: this file, GLOSSARY.md, TUTORIAL.md (+ .zh)
```

### Layer 1 — Commands (entry)

The three skills need no command: Claude Code exposes each skill as a slash command, so
`/finding-unknowns`, `/keep-the-reasoning` and `/theory-vs-result` invoke the skill
directly, starting at its own first step (Phase 0; Step 0 stakes triage; Step 0 triage:
Debug path or rigor level). Until 4.2 the plugin also shipped command files with those
same names; a command and a skill sharing a name collide (the command shadows the skill
and, by invoking the skill of its own name, risks recursion), so 4.3.0 removed them.

The remaining commands are deliberately logic-free. Each one invokes the
`finding-unknowns` skill through the Skill tool (so plugin and manual installs resolve the
same way, with no hard-coded file path) and jumps to a named entry point, passing
`$ARGUMENTS` as the task:

| Command | Entry point |
|---------|-------------|
| `/blindspot` | Technique 1 (blind-spot pass) |
| `/cartographer` | Phase C (Cartographer mode) |
| `/change-quiz` | Technique 8 (quiz) |

Keeping commands thin means each protocol has exactly one source of truth: its `SKILL.md`.
A command never restates procedure; it names the section to execute.

### Layer 2 — The skills (protocol)

There are three sibling skills. `finding-unknowns` covers the unknowns *before and during*
work. `keep-the-reasoning` covers the human's judgment *at acceptance*: stakes triage
into a packet size (offload · compact · full), a prior before asking, "verified" defined up front,
and a fixed-order handoff packet sized to the stakes: a compact four-section packet at
medium stakes (evidence; what the checks did NOT prove; a never-empty "not checked";
summary), the full nine-section packet at high stakes or on request (evidence first; what
each check proved and did NOT prove; decisions and assumptions; prior vs result; the
strongest counterargument and "did I miss anything?" from a fresh-context refutation; a
never-empty "not checked"; summary last). Packet
sections are referred to by name, not number; the compact packet adds a Prior vs result
line when a prior was recorded or the claim is measured. `finding-unknowns` Phase 3 and
Cartographer's merge (and the back end of the experimental Phase E, when it runs) hand
over to it; Cartographer's merge always gets the full packet.

The third, `theory-vs-result`, covers *measured results*: a result is reported as a
fixed card — Theory → Measured → Consistent? → Mechanism — with the prediction written
before the data (else `post-hoc`), a noise floor, fairness checks, a consistency verdict,
and mechanism evidence tiers (verified · supported · inferred · untested). The *rule
verdict* (PASS · FAIL · UNCERTAIN · descriptive only) is kept apart from the *direction
verdict* (alive · alive-but-constrained · weakened · dead), and a new or tightened
threshold is explained in plain language and approved before it is frozen. Step 0 picks
a rigor level (note · report · decision), or the lighter **Debug path** for a
reproducible, deterministic failure: repro + observed output, prior, at least two
competing explanations, one discriminating check each, fix, and the repro re-run plus an
unchanged neighbour; no noise floor, no frozen rule, and an escalation to a rigor level
when the failure is flaky or a ship/no-ship rides on it. It meets `finding-unknowns` at
the `experiment` route and `keep-the-reasoning` at the packet's Prior vs result section.

The three skills share two things by name rather than each defining its own. A **prior**
(any expectation recorded before the result) captured by one skill in a session is reused
by the others, never asked twice; a `theory-vs-result` prediction card is its
measured-claim form. The **fresh-context refutation** primitive is defined once, in
`keep-the-reasoning`: a context that did not produce a claim tries to refute it from the
same evidence and returns the strongest alternative explanation plus the cheapest
discriminating check; without a separate context the fallback is labelled
`same-context — weaker`. It fills the full packet's Strongest counterargument and Did I
miss anything?, and, with its own mechanics on top, backs `theory-vs-result`'s
Fresh_Context_Check (`mechanism-auditor`), Cartographer's C1 step 3.5 adversarial check,
and the `fu-verify-panel` workflow.

`SKILL.md` is written as an executable protocol, not a description. Its structure:

- **Contract**: `Purpose`, `Use_When`, `Do_Not_Use_When`, `Why_This_Exists` — when to
  fire and when to route elsewhere.
- **Execution_Policy**: the non-negotiables (explore before asking; up to 3 independent
  questions per round via AskUserQuestion, dependent questions one at a time; gate on
  blast radius, not confidence; discovery ends at understanding; lightweight by default:
  a short report of 3 findings with evidence + 1 next action, the full output on request or at high stakes;
  text first: Markdown reports, HTML on request, prototypes stay HTML).
- **Steps**: Phase 0 (blocking quadrant routing) → Phases 1–3 (eight techniques, each a
  When / Procedure / Stop-when / Guardrails block) → Phase C (Cartographer mode, as a summary).
- **Templates**: exact per-round report and question formats, so output is reproducible
  rather than improvised.
- **Examples**: Good/Bad pairs with rationale — the strongest behavioural steering.
- **Escalation_And_Stop_Conditions** and a **Final_Checklist** per mode (lightweight,
  Cartographer).
- **References**: `references/cartographer.md` — the full normative Cartographer protocol
  (C0–C3, the § E1 next-step offer and the experimental § E2 Workflow execution, resume,
  settings, checklist), read on demand before entering
  the mode. `SKILL.md` holds only its summary; the two must stay consistent, and the
  reference wins on any conflict.
- **References**: `references/workflows.md` — dynamic-workflow (Workflow tool) scripts
  for the three fan-out-heavy operations: multi-lens sweep with pipelined per-finding
  adversarial verification, a perspective-diverse refutation panel for cost ≥ 4
  resolutions, and a UU loop-until-dry probe; plus `fu-execute-verified` for § E2
  (experimental, optional; not yet run in a live Workflow runtime; only on the user's
  explicit request). Each template encodes the
  fan-out/verify/merge structure deterministically and returns schema-validated ledger
  rows; a fallback ladder (Workflow → parallel Agent calls → inline) keeps the logic
  normative even where the mechanism is unavailable.

### Layer 3 — Agents (specialists)

Each agent exists because it has an execution profile the main conversation cannot match.
The governing principle: **discovery, scoring, and examination must not be performed by
the same context that implements.**

| Agent | Model | Tools | Why isolated |
|-------|-------|-------|--------------|
| `blindspot-scout` | sonnet | no Write/Edit; Bash for inspection (by instruction) | Wide recon in its own context window; without file-editing tools it cannot quietly start implementing |
| `prototype-smith` | inherit | Write + Bash; throwaway files only (by instruction) | Diverges into N directions in one pass; instructed to stay away from the real application (not a sandbox) |
| `ledger-keeper` | inherit | ledger file only | Scoring and gate verdicts need consistency and independence — a bookkeeper that did not conduct the interview will not inflate its verdict |
| `quiz-master` | inherit | no Write/Edit; Bash for inspection and its report (by instruction) | An examiner that did not author the diff probes what the author glosses over |
| `mechanism-auditor` | inherit | no Write/Edit; Bash for inspection and recomputation into /tmp (by instruction) | The context that predicted an effect and measured it believes its own mechanism; a fresh referee re-derives the numbers and downgrades unearned verdicts and tiers |

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

Every file the skills write lives under `.finding-unknowns/` at the project root, created
on first write. It is working state: the default `.gitignore` line is `.finding-unknowns/`.
A team that reviews ledgers and specs in PRs ignores the contents instead and re-includes
the two files (git cannot re-include a file inside an ignored directory):

```
.finding-unknowns/*
!.finding-unknowns/unknowns-ledger.md
!.finding-unknowns/unknowns-spec-*.md
```

| Artifact | Producer | Consumer | Lifetime |
|----------|----------|----------|----------|
| `.finding-unknowns/unknowns-ledger.md` | ledger-keeper (or skill inline) | clearing loop, gate, quiz | whole task; IS the resume state. First line `schema: 2`, then the header (depth + source, locked topology, UK status (in scope, or not applicable with the user's confirmation), per-round quadrant score history). Rows carry a prior and a `reversibility` value, the row's lane (reversible · wide · irreversible) |
| `.finding-unknowns/predictions/{slug}.md` (or the ledger row) | theory-vs-result Step 1 | the measurement, mechanism-auditor | one claim; saved before measuring with a `Written` line, so timing can be audited (a timestamp when the folder is gitignored) |
| result cards + summary table, or the Debug path record | theory-vs-result Steps 0–4 | user, mechanism-auditor, Cartographer ledger, keep-the-reasoning Prior vs result | one report |
| `.finding-unknowns/unknowns-spec-{slug}.md` | Cartographer gate PASS | user approval; consensus-refine plan (§ E1); the experimental § E2 Workflow execution (on request) | one task; the default end of Cartographer; pending-approval handoff artifact, including the verification contract (per criterion: failable check, artifact, what it proves, what it does NOT prove, lane) |
| `.finding-unknowns/implementation-notes.md` | build phase | quiz-master, next attempt | one build |
| `.finding-unknowns/prototypes/*.html` | prototype-smith | user reaction | throwaway |
| `.finding-unknowns/change-report.md` (`.html` on request) | quiz-master | merge decision | one review |
| `.finding-unknowns/handoff-{slug}.md` | keep-the-reasoning Step 3, when the packet is written to disk | user, reviewers | one handoff |

Resume semantics: Cartographer sessions resume by re-reading the ledger — no separate
state store, no re-seeding. Two upgrade paths, both owned by `ledger-keeper`'s RESUME
operation (inline otherwise):

- **Legacy location.** If `.finding-unknowns/unknowns-ledger.md` is absent but a pre-4.3
  root-level `unknowns-ledger.md` exists, it is read (with any root-level notes and specs)
  and a one-line move offer goes to the user. Nothing is moved silently; until the user
  agrees, work continues on the root-level files. Likewise, `theory-vs-result` reads a
  pre-4.3 prediction card at root `predictions/{slug}.md` in place (its `Written` line
  stands) and offers the move into `.finding-unknowns/predictions/`.
- **Schema upgrade.** A ledger whose first line is not `schema: 2` is schema 1. The missing
  header fields are reconstructed from the rows where possible and written as
  `{value} (reconstructed, legacy)`, otherwise marked `unknown (legacy)`, and each
  addition is reported. A reconstructed or `unknown (legacy)` field never satisfies a gate
  condition until the user confirms it; the marker is then removed.

## Design principles

1. **One source of truth.** Procedure lives only in each skill's `SKILL.md` (and, for
   Cartographer, in `references/cartographer.md`); commands dispatch, agents execute their
   contract, docs explain.
2. **Separation of judgment.** The verdict-giving roles (gate, quiz grade) belong to
   contexts that did not produce the work being judged.
3. **Graceful degradation.** Every technique works inline with no agents and no
   commands installed; each layer is an enhancement, not a dependency.
4. **Coverage over confidence — and clarity made visible.** Cartographer gates on six
   ledger-checkable conditions: KK written down; KU resolved or deferred-with-default; UK
   extracted, or marked not applicable with the user's confirmation; UU probed; no open
   row with regret ≥ 1.0; every irreversible row user-confirmed. Per-quadrant clarity
   scores, rolled into a weighted ambiguity figure (adapted from oh-my-claudecode's
   deep-interview), are display-only: shown every round, never a gate condition. Coverage
   catches "we never looked there"; the score table catches "we looked, but the user
   can't tell how clear the map is" — the fuzzy-drift failure mode a field test surfaced
   — without letting a self-scored figure decide when building starts. Depth flags set
   breadth, not a threshold (`--quick` single-lens pass; `--standard` one blind-spot
   pass, escalating to a multi-lens sweep when the task spans more than one risk domain;
   `--deep` always a multi-lens sweep + UU loop-until-dry); a soft check at round 10 and
   every 10 rounds after (5 and every 5 under `--quick`) replaces any hard cap.
5. **Regret-priced attention.** Questions are spent where cost-if-wrong × P(wrong) is
   high; everything else gets a logged conservative default.
6. **Route-typed clearing.** Regret decides which unknown to clear first; the row's route
   decides the instrument — interview (user's head), territory (verify in code/data),
   experiment (measure), or audit (review an external artifact). The Cartographer loop is
   a router, not an interview: territory rows are never asked of the user, and pending
   experiment/audit rows suspend the loop instead of spawning useless extra rounds.
   (Field-test finding: in a real quant×DL session, the three highest-regret rows all had
   non-interview routes.)
7. **Author never self-approves.** Cartographer ends at the crystallized spec by
   default; nothing executes without a separate yes. Plans are cross-validated by an
   independent reviewer agent, and execution under the experimental Phase E (inline or
   via the `fu-execute-verified` Workflow template, only on request) pairs every
   implementer with a refute-framed verifier from a different context. No context grades
   its own work. `keep-the-reasoning` extends this to the human side: the agent that did
   the work does not get to declare it accepted, so the handoff packet states what each
   check did NOT prove and what went unchecked, and leaves the acceptance to the human.
8. **Gate on blast radius, not confidence.** Regret contains P(wrong), which is a confidence
   estimate. For rows whose `reversibility` is irreversible, confidence never substitutes
   for the user: they are never silently defaulted under the regret bar and resolve only
   with recorded user confirmation (the sixth gate condition). The same holds after the
   spec: in any build, whatever the execution path, the implementer prepares each
   irreversible change and its exact command but executes none; the user runs it or gives
   a per-command yes, and post-checks run before the row closes.
9. **Prior before discovery.** Each row records a prior before evidence-based scoring;
   findings that contradict it surface as surprises (blindspot-scout reports a Surprises
   section when given a prior) rather than being absorbed quietly. A prior recorded by any
   of the three skills is reused by the others, never asked twice.
10. **Checks the implementer cannot edit.** The verification contract is locked against the
    implementer, since agents can also edit their own checks.
11. **Prediction before measurement; two verdicts never merged.** A theory written after the
    data is labelled `post-hoc`. The verdict under the pre-agreed rule is final for that run;
    the judgment about the direction is separate, and a mechanism can keep a direction alive
    but cannot overturn a rule verdict.

### Phase E execution rules

**Status: experimental, optional; not yet run in a live Workflow runtime.** The default end
of Cartographer is the spec (C2.5), followed by the § E1 next-step offer (consensus plan,
or keep refining), which is the default and not experimental. Workflow execution (§ E2)
runs only on the user's explicit request. Normative text is in
`references/cartographer.md`; the design intent is:

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
- Every lane (reversibility, the only meaning of "lane" in this repository) requires
  green contract checks from a separate check-runner context with check files unchanged against a pre-run baseline; `wide` also requires a dependents
  check; `irreversible` never closes in-run — its checks are dry-runs, the user executes,
  post-checks close it (the C2.5 build rule, applied per task).
- The human sits at both ends (spec, contract and task graph at the front; irreversible
  lane and merge at the back), not in the middle. Exits from discovery never waive the
  irreversibility floor.

The Workflow template `fu-execute-verified` encodes these with argument validation that
fails closed, per-task scheduling (no wave barrier), path locks, code-compared check
results and hashes, and resume inputs (`closed`, `executed`). It states which guarantees
are enforced in code and which only by prompt.

## Relationship to upstream paradigms

- Technique content derives from Thariq Shihipar's essay (see README attribution).
- `theory-vs-result` is distilled from the author's own empirical research practice, generalized for any
  measured claim.
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
