# Debrief

The Debrief compares what happened with what the frozen card predicted, and hands the
work back so the person can judge it. One agent wrote both the predictions and the work,
so honesty here is structural, not a promise of self-criticism.

## Steps

1. **Read the frozen card**, its Amendments and its deltas file. Quote each prediction
   by ID, verbatim. Never restate a prediction in new words.
2. **Integrity checks** (the grader runs them):
   - the frozen Brief on the card matches the freeze commit (`git show {hash}:{card}`);
   - the contract's check files are unchanged since the freeze (`git diff {hash} -- {files}`);
   - every diff hunk is explained by a delta, an Amendment or a contract item; any other
     hunk is an **unlogged deviation** and is listed.

   With `timing: self-reported`, say that these checks could not run.
3. **Fresh-context grading.** Give `mechanism-auditor` (or any fresh subagent) the frozen
   card and the paths of the artifacts behind every result: not the build transcript and
   not your conclusions. It fills **Measured** and **Consistent?** for every prediction
   and names, per row, the strongest alternative explanation and the cheapest check that
   would tell them apart. Without subagents, grade it yourself and label the Debrief
   `same-context — weaker`.
4. **Grade the person's predictions first.** Then the agent's.
5. **Write the Mechanism** for each row, with its tier: `verified` (a test that would have
   come out differently if the mechanism were false) · `supported` · `inferred` ·
   `untested`. When the evidence cannot separate a pipeline problem from a wrong idea,
   say so and name the check that would.
6. **Explain at the point of error.** Rows where a prediction missed get the explanation,
   the person's own misses first. In learn mode, a short why with one concrete example;
   in ship mode, one line. A correct, confident prediction needs no explanation.
7. **Model changes:** "You expected X → it is Y, because Z", at most five, each
   `shown, not confirmed` until the person confirms.
8. **Evidence block** (below), then Open: what the person needs to decide.
9. **Append to the prediction log; commit** per `card.md`; update Last seen.

For measured results (benchmarks, backtests, A/B tests, training runs, load tests), the
rows follow `results.md`: verdict labels, the interval rule, the two verdicts.

## Default view

One screen, no longer than a plain answer would be. Detail on request.

```
Evidence: `{command}` → {output, trimmed} · {artifact paths}

| ID | Prediction (quoted) | Measured | Consistent? | Mechanism [tier] |
|----|---------------------|----------|-------------|------------------|

Did NOT prove: {one line per check; flag tests written in the same context as the code}
Not checked: {at least one item; never empty}
Model changes: {at most five lines}
Bottom line: {one line: what holds, what did not}
Needs you: {decisions; recommendation labelled as such}
```

`Consistent?` is one of `consistent · partly · inconsistent · can't tell`; `post-hoc fit`
when the prediction was written after the result was seen.

## Rules

- **Evidence first, summary last.** The commands actually run and their actual output
  come before any prose about them; the bottom line comes after them. A check that was not run is reported as not run.
- **Every check states what it did not prove.** A test written by the context that wrote
  the code can share its mistake and still pass; say when that is the case.
- **"Not checked" is never empty.**
- **High-consequence decisions** (what to build, ship or not, who it affects): two or
  three options with trade-offs and a labelled recommendation. The decision stays with the
  person.
- **No rescue.** An Amendment or a good story explains a miss; it does not turn it into
  a hit.
- **Hit rate.** If the agent's predictions are consistent on nearly every card, they are
  too soft; say so when the log shows it.

## Surrender signals

Name the signal once, plainly, with the evidence; then the person decides. No lectures.

- approval of a large change with no question about any listed decision or unchecked item;
- the agent's own tests offered as the only evidence for the agent's own code;
- "just tell me what to do" on a decision whose consequences fall on other people;
- reasoning from another agent's summary instead of the source.

## Recall questions (`/catch-up`)

Asked before the card is shown, so the person practises recall and a stale Brief shows
up.

- Drawn from the deltas and the wrong predictions since Last seen; `quiz-master` may draft
  them from the card and the diff.
- Learn mode: two or three. Ship mode: one, skippable.
- Application, not vocabulary: "Which workload should benefit least, and why?", never
  "what is the function called?".
- A two-sentence teach-back counts in place of the questions.
- There is no pass mark and no gate. A wrong answer becomes a line under Model changes.

## The prediction habit

Before asking for work, write what you expect. Afterwards, name one thing that was not
checked. The card makes this the default; outside a card, offer it once when the person
asks how to keep their own judgement sharp.
