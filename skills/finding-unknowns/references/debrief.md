# Debrief

## Steps

1. Run `fu integrity {slug}`; its three lines go in verbatim.
2. **Grader.** Irreversible lane, measured result, or on request: `mechanism-auditor`
   gets artifact paths and the frozen card (`git show {brief commit}:{card}` plus
   Amendments and deltas file; no Debrief or Model changes), never the transcript or your
   claims. Its verdicts and tiers stand; the reply shows where yours differed. Otherwise:
   `same-context — weaker`.
3. Grade every Brief prediction, the person's first, quoted exactly as frozen. An
   Amendment never removes a miss.
4. Write `mechanism` with its tier. Explain misses only, the person's first, in one line.
5. Card `Model changes`: `- You expected X → it is Y, because Z [shown, not confirmed]`,
   `[confirmed]` once the person confirms; no verdicts or numbers.
6. Append `## Debrief ({time}; graded by fresh context | same-context — weaker)`, fields
   as in `card.md`; set the header `Needs you`; run `fu lint`, `fu log`,
   `fu freeze {slug} --stage debrief`; update Last seen.

## Field rules

- `measured`: its path and only the number the verdict rests on.
- The verb matches the tier: `verified` is or causes; `supported` fits; `inferred` may;
  `untested` opens with "untested:". One hedge per claim. A verdict word is never upgraded:
  `consistent` is not "confirmed".
- `Did NOT prove`: `{check} → leaves open: {part of which claim} · still holds: {…}`.
- Every graded ID appears once in `Bottom line`: `holds` consistent; `did not hold`
  partly, inconsistent; `stops at` can't tell, post-hoc fit.
- The terminal never hides a miss, a fired falsifier, an unlogged hunk or
  `same-context — weaker`.
- A rewrite for clarity changes words only; verdicts, tiers, quotes, numbers and
  `Not checked` stay.

## Reply

Nested lists in this order. Consistent rows: ID line and
`consistent?` only.

```
Evidence:
  - `{command}` → {output, trimmed}
P1 (you · medium) "{quoted}"
  - measured: {value} ({path})
  - consistent?: inconsistent
  - mechanism: {text} [inferred]
Integrity: {three fu integrity lines}
Did NOT prove: {lines}
Not checked: {at least one}
Model changes: {at most five}
Bottom line:
  - holds: {claim} ({IDs})
  - did not hold: {claim} ({IDs}) | none
  - stops at: {boundary} ({IDs})
Needs you: {X} (recommendation: {Y}; settles {Z}) | nothing
```

Add `fu log`'s calibration line when it prints one.

## Rules

- Evidence first; `Needs you` last, stated, not asked. No menu, no further work.
- High-consequence decisions: options under Open; the reply gives one recommendation.
- **No rescue.** A good story explains a miss, never turns it into a hit.
- **Surrender signals**, named once with evidence: a large change approved without a
  question; your own tests as the only evidence for your code; "just tell me" on a
  decision that falls on others.
