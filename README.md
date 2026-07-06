<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns — a Claude Code skill" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Skill-8A63D2" alt="Claude Code Skill">
  <img src="https://img.shields.io/badge/scope-global-5B8DEF" alt="global scope">
  <img src="https://img.shields.io/badge/trigger-manual-F59E0B" alt="manual trigger">
  <img src="https://img.shields.io/badge/covers-pre_%C2%B7_during_%C2%B7_post-2DD4BF" alt="lifecycle">
  <img src="https://img.shields.io/badge/license-MIT-22C55E" alt="MIT license">
</p>

<p align="center"><em>The map is not the territory. The quality of long-horizon work is bounded by how well you clarify your <strong>unknowns</strong>.</em></p>

`finding-unknowns` is a Claude Code skill-and-agent framework that helps you surface what you
do not yet know — before, during, and after implementation — so that ambiguity is resolved
with cheap questions up front rather than expensive rework later. A single orchestrating
skill provides eight discovery techniques and a rigorous gated mode; four companion agents
back the techniques where isolation, divergence, or independent judgement pays.

> **Attribution.** This skill distills Thariq Shihipar's essay _"A Field Guide to Fable:
> Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)). Credit
> for the underlying ideas and technique names belongs to the original author; this repository
> packages them as an installable Claude Code skill.

---

## Overview

The **map** is what you give Claude (the prompt, context, and skills). The **territory** is
where the work actually happens (the codebase and the real world). The gap between them is
made of unknowns, and every unknown forces the model to guess your intent.

This skill provides eight concrete techniques for surfacing those unknowns across the full
task lifecycle, plus an optional rigorous mode ("Cartographer mode") for high-stakes work.

<p align="center">
  <img src="assets/lifecycle.svg" alt="Three windows to catch unknowns: pre, during, post" width="92%">
</p>

## Features

- **Four-quadrant framing** — classify a gap as a known or unknown unknown before acting.
- **Blind-spot pass** — surface the unknowns you were not aware you had, tuned to your context.
- **Brainstorm and prototype** — react to several throwaway directions before committing code.
- **Interview** — one question at a time, prioritising answers that change the architecture.
- **References** — treat existing source code as the richest available specification.
- **Implementation plan** — lead with the decisions most likely to change.
- **Implementation notes** — record deviations during the build for later review.
- **Pitch and quiz** — a review artifact for buy-in, and a comprehension check before merge.
- **Cartographer mode** — a gated, regret-weighted interview backed by a persistent ledger.
- **Companion agents** — four specialists (`blindspot-scout`, `prototype-smith`,
  `ledger-keeper`, `quiz-master`) the skill delegates to when depth pays.

## Architecture

The framework is layered — commands dispatch, the skill decides, agents execute, documents
persist. Procedure lives in exactly one place (`SKILL.md`); every other layer either enters
it or carries out a contract from it. Every technique works standalone — commands and
agents are enhancements, not dependencies. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
for the full design reference.

| Layer | Contents | Role |
|-------|----------|------|
| Commands | `/finding-unknowns` `/blindspot` `/cartographer` `/change-quiz` | Thin entry points; name a skill section, pass arguments |
| Skill | `SKILL.md` | The protocol: quadrant routing, eight techniques, Cartographer mode, guardrails |
| Agents | four specialists | Isolated execution profiles with explicit I/O contracts |
| Artifacts | ledger, notes, prototypes, report | Persistent state; the ledger is the resume point |
| Workflows | `references/workflows.md` | Optional dynamic-workflow scripts for the fan-out-heavy operations; degrade to plain agents or inline |

<p align="center">
  <img src="assets/framework.svg" alt="Framework: one skill orchestrating four specialist agents" width="96%">
</p>

| Agent | Model | Backs | Execution profile |
|-------|-------|-------|-------------------|
| `blindspot-scout` | sonnet | Blind-spot pass, References | Read-only reconnaissance; explores in its own context window and structurally cannot start implementing |
| `prototype-smith` | sonnet | Brainstorm & prototype, Implementation plan | Sandboxed to new throwaway files; produces N genuinely divergent directions in one pass |
| `ledger-keeper` | opus | Cartographer mode | Independent bookkeeper for the unknowns ledger; scores regret and rules on the coverage gate without grading its own work — verdicts get the strongest model |
| `quiz-master` | sonnet | Quiz, Pitch & explainer | Fresh-eyes examiner that did not author the change; probes what the author would gloss over |

The separation follows one principle: **discovery, scoring, and examination should not be
performed by the same context that implements.** A scout that cannot edit files cannot
drift into building; a bookkeeper that did not conduct the interview will not inflate its
gate verdict; an examiner that did not write the diff asks harder questions.

## The four quadrants

Locate where an unknown lives; the quadrant indicates which technique to use.

<p align="center">
  <img src="assets/quadrants.svg" alt="The four quadrants of unknowns" width="78%">
</p>

## Installation

**Option A — plugin marketplace:**

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
/plugin install finding-unknowns@finding-unknowns-skill
```

**Option B — clone and install:**

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill
bash install.sh              # installs the skill and the four companion agents
```

**Option C — passive drop-in (no installation):** copy [`CLAUDE.md`](CLAUDE.md) into a project
root for lightweight, always-on guidance.

**Option D — manual copy:**

```bash
mkdir -p ~/.claude/skills/finding-unknowns
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
```

## Usage

At the start of an ambiguous or unfamiliar task, invoke the skill through the Skill tool:

```
finding-unknowns
```

With the plugin installed, slash commands provide direct entry points:

| Command | Enters at |
|---------|-----------|
| `/finding-unknowns <task>` | Phase 0 — quadrant routing, then the matching technique |
| `/blindspot <goal or area>` | Blind-spot pass (reconnaissance only) |
| `/cartographer <task>` | Cartographer mode — ledger, interview loop, coverage gate |
| `/change-quiz [diff range]` | Change report + must-pass comprehension quiz |

Individual techniques can also be requested in plain language, for example: _"do a
blind-spot pass"_, _"interview me"_, or _"brainstorm four directions"_. See
[`EXAMPLES.md`](EXAMPLES.md) for complete, copy-paste prompts.

## The eight techniques

| Phase  | Technique              | Use for                                          |
|--------|------------------------|--------------------------------------------------|
| Pre    | Blind-spot pass        | Unknown unknowns in a new domain or codebase     |
| Pre    | Brainstorm & prototype | Unknown knowns — "I'll know it when I see it"     |
| Pre    | Interview              | Residual ambiguity after brainstorming           |
| Pre    | References             | When you cannot describe it — point at code      |
| Pre    | Implementation plan    | Surface the risky decisions early                |
| During | Implementation notes   | Edge cases that force a deviation                |
| Post   | Pitch & explainer      | Buy-in and approvals                             |
| Post   | Quiz                   | Confirm understanding before merge               |

Full prompts for each technique are documented in
[`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md).

## Cartographer mode

The eight techniques are lightweight probes. Cartographer mode is the rigorous escalation for
high-stakes work: a gated interview that does not permit implementation until the problem space
is adequately mapped. It is inspired by the Deep Interview skill in
[oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode), and re-optimised along
three axes that a clarity-scoring interview does not address.

<p align="center">
  <img src="assets/cartographer.svg" alt="Cartographer mode: coverage gate, unknowns ledger, regret-weighted targeting" width="96%">
</p>

| Axis              | Deep Interview                          | Cartographer mode                                                        |
|-------------------|-----------------------------------------|--------------------------------------------------------------------------|
| Gate criterion    | Ambiguity ≤ threshold (known dimensions) | Coverage — all four quadrants probed, including a required blind-spot pass |
| Blind spots (UU)  | Not modelled                            | First-class; expanding the map is the purpose of the gate                |
| Lifecycle         | Ends at the specification               | One ledger, seeded pre, appended during, closed post                     |
| Prioritisation    | Fixed dimension weights                 | Regret = cost-if-wrong × P(wrong); items below 1.0 are deferred          |
| Clearing instrument | Socratic Q&A only                     | Route-typed per unknown: interview / territory-verify / experiment / audit — the loop is a router, not an interview |

The mechanism is a persistent unknowns ledger (`id · quadrant · cost-if-wrong · P(wrong) ·
regret · status · phase`). Each round targets the highest-regret open item with a single
question, re-scores it, and does not permit implementation while any quadrant is un-probed or
any open item carries `regret ≥ 1.0`. The full schema and kick-off prompt are in
[`SKILL.md`](skills/finding-unknowns/SKILL.md).

When the host exposes Claude Code's **Workflow tool** (dynamic workflows) and the user has
opted into orchestration, the three fan-out-heavy operations run as deterministic scripts —
multi-lens sweep with per-finding adversarial verification (pipelined, no barrier), a
three-lens refutation panel for cost ≥ 4 resolutions, and a UU probe loop that stops only
after two consecutive dry rounds. Templates and the graceful fallback ladder live in
[`references/workflows.md`](skills/finding-unknowns/references/workflows.md).

## Relationship to other tools

`finding-unknowns` operates at a different altitude from heavier workflow skills. It is a
lightweight orienting layer, not an execution engine.

| Property     | finding-unknowns          | Deep Interview ([OMC](https://github.com/Yeachan-Heo/oh-my-claudecode)) | OMC execution (autopilot / ralph / team) | [Superpowers](https://github.com/obra/superpowers) |
|--------------|---------------------------|-------------------------|------------------------|------------------------|
| Altitude     | Meta / orienting          | One phase: requirements | Execution & delivery   | Discipline primitives  |
| Lifecycle    | Pre · During · Post       | Pre only                | During · Post          | Mostly single-phase    |
| Rigor        | Flexible                  | Ambiguity gating        | Verification-gated     | Checklist-driven        |
| State        | Stateless                 | Persisted, resumable    | Persisted, multi-agent | Varies                 |
| Best when    | You do not yet know your unknowns | You need a validated specification | The specification is clear | You need one disciplined move |

These tools are complementary rather than competing. The recommended pattern is to use
`finding-unknowns` to locate an unknown, then escalate to the appropriate specialist:

```
finding-unknowns  (orient: which quadrant is this unknown in?)
        ├─ a light reframe is sufficient          → the eight techniques
        ├─ high-stakes, want a coverage gate       → Cartographer mode (this skill)
        ├─ want ambiguity gating + resumable state → OMC Deep Interview
        ├─ divergent option generation             → superpowers:brainstorming
        ├─ a rigorous written plan                 → superpowers:writing-plans / omc-plan
        └─ the specification is already concrete    → OMC autopilot / ralph / team
```

## Project structure

```
finding-unknowns-skill/
├── .claude-plugin/         Plugin and marketplace manifests (/plugin install)
├── commands/               Slash-command entry points (thin dispatchers)
│   ├── finding-unknowns.md   /finding-unknowns — Phase 0 routing
│   ├── blindspot.md          /blindspot — blind-spot pass
│   ├── cartographer.md       /cartographer — Cartographer mode
│   └── change-quiz.md        /change-quiz — report + merge quiz
├── skills/
│   └── finding-unknowns/
│       ├── SKILL.md        The protocol: routing, eight techniques, Cartographer mode
│       └── references/
│           └── workflows.md  Workflow-orchestration templates (multi-lens sweep, verify panel, UU loop)
├── agents/
│   ├── blindspot-scout.md  Read-only reconnaissance (sonnet)
│   ├── prototype-smith.md  Divergent throwaway prototyping (sonnet)
│   ├── ledger-keeper.md    Regret scoring and coverage-gate verdicts (opus)
│   └── quiz-master.md      Independent examiner (sonnet)
├── docs/
│   └── ARCHITECTURE.md     Design reference: layers, contracts, principles
├── assets/                 README diagrams (SVG)
├── AGENTS.md               Repository guide for coding agents and contributors
├── EXAMPLES.md             Copy-paste, end-to-end prompts
├── CLAUDE.md               Passive single-file drop-in
├── install.sh              Installer (skill + agents + commands)
├── CONTRIBUTING.md         Contribution guidelines
├── CHANGELOG.md            Release history
├── LICENSE                 MIT
└── README.md
```

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Acknowledgements

- The ideas and technique names originate from Thariq Shihipar's essay _"A Field Guide to
  Fable: Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)).
- The Cartographer mode comparison references the Deep Interview skill from
  [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) and the primitives in
  [Superpowers](https://github.com/obra/superpowers).

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Disclaimer

This is an independent community project. It is not affiliated with, authorised by, or endorsed
by Anthropic.
