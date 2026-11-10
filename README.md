<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns v4.0.0 — map the territory before you build; keep the reasoning when agents hand the work back" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-D97757?style=for-the-badge" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/version-4.0.0-141413?style=for-the-badge" alt="version 4.0.0">
  <img src="https://img.shields.io/badge/skills-2-C15F3C?style=for-the-badge" alt="2 skills">
  <img src="https://img.shields.io/badge/agents-4-D4A27F?style=for-the-badge" alt="4 agents">
  <img src="https://img.shields.io/badge/license-MIT-788C5D?style=for-the-badge" alt="MIT license">
</p>

<p align="center"><strong>Surface your unknowns before they get expensive — and keep your judgment when agents hand the work back.</strong></p>

<p align="center">
  <a href="#-quick-start">Quick start</a> ·
  <a href="#-how-it-works">How it works</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#-demo">Demo</a> ·
  <a href="README.zh.md">中文</a>
</p>

---

## ⚡ TL;DR

- **Two skills, one lifecycle.** `finding-unknowns` surfaces what you don't know *before and during* the work; `keep-the-reasoning` keeps your judgment *at the handoff*, when you accept what the agent built.
- **Route by quadrant, not by habit.** Every unknown is placed on a four-quadrant map first; the quadrant picks one of eight cheap techniques — blind-spot pass, prototype, interview, references, plan, notes, pitch, quiz.
- **Cartographer mode for high stakes.** A regret-ordered unknowns ledger, per-quadrant clarity scores shown every round, a seven-condition gate, and an approval-gated execution bridge. Irreversible steps always reach you.
- **Plain Markdown, zero dependencies.** Four optional agents and Workflow scripts add depth; every technique also runs fully inline.

## 💡 Inspiration

**The map is not the territory.** The map is what you give Claude — prompt, context, skills. The territory is where the work actually happens — the codebase and the real world. The gap between them is made of unknowns, and every unknown forces the model to guess your intent. Model capability is no longer the bottleneck on long-horizon work; clarity is.

Generic requirements gathering asks "what do you want?" — but nobody can answer for unknowns they aren't aware of. Different kinds of unknowing need different instruments: blind spots need reconnaissance, tacit taste needs prototypes to react to, nameable gaps need targeted questions, comprehension needs examination.

> **Attribution.** The techniques and their names come from Thariq Shihipar's essay _"A Field Guide to Fable: Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)). Credit for the underlying ideas belongs to the original author; this repository packages them as an installable Claude Code plugin.

**The handoff problem.** Agents now produce fast, mostly-correct work — and mostly-correct work does not demand a second look. Across many handoffs the human slides down a spectrum: **offloading** (delegate the work, keep ownership) → **deferral** (the output stops being a hypothesis and becomes the next input) → **cognitive surrender** (the output quietly becomes your own). Nothing in an agentic workflow pushes back on that slide by default. `keep-the-reasoning` is the push-back, applied at the one moment it is cheap — distilled from Addy Osmani's _"Critical thinking when agents do the work"_ ([source](https://x.com/addyosmani/status/2117512471930167377)).

## 🛠 What it does

| Skill | Covers | What you get |
|-------|--------|--------------|
| `finding-unknowns` | Before & during work | Phase 0 quadrant routing → eight techniques → optional Cartographer mode |
| `keep-the-reasoning` | The handoff | Stakes triage, "verified" defined up front, a fixed-order handoff packet |

`finding-unknowns` hands over to `keep-the-reasoning` at the end of Phase 3 and of the Cartographer execution bridge.

<p align="center">
  <img src="assets/lifecycle.svg" alt="Lifecycle: four windows — pre, during, post, handoff — with the techniques in each, the two human touchpoints, and the unknowns ledger persisting underneath" width="92%">
</p>

**Locate the unknown first.** Phase 0 is blocking: classify the gap, capture your prior in one line, and announce the route before any technique runs.

<p align="center">
  <img src="assets/quadrants.svg" alt="The four quadrants: known knowns, known unknowns, unknown knowns, unknown unknowns — each mapped to its techniques" width="78%">
</p>

| Phase | Technique | Quadrant | Use for |
|-------|-----------|----------|---------|
| Pre | 1 · Blind-spot pass | UU | Unknown unknowns in a new domain or codebase |
| Pre | 2 · Brainstorm & prototype | UK | "I'll know it when I see it" |
| Pre | 3 · Interview | KU | Nameable gaps — up to 3 independent questions per round; dependent questions wait for the next round |
| Pre | 4 · References | UK | When you can't describe it — point at code |
| Pre | 5 · Implementation plan | KU | Expensive-to-change decisions first, plus a definition of "verified" |
| During | 6 · Implementation notes | — | Deviations and edge cases, logged as they happen |
| Post | 7 · Pitch & explainer | — | Buy-in and approvals |
| Post | 8 · Quiz | UU (post-hoc) | Comprehension check before merge |

Known knowns just get written down before they drift. Full procedures live in [`SKILL.md`](skills/finding-unknowns/SKILL.md).

**Cartographer mode** — the rigorous escalation for high-stakes work. It won't let implementation start while the territory is unmapped.

- **Unknowns ledger** — every row carries a quadrant, a prior, `regret = cost-if-wrong × P(wrong)`, a **route** (interview · territory · experiment · audit) and a **reversibility** (reversible · wide · irreversible). The ledger *is* the resume state.
- **A router, not an interview** — each round clears the highest-regret open row by its route. Territory rows are never asked of the user.
- **Clarity you can see** — all four quadrants are re-scored every round: `ambiguity = 1 − (KK×0.20 + KU×0.25 + UK×0.25 + UU×0.30)`, threshold 0.25 by default.
- **Dual gate** — coverage (every quadrant probed) AND clarity, plus the irreversibility floor. A PASS crystallizes a pending-approval spec with a verification contract.

**keep-the-reasoning** — the acceptance-time protocol.

- **Stakes triage first** — `offload` (cheap, reversible, lands only on you) or `keep-the-reasoning` (lands on others, hard to reverse).
- **Hypothesis before asking; "verified" before building** — a check must be able to fail. "The model is confident" is not a check.
- **Fixed-order handoff packet** — evidence first, what each check proved and did NOT prove, decisions & assumptions, prior vs result, a fresh-context counterargument, a never-empty "not checked", summary last.
- **After the handoff** — a rejection becomes a rule (a test, hook, or lint rule); surrender signals are named once, without moralizing.

## 🚀 Quick start

**Requirements:** Claude Code (CLI, desktop app, or IDE extension). No runtime, no dependencies — skills, agents, and commands are plain Markdown. `bash` only for `install.sh`.

**A — plugin marketplace (recommended)**

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
/plugin install finding-unknowns@finding-unknowns-skill
```

**B — clone and install** (both skills, `references/`, the four agents, and the slash commands)

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && bash install.sh
```

**C — passive drop-in, no install.** Copy [`CLAUDE.md`](CLAUDE.md) into a project root for lightweight, always-on guidance.

<details>
<summary><b>D — manual copy</b></summary>

```bash
mkdir -p ~/.claude/skills/finding-unknowns/references ~/.claude/skills/keep-the-reasoning
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
cp skills/keep-the-reasoning/SKILL.md ~/.claude/skills/keep-the-reasoning/
```

</details>

### 60-second tour

```
/finding-unknowns <task>             # Phase 0: locate the unknown, announce the route, run the technique
/blindspot <goal or area>            # read-only recon: landmines, hidden context, expert questions
/cartographer --deep <task>          # high stakes: ledger, scored clearing loop, dual gate, execution bridge
/change-quiz [diff range]            # change report + must-pass comprehension quiz before merge
/keep-the-reasoning [work/decision]  # stakes triage, then the evidence-first handoff packet
```

No plugin? Invoke the `finding-unknowns` skill through the Skill tool, or just ask: _"do a blind-spot pass"_, _"interview me"_, _"brainstorm four directions"_. [`EXAMPLES.md`](EXAMPLES.md) has copy-paste prompts.

<details>
<summary><b>Configuration (optional — zero config by default)</b></summary>

**Clarity threshold.** Cartographer's weighted-ambiguity gate defaults to `0.25`. Override per project or per user in `.claude/settings.json` (project overrides user); Cartographer announces the resolved threshold and its source on entry.

```json
{ "findingUnknowns": { "ambiguityThreshold": 0.25 } }
```

**Depth presets.** A flag overrides any settings value.

| Flag | Threshold | Use for |
|------|-----------|---------|
| `/cartographer --quick <task>` | 0.35 | quick orientation, lower-stakes work |
| `/cartographer --standard <task>` | 0.25 (default) | most tasks |
| `/cartographer --deep <task>` | 0.15 | high-stakes, hard-to-reverse work |

**Other defaults** — prototype directions (4), regret question bar (1.0, never applied to irreversible rows), quiz size and rounds, Cartographer round caps (soft 10 / hard 20), execution attempt cap (3) — live in the **Defaults** table in [`SKILL.md`](skills/finding-unknowns/SKILL.md) and can be overridden in plain language.

</details>

## 🎬 Demo

> _Illustrative transcripts, written to the output templates in the two `SKILL.md` files and `references/cartographer.md` — not recordings of real sessions._

**1 · Phase 0 routing** — announced before any technique runs, so you can veto it.

```
> /finding-unknowns add a usage dashboard to the admin app

Prior: "a few charts over the existing usage table"
Routing: UU + UK → blind-spot pass, then 4-direction prototype — you're new to this
subsystem (UU) and the dashboard layout is know-it-when-you-see-it (UK).
```

**2 · A Cartographer round report** — scores and the seven-condition gate after every round, so you steer instead of discovering drift at the end.

```
Round 3 complete.

Ledger: 4 open | 1 probing | 6 resolved | 2 deferred
Top regret: U2 (2.0) — which auth path to extend [route: interview]

| Quadrant      | Score   | Weight        | Gap                                        |
|---------------|---------|---------------|--------------------------------------------|
| KK            | 0.90    | 0.20          | clear                                      |
| KU            | 0.50    | 0.25          | auth path (U2) undecided                   |
| UK            | 0.70    | 0.25          | session-UX criteria not yet confirmed      |
| UU            | 0.70    | 0.30          | two scout lenses run; not yet dry          |
| **Ambiguity** | **31%** | threshold 25% | KU × auth middleware — U2 sets the design  |

Coverage gate:
[x] KK locked          [ ] KU resolved/deferred
[x] UK extracted       [x] UU probed
[ ] no open row with regret ≥ 1.0
[x] every irreversible row user-confirmed
[ ] ambiguity 31% ≤ threshold 25%

Next target: U2 — highest-regret open row; a wrong guess forces a rewrite of the
middleware layer.
```

**3 · A keep-the-reasoning handoff packet** — evidence first, limits stated, summary last.

```
Handoff lane: keep-the-reasoning — schema migration on a shared production table.
1. Evidence: `pytest tests/migrations -q` → 14 passed; `alembic upgrade head --sql` →
   plan at artifacts/upgrade.sql (ALTER + backfill, 2 statements)
2. Proved: upgrade SQL applies cleanly to an empty schema. NOT proved: runtime on the
   41M-row table; lock behaviour under write load. Tests written in this session.
3. Decisions: backfill default = 'unknown' (spec silent); downgrade drops the column
   (data loss) — see migrations/0042.py:31
4. Your prior: "a quick additive change". Mismatch: the backfill rewrites every row.
5. Counterargument (fresh subagent): if writes continue during backfill, the table lock
   stalls checkout. Not checked.
6. Missed: the replica lag alert threshold.
7. Not checked: lock duration at production size; replica lag.
8. Would you bet on this in front of the on-call? If not: run it on the staging snapshot.
9. Summary: migration is correct on small data; production behaviour unverified.
```

The anti-pattern it replaces: _"Done! The migration is ready and all tests pass ✅."_

## 🏗 How it works

### Architecture

**Commands dispatch, skills decide, agents execute, documents persist.** Procedure lives in exactly one place per skill — its `SKILL.md`; for Cartographer, the normative protocol is [`references/cartographer.md`](skills/finding-unknowns/references/cartographer.md), read on demand. Every technique works standalone; commands and agents are enhancements, not dependencies. Full design reference: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

<p align="center">
  <img src="assets/framework.svg" alt="Framework layers: five slash commands dispatch into two skills, which delegate to four specialist agents that write persistent artifacts" width="96%">
</p>

| Layer | Contents | Role |
|-------|----------|------|
| Commands | `/finding-unknowns` `/blindspot` `/cartographer` `/change-quiz` `/keep-the-reasoning` | Thin entry points; name a skill section, pass arguments |
| Skills | `finding-unknowns`, `keep-the-reasoning` | The protocols: routing, techniques, Cartographer, guardrails; the handoff |
| Agents | four specialists | Isolated execution profiles with explicit I/O contracts |
| Artifacts | ledger, spec, notes, prototypes, report | Persistent state; the ledger is the resume point |
| References | `cartographer.md`, `workflows.md` | Full Cartographer protocol; optional Workflow scripts with a fallback ladder |

**Discovery, scoring, and examination are never done by the context that implements.** A scout that cannot edit files cannot drift into building; a bookkeeper that did not run the interview will not inflate its gate verdict; an examiner that did not write the diff asks harder questions.

| Agent | Model | Tools | Backs | Why isolated |
|-------|-------|-------|-------|--------------|
| `blindspot-scout` | sonnet | read-only | Blind-spot pass, References | Wide recon in its own context window; structurally cannot implement |
| `prototype-smith` | inherit | writes throwaway files only | Prototype, Plan | N genuinely divergent directions in one pass, sandboxed from the real app |
| `ledger-keeper` | inherit | ledger file only | Cartographer | Regret, clarity scores, and the gate verdict — without grading its own interview |
| `quiz-master` | inherit | read-only + report | Pitch, Quiz | Fresh-eyes examiner that did not author the change; flags unlogged deviations |

**Model routing.** Judgment and creative agents use `model: inherit`, so they run at the session's own strength and are never downgraded. `blindspot-scout` is the one deliberate cost tier (`sonnet`) because recon fans out in parallel; set it to `inherit` for single-lens passes. The scheme follows OMC's role tiers and Deep Research's "strongest model at the synthesis centre, cheaper fan-out" — with the top tier inherited rather than pinned.

### Cartographer, end to end

<p align="center">
  <img src="assets/cartographer.svg" alt="Cartographer mode: Round 0 topology, seeded unknowns ledger, regret-ordered clearing loop by route, per-round quadrant scores, dual gate with irreversibility floor, approval-gated execution bridge" width="96%">
</p>

Threshold announced → Round 0 topology (1–6 components) confirmed → **C0** seed the ledger from all four quadrants plus a domain checklist → **C1** clear by route, adversarially verify cost ≥ 4 resolutions, re-score every round → **C2** dual gate + completeness critic → **C2.5** close-out report and crystallized spec → **E** approval-gated execution bridge (independent planner + reviewer consensus, or Workflow execution) → **C3** the ledger stays open through the build and feeds the quiz.

**New in v4.0.0**

- **Irreversibility floor.** Regret contains P(wrong) — a confidence estimate. For `irreversible` rows, confidence never substitutes for the user: never silently defaulted under the regret bar, resolved only with recorded user confirmation. It is the seventh gate condition, and no exit waives it.
- **Priors and surprises.** Each row records the expectation held before evidence-based scoring; contradictions surface as surprises instead of being absorbed.
- **Verification contract.** The crystallized spec lists, per criterion, a failable check, its artifact, what it proves, what it does NOT prove, and its lane — locked against the implementer.
- **Phase E execution rules.** The loop lives inside a task, the graph between tasks. Edges must name what crosses; failures return `UNIT · VERDICT · REASON · EVIDENCE · SCOPE`; an attempt cap turns a task into a plan-suspect row; a learning edge feeds derived constraints forward; tasks close by reversibility lane on results from a separate check-runner. The human sits at both ends — spec, contract, and task graph at the front; irreversible lane and merge at the back.

### Workflow orchestration

When the host exposes Claude Code's **Workflow tool** and you opt in, the fan-out-heavy operations run as deterministic scripts from [`references/workflows.md`](skills/finding-unknowns/references/workflows.md):

<p align="center">
  <img src="assets/workflows.svg" alt="Execution: fail-closed validation, a task graph whose edges name what crosses, a verified loop per task with correction and learning edges, reversibility lanes, a human at both ends, plus the discovery templates and fallback ladder" width="96%">
</p>

| Script | Does |
|--------|------|
| `fu-multi-lens-sweep` | Parallel lens scouts; each finding adversarially verified as its lens completes (no barrier); schema-validated ledger rows |
| `fu-verify-panel` | Three refuters (alternative explanation / evidence independence / reproduction) for cost ≥ 4 resolutions |
| `fu-uu-until-dry` | UU probe loop that stops after two consecutive dry rounds — bounded by information, not a count |
| `fu-execute-verified` | Approved execution under Phase E rules: every implementer paired with an independent refute-framed verifier |

**Fallback ladder:** Workflow → parallel Agent calls → fully inline. The logic is normative; the mechanism is not. When execution runs with no subagents at all, implementer and verifier would share a context, so no lane closes automatically — every task comes to you as `awaiting-human`.

**Enforced in code vs by prompt — stated honestly.** In `fu-execute-verified`, code enforces fail-closed argument validation, no silent edge drops, per-task scheduling, path locks, lane-based closing, and the comparison of check results and check-file hashes against a pre-run baseline. Still *prompted*: the check-runner's report itself, the implementer not executing irreversible actions, and the runner refusing irreversible checks. Verifier independence is structural.

### The handoff

<p align="center">
  <img src="assets/handoff.svg" alt="keep-the-reasoning: the offloading → deferral → cognitive-surrender spectrum, and the fixed-order handoff packet from evidence to summary" width="96%">
</p>

The agent that did the work does not get to declare it accepted. When `finding-unknowns` already ran, `keep-the-reasoning` reuses its priors, its verification contract, and the quiz-master's Decisions & assumptions rather than repeating them.

## 🧗 Challenges we ran into

- **The interview was the wrong instrument.** In a live field test (a quant × deep-learning research task), the three highest-regret unknowns all had non-interview routes. Cartographer's loop became a router with a `route` column; territory rows are never asked of the user, and pending experiments suspend the loop instead of spawning empty rounds. (v3.3.0)
- **A strong result is not a resolved one.** A strong RankIC result looked like it settled "is the signal real?" — but leakage produces the same IC. Cost ≥ 4 rows now need an adversarial check and two independent sources before they count as resolved. (v3.4.0)
- **Users couldn't see the model's certainty.** A second field test: discovery was strong, but work drifted into a fuzzy zone the user could not steer. Fix: per-quadrant clarity scores shown every round, scored in one call from ledger evidence only, with "score drift" named as a failure mode. (v3.6.0)
- **Confidence vs blast radius.** Regret multiplies by P(wrong) — the input most prone to optimism — so a confident agent could silently default an irreversible step. v4 adds the irreversibility floor: gate on blast radius, not confidence.
- **Our own executor failed open.** An independent adversarial review of `fu-execute-verified` found 1 CRITICAL and 6 HIGH issues, reproduced against a stubbed runtime — including argument validation that let an unknown or missing lane through. Validation now fails closed, check-file tampering stops the task, and edits outside declared paths halt the run. Three review rounds later, the fixes are exercised by a 50-scenario harness against a stubbed agent runtime.
- **Saying no to good-sounding advice.** "Approve only the last step" was deliberately not adopted — a human reviewing only a final artifact they never framed is rubber-stamping.

## 🧩 How it compares

`finding-unknowns` is a lightweight orienting layer, not an execution engine. These tools are complementary: use it to locate an unknown, then escalate to the right specialist.

| Property | finding-unknowns | Deep Interview ([OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)) | OMC execution (autopilot / ralph / team) | [Superpowers](https://github.com/obra/superpowers) |
|----------|------------------|-------------------------|-------------------------|-----------------------|
| Altitude | Meta / orienting | One phase: requirements | Execution & delivery | Discipline primitives |
| Lifecycle | Pre · During · Post | Pre only | During · Post | Mostly single-phase |
| Rigor | Flexible | Ambiguity gating | Verification-gated | Checklist-driven |
| State | Stateless (Cartographer: ledger file) | Persisted, resumable | Persisted, multi-agent | Varies |
| Best when | You don't yet know your unknowns | You need a validated spec | The spec is clear | You need one disciplined move |

Deep Interview (as of OMC 5.8.1) is approval-gated; its `--frontier` mode is the closest analogue of batched independent questions plus territory routing. Cartographer *adopts* its transparency machinery — clarity scores with a threshold, Round 0 topology, challenge modes — and keeps the axes a clarity-scoring interview alone does not cover.

<details>
<summary><b>Cartographer vs Deep Interview, axis by axis</b></summary>

| Axis | Deep Interview | Cartographer mode |
|------|----------------|-------------------|
| Gate criterion | Ambiguity ≤ threshold (goal/constraint/criteria) | Dual: coverage (all four quadrants probed, blind-spot pass required) AND per-quadrant weighted ambiguity ≤ threshold, plus the irreversibility floor |
| Blind spots (UU) | Not modelled | First-class; heaviest weight (0.30) |
| Lifecycle | Ends at the specification | One ledger, seeded pre, appended during, closed post |
| Prioritisation | Fixed dimension weights | Regret orders rows; ambiguity scores quadrants |
| Clearing instrument | Socratic Q&A | Route-typed per unknown: interview / territory / experiment / audit |
| Execution | Approval-gated handoff into OMC pipelines | Approval-gated bridge: planner + reviewer consensus, or Workflow execution with per-task refute-framed verification |

```
finding-unknowns  (orient: which quadrant is this unknown in?)
        ├─ a light reframe is sufficient            → the eight techniques
        ├─ high-stakes, want a coverage gate         → Cartographer mode
        ├─ want ambiguity gating + resumable state   → OMC Deep Interview
        ├─ divergent option generation               → superpowers:brainstorming
        ├─ a rigorous written plan                   → superpowers:writing-plans / omc-plan
        ├─ the specification is already concrete     → OMC autopilot / ralph / team
        └─ the work is done, the risk is the handoff → keep-the-reasoning
```

</details>

**Defer, don't duplicate.** When a sibling is installed, `finding-unknowns` uses it for the mechanism it owns and keeps the unknowns lens — quadrant routing, regret-priced rows, route-typed clearing, the reversibility floor, lifecycle persistence.

| Need | Sibling (when installed) |
|------|--------------------------|
| Accepting agent output without surrendering judgment | `keep-the-reasoning` (this repository) |
| Ontology tracking, OMC state, ralplan/autopilot handoff | `oh-my-claudecode:deep-interview` |
| Fog test and decision tickets on a tracker | `oh-my-claudecode:ask-navigator` |
| Adversarial review of a diff or design | `oh-my-claudecode:interrogate` |
| Throwaway prototype to settle a design | `oh-my-claudecode:loft` |
| Decision trail for autonomous work | `oh-my-claudecode:show-me-your-work` |
| Prove a change's blast radius | `oh-my-claudecode:blast-radius` |
| Restate the brief before starting | `oh-my-claudecode:in-your-own-words` / `sharpen` |
| Learner-paced explanation | `oh-my-claudecode:teach` |

## 🔭 What's next

Not done yet, stated plainly:

- **Run `fu-execute-verified` in a live Workflow runtime.** So far it has been exercised only against a stubbed agent runtime.
- **Move the remaining prompted guarantees into code** where the runtime allows — today the check-runner's report and the irreversible-action refusals rely on prompts.
- **Chinese-language diagram variants.** [README.zh.md](README.zh.md) currently reuses the English SVGs.
- **Ontology / entity-convergence tracking** — consciously deferred in v3.6.0 because the Round 0 topology gate covers convergence more cheaply; to revisit if component drift shows up in tests.

## 📁 Project layout

<details>
<summary><b>Repository tree</b></summary>

```
finding-unknowns-skill/
├── .claude-plugin/          Plugin and marketplace manifests (/plugin install)
├── commands/                Slash-command entry points (thin dispatchers)
│   ├── finding-unknowns.md    /finding-unknowns — Phase 0 routing
│   ├── blindspot.md           /blindspot — blind-spot pass
│   ├── cartographer.md        /cartographer — Cartographer mode
│   ├── change-quiz.md         /change-quiz — report + merge quiz
│   └── keep-the-reasoning.md  /keep-the-reasoning — the handoff
├── skills/
│   ├── finding-unknowns/
│   │   ├── SKILL.md         Routing, eight techniques, Cartographer summary
│   │   └── references/
│   │       ├── cartographer.md  Full Cartographer protocol (normative), read on demand
│   │       └── workflows.md     Workflow templates + fallback ladder
│   └── keep-the-reasoning/
│       └── SKILL.md         Stakes triage, handoff packet
├── agents/                  blindspot-scout (sonnet) · prototype-smith · ledger-keeper · quiz-master (inherit)
├── docs/ARCHITECTURE.md     Design reference: layers, contracts, principles
├── assets/                  README diagrams (SVG)
├── AGENTS.md                Repository guide for coding agents and contributors
├── EXAMPLES.md              Copy-paste, end-to-end prompts
├── CLAUDE.md                Passive single-file drop-in
├── install.sh               Installer (skills + references + agents + commands)
├── CONTRIBUTING.md · CHANGELOG.md · LICENSE (MIT)
└── README.md (English, canonical) · README.zh.md (简体中文)
```

</details>

## 🔄 Updating

Update with the same method you installed with. The latest release is **v4.0.0**.

```
/plugin marketplace update finding-unknowns-skill
/plugin update finding-unknowns@finding-unknowns-skill
```

<details>
<summary><b>Clone-and-install, manual copy, and version check</b></summary>

**Option B** — `install.sh` overwrites in place, so it doubles as the updater:

```bash
cd finding-unknowns-skill && git pull origin main && bash install.sh
```

**Option D** — overwrite the same files. `references/` carries the Cartographer protocol and the Workflow templates and must be updated too; v4 also adds the `keep-the-reasoning` skill.

```bash
cd finding-unknowns-skill && git pull origin main
mkdir -p ~/.claude/skills/finding-unknowns/references ~/.claude/skills/keep-the-reasoning
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
cp skills/finding-unknowns/references/*.md ~/.claude/skills/finding-unknowns/references/
cp skills/keep-the-reasoning/SKILL.md ~/.claude/skills/keep-the-reasoning/
cp agents/*.md   ~/.claude/agents/
cp commands/*.md ~/.claude/commands/
```

**Verify the installed version:**

```bash
grep '"version"' ~/.claude/plugins/*/finding-unknowns*/.claude-plugin/plugin.json 2>/dev/null \
  || ls ~/.claude/skills/finding-unknowns/references/cartographer.md ~/.claude/skills/keep-the-reasoning/SKILL.md
# expect: 4.0.0 (plugin) — or both files listed (they exist only from v4.0.0 on)
```

</details>

## 🤝 Contributing

Contributions are welcome — new techniques, prompt refinements, documentation, diagrams. Start with [CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and local validation, and [AGENTS.md](AGENTS.md) for the repository's invariants.

## 🙏 Credits & license

- Technique ideas and names: Thariq Shihipar, _"A Field Guide to Fable: Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)).
- `keep-the-reasoning` and the verification contract: Addy Osmani, _"Critical thinking when agents do the work"_ ([source](https://x.com/addyosmani/status/2117512471930167377)).
- Phase E execution rules: Anthropic's _"Building effective agents"_ (evaluator-optimizer, orchestrator-workers) and @hanakoxbt's _"Loops and Graphs"_ ([source](https://x.com/hanakoxbt/status/2091515787366306154)).
- Cartographer's ambiguity gating, topology gate, and challenge modes are adapted from the deep-interview skill in [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode); the comparison also references [Superpowers](https://github.com/obra/superpowers).

Released under the [MIT License](LICENSE).

**Disclaimer.** This is an independent community project. It is not affiliated with, authorised by, or endorsed by Anthropic.
