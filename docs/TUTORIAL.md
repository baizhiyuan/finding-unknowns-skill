# 5-minute tutorial

For anyone new to the plugin: install it, then try each of the three skills once on
something real. Every prompt below is copy-paste. Your output will be worded differently
from the samples; the *shape* is what to check. [中文版](TUTORIAL.zh.md)

## Install (1 minute)

Inside a Claude Code session, enter these one at a time:

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

You now have three skills, five agents and three slash commands (`/blindspot`,
`/cartographer`, `/change-quiz`). The three skills are invoked directly as
`/finding-unknowns`, `/keep-the-reasoning` and `/theory-vs-result`, because Claude Code
exposes skills as slash commands. Other install routes are in the
[README](../README.md#quick-start). Files the skills write go under `.finding-unknowns/` in
your project; it is working state, so add `.finding-unknowns/` to `.gitignore`. To review
the ledger and specs in PRs instead, use the three-line form in the
[README](../README.md#commands) (git cannot re-include a file inside an ignored directory).

## Exercise 1: a blind-spot pass on a repo you don't know (2 minutes)

The point: before you change unfamiliar code, find out what you don't know you don't know.
Use a small public library:

```bash
git clone https://github.com/pallets/itsdangerous.git
cd itsdangerous && git checkout 672971d   # the commit the recorded run used
claude
```

Then, in Claude Code, state your goal *and* your prior (what you expect the answer to be):

```
/blindspot I'm a grad student new to this library. I want to add secret-key rotation to
itsdangerous so our Flask app can change its SECRET_KEY without logging everyone out.
Where should I start?
Prior: I think I'll need to add a new parameter to Signer and change how signatures are
verified.
```

What you should get back, in this order:

1. **Surprises**: where the code contradicts what you expected. Here, the
   feature already exists: `secret_key` accepts a list of keys, oldest to newest.
2. **Top findings**: at most three, ranked by blast radius, each citing `file:line`. Claims
   about things the scout could not see (Flask, your app) carry a confidence label.
3. **Rewritten request**: your request, upgraded by what was found. Use it as your next
   prompt.

Compare yours with the [recorded run](../EXAMPLES.md#a-real-blind-spot-pass-recorded). No
citations, or no Surprises section although you gave a prior, means something went wrong.

## Exercise 2: keep the reasoning when a change comes back (1 minute)

The point: accepting agent work without quietly giving up your judgment. Exercise 1 found
that rotation already works at the signer level, and `test_secret_keys`
(`tests/test_itsdangerous/test_signer.py:94-102`) already covers it: a `Signer(["a", "b"])`
validates a value signed with `"a"`. Your Flask app, however, signs its session with a
`URLSafeTimedSerializer`, and no test in `test_serializer.py`, `test_timed.py` or
`test_url_safe.py` builds a serializer from a key list (their fixtures all pass one string
key). So test that layer. First set up the clone, in a virtual environment:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -e . pytest freezegun   # freezegun: test_timed.py imports it
```

Then let Claude make one small change:

```
Add a test that a URLSafeTimedSerializer token signed with secret_key="old" still loads
after the serializer is rebuilt with secret_key=["old", "new"]. Do not modify the library.
```

Then ask for the handoff, saying where the change is going:

```
/keep-the-reasoning the test you just added — it goes into a PR to the shared repo
```

The skill first picks a **packet size** from the stakes: `offload` (one line), `compact`
or `full`. Where the change goes decides it. A test that stays in your private clone is
cheap to be wrong about and lands only on you, so it would be `offload`. A PR to the shared
repo lands on others but is reversible and runs behind CI, so it is medium stakes and gets
the compact packet: evidence first, summary last.

```
Packet size: compact — new test in a PR to a shared library, reversible, behind CI.
Evidence           — the commands actually run and their real output
                     (e.g. `pytest tests/test_itsdangerous -q` → N passed)
What the checks did NOT prove
                   — e.g. that a real Flask session cookie survives rotation
Not checked        — at least one thing nobody verified. Never empty.
Prior vs result    — your Exercise 1 prior (a new Signer parameter would be needed)
                     against what came back (key lists already work)
Summary            — last, and short.
```

The Prior vs result line appears because Exercise 1 recorded a prior; without one the
compact packet has only the other four sections. Read "What the checks did NOT prove"
first. If it claims the checks proved everything, push back.

## Exercise 3: theory vs result (1 minute)

The point: write the expectation before you look at the number, so the number can
disagree with you. Two shapes.

**(a) A measurement: predict before you run.** The skill picks a **rigor level** (`note`,
`report` or `decision`) from what rides on the result.

```
/theory-vs-result I'm about to benchmark verify_signature with 1 key vs 3 keys in the list.
Write the prediction card first: direction, rough size, where it should show up (valid
token signed with the newest key vs an invalid token), the noise floor, and the result
that would prove me wrong. Stop before I run anything.
```

Expect a prediction card (Claim, Mechanism chain, Prediction, Noise floor, Falsifier,
Written ...) and nothing else yet. After the run, ask again with the numbers and you get a
Theory → Measured → Consistent? → Mechanism card.

**(b) A failing test: the Debug path.** A failure that reproduces every time has no noise
floor, so it takes the lighter Debug path instead of a rigor level. To practise, break the
test from Exercise 2 on purpose: rebuild the serializer with `secret_key=["new"]` alone (the
old key is retired too early), run it, and then:

```
/theory-vs-result the key-rotation test fails the same way on every run. Take the Debug path.
```

Expect six items: the repro command and its actual output, your prior, at least two
competing explanations, one cheapest check per explanation with its outcome, the fix, and
the same repro re-run plus one neighbouring case that should not change.

## When NOT to use it

- **Trivial fixes**: a typo, a rename, a one-line change you already understand.
- **Detailed specs**: when the request is already concrete and reviewed, just build it.
- **Numbers nothing rides on**: one sentence ("measured X, as expected") is enough.

"No significant unknowns here" is a valid result; the skills will say so.

## Next

[README](../README.md) (every feature, command and default) ·
[Glossary](GLOSSARY.md) (prior, lane, rigor level, packet size, mode, fresh-context
refutation) · [Architecture](ARCHITECTURE.md) (how commands, skills, agents and artifacts
fit together) · [EXAMPLES.md](../EXAMPLES.md) (more copy-paste prompts)
