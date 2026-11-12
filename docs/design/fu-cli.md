# `fu` CLI contract (5.2)

Phase 1 (the prose layer) calls these commands; `scripts/fu.py` implements this contract.
The normative card format is [`references/card.md`](../../skills/finding-unknowns/references/card.md);
the design source is [`5.2.md`](5.2.md) (§4 enforcement, §7 views and schema, §8 Tier 0).
Tier 0 tests: `python3 -m unittest discover -s tests` (run in CI).

## Location and invocation

- One stdlib-only Python file, `scripts/fu.py` at the plugin root (Python ≥ 3.8, no
  third-party imports, no network). Its second line starts with `# finding-unknowns:`;
  the agent and command files carry `#finding-unknowns:plugin-file` on frontmatter line 2.
  `install.sh` treats a file as its own only with that marker in the first three lines:
  anything else of the same name is moved to `{file}.bak.{timestamp}`, never overwritten
  or deleted; earlier versions without the marker are left in place (a separately
  installed `keep-the-reasoning` or `theory-vs-result` skill is never touched); a symlink
  at a destination is removed, never written through.
- **From the skill and commands** the invocation is always
  `python3 "{base}/../../scripts/fu.py" <subcommand> …`, where `{base}` is the skill's base
  directory that Claude Code prints when the skill loads. SKILL.md defines this once as
  `fu`. It holds in both install layouts:
  - plugin: `{plugin root}/skills/finding-unknowns` → `{plugin root}/scripts/fu.py`;
  - `install.sh`: `$CLAUDE_CONFIG_DIR/skills/finding-unknowns` →
    `$CLAUDE_CONFIG_DIR/scripts/fu.py` (`install.sh` copies it there).
- **From hooks**: `hooks/hooks.json` runs
  `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/fu.py" guard pre|post 2>/dev/null || python … 2>/dev/null || true`
  (so a system with only `python`, e.g. native Windows, works and nothing is printed to
  stderr) on `PreToolUse` (`pre`), `PostToolUse` and `PostToolUseFailure` (`post`), matcher
  `Bash`, timeout 10 s (a timed-out PreToolUse hook does not block the call).
- Optional: `bin/fu`, a two-line wrapper
  (`exec python3 "$(dirname "$(readlink -f "$0")")/../scripts/fu.py" "$@"`, so a symlink on
  `PATH` works) for people who want it on `PATH`. The skill never relies on it.
- If the script cannot start (no `python3`, file missing), the skill says so in one line
  and degrades: Timing `self-reported`, integrity `not run`, no lint, no log.

## Common behaviour

- **Project root**: `--root DIR` if given (before or after the subcommand); else the
  nearest ancestor of the working directory containing `.finding-unknowns/`; else the git
  top level; else the working directory. All paths below are relative to
  `{root}/.finding-unknowns/`.
- **Card argument**: a slug (`tasks/{slug}.md`, or `predictions/{slug}.md` when only a
  claim file exists) or a path to either. `lint`, `integrity`, `log` and `render` accept no
  slug: they take the most recently modified open card, and when several cards are open
  the first output line is `card: {slug} (most recently modified open card)`. `freeze`
  always needs a slug.
- **Open card**: State is not `debriefed` (guard, list and catch-up all use this).
- **Output**: plain text, no colour, one finding per line, nested lists with fixed keys
  where there is structure; nothing is printed that the model must reformat to show.
- **Exit codes** (all subcommands except `guard`, which always exits 0 and never writes to
  stderr):
  - `0` success (lint: no FAIL; warnings allowed);
  - `1` the check ran and found problems (lint FAIL, integrity finding, unparsable Debrief);
  - `2` usage error, card or root not found;
  - `3` skipped by design (freeze could not commit, integrity could not run); the reason
    is printed.
- Never edits `.gitignore`, never runs `git push`, never stages anything outside the paths
  it commits. Git runs with `GIT_TERMINAL_PROMPT=0`, stdin closed, a 120 s timeout (a
  signing prompt fails instead of hanging; `git commit` gets 15 min because it runs the person's
  hooks; git runs in its own process group and the whole group is killed on timeout), and `-c core.fsmonitor=false`, so no fsmonitor
  command runs; `git diff` adds `--no-ext-diff --no-textconv`. The person's commit hooks
  still run (never `--no-verify`); a failing hook makes freeze exit 3 and self-report. A commit killed on timeout may leave
  `.git/index.lock` and staged card files; the self-report says `.git/index.lock may remain;
  remove it if no git process is running`. Formatters in commit hooks (lint-staged/prettier
  on `*.md`) may rewrite the card's indentation; `fu lint` after the freeze reports it.
  (Other repo-local config, e.g. `gpg.program` or clean filters on `git add`, still
  applies; hooks and config are not transferred by `git clone`.)
- **Writes** go through one helper: the target must lie inside `.finding-unknowns/`; no
  symlink is allowed on the target or any directory from `.finding-unknowns/` itself down
  (dangling or not; missing directories are created one level at a time); the resolved
  parent must stay inside `.finding-unknowns/`; appends open with `O_NOFOLLOW`; whole-file
  writes go to a fresh temp file (`O_EXCL|O_NOFOLLOW`) moved over the target with
  `os.replace`. A refused write is `fu {cmd}: refusing to write through a symlink: {path}`,
  exit 2 (the guard drops that side effect silently).

## Files

| Path under `.finding-unknowns/` | Written by | Git |
|---|---|---|
| `tasks/{slug}.md` | model; State, Timing and the Brief heading by `fu freeze` (State also by `fu guard post`) | committed by `fu freeze` |
| `tasks/{slug}.deltas.md` | model (append-only); created by `fu freeze --stage brief` | committed |
| `predictions/{slug}.md` | model (claim file, `results.md`); its `Timing:` line by `fu freeze` | committed |
| `decisions.md`, `decisions-archive.md` | model (`decisions.md` ≤ 30 lines; older lines move to the archive) | committed when changed |
| `profile.md` | model, `fu init` or `fu freeze --stage brief` | local |
| `predictions-log.md` | `fu log` only | local |
| `logs/approvals.jsonl`, `logs/guard.jsonl` | `fu guard` | local |
| `view/{slug}.html`, `view/index.html` | `fu render` | local |

`profile.md` keys, one `key: value` per line: `mode: ship|learn` (default `ship`),
`strict: no|yes` (default `no`), `view: yes|no` (absent until offered), `commits: yes|no`
(default `yes`), `guard: off|log|ask` (default `ask` when `hooks/hooks.json` sits beside
the script's directory, i.e. the plugin install; `off` for an `install.sh` copy, which has
no hook; the hooks file must contain `fu.py" guard pre`, so another tool's `hooks.json` does
not count). Unknown keys are ignored.

## Subcommands

### `fu init [--strict] [--guard off|log|ask]`

Creates `tasks/`, `predictions/`, `logs/`, `view/` and `profile.md` (existing keys are
kept; flags overwrite theirs; missing keys get their defaults). Idempotent. Only when it
creates `profile.md` (the first time in a repository) does it print `add to .gitignore:`
and the gitignore lines from `card.md` that `.gitignore` does not already contain; the
model shows them once, in the Brief-approval ask. `fu freeze --stage brief` runs the same
step first. Exit 0.

### `fu lint [slug] [--strict]`

Checks the card, its deltas file (if it exists; lint before the first freeze does not need
it), `decisions.md` and the claim file `predictions/{slug}.md` (with or without a card)
against `card.md`. Strict caps apply with `--strict` or `strict: yes`.

```
FAIL tasks/{slug}.md:{line} {rule}: {message}
WARN tasks/{slug}.deltas.md:{line} {rule}: {message}
lint: {n} FAIL, {m} WARN
```

Rule IDs (stable; the renderer shows WARN as chips):

| ID | Level | Rule |
|---|---|---|
| `header` | FAIL | five header lines in order with their closed values; `Needs you` reads `{X} (recommendation: {Y}; settles {Z})` or `nothing`; slug matches the file name |
| `sections` | FAIL | sections exactly `## Brief (draft)` or `## Brief (frozen {time})`, `## Amendments`, `## Deltas`, `## Model changes`, `## Open`, in that order, then `## Debrief (…)` sections only at the end (absent until the Debrief: not a FAIL) |
| `placeholder` | FAIL | a template placeholder is left: in prose `{…}`, `{a \| b}` or `{lowercase words}`; inside code spans only the template's command placeholders (`{exact command}`, `{command that can fail}`, `{command}`), since code may use braces. The unfilled template fails; the filled template passes |
| `needs-you-once` | FAIL | exactly one `Needs you:` line, on header line 3 |
| `brief-form` | FAIL | `Approach:` alone, then `  - {decision} because {why}` (at least one); `Stop-points: irreversible · scope · dead-premise · budget > …`; ``Irreversible: `{command}` `` one per line (also allowed directly under a dated `M{n}` Amendment, same form; an `Irreversible:` line anywhere else outside the Brief FAILs); `Check files: {paths} \| none`; no other line in the Brief |
| `id-reserved` | FAIL in the Brief, WARN elsewhere | a single-digit `P{n}`/`A{n}` cited in the card or deltas file (outside code spans, and not inside a prediction line's quoted claim, Brief or Debrief) is a defined Brief prediction; `P10` and longer are not read as IDs. FAIL always: P belongs to `you`, A to `agent`; no ID defined twice |
| `prediction-form` | FAIL | `{ID} ({you\|agent} · {confidence}) "{claim}"` then `  - falsifier:` and `  - should not change:`; a `P` claim is one double-quoted string whose inner quotes are written `\"` (an unescaped inner quote fails); `A` may be unquoted; no answer is exactly `P: none given`; not both |
| `confidence` | FAIL | person `low · medium · high · no idea · not given`; agent `low · medium · high` |
| `contract-form` | FAIL | `C{n} {claim}` with `check`, `does NOT prove`, `lane` (`reversible \| wide \| irreversible`), in that order; an irreversible item adds `post-check`; at least one item; an irreversible lane and an `Irreversible:` line come together; no tables |
| `irreversible-check` | FAIL | a segment of a `check:` or `post-check:` (its code spans, else its text) equals an `Irreversible:` command under the guard's normalisation (below: wrappers and redirections dropped, `sh -c`/`eval`/substitutions followed). A dry-run variant with extra flags is not a FAIL (the guard exempts it when it is the card's own check) |
| `delta-location` | FAIL | no `D{n} ` delta line in the card |
| `delta-form` | FAIL | deltas-file line `D{n} {date} {HH:MM} {deviation\|surprise\|decided-for-you}: {text} → {evidence path}[ · cost if wrong: …][ [stop: irreversible\|scope\|dead-premise\|budget]]`; `cost if wrong` required on `decided-for-you`; IDs unique; an optional first `#` header line |
| `delta-time` | WARN | delta without `HH:MM` |
| `rollup` | FAIL | the card's `## Deltas` holds `Latest: D{n} \| none`, `Rollup:`, then at most three lines |
| `amend-anchor` | WARN | amendment without `after D{n}` |
| `amend-form` | WARN | amendment not in the form `M{n} {time} · after D{n} · {decided-for-you\|confirmed}: {what} · why: {why}` |
| `decisions-form` | WARN | a `decisions.md` line (not blank, not `#`) not in the form `{YYYY-MM-DD} "{their words}" → {what it settles}` |
| `model-changes` | FAIL | `## Model changes` lines read `- You expected X → it is Y, because Z [shown, not confirmed \| confirmed]`, at most five |
| `model-changes-place` | WARN | a `You expected … →` line or Model changes heading outside its section |
| `live-length` | WARN (FAIL strict) | header to Open > 40 non-blank lines, a frozen Brief's lines not counted |
| `debrief-form` | FAIL | heading `## Debrief ({time}; graded by fresh context \| same-context — weaker)`; blocks `Evidence:` (≥ 1 bullet), prediction rows, `Integrity:` (exactly the three `fu integrity` lines), `Did NOT prove:` (each `{check} → leaves open: {…} · still holds: {…}`), `Not checked:`, `Bottom line:`, in that order; nothing else |
| `debrief-coverage` | FAIL | every Brief prediction graded once, ID line identical to the Brief, P before A, with `measured`, `consistent?`, `mechanism` in order; with `P: none given` there is no P row (a `P: none given` line may stand in its place) |
| `verdict` | FAIL | `consistent?` in `consistent · partly · inconsistent · can't tell · post-hoc fit` (`post-hoc fit (not a test)` accepted); mechanism ends with `[verified\|supported\|inferred\|untested]` |
| `not-checked` | FAIL | `Not checked` has at least one item |
| `bottom-line` | FAIL | `holds`, `did not hold`, `stops at` in order; every graded ID appears exactly once across them: `consistent` under `holds`, `partly`/`inconsistent` under `did not hold`, `can't tell`/`post-hoc fit` under `stops at`; no ungraded ID |
| `verb-tier` | WARN | below `verified`, a strong verb (causes, proves, confirms, demonstrates, guarantees, establishes, due to, results in, leads to, drives); an `untested` mechanism not opening with `untested:` |
| `superlative` | WARN | "all", "every", "works", "no regressions" under `holds` while a row is not `consistent` |
| `decisions-length` | WARN | `decisions.md` > 30 lines |
| `strict-caps` | FAIL strict | ≤ 900 words (a CJK character counts as a word) in the live part plus the last Debrief only, not counting the person's quoted claims and code spans (sized for a card at the item caps with ~10-word fields); ≤ 3 agent predictions (more than 3 person predictions: WARN); ≤ 5 contract items; ≤ 20 words per field (last Debrief only), not counting code spans and exempting quoted `P{n}` claims and `Irreversible:` lines |
| `claim-form` | FAIL | claim file: `Claim under test`, `Person prediction` (pre-5.2 label `Your prediction` accepted), `Agent prediction`, `Falsifier`, `Written` lines; `Person prediction` is `"{their words}"` with optional ` ({confidence})`, or `none given`; a `Timing:` line, if present, in the card's Timing form |

A Debrief section is linted only if present. Lint never edits files. A FAIL line number
of `1` means the whole file.

### `fu freeze <slug> --stage brief|stop|resume|debrief [--needs TEXT]`

`fu freeze` owns `State`, `Timing` and the frozen Brief heading. `--needs` (only with
`--stage stop`; it must read `{X} (recommendation: {Y}; settles {Z})`, else exit 2 before
any write) replaces the header's `Needs you`; `--stage resume` sets it to `nothing`. At
`brief`, `fu init`'s step runs first (and prints the gitignore lines if it created
`profile.md`).

1. Card edits first, before any skip check, so they happen even when the commit is
   skipped: at `brief`, replace `## Brief (draft)` with `## Brief (frozen {YYYY-MM-DD HH:MM})`
   and create the deltas file with a one-line `# {slug} deltas (append-only)` header if
   missing. Every stage sets State: `brief` → `building`, `stop` → `waiting on you`,
   `resume` → `building`, `debrief` → `debriefed` (from any State).
2. Paths: the card, its deltas file if present, `predictions/{slug}.md` if present,
   `decisions.md` if changed (with `decisions-archive.md` if that changed too). A claim
   file without a card: the claim file plus the decisions files; step 1 does not apply.
3. Skip checks, before anything is staged: `commits: no`; not a git repository; merge,
   rebase, cherry-pick or revert in progress; detached HEAD; a path ignored; other paths
   already staged. Any hit: no commit; at `brief`, `Timing: self-reported`; print
   `self-reported: {reason}`; exit 3.
4. `git add -- <paths>` then `git commit --only -m "chore(card): {stage} {slug}" -- <paths>`.
   A failing commit hook or signing prompt: `git reset -q -- <paths>`, at `brief` Timing
   `self-reported`, print `self-reported: commit failed ({last error line})`, exit 3.
5. At `brief`, after the commit: write `Timing: Brief frozen {time}, commit {short hash}`
   (left uncommitted until the next freeze). For a claim file the line replaces its
   `Timing:` line, else goes after `Written`, else at the end. Print
   `committed {short hash} ({stage} {slug})`; exit 0.

### `fu integrity [slug]`

Needs a card with a `Timing: … commit {hash}` header (a claim file alone: exit 2). Prints
exactly three lines:

```
Brief vs freeze: unchanged | edited: lines {a-b}, …
Check files: unchanged | changed: {paths}[ · created after the freeze: {paths}] | created after the freeze: {paths} | none named
Unlogged hunks: none | {path}:{start}-{end}, …
```

- Brief: the `## Brief` block in the working tree vs `git show {hash}:{card}`; line numbers
  are working-tree lines.
- Check files: `git diff --name-only {hash} -- {Check files paths}`; a named path absent
  from the freeze commit (`git cat-file -e {hash}:{path}` fails) that exists now, or an
  untracked file under one, is `created after the freeze`.
- Hunks: `git diff -U0 {hash}` plus untracked files (whole file; line count read only for
  regular files up to 5 MB, else `1-1`), excluding `.finding-unknowns/`. A hunk is logged
  when its path or file name equals a path token (`[\w./-]+`, `:line` and trailing dots
  dropped) in the deltas file, an Amendment, the Approach or the contract; a substring is
  not a match. This is a mechanical approximation; the Debrief lists what it prints.
- `self-reported`, `draft` or no commit: each line reads `not run (timing: {value})`;
  exit 3. Git failing or the commit unreadable: `not run ({reason})`; exit 3. Any
  finding: exit 1. Clean: exit 0.

### `fu log [slug]`

Parses the last Debrief section and appends one line per graded prediction to
`predictions-log.md`:
`{YYYY-MM-DD} · {slug} · {ID} · {you|agent} · {consistent?} · {confidence}` (date of the
Debrief heading). `P: none given` adds no line. A line is appended only when it differs
from the latest line for the same slug and ID, so re-running the same Debrief appends
nothing (`log: nothing new for {slug}`) and a re-grade appends its changes; statistics use
the latest line per slug and ID. Prints the appended lines, then, when a side has n ≥ 5
graded predictions (excluding `can't tell` and `post-hoc fit`; held = `consistent`):

```
You: {k} of {n} held · Agent: {k} of {n} held{ · the agent held every one: its predictions are likely too safe — when the agent, n ≥ 5, held all}
```

No Debrief, or a FAIL in `debrief-form`, `debrief-coverage`, `verdict`, `not-checked`,
`bottom-line` or `id-reserved`: lint output, exit 1.

### `fu list [--all]`

Open cards by default; `--all` adds the rest. Newest first (file modification time):

```
{slug} · {state}
  - needs you: {text | nothing}
  - last seen: {after D{n} | never} · unseen deltas: {k}
  - graded: you {k} of {n} held · agent {k} of {n} held | not yet
```

`unseen deltas` counts `D{n}` lines in the deltas file above the `Last seen … after D{n}`
number (all of them when `never`). `graded` uses the card's last Debrief with the stat
line's rule (n excludes `can't tell` and `post-hoc fit`). Then the calibration stat line
from `predictions-log.md` when a side has n ≥ 5. Exit 0; no `.finding-unknowns/`: exit 2.

### `fu render [slug] | --list`

- `view/{slug}.html`: direction A. `Needs you` first; where the evidence stops (Bottom
  line `stops at` / `holds` / `did not hold`, then `Did NOT prove` and `Not checked`; before
  a Debrief, each contract item's `does NOT prove`); a one-row strip of Brief freeze,
  deltas, amendments (after their anchor), recorded irreversible runs from
  `logs/approvals.jsonl` (placed by time) and the last-seen marker, the irreversible step
  marked; verdict tally and one row per prediction (person filled ID badge, agent hollow);
  Brief, deltas, Model changes, Open, Evidence and Integrity folded below. Headings carry
  counts computed from the verdicts.
- `view/index.html`: one item per card (need-you first, then newest), state, `Needs you`,
  last seen, verdict marks (colour = verdict; filled = person, hollow = agent, dashed =
  not graded); a calibration block from `predictions-log.md`: the stat line always (any
  n); a curve (share held per stated confidence, person and agent on one axis, k/n
  printed) only at ≥ 10 graded predictions with a `low|medium|high` confidence. The caption
  defines n and says predictions on one card are not independent.
- Fixed templates, inline CSS, light/dark via `prefers-color-scheme`, CJK font stack,
  print styles; no script, no external resource; a CSP meta tag
  (`default-src 'none'; style-src 'unsafe-inline'; img-src data:`). The index links a card
  as `./` + URL-quoted `{slug}.html`, escaped. Every card string is HTML-escaped;
  backtick spans become `<code>` around escaped text; nothing else passes through.
- Lint first. A FAIL inside a frozen Brief, or a whole-card `strict-caps` or `live-length`
  FAIL (line 1), does not block: the page shows a banner listing those FAILs (the Brief is
  reported, never edited). Any other FAIL: print the lint
  output and `render: lint FAIL outside the frozen Brief; fix the card, nothing written`,
  write nothing, exit 1. Prints the written path; exit 0.

### `fu guard pre|post` (hook entry)

Reads the Claude Code hook JSON on stdin (`tool_name`, `tool_input.command`, `cwd`,
`hook_event_name`). Always exits 0, never writes to stderr, prints nothing but an `ask`
decision; any error, malformed input, bad arguments, a non-`Bash` tool, no
`.finding-unknowns/` above `cwd`, no card or no match prints nothing. Never returns `deny`.

- **Advisory.** The guard asks; it never denies and fails open. Hard enforcement is a
  Claude Code `permissions.ask` rule for the exact command in user or managed settings,
  which the agent cannot edit.
- **Per-card isolation.** Collects ``Irreversible: `…` `` commands from open cards (Brief or Amendments; adding one mid-build is a scope stop-point the person confirms); a card
  that cannot be read (invalid UTF-8 is replaced, a dangling symlink or unreadable file is
  skipped) does not stop the others. The prior-run lookup and each log write fail on their
  own without changing the decision.
- **Matching** (first 8192 characters). A command is split into segments on newlines, `;`,
  `&&`, `||`, `|`, `&`, `(`, `)`, `$(`, backticks; redirections (`2>&1`, `> out.log`,
  `<<EOF`) and their targets are dropped; the bodies of `sh|bash|zsh|dash|ksh -c "…"`,
  `eval …`, `$( … )` and backticks become segments of their own (three levels deep).
  Each segment is normalised: leading `VAR=value`, shell keywords (`!`, `{`, `then`, `do`,
  …), and wrappers with their options (`env`, `timeout {duration}`, `nohup`, `sudo`,
  `doas`, `time`, `command`, `exec`, `nice`, `stdbuf`, `xargs`) are dropped; the program
  becomes its base name; `python3`/`python3.N` becomes `python` and an interpreter path
  (`/usr/bin/python3`) its name anywhere in the segment; a leading `./` is removed from every
  token; interpreter options between the interpreter and its script (`-u`, `-X val`, `-W val`,
  `--`) are dropped; `npm|pnpm|yarn run-script` becomes `run`; `uv|poetry|pipenv run` before an
  interpreter is dropped.
  - **Exact**: a segment equals the `Irreversible:` command.
  - **Variant**: the command's tokens, or for a known runner (`python -m X`,
    `npm|pnpm|yarn|bun run X`, `uv|poetry|pipenv run X`, `npm|pnpm exec X`,
    `cargo|go|deno run X`, `bundle exec X`, or a runner followed by an interpreter) its
    runner plus target, appear as a contiguous run anywhere in a segment. An extra ask is
    cheap; a miss is not. So `python -m pytest` never matches `python -m pkg.publish`, and
    `python publish.py --dry-run …` does not match `python publish.py build/quotes.json`.
  - **The card's own checks.** A variant segment equal to a segment of that card's
    `check:` or `post-check:` code span (a dry run) neither asks nor is recorded.
  - A compound `Irreversible:` line (several segments) matches when its segments appear
    in order.
  - **Known gap**: a command passed to another host, e.g. `ssh host 'python publish.py …'`, is
    not read; the guard sees only `ssh`.
- **pre**, on a match with `guard: ask`, prints

  ```json
  {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
    "permissionDecisionReason": "card {slug}: irreversible step `{command}` · .finding-unknowns/tasks/{slug}.md"}}
  ```

  (`variant of the irreversible step` for a variant). Slug and command are shown with
  control and bidi characters replaced, the command cut to 120 characters. If
  `logs/approvals.jsonl` already holds this normalised command's hash, or an exact run of
  the same `Irreversible:` line, for this card, the reason is
  `card {slug}: `{command}` already ran once at {time}[ and failed (it may have partly run)]; a post-check must not re-execute it · {card path}`.
  With `guard: log` the match is appended to `logs/guard.jsonl` as
  `{"time", "slug", "sha256", "would": "ask"}` and nothing is printed.
- **post** (`PostToolUse`, and `PostToolUseFailure` for a run that failed), on a match:
  appends `{"sha256": sha256(normalised command), "line_sha256": …, "exact": …, "time": …,
  "slug": …}` (plus `"failed": true` from `PostToolUseFailure`) to `logs/approvals.jsonl`,
  and moves that card from `waiting on you` to `building` with `Needs you: nothing`. A
  failed, possibly partial run therefore still warns on a retry.
- Generic destructive patterns, checked by tokens over the same segments (`rm` with
  recursive and force flags, `git … push` with `-f`/`--force*`/`+ref`, `git … reset
  --hard`) and a linear regex for `DROP TABLE|DATABASE|SCHEMA|INDEX|VIEW`: appended to
  `logs/guard.jsonl` as `{"time", "pattern", "sha256"}` only (never the command text);
  they ask only under `strict: yes` with `guard: ask`.
- `guard: off` does nothing.
- **The prompt is the yes.** With `guard: ask` and a working native prompt, the person's
  answer to the permission prompt is the per-command yes for a card-named irreversible
  command; the prompt shows the exact command and the reason (with a `[plugin:…]` source
  label). No separate chat yes is needed.
- **Hosts and modes** (Claude Code hooks reference, checked 2026-11-12): `ask` "prompts the
  user to confirm" and the reason is shown in the prompt; in a `-p` run where no one can
  answer, Claude Code denies the call and Claude reads the reason in the tool result. Under
  `auto` mode an `ask` normally goes to the prompt. The reference says nothing about `ask`
  under `bypassPermissions`; that, and one live run, remain to verify before release. If
  `ask` cannot surface there, the fallback (deny with a message telling the agent to stop
  and show the command) is a design change to record here. Tier 0 replays recorded
  hook JSON through `guard pre|post`.
