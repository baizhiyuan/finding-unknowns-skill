# Architecture

How finding-unknowns 5.0 is put together. The [README](../README.md) is the landing page,
the [Glossary](GLOSSARY.md) defines the terms, and the [5.0 design](design/5.0.md) gives
the reasons. Whether any of this helps people is untested.

## Components

```
commands/        /fu-brief · /fu-catch-up · /fu-debrief   thin dispatchers, no procedure
skills/finding-unknowns/
  SKILL.md       the card, the three operations, the stop-points, always-on rules
  references/    loaded only by the phase that needs it
agents/          blindspot-scout · mechanism-auditor · quiz-master   (all read-only)
extras/session-start-hook/   not shipped; pending the Stage 0 evaluation
```

| Part | Role |
|---|---|
| `SKILL.md` | The only skill. Its body holds the rules that must always be loaded; at most 1,500 words |
| `references/card.md` | Card template, file layout, gitignore lines, commit procedure, prediction log |
| `references/brief.md` | Discovery instruments (blind-spot pass, directions, references, interview, plan) and the contract |
| `references/debrief.md` | Grading steps, the default view, surrender signals, recall questions |
| `references/results.md` | Theory → Measured → Consistent? → Mechanism, the run table, the Debug path, the two verdicts |
| `references/results-examples.md` | Example cards and anti-patterns |
| `blindspot-scout` | Reconnaissance for the Brief: Surprises against the person's prior, cited findings, a rewritten request |
| `mechanism-auditor` | Fresh-context grader at `/fu-debrief` and for measured results |
| `quiz-master` | Drafts recall questions for `/fu-catch-up`; flags diff hunks no delta explains. No gate |
| SessionStart hook | Prints each open card's header. Kept in [`extras/`](../extras/session-start-hook/README.md), outside the plugin, until Stage 0 shows it helps |

The commands only invoke the skill and name an operation. Every agent is optional: without
subagents, the skill runs each step inline and labels the grading `same-context — weaker`.

## The task card

All state lives in files, because phases do not survive a session boundary and files do.
Phase changes follow file state, not model judgement: if an open card exists, work
continues from it.

| Path | Content | Committed |
|---|---|---|
| `.finding-unknowns/tasks/{slug}.md` | The card | yes |
| `.finding-unknowns/tasks/{slug}.deltas.md` | Every delta, append-only | yes |
| `.finding-unknowns/predictions/{slug}.md` | Research claim cards and run tables | yes |
| `.finding-unknowns/profile.md` | `mode: ship \| learn`, `commits: yes \| no` | no |
| `.finding-unknowns/predictions-log.md` | One line per graded prediction | no |
| `.finding-unknowns/logs/` | Command output and other detail | no |

A card has a header (goal, state, next decision that needs you, mode, Last seen, Timing),
the frozen **Brief**, append-only **Amendments**, this session's **Deltas**, at most five
**Model changes**, **Open** items and the **Debrief**. The live part stays within about 40
lines. The full template is in
[`references/card.md`](../skills/finding-unknowns/references/card.md).

## Data flow

```
/fu-brief ──► Brief frozen on your yes ──► build (quiet) ──► /fu-catch-up ──► /fu-debrief
  │                                          │    ▲             │             │
  your prediction, territory,                │    └ stop-point ─┘             │
  agent's prediction, contract               deltas → {slug}.deltas.md        graded table,
                                                                              model changes,
                                                                              prediction log
```

1. **Brief.** Mode once per project. The person's prediction comes first, with a
   confidence: it is their prior, recorded before any sweep, so the blind-spot pass can
   report Surprises against it. Then the agent maps the territory (never asking what the
   territory answers) and gives its own prediction. It writes the approach (one line of
   why per decision), both sides' predictions with falsifiers, the stop-points with this
   task's budget multiple, and the contract. On the person's yes the Brief is frozen and
   committed; the hash goes on the Timing line.
2. **Build.** Quiet by default. A reversible choice takes the most reversible option and
   becomes a one-line delta (`deviation | surprise | decided-for-you`) with an evidence
   pointer. The card is committed at each stop; at a session's end the deltas roll up to
   three lines on the card.
3. **Catch-up.** Recall questions first, then only what changed since Last seen, then the
   next decision.
4. **Debrief.** Each frozen prediction is quoted by ID and graded; explanation goes on the
   rows that missed; an evidence block closes it. The card is committed again.

Research claims use a prediction card, a stopping rule and a run table in
`predictions/{slug}.md`; no verdict before the stopping rule is met.

## Stop-points and lanes

Work stops for the person only on conditions checkable against the card:

1. **Irreversible action.** The build rule: the agent prepares the exact command, the
   person runs it or says yes to that command (a general "go ahead" is not one), and the
   contract's post-check runs before the item closes.
2. **Scope change:** outside the Brief's approach or contract.
3. **Dead premise:** a premise or falsifier fired and no reversible path remains.
4. **Budget:** an overrun past the agreed multiple.

Lanes: `reversible` (contained, cheap to undo) · `wide` (undoable, touches shared surface) ·
`irreversible` (data rewritten or dropped, deletion, production data, money, external
publication, commitments to people). Classify upward when unsure; downgrading from
`irreversible` needs the person's yes. Confidence never substitutes for the person on an
irreversible item: this is the irreversibility floor.

## Honesty structure

One agent writes both the predictions and the work, so the guards are structural:

- **Frozen predictions.** The Brief is never edited. Changes go to dated Amendments, and
  every original prediction is still graded. The commit, plus the hash on the Timing line,
  shows the predictions came first; without git, timing is `self-reported`.
- **Predictions vs contract.** A prediction is about something the agent does not control.
  What the agent makes true ("tests pass") is a contract check, which must be able to fail
  and must say what it does not prove.
- **The person predicts first,** unanchored, and is graded first.
- **Fresh-context grading.** `mechanism-auditor` receives the frozen card and the artifact
  paths, never the build transcript, and fills Measured and Consistent?. The builder
  writes only the Mechanism, with its tier.
- **Evidence block.** Commands run and their output, what each check did not prove, and
  "not checked", which is never empty.

## Design principles

- **The token rule.** The scarce resource is the reader's attention. Worth spending on:
  the card, delta lines, raw evidence, explanation at the point of error. Waste: skill
  text loaded on trivial tasks, score tables, a rule stated three times, any sentence that
  changes neither a decision nor the person's model. Hence per-phase references, a
  one-screen Debrief, and no announced modes or levels.
- **Territory before questions.** Never ask what the code, docs or data can answer.
- **Teaching at the point of error.** Depth follows prediction accuracy, not
  self-description: a correct, confident prediction skips the explanation.
- **Evidence honesty.** Every component is kept on design grounds. Three evaluations of
  4.x as a boost to model output found no gain that replicated; the value to people is
  untested. Docs claim nothing beyond the [design](design/5.0.md) and the
  [evals](evals/).

## Removed in 5.0

Cartographer (quadrant routing, the unknowns ledger, regret, clarity scores, the
six-condition gate), Workflow execution, the must-pass quiz, the separate
keep-the-reasoning and theory-vs-result skills (merged into the references),
`ledger-keeper`, `prototype-smith`, and `/blindspot`, `/cartographer`, `/change-quiz`.
They were protocol for the model, not explanation for the person. A blind-spot pass is
still available inside `/fu-brief`. The 4.x content is available at tag `v4.3.2`; the
reasoning is in [design §1 and §9](design/5.0.md).
