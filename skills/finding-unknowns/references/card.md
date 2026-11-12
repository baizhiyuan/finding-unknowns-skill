# Card schema

Normative. The fill-in template is in `/fu-brief`; `fu lint` enforces this file. **FAIL**
blocks `fu render` and, under strict, the Brief-approval ask; **WARN** renders with a chip.
One format everywhere: lines with fixed keys in a fixed order, nested lists, no tables.

## Files under `.finding-unknowns/`

- `tasks/{slug}.md`: the card · committed by `fu freeze`
- `tasks/{slug}.deltas.md`: every delta, append-only, the only place deltas live · committed
- `predictions/{slug}.md`: a claim file (`results.md`) · committed
- `decisions.md`: answers only the person could give, at most 30 lines · committed
- `profile.md`: `mode: ship | learn` · `strict: no | yes` · `view: yes | no` (absent until
  offered) · `commits: yes | no` · `guard: off | log | ask` (default `ask`) · local
- `predictions-log.md`: written by `fu log` only · local
- `logs/`, `view/`: command output, guard records, HTML · local

Gitignore lines: `.finding-unknowns/logs/`, `.finding-unknowns/view/`,
`.finding-unknowns/profile.md`, `.finding-unknowns/predictions-log.md`.

## Card

Times are `YYYY-MM-DD HH:MM`, local. Header, five lines in this order:

```
# {slug}
Goal: {one line} · State: {briefing | building | waiting on you | debriefed}
Needs you: {X} (recommendation: {Y}; settles {Z}) | nothing
Mode: {ship | learn} · Last seen by you: {time}, after D{n} | never
Timing: draft | Brief frozen {time}, commit {hash} | self-reported
```

- `Needs you` exists once, here; the Debrief updates it (FAIL if twice). `Timing` and the
  Brief heading's time are written by `fu freeze`.
- Sections in order: `## Brief (draft)` or `## Brief (frozen {time})`, `## Amendments`,
  `## Deltas`, `## Model changes`, `## Open`, `## Debrief (…)`.
- The live part (header to Open) stays within 40 lines (WARN); a new line first replaces
  the line it supersedes.

**Brief lines** (FAIL unless noted):

- `Approach:` then `  - {decision} because {why}`.
- Prediction: `{ID} ({you | agent} · {confidence}) "{claim}"`, then `  - falsifier: …` and
  `  - should not change: …`. `P{n}` is the person's and must be quoted; `A{n}` is the
  agent's. No answer: exactly `P: none given`. Confidence: `low | medium | high | no idea |
  not given`.
- `P{n}`/`A{n}` name predictions only. Every one cited anywhere is defined in the Brief;
  premises are named in words.
- `Stop-points: irreversible · scope · dead-premise · budget > {k}× {estimate}`.
- ``Irreversible: `{exact command}` ``, one line per irreversible step.
- Contract item `C{n} {claim}`, then `  - check: …`, `  - does NOT prove: …`,
  `  - lane: reversible | wide | irreversible`; an irreversible item adds `  - post-check: …`.
  A check containing an `Irreversible:` command fails. Lanes: `reversible` contained and
  cheap to undo; `wide` undoable but touches shared surface; `irreversible` as SKILL.md.
- `Check files: {paths} | none`.

**Deltas file**, one line each:
`D{n} {time} {deviation | surprise | decided-for-you}: {text} → {evidence path}`, then
` · cost if wrong: {text}` (required on `decided-for-you`), then optional
` [stop: irreversible | scope | dead-premise | budget]`. A `D{n}` line inside the card
fails; a missing `HH:MM` warns. The card's `## Deltas` holds `Latest: D{n}` and
`Rollup:` with at most three lines.

**Amendment**: `M{n} {time} · after D{n} · {decided-for-you | confirmed}: {what changed} ·
why: {text}`. No `after D{n}`: WARN.

**Model changes**: `- You expected X → it is Y, because Z [shown, not confirmed |
confirmed]`, at most five, in this section only (WARN elsewhere).

**Debrief** (a re-grade appends another; `fu log` reads the last): heading
`## Debrief ({time}; graded by fresh context | same-context — weaker)`, then `Evidence:`, every Brief prediction (P before A, ID line identical to the Brief) with
`  - measured:`, `  - consistent?: consistent | partly | inconsistent | can't tell |
post-hoc fit`, `  - mechanism: {text} [verified | supported | inferred | untested]`; then
`Integrity:` (three lines), `Did NOT prove:`, `Not checked:` (at least one item),
`Bottom line:` with `  - holds:`, `  - did not hold:`, `  - stops at:`. IDs under `holds`
are `consistent`; every `partly` or `inconsistent` ID is under `did not hold`. WARN: a
mechanism verb stronger than its tier; "all", "every" or "works" under `holds` while a row
missed.

## Strict caps (FAIL under `strict: yes`)

Card at most 600 words; at most 3 predictions per side; at most 5 contract items; at most
20 words per field; live part at most 40 lines.

## Prediction log line

`{YYYY-MM-DD} · {slug} · {ID} · {you | agent} · {consistent?} · {confidence}`
