# Examples

Real, copy-paste prompts showing `finding-unknowns` in action. Each maps to a technique or to
Cartographer mode. Adapt the specifics to your task.

## Blind-spot pass — entering an unfamiliar codebase

```
I need to add a new position-sizing rule to this backtest engine, but I've never touched
the order-execution path. Do a blindspot pass first: show me the landmines, the hidden
context (invariants I must not break), what "good" looks like here, and the 3-5 questions
an expert would ask before starting. Don't implement yet.
```

## Brainstorm & prototype — "I'll know it when I see it"

```
I want a dashboard for my strategy's drawdown/exposure but I have no visual taste. Make one
HTML file with 4 wildly different layout directions using fake data so I can react before
we wire up anything real.
```

## Interview me — architecture-first, independent questions batched

```
Interview me about this new signal using AskUserQuestion: up to 3 independent questions per
round, but ask dependent questions one at a time. Prioritize questions where my answer would
change the architecture (data model, where it plugs into the pipeline). Stop when you could
write the acceptance criteria yourself.
```

## Reference hunt — point at the real code

```
The factor in factors/MtmMeanBBW.py implements exactly the state-aware smoothing I want.
Read it and reimplement the same semantics for a volume-based factor. Match its conventions.
```

## Implementation plan — lead with the risky decisions

```
Write an implementation plan in HTML. Lead with what I'm most likely to tweak: the schema
changes and any new public interfaces. Put the mechanical refactors at the bottom — I trust
you on those.
```

## Implementation notes — log deviations mid-build

```
As you build this, keep an implementation-notes.md. If an edge case forces you off the plan,
pick the conservative option, log it under 'Deviations', and keep going. Show me the notes
at the end.
```

## Pitch & quiz — before merge

```
Package the spec, the prototype, and the implementation notes into one doc I can share to
get buy-in — lead with the demo. Then give me an HTML report on what changed, with a quiz at
the bottom I have to pass before I merge.
```

## Cartographer mode — high-stakes, full rigor

```
Enter Cartographer mode for this refactor of the equity/PnL accounting.

Maintain unknowns-ledger.md with columns: id, quadrant (KK/KU/UK/UU), unknown,
cost-if-wrong (1-5), P(wrong), regret (=cost×P), reversibility (reversible/wide/irreversible),
prior, status, phase, resolution.

1. Seed it: run a blind-spot pass to populate Unknown Unknowns, then list Known Unknowns
   and any tacit "done means..." criteria.
2. Interview me via AskUserQuestion, up to 3 independent questions per round (dependent
   ones one at a time), always targeting the highest-regret open rows. Re-score P(wrong)
   after each answer. Skip anything with regret < 1.0 — log a conservative default instead,
   except for rows marked irreversible, which always come to me.
3. Show the ledger + four-quadrant coverage checklist each round. Do NOT let me start until
   all four quadrants are probed (especially UU) and no open row has regret >= 1.0.

Keep the ledger open through implementation and build the final merge quiz from it.
```

## Keep the reasoning — at the handoff

```
/keep-the-reasoning the migration plan you just wrote

Before I accept it: triage the stakes, define what "verified" means for this, then give me
the handoff packet. Evidence first, what each check did NOT prove, the decisions and
assumptions you made, and what you did not check.
```

## Theory vs result — report a model evaluation

```
/theory-vs-result the evaluation we just ran: new model vs baseline, 5 training runs each

Report it as Theory → Measured → Consistent? → Mechanism. If no prediction was written
before the run, mark the theory post-hoc. Lead with the metric we actually ship on, give the
run-to-run spread as the noise floor, and tell me which parts held (direction, size, where).
If it is inconsistent, walk pipeline → comparison → metric → theory → environment and name
the broken link and the smallest check. Keep the rule verdict (PASS/FAIL/UNCERTAIN)
separate from whether the idea is still alive, and finish with a non-empty "not checked".
```

## Theory vs result — write the prediction before a benchmark

```
Before I run the cache benchmark, write the prediction card: the claim, the chain of
assumptions (each link that can fail), the expected direction, size and where it should
show up (and where it should not), the noise floor from past reruns, and the result that
would prove us wrong. If I want a pass/fail line, explain it in plain words first: what it
protects against, why that number, and what failing it would mean. Don't freeze it until
I approve.
```
