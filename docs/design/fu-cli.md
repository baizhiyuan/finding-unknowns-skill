# `fu` CLI contract (5.2)

Phase 1 (the prose layer) calls these commands; phase 2 builds the script to this contract.
The normative card format is [`references/card.md`](../../skills/finding-unknowns/references/card.md);
the design is round 2 of the 5.x review (Fable, 2026-11-11), §4 and §7.

## Location and invocation

- One stdlib-only Python file, `scripts/fu.py` at the plugin root (Python ≥ 3.8, no
  third-party imports, no network).
- **From the skill and commands** the invocation is always
  `python3 "{base}/../../scripts/fu.py" <subcommand> …`, where `{base}` is the skill's base
  directory that Claude Code prints when the skill loads. SKILL.md defines this once as
  `fu`. It holds in both install layouts:
  - plugin: `{plugin root}/skills/finding-unknowns` → `{plugin root}/scripts/fu.py`;
  - `install.sh`: `$CLAUDE_CONFIG_DIR/skills/finding-unknowns` →
    `$CLAUDE_CONFIG_DIR/scripts/fu.py` (`install.sh` copies it there once it exists).
- **From hooks**: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fu.py" guard pre|post`
  (`CLAUDE_PLUGIN_ROOT` is set for plugin hooks).
- Optional: `bin/fu`, a two-line wrapper (`exec python3 "$(dirname "$0")/../scripts/fu.py" "$@"`)
  for people who want it on `PATH`. The skill never relies on it.
- If the script cannot start (no `python3`, file missing), the skill says so in one line
  and degrades: Timing `self-reported`, integrity `not run`, no lint, no log.

## Common behaviour

- **Project root**: `--root DIR` if given; else the nearest ancestor of the working
  directory containing `.finding-unknowns/`; else the git top level; else the working
  directory. All paths below are relative to `{root}/.finding-unknowns/`.
- **Card argument**: a slug (`tasks/{slug}.md`) or a path to the card. Several open cards
  and no slug, where a subcommand allows that: the most recently modified open card
  (State not `debriefed`); the first output line says which.
- **Output**: plain text, no colour, one finding per line, nested lists with fixed keys
  where there is structure; nothing is printed that the model must reformat to show.
- **Exit codes** (all subcommands):
  - `0` success (lint: no FAIL; warnings allowed);
  - `1` the check ran and found problems (lint FAIL, integrity finding, unparsable Debrief);
  - `2` usage error, card or root not found;
  - `3` skipped by design (freeze could not commit, integrity could not run); the reason
    is printed.
- Never edits `.gitignore`, never runs `git push`, never uses `--no-verify`, never stages
  anything outside the paths it commits.

## Files

| Path under `.finding-unknowns/` | Written by | Git |
|---|---|---|
| `tasks/{slug}.md` | model (Timing line and Brief heading time: `fu freeze`) | committed by `fu freeze` |
| `tasks/{slug}.deltas.md` | model (append-only); created by `fu freeze --stage brief` | committed |
| `predictions/{slug}.md` | model (claim file, `results.md`) | committed |
| `decisions.md` | model (≤ 30 lines) | committed when changed |
| `profile.md` | model or `fu init` | local |
| `predictions-log.md` | `fu log` only | local |
| `logs/approvals.jsonl`, `logs/guard.jsonl` | `fu guard` | local |
| `view/{slug}.html`, `view/index.html` | `fu render` | local |

`profile.md` keys, one `key: value` per line: `mode: ship|learn` (default `ship`),
`strict: no|yes` (default `no`), `view: yes|no` (absent until offered), `commits: yes|no`
(default `yes`), `guard: off|log|ask` (default `ask`). Unknown keys are ignored.

## Subcommands

### `fu init [--strict] [--guard off|log|ask]`

Creates the directory tree and `profile.md` (existing keys are kept; flags overwrite
theirs). Prints the four gitignore lines from `card.md` if `.gitignore` does not already
contain them. Exit 0.

### `fu lint <slug> [--strict]`

Checks the card, its deltas file and `decisions.md` against `card.md`. Strict caps apply
with `--strict` or `strict: yes`.

```
FAIL tasks/{slug}.md:{line} {rule}: {message}
WARN tasks/{slug}.deltas.md:{line} {rule}: {message}
lint: {n} FAIL, {m} WARN
```

Rule IDs (stable; the renderer shows WARN as chips):

| ID | Level | Rule |
|---|---|---|
| `header` | FAIL | five header lines, order, closed values |
| `needs-you-once` | FAIL | exactly one `Needs you:` line, in the header |
| `id-reserved` | FAIL | `P{n}`/`A{n}` cited anywhere are defined Brief predictions; P belongs to `you`, A to `agent` |
| `prediction-form` | FAIL | one form; `P` claims quoted; or exactly `P: none given`; falsifier and should-not-change present |
| `confidence` | FAIL | `low · medium · high · no idea · not given` |
| `delta-location` | FAIL | no `D{n}` delta line in the card |
| `delta-form` | FAIL | delta kind closed; `cost if wrong` on `decided-for-you` |
| `delta-time` | WARN | delta without `HH:MM` |
| `contract-form` | FAIL | `C{n}` with check, does NOT prove, lane; irreversible lane has post-check |
| `irreversible-check` | FAIL | a contract check contains a command from an `Irreversible:` line |
| `amend-anchor` | WARN | amendment without `after D{n}` |
| `model-changes-place` | WARN | a Model changes block outside its section |
| `live-length` | WARN (FAIL strict) | header to Open > 40 lines |
| `debrief-coverage` | FAIL | every Brief prediction graded, ID line identical, P before A |
| `verdict` | FAIL | `consistent?` closed set; mechanism ends with a tier |
| `not-checked` | FAIL | `Not checked` has at least one item |
| `bottom-line` | FAIL | three keys; IDs under `holds` are consistent; every partly/inconsistent ID under `did not hold` |
| `verb-tier` | WARN | mechanism verb stronger than its tier (word list) |
| `superlative` | WARN | "all", "every", "works", "no regressions" under `holds` while a row missed |
| `decisions-length` | WARN | `decisions.md` > 30 lines |
| `strict-caps` | FAIL strict | card ≤ 600 words; ≤ 3 predictions per side; ≤ 5 contract items; ≤ 20 words per field |

A Debrief section is linted only if present. Lint never edits files.

### `fu freeze <slug> --stage brief|stop|debrief`

1. Skip checks, before anything is staged: not a git repository; a path ignored; merge,
   rebase or cherry-pick in progress, or detached HEAD; other changes already staged;
   `commits: no`. Any hit: no commit; at `brief`, set `Timing: self-reported`; print
   `self-reported: {reason}`; exit 3.
2. At `brief` only, before committing: replace `## Brief (draft)` with
   `## Brief (frozen {YYYY-MM-DD HH:MM})`; set `State: building`; create the deltas file
   with a one-line header if missing.
3. Paths: the card, its deltas file, `predictions/{slug}.md` if present, `decisions.md` if
   changed. `git add -- <paths> && git commit --only -m "chore(card): {stage} {slug}" -- <paths>`.
4. A failing commit hook or signing prompt: `git reset -q -- <paths>`, Timing
   `self-reported`, exit 3.
5. At `brief`, after the commit: write `Timing: Brief frozen {time}, commit {short hash}`
   into the header (left uncommitted until the next freeze). Print
   `committed {short hash} ({stage} {slug})`; exit 0.

### `fu integrity <slug>`

Needs a `Timing: … commit {hash}` header. Prints exactly three lines:

```
Brief vs freeze: unchanged | edited: lines {a-b}, …
Check files: unchanged | changed: {paths} | none named
Unlogged hunks: none | {path}:{start}-{end}, …
```

- Brief: the `## Brief` block in the working tree vs `git show {hash}:{card}`.
- Check files: `git diff --quiet {hash} -- {Check files paths}`.
- Hunks: `git diff {hash}` plus untracked files, excluding `.finding-unknowns/`. A hunk is
  logged when its path appears in a delta, an Amendment, the Approach or the contract.
  This is a mechanical approximation; the Debrief lists what it prints.
- `self-reported` or no commit: the three lines read `not run (timing: self-reported)`;
  exit 3. Any finding: exit 1. Clean: exit 0.

### `fu log <slug>`

Parses the last Debrief section and appends one line per graded prediction to
`predictions-log.md`:
`{YYYY-MM-DD} · {slug} · {ID} · {you|agent} · {consistent?} · {confidence}`.
Idempotent for the same Debrief time; a re-grade appends new lines and statistics use the
latest line per slug and ID. Prints the appended lines, then, when a side has n ≥ 5
graded predictions (excluding `can't tell` and `post-hoc fit`; held = `consistent`):

```
You: {k} of {n} held · Agent: {k} of {n} held{ (too soft?) when the agent held all}
```

Unparsable Debrief: lint output, exit 1.

### `fu list [--all]`

Open cards by default (State not `debriefed`); `--all` adds the rest. Newest first:

```
{slug} · {state}
  - needs you: {text | nothing}
  - last seen: {after D{n} | never} · unseen deltas: {k}
  - graded: you {k} of {n} held · agent {k} of {n} held | not yet
```

Then the calibration stat line from `fu log` when available. Exit 0.

### `fu render <slug> | --list`

Writes `view/{slug}.html` (direction A: decision first, where the evidence stops, then a
one-row delta strip with the irreversible step marked) or `view/index.html` (task list,
calibration stat line; a curve only at ≥ 10 graded predictions with a confidence; the
caption says predictions on one card are not independent). Fixed templates, everything
escaped, no raw HTML passthrough, no external resources. Headings are computed from the
verdict counts. Any lint FAIL: print the lint output, write nothing, exit 1. Prints the
written path; exit 0.

### `fu guard pre|post` (hook entry)

Reads the Claude Code hook JSON on stdin (PreToolUse / PostToolUse, tool `Bash`).

- Collects `Irreversible:` commands from cards whose State is not `debriefed`.
- **pre**: a command equal after whitespace normalisation, or matching the first two
  tokens, returns `permissionDecision: "ask"` with the reason
  `card {slug}: irreversible step`; if `logs/approvals.jsonl` already holds its hash, the
  reason is `already ran once at {time}; a post-check must not re-execute it`.
- **post**: appends `{"sha256": …, "time": …, "slug": …}` to `logs/approvals.jsonl`.
- Generic destructive patterns (`rm -rf`, force-push, `DROP`, `reset --hard`): appended to
  `logs/guard.jsonl` as "would have asked"; they ask only under `strict: yes`.
- `guard: off` does nothing; `guard: log` only records.
- Fails open: any error, no card or no match prints nothing and exits 0. Never returns
  `deny`.
- To verify before release: replay recorded tool-call JSON; one live run; behaviour of
  `ask` under `claude -p` and bypass-permissions mode. If `ask` cannot surface there, the
  fallback (deny with a message telling the agent to stop and show the command) is a
  design change to record here.
