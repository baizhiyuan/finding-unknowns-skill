# Brief

## Questions: one batch

- Read what is established first, `decisions.md` included; never ask what is answered or
  discoverable.
- Ask only what only the person can decide: audience, scope, definition of done,
  preferences. Architecture before behaviour; polish you decide and state.
- Each question: one line of context, two or three options, and your recommendation worded
  so "yes" accepts it. A question whose framing depends on another answer is not asked:
  take the most reversible default and state it in the Brief.
- The prediction ask has no recommendation, options or example answer: they anchor.
- Record each answer in `decisions.md` as `{YYYY-MM-DD} "{their words}" → {what it settles}`.
- Stop asking when the rest is cheaper to find during the build.

## Predictions

- A prediction is a claim about what you do not control: where the bug is, a number, an
  outcome. "The tests will pass" is a contract check.
- Each has a falsifier and a "should not change" half; magnitude and location when honest.
- The person's come first, in their words, in quotes. A confidence they did not give is
  `not given`; it is never inferred.

## The contract

Written before the build, because afterwards any outcome can be rationalised.

- **A check must be able to fail.** "Tests exit 0" and "the diff touches only the planned
  files" are checks; "looks good" and "no errors" are not.
- **`does NOT prove` is mandatory.** If you cannot say what a check would miss, add a
  different check or a human review.
- **Check files are locked.** List them on `Check files:`; the builder does not edit them.
- **Irreversible lane.** One `Irreversible:` line per step, with the exact command. Its
  checks are dry runs (`--dry-run`, plan output, `--sql`); a check that would run the step
  fails `fu lint`. A `post-check` names what closes the item after the one run.

## Explaining

One sentence of why per decision. A principle only when it changes a decision or predicts
something observable. Experts get assumptions and boundaries; newcomers one example and
one causal link.
