# Debrief

## Steps

1. **Grader.** Irreversible lane, measured result, or on request: `mechanism-auditor`
   gets artifact paths and the frozen card (`git show {brief commit}:{card}`,
   Amendments, deltas file), never the transcript or your claims. Do not grade first:
   its rows, minus `alternative`, are the Debrief rows; its verdicts stand (disagree in one
   line). Otherwise: `same-context — weaker`.
2. Grade every Brief prediction, the person's first, ID line exactly as frozen. An
   Amendment never removes a miss. Explain misses only, one line.
3. Card `Model changes`: `- You expected X → it is Y, because Z [shown, not confirmed]`;
   `[confirmed]` once the person confirms.
4. Append the block below in one write; set the header `Needs you`. Then run
   `fu freeze {slug} --stage debrief` once: it writes `Integrity:`, lints, logs, sets Last
   seen and commits. On a FAIL fix the named lines; rerun.

```
## Debrief ({YYYY-MM-DD HH:MM}; graded by fresh context | same-context — weaker)
Evidence:
  - `{command}` → {output, trimmed}
P1 (you · medium) "{quoted as frozen}"
  - measured: {value} ({path})
  - consistent?: inconsistent
  - mechanism: {text} [inferred]
Did NOT prove:
  - {check} → leaves open: {…} · still holds: {…}
Not checked:
  - {at least one}
Bottom line:
  - holds: {claim} ({IDs})
  - did not hold: {claim} ({IDs}) | none
  - stops at: {boundary} ({IDs})
```

## Field rules

- `measured`: its path and the number the verdict rests on.
- The verb matches the tier: `verified` is or causes; `supported` fits; `inferred` may;
  `untested` opens with "untested:". One hedge per claim. `consistent` is not "confirmed".
- Bottom line: `holds` consistent; `did not hold` partly, inconsistent; `stops at` can't
  tell, post-hoc fit; each graded ID once.
- A rewrite never changes verdicts, tiers, quotes, numbers or `Not checked`.

## Reply

In this order:

```
{one line: what was done}[ · graded by: same-context — weaker]
Missed:
  - P1 (you · medium) "{quoted}" → {measured}; {mechanism} [{tier}]
Held: {IDs} | none
Integrity: {non-clean lines fu printed} | clean
Did NOT prove: {the line that matters most}
Not checked: {items}
Bottom line: {holds · did not hold · stops at}
Needs you: {X} (recommendation: {Y}; settles {Z}) | nothing
```

Add any calibration line `fu freeze` prints. Never hide a miss, a fired
falsifier, an integrity finding or `same-context — weaker`.

## Rules

- `Needs you` last, stated, not asked. No menu, no further work.
- High-consequence decisions: options under Open, one recommendation in the reply.
- **No rescue.** A good story explains a miss, never turns it into a hit.
- **Surrender signals**, named once with evidence: a large change approved without a
  question; your own tests as the only evidence; "just tell me" on others' decisions.
