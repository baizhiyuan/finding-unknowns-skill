# Brief instruments

Use the instrument the gap needs; most briefs need one or two, not all. The kinds of gap
(internal vocabulary, not announced to the person):

| | The person knows it is a gap | The person does not |
|---|---|---|
| **They know the answer** | written down in the Brief | taste they will recognise → directions, references |
| **They don't** | nameable question → interview, plan | blind spot → blind-spot pass |

Every instrument starts from the territory and ends at understanding. None of them slides
into implementation.

## Blind-spot pass

Delegate to `blindspot-scout` for a real codebase or domain sweep; run inline for small
cases.

1. Goal, the person's experience level (infer conservatively), and the prior already
   recorded in the Brief (never ask for it again; if none was given, infer one and say
   so).
2. Explore first: the module, tests, git history, conventions, prior art; for an external
   domain, what practitioners treat as table stakes.
3. Report compactly, at most about 25 lines plus Surprises:
   - **Surprises:** every finding that contradicts the prior, or "prior consistent with
     the territory". Never capped.
   - **Top findings,** at most three, ranked by blast radius, each cited. Fewer when
     fewer matter.
   - **Rewritten request:** the request upgraded by what was found.
4. The full five-section report (Landmines, Hidden context, What good looks like,
   Questions you should be asking with best-guess answers, Rewritten request) only on
   request.

## Divergent directions (for taste the person will recognise)

1. Gather real material (data samples, constraints, references) so options are concrete.
2. Produce several genuinely different directions (default 3–4): different structures,
   framings or interaction models. Variations on one idea do not count.
3. One self-contained artifact (`.finding-unknowns/prototypes/{slug}.html` for
   visual work, Markdown otherwise), each direction with a one-line thesis and what it
   optimises for and gives up. Fake every backend; never touch the real application.
4. Three to five reaction prompts inside the artifact that help the person say what
   they like. They are not questions that need answers before building and do not count
   toward the /fu-brief question limits.

Convert the reactions into explicit criteria in the Brief before any real code.

## References

1. The person points at the reference and names the property they want: semantics,
   structure or feel.
2. Read the implementation itself, not a summary.
3. Extract what transfers (behaviour, invariants, structure) and say what will not
   (idioms, dependencies, scale assumptions).
4. Confirm the extraction before reimplementing. If the reference conflicts with the host
   codebase's conventions, say so; do not pick silently.

## Interview

The default flow allows two asks before the Brief: the first message (the person's
prediction plus any choice the repository cannot answer: audience, out of scope,
definition of done, business preferences; at most three questions), and after the sweep
at most one bundled follow-up. Structured mode follows its own interview and ledger
rules (`structured.md`, `cartographer.md`).

1. Read everything established; never ask what is answered or discoverable.
2. Sort open questions by blast radius: architecture first (data model, interfaces,
   approach), then behaviour (edge cases, failure modes, defaults), polish last
   (propose and move on).
3. Ask with clickable options when the host offers them: up to three **independent**
   questions in the follow-up, each with the context that makes it matter, two or three
   concrete options and your recommendation. A question whose framing depends on another
   answer is not asked: take the most reversible default and state it in the Brief.
   "You decide" is an answer you then own.
4. If an answer contradicts an earlier decision, say so at once.

Stop when the remaining unknowns are cheaper to find during the build than to ask about,
and say so.

## A plan that leads with the decisions likely to change

Reviewable in minutes. It puts expensive-to-change decisions in front of the person
while changing them is free.

1. Three lines: what is being built, the approach, the riskiest assumption.
2. **Decisions likely to change** (data model, interfaces, anything user-facing): the
   choice, one alternative, the cost of changing later.
3. **Known unknowns and their defaults:** the default taken and the signal that would
   trigger a pivot.
4. The contract (below).
5. Mechanical work last, compressed.
6. End with the two to four decisions that need a yes, a no or a pick.

## The contract

Written before the build, because afterwards any outcome can be rationalised.

| claim | check (what runs) | does NOT prove | lane |
|---|---|---|---|

- **A check must be able to fail.** "Tests exit 0", "every claim carries a source line"
  and "the diff touches only the planned files" are checks. "Looks good", "the model is
  confident" and "no errors were raised" are not.
- **The "does NOT prove" column is mandatory.** If you cannot say what a check would
  miss, the claim needs a second, different check or a human review.
- **Checks are locked against the implementer.** Name the check files in the contract;
  the implementing context does not edit them. A test written with the same mistake as
  the feature passes.
- **Irreversible-lane checks are safe dry-runs** (plan output, `--sql`, `--dry-run`);
  anything that would perform the irreversible action is a post-check, never a contract
  check.
- **Irreversible-lane claims name their post-check:** what runs after the person executes
  the command, and what result closes the item.
- The person approves the contract with the Brief.

## Explaining in the Brief

- One sentence of "why" per decision; more only on request.
- Explain a principle only when it changes a decision or predicts something observable.
  Example: "Caching helps repeated requests. Your keys include session IDs, so repeats
  across sessions may miss. We'll measure the hit rate before predicting the latency
  gain."
- Experts get assumptions and boundary conditions; newcomers get one concrete example and
  one causal link. Prediction accuracy, not self-description, decides which over time.
