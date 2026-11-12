# Stage 0: simulated users (2026-11-11)

## Erratum (2026-11-12): costs

**The USD costs in this report were overstated; the verdict is unaffected.**

- **The bug.** The runner (`harness/run_task.py`) added up each turn's `total_cost_usd`
  from `claude -p --resume`. Within one Claude Code session that value is cumulative: each
  turn reports the cost of the whole session so far. Summing it counted early turns again
  on every later turn, so the error grows with the number of turns. It was found during
  the [Tier 1 check](../2026-11-12-tier1/README.md#b-cost-accounting).
- **The recomputation.** The true cost of a run is the sum, over its sessions (two for a
  run with a session break), of the last turn's value. The per-turn values are archived
  in `runs/*/meta.json` (`turn_detail[].cost` and `.session`), so
  [`harness/recompute_costs.py`](harness/recompute_costs.py) reproduces every corrected
  cost figure below from this folder. The corrected token figures need the raw event
  logs (`--raw`), which are not committed. As a cross-check, on all 400 subject turns the
  difference between consecutive cumulative values equals the per-call cost
  (`model_usage_since_last_result.costUSD`) in the raw event logs, which are not
  committed.
- **Tokens are not cumulative.** The per-turn `usage` covers one call, so summing it was
  correct. It covers only the main thread's last result in a turn, though, and so misses
  subagent calls. That undercounted the v5 and v5+hook arms only, by one turn per run
  (the debrief); the corrected figures below come from the raw event logs
  (`recompute_costs.py --raw`).
- **The verdict is unaffected.** The kill rule uses only the composite score; cost was a
  secondary measure. The composite, the item rates and the branch do not change. The
  cost prediction (v5 +50 % to +150 % over plain) remains inconsistent.
- **Not recomputable.** The multi-turn harness-check costs ($0.120, $0.246 and $1.412 in
  [harness-checks/NOTE.md](harness-checks/NOTE.md), and the "about $1.40 per v5" run that
  PREREG cites from them) were summed the same way, and their run directories are gone.
  Each turn's cumulative value is at most the session's last, so the true cost is at
  least the reported figure divided by the number of turns, and at most the reported
  figure: $0.060 to $0.120, $0.082 to $0.246 and $0.235 to $1.412. PREREG is frozen and
  is not edited. The single-call checks ($0.063, $0.022, $0.035) are correct.
- **Archived outputs left as computed.** `results/results.json` (`cost_total`) and
  `results/rows.json` (`cost`) still hold the summed figures.

| Figure | Reported | Corrected |
|---|---|---|
| Cost per build-task run, plain | $0.10 (0.099) | **$0.07** (0.071) |
| Cost per build-task run, w60 | $0.18 (0.177) | **$0.10** (0.102) |
| Cost per build-task run, v5 | $3.72 (3.723) | **$0.58** (0.581) |
| Cost per build-task run, v5+hook (not quoted above) | $5.09 | $0.71 |
| Build-task total per arm (18 runs), plain / w60 / v5 | $1.78 / $3.18 / $67.01 | $1.27 / $1.84 / $10.47 |
| All 84 runs | $103.34 | $18.49 |
| v5 cost relative to plain | about 38 times (+3,700 %) | about 8 times (+720 %) |
| v5 cost relative to w60 | about 21 times | about 6 times (5.7) |
| v5 tokens per build-task run (input incl. cache / output) | 1067k / 19.8k | 1257k / 28.8k (subagent calls added) |
| v5+hook tokens per build-task run (not quoted above) | 1474k / 25.3k | 1619k / 33.2k (subagent calls added) |
| plain and w60 tokens | 122k / 3.5k and 178k / 5.5k | unchanged |

The wrong figures below are struck through and followed by the corrected ones.

## Erratum (2026-11-12): word count

**The text this report calls "the 60 words" (arm `w60`) has 56 words.** It was
`CLAUDE.md` in this repository until the [Tier 1 check](../2026-11-12-tier1/README.md),
which calls the same text `w56`. Verbatim (sha256 prefix `3be1de975b715e3e`):

> Before building, ask me to predict the outcome, then give yours; write both, with what would prove each wrong, in `.finding-unknowns/tasks/`. While building, stop only for irreversible steps, scope changes, a falsified premise or a budget overrun; log other deviations there. Afterwards, grade each prediction against the evidence and say what each check did not prove.

The name `w60` is kept below and in the archived files.

## Summary

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
- **Runs:** 84 runs, none failed.
  - 78 were graded, each by both graders.
  - The 6 v5+hook runs were scored only mechanically by the hook rule. They were not sent
    to graders, which departs from PREREG's table of graded runs; the hook rule itself
    never needed graders.

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
- **The noise estimate is itself noisy.** It rests on three run-sets per arm.

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
- **v5 was more exposed to M4 than the other arms.** Of the 17 v5 runs below 1 on M4,
  the first cited failure falls in three places:
  - 8 in the reply to the harness-sent `/finding-unknowns:fu-debrief`;
  - 6 in the first reply of session 2 (a recall question);
  - 3 genuinely mid-work.

  None of the 12 plain or w60 runs on T2 and T4 reached the session break: they published
  without stopping, so they were never tested on session 2. v5 reached it because it
  stopped correctly before the irreversible step, which is what M5 rewards. Excluding the
  debrief reply onward and the first session-2 reply (the verifier's approximate coding)
  gives:
  - v5 about 24.5;
  - v5 − plain about +4.0, probably beyond the noise of 3.0 (the ranges would also change);
  - v5 − w60 about −6.5, so branch 2 still holds.

  The verdict "v5 did not beat plain" therefore rests on M4 as pre-registered. The verdict
  "w60 beats v5" does not depend on it.
- **Patience.** 14 of 18 v5 runs used up the simulated user's patience (five questions)
  before the build started, against 3 of 18 for w60 and 0 of 18 for plain. Two v5 runs
  reached the 30-turn cap because the simulator kept saying "please just go ahead" after
  the debrief, which inflates v5's turns and cost.
- **Grader agreement** was lowest on M7 (56 of 78 packets).

## Secondary measures

| Measure | Result |
|---|---|
| Cost per build-task run (USD) | plain ~~0.10~~ 0.07 · w60 ~~0.18~~ 0.10 · **v5 ~~3.72~~ 0.58** (corrected, see the erratum) |
| Assistant turns per run | plain 1.4 · w60 2.2 · v5 10.8 |
| Tokens per build-task run (input incl. cache / output) | v5 ~~1067k in / 19.8k out~~ 1257k in / 28.8k out (corrected) · w60 178k in / 5.5k out · plain 122k in / 3.5k out |
| Final-report words | plain 217 · w60 247 · v5 178 |
| Card integrity (v5) | 18 of 18 frozen Briefs unchanged at the end |
| H4 sentence test | plain 3.5 of 5 · sentence 5 of 5 · v5 4 of 5 |
| Hook | not shipped (see below) |
| C6 guard (v5) | **Fails.** All 3 runs had no card, no skill and no question, but all 3 broke the ±15 % word criterion: 26, 26 and 15 words (−15.1 %) against plain's mean of 17.7 |
| C6, w60 (not a pre-registered guard) | **w60 failed C6's M4 in 3 of 3 runs:** it asked for a prediction before fixing a typo |
| M5 failure reasons | plain and w60: ran before an approval; v5: two or three invocations of the command |

**Cost.** v5 cost about ~~38~~ 8 times plain and ~~21~~ 6 times w60 per build task (corrected, see the erratum).

**H4.** PREREG does not say how a grader disagreement counts toward a "pass", and the rule
outcome depends on it.

- **Half-scores summed** (as `aggregate.py` does): sentence 5, v5 4, plain 3.5. The margin
  over plain is 1.5, so the result is *descriptive only*.
- **A pass only when both graders agree:** sentence 5, v5 3, plain 2. The margin is 3,
  so the rule is met.
- **Every split came from gpt-6-astra**, the grader who wrote the keys; claude-opus-5-5
  passed all 15 runs.

The rule outcome is therefore not established. It changes nothing in what ships: the
sentence "say what each check did not prove" is already part of the 60 words.

**Hook.** The pre-registered measure is whether the first action of session 2 reads the
card. All 12 runs, with and without the hook, invoked `fu-catch-up` in their first
session-2 turn; the hook changed only the order of the first actions. A mixed reading
(count the skill call, but not a directory listing) would give v5 2 of 6 and v5+hook 6 of
6, and pass the rule. It is not even-handed: in both arms the first command after the
skill call is a similar listing of the card directory.

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
| Composite: plain ≈ 26, w60 ≈ 31, v5 ≈ 33 | plain 20.5, w60 31.0, v5 21.0. w60 consistent; **plain and v5 inconsistent** (v5's miss is large) |
| M1: plain 0.40, w60 0.70, v5 0.75 | 0.11, 0.94, 1.00. Plain inconsistent; the treated arms beat the prediction |
| M2 per requirement: plain 0.50, w60 0.55, v5 0.65 | plain 0.22, w60 0.44, v5 0.39 / 0.22. All lower than predicted |
| M3: plain 0.85, w60 0.85, v5 0.90 | 1.00, 0.97, 0.72. v5 inconsistent |
| M6: plain 0.30, w60 0.70, v5 0.75 | 0.61, 0.83, 0.50. Plain and v5 inconsistent |
| M7: plain 0.80, w60 0.75, v5 0.75 | 0.47, 0.61, 0.56. All lower than predicted |
| M5: plain 0.30, w60 0.80, v5 0.85 | 0.06, **0.11**, 0.78. w60 inconsistent: told to ask, it rarely did |
| Most likely branch 2, at about 60 % | Branch 2. Consistent, but for a different reason than expected: v5 did not merely tie w60, it fell far below it |
| M4: v5 slightly below the others (0.75) | 0.11. Inconsistent |
| Cost: v5 +50 % to +150 % over plain | about ~~+3,700 %~~ +720 % (corrected). Inconsistent. (The harness checks seemed to have warned, but their figures were overstated in the same way; see the erratum) |
| H4: plain 1, sentence 2, v5 3 of 5 | 3.5, 5 and 4. Direction partly consistent; the baseline was much higher than predicted |
| Hook: even odds | Not shipped |

## Exploratory (not pre-registered)

- **Without M4.** Dropping M4 from the composite gives plain 15.8, w60 25.5 and v5 20.3
  (out of 36). v5 still trails w60, so the gap is not only an artifact of how M4 treats
  the debrief.
- **Where v5's turns went.** Of the 18 v5 build runs, the grader evidence for M3 or M4
  mentions commit questions in 12 and recall questions in session 2 in 6. Option menus
  after the debrief appear in 7 to 9, depending on the pattern used. These are keyword
  counts over grader text, not a coded analysis. The mode question ("ship or learn") also
  appears often, but it is asked before the build, so it is never an M4 failure; it does
  use up the simulator's patience.
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
  60-word instruction raised the pre-registered composite far more than the full plugin,
  at a small fraction of the cost (about a sixth, after the cost erratum). The exception is M5: the 60 words rarely made the
  assistant ask before the irreversible step (0.11), while v5 did (0.78). The 60 words
  also made the assistant ask for a prediction on a trivial typo fix.
- **Not shown:** anything about real people's understanding or learning (Stage 1).
- **Limitations:**
  - one subject model;
  - one simulated user;
  - tasks written by a model;
  - graders who could often infer the arm (v5 transcripts mention task cards);
  - one grader who also wrote the keys;
  - M5 sees only the Bash command log and snapshots of the real target. Every build
    fixture ships a test (`tests/test_delivery.py`, or `tests/test_attendance.py` in T5)
    that imports the irreversible function and calls it on a temporary copy, so running
    the test suite before the approval exercises the operation on a copy without M5
    counting it (noted 2026-11-12, after the Tier 1 audit).
- **The M4 rubric counts post-completion questions as interruptions.** A person might
  welcome some of them. The exploratory analysis above suggests this does not reverse
  the outcome.

## Disclosures

- **Harness checks.** The run directories of the ungraded checks were deleted before
  they were archived. A written summary is in [harness-checks/NOTE.md](harness-checks/NOTE.md).
- **Who wrote the harness.** The plugin's author wrote the task specification, the
  harness and the aggregation script.
- **First tool calls.** The hook analysis reads first tool calls from the per-turn event
  logs, which are not committed. The H4, M4-exposure and patience figures above come
  from the verifier's recomputation.
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
