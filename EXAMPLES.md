# Examples

Copy-paste prompts for 5.2. Adapt the specifics to your task. The prompts are
illustrative; [A real blind-spot pass (recorded)](#a-real-blind-spot-pass-recorded) is an
actual run from 4.x. For one card walked end to end, see the
[5-minute tutorial](docs/TUTORIAL.md); for the terms, the [Glossary](docs/GLOSSARY.md).

## No plugin: the 56 words

Append [`CLAUDE.md`](CLAUDE.md) to `~/.claude/CLAUDE.md` (see the
[README](README.md#recommended-setup-56-words)). Then work as usual; the assistant asks for
your prediction first. To be explicit on one task:

```
Before you start on the CSV importer rewrite, ask me what I expect, then give your own
prediction, and write both under .finding-unknowns/tasks/ with what would prove each wrong.
```

## Start a brief

```
/fu-brief add a position-sizing rule to the backtest engine; I have never touched the
order-execution path
```

You get one message with at most three questions: your prediction first, with no
suggested answer, then decisions only you can make, each with a recommendation. Answer in
one reply; "yes" accepts the recommendations. Nothing is built until you approve the
Brief.

Saying what you already believe helps the agent check it:

```
/fu-brief migrate the session store from Redis to Postgres. My prediction: the hard part
is the TTL cleanup job, medium confidence.
```

## An irreversible step

Name it, so the Brief gets an `Irreversible:` line with the exact command:

```
/fu-brief regenerate build/quotes.json and publish it with `python publish.py
build/quotes.json`. Publishing can only happen once.
```

The contract's checks for that step are dry runs (`--dry-run`, plan output). With the
plugin's guard hook, Claude Code asks you before the exact command runs, and asks again if
anything tries to run it a second time. With `install.sh` (no hook), the agent stops and
waits for your chat yes to that exact command.

For enforcement the agent cannot edit, add a permission rule to your user settings
(`~/.claude/settings.json`):

```json
{ "permissions": { "ask": ["Bash(python publish.py build/quotes.json)"] } }
```

## Learn mode and the strict profile

`ship` by default and never asked. To learn:

```
Switch this project to learn mode: on the predictions I miss, give me a short why with
one example.
```

For a small or open-weight model, turn on the strict profile (template only, lint caps,
destructive commands ask):

```
Use the strict profile for this project.
```

or, from your project's directory, run `fu init --strict` (with the repository's `bin/fu`
on your `PATH`).

## A research claim with a stopping rule

```
/fu-brief test whether the new tokenizer cuts p95 latency on the bench suite.
My prediction first, then yours, each with direction, rough size, where it should show
up and where it should not. Measure the noise floor from at least three reruns of the
current tokenizer first. Stopping rule: 5 seeds per arm, no verdict before all 10 runs
are in.
```

As results arrive over days:

```
Add run 3 to the tokenizer claim's run table: config, what changed, result, cumulative
trials. One-line note only; no verdict yet.
```

## Resume where you left off

```
/fu-catch-up
```

With several open cards it takes the most recently changed one and says which in one
line. To see them all:

```
Show me every open card.
```

## Views

```
/fu-view                # the most recently changed card as a local HTML page
/fu-view --list         # every card, with your calibration as a stat line
```

## Debrief

Carded work ends with the Debrief as its completion report. For results that arrive
later, or a second look:

```
/fu-debrief export-resumable
```

```
Re-grade export-resumable with a fresh subagent: the frozen card and the artifacts only,
mine first, and keep the earlier Debrief.
```

For a measured result, keep the two verdicts apart:

```
Is this result consistent with the prediction? Keep the frozen rule's verdict
(PASS/FAIL/UNCERTAIN) separate from whether the idea is still alive; that second verdict
is mine.
```

## A reproducible failure (Debug path)

```
tests/test_dates.py::test_parse_dst fails the same way on every run. Take the Debug
path: the exact repro command and its output, what I expected, at least two competing
explanations before touching the code, one cheapest check per explanation with its
outcome, the fix by path, then the same repro re-run plus one neighbouring case that
should not change.
```

## A real blind-spot pass (recorded)

Unlike the prompts above, this one was actually run: recorded 2026-11-10 with
finding-unknowns v4.2.0, by sending a brief directly to the `blindspot-scout` agent, on
[pallets/itsdangerous](https://github.com/pallets/itsdangerous) at commit `672971d`. The
agent is not part of 5.2 (it remains on branch `v4`): in 5.2 the agent reads the
repository silently before the Brief, and Claude Code's own explorer covers larger
sweeps.

The user's prior was "add a new parameter to Signer and change how signatures are
verified". The scout's first Surprise: the feature already exists. `secret_key` accepts a
list of keys, oldest to newest, and verification tries each one (`signer.py:68-73`,
`:236-240`). The planned patch would have been wasted work on crypto code.

The brief as sent, the verbatim output and the spot-checked citations are in
[docs/recordings/itsdangerous-blindspot.md](docs/recordings/itsdangerous-blindspot.md).
