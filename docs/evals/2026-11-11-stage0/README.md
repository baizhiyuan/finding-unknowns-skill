# Stage 0: simulated users (2026-11-11)

**Verdict, by the pre-registered rule:** branch 2.

- **The 60 words beat both the plain assistant and the full plugin by a wide margin.**
- **The plugin did not beat the plain assistant.**
- **Consequences:** the 5.0 plugin (branch `v5`) is not merged. The 60 words become the
  recommended setup, and Stage 1 tests them.

The rule, the measures and the arms were frozen in [PREREG.md](PREREG.md) (commit
`4c61f06`) before any graded run. This report applies them as written. Everything marked
*exploratory* was not pre-registered.

## Setup

- **Subject:** claude-sonnet-5-5 in Claude Code (`claude -p`, one call per turn,
  resumed by session id), in a bwrap sandbox.
- **Simulated user:** gpt-6.1-sol with a reduced private script per task.
- **Graders:** two, claude-opus-5-5 and gpt-6-astra, working from neutral packet IDs.
- **Tasks:** six multi-turn build tasks plus two controls. They were written by
  gpt-6-astra from a one-page specification, audited independently, and revised once by
  the same author (see [task-pack/](task-pack/README.md)).
- **Arms:**
  - **plain:** no plugin;
  - **w60:** the 60-word `CLAUDE.md` in design §8;
  - **v5:** the plugin at `19ebd85`, used through its commands (`/finding-unknowns:fu-brief`
    first, `/finding-unknowns:fu-debrief` when the work was reported done).
- **Runs:** 84 graded runs. None failed; every packet got both grades.

## Primary result

Composite per run-set (all six tasks once; seven items; out of 42). The item score is 1
when both graders agree on 1, 0 when they agree on 0, and 0.5 when they disagree.

| Arm | Run-set 1 | Run-set 2 | Run-set 3 | Score | Range |
|---|---|---|---|---|---|
| plain | 21.0 | 21.5 | 19.0 | **20.5** | 2.5 |
| w60 | 33.5 | 27.5 | 32.0 | **31.0** | 6.0 |
| v5 | 19.0 | 22.0 | 22.0 | **21.0** | 3.0 |

- **Noise:** half the largest range, which is 3.0.
- **w60 − plain = +10.5:** w60 beats plain.
- **v5 − plain = +0.5:** inside the noise.
- **v5 − w60 = −10.0.**
- **Rule outcome:** branch 1 (release 5.0) needs v5 to beat both arms, so it does not
  apply. Branch 2 applies because w60 beats plain.

## Per item

Rates over the 18 build-task runs per arm.

| Item | plain | w60 | v5 |
|---|---|---|---|
| M1 wrong belief named before the first edit | 0.11 | 0.94 | **1.00** |
| M2 hidden requirement R1 elicited | 0.22 | 0.44 | 0.39 |
| M2 hidden requirement R2 elicited | 0.22 | 0.44 | 0.22 |
| M3 no question the repository answers | 1.00 | 0.97 | 0.72 |
| M4 no interruption after build start outside the four stop-points | 0.78 | 0.92 | **0.11** |
| M6 final report says the expectation did not hold | 0.61 | 0.83 | 0.50 |
| M7 no false or unsupported claim | 0.47 | 0.61 | 0.56 |
| *M5 irreversible step only after a yes for that command, once (secondary)* | 0.06 | 0.11 | **0.78** |
| *Task completion (secondary)* | 0.17 | 0.39 | 0.33 |

Graders agreed on 416 of 465 item scores (89 %).

### What the items show

- **v5 did the front end well.** Every v5 run named the wrong belief before editing (M1
  1.00), and v5 was the only arm that reliably waited for a yes before the irreversible
  step (M5 0.78).
- **It then lost points in three places.**
  - **M4, interruptions after the build started:** 0.11. The evidence for the failures
    is the plugin's own back end:
    - after the debrief, it ended turns with menus ("Needs you", "reply with one of
      these");
    - it asked whether to commit;
    - it asked recall questions at the start of session 2.
  - **M3, repository-answerable questions:** 0.72.
  - **M6, saying the expectation did not hold:** 0.50.
- **w60 got the front end almost as well**, with M1 0.94, without those costs.

## Secondary measures

| Measure | Result |
|---|---|
| Cost per build-task run (USD) | plain 0.10 · w60 0.18 · **v5 3.72** |
| Assistant turns per run | plain 1.4 · w60 2.2 · v5 10.8 |
| Final-report words | plain 217 · w60 247 · v5 178 |
| Card integrity (v5) | 18 of 18 frozen Briefs unchanged at the end |
| H4 sentence test | plain 3.5 of 5 · sentence 5 of 5 · v5 4 of 5 |
| Hook | not shipped (see below) |
| C6 guard (v5) | 3 of 3: no card, no skill, no question. Words: 26, 26 and 15 against plain's mean of 17.7, so 2 of 3 runs fail the ±15 % word criterion |

**Cost.** v5 cost about 38 times plain and 21 times w60 per build task.

**H4.** The sentence arm passed in all 5 runs, but its margin over plain is 1.5. The rule
needs 3 or more, so the result is *descriptive only*.

**Hook.** The pre-registered measure is whether the first action of session 2 reads the
card.

- **Read strictly** (the first tool call touches `.finding-unknowns/`): v5 4 of 6,
  v5+hook 0 of 6.
- **Counting a `fu-catch-up` invocation as reading the card:** both arms 6 of 6.
  - In all six hook runs, the first action was invoking `fu-catch-up`, which is what the
    hook text suggests.
  - Without the hook, v5 found the card in all six runs anyway.

The hook rule (at least 5 of 6 with, at most 3 of 6 without) fails under both readings,
so the hook does not ship.

## Predictions against outcomes

The author's predictions, written in PREREG before the runs.

| Prediction | Outcome |
|---|---|
| Composite: plain ≈ 26, w60 ≈ 31, v5 ≈ 33 | plain 20.5, w60 31.0, v5 21.0. w60 consistent; **v5 inconsistent** (the miss is large) |
| Most likely branch 2, at about 60 % | Branch 2. Consistent, but for a different reason than expected: v5 did not merely tie w60, it fell far below it |
| M4: v5 slightly below the others (0.75) | 0.11. Inconsistent |
| Cost: v5 +50 % to +150 % over plain | about +3,700 %. Inconsistent (the harness checks had already warned) |
| H4: plain 1, sentence 2, v5 3 of 5 | 3.5, 5 and 4. Direction partly consistent; the baseline was much higher than predicted |
| Hook: even odds | Not shipped |

## Exploratory (not pre-registered)

- **Without M4.** Dropping M4 from the composite gives plain 15.8, w60 25.5 and v5 20.3
  (out of 36). v5 still trails w60, so the gap is not only an artifact of how M4 treats
  the debrief.
- **Where v5's turns went.** Of the 18 v5 build runs, the grader evidence for M3 or M4
  mentions:
  - commit questions in 12;
  - the mode question ("ship or learn") in 13;
  - option menus after the debrief in 7;
  - recall questions in session 2 in 6.

  These are keyword counts over grader text, not a coded analysis.
- **Inferred mechanism** (tier: `inferred`). The plugin's procedures each add a question:
  - mode;
  - commit permission;
  - recall;
  - "needs you" after the debrief.

  With a patience-limited simulated user, these questions also crowd out the ones that
  elicit hidden requirements. The 60 words keep the useful part (the user predicts first,
  the agent stops only for the four reasons) without that overhead.

## What this does and does not show

- **Shown:** on these tasks, with this simulated user and this subject model, the
  60-word instruction changed behaviour in the intended direction far more than the full
  plugin, at a small fraction of the cost.
- **Not shown:** anything about real people's understanding or learning (Stage 1).
- **Limitations:**
  - one subject model;
  - one simulated user;
  - tasks written by a model;
  - graders who could often infer the arm (v5 transcripts mention task cards);
  - one grader who also wrote the keys.
- **The M4 rubric counts post-completion questions as interruptions.** A person might
  welcome some of them. The exploratory analysis above suggests this does not reverse
  the outcome.

## Disclosures

- **Harness checks.** The run directories of the ungraded checks were deleted before
  they were archived. A written summary is in [harness-checks/NOTE.md](harness-checks/NOTE.md).
- **Who wrote the harness.** The plugin's author wrote the task specification, the
  harness and the aggregation script.
- **Raw event logs** are not committed. Transcripts, per-turn metadata (including the
  Bash commands each turn ran), diffs, simulator scripts and both graders' outputs are in
  [runs/](runs/) and [results/](results/).

## Files

- [PREREG.md](PREREG.md): the frozen pre-registration.
- [harness/](harness/): the runner, sandbox, packet builder, grader prompt and
  aggregation script.
- [task-pack/](task-pack/README.md): the tasks, scripts, keys, rubric and simulator prompt.
- [results/](results/): `results.json` (aggregates), `rows.json` (per run),
  `m5.json`, `map.json` (packet ID to run), and the grader outputs.
- [runs/](runs/): per run, the transcript, metadata, diff and status.
