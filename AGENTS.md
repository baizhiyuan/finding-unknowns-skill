# Repository guide for coding agents

This file orients AI coding agents (and human contributors) working **on** this repository.
It is about maintaining the project — for what the skill does at runtime, read
`skills/finding-unknowns/SKILL.md` and `skills/keep-the-reasoning/SKILL.md`.

## Layout and single-source-of-truth rules

| Path | Role | Rule |
|------|------|------|
| `skills/finding-unknowns/SKILL.md` | The protocol (before/during work) | The ONLY place procedure lives for this skill, except Cartographer (next row). All behavioural changes happen here first. |
| `skills/finding-unknowns/references/cartographer.md` | Full Cartographer protocol | Normative for Cartographer. `SKILL.md` holds only its summary. |
| `skills/finding-unknowns/references/workflows.md` | Workflow templates | Dynamic-workflow scripts; keep consistent with the Cartographer reference. |
| `skills/keep-the-reasoning/SKILL.md` | The handoff protocol | Single source of truth for that skill; `commands/keep-the-reasoning.md` only dispatches to it. |
| `commands/*.md` | Slash-command dispatchers | Thin: name a SKILL.md section and pass `$ARGUMENTS`. Never restate procedure. |
| `agents/*.md` | Specialist subagents | Each declares tools, model tier, and an I/O contract. Keep read-only agents read-only. |
| `docs/ARCHITECTURE.md` | Design reference | Update when layers/contracts change. |
| `CLAUDE.md` | Passive drop-in | A lightweight summary of the skill; keep consistent with the SKILL.md files after edits. |
| `EXAMPLES.md` | User-facing prompts | Keep consistent with the SKILL.md files after edits. |
| `README.md` / `README.zh.md` | Landing pages | zh is a faithful translation of the English structure; update both together. |

## Invariants to preserve

- YAML frontmatter values containing `:` must be quoted (a colon in an unquoted
  description has broken parsing before).
- `blindspot-scout` and `quiz-master` stay read-only (no Write/Edit in `tools:`).
- `prototype-smith` writes throwaway files only; `ledger-keeper` touches only the ledger.
- The Cartographer summary in `finding-unknowns/SKILL.md` and `references/cartographer.md`
  must stay consistent; on conflict the reference is correct, so fix the summary.
- Every technique must remain runnable inline — no hard dependency on agents or commands.
- Preserve the attribution block (Thariq Shihipar / @trq212) and the non-affiliation
  disclaimer in SKILL.md, README.md, and CLAUDE.md. Credit sources as in each SKILL.md
  `metadata.credits` (Osmani for `keep-the-reasoning` and the verification contract;
  Anthropic and @hanakoxbt for the execution heuristics); neutral credit only.

## After any change

1. Validate:
   ```bash
   python3 -c "import yaml,glob; [yaml.safe_load(open(p).read().split('---',2)[1]) for p in glob.glob('skills/*/SKILL.md')+glob.glob('agents/*.md')+glob.glob('commands/*.md')]"
   python3 -c "import json; json.load(open('.claude-plugin/plugin.json')); json.load(open('.claude-plugin/marketplace.json'))"
   for f in assets/*.svg assets/zh/*.svg assets/zh/src/*.svg; do python3 -c "import xml.dom.minidom; xml.dom.minidom.parse('$f')"; done
   bash -n install.sh
   ```
2. Bump `version` in `.claude-plugin/plugin.json` (SemVer) and add a `CHANGELOG.md` entry.
3. Use Conventional Commits (`feat:`, `fix:`, `docs:`, …).
