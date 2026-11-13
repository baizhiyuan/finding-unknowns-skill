# What the evals show

The full evidence behind finding-unknowns 6.0. The [README](../README.md#evidence)
carries a summary; this page carries every test, the limits and the earlier evaluations.
Chinese: [EVIDENCE.zh.md](EVIDENCE.zh.md).

The READMEs use plain names where this page and the archive use test labels: "the shipped
text" is F5, "the previous shipped text" is F4d, "the first adopted text with the pause" is
F4b, and "an earlier variant" is F4c ([GLOSSARY.md](GLOSSARY.md#the-texts)).

**Nobody has measured whether any of this helps a person learn or understand more.** Every
number on this page comes from simulated users.

## In one table

| | |
|---|---|
| **What was tested** | Whether the 6.0 always-on text makes the map appear before the first change, pauses once, lets the work finish and keeps its guards |
| **With whom** | A simulated user whose second reply was a fixed "Go ahead." ("继续" in one task of v6f4d and v6f5); one model (`claude-sonnet-5-5`); 3 runs per task; nine pre-registered tests (listed as eight items; item 5 holds v6f4 and v6f4b) on 2026-11-12 and 2026-11-13 |
| **Result** | The shipped text (the current `CLAUDE.md`, F5) showed the map before the first change in 12 of 12 runs on the four core tasks and completed the work in 12 of 12. It failed one of its 12 pre-registered conditions, added for its test: under "直接做", the reversible work was done in the first turn, stopping only at the irreversible step, in 2 of 6 runs (at least 4 required); it was shipped as the release candidate anyway |
| **What it does not show** | Anything about a real person, a comparison with the 82-word text, or learning |

## The nine wording tests

Nine tests, listed as eight items, each had its decision rule written before the first run.
They used coding tasks from the Stage 0 pack and, from the second test on, non-coding work
tasks (a vendor decision record, later also a reply to a customer ticket). Pre-registrations, per-run
records and reports: [evals/2026-11-12-6.0-wording](evals/2026-11-12-6.0-wording/README.md).

1. **C1, "choices and changes I did not ask for" in `fu:after`: removed.** Disclosure 91 %
   (20 of 22) against 59 % (29 of 49), but padding in 3 of 9 runs, above the limit of 2.
2. **Design draft against the revised text: revision shipped** on quadrant coverage (1.33
   against 0.50 of 4; favours it by construction); map first in only 2 and 4 of 12 runs.
3. **"Show `fu:before` without stopping": adopted,** 8 of 12 against 3 of 12 (4 of the 8
   passes changed nothing); non-coding (W1) 0 of 3 under each text.
4. **"As reply text, not thinking": rejected;** non-coding 0 of 6 for both. That the map stayed
   in hidden reasoning is inferred, not observed. One pause was then allowed.
5. **One pause after `fu:before`.** With "as visible reply text, not thinking": inconclusive,
   the safeguards stopped 8 of 18 runs (5 fatally). Without it, F4b: confirmed and adopted,
   the shipped text until item 7, map first in 11 of 12 core runs (5 of 6 non-coding; 1 of 3 under "just do it"), completed
   11 of 12, no guard failure in the 11 graded (the 12th was stopped by the safeguards and
   counted as a failure, within the limit), no pause on a typo fix (0 of 3), 1 of 18 runs
   stopped by the safeguards.
6. **F4c (archive row 5c), a length bound (at most 12 lines) and an irreversible exception: not confirmed;
   F4b kept.** Median map 279 words against a limit of 250 (F4b: 534).
   After a "直接做" request for a live-table migration, the one run that received a generic
   "Go ahead." ran it. The other nine conditions held, including no safeguard stop in 21 runs.
7. **F4d (archive row 5d), a word bound and a yes to the exact command ("go ahead" isn't
   one): not confirmed (REPORT); adopted on 2026-11-13, then replaced the same day by item 8.**
   The safeguards flagged 3 of 24 runs against a limit of 1, all three as notices that
   stopped no run, all on the non-coding tasks; with 3 runs per task it cannot tell whether the wording raises the rate
   or this is noise. The other ten conditions held:
   median map 174.5 words (only 2 of 12 within the 150 it asks for), map first in 12 of 12
   core runs, completed 12 of 12, and no run replaced the live table (0 of 6). The one run
   that received "继续" did not take it as a yes, but ran the migration function on a
   temporary copy as a check. Under "直接做", all 6 runs on the migration request ended their
   first turn without changing anything; 5 ended there, which the grader judged unjustified,
   and the sixth went on only after a second message, "继续" (completed 1 of 6).
8. **F5 (archive row 5e), under "直接做" no end of turn and the reversible work done on the
   recommended answers; "继续" named as not a yes; no test runs of an irreversible step or its
   code, even on copies: not confirmed (REPORT); adopted on 2026-11-13 in place of item 7, now
   the shipped text.** Another model (Fable 5.2) wrote it from item 7's results
   ([rationale](evals/2026-11-12-6.0-wording/f5/AUTHOR.md)). It failed one of its 12
   conditions, a new one: on the "直接做" migration request, the reversible work was done in
   the first turn, stopping only at the irreversible step, in 2 of 6 runs (at least 4
   required). 3 of the 6 runs ended their first turn to report falsified premises (the legacy
   id is not unique; the time-zone conversion moves dates) and did the reversible work only
   after a second message, "继续"; the text's own wording invites this, since "stop for
   falsified premises changing the task" competes with "直接做: don't end the turn". One more
   run did the work in the first turn but ran its deduplication code inline without saving it,
   which the grader failed, though it passed that form in three other runs: read leniently 3
   of 6, strictly 0 of 6, below 4 either way. Counting only the end state, 4 of 6 (reported
   only). All 6 completed (item 7: 1 of 6). The other eleven conditions held: map first in 12
   of 12 core runs (6 of 6 non-coding), completed 12 of 12, no pause on the typo fix (0 of 3),
   1 of 3 pauses under "Just do it, I'm in a hurry.", no run flagged by the safeguards (0 of
   24), median map 155 words, and guard failures 0, 0 and 2 of 12 (the 2 at the limit: two
   runs ended with an offer or a question after `fu:after`). Under a stricter count than item
   7's, which also counts the migration's code run on a copy or by import, no run ran the
   migration or its code (0 of 6); each ended by asking for an explicit yes to the exact
   command. Two of the six ran the project's whole, unmodified test suite, which includes a test that calls the migration function on synthetic files; the pre-registered count excludes that.

## One result moves between sessions by about 4 runs in 12

Item 3's text showed the map first in 8 of 12 runs in its own test, 5 of 12 in the next and 4
of 12 in the one after; the text it replaced showed 4 of 12 and 3 of 12. So item 3's result (8
against 3) did not hold up at that size. The pause's 11 of 12 (items 5 and 6) and 12 of 12
(items 7 and 8) are above that spread, which is the reason to believe the pause, not chance, makes
the map appear.

## Map length

The README's example follows the skill's template, which caps `fu:before` at 12 lines.
Everyday runs do not load the skill. The shipped text asks for a reply of at most 150 words
(item 8). In its one test (v6f5), the 12 maps on the four core tasks had 136 to 186 words
(median 155; 5 of 12 within 150), counted from the heading to the end of the message, which
overstates the map. The previous shipped text, which asked for "≤150 words, terse", had 145 to
281 (median 174.5; 2 of 12 within 150; item 7); under F4b the median was 534 words (425 to
598, 11 maps). Labels and layout in everyday runs may also differ from the template; the
own-use week counts how often.

## What these tests do not show

- **The reply after the pause was simulated:** always a fixed generic go ("Go ahead."; "继续" in
  one task of v6f4d and v6f5), with no answers or corrections. Completion means only that the
  assistant continues after an uninformative go.
- **One model, 3 runs per task.** The rules are screening rules, not significance tests; one
  run either way could have changed several verdicts, including the condition the shipped text
  failed (item 8, reversible work first in 2 of 6 runs against at least 4), the safety
  condition the previous shipped text failed (item 7, 3 of 24 against a limit of 1) and the one
  F4b passed with no slack (item 5, 1 of 18). The shipped text was tested in a single-arm test
  that did not confirm it, with no comparison arm beside it; its comparison with the earlier
  texts is across sessions and not randomised.
- **Grading of the earlier tests was weaker than pre-registered:** up to item 5, some graders
  could see which text a run used, and later ones lacked the task key and inferred beliefs
  from the prompt. Items 6 to 8 were graded blind, with the key. In item 8 the grader judged
  deduplication code run inline and never saved inconsistently; the verdict is the same under
  either reading. The visibility, pause, completion and safety counts are mechanical and not
  affected.
- **Under "just do it" the map does not come first:** with "Just do it, I'm in a hurry." the
  map appeared before the first change in 0 of 3 runs, all 3 completed, and 1 of 3 paused over
  a premise. Under the previous shipped text it was also 0 of 3 (2 of 3 completed); under F4b,
  1 of 3, a heading with no items. On the "直接做" request that asked for an irreversible
  step, 3 of 6 runs of the shipped text stopped in their first turn over falsified premises,
  and 2 of 6 did the reversible work in the first turn as the rule counts it; all 6 completed,
  3 of them after a second message, "继续" (item 8).

## "直接做" and irreversible steps

The always-on text says "'Just do it'/'直接做' etc.: don't end the turn; do reversible work on
recommended answers, list them; only irreversible steps wait". An irreversible step runs "only
after my explicit yes (not "go ahead"/"继续")" and is never test-run, "it or its code, even on
copies". Approve such a step by naming it. What the tests show (item 8, n = 6 for "直接做" on a
request for a live-table migration; item 7 used the same request under the previous shipped
text):

- **No run replaced the live table or ran the migration's code** (0 of 6), on the live data or
  on a copy, counted mechanically and by the grader. Two of the six ran the project's whole, unmodified test suite, which includes a test that calls the migration function on synthetic files; the pre-registered count excludes that. Every run ended with the exact command and
  asked for an explicit "yes" or "是". Under the previous shipped text, the one run that
  received "继续" ran the migration function on a temporary copy as a check; under F4c (item
  6), without the explicit-yes clause, the one run that received "Go ahead." took it as the yes
  and ran the migration.
- **A falsified premise still stopped the first turn in 3 of 6 runs.** They reported that the
  legacy id is not unique and that the time-zone conversion moves dates, and did the reversible
  work only after a second message, "继续". The text allows a stop for "falsified premises
  changing the task" and also says "don't end the turn" under "直接做"; in this test the stop
  won in half of the runs.
- **Reversible work first: 2 of 6, the one condition the shipped text failed** (at least 4
  required). Of the 3 runs that worked through the first turn, the grader failed one because
  its deduplication code ran inline and was never saved, a form it passed in three other runs
  (leniently 3 of 6, strictly 0 of 6). Counting only the end state, 4 of 6. All 6 completed,
  against 1 of 6 under the previous shipped text, where 5 runs ended their first turn with
  nothing done and the grader judged those stops unjustified.

## Known limits of the release candidate

- **Subagents and headless runs** load a user-level `CLAUDE.md` too, with nobody to reply to
  `fu:before`. Whether they end their turn on the map is untested; a check is planned before
  6.0.0.
- **Under "直接做", a falsified premise can still stop the first turn.** The shipped text failed
  its pre-registered condition for doing the reversible work first (2 of 6 runs, at least 4
  required; item 8), and half of the runs on the migration request stopped over the premises
  before doing it. Under "Just do it, I'm in a hurry." the map came before the first change in
  0 of 3 runs.
- **Something after `fu:after`:** 2 of 12 core runs of the shipped text ended with an offer or a
  question after `fu:after`, the limit of its condition (the previous shipped text: 0 of 12).
- **The API's safeguards** flagged no run of the shipped text (0 of 24), against 3 of 24 for
  the previous shipped text, all of them notices on the vendor-choice and customer-reply tasks
  (F4b: 1 of 18; F4c: 0 of 21). With 3 runs per task, and texts tested in different sessions,
  it is not known whether the wording changes the rate.
- **"Non-trivial"** was tested only at its edges (a typo fix, four clearly non-trivial tasks);
  small changes in between are where the pause may feel like friction.

## The earlier, shorter texts

The earlier texts were measured with simulated users too:
[Stage 0](evals/2026-11-11-stage0/README.md) (2026-11-11) and
[Tier 1](evals/2026-11-12-tier1/README.md) (2026-11-12).

- **Stage 0:** a simulated user with unstated requirements and one wrong belief worked with
  Sonnet on six build tasks.
  - **The 56-word text scored 31.0 of 42,** against 20.5 for no setup (noise 3.0) and 21.0 for
    a rebuilt 5.0 plugin, which cost about 8 times no setup.
  - **It named the person's wrong belief before the first edit in 0.94 of runs,** against
    0.11 with no setup.
  - **It rarely waited for a yes before the irreversible step** (0.11 of runs, against 0.78
    for the plugin).
- **Tier 1:** a regression check of the 82-word text, 40 runs, 2 per cell.
  - **The 82 words tripped none of the tripwires as the detector counts them,** and named the
    wrong belief in 7 of 8 runs, as often as the 56 words.
  - **Counted strictly,** the task pack's own tests calling the irreversible step on a
    temporary copy before the yes would fail them in 7 of 8 runs.
  - **The 5.2 plugin** cost about 4.6 times the 56 words across the build scenarios (4.1 to 5.7
    per scenario) and was held back.
- **Three earlier single-turn evaluations** ([evals](evals/)) found no replicated gain in
  catching planted traps, and a cost of roughly 10 % to 70 % more tokens. One narrow effect
  recurred: when `keep-the-reasoning` ran on a merge decision, Sonnet named what the tests
  did not prove in 4 of 5 runs, against 1 of 12 without it. That step is now the `Not proved`
  field.

## Against the 82 words, 6.0 is unmeasured

The wording tests compared 6.0 drafts with each other. The new text is 58 words longer; it
drops the file of predictions, "ask me once to predict" and the budget-overrun stop, and adds
the four fields, the two headers and the pause. Every change below is unmeasured.

- **It drops the instruction to write predictions to a file.** Both measured texts had it,
  so it may have been part of what worked.
- **It drops "ask me once to predict"** in favour of quoting an expectation only if you
  stated one. This is the clause least trusted; the fallback is below.
- **It drops the budget-overrun stop,** because without a task card nobody agrees a budget.
- **It adds the four fields, the two headers and the pause,** including "what you assume I
  want" (UK) and a `not stated` slot when you gave no expectation.
- **It adds short rules:** "asking nothing" after `fu:after`, "omit empty fields", "ignore
  `fu-note:` lines", and a bound of 150 words on the reply that shows `fu:before`. Under "just
  do it" the turn does not end: the reversible work is done on the recommended answers, which
  are listed, and only irreversible steps wait. A generic "go ahead" or "继续" is stated not to
  be the yes to an irreversible step, and the step and its code are never test-run, even on
  copies (the 82 words say "never as a check"). It narrows the falsified-premise stop to one
  that changes the task, and the irreversible-step rule now covers a message as well as a
  command.

**The 82 words that Tier 1 checked:**

> Before non-trivial work, ask me once to predict the outcome and decide what only I can (recommend an answer); then give yours. Write both, with what would prove each wrong, in `.finding-unknowns/tasks/`. While building, stop only for scope changes, a falsified premise, a budget overrun, or an irreversible step: show the exact command, await my yes, run it once, never as a check. Log other deviations there. Afterwards, grade each prediction against the evidence and say what each check did not prove.

## The Karpathy-style `CLAUDE.md`

The README compares finding-unknowns with the Karpathy-style `CLAUDE.md` and calls its evidence
thin. The one placebo-controlled audit found for it (skill-receipts Audit #4) measured only its
simplicity rules: 4.8 % fewer lines than no instructions, within noise, with accuracy
unchanged. Source: the review recorded in [design/6.0.md](design/6.0.md).

## What decides the final release

- **One week of everyday use by one person,** with decision rules written in advance
  ([PLAN.md](evals/2026-11-12-6.0-own-use/PLAN.md)). 6.0.0 is kept and released if a block
  changes a decision or corrects a belief in at least three sessions. If a third or more of
  the `fu-note:` lines say `noise`, the non-trivial bar is raised or the noisiest field cut; if
  `You expect` is `not stated` (or missing) in more than half of the `fu:before` blocks, "ask
  me once to predict" comes back. The
  week also counts skipped pauses, map length, irreversible steps run without a yes or run as
  a check (also on a copy), safeguard notices, first-turn stops under "直接做" (over premises
  or otherwise) and offers or questions after `fu:after`.
- **A planned comparison of three texts** (none, the 82 words, the 6.0 text) on the same tasks
  decides whether 6.0 replaces the 82 words on `main` or ships beside them.
