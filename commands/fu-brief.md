---
description: "Start a task card: you predict first and answer only what only you can decide; the agent predicts, writes the Brief with four stop-points and a contract, and freezes it on your yes."
argument-hint: "<task>"
---

# fu-brief

1. Invoke the `finding-unknowns` skill with the Skill tool; `references/…` paths are
   relative to its base directory.
2. Read `profile.md` and `decisions.md`; look at the repository silently, read-only. An
   open card covering this task: point to `/fu-catch-up`; that is the offer and counts as
   a question. A new card only if the person asks.
3. One message, at most three questions: the person's prediction with its confidence (one
   question, no recommendation), plus decisions only they can make, each recommended
   (`references/brief.md`).
4. Record their words verbatim (`"` as `\"`), or `P: none given`. Then write yours.
5. Fill the template below as `.finding-unknowns/tasks/{slug}.md`; run `fu lint {slug}`
   and fix every FAIL without trimming the person's words (`references/card.md`).
6. Show the Brief. End with one approval ask: open decisions, the view offer for a complex
   task (`references/view.md`), that the card will be committed, and `lint not run` when
   `fu` is missing.
7. On yes: `fu freeze {slug} --stage brief`.
8. Build quietly; the completion report is the Debrief (`references/debrief.md`).

Omit `Irreversible:` and `post-check` when nothing is irreversible.

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
```
