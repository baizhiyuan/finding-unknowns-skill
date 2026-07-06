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

## Interview me — architecture-first, one question at a time

```
Interview me one question at a time about this new signal. Prioritize questions where my
answer would change the architecture (data model, where it plugs into the pipeline). Stop
when you could write the acceptance criteria yourself.
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
cost-if-wrong (1-5), P(wrong), regret (=cost×P), status, phase, resolution.

1. Seed it: run a blind-spot pass to populate Unknown Unknowns, then list Known Unknowns
   and any tacit "done means..." criteria.
2. Interview me ONE question at a time, always targeting the highest-regret open row.
   Re-score P(wrong) after each answer. Skip anything with regret < 1.0 — log a conservative
   default instead.
3. Show the ledger + four-quadrant coverage checklist each round. Do NOT let me start until
   all four quadrants are probed (especially UU) and no open row has regret >= 1.0.

Keep the ledger open through implementation and build the final merge quiz from it.
```
