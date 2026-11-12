# Repository guide for coding agents

This file orients AI coding agents (and human contributors) working **on** this repository.
It is about maintaining the project — for what the skill does at runtime, read
`skills/finding-unknowns/SKILL.md`, `skills/keep-the-reasoning/SKILL.md`, and
`skills/theory-vs-result/SKILL.md`.

## Layout and single-source-of-truth rules

| Path | Role | Rule |
|------|------|------|
| `skills/finding-unknowns/SKILL.md` | The protocol (before/during work) | The ONLY place procedure lives for this skill, except Cartographer (next row). All behavioural changes happen here first. |
| `skills/finding-unknowns/references/cartographer.md` | Full Cartographer protocol | Normative for Cartographer. `SKILL.md` holds only its summary. |
| `skills/finding-unknowns/references/workflows.md` | Workflow templates | Dynamic-workflow scripts; keep consistent with the Cartographer reference. |
| `skills/keep-the-reasoning/SKILL.md` | The handoff protocol | Single source of truth for that skill; invoked directly as `/keep-the-reasoning` (no command file). |
| `skills/theory-vs-result/SKILL.md` | The measured-result protocol | Single source of truth for that skill; invoked directly as `/theory-vs-result` (no command file). `agents/mechanism-auditor.md` is its read-only fresh-context audit. |
| `commands/*.md` | Slash-command dispatchers (`/blindspot`, `/cartographer`, `/change-quiz`) | Thin: invoke the skill with the Skill tool, name a section, and pass `$ARGUMENTS`. Never restate procedure or hard-code a SKILL.md path. Never name a command after a skill: the skills already answer to `/finding-unknowns`, `/keep-the-reasoning`, `/theory-vs-result`, and a same-named command shadows the skill. |
| `agents/*.md` | Specialist subagents | Each declares tools, model tier, and an I/O contract. Keep read-only agents read-only. |
| `docs/ARCHITECTURE.md` | Design reference | Update when layers/contracts change. |
| `docs/GLOSSARY.md` | Shared vocabulary | Where the three skills' terms meet. Update when a term is added, renamed, or changes meaning; each SKILL.md still defines what it uses. |
| `docs/TUTORIAL.md` / `docs/TUTORIAL.zh.md` | 5-minute tutorial | Keep both in step with the commands, packet sizes, rigor levels, and EXAMPLES.md's recorded run. |
| `CLAUDE.md` | Passive drop-in | The 82-word text promoted after the Tier 1 regression check (`docs/evals/2026-11-12-tier1/`), byte-identical to the text tested there. It replaced the 56 words measured in Stage 0. Frozen: any change needs a new pre-registered check. |
| `EXAMPLES.md` | User-facing prompts | Keep consistent with the SKILL.md files after edits. |
| `README.md` / `README.zh.md` | Landing pages | zh is a faithful translation of the English structure; update both together. |

## Invariants to preserve

- YAML frontmatter values containing `:` must be quoted (a colon in an unquoted
  description has broken parsing before).
- `blindspot-scout`, `quiz-master`, and `mechanism-auditor` stay read-only (no Write/Edit in `tools:`).
- `prototype-smith` writes throwaway files only; `ledger-keeper` touches only the ledger.
- The Cartographer summary in `finding-unknowns/SKILL.md` and `references/cartographer.md`
  must stay consistent; on conflict the reference is correct, so fix the summary.
- Every technique must remain runnable inline — no hard dependency on agents or commands.
- One vocabulary (see `docs/GLOSSARY.md`): "lane" means reversibility only; use *rigor level*
  (`theory-vs-result`), *packet size* (`keep-the-reasoning`), *mode* (lightweight vs
  Cartographer), and *prior* for any expectation recorded before a result.
- Every file the skills write goes under `.finding-unknowns/` at the project root; the
  ledger's first line is `schema: 2`. Root-level legacy files are read and a move offered,
  never moved silently.
- Preserve the attribution block (Thariq Shihipar / @trq212) and the non-affiliation
  disclaimer in SKILL.md and README.md (the frozen `CLAUDE.md` carries neither). Credit
  sources as in each SKILL.md `metadata.credits` (Osmani for `keep-the-reasoning` and the verification contract;
  Anthropic and @hanakoxbt for the execution heuristics; the author's own
  empirical research practice for `theory-vs-result`); neutral credit only.

## After any change

1. Validate (the same two commands run in CI on every push to `main` and every pull request):
   ```bash
   python3 scripts/validate.py      # frontmatter, JSON, SVG safety, links, fences, en/zh
                                    # README parity, em dashes in zh docs,
                                    # version/count drift, install.sh
   node tests/workflows/run.mjs     # Workflow templates, extracted from workflows.md
   ```
   When you change a Workflow template, add a scenario to `tests/workflows/run.mjs` that
   fails on the old code and passes on the new.
2. Bump `version` in `.claude-plugin/plugin.json` (SemVer) and add a `CHANGELOG.md` entry.
3. Use Conventional Commits (`feat:`, `fix:`, `docs:`, …).
