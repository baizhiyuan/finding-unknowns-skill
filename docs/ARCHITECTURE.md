# Architecture

How finding-unknowns 5.2 is put together. The [README](../README.md) is the landing page,
the [Glossary](GLOSSARY.md) defines the terms, the [5.2 design](design/5.2.md) gives the
reasons, and the [`fu` contract](design/fu-cli.md) specifies the script. 5.2 has not been
evaluated; whether any of this helps people is untested.

## Four layers

| Layer | Parts | Model cost | Why it exists |
|---|---|---|---|
| **1. Always-on text** | `CLAUDE.md`, 56 words (for Codex, the same words in your own `AGENTS.md`); `CLAUDE.next.md` is an untested 82-word candidate | about 75 tokens per session | The one part Stage 0 measured: +10.5 of 42 over no setup at +$0.08 per task |
| **2. Guard hook + `fu` script** | `hooks/hooks.json` → `scripts/fu.py guard pre\|post`; `scripts/fu.py` (`init`, `lint`, `freeze`, `integrity`, `log`, `list`, `render`) | none to carry; one short Bash call each | The only clear plugin win in Stage 0 (M5, the irreversible step) is a rule code can enforce. The rest is bookkeeping the model used to do by hand |
| **3. Card skill + commands** | `skills/finding-unknowns/SKILL.md` (≤ 700 words) and five references; `/fu-brief`, `/fu-catch-up`, `/fu-debrief`, `/fu-view` (≤ 450 words together, plus the card template inside `/fu-brief`) | loaded only when a card is started or open | The card survives sessions, where phases in a conversation do not. A design argument, not a finding |
| **4. One auditor** | `agents/mechanism-auditor.md` (≤ 500 words) | one subagent call, only when used | Fresh-context grading for an irreversible-lane card, a measured result, or on request. Kept narrow because Stage 0 gave it weak support |

```
commands/        /fu-brief · /fu-catch-up · /fu-debrief · /fu-view    thin; /fu-brief holds the card template
skills/finding-unknowns/
  SKILL.md       the card, the four stop-points, the always-on rules
  references/    card · brief · debrief · results · view, loaded by the phase that needs it
agents/          mechanism-auditor (read-only)
scripts/fu.py    stdlib Python ≥ 3.8; everything deterministic
hooks/hooks.json PreToolUse, PostToolUse, PostToolUseFailure on Bash → fu guard (plugin install only)
bin/fu           optional wrapper for PATH; the skill never relies on it
```

| Part | Role |
|---|---|
| `SKILL.md` | Tools and memory (`fu`, `profile.md`, `decisions.md`), the always-on rules, the quiet build and its four stop-points, the turn-end rule, `/fu-catch-up`, learn and strict modes |
| `references/card.md` | Normative card schema; `fu lint` enforces it. Files, header, Brief lines, deltas, Amendments, Debrief, strict caps, the prediction-log line |
| `references/brief.md` | One batch of questions, predictions, the contract, the irreversible lane |
| `references/debrief.md` | Grading steps, field rules, the reply, no rescue, surrender signals |
| `references/results.md` | Theory → Measured → Consistent? → Mechanism, the run table, the Debug path, the two verdicts |
| `references/view.md` | When to offer the HTML view, and what the page leads with |
| `mechanism-auditor` | Grades every prediction, tiers the mechanism, names an alternative and the cheapest separating check; never given the transcript or the builder's claims |

The commands invoke the skill and name an operation. Every step runs without extras:
without the auditor, grading is labelled `same-context — weaker`; without the script,
Timing is `self-reported` and integrity `not run`; without the hook (an `install.sh`
install, or Codex), the irreversible step needs a chat yes to the exact command.

## Files

Everything the plugin writes is under `.finding-unknowns/`; `.gitignore` is never edited
(`fu init` prints the lines to add, once).

| Path | Written by | Git |
|---|---|---|
| `tasks/{slug}.md` | the model; `State`, `Timing` and the frozen Brief heading by `fu freeze` | committed by `fu freeze` |
| `tasks/{slug}.deltas.md` | the model, append-only; the only place deltas live | committed |
| `predictions/{slug}.md` | the model: a claim file for a measured result | committed |
| `decisions.md` | the model: answers only the person could give, quoted and dated, newest 30 lines (older ones in `decisions-archive.md`) | committed |
| `profile.md` | `fu init` or the model: `mode`, `strict`, `view`, `commits`, `guard` | local |
| `predictions-log.md` | `fu log` only | local |
| `logs/approvals.jsonl`, `logs/guard.jsonl` | `fu guard` | local |
| `view/{slug}.html`, `view/index.html` | `fu render` | local |

## Data flow

```
/fu-brief ──► one batch of questions ──► Brief shown ──► your yes ──► fu freeze --stage brief
                                                                              │
              ┌───────────────────────── quiet build ◄────────────────────────┘
              │   deltas → {slug}.deltas.md
              │   stop-point → fu freeze --stage stop ──► your answer ──► --stage resume
              │   card-named irreversible command → guard asks → runs once → approvals.jsonl
              ▼
completion report = Debrief ──► fu integrity · fu lint · fu log · fu freeze --stage debrief
/fu-catch-up: what changed since Last seen · /fu-debrief: late results, re-grade · /fu-view: fu render
```

1. **Brief.** The agent reads `profile.md`, `decisions.md` and the repository silently.
   One message, at most three questions: the person's prediction and confidence (no
   recommendation, so nothing anchors it) and decisions only the person can make, each
   with a recommended answer. The person's words are quoted verbatim; no answer is
   `P: none given`; the agent never writes a prediction for them. The agent then fills
   the template, runs `fu lint`, shows the Brief and asks once for approval (with the
   view offer for a complex task). On yes, `fu freeze --stage brief` commits the card.
2. **Build.** Quiet. Anything outside the four stop-points takes the most reversible
   option and becomes one delta line; a `decided-for-you` delta states its cost if wrong.
   At a stop, `fu freeze --stage stop` records `Needs you` and the turn ends with
   `Stop ({stop-point}): … · {exact command or decision} · recommend: …`. Every turn ends
   with a completion report or a stop, never a menu or an optional question; the person's
   code is left uncommitted.
3. **Debrief.** The completion report of carded work is the Debrief. `fu integrity`
   prints three lines; the auditor grades when the card has an irreversible lane, a
   measured result, or the person asks; every prediction is graded, the person's first;
   `fu log` appends to the prediction log; `fu freeze --stage debrief` closes the card.
4. **Catch-up.** The named card, else the most recently changed open one: only what
   changed since Last seen, and `Needs you`. Recall questions only on request.

Measured results use a claim file in `predictions/{slug}.md` with a stopping rule and a
run table; no verdict before the stopping rule is met.

## The guard hook

- **Match.** `fu guard pre` reads the hook JSON, collects the `Irreversible:` commands of
  every open card, splits the Bash command into segments (following `sh -c`, `eval`,
  substitutions; dropping wrappers such as `env`, `sudo`, `timeout`), and compares each
  segment with those commands, exactly or as a variant. The card's own dry-run checks
  are exempt.
- **Ask.** On a match with `guard: ask` it returns `permissionDecision: "ask"` with the
  card and command as the reason. The native prompt is the stop-point; the person's
  answer is the per-command yes.
- **Once.** `fu guard post` records each run (failed ones too) in `logs/approvals.jsonl`
  and moves the card from `waiting on you` to `building`. A second attempt asks again
  with "already ran once".
- **Log only.** Generic destructive patterns are recorded as hashes in
  `logs/guard.jsonl`; they ask only under the strict profile.
- **Advisory.** It never denies and fails open. Hard enforcement is a Claude Code
  `permissions.ask` rule for the exact command in user or managed settings. Not yet
  verified: `ask` under bypass-permissions mode, and one live run.

## Stop-points and lanes

1. **Irreversible step:** the exact command on a Brief `Irreversible:` line; its checks
   are dry runs (a check that would run it fails `fu lint`); it runs once; a `post-check`
   closes it.
2. **Scope change** outside the Brief.
3. **Dead premise:** a premise or falsifier fired and no reversible path remains; two
   failed fixes sharing an assumption are logged and the assumption tested; a third
   failure is this stop.
4. **Budget** past the agreed multiple.

Lanes: `reversible` (contained, cheap to undo) · `wide` (undoable, touches shared
surface) · `irreversible` (data rewritten or dropped, deletion, production, money,
publication, commitments to people). Classify upward when unsure.

## Honesty structure

One agent writes both the predictions and the work, so the guards are structural:

- **Frozen predictions.** The Brief is committed before the work and never edited;
  changes go to dated Amendments, and every original prediction is still graded.
  `fu integrity` compares the Brief with its freeze commit.
- **The person's words are theirs.** Quoted verbatim, asked without a suggested answer,
  graded first; the agent never authors them.
- **Predictions vs contract.** A prediction is about what the agent does not control.
  What the agent makes true is a contract check: it must be able to fail, must say what it
  does not prove, and its files are locked against the builder (`fu integrity` reports
  changes).
- **Grading without the builder's claims.** The auditor gets the frozen card and artifact
  paths, never the transcript, the Debrief draft or the builder's verdicts.
- **The evidence stops somewhere.** `Not checked` is never empty; the bottom line names
  where the evidence stops; the verb matches the mechanism tier.

## Design principles

- **The token rule.** The scarce resource is the reader's attention. Spend words on the
  card, delta lines, raw evidence and explanation at the point of error. Text loaded on
  trivial tasks, score tables and announced modes are waste.
- **Code before prose.** A rule that code can check (the irreversible command, the frozen
  Brief, the card schema, the log) goes into the hook or the script, at zero tokens.
- **Fewer turns.** Stage 0's cost was turns and subagent calls, not skill words: the
  5.0 plugin used 10.8 turns and $3.72 per task against 2.2 turns and $0.18 for the 56 words.
- **Evidence honesty.** Every component is kept on design grounds. Docs claim nothing
  beyond the [design](design/5.2.md) and the [evals](evals/).

## Removed in 5.2

Structured mode, Cartographer (the unknowns ledger, regret, clarity scores, the
six-condition gate), the numbered techniques, the full handoff packet, the
`blindspot-scout`, `ledger-keeper`, `prototype-smith` and `quiz-master` agents,
`/fu-cartographer`, the SessionStart hook prototype, recall questions by default and the
457-word passive `CLAUDE.md` of 5.0. The classic line is branch `v4` (v4.3.2, bug fixes
only). The reasons are in [design §2](design/5.2.md#2-cut--keep--add).
