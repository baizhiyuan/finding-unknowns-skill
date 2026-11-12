# Repository guide for coding agents

This file orients AI coding agents (and human contributors) working **on** this repository.
It is about maintaining the project. For what the plugin does at runtime, read
`skills/finding-unknowns/SKILL.md` and its references; for why it is built this way, read
[`docs/design/5.0.md`](docs/design/5.0.md) and the 5.2 re-architecture it led to; the `fu`
script's contract is [`docs/design/fu-cli.md`](docs/design/fu-cli.md).

## Layout and single-source-of-truth rules

| Path | Role | Rule |
|------|------|------|
| `docs/design/5.0.md` | The design | The reasons and the evaluation plan. A behavioural change that contradicts it needs a design change first. |
| `skills/finding-unknowns/SKILL.md` | The only skill | Holds the card, the three operations, the four stop-points and the rules that must always be loaded. At most 700 words. Everything else goes in a reference. |
| `skills/finding-unknowns/references/*.md` | Per-phase detail | `card.md` (normative card schema and lint rules) · `brief.md` (questions, predictions, contract; ≤ 350 words) · `debrief.md` (grading, field rules, reply; ≤ 450) · `results.md` (Theory → Measured → Consistent? → Mechanism; ≤ 1,200) · `view.md` (HTML view offer; ≤ 150). Normative for their topic. On conflict, fix whichever contradicts the design. |
| `commands/*.md` | `/fu-brief`, `/fu-catch-up`, `/fu-debrief`, `/fu-view` | Thin: invoke the skill with the Skill tool and name the operation; together at most 450 words. Exception: `/fu-brief` holds the card's fill-in template (not counted). Never name a command after a skill or a Claude Code built-in (`/brief`, `/status` and `/resume` collide). |
| `agents/mechanism-auditor.md` | The one agent | Read-only grader, at most 500 words; used for irreversible-lane cards, measured results, or on request; never given the builder's claims. |
| `scripts/fu.py` | The `fu` script (5.2 phase 2) | Stdlib only. Everything deterministic: lint, freeze, integrity, log, list, render, guard. Built to `docs/design/fu-cli.md`. |
| `CLAUDE.next.md` | Candidate always-on text | 82 words. Replaces `CLAUDE.md` only after the Tier 1 check passes. |
| `docs/evals/`, `docs/field-notes/` | Evidence and field notes | Protected: do not rewrite results or notes after the fact. |
| `docs/ARCHITECTURE.md`, `docs/GLOSSARY.md` | Reference | Update when a part, a file or a term changes. |
| `docs/TUTORIAL.md` / `docs/TUTORIAL.zh.md` | 5-minute tutorial | One illustrative card; keep both in step with the commands and with each other. |
| `CLAUDE.md` | Always-on text | The 56 measured words (Stage 0). Frozen; changes go through `CLAUDE.next.md`. |
| `EXAMPLES.md` | Copy-paste prompts | Keep consistent with SKILL.md. Keep the `#a-real-blind-spot-pass-recorded` anchor; `docs/recordings/` links to it. |
| `README.md` / `README.zh.md` | Landing pages | English is canonical. The Chinese README must match it heading for heading (`##` and `###`); update both together. |
| `assets/zh/src/*.svg` | Chinese diagram sources | Edit here, then outline the glyphs: `python3 scripts/outline_cjk.py --fonts /path/to/noto-sans-sc --out assets/zh assets/zh/src/*.svg`. Never hand-edit `assets/zh/*.svg`. |

## Protected rules

These came from 4.x and must keep a home in 5.0 (design §9). Do not weaken or drop them:

- The irreversibility floor, the three lanes and the build rule: exact command, one run,
  dry-run contract checks (SKILL.md body; `references/card.md`).
- The contract: a check must be able to fail; "does NOT prove"; checks locked against the
  implementer (SKILL.md short form; `references/brief.md` full form).
- Never ask what the territory can answer (SKILL.md body).
- Questions: one batch, only what only the person can decide, each with a recommended
  answer; the prediction ask without one; never author the person's prediction
  (`references/brief.md`).
- The evidence-first Debrief and surrender signals (`references/debrief.md`).
- theory-vs-result in full: verdicts, mechanism tiers, Chinese labels, the mismatch walk,
  the Debug path, the threshold gate, the two-verdict rule (`references/results.md`).
- Credits: Thariq Shihipar, Addy Osmani, the author's research practice.

## Invariants to preserve

- **Word budgets** (checked by `scripts/validate.py`): SKILL.md 700, and the budgets in
  the table above. New detail goes in a reference loaded by the phase that needs it, or
  into the `fu` script.
- **No protocol narration.** Nothing tells the person a mode, level or route.
- **Few interruptions.** No mode question (ship by default), no questions about committing
  the person's code; once the build starts, every turn ends with a completion report or a
  stop-point request; the completion report is the Debrief; recall questions only on
  request; the Debrief ends without a menu.
- **One name, one thing.** "Card" means the task card; runtime text says "person", not
  "user".
- **The token rule.** Spend words on the card, delta lines, raw evidence and explanation
  at the point of error. Do not add score tables, a rule stated three times, or text that
  loads on trivial tasks.
- **Evidence-honest claims.** The value to people is untested; say so. Claim nothing beyond
  the design and the evals. A pattern found after the fact is a `post-hoc fit`, not a
  finding.
- **Never commit raw eval logs** (for example the `events.jsonl` run logs).
- YAML frontmatter values containing `:` must be quoted.
- Every step stays runnable without extras: without the agent, grading is labelled
  `same-context — weaker`; without the `fu` script, Timing is `self-reported` and
  integrity `not run`.
- "Lane" means reversibility only: `reversible` · `wide` · `irreversible`.
- Every file the plugin writes goes under `.finding-unknowns/`; `.gitignore` is never
  edited.
- No em dash `——` in the Chinese README or tutorial (the validator rejects it).
- Preserve the attribution (Thariq Shihipar / @trq212; Addy Osmani) and the
  non-affiliation disclaimer in SKILL.md, README.md and README.zh.md (`CLAUDE.md` holds only
  the measured words). Neutral credit only.

Removed from 5.x and kept on branch `v4` (the classic line, bug fixes only): structured
mode, Cartographer, the ledger, regret, clarity scores, the six-condition gate, the
numbered techniques, the full handoff packet, and the `blindspot-scout`, `ledger-keeper`,
`prototype-smith` and `quiz-master` agents. Removed in 5.0 and not to be reintroduced
without a design change: Workflow execution, the must-pass quiz, and the separate
keep-the-reasoning and theory-vs-result skills. 4.x is at tag `v4.3.2`.

## After any change

1. Validate (CI runs the same on every push to `main` and every pull request):
   ```bash
   python3 scripts/validate.py   # frontmatter, JSON, SVG safety, links, fences, en/zh
                                 # README parity, em dashes in zh docs,
                                 # version/count drift, install.sh
   ```
2. Bump `version` in `.claude-plugin/plugin.json` (SemVer) and add a `CHANGELOG.md` entry.
3. Use Conventional Commits (`feat:`, `fix:`, `docs:`, …).
