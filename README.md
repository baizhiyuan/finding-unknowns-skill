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

> **The map is not the territory.**
> The quality of long-horizon work isn't bottlenecked by the model anymore — it's
> bottlenecked by your ability to clarify your *unknowns*.

> 📎 **Source.** This skill distills the essay _"The map is not the territory"_ by
> **Thariq ([@trq212](https://x.com/trq212/status/2073100352921215386))**. All credit for
> the underlying ideas and technique names goes to the original post; this repo just
> packages them as an installable, reusable Claude Code skill.

* * *

## 💡 What this skill does

`finding-unknowns` is a toolbox for **discovering your unknowns cheaply — before they get
expensive to fix.** The **map** is what you give Claude (prompt, context, skills). The
**territory** is where the work actually happens (the codebase, the real world). The gap
between them is unknowns, and every unknown forces Claude to guess what you want.

This skill gives Claude _eight concrete techniques_ to surface those unknowns **before,
during, and after** implementation — so you spend cheap words up front instead of expensive
rework later.

<p align="center">
  <img src="assets/lifecycle.svg" alt="Three windows to catch unknowns: pre, during, post" width="92%">
</p>

* * *

## ✨ Key features

- 🧭 **Four-quadrant framing** — locate whether your gap is a _known unknown_ or an _unknown unknown_ before you act.
- 🔦 **Blind-spot pass** — Claude teaches you the gaps you didn't know you had, tuned to who you are.
- 🎨 **Brainstorm & prototype** — react to N wildly different HTML directions before anything gets wired up.
- 🎤 **Interview me** — one question at a time, prioritizing answers that change the architecture.
- 📎 **References** — point Claude at source code as the richest possible spec, even across languages.
- 📋 **Implementation plan** — leads with the decisions you're most likely to tweak, buries the mechanical parts.
- 📝 **Implementation notes** — logs deviations mid-build so you learn from each attempt.
- 🎓 **Pitch & quiz** — a buy-in doc for reviewers, and a quiz you must pass before you merge.

* * *

## 🧭 The four quadrants

Before acting, locate where your unknowns live — the quadrant tells you which technique to reach for.

<p align="center">
  <img src="assets/quadrants.svg" alt="The four quadrants of unknowns" width="78%">
</p>

> Every explainer, brainstorm, interview, prototype, and reference is a cheap way to find
> out what you didn't know — before it gets expensive to fix.

* * *

## 🚀 Quickstart

**Option A — one-line install (clone + run):**

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill
bash install.sh              # copies SKILL.md into ~/.claude/skills/finding-unknowns/
```

**Option B — manual copy:**

```bash
mkdir -p ~/.claude/skills/finding-unknowns
cp skills/finding-unknowns/SKILL.md ~/.claude/skills/finding-unknowns/
```

Then, at the start of any ambiguous task, **invoke it via the Skill tool**:

```
finding-unknowns
```

Or just say a trigger phrase — _"do a blindspot pass"_, _"interview me"_, _"brainstorm 4 directions"_.

* * *

## 🧩 The eight techniques

| Phase | Technique | For |
|-------|-----------|-----|
| Pre | 🔦 Blind-spot pass | Unknown unknowns in a new domain / codebase |
| Pre | 🎨 Brainstorm & prototype | Unknown knowns — "I'll know it when I see it" |
| Pre | 🎤 Interview me | Residual ambiguity after brainstorming |
| Pre | 📎 References | When you can't describe it — point at code |
| Pre | 📋 Implementation plan | Surface the risky decisions early |
| During | 📝 Implementation notes | Edge cases that force a deviation |
| Post | 🎓 Pitch & explainer | Buy-in and approvals |
| Post | ✅ Quiz | Understand the change before you merge |

Full copy-paste prompts for each live inside [`skills/finding-unknowns/SKILL.md`](skills/finding-unknowns/SKILL.md).

* * *

## 🔗 How it relates to Deep Interview, OMC, and other skills

`finding-unknowns` deliberately operates at a **different altitude** from the heavier
workflow skills. It is a lightweight *orienting layer*, not an execution engine. Here's the
honest comparison so you know when to reach for which.

### At a glance

| | **finding-unknowns** | **Deep Interview** (OMC) | **OMC execution** (autopilot / ralph / team) | **Superpowers** (brainstorming, writing-plans, TDD…) |
|---|---|---|---|---|
| **Altitude** | Meta / orienting | One deep phase: requirements | Execution & delivery | Discipline primitives |
| **Lifecycle** | Pre · During · Post | Pre only | During · Post | Mostly single-phase |
| **Rigor** | Flexible, human-taste | Mathematical ambiguity gating | Verification-gated | Rigid, checklist-driven |
| **State / persistence** | None (stateless) | Persisted, resumable | Persisted, multi-agent | Varies |
| **Output** | HTML/MD artifacts you react to | A gated spec (`.omc/specs/…`) | Shipped code + tests | Plans, tests, fixes |
| **Best when** | You don't yet know your unknowns | You have a vague idea and need a bulletproof spec | The spec is clear; go build | You need one disciplined move |

### Strengths & weaknesses

- **finding-unknowns** — 🟢 broad, cheap, covers the *whole* lifecycle, great for taste/design work and for the moment you realize "I don't even know what to ask." 🔴 no rigor, no gating, no state — it won't *stop* you from proceeding while still confused.
- **Deep Interview** — 🟢 unmatched depth on *one* thing: turning a fuzzy idea into a mathematically-validated spec, with topology/ontology tracking and a hard "don't proceed until ambiguity ≤ threshold" gate, then a clean handoff to execution. 🔴 heavyweight, pre-implementation only, single-track (Socratic Q&A) — overkill for a quick reframe, and silent on the *during*/*post* windows.
- **OMC execution (autopilot/ralph/team)** — 🟢 actually delivers: parallel agents, verification loops, persistence. 🔴 assumes you already know what to build — feed it a vague goal and it confidently builds the wrong thing.
- **Superpowers primitives** — 🟢 sharp, composable, battle-tested single moves (brainstorm, write-plan, TDD, debug). 🔴 each is one tool; none owns the "am I even solving the right problem?" question end-to-end.

### Should you merge them? — Recommendation

**No — don't fuse them into one mega-skill. Compose them instead.** They're complementary
layers, not competitors, and merging would fight the "small, high-cohesion skills with
distinct triggers" principle. The sweet spot is to treat **finding-unknowns as the
front-door / dispatcher** that (1) helps you locate your unknown on the quadrant, then
(2) hands off to the specialist when a technique needs depth:

```
finding-unknowns  (orient: which quadrant is my unknown in?)
        │
        ├─ needs a bulletproof, gated spec?      → Deep Interview
        ├─ needs divergent option generation?    → superpowers:brainstorming
        ├─ needs a rigorous written plan?        → superpowers:writing-plans / omc-plan
        ├─ spec is clear, time to build?         → OMC autopilot / ralph / team
        └─ light reframe is enough?              → stay in finding-unknowns
```

Rules of thumb:

- **Reach for finding-unknowns first** when the task is fuzzy, unfamiliar, or taste-driven — it's the cheapest way to discover *that you're confused* and *where*.
- **Escalate to Deep Interview** when the stakes justify a gated, resumable spec and you want math to tell you when you're actually ready.
- **Skip straight to OMC execution** when the spec is already concrete (file paths, acceptance criteria).
- **Use Superpowers primitives** inside any of the above whenever you need one disciplined move.

> **TL;DR** — finding-unknowns is the *compass*; Deep Interview is the *deep drill*; OMC is
> the *factory*. Keep the compass in your pocket, and let it point you at the right heavy
> tool. A future version of this skill may add explicit `Skill()` hand-off hooks to make
> that routing automatic.

* * *

## 📁 Project structure

```
finding-unknowns-skill/
├── skills/
│   └── finding-unknowns/
│       └── SKILL.md        # the skill itself — frontmatter + 8 techniques
├── assets/                 # README SVGs (hero, quadrants, lifecycle)
├── install.sh              # copies the skill into ~/.claude/skills/
├── LICENSE                 # MIT
└── README.md               # you are here
```

* * *

## 🙌 Acknowledgements

Ideas, framing, and technique names come from **Thariq
([@trq212](https://x.com/trq212/status/2073100352921215386))**'s essay _"The map is not the
territory."_ This repo packages those ideas as an installable Claude Code skill and adds the
comparison to Deep Interview / OMC / Superpowers.

* * *

## 📄 License

MIT — see [LICENSE](LICENSE). Contributions and updates welcome; this skill will keep evolving.
