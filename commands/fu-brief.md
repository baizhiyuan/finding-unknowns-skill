---
description: "Start a task card: you predict first and answer only what only you can decide; the agent predicts, writes the Brief with four stop-points and a contract, and freezes it on your yes."
argument-hint: "<task>"
---

# fu-brief

1. Invoke the `finding-unknowns` skill with the Skill tool; `references/…` paths are
   relative to its base directory.
2. Read `profile.md` and `decisions.md`; look at the repository silently, read-only. If an
   open card covers this task, say so and point to `/fu-catch-up`.
3. One message: ask the person's prediction and confidence (no recommendation), plus the
   decisions only they can make, each with your recommendation (`references/brief.md`).
   At most three questions.
4. Record their words, quoted, or `P: none given`. Then write your predictions.
5. Fill the template below as `.finding-unknowns/tasks/{slug}.md`; run `fu lint {slug}`
   and fix every FAIL (strict: it must pass).
6. Show the Brief in the reply. End with one approval ask: open decisions, the view offer
   for a complex task (`references/view.md`), and a note that the card will be committed.
7. On yes: `fu freeze {slug} --stage brief`.
8. Build quietly (the skill's stop-points); the completion report is the Debrief
   (`references/debrief.md`).

Omit `Irreversible:` and `post-check` when nothing is irreversible; fill the Debrief
section only at the end.

```markdown
# {slug}
Goal: {one line} · State: briefing
Needs you: {decision} (recommendation: {answer}; settles {what}) | nothing
Mode: {ship | learn} · Last seen by you: never
Timing: draft

## Brief (draft)
Approach:
  - {decision} because {one-line why}
P1 (you · {low | medium | high | no idea | not given}) "{their words, verbatim}"
  - falsifier: {the result that would prove it wrong}
  - should not change: {where no effect should appear}
A1 (agent · {low | medium | high}) "{your claim}"
  - falsifier: {…}
  - should not change: {…}
Stop-points: irreversible · scope · dead-premise · budget > {k}× {estimate}
Irreversible: `{exact command}`
C1 {claim}
  - check: `{command that can fail}`
  - does NOT prove: {what it would miss}
  - lane: {reversible | wide | irreversible}
  - post-check: {what closes it after the one run}
Check files: {paths | none}

## Amendments

## Deltas
Latest: none
Rollup:

## Model changes

## Open

## Debrief ({time}; graded by {fresh context | same-context — weaker})
Evidence:
  - `{command}` → {output, trimmed}
P1 (you · {confidence}) "{identical to the Brief line}"
  - measured: {the number the verdict rests on} ({path})
  - consistent?: {consistent | partly | inconsistent | can't tell | post-hoc fit}
  - mechanism: {verb matched to tier} [{verified | supported | inferred | untested}]
Integrity:
  - {the three fu integrity lines}
Did NOT prove:
  - {check} → leaves open: {…} · still holds: {…}
Not checked:
  - {at least one item}
Bottom line:
  - holds: {claim} ({IDs})
  - did not hold: {claim} ({IDs}) | none
  - stops at: {boundary}
```
