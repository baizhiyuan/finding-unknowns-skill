# Repository guide for coding agents

This file orients AI coding agents (and human contributors) working **on** this repository.
For what the skill does at runtime, read `CLAUDE.md` and `skills/finding-unknowns/SKILL.md`.

## What ships in 6.0

Three things and no machinery: an always-on text, one skill, two thin commands. No agents,
installed scripts, hooks, HTML or files written by the skill (except on "save"). `install.sh`
is the only script, and the look-back runs one inline filter.
The design and its owner decisions are in `docs/design/6.0.md`.

| Path | Role | Rule |
|------|------|------|
| `CLAUDE.md` | The always-on text | At most 140 words (CI checks). It is quoted verbatim in both READMEs; change all three together. Any change in meaning is a behaviour change: say so in the CHANGELOG and note that it is unmeasured |
| `skills/finding-unknowns/SKILL.md` | Templates, interview, look-back with the inline transcript filter | The only place procedure lives. At most 1,150 words (CI checks). The filter is tested as written (`tests/test_lookback_filter.py`) |
| `commands/fu-interview.md`, `commands/fu-lookback.md` | Opt-in entry points | Thin: name the skill section and pass `$ARGUMENTS`. Never restate procedure. Never name a command after the skill |
| `install.sh` | Installer | Installs the 6.0 files; retires 4.x files only when they carry this project's marker; backs up anything else before replacing it; never edits `CLAUDE.md` outside its marker comments. Tested by `tests/test_install.py` in temporary config directories |
| `README.md` / `README.zh.md` | Landing pages | Same heading structure (CI checks). The Chinese templates must match `SKILL.md`'s Chinese labels and `docs/GLOSSARY.md` |
| `docs/GLOSSARY.md` | Terms, English and Chinese | Update when a field, header or verdict is added or renamed |
| `docs/design/` | Design history | `6.0.md` is the accepted design. Do not rewrite history files |
| `docs/evals/` | Evaluation reports and plans | Never edit a report's results after the fact; add a dated erratum instead |

## Invariants to preserve

- The header tokens `fu:before`, `fu:after`, `fu:interview`, `fu:lookback` and the note prefix
  `fu-note:` stay literal in every language. The look-back filter depends on them.
- The person's expectation is quoted, never written for them.
- `Not proved` and `Still unknown` are never both empty; nothing follows `fu:after`.
- The look-back never reads a transcript whole, and only reads transcripts when asked.
- The README's evidence section says that the 6.0 always-on text was tested only in wording
  tests with a simulated user, that the shipped text's own test did not confirm it (REPORT:
  safeguard notices in 3 of 24 runs, limit 1) and the owner adopted it regardless, that its
  changes relative to the 82 words are unmeasured, and that nobody has measured learning or
  understanding, until a check says otherwise.
- YAML frontmatter values containing `:` must be quoted.
- Preserve the attribution (Thariq Shihipar / @trq212; Addy Osmani) and the non-affiliation
  disclaimer in both READMEs. Neutral credit only.

## After any change

1. Validate (the same commands run in CI on every push to `main` and every pull request):
   ```bash
   python3 scripts/validate.py              # word budgets, frontmatter, file set, JSON, SVG
                                            # safety, links, fences, en/zh README parity,
                                            # em dashes in zh, version drift, install.sh syntax
   python3 -m unittest discover -s tests    # install.sh and the look-back filter
   ```
2. Bump `version` in `.claude-plugin/plugin.json` (SemVer) and add a `CHANGELOG.md` entry.
3. Use Conventional Commits (`feat:`, `fix:`, `docs:`, …).
