---
name: finding-unknowns
description: "Use when the user says 'brief me', 'catch me up', 'where were we', 'what am I missing', 'did it match what we expected' or 'is this result consistent'; runs /fu-brief, /fu-catch-up or /fu-debrief; or an open card exists under .finding-unknowns/tasks/. Keeps one task card: predictions frozen before the work, a quiet build with four stop-points, a debrief graded by a fresh context. Not for typos, one-liners or tasks the user says to just do."
aliases: []
metadata:
  credits:
    discovery: "Thariq Shihipar — A Field Guide to Fable: Finding Your Unknowns (https://x.com/trq212/status/2073100352921215386)"
    handoff: "Addy Osmani — Critical thinking when agents do the work (https://x.com/addyosmani/status/2117512471930167377)"
    results: "Theory → Measured → Consistent? → Mechanism, from the author's own research practice (baizhiyuan)"
    cognitive-surrender: "Shaw & Nave, Thinking—Fast, Slow, and Artificial (SSRN 6097646); cognitive debt: Margaret-Anne Storey"
    design: "docs/design/5.0.md, after an advisor review by Fable 5.2"
---

# Finding Unknowns

*Discovery distilled from Thariq Shihipar's "A Field Guide to Fable: Finding Your
Unknowns"; the handoff from Addy Osmani's "Critical thinking when agents do the work".
Community skill; not affiliated with or endorsed by Anthropic.*

<Purpose>
Help the person stay the owner of the work: know what is being done and why, predict
what should happen, see where reality differed and what that changes in their own model.
One Markdown **task card** per task carries this across sessions. Interrupt the person
only at four checkable stop-points; everything else goes on the card for them to read
when they choose. Whether this helps people is untested (see the README); spend words
only where they change a decision or the person's model.
</Purpose>

<Use_When>
- `/fu-brief`, `/fu-catch-up`, `/fu-debrief`, or the phrases in the description
- The person is starting work they will have to stand behind, in territory they or you
  do not know well
- A session starts and `.finding-unknowns/tasks/` holds an open card
- A measured result is planned or comes back (load `references/results.md`)
</Use_When>

<Do_Not_Use_When>
- Typos, one-liners, obvious fixes, lookups: just do them. No card, no question
- The person says "just do it": state the single biggest risk in one line, then proceed.
  An irreversible step still gets the build rule (exact command, a yes for that command)
- Pure option generation with a clear goal: brainstorm directly
</Do_Not_Use_When>

<Always>
- **Territory first.** Never ask what the code, docs or data can answer; look first.
  Never report a fact as absent or "needs device check" without searching: cite the hit
  (say if it is only a draft) or the search that came back empty.
- **Remote targets** (device, server, hosted service): cite the recorded access path
  (host entry, user, route; never key material, no network probe unless asked) or say
  none is recorded. A record can predate a migration: the first step of any plan
  touching the target confirms the login reaches the intended machine.
- **Priors are recorded before checks.** A prior stated later (a follow-up that assumes
  an answer) is checked like the first, inline or with a scoped scout pass. Findings that
  contradict a prior are surprises: list every one, never absorb them.
- **A check must be able to fail**, and each check states what it does NOT prove.
  "Looks good", "no errors" and "the model is confident" are not checks. Checks named in
  the contract are not edited by the implementer.
- **No protocol narration.** Do not announce modes, levels or routing. Show the person
  the card, the question, or the evidence.
- **Short by default.** A Debrief is no longer than a plain answer; detail on request.
- **"No significant unknowns"** and **"no real prediction here"** are valid results.
</Always>

<Steps>

## The card

Path `.finding-unknowns/tasks/{slug}.md`. Template, file layout, gitignore lines and the
commit procedure: `references/card.md`. The frozen Brief is never edited; changes go to
dated, append-only Amendments, and every original prediction is still graded.

## /fu-brief — create and freeze the card

1. **Mode, once per project.** If `.finding-unknowns/profile.md` lacks it, ask `ship` or
   `learn`. Read 4.x files in place (`unknowns-ledger.md`, `unknowns-spec-*.md`,
   `implementation-notes.md`, `predictions/`) and offer once to fold them into a card. If
   `.gitignore` hides `.finding-unknowns/` entirely, offer once to replace that line
   (`references/card.md`); never edit it silently.
2. **The person predicts first.** Ask what they expect, with a confidence: one skippable
   question in ship mode, up to three in learn mode. This is their prior; record it before
   any sweep. Predictions are claims about what you do not control (where the bug is, how
   many callers break, a number, an outcome), each with a falsifier and a "should not
   change" half. Things you make true belong in the contract.
3. **Map the territory.** Use the instruments in `references/brief.md` as the gap
   requires: blind-spot pass (`blindspot-scout` for a real sweep, given the prior so it
   reports Surprises), divergent directions, references, interview, a plan that leads
   with the decisions likely to change. Never ask again for a prior already recorded.
4. **Write the Brief:** approach with a one-line why per decision (more on request), the
   person's predictions and then yours, the four stop-points with this task's budget
   multiple, and the contract (claim · check · does NOT prove · lane). Say that the card
   will be committed; declining is remembered in `profile.md`.
5. **Freeze on the person's yes** to the Brief and its contract. Commit per
   `references/card.md`, then write the Timing line in the header.

## Building — quiet by default

Stop for the person only at these points:

1. **Irreversible action.** Lanes: `reversible` (contained, cheap to undo) · `wide`
   (undoable, touches shared surface) · `irreversible` (data rewritten or dropped,
   deletion, production data, money, external publication, commitments to people).
   Classify upward when unsure; downgrading from `irreversible` needs the person's yes.
   **Build rule:** prepare the exact command; the person runs it or says yes to that
   command (a general "go ahead" is not one); run the contract's post-check before the
   item closes. Confidence never substitutes for the person here.
2. **Scope change:** outside the Brief's approach or contract.
3. **Dead premise:** a Brief premise or a prediction's falsifier fired and no reversible
   path remains. The Amendment is confirmed by the person.
4. **Budget:** overrun past the agreed multiple.

Everything else: take the most reversible option, log a one-line delta
(`deviation | surprise | decided-for-you`, with an evidence pointer), keep going. A dead
premise with a reversible path left gets an Amendment tagged `decided-for-you`, shown at
the next stop. Non-urgent questions wait in Open. Commit the card at each stop
(`references/card.md`). At a session's end, roll the deltas up to three lines on the card
(full lines stay in `{slug}.deltas.md`).

## /fu-catch-up — re-orient without restarting

1. Several open cards: list them one line each and ask which; default the most recent.
   4.x files and no card: offer once to fold them into one.
2. **Recall before showing**, from the deltas and wrong predictions since Last seen: two
   or three questions in learn mode, one skippable in ship mode; a two-sentence
   teach-back counts. `quiz-master` may draft them.
3. Show only what changed after Last seen: state, deltas, Amendments, model changes,
   the next decision that needs the person. Reconcile with the files and runs first;
   never summarise an old summary.
4. Update Last seen.

## /fu-debrief — grade against the frozen card

Read `references/debrief.md`. In short: quote each prediction by ID, never restate it;
a fresh context (`mechanism-auditor`) given the frozen card and artifact paths fills
Measured and Consistent?; you write only the Mechanism with its tier; the person's predictions are
graded first; explanation goes on the rows that missed; evidence block (commands run →
output, what each check did NOT prove, not checked: never empty); model changes marked
`shown, not confirmed` until the person confirms; append to the prediction log; commit.
For measured results, the card's rows use `references/results.md`.

</Steps>

<References>
| File | Load when |
|---|---|
| `references/card.md` | creating, committing or migrating a card |
| `references/brief.md` | running a discovery instrument or writing the contract |
| `references/debrief.md` | `/fu-debrief`, a handoff, recall questions |
| `references/results.md` | a benchmark, backtest, A/B test, training run or reproducible failure; any measured prediction |
| `references/results-examples.md` | an example card is needed |
</References>
