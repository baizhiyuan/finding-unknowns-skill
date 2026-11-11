# Examples

Copy-paste prompts for 5.0. Adapt the specifics to your task. The prompts are
illustrative; [A real blind-spot pass (recorded)](#a-real-blind-spot-pass-recorded) is an
actual run. For one card walked end to end, see the [5-minute tutorial](docs/TUTORIAL.md);
for the terms, the [Glossary](docs/GLOSSARY.md).

## Start a brief

```
/fu-brief add a position-sizing rule to the backtest engine; I have never touched the
order-execution path
```

You are asked for your prediction first (it is your prior), then the agent maps the
territory and reports what contradicts it, then gives its own prediction. Ask for a
blind-spot pass explicitly if you want one:

```
/fu-brief migrate the session store from Redis to Postgres. What am I missing? Do a
blind-spot pass against my prior before writing the Brief: I expect the hard part to be
the TTL cleanup job.
```

Nothing is built until you say yes to the Brief and its contract.

## Learn vs ship mode

`ship` by default and never asked; say you want to learn and it is stored in
`.finding-unknowns/profile.md` (personal, not committed). Edit that file, or ask:

```
Switch this project to learn mode: ask me up to three predictions per brief, and on
the rows I get wrong, give me the why with one concrete example.
```

```
Switch this project to ship mode: one skippable prediction question, one-line
explanations.
```

## A research claim with a stopping rule

```
/fu-brief test whether the new tokenizer cuts p95 latency on the bench suite.
Write the prediction card before anything runs: my prediction first, then yours, each
with direction, rough size, where it should show up and where it should not. Measure
the noise floor from at least three reruns of the current tokenizer first. Stopping
rule: 5 seeds per arm, no verdict before all 10 runs are in. If I want a pass/fail
line, explain it in plain words before freezing it.
```

As results arrive over days:

```
Add run 3 to the tokenizer claim's run table: config, what changed, result,
cumulative trials, data spent. One-line note only; no verdict yet.
```

## Resume where you left off

```
/fu-catch-up
```

```
Catch me up on export-resumable. Ask me the recall questions first.
```

With several open cards, `/fu-catch-up` lists them one line each and suggests the most
recently changed.

## Debrief

```
/fu-debrief export-resumable
```

```
Did it match what we expected? Quote each prediction from the frozen card, mine first,
have a fresh subagent grade them from the card and the artifacts, and explain only
the ones that missed. Then the commands you ran with their output, what each check did
not prove, and what nobody checked.
```

For a measured result, the rows follow Theory → Measured → Consistent? → Mechanism, and
the rule verdict stays apart from the verdict on the idea:

```
Is this result consistent with the prediction card? Keep the frozen rule's verdict
(PASS/FAIL/UNCERTAIN) separate from whether the idea is still alive; that second
verdict is mine to make.
```

## A reproducible failure (Debug path)

```
tests/test_dates.py::test_parse_dst fails the same way on every run. Take the Debug
path: the exact repro command and its output, what I expected, at least two competing
explanations before touching the code, one cheapest check per explanation with its
outcome, the fix by path, then the same repro re-run plus one neighbouring case that
should not change.
```

## No install: the passive CLAUDE.md

Copy [`CLAUDE.md`](CLAUDE.md) into a project root, or paste it into your own. It carries
the habits without the commands or agents: ask for your prediction first, stop only at
the four points, grade afterwards and say what each check did not prove. Then work as
usual:

```
Before you start on the CSV importer rewrite, ask me what I expect, then give your own
prediction, and write both under .finding-unknowns/tasks/.
```

## A real blind-spot pass (recorded)

Unlike the prompts above, this one was actually run: recorded 2026-11-10 with
finding-unknowns v4.2.0, by sending a brief directly to the `blindspot-scout` agent, on
[pallets/itsdangerous](https://github.com/pallets/itsdangerous) at commit `672971d`. In
5.0 the same agent serves the blind-spot pass inside `/fu-brief`, and its compact report
has the same shape: Surprises against the person's prior, at most three cited findings, a
rewritten request.

The user's prior was "add a new parameter to Signer and change how signatures are
verified". The scout's first Surprise: the feature already exists. `secret_key` accepts a
list of keys, oldest to newest, and verification tries each one (`signer.py:68-73`,
`:236-240`). The planned patch would have been wasted work on crypto code.

The brief as sent, the verbatim output and the spot-checked citations are in
[docs/recordings/itsdangerous-blindspot.md](docs/recordings/itsdangerous-blindspot.md).
