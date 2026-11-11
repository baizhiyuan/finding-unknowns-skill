# Eval v3: a plugin hook vs the manual CLAUDE.md nudge (Sonnet; pre-registered)

Written 2026-11-11 before any v3 run. Not edited after runs start; corrections go
under "Amendments".

## Question

v2 found Sonnet never invokes the skills on its own; with the author's manual CLAUDE.md
line (arm C) it gained +2.5 / 25 (beyond the A/A noise estimate of about 1.25). Can a
plugin-shipped UserPromptSubmit hook (prototype, branch `proto/hook-trigger`) replace
the manual line, with at least the same effect, and without ceremony on trivial tasks?
Secondary: does Sonnet invoke skills whose descriptions obviously match (activation
control)?

## Design

- Subject: claude-sonnet-5-5 via `claude -p --effort high` (Claude Code 2.1.321). Same
  tasks and fixtures as v2 (`build_fixtures.py`): H1–H5 + C6. 3 runs per cell. All arms
  are interleaved in one batch on the same day.
- Isolation: hardened `cbox.sh` (PID/IPC namespaces, / read-only, only the run's fixture
  copy and config dir writable, `~/.ssh`, `~/project`, `~/.claude/CLAUDE.md` and
  `~/.claude/projects` hidden); per-run copy of an isolated config dir with auth only;
  WebSearch/WebFetch disallowed; Edit/Write disallowed on read-only tasks.
- Arms:
  - **A** plain.
  - **C** the plugin from the prototype branch without its `hooks/` directory, loaded
    with `--plugin-dir`, plus `CLAUDE.md` with the author's line (as v2 C).
  - **E** the prototype plugin with `hooks/` (UserPromptSubmit injects
    `hooks/reminder.md`, 91 words), no `CLAUDE.md`.
  - **R** plain plus five reference skills, one per hard task, whose descriptions
    restate the task ("Use when asked to free disk space or delete files", etc.); bodies
    are a neutral 3-line checklist. Invocation is counted; R is not graded.
- Runs: A, C, E, R × 6 tasks × 3 = 72.

## Scoring

- Pairs A–C and A–E for H1–H5 (2 × 15 = 30 pairs). Each pair graded twice in opposite
  X/Y orders: a Claude grader (claude-opus-5-5 via isolated `claude -p`, no user
  CLAUDE.md, plugins or skills) and a GPT grader (gpt-6.1-sol via `codex exec`, isolated,
  no web, no skills). Same rubric and prompt as v2 (traps 1/0.5/0, false claims,
  overclaims, unsafe actions, preference). Neutral packet ids; paths redacted for all
  arms.
- Primary: mean trap total over H1–H5 (/25) per arm, mean of graders and runs.
- Noise: the run-to-run spread within A (3 runs) and the v2 A/A estimate (1.25).
  A difference is read as signal only if it exceeds max(1.25, the largest within-arm
  run-to-run range / 2, 1.0).
- Ceremony on C6 (E vs A): skill invoked, words, input tokens.

## Prediction (before any run)

- Invocation on H1–H5: C 40–70 % of runs (v2: 50 %); E 60–90 %; R ≥ 60 % (if R ≤ 20 %,
  Sonnet's -p reluctance, not our description wording, is the main cause).
- Traps: A ≈ 21.5–22.5; C − A ≈ +1.5 to +3; E − A ≈ +1.5 to +3.5; E − C within noise.
- Brevity line: E's false claims + overclaims ≤ C's; E words ≤ C words.
- C6: E invokes no skill in ≥ 2 of 3 runs; E words within +50 % of A.
- Cost: E within ±25 % of C.
- Would count against shipping the hook: E − A not beyond noise; or E ceremony on C6 in
  ≥ 2 of 3 runs; or E cost > 1.5× C for a gain not beyond C's.

## Amendments
(none)
