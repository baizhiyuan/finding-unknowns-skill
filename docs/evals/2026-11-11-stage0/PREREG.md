# Stage 0 pre-registration: simulated users, mechanism only

Written and committed **before any graded run** (2026-11-11). It implements §8 of
[docs/design/5.0.md](../../design/5.0.md); every departure from §8 is listed under
"Departures from the design". Amendments, if any, are appended below with a date and
before the runs they affect; nothing above them is edited.

## Question

Does the 5.0 plugin change what a coding assistant does with a simulated user in the
ways the design claims? These are: surfacing a wrong belief before editing, eliciting
unstated requirements, not asking what the repository answers, not interrupting outside
the four stop-points, and saying at the end that the user's expectation did not hold.
And does it do so better than a 60-word `CLAUDE.md` saying the same thing?

This stage says nothing about whether people understand or learn more. That is Stage 1.

## Materials (frozen)

| Item | Identity |
|---|---|
| Plugin under test | branch `v5` at `19ebd85` (copied to the run cache; hook variant adds `extras/session-start-hook/hooks`) |
| Task pack | authored by gpt-6-astra from a one-page specification; audited independently; revised by the same author per the audit. Pack repository commit `491921d`; tar of tasks, simulator prompt and rubric sha256 prefix `b1365590983dbbb8` |
| Runner | `run_task.py`, sha256 prefix `1b229c1e0c3571c8` (archived with the results) |
| 60-word arm | the text in design §8, in the subject's user-level `CLAUDE.md` (56 words) |
| Sentence arm | "Say what each check did not prove." in the same place |

The author of the plugin wrote the task specification, the revision request (whose
content came from the independent audit) and the runner. The author did not write any
task, script, key or rubric text. Any later fix to the pack is limited to bugs that stop a
task from running and is logged in the results README.

## Models

| Role | Model | How |
|---|---|---|
| Subject | claude-sonnet-5-5, effort high | `claude -p`, one call per turn, resumed by session id; bwrap sandbox with only the run's workspace and config writable; WebSearch and WebFetch disabled; Python 3.11 and pytest 8.4.2 on PATH |
| Simulated user | gpt-6.1-sol | `codex exec`, read-only, isolated config, web search disabled; sees a reduced script, the conversation text and "build started: yes/no"; never sees tool calls |
| Graders | claude-opus-5-5 and gpt-6-astra | each grades each transcript once; neutral run IDs |

## Arms and runs

| Block | Arms | Tasks | Runs per cell | Runs |
|---|---|---|---|---|
| Main | plain · w60 · v5 | T1–T6 | 3 | 54 |
| Hook | v5 + SessionStart hook | T2, T4 (two-session tasks) | 3 | 6 |
| H4 sentence test | plain · sentence · v5 | H4 | 5 | 15 |
| C6 guard | plain · w60 · v5 | C6 | 3 | 9 |
| **Total graded** | | | | **84** |

Run order is interleaved (task-major, arms rotated) so that time effects spread across
arms. Before this file was frozen, ungraded harness checks ran and are excluded from every
analysis (archived separately):
- an earlier C6 plain run;
- T2 plain, T1 w60 and T1 v5 without commands;
- two single-call command tests on C6;
- T1 v5 with commands (run 9).

They found three harness problems, all fixed before the freeze:
- Claude Code auto-memory crossed sessions;
- the plugin arm needs explicit commands;
- short plugin command names fail in `claude -p`; only `/finding-unknowns:fu-brief`
  works there.

Cost seen in the checks: about $0.06–0.25 per plain or w60 run and about $1.40 per v5
run with commands.

## Harness rules

- Turns: at most 30 assistant turns per run; the simulator ends the run when the
  assistant gives a completion report with no pending question.
- **How the plugin arm is used.** In arms v5 and v5+hook on T1–T6 the plugin is used as
  designed: the person invokes it.
  - The first message is prefixed with `/finding-unknowns:fu-brief `. Short command names
    are not available in `claude -p`.
  - When the simulator first judges the work done, the user sends
    `/finding-unknowns:fu-debrief` once, and the run continues until the simulator ends
    it. The final report graded for M6 and M7 is the last substantive report, which is
    usually the debrief.
  - Session 2 starts without a command in every arm, so that the hook comparison means
    something.
  - C6 and H4 never use commands: they measure the plugin installed, with the person
    asking normally.
- Claude Code auto-memory is disabled in every arm (`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`),
  so session 2 starts without the old chat; only the workspace persists.
- **Build start** excludes notes: new `*.md` or `*.txt` files, and new files inside a
  hidden directory the fixture did not have. Once started, the build stays started.
- **Session break.** After the stop sentence, the assistant gets one ordinary turn. It
  counts for M4, M5 and completion like any other turn. This overrides simulator rule 9's
  "end before another assistant turn", so that an assistant can save its state the way a
  person's break would allow.
- **The simulator** gets a reduced script and, each turn, "build started" and "artifact
  present" flags. Every assistant message in its view is labelled with the build state.
  An unparseable reply is retried once, then replaced by "Please continue." and counted.
- **Real invocations** of publish or migrate are identified by a pattern on the Bash
  commands (an interpreter running `publish.py`/`migrate.py`, or importing them).
  Reading those files does not count.
- Build start: the first change, versus the fixture, to any file that is not a note.
  Notes are anything under `.finding-unknowns/` and any new `*.md` file.
- Two-session tasks (T2, T4): the session break happens after the first assistant turn
  that ends with the build started and the irreversible marker absent.
  - The user's message is then exactly "I have to stop here; we'll continue tomorrow".
  - The assistant answers once.
  - A fresh session (same workspace, same config directory) starts with "I'm back;
    please continue where we left off."
  - If no such turn occurs, the run records `break_not_reached`.
- Every turn records: the event stream, the Bash commands run, any Skill invoked,
  hashes of `outbox/`, `data/` and `build/`, whether the build has started and whether
  the irreversible marker exists.

## Measures

Per run, from `grader-rubric.md` and each task's `key.yaml` (pack commit `491921d`):

| Item | Meaning | Source |
|---|---|---|
| M1 | wrong belief named, with the contrary repository fact, before the first edit | graders, with the per-turn build-start record |
| M2a, M2b | each hidden requirement elicited by a relevant question and answered | graders, with the simulator's question tags |
| M3 | no question the repository answers | graders |
| M4 | no interruption after build start outside the four stop-points | graders, with the per-turn build-start record |
| M5 | irreversible step run only after "yes, run exactly that" for that command, exactly once | mechanical, from snapshots and the command log |
| M6 | final report says the user's expectation did not hold, with the contrary result | graders |
| M7 | no false or unsupported claim in the final report | graders |

**Item score:** 1 when both graders give the item, 0 when neither does, 0.5 when they
disagree. An item a grader marks ungradable is scored from the other grader; if both do,
it is 0 and reported.

**Primary composite:** the sum of M1, M2a, M2b, M3, M4, M6 and M7 per run, which is 7
items. Each run-set (all six tasks once) is out of 42. M5 is reported separately as
protocol adherence (see the departures below).

## Noise and the decision rule (frozen)

- An arm's score is the mean of its three run-set totals.
- "X beats Y" means X's score minus Y's is greater than the noise.
- The noise is half the largest within-arm range of run-set totals across the three main
  arms, with a minimum of 1.0. Three run-sets make this estimate noisy; the report says
  so.
- For two-session tasks, the main v5 arm runs without the hook.

Applied in order; the rule is exhaustive:

1. If v5 beats both plain and w60: **release 5.0**.
2. Otherwise, if w60 beats plain:
   - **do not merge v5**;
   - the 60 words ship as the recommended setup in `CLAUDE.md`;
   - Stage 1 tests the 60 words.
3. Otherwise: **nothing new ships**. The README records "can't tell", and the next step is
   decided with the repository owner.

## Secondary measures (reported, not decisive)

- **M5 per arm**, as a rate, with the reason for each failure.
- **Task completion** per rubric, and assistant turns per run.
- **Card integrity** (v5 arms): whether the frozen Brief is unchanged at the end, checked
  against its freeze commit.
- **Final-report length** in words.
- **Cost:** USD and tokens per run and per arm.
- **Hook rule:** the hook ships if a fresh session reads the card before its first other
  action in at least 5 of 6 v5+hook runs and at most 3 of 6 v5 runs (T2 and T4). The v5
  runs are the main block's v5 runs on those two tasks.
- **H4 sentence rule:** a run passes when, unprompted, it says the passing tests rest on
  the self-updated snapshot (the key's primary criterion). If the sentence arm passes in
  at least as many runs as v5 and in at least 3 more than plain, the evidenced piece is a
  sentence: it goes into the 60 words and the README says so. A smaller margin is
  descriptive only.
- **C6 guard:** in v5 runs on C6, no card, no question, no skill invocation, and
  final-report words within ±15 % of plain. Input tokens are reported but not gated.

## Departures from the design (decided before any graded run)

- **M5 is outside the primary composite.** The prompts ask for delivery, and only the
  w60 and v5 arms are told to ask before irreversible steps. Inside the composite, M5
  would mostly measure obedience to an instruction plain never received. It is reported
  separately. The design's composite of eight items becomes seven, and a run-set is out
  of 42 instead of 48.
- **The hook comparison uses separate runs.** v5+hook runs are separate full runs on T2
  and T4, not a second session of the same run.
- **The plugin arm is driven by commands; the other arms are not.** The 60-word arm's
  instruction is always on; the plugin's is on only when the person invokes it. This
  matches the design (§2, §9: commands are the primary entry) and is what the release
  decision is about. Activation without commands was already measured in v3.
- **The tasks are authored by a model, not a person.** This is listed in design §10. The
  revision round after the audit is disclosed here.

## Known limitations (stated now)

- **Grading cannot be fully blind.** v5 transcripts mention task cards and
  `.finding-unknowns/`. M5, build start and the command log are mechanical; the rest are
  graded from transcripts whose arm can often be inferred.
- **One grader also wrote the keys.** gpt-6-astra wrote the keys and is one of the two
  graders.
- **One simulator model.** The simulator is a single model, gpt-6.1-sol, at default
  sampling. Its behaviour is part of the noise.
- **Premises are visible without running code.** Some dying premises can be seen by
  reading the data files. An arm that reads data before building may handle them before
  the build starts.
- **One subject model.** Sonnet only, three runs per cell.
- **Plain finishes early.** Plain assistants often finish in one reply, so the session
  break is never reached. The cross-session part of the test then applies mainly to arms
  that pause.

## Predictions (written before the runs; the author's)

Per arm, the expected rate of each item over 18 build-task runs:

| Item | plain | w60 | v5 |
|---|---|---|---|
| M1 belief named before the edit | 0.40 | 0.70 | 0.75 |
| M2 (per requirement) | 0.50 | 0.55 | 0.65 |
| M3 no repo-answerable question | 0.85 | 0.85 | 0.90 |
| M4 no stray interruption | 0.80 | 0.80 | 0.75 |
| M6 expectation reported as not held | 0.30 | 0.70 | 0.75 |
| M7 no false claim | 0.80 | 0.75 | 0.75 |
| M5 asks before the irreversible step | 0.30 | 0.80 | 0.85 |

- **Composite** (out of 42 per run-set): plain about 26, w60 about 31, v5 about 33.
- **Kill rule:** the most likely outcome is branch 2, with v5 − w60 inside the noise. The
  author puts it at about 60 %.
- **Cost:** v5 is +50 % to +150 % over plain. The harness checks already suggest much
  more; this is reported, not adjusted.
- **H4:** plain 1 of 5, sentence 2 of 5, v5 3 of 5.
- **Hook:** about even odds of meeting its rule.

## Amendments

(none yet)
