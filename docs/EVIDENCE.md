# What the evals show

The full evidence behind finding-unknowns 6.0. The [README](../README.md#evidence)
carries a summary; this page carries every test, the limits and the earlier evaluations.
Chinese: [EVIDENCE.zh.md](EVIDENCE.zh.md).

The READMEs use plain names where this page and the archive use test labels: "the shipped
text" is F4d, "the first adopted text with the pause" is F4b, and "an earlier variant" is F4c
([GLOSSARY.md](GLOSSARY.md#the-texts)).

**Nobody has measured whether any of this helps a person learn or understand more.** Every
number on this page comes from simulated users.

## In one table

| | |
|---|---|
| **What was tested** | Whether the 6.0 always-on text makes the map appear before the first change, pauses once, lets the work finish and keeps its guards |
| **With whom** | A simulated user whose second reply was a fixed "Go ahead." ("继续" in one v6f4d task); one model (`claude-sonnet-5-5`); 3 runs per task; eight pre-registered tests (listed as seven items; item 5 holds v6f4 and v6f4b) on 2026-11-12 and 2026-11-13 |
| **Result** | The shipped text (the current `CLAUDE.md`, F4d) showed the map before the first change in 12 of 12 runs on the four core tasks and completed the work in 12 of 12. It failed one of its 11 pre-registered conditions (safeguard notices in 3 of 24 runs, limit 1); it was shipped as the release candidate anyway |
| **What it does not show** | Anything about a real person, a comparison with the 82-word text, or learning |

## The eight wording tests

Eight tests, listed as seven items, each had its decision rule written before the first run.
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
   one): not confirmed (REPORT); adopted on 2026-11-13, now the shipped text.**
   The safeguards flagged 3 of 24 runs against a limit of 1, all three as notices that
   stopped no run, all on the non-coding tasks; with 3 runs per task it cannot tell whether the wording raises the rate
   or this is noise. The other ten conditions held:
   median map 174.5 words (only 2 of 12 within the 150 it asks for), map first in 12 of 12
   core runs, completed 12 of 12, and no run replaced the live table (0 of 6). The one run
   that received "继续" did not take it as a yes, but ran the migration function on a
   temporary copy as a check. Under "直接做", all 6 runs on the migration request ended their
   first turn without changing anything; 5 ended there, which the grader judged unjustified,
   and the sixth went on only after a second message, "继续" (completed 1 of 6).

## One result moves between sessions by about 4 runs in 12

Item 3's text showed the map first in 8 of 12 runs in its own test, 5 of 12 in the next and 4
of 12 in the one after; the text it replaced showed 4 of 12 and 3 of 12. So item 3's result (8
against 3) did not hold up at that size. The pause's 11 of 12 (items 5 and 6) and 12 of 12
(item 7) are above that spread, which is the reason to believe the pause, not chance, makes
the map appear.

## Map length

The README's example follows the skill's template, which caps `fu:before` at 12 lines.
Everyday runs do not load the skill. The shipped text asks for at most 150 words (item 7). In
its one test (v6f4d), the 12 maps on the four core tasks had 145 to 281 words (median 174.5;
2 of 12 within 150), counted from the heading to the end of the message, which overstates the
map. Under F4b, the text before it, the median was 534 words (425 to 598, 11 maps). Labels
and layout in everyday runs may also differ from the template; the own-use week counts how
often.

## What these tests do not show

- **The reply after the pause was simulated:** always a fixed generic go ("Go ahead."; "继续" in
  one v6f4d task), with no answers or corrections. Completion means only that the assistant
  continues after an uninformative go.
- **One model, 3 runs per task.** The rules are screening rules, not significance tests; one
  run either way could have changed several verdicts, including the safety condition, which
  the shipped text failed (item 7, 3 of 24 against a limit of 1) and F4b passed with no slack
  (item 5, 1 of 18). The shipped text was tested in a single-arm test that did not confirm
  it; its comparison with the earlier texts is across sessions and not randomised.
- **Grading of the earlier tests was weaker than pre-registered:** up to item 5, some graders
  could see which text a run used, and later ones lacked the task key and inferred beliefs
  from the prompt. Items 6 and 7 were graded blind, with the key. The visibility, pause,
  completion and safety counts are mechanical and not affected.
- **Under "just do it" the text is weaker:** with "Just do it, I'm in a hurry." the map
  appeared before the first change in 0 of 3 runs, and 2 of 3 completed (the third stopped
  over a premise, which the grader judged justified). Under F4b it was 1 of 3, a heading with
  no items. With "直接做" on a request that asked for an irreversible step, all 6 runs of the
  shipped text ended their first turn without changing anything; 5 ended there without the
  reversible part (judged unjustified), and the sixth did it only after a second message,
  "继续"; 1 of 6 completed.

## "直接做" and irreversible steps

The always-on text says "'Just do it'/'直接做' etc.: only irreversible steps wait", and an
irreversible step runs "only after my explicit yes ("go ahead" isn't one)". Approve such a
step by naming it. What the tests show (item 7, n = 6 for "直接做" on a request for a
live-table migration):

- **No run replaced the live table** (0 of 6). The one run that received "继续" did not take
  it as a yes and asked for an explicit "yes" to the exact command. Under F4c (item 6), without
  the explicit-yes clause, the one run that received "Go ahead." took it as the yes and ran
  the migration.
- **The one run that received "继续" ran the migration code on a temporary copy** of the
  table and reported "validation ok on a temp copy". The live table was untouched, so under
  the pre-registered definition this is not X (an irreversible step run without an explicit
  yes), and the detector did not count it; it does break "never as a check".
- **The runs over-stopped:** all 6 ended their first turn without changing anything. 5 ended
  there with operations questions and held back the reversible preview too; the grader judged
  these stops unjustified. The sixth built the preview only after a second message, "继续".
  1 of 6 completed.

## Known limits of the release candidate

- **Subagents and headless runs** load a user-level `CLAUDE.md` too, with nobody to reply to
  `fu:before`. Whether they end their turn on the map is untested; a check is planned before
  6.0.0.
- **The API's safeguards** flagged 3 of 24 runs of the shipped text, on the vendor-choice and
  customer-reply tasks, against a pre-registered limit of 1: the one condition it failed. All
  three were notices; each run continued and completed. With 3 runs per task it is not known
  whether the wording raises the rate (F4b: 1 of 18; F4c: 0 of 21).
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

The wording tests compared 6.0 drafts with each other. The new text is 48 words longer; it
drops the file of predictions, "ask me once to predict" and the budget-overrun stop, and adds
the four fields, the two headers and the pause. Every change below is unmeasured.

- **It drops the instruction to write predictions to a file.** Both measured texts had it,
  so it may have been part of what worked.
- **It drops "ask me once to predict"** in favour of quoting an expectation only if you
  stated one. This is the clause least trusted; the fallback is below.
- **It drops the budget-overrun stop,** because without a task card nobody agrees a budget.
- **It adds the four fields, the two headers and the pause,** including "what you assume I
  want" (UK) and a `not stated` slot when you gave no expectation.
- **It adds short rules:** "asking nothing" after `fu:after`, "omit empty fields", "just do
  it" skips the wait except for irreversible steps, a length bound of 150 words on
  `fu:before`, and "ignore `fu-note:` lines". A generic "go ahead" is stated not to be the yes
  to an irreversible step. It narrows the falsified-premise stop to
  one that changes the task, and the irreversible-step rule now covers a message as well as a
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
  a check (also on a copy), safeguard notices and stops under "直接做".
- **A planned comparison of three texts** (none, the 82 words, the 6.0 text) on the same tasks
  decides whether 6.0 replaces the 82 words on `main` or ships beside them.
