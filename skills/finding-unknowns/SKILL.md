---
name: finding-unknowns
description: "Use on /fu-brief, /fu-catch-up, /fu-debrief or /fu-view; on 'brief me', 'catch me up', 'where were we' or 'did it match what we expected'; or when an open card exists under .finding-unknowns/tasks/. One task card: the person predicts first, a quiet build with four stop-points, every prediction graded. Not for typos or one-liners."
metadata:
  credits:
    discovery: "Thariq Shihipar, A Field Guide to Fable: Finding Your Unknowns (https://x.com/trq212/status/2073100352921215386)"
    handoff: "Addy Osmani, Critical thinking when agents do the work (https://x.com/addyosmani/status/2117512471930167377)"
    results: "Theory → Measured → Consistent? → Mechanism, from the author's research practice (baizhiyuan)"
---

# Finding Unknowns

*After Thariq Shihipar and Addy Osmani (credits above). Community skill; not affiliated
with or endorsed by Anthropic.*

The person predicts, you build quietly, the evidence grades both. One **card**,
`.finding-unknowns/tasks/{slug}.md`, carries the task across sessions.

## Tools and memory

- `fu` means `python3 "{base}/../../scripts/fu.py"`, `{base}` being this skill's base
  directory. Never do by hand what a `fu` subcommand does. If `fu` cannot start,
  say so in one line; Timing is then `self-reported`, integrity and lint `not run`.
- Read `.finding-unknowns/profile.md` and `decisions.md` before the Brief.

## Always

- **Look before asking.** Never ask what code, docs or data answer.
- **Ask only what only the person can decide**, in one batch, each with your recommended
  answer worded so "yes" accepts it. Never re-ask an answer in `decisions.md`; add new ones,
  quoted and dated; past 30 lines, the oldest move to `decisions-archive.md`.
- **Never write the person's prediction.** Quote their words; no answer is `P: none given`.
  The prediction ask carries no recommendation.
- **A check must be able to fail** and says what it does NOT prove. The builder never
  edits check files.
- **No protocol narration.** Short by default; "no real prediction here" is valid.

## /fu-brief

The command holds the procedure and the card template. Show the Brief in full; `fu freeze`
it on the person's yes. The frozen Brief is never edited; changes go to dated Amendments.

## Building: quiet

Stop for the person only at:

1. **Irreversible step**: data rewritten or dropped, deletion, production, money,
   publication, commitments to people; classify upward when unsure. Its exact command is
   on a Brief `Irreversible:` line. Show it; the guard's permission prompt is the yes,
   else (no guard) a chat yes to that exact command ("go ahead" is not one). Run it
   once. Its contract checks are dry runs; nothing re-executes it.
2. **Scope change** outside the Brief.
3. **Dead premise**: a Brief premise or a falsifier fired and no reversible path remains.
   Two failed fixes sharing an assumption: log and test it; a third failure is this stop.
4. **Budget** past the agreed multiple.

Everything else: take the most reversible option and append a delta to
`{slug}.deltas.md` (a `decided-for-you` delta states its cost if wrong). At each stop, run
`fu freeze {slug} --stage stop` and send one line: `Stop ({stop-point}): {what happened} ·
{exact command or decision} · recommend: {answer}`.

**A turn ends** with a completion report or a stop-point request; never an optional
question, a menu, or a request to commit the person's code (leave it uncommitted).

## Completion report = Debrief

When carded work is done, the completion report is the Debrief. `/fu-debrief` is
for late results and re-grading.

## /fu-catch-up

Named card, else the most recently changed open one (say which). Reconcile it with
files and runs; show only what changed since Last seen, and `Needs you`; update Last
seen. Recall questions only on request: two or three, applied, from misses and recent
deltas; no pass mark.

## Modes (profile.md)

- **learn**, only on request: missed rows get a short why and one example, until the
  person predicts that behaviour correctly.
- **strict** (`strict: yes`, when the person says "strict"): fill the template only;
  `fu lint` enforces the caps in `references/card.md` and must pass before the
  Brief-approval ask.

## References

| File | Load when |
|---|---|
| `references/brief.md` | questions, predictions, the contract |
| `references/card.md` | `fu lint` fails; a card written outside `/fu-brief` |
| `references/debrief.md` | the work completes; `/fu-debrief` |
| `references/results.md` | benchmark, backtest, A/B test, training run, reproducible failure |
| `references/view.md` | a complex task's Brief-approval ask; `/fu-view` |
