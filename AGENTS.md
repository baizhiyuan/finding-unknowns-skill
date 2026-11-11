# Repository guide for coding agents

This file orients AI coding agents (and human contributors) working **on** this repository.
It is about maintaining the project. For what the plugin does at runtime, read
`skills/finding-unknowns/SKILL.md` and its references; for why it is built this way, read
[`docs/design/5.0.md`](docs/design/5.0.md).

## Layout and single-source-of-truth rules

| Path | Role | Rule |
|------|------|------|
| `docs/design/5.0.md` | The design | The reasons and the evaluation plan. A behavioural change that contradicts it needs a design change first. |
| `skills/finding-unknowns/SKILL.md` | The only skill | Holds the card, the three operations, the four stop-points and the rules that must always be loaded. At most 1,500 words. Everything else goes in a reference. |
| `skills/finding-unknowns/references/*.md` | Per-phase detail | `card.md` (template, files, commits, prediction log) · `brief.md` (discovery instruments, contract) · `debrief.md` (grading, evidence block, recall) · `results.md` (Theory → Measured → Consistent? → Mechanism) · `results-examples.md` · structured mode, loaded only on request: `structured.md` (quadrant routing, eight techniques) · `cartographer.md` · `handoff-full.md`. Normative for their topic; the SKILL.md body holds only the short form. On conflict, fix whichever contradicts the design. |
| `commands/*.md` | `/fu-brief` (`--structured`), `/fu-catch-up`, `/fu-debrief`, `/fu-cartographer` | Thin: invoke the skill with the Skill tool and name the operation. Never restate procedure or hard-code a SKILL.md path. Never name a command after a skill or a Claude Code built-in (`/brief`, `/status` and `/resume` collide). |
| `agents/*.md` | `blindspot-scout`, `mechanism-auditor`, `quiz-master`; structured mode: `ledger-keeper`, `prototype-smith` | Each declares tools, model tier and an I/O contract. The first three are read-only; `ledger-keeper` writes only the ledger, and `prototype-smith` writes only throwaway files under `.finding-unknowns/prototypes/`. |
| `extras/session-start-hook/` | Unshipped hook | Stays outside the plugin's `hooks/` until the Stage 0 hook sub-arm supports it (design §8). |
| `docs/evals/`, `docs/field-notes/` | Evidence and field notes | Protected: do not rewrite results or notes after the fact. |
| `docs/ARCHITECTURE.md`, `docs/GLOSSARY.md` | Reference | Update when a part, a file or a term changes. |
| `docs/TUTORIAL.md` / `docs/TUTORIAL.zh.md` | 5-minute tutorial | One illustrative card; keep both in step with the commands and with each other. |
| `CLAUDE.md` | Passive drop-in | The habits without the plugin; keep consistent with SKILL.md. |
| `EXAMPLES.md` | Copy-paste prompts | Keep consistent with SKILL.md. Keep the `#a-real-blind-spot-pass-recorded` anchor; `docs/recordings/` links to it. |
| `README.md` / `README.zh.md` | Landing pages | English is canonical. The Chinese README must match it heading for heading (`##` and `###`); update both together. |
| `assets/zh/src/*.svg` | Chinese diagram sources | Edit here, then outline the glyphs: `python3 scripts/outline_cjk.py --fonts /path/to/noto-sans-sc --out assets/zh assets/zh/src/*.svg`. Never hand-edit `assets/zh/*.svg`. |

## Protected rules

These came from 4.x and must keep a home in 5.0 (design §9). Do not weaken or drop them:

- The irreversibility floor, the three lanes and the build rule (SKILL.md body).
- The contract: a check must be able to fail; the "does NOT prove" column; checks locked
  against the implementer (SKILL.md short form; `references/brief.md` full form).
- Never ask what the territory can answer; absence claims cite the hit or the empty
  search; remote targets cite the recorded access path; late priors are recorded before
  checks (SKILL.md body).
- Interview rules: up to three independent questions per round, architecture first,
  dependent questions one at a time (`references/brief.md`).
- The compact evidence packet, surrender signals and the prediction habit
  (`references/debrief.md`).
- theory-vs-result in full: verdicts, mechanism tiers, Chinese labels, the mismatch walk,
  the Debug path, the threshold gate, the two-verdict rule (`references/results.md`).
- Credits: Thariq Shihipar, Addy Osmani, the author's research practice.

## Invariants to preserve

- **SKILL.md stays at or under 1,500 words.** New detail goes in a reference loaded by the
  phase that needs it.
- **No protocol narration in the default flow.** Nothing tells the person a mode, level,
  route or packet size ("Routing:", "Rigor level:", "Depth:"); quadrants are internal
  vocabulary. Structured mode, on request, announces Routing, Depth and Packet size.
- **Few interruptions (v5.1).** No mode question (ship by default), no questions about
  committing the person's code; once the build starts, every turn ends with a completion
  report or a stop-point request; recall questions only in learn mode; the Debrief ends
  without a menu.
- **The token rule.** Spend words on the card, delta lines, raw evidence and explanation
  at the point of error. Do not add score tables, a rule stated three times, or text that
  loads on trivial tasks.
- **Evidence-honest claims.** The value to people is untested; say so. Claim nothing beyond
  the design and the evals. A pattern found after the fact is a `post-hoc fit`, not a
  finding.
- **Never commit raw eval logs** (for example the `events.jsonl` run logs).
- YAML frontmatter values containing `:` must be quoted.
- Every step stays runnable inline: agents are optional, and without them grading is
  labelled `same-context — weaker`.
- "Lane" means reversibility only: `reversible` · `wide` · `irreversible`.
- Every file the plugin writes goes under `.finding-unknowns/`. 4.x files are read in
  place and a fold-in is offered, never moved silently; `.gitignore` is never edited
  silently.
- No em dash `——` in the Chinese README or tutorial (the validator rejects it).
- Preserve the attribution (Thariq Shihipar / @trq212; Addy Osmani) and the
  non-affiliation disclaimer in SKILL.md, README.md, README.zh.md and CLAUDE.md. Neutral
  credit only.

Opt-in only, never in the default flow: Cartographer, the ledger, regret, clarity
scores, the six-condition gate, the numbered techniques and the full handoff packet
(structured mode). Removed in 5.0 and not to be reintroduced without a design change:
Workflow execution, the must-pass quiz (structured mode's quiz is optional and graded
inline), and the separate keep-the-reasoning and theory-vs-result skills. 4.x is at tag
`v4.3.2`.

## After any change

1. Validate (CI runs the same on every push to `main` and every pull request):
   ```bash
   python3 scripts/validate.py   # frontmatter, JSON, SVG safety, links, fences, en/zh
                                 # README parity, em dashes in zh docs,
                                 # version/count drift, install.sh
   ```
2. Bump `version` in `.claude-plugin/plugin.json` (SemVer) and add a `CHANGELOG.md` entry.
3. Use Conventional Commits (`feat:`, `fix:`, `docs:`, …).
