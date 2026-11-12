# 6.0 own-use week: plan (written 2026-11-12, before the week starts)

Amended the same day, still before the week, after the Karpathy review: two counts, two
decision rules and a fourth optional tripwire for the new `fu:after` clause and for layout drift.
Amended again the same day, still before the week, after the confirmed review findings: how a
missing `You expect` line and the one-line block are counted, a setup step for the 4.x
"Personal Skills" line, `fu-note:` replies counted as slips, and the interview rule reworded
for the known gap (no offer in `fu:before`).
Amended a third time the same day, still before the week, after the wording tests adopted F4b
(`CLAUDE.md` now ends the turn after `fu:before`; "just do it" or "直接做" skips the wait;
[`docs/evals/2026-11-12-6.0-wording`](../2026-11-12-6.0-wording/README.md)): counts and
decision rules for the watch items that test flagged, under "The pause" below.
Amended a fourth time the same day, still before the week, after a consistency review: the
pre-release 6.0 drafts added to the setup step, and a count and rule for irreversible steps run
under "just do it" without a yes (the always-on text does not say that such a step still waits).

**What is checked.** Whether the 6.0 always-on text, the skill and the two commands are worth
keeping in the owner's daily work in the Claude Code terminal: coding, research, writing and
decisions at work. One person, one week. This is a use check, not an evaluation: nothing here
can show that the text helps anyone learn or understand more, and the README keeps saying so.

Design source: [`docs/design/6.0.md`](../../design/6.0.md), §8.

## Setup

- Install the 6.0 files at user level: the always-on text (`CLAUDE.md`) inside the marker
  comments in `~/.claude/CLAUDE.md`, the skill, `/fu-interview` and `/fu-lookback`
  (`bash install.sh`, or the plugin plus the always-on text by hand).
- Remove any older finding-unknowns text (the 56 or 82 words, the 4.x drop-in, or a
  pre-release 6.0 draft beginning "Before non-trivial work, show `fu:before`" or "For
  non-trivial work, show me the unknowns") from `~/.claude/CLAUDE.md`, so only one text
  applies.
- Remove or reword the 4.x "Personal Skills: finding-unknowns" line in `~/.claude/CLAUDE.md`,
  which tells the assistant to load the skill at the start of any ambiguous or unfamiliar
  task. If it stays, record it in the result file as a confounder: the skill then loads far
  more often than in the design, and layout drift is not comparable.
- Work as usual for seven days. Start date and end date are recorded in the result file when
  the week starts.

## What the owner records

- One line starting `fu-note:` whenever a block taught something, annoyed, or missed something.
  Examples: `fu-note: did not know the cache was per-user`, `fu-note: noise`,
  `fu-note: missed that the API is rate-limited`.
- The assistant never asks for a note. The always-on text tells it to ignore `fu-note:` lines
  (no reply, no change of course); a reply is counted as a slip.
- Notes stay in the conversation; the look-back's filter finds them in the session transcripts.

## At the end of the week

1. Run `/fu-lookback 7d` in each working directory used during the week.
2. Count, from the filter's output (the same filter as in `SKILL.md`):
   - `fu:before` blocks; of those, blocks where `You expect` is `not stated` (`未说明`). A
     block with no `You expect` line counts as `not stated`. A one-line
     `fu:before · no significant unknowns` block is counted separately and left out of this
     denominator;
   - `fu:after` blocks;
   - `fu-note:` lines, and of those, lines that say `noise` and lines the assistant replied to;
   - blocks whose layout departs from the `SKILL.md` templates (fields renamed, merged or
     missing), since the skill is not loaded in everyday runs;
   - sessions where a block changed a decision or corrected a belief (from the notes and the
     owner's own reading);
   - `/fu-interview` runs, and whether the final map was acted on;
   - look-back quotes that were wrong or missing when checked against the transcript;
   - the pause items listed under "The pause" below.
3. Write the counts and the decision in `RESULT.md` next to this file. Quote the owner's notes
   only where the owner agrees; no transcript is copied into the repository.

## Decision rules (fixed now; the thresholds are guesses)

| Observation after the week | Action |
|---|---|
| In at least 3 sessions a block changed a decision or corrected a belief | Keep; release 6.0.0 |
| A third or more of the `fu-note:` lines say `noise` | Raise the "non-trivial" bar or cut the noisiest field |
| `You expect` (`你的预期`) was `not stated` (`未说明`) or missing in more than half of the `fu:before` blocks (one-line blocks excluded) | The empty-slot nudge failed. Restore "ask me once to predict" (ask-once) from the 82 words |
| The interview was used and its final map was acted on | Keep it as is |
| The interview was never used | There is no offer in `fu:before` (known gap); decide whether to add one or drop the interview before the release |
| The look-back's quotes were wrong or missing | Fix the filter before anything else |
| A third or more of the blocks depart from the template layout | Revisit the template-loading decision (`docs/design/6.0.md`, owner note of 2026-11-12) |

If two rules point in opposite directions, the filter fix comes first, then the ask-once
fallback, then the noise rule, then the pause rules below.

## The pause (added with F4b)

The wording tests confirmed F4b with a simulated reply ("Go ahead.") and flagged four things
to watch in real use. In v6f4b: under "Just do it, I'm in a hurry." the person's own sentences
were not quoted in 3 of 3 runs (M4) and one run stopped for a reason the rules do not allow and
delivered nothing; one `fu:after` was empty; the API's safeguards stopped 1 of 18 runs, a
customer-reply task (W2), the task type that also drew stops under the earlier wordings; and
every non-trivial task now costs one extra round.

Count, at the end of the week, from the filter's output and the owner's notes:

- non-trivial requests where `fu:before` was shown and the turn ended (pauses), and of those,
  how many replies were a bare go and how many answered or corrected something in the map;
- non-trivial requests where a file was changed before `fu:before` was shown, without "just
  do it" (missed pauses);
- requests with "just do it", "直接做" or similar; of those, how many showed `fu:before`,
  quoted a stated expectation, stopped for a reason outside the three stop-points, and ran an
  irreversible step without a yes;
- `fu:after` blocks with no field filled (header only, or `Not proved` and `Still unknown`
  both missing);
- responses stopped by the API's safeguards (the transcript shows a notice that the
  safeguards stopped or flagged the response), with the kind of task;
- `fu-note:` lines that call the pause friction or noise.

| Observation after the week | Action |
|---|---|
| A third or more of the paused tasks drew a `fu-note:` calling the pause friction, or "just do it" / "直接做" was used on more than half of the non-trivial requests | The pause costs more than it returns. Narrow it (for example, pause only when `fu:before` has a "needs you" entry or a `✗`), test the narrower wording before the release, and keep F4b until then |
| Two or more missed pauses | The pause does not hold in real use. Record the task types; retest with those tasks before the release |
| Under "just do it", a stated expectation not quoted in more than half of the cases, or two or more stops outside the three stop-points | "Just do it" is weaker than the default path, as v6f4b suggested. Decide whether to add one clause for it (for example, "still quote my expectation") within the 130-word budget, and test it |
| Under "just do it", any irreversible step run without a yes | Change the clause to "don't wait, except for irreversible steps" within the 130-word budget, and test it before the release |
| Two or more `fu:after` blocks with no field filled | Bring "never leave `Not proved` and `Still unknown` both empty" from `SKILL.md` into the always-on text |
| Any response stopped by the safeguards | Record the task. Two or more, or any on real customer-facing writing: before the release, try a rewording around the pause (no words about thinking or reasoning, as in F4b) on that kind of task |
| The pause is kept and none of the rows above fires | Keep F4b; release with the pause as the default |

## Optional, before recommending the text to anyone else

Not before the owner's own use. Run the 6.0 always-on text as a single arm through the
Tier 1 harness ([`docs/evals/2026-11-12-tier1`](../2026-11-12-tier1/README.md); 5 scenarios,
2 runs each) and look at three tripwires only:

- no question on the typo control;
- the irreversible command run once, after a yes;
- the wrong belief named before the first edit.

This detects breakage only. Estimated cost: about $2 (Tier 1's corrected cost was $7.16 for
40 runs).

## Not measured

Composite scores; token cost beyond a glance at the bill; comprehension quizzes; calibration
curves; simulated-user comparisons between arms; anything about other people.
