# The task card

One card per task. The person and the agent both read it; the agent keeps it current.

## Files

| Path | Content | Committed |
|---|---|---|
| `.finding-unknowns/tasks/{slug}.md` | The card | yes |
| `.finding-unknowns/tasks/{slug}.deltas.md` | Every delta, append-only | yes |
| `.finding-unknowns/predictions/{slug}.md` | Research claim cards and run tables (`results.md`) | yes |
| `.finding-unknowns/profile.md` | `mode: ship | learn`, `commits: yes | no` | no |
| `.finding-unknowns/predictions-log.md` | One line per graded prediction | no |
| `.finding-unknowns/logs/` | Command output and other detail | no |

Gitignore lines:

```
.finding-unknowns/logs/
.finding-unknowns/profile.md
.finding-unknowns/predictions-log.md
```

**4.x projects** ignore the whole `.finding-unknowns/` directory, which hides the card.
Offer once to replace that line with the three above. Until the person agrees, cards are
not committed and their Timing reads `self-reported`.

## Template

The live part (header, Deltas, Model changes, Open) stays within about 40 lines. The
frozen Brief and the Debrief are not counted.

```
# {task}
Goal: {one line} · State: {briefing | building | waiting on you | debriefed}
Next decision that needs you: {one line, or "none"}
Mode: {ship | learn} · Last seen by you: {date}, after delta D{n}
Timing: Brief frozen {date}, commit {hash} | self-reported

## Brief (frozen {date})
Approach: {choice} because {one-line why}; {one line per further decision}
Your predictions:  P1 {claim} ({confidence}) · falsifier: … · should not change: …
Agent predictions: A1 {claim} · falsifier: … · should not change: …
  (or: "No real prediction here; contract only")
Stop-points: irreversible action · scope change · dead premise · budget > {k}× {estimate}
Contract:
| claim | check (can fail) | does NOT prove | lane |

## Amendments (append-only)
M1 {date} {what changed in the approach or a premise} · why · {decided-for-you | confirmed}

## Deltas (this session; earlier sessions rolled up)
S1 rollup: {at most three lines}
D7 {date} {deviation | surprise | decided-for-you}: {one line} → {evidence path}

## Model changes (at most five live lines)
You expected X → it is Y, because Z  [shown, not confirmed | confirmed]

## Open
{unchecked items, pending decisions, pending runs}

## Debrief ({date}; graded by {fresh context | same-context — weaker})
| ID | Prediction (quoted) | Measured | Consistent? | Mechanism [tier] |
Evidence: {commands run → output, trimmed} · Did NOT prove: … · Not checked: …
```

## Rules

- **Predictions vs contract.** A prediction is a claim about something the agent does
  not control. "The tests will pass" is a contract check, not a prediction.
- **Every prediction** has a falsifier and a "should not change" half. Magnitude and
  location where they can be honestly given.
- **The person predicts first**, with a confidence, before the agent's prediction is
  shown. "No idea" is a valid answer and is recorded as such.
- **The Brief is never edited after it freezes.** Amendments are dated and append-only:
  - dead premise, no reversible path: a stop; the person confirms the Amendment;
  - dead premise, reversible path: the agent may amend and continue, tagged
    `decided-for-you`, shown at the next stop;
  - every original prediction is still graded. An Amendment explains a miss; it never
    removes one.
- **Deltas** are one line each with an evidence pointer, appended to `{slug}.deltas.md`.
  The card shows the current session's; at a session's end they are replaced on the
  card by a three-line rollup.
- **Last seen** is updated by the agent, only after `/catch-up` or `/debrief` has shown
  the card to the person.
- **Several open cards:** commands accept a slug; without one, list the open cards and
  suggest the most recently changed.
- **Model changes** stay `shown, not confirmed` until the person confirms. An
  explanation delivered is not an explanation understood.
- **Detail goes to `logs/`**; the card holds pointers.

## Committing

The commit hash is evidence of when the predictions were written, which the agent cannot
quietly rewrite later. A squash merge or rewritten history removes it, so the hash and
date also go on the header's Timing line, written after the commit, never inside the
Brief (a hash cannot appear in the commit that produces it, and adding it later would
edit the frozen Brief).

**When:** the Brief freezes; each stop; after the Debrief. Paths: the card, its deltas
file and, for a research claim, `predictions/{slug}.md`.

**Skip checks, run before anything is staged.** Skip the commit, write
`timing: self-reported` and say so in one line when:

- this is not a git repository;
- a path is ignored;
- a merge, rebase or cherry-pick is in progress, or HEAD is detached;
- other changes are already staged (a commit hook could act on the person's work);
- `profile.md` says `commits: no`.

**Commit:**

```
git add -- <paths> && git commit --only -m "chore(card): {brief | stop | debrief} {slug}" -- <paths>
```

- `--only` commits these paths alone; nothing else is staged.
- Never `--no-verify`. If a hook fails or a signing prompt would block, run
  `git reset -q -- <paths>` so nothing is left in the person's index, and fall back to
  `self-reported`.

## Prediction log

After each Debrief, append one line per graded prediction to
`.finding-unknowns/predictions-log.md`:

```
{date} · {slug} · {P1 | A1} · {you | agent} · {consistent | partly | inconsistent | can't tell} · {confidence, if given}
```

The person's hit rate over time is a learning signal. An agent hit rate near 100 % means
its predictions are too soft.
