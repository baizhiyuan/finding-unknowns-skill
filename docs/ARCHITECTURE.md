# Architecture

This document describes the design of the finding-unknowns framework: its components, the
contracts between them, and the principles that decide where a responsibility lives. The
README is the landing page; this is the reference.

## Components

```
commands/            Entry points (slash commands) — thin dispatchers, no logic
skills/
  finding-unknowns/  The protocol — routing, techniques, Cartographer mode, guardrails
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

Keeping commands thin means the protocol has exactly one source of truth: `SKILL.md`.
A command never restates procedure; it names the section to execute.

### Layer 2 — The skill (protocol)

`SKILL.md` is written as an executable protocol, not a description. Its structure:

- **Contract**: `Purpose`, `Use_When`, `Do_Not_Use_When`, `Why_This_Exists` — when to
  fire and when to route elsewhere.
- **Execution_Policy**: the non-negotiables (explore before asking; one question at a
  time; discovery ends at understanding).
- **Steps**: Phase 0 (blocking quadrant routing) → Phases 1–3 (eight techniques, each a
  When / Procedure / Stop-when / Guardrails block) → Phase C (Cartographer mode).
- **Templates**: exact per-round report and question formats, so output is reproducible
  rather than improvised.
- **Examples**: Good/Bad pairs with rationale — the strongest behavioural steering.
- **Escalation_And_Stop_Conditions** and a two-lane **Final_Checklist**.

### Layer 3 — Agents (specialists)

Each agent exists because it has an execution profile the main conversation cannot match.
The governing principle: **discovery, scoring, and examination must not be performed by
the same context that implements.**

| Agent | Model | Tools | Why isolated |
|-------|-------|-------|--------------|
| `blindspot-scout` | sonnet | read-only | Wide recon in its own context window; structurally cannot drift into implementing |
| `prototype-smith` | sonnet | writes throwaway files only | Diverges into N directions in one pass; sandboxed away from the real application |
| `ledger-keeper` | opus | ledger file only | Scoring and gate verdicts need consistency and independence — a bookkeeper that did not conduct the interview will not inflate its verdict |
| `quiz-master` | sonnet | read-only + report | An examiner that did not author the diff probes what the author glosses over |

Model tiers follow the cost/judgment routing used by mature skill frameworks: the one
agent whose output is a *verdict* (regret scores, gate pass/fail) gets the strongest
model; recon, prototyping, and examination are standard-tier work.

Every agent declares an explicit I/O contract (inputs it needs, artifact it returns) in
its frontmatter description and body. The skill relays agent reports; it does not re-run
their exploration.

## Data artifacts

| Artifact | Producer | Consumer | Lifetime |
|----------|----------|----------|----------|
| `unknowns-ledger.md` | ledger-keeper (or skill inline) | interview loop, gate, quiz | whole task; IS the resume state |
| `implementation-notes.md` | build phase | quiz-master, next attempt | one build |
| `prototypes/*.html` | prototype-smith | user reaction | throwaway |
| `change-report.html` | quiz-master | merge decision | one review |

Resume semantics: Cartographer sessions resume by re-reading the ledger — no separate
state store, no re-seeding.

## Design principles

1. **One source of truth.** Procedure lives only in `SKILL.md`; commands dispatch,
   agents execute their contract, docs explain.
2. **Separation of judgment.** The verdict-giving roles (gate, quiz grade) belong to
   contexts that did not produce the work being judged.
3. **Graceful degradation.** Every technique works inline with no agents and no
   commands installed; each layer is an enhancement, not a dependency.
4. **Coverage over confidence.** Cartographer gates on whether the four quadrants were
   probed — clarity on the questions you thought to ask is not coverage of the ones you
   did not.
5. **Regret-priced attention.** Questions are spent where cost-if-wrong × P(wrong) is
   high; everything else gets a logged conservative default.

## Relationship to upstream paradigms

- Technique content derives from Thariq Shihipar's essay (see README attribution).
- The protocol format (contract sections, phased steps, templates, Good/Bad examples,
  stop conditions, checklists) follows the skill paradigm of
  [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode); the layered
  command → skill → agent architecture and model-tier routing likewise. This project
  intentionally does not adopt OMC's runtime machinery (state stores, hooks, settings
  resolution) — the file-based ledger provides resumability without a framework
  dependency.
