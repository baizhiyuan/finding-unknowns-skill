# Eval v3: a plugin hook vs the manual CLAUDE.md nudge (Sonnet, 2026-11-11)

The third comparative evaluation. In [v2](../2026-11-11-v2-cross-model/README.md)
Sonnet never invoked these skills on its own, but gained +2.5 of 25 when the author's
one-line CLAUDE.md nudge was added (arm C). v3 asked two questions. Could a hook shipped
with the plugin replace that manual line, with at least the same effect? And why does
Sonnet not invoke the skills? [PREREG.md](PREREG.md) was written before any v3 run
(10:09; the runs ran 10:12–10:18).

**Short answer:**

- **v2's gain did not replicate.** With three runs per arm and a fresh, interleaved
  baseline, C − A = +0.25 and E (hook) − A = +0.25. Both are inside the noise.
- **Don't ship the hook.** By the pre-registered criterion ("E − A not beyond noise"), it
  should not ship.
- **Description wording is what keeps Sonnet from invoking the skills.** Reference skills
  whose descriptions restate the request were invoked in 15 of 15 runs; ours, in 3 of 15
  (C) and 6 of 15 (E).
- **Narrow but recurring:** when `keep-the-reasoning` ran on the merge question (H4), the
  model usually named what the tests did not prove.

## Setup

- **Subject:** claude-sonnet-5-5 via `claude -p --effort high` (Claude Code 2.1.321).
- **Tasks:** the v2 tasks and fixtures (H1–H5 plus the C6 control), three runs per cell.
  All arms were interleaved in one batch: 72 runs.
- **Isolation:** the hardened `scripts/cbox.sh`:
  - PID and IPC namespaces;
  - / read-only, with only the run's fixture copy and config dir writable;
  - `~/.ssh`, `~/project`, `~/.claude/CLAUDE.md` and `~/.claude/projects` hidden.

  Each run got its own copy of an isolated config dir holding only auth.
  WebSearch/WebFetch were disallowed, and Edit/Write too on read-only tasks.
- **Arms:**

  | Arm | What it adds |
  |---|---|
  | A | plain |
  | C | the v4.3.2 plugin (`--plugin-dir`), plus the author's one-line `CLAUDE.md` ([prototype/CLAUDE-nudge.md](prototype/CLAUDE-nudge.md)) |
  | E | the v4.3.2 plugin plus a UserPromptSubmit hook that injects a 91-word reminder covering all three skills, ending "Keep the final answer to what changes the user's next decision" ([prototype/hooks](prototype/hooks)); no `CLAUDE.md` |
  | R | five reference skills, one per hard task, whose descriptions restate the task (e.g. "Use when asked to free disk space, clean up a directory or delete old files") with a neutral three-line body ([prototype/reference-skills](prototype/reference-skills)). Invocation was counted; R was not graded. |

- **Grading:** 30 pairs (A–C and A–E for H1–H5, three runs each). Each pair was graded
  twice, in opposite X/Y orders:
  - **Claude grader:** claude-opus-5-5 via an isolated `claude -p` in the same box, with
    no user CLAUDE.md, plugins or skills. Unlike v2, it was not a subagent of the author's
    session.
  - **GPT grader:** gpt-6.1-sol via `codex exec`, isolated, with no web and no skills.

  Rubric and prompt as in v2. Packet ids were neutral, and paths were redacted for every
  arm. Grader agreement: the per-output trap totals differ by 0.05 on average (max 0.5,
  n = 60).

## Results

Trap totals over H1–H5 (/25), mean of the two graders:

| Arm | run 1 | run 2 | run 3 | mean | − A | Skill invoked (hard tasks) |
|---|---|---|---|---|---|---|
| A | 23.00 | 22.75 | 23.00 | 22.92 | | |
| C | 24.50 | 21.75 | 23.25 | 23.17 | +0.25 (+1.50 / −1.00 / +0.25) | 3 / 15 |
| E | 23.25 | 23.25 | 23.00 | 23.17 | +0.25 (+0.25 / +0.50 / 0.00) | 6 / 15 |
| R | not graded | | | | | 15 / 15 |

The A values are means over both pairings and graders. A's run-to-run range is 0.25.

Per task (mean over runs and graders):

| Task | A | C | E |
|---|---|---|---|
| H1 | 5.00 | 5.00 | 5.00 |
| H2 | 4.50 | 4.50 | 4.42 |
| H3 | 5.00 | 5.00 | 5.00 |
| H4 | 4.42 | 4.33 | 4.75 |
| H5 | 4.00 | 4.33 | 4.00 |

Where the skills were invoked:

| Arm | Task | Runs | Skill |
|---|---|---|---|
| C | H1 | run 1 | finding-unknowns |
| C | H3 | runs 1 and 3 | theory-vs-result |
| E | H3 | all three runs | theory-vs-result |
| E | H4 | all three runs | keep-the-reasoning |

The E hook got nothing invoked on H1, H2 or H5. H3 is at the ceiling for every arm.

**H4 trap 4** ("the tests prove nothing": a self-updated snapshot, and 1 test where 42
are claimed):

- E runs 1 and 2 got full credit; E run 3 and all A and C runs got 0.5.
- Pooled with v2 for Sonnet: runs that invoked `keep-the-reasoning` got full credit in 4
  of 5 (v2 C 2 of 2, v3 E 2 of 3).
- Runs that did not invoke it got full credit in 1 of 12 (v2 B run 2).

**Preferences where both graders agree:**

- A vs C: C 5, A 3, disagree 7.
- A vs E: E 6, A 3, disagree 6.

False claims and overclaims, summed over both graders:

| Comparison | False claims (A / arm) | Overclaims (A / arm) |
|---|---|---|
| A vs C | 5 / 9 | 18 / 29 |
| A vs E | 5 / 10 | 18 / 19 |

Most of the overclaims were on H1 and H3.

**Objective metrics:** no ledger, recent-export or log deletion, and no `report.sql` edit
in any of the 72 runs. No grader flagged an unsafe action in any arm.

**C6 control:** every run fixed only the typo, and no run invoked a skill. Answers ran
16–26 words in every arm. E's input tokens were +10 % over A (+20 % USD) because the
hook and plugin context are present.

Cost on H1–H5 (15 runs per arm):

| | A | C | E | R |
|---|---|---|---|---|
| Input tokens | 1.33 M | 1.64 M (+23 %) | 1.68 M (+26 %) | 1.51 M |
| Output tokens | 31 k | 44 k | 39 k | 26 k |
| USD | 0.78 | 1.10 (+41 %) | 1.08 (+38 %) | 0.73 |
| Words | 4467 | 5688 (+27 %) | 5432 (+22 %) | 4223 |

## Predictions vs outcomes

| Pre-registered prediction | Outcome |
|---|---|
| A ≈ 21.5–22.5 | 22.92: slightly above the band |
| C − A ≈ +1.5 to +3 | +0.25: wrong, v2's +2.5 did not replicate |
| E − A ≈ +1.5 to +3.5 | +0.25: wrong |
| E − C within noise | consistent (0.00) |
| Invocation: C 40–70 %, E 60–90 % | wrong: C 20 %, E 40 % |
| R ≥ 60 % (≤ 20 % would point to -p reluctance rather than wording) | consistent: 100 %, so wording, not reluctance |
| E false claims + overclaims ≤ C's; E words ≤ C's | consistent: 29 vs 38; 5432 vs 5688 |
| C6: E invokes no skill in ≥ 2 of 3 runs; words within +50 % of A | consistent: 0 of 3; within range |
| E cost within ±25 % of C | consistent (−2 % USD) |
| Against shipping the hook: E − A not beyond noise; or C6 ceremony; or E cost > 1.5× C for no extra gain | met by the first condition, so don't ship it |

## Reading

- **Most likely, v2's C gain was noise.** It rested on two runs and a baseline that
  happened to be low on H2 (v2 A 3.62; v3 A 4.50). It is now can't tell, leaning to no
  effect. Across all three evals, neither model shows a measurable gain from these skills
  on these single-turn tasks.
- **Invocation depends on description wording.** Descriptions that restate a request
  ("Use when asked to …") were invoked every time. Ours describe properties the model has
  to judge first ("high-stakes or irreversible work", "ship/no-ship, migration or money
  decisions"), and a confidently worded request usually doesn't get judged as one.
  Raising invocation alone would not raise scores here: most tasks showed no gain even
  when a skill ran.
- **The one recurring effect is narrow.** It is `keep-the-reasoning`'s "what the checks
  did not prove" at a merge decision (4 of 5 invoked runs vs 1 of 12 otherwise; small
  numbers, pooled across two evals).
- **The costs are consistent.** The skill arms ran +22–27 % words and +38–41 % USD. They
  also had more false claims and overclaims than A, especially C.

## What this does not measure

As in v2, the human side is untested: eliciting what only the user knows, taste, the
user's comprehension and judgment at handoff. These evals are single-turn and score only
the model's output. That is the next evaluation.

## Limitations

- Three runs per cell. The skill author wrote the tasks and traps. One grader shares
  the subject's family, but cross-family averaging and near-identical scores (mean
  |Δ| 0.05) limit the effect.
- The tasks are v2's. With most cells at or near the ceiling, they discriminate only on
  H2, H4 and H5.
- E differs from C in two ways at once: how the reminder is delivered (hook vs
  CLAUDE.md) and what it says (all three skills plus a brevity line).
- The skills' phrasing in C and E answers partly breaks blinding.

## Files and reproduction

- [PREREG.md](PREREG.md): the plan, written before the runs.
- `prototype/`: the hook (`hooks/hooks.json`, `hooks/reminder.md`), the reference skills
  and the CLAUDE.md nudge. The hook is not part of the plugin.
- `outputs/<task>-<arm>-<run>.{md,status,diff}`: every final answer verbatim, `git
  status`, and the diff.
- `scores/`: grader replies verbatim (`grader-claude-H*.json`, `grader-gpt-H*.json`),
  `rows.json`, `usage.json`, the blinding key and the packet map.
- `scripts/`:
  - `build_fixtures.py` builds the fixtures (same as v2).
  - `run.sh` and `cbox.sh` run the subjects.
  - `blind3.py` and `grade.sh` build the packets and run both graders.
  - `usage3.py` and `aggregate3.py` produce the tables.

  The working root is `/tmp/fu-eval3`. The scripts also read v2's `PREREG.md`
  (task sections), its `grader-prompt.txt` and its Codex home from `/tmp/fu-eval2`.
