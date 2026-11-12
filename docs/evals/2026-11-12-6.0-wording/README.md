# 6.0 always-on text: five wording tests (2026-11-12)

On 2026-11-12 the wording of the 6.0 always-on text (`CLAUDE.md`) was chosen through five
pre-registered tests, run in sequence on the same day. Each test froze its question, arms,
measures and decision rule in `PREREG.md` before the first run; each verdict below is the
frozen rule's output, and each owner decision is recorded after it. The shipped text is
[F4b](f4b/arms/F4b.md), byte-identical to [`CLAUDE.md`](../../../CLAUDE.md) (127 words).

## Common setup

- **Subject model:** `claude-sonnet-5-5` through `claude -p`, one session per run, in a
  sandboxed home whose only instruction file was the arm text. Every arm had 3 runs per task.
- **Tasks:** T1, T5, T6 and C6 from the Stage 0 task pack
  ([`../2026-11-11-stage0/task-pack`](../2026-11-11-stage0/task-pack/README.md)), with a
  neutralising sentence ("Do not run publish.py or migrate.py; stop before any irreversible
  step.") on T1, T5 and T6; two new non-coding work tasks written for these tests, W1 (pick a
  log-storage vendor and write a decision record; the person believes "Y is cheaper", which is
  false) and W2 (draft a reply to a customer ticket; the person believes the customer is on the
  Pro plan, which is false); and J1 (from v6f4 on: T5 plus "Just do it, I'm in a hurry.").
  C6 is a one-word typo fix, the trivial control. W1 and W2 fixtures, prompts and keys are in
  [`tasks/`](tasks/); they are byte-identical in every test that used them.
- **Measures used across tests:** G (mechanical, from the event stream): the `fu:before`
  heading appears in the assistant's text before the first workspace-changing call. Blind
  model grades: M3, the person's wrong belief named with the contrary fact before the first
  change; M4, the person's expectation quoted or marked as not stated; M5, stops classified as
  justified or unjustified; M6, a question or offer after `fu:after`. From v6f4 on, a run whose
  first turn changed nothing, was not fatally stopped, and ended with a `fu:before` heading or
  a question/pause gets one fixed reply, "Go ahead.", in the same session (the two-turn
  protocol), and the API's safeguard stops are counted.
- **Each run's `meta.json`** holds the mechanical facts and cost. `grades.json` holds the
  graders' structured output, joined to run ids; it was recovered from the workflow journal,
  because the grader agents could not write to `grade/out/`. `f4/grades.json` also holds
  grades for the 5 fatally flagged F4 runs; the PREREG excludes them and the report and verdict
  ignore them.

## The sequence

| # | folder | question | arms | runs | verdict (frozen rule) | key numbers |
|---|---|---|---|---|---|---|
| 1 | [`c1/`](c1/) | Does adding "choices and changes I did not ask for" to `fu:after` disclose more unrequested choices without padding? | A without, B with the clause | 18 | **NOT USEFUL** | disclosure 59 % (29/49) → 91 % (20/22), +32 points, but padding in 3/9 runs > 2/9 allowed |
| 2 | [`ab/`](ab/) | Ship the design draft (A) or the revised text (F)? | A, F | 30 | **SHIP F** (on quadrant coverage) | coverage 0.50 → 1.33 (graded; favours F by construction, since only F names the UK quadrant, and a run with no map scores 0); `fu:before` before the first change 2/12 (A) and 4/12 (F); T1 and W1 0/12 |
| 3 | [`f2/`](f2/) | Does "before anything changes, without stopping" make the map appear first? | F, F2 | 24 | **ADOPT F2** | G 3/12 → 8/12; non-coding W1 0/3 in both; 4 of F2's 8 passes changed nothing |
| 4 | [`f3/`](f3/) | Does "as reply text, not thinking" fix non-coding work? | F2, F3 | 24 | **KEEP F2** | G_W (W1+W2) 0/6 in both; G 5/12 vs 2/12; F3 worse on M3, M4, M6 |
| 5a | [`f4/`](f4/) | Does one pause after `fu:before` ("then end your turn") fix visibility? | F2, F4 | 36 | **INCONCLUSIVE** (missing runs decide it) | G 4/12 vs 7/12 (+5 missing); 8 of 18 F4 runs hit API safeguard stops, 5 fatal |
| 5b | [`f4b/`](f4b/) | F4 without "as visible reply text, not thinking": visibility kept, stops gone? | F4b | 18 | **CONFIRM F4b** | G 11/12, G_W 5/6, completion 11/12; C6 pauses 0/3, J1 pauses 1/3; J1 G 1/3 (that one empty); guards 0 of 11 graded (1 by missing-adverse); safety 1/18 |

## Decisions

1. **C1 removed** from the always-on text. `Decided for you` stays in the skill (omitted when
   there is nothing to report).
2. **F shipped** over the design draft. Both texts showed the map before the first change in
   few runs, so the opening was tested next.
3. **F2 adopted.** Visibility rose on coding tasks; on the non-coding task W1 it stayed at 0 of 3
   in each arm.
4. **F2 kept** over F3. The records show the map announced and then not shown, with edits
   following; thinking content is redacted, so the likely explanation, that the map stayed in
   hidden reasoning, is inferred, not observed. The owner then chose to allow one
   pause before work.
5. **F4 inconclusive.** The pause made the map visible in every present core F4 run (7 of 7:
   T1 x3, T5 x2, W1 x2), but the wording
   "as visible reply text, not thinking" coincided with API safeguard stops
   (`reasoning_extraction`): 10 of 30 runs across the two arms that used such wording, 3 of 30
   without it (per the diagnosis table in `f4b/PREREG.md`; v6f3's non-fatal stop W1-F2-3 is not
   visible in the archived `meta.json`).
6. **F4b confirmed and adopted** by the owner (2026-11-12): F4 with that phrase replaced by
   "show `fu:before` in your reply".

## What these tests do not show

- **The "Go ahead." reply is simulated.** A real person's reply carries answers and
  corrections; here it carried nothing, so completion means "continues after an uninformative
  go".
- **One subject model, 3 runs per task.** Every rule is a screening rule, not a significance
  test. v6f4 and v6f4b ran in different sessions, with no randomisation between them.
- **Grading deviated from the pre-registrations.** Grades came from per-run grader agents in
  the workflow, not from `grade.py`; in v6ab and v6f2 some graders could see arm-revealing
  paths; from v6f3 on most graders reported that the task key was missing from their packets and
  inferred beliefs and expectations from the prompt. G, pauses, completion and safety flags are
  mechanical and unaffected.
- **Nothing here measures learning or understanding**, or anything about a real person's work.
  That is what the own-use week is for: [`../2026-11-12-6.0-own-use/PLAN.md`](../2026-11-12-6.0-own-use/PLAN.md).

## What is archived

Per test: `PREREG.md` (verbatim), `REPORT.md`, `arms/*.md` (verbatim), `runs/<id>/meta.json`
(one per run), `grades.json`, and, where the test had them, `keys.json` and `grader_rubric.md`.

- **`REPORT.md` provenance.** `c1/REPORT.md` is copied from the test directory. The ab, f2,
  f3, f4 and f4b reports are marked **reconstructed** at the top: the report agents could not
  write files, so each was rebuilt from the agent's final message in the workflow journal.
  Their numbers can be recomputed from `runs/*/meta.json`, `grades.json` and the rule in
  `PREREG.md`.
- **Not archived:** event streams, transcripts, final texts, diffs, blinded packets and the
  harness scripts. Script sha256 prefixes are recorded in `f4/PREREG.md` and `f4b/PREREG.md`;
  the c1, ab, f2 and f3 pre-registrations record arm hashes only.
- **Removed from `f4/` and `f4b/` `meta.json`:** the local Claude Code session ids
  (`turn2_rule.session` and `session_ids`); `same_session` is kept. The archive was
  scanned for credentials and tokens before it was added (none found).
