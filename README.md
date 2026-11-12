<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns v5.2.0: you predict first, the agent builds quietly and stops only at four points, and the completion report grades every prediction." width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-D97757?style=for-the-badge&labelColor=F0EEE6" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/version-5.2.0-C15F3C?style=for-the-badge&labelColor=F0EEE6" alt="version 5.2.0">
  <img src="https://img.shields.io/badge/skills-1-D4A27F?style=for-the-badge&labelColor=F0EEE6" alt="1 skill">
  <img src="https://img.shields.io/badge/agents-1-C15F3C?style=for-the-badge&labelColor=F0EEE6" alt="1 agent">
  <img src="https://img.shields.io/badge/license-MIT-788C5D?style=for-the-badge&labelColor=F0EEE6" alt="MIT license">
</p>

<p align="center"><strong>Stay the owner of work an agent does for you: say what you expect before it starts, and see afterwards where reality differed.</strong></p>

<p align="center">
  <a href="#recommended-setup-56-words">Setup</a> ·
  <a href="#what-the-evals-showed">Evals</a> ·
  <a href="#the-plugin">Plugin</a> ·
  <a href="#task-card-and-views">Card and views</a> ·
  <a href="#documentation">Docs</a> ·
  <a href="README.zh.md">中文</a>
</p>

---

## What it is

finding-unknowns is a way of working with a coding agent. Before the work, you predict
the outcome and the agent gives its own prediction; both are written down with what would
prove them wrong. During the work, the agent stops only for an irreversible step, a scope
change, a falsified premise or a budget overrun, and logs everything else. Afterwards,
each prediction is graded against the evidence, and the report says what each check did
not prove. It comes in two sizes: 56 words for your `CLAUDE.md`, which is the measured
setup, and a Claude Code plugin that keeps one task card per task across sessions. The
plugin (5.2) has not been evaluated, and neither form has been tested for whether it
helps people understand their work.

---

## Recommended setup: 56 words

Append [`CLAUDE.md`](CLAUDE.md) to your user-level `~/.claude/CLAUDE.md`, where it was
tested, or to a project's `CLAUDE.md`. Append; do not overwrite your file.

```bash
printf '\n' >> ~/.claude/CLAUDE.md
curl -fsSL https://raw.githubusercontent.com/baizhiyuan/finding-unknowns-skill/main/CLAUDE.md >> ~/.claude/CLAUDE.md
```

The whole text:

> Before building, ask me to predict the outcome, then give yours; write both, with what
> would prove each wrong, in `.finding-unknowns/tasks/`. While building, stop only for
> irreversible steps, scope changes, a falsified premise or a budget overrun; log other
> deviations there. Afterwards, grade each prediction against the evidence and say what
> each check did not prove.

There are no commands to learn. Start a task as usual; the assistant asks for your
prediction first. This exact text is what Stage 0 measured (the report calls it "w60",
the 60 words). It is pinned in this repository and changes only after a new check.

[`CLAUDE.next.md`](CLAUDE.next.md) is an 82-word candidate that targets the three holes
Stage 0 found: it skips trivial work, asks once for the decisions only you can make, and
spells out the irreversible step (exact command, your yes, one run, never as a check).
**It is untested.** It replaces the 56 words only if the Tier 1 check in the
[5.2 design](docs/design/5.2.md#8-light-validation) shows that it fixes those holes
without losing what the 56 words do well.

---

## What the evals showed

### Stage 0: simulated users

The [Stage 0 report](https://github.com/baizhiyuan/finding-unknowns-skill/blob/main/docs/evals/2026-11-11-stage0/README.md)
(on `main`; pre-registered) ran Claude Sonnet 5.5 in Claude Code with a simulated user
(gpt-6.1-sol) on six multi-turn build tasks and two controls. The user held one wrong
belief and two unstated requirements. Three arms, three run-sets each, 84 runs, two
graders.

| | no setup | 56 words | 5.0 plugin |
|---|---|---|---|
| Composite, of 42 (noise 3.0) | 20.5 | **31.0** | 21.0 |
| Wrong belief named before the first edit (M1) | 0.11 | 0.94 | 1.00 |
| No interruption after the build started, outside the four stop-points (M4) | 0.78 | 0.92 | 0.11 |
| Irreversible step only after a yes for that command, run once (M5, secondary) | 0.06 | 0.11 | **0.78** |
| Cost per build task (USD) | 0.10 | 0.18 | 3.72 |
| Assistant turns per run | 1.4 | 2.2 | 10.8 |

- **The 56 words beat no setup by 10.5 points**, at $0.08 more per task.
- **The 5.0 plugin did not beat no setup** (+0.5, inside the noise) and scored 10 points
  below the 56 words, at about 21 times their cost. Its own procedures added questions:
  a mode question, commit questions, recall questions in the next session, and menus
  after the debrief.
- **The plugin's one clear win was the irreversible step:** it waited for a yes and ran
  the command once in 0.78 of runs; the 56 words did so in 0.11.
- **The 56 words also asked for a prediction before fixing a typo** (3 of 3 control runs).
- **Scope:** one subject model, one simulated user, tasks written by a model. Nothing
  here measures a real person's understanding; that is Stage 1, not yet run.

By the pre-registered rule, the plugin was not released. The tag
[`eval/stage0-v5`](https://github.com/baizhiyuan/finding-unknowns-skill/tree/eval/stage0-v5)
marks the exact plugin that was evaluated.

### Earlier evals

Three earlier pre-registered evaluations ([docs/evals](docs/evals/)) tested the 4.x skills
as a boost to model output on single-turn tasks with planted traps. No gain survived
replication (baselines already caught 22 to 23 of 25 traps), and the skills cost roughly
10 % to 70 % more input tokens or USD.

### What 5.2 changed in response

5.2 is a rebuild of the plugin sized by those numbers
([design](docs/design/5.2.md)):

- **Fewer turns.** No mode question, no commit question, recall questions only on
  request; the completion report *is* the Debrief, so there is no separate debrief turn;
  questions come once, in one batch, each with a recommended answer.
- **The irreversible step moved into code.** The command is named on the card; a guard
  hook asks before it runs and flags a second run; a lint rule rejects a contract check
  that would re-run it.
- **Bookkeeping moved into a script.** Freezing, integrity checks, lint, the prediction
  log, lists and the HTML view are done by `fu`, a stdlib Python script, not by the model.
- **Less to load.** Structured mode, Cartographer and four of the five agents were cut
  (they stay on branch `v4`). The grader is used only where it matters most.
- **The person's words stay theirs.** The agent never writes a prediction on your behalf;
  if you give none, the card says `P: none given`.

**5.2 itself has not been evaluated.** The design's target (at most four of your turns
and under about $0.60 for a task without an irreversible step) is a guess to check, not
a result. Until the Tier 1 check runs, the 56 words remain the recommendation.

---

## The plugin

### When to use it

Use the plugin when the 56 words are not enough:

- **Work that spans sessions.** The card is a file; the plan, the predictions and what
  happened survive a restart, and `/fu-catch-up` shows only what changed.
- **An irreversible step.** Publishing, a production migration, deleting data, sending
  money. The card names the exact command, and the guard hook asks before it runs.
- **Predictions you want graded.** Your predictions are frozen in a git commit before the
  work, graded afterwards, and logged so you can see your own calibration over time.
- **Measured results.** Benchmarks, backtests, A/B tests and training runs, with a
  stopping rule and a noise floor (`references/results.md`).

For a typo or a one-liner, use neither the card nor the commands.

### Install and update

From the plugin marketplace. These are Claude Code slash commands; enter them **one at a
time**:

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

The plugin brings the skill, four commands, one agent, the `fu` script and the guard
hook. It needs `python3` (3.8 or later, standard library only) for the script and the
hook; without it, the card still works, with Timing `self-reported` and no lint or
integrity check.

`install.sh` copies the skill, the commands, the agent and the script into
`~/.claude/`, **without the guard hook** (hooks ship with the plugin only). With that
install, an irreversible step runs only after your chat yes to the exact command.

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && git checkout v5 && bash install.sh
```

Next release: **v5.2.0**. It is not released yet: until it is, the marketplace serves
v4.3.2, and 5.2 is available only from branch `v5` through `install.sh` as above. Update
the way you installed:

```
/plugin marketplace update finding-unknowns-skill
```

```
/plugin update finding-unknowns@finding-unknowns-skill
```

<details>
<summary><b>Upgrading from 4.x or 5.0, and version check</b></summary>

`install.sh` moves a same-named file that is not its own to `{file}.bak.{timestamp}`; it
never deletes. It sets aside earlier files that carry its marker and lists unmarked 4.x
leftovers (old commands and agents) for you to remove by hand.

```bash
grep -h '"version"' ~/.claude/plugins/cache/finding-unknowns-skill/finding-unknowns/*/.claude-plugin/plugin.json 2>/dev/null \
  || ls ~/.claude/scripts/fu.py
# expect: 5.2.0 (plugin) — or the script listed (install.sh)
```

</details>

### Commands

```
/fu-brief "make the export job resumable"   # you predict; the agent predicts; frozen on your yes
/fu-catch-up                                # next session: only what changed, and what needs you
/fu-debrief                                 # late results or a re-grade
/fu-view                                    # the card, or the task list, as a local HTML page
```

| Command | What it does |
|---|---|
| `/fu-brief <task>` | Reads the repository silently, then asks once: your prediction (with no suggested answer) and up to two decisions only you can make, each with a recommendation. Writes the Brief, shows it in full, and freezes it on your yes |
| `/fu-catch-up [slug]` | The named card, else the most recently changed open one: what changed since you last looked, and `Needs you` |
| `/fu-debrief [slug]` | Grades the card again when results arrive late or you ask for a re-grade. The usual Debrief is the completion report itself |
| `/fu-view [slug \| --list]` | Renders the card, or the list of cards, with `fu render` |

Saying "brief me", "catch me up" or "did it match what we expected" works too. In
non-interactive `claude -p`, use the full names (`/finding-unknowns:fu-brief`).

### How a carded task runs

<p align="center"><img src="assets/lifecycle.svg" alt="A carded task: the Brief before the build, a quiet build with four stop-points, and a completion report that is the Debrief; catch-up when you come back" width="100%"></p>

1. **Brief.** You predict first, in your own words; the agent then reads what it needs and
   gives its own prediction. It writes the approach, both predictions, the stop-points,
   any irreversible command, and a contract of checks that can fail. You approve once;
   `fu freeze` commits the Brief, so git shows the predictions came first.
2. **Quiet build.** The agent stops only at the four stop-points. Everything else takes
   the most reversible option and becomes one line in the deltas file; a decision made for
   you states what it costs if wrong. Every turn ends with a completion report or a stop,
   never an optional question or a menu.
3. **Completion report = Debrief.** Evidence first, every prediction graded (yours first),
   what the checks did not prove, what nobody checked, and one line on what needs you.

### Four layers

<p align="center"><img src="assets/framework.svg" alt="Four layers: always-on text; the guard hook and the fu script; the card skill and commands; one auditor. All files under .finding-unknowns/" width="100%"></p>

| Layer | What it is | Cost to the model |
|---|---|---|
| Always-on text | The 56 words in `CLAUDE.md` | about 75 tokens per session |
| Guard hook + `fu` script | Deterministic work: the irreversible-command prompt, lint, freeze, integrity, log, list, render | none to carry; one short call each |
| Card skill + commands | `SKILL.md` (≤ 700 words) and five references loaded per phase; four thin commands | loaded only when you start a card |
| One auditor | `mechanism-auditor`, a fresh-context grader | called only for an irreversible-lane card, a measured result, or on request |

Without the auditor, the Debrief is graded in the same context and says so
(`same-context — weaker`).

### Four stop-points

<p align="center"><img src="assets/stop-points.svg" alt="The four stop-points; the irreversible step names its exact command, the guard hook asks, it runs once and its checks are dry runs; everything else is logged" width="100%"></p>

1. **Irreversible step:** data rewritten or dropped, deletion, production, money,
   publication, commitments to people. The exact command is on the Brief's
   `Irreversible:` line; it runs once; its contract checks are dry runs. With the guard
   hook, the permission prompt is the stop and your answer is the yes. Without it, the
   agent stops and only a chat yes to that exact command runs it ("go ahead" is not one).
2. **Scope change** outside the Brief.
3. **Dead premise:** a premise or a falsifier fired and no reversible path remains. Two
   failed fixes that share an assumption mean the assumption is logged and tested; a third
   failure is this stop.
4. **Budget** past the multiple agreed in the Brief.

### The guard hook

A `PreToolUse` hook on Bash, shipped with the plugin. When a command matches an
`Irreversible:` line on an open card, it returns `ask`: Claude Code shows its native
permission prompt with the exact command and the card. After the command has run, a
second attempt asks again with "already ran once at {time}; a post-check must not
re-execute it". Generic destructive patterns (`rm -rf`, force-push, `reset --hard`,
`DROP TABLE`) are only logged, as hashes, unless the strict profile is on.

- **Advisory.** It asks; it never denies. It fails open: any error, no card or no match,
  and it does nothing. A command run through another host (`ssh host '…'`) is not read.
- **Hard enforcement** is Claude Code's own permission system: an `ask` rule for the exact
  command in user or managed settings, which the agent cannot edit, for example
  `{"permissions": {"ask": ["Bash(python publish.py build/quotes.json)"]}}`.
- **Modes:** `guard: off | log | ask` in `.finding-unknowns/profile.md`. The default is
  `ask` with the plugin, `off` with `install.sh`.
- **Not yet verified:** how `ask` behaves under bypass-permissions mode, and a live run.
  Under `claude -p`, where no one can answer, Claude Code denies the call and the agent
  reads the reason.

### Completion report = Debrief

<p align="center"><img src="assets/debrief.svg" alt="The Debrief in order: evidence, predictions graded with yours first, integrity, what the checks did not prove, not checked, model changes, bottom line, needs you" width="100%"></p>

When carded work completes, the report you get is the Debrief. It runs in this order:

- **Evidence:** the commands that ran and their output, before any prose.
- **Every prediction, quoted from the frozen card, yours first,** with what was measured,
  a verdict (`consistent · partly · inconsistent · can't tell · post-hoc fit`) and a
  mechanism tagged `verified · supported · inferred · untested`. The verb never claims
  more than the tier.
- **Integrity:** three lines from `fu integrity`: the Brief against its freeze commit, the
  check files, and changes no delta explains.
- **Did NOT prove** for each check, and **Not checked**, which is never empty.
- **Bottom line:** what holds, what did not hold, where the evidence stops.
- **Needs you:** one decision with a recommendation, stated, not asked.

**Who grades.** For a card with an irreversible step, a measured result, or on your
request, `mechanism-auditor` grades from the frozen card and the artifacts. It never sees
the transcript or the builder's claims. Otherwise the Debrief is graded in the same
context and labelled `same-context — weaker`. In Stage 0 the plugin, grader included,
reported a missed expectation less often than the 56 words (0.50 against 0.83), so the
grader is now used narrowly.

### Measured results

Benchmarks, backtests, A/B tests and training runs use **Theory → Measured → Consistent?
→ Mechanism**, from the author's research practice:

- the prediction is written before the data, with a stopping rule and a noise floor from
  at least three reruns;
- results that arrive over days go into a run table; no verdict before the stopping rule
  is met;
- the rule verdict is mechanical; whether the idea is still alive is your call.

---

## Task card and views

### The card

<p align="center"><img src="assets/card.svg" alt="Anatomy of a task card: a five-line header, the frozen Brief, Amendments, the deltas rollup, Model changes, Open and the Debrief; the deltas file beside it" width="100%"></p>

`.finding-unknowns/tasks/{slug}.md`, committed by `fu freeze`. One format everywhere:
lines with fixed keys in a fixed order, nested lists, no tables.

```
P1 (you · medium) "the bulky parcel's cheapest quote is Economy at 4.00"
  - falsifier: cheapest(bulky) is not Economy 4.00
  - should not change: the small parcel stays Economy 3.00
```

- **Header:** goal and state, `Needs you`, mode and when you last looked, and Timing (the
  freeze commit).
- **Frozen Brief:** the approach with one reason per decision; your predictions, quoted,
  then the agent's; the stop-points; `Irreversible:` lines; the contract, where each check
  says what it does **not** prove.
- **Amendments** (dated, append-only; a miss is still graded), a rollup of the deltas
  file, **Model changes** ("you expected X, it is Y, because Z"), **Open**, and the
  **Debrief** at the end.
- **Beside it:** `{slug}.deltas.md`, one line per deviation, surprise or decision made for
  you; and `decisions.md`, the answers only you could give, quoted and dated, so an
  answered question is never asked again.

`fu lint` checks the card against [`references/card.md`](skills/finding-unknowns/references/card.md).

### Terminal lists

In the terminal everything is a nested list. `fu list --all` on the repository's test
fixtures (open cards first; `fu list` alone shows only those):

```
search-export · building
  - needs you: nothing
  - last seen: never · unseen deltas: 1
  - graded: not yet
quote-export · debriefed
  - needs you: the carrier's remote-zone rate card (recommendation: send it and I re-check parcel 3; settles whether 8.00 stands)
  - last seen: after D3 · unseen deltas: 0
  - graded: you 1 of 2 held · agent 1 of 1 held
```

Once you or the agent have five graded predictions, a calibration line follows, such as
`You: 4 of 6 held · Agent: 6 of 6 held`; an agent that holds every one is probably
predicting too safely.

### HTML view

<p align="center"><img src="assets/view-card.png" alt="HTML view of a debriefed card: Needs you first, where the evidence stops, what the checks did not prove, and a one-row strip of what happened in order" width="80%"></p>

For a complex task (an irreversible step, more than three predictions, or work you expect
to resume later), the Brief-approval ask includes one clause offering an HTML view. Your
answer is remembered in `profile.md`; it is never a separate question. `fu render` writes
`.finding-unknowns/view/{slug}.html` from fixed templates: no script, no network,
everything escaped. The page leads with `Needs you` and where the evidence stops, then
one row of what happened in order with the irreversible step marked. The task-list page
carries your calibration as a stat line. The view adds detail; it never shows a miss the
terminal left out.

---

## Small models: the strict profile

For open-weight and other small models, turn on the strict profile with `fu init --strict`
or by saying "strict". It stores `strict: yes` in `profile.md`:

- the agent fills the template inside `/fu-brief` instead of composing a card;
- `fu lint` enforces caps (at most 3 agent predictions, 5 contract items, 20 words per
  field, a 40-line live part) and must pass before the Brief-approval ask;
- your prediction is a quoted slot, or `P: none given`;
- with the guard on `ask`, generic destructive commands also ask.

This rests on one ungraded run of a small model with the 4.x structured protocol, which
produced orderly paperwork around a wrong, irreversible result. Whether strict does better
is untested; a three-run check is in the [design](docs/design/5.2.md#5-small-models).

---

## Classic line: branch `v4`

Structured mode, Cartographer (the unknowns ledger, regret ordering, the six-condition
gate), the eight numbered techniques and the 4.x agents are not in 5.x. They stay on
branch `v4` (v4.3.2), which gets bug fixes only:

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && git checkout v4 && bash install.sh
```

---

## Principles

- **You predict first.** Your prediction is recorded before you see the agent's, in your
  words, and graded first.
- **Look before asking.** The agent never asks what the code, docs or data answer; it asks
  only what only you can decide.
- **A check must be able to fail** and says what it does not prove.
- **Stop for the four reasons, log the rest.** An interruption costs your attention; a
  delta line costs nothing until you read it.
- **Code enforces what code can.** The irreversible-command prompt, the frozen Brief and
  the integrity checks are mechanical, not promises in prose.
- **No rescue.** A good story explains a miss; it never turns it into a hit.
- **Claim nothing beyond the evidence.** Every component is kept on design grounds; what
  has been measured is stated above.

These come from the discovery practice of Thariq Shihipar's field guide and from Addy
Osmani's account of the slide from offloading to deferral to **cognitive surrender** (the
term is from Shaw & Nave, _Thinking—Fast, Slow, and Artificial_, SSRN 6097646).

### Roadmap

- **Tier 1:** four Stage 0 scenarios, two runs each, comparing the 56 words, the 82-word
  candidate, a length-matched placebo and the plugin with the hook. Mechanical tripwires
  only (for example, exactly one irreversible run, after a yes); it detects breakage, not
  small differences.
- **Small models:** the strict profile against the 4.x structured run, three runs.
- **Stage 1:** real people, deferred, not cancelled. Until then, nothing here claims to
  improve understanding.

---

## Documentation

- **[5-minute tutorial](docs/TUTORIAL.md):** one card, Brief to Debrief
- **[Glossary](docs/GLOSSARY.md):** card, prediction, contract, stop-point, lane, verdicts
- **[Architecture](docs/ARCHITECTURE.md):** the four layers, files and data flow
- **[5.2 design](docs/design/5.2.md)** (the governing design) and the **[`fu` contract](docs/design/fu-cli.md)**
- **[SKILL.md](skills/finding-unknowns/SKILL.md)** and its [card schema](skills/finding-unknowns/references/card.md)
- **[Examples](EXAMPLES.md):** copy-paste prompts
- **[Changelog](CHANGELOG.md)** · **[AGENTS.md](AGENTS.md)** · **[Contributing](CONTRIBUTING.md)**

---

## Requirements

- **Claude Code:** the CLI, desktop app or an IDE extension. The skill's Markdown also
  works in Codex, without the hook.
- **Python 3.8 or later** for the `fu` script and the guard hook, standard library only.
- **git** for freezing cards (optional; without it, Timing is `self-reported` and the
  integrity check does not run).
- **`bash`** only for `install.sh`.

## Project Layout

<details>
<summary><b>Repository tree</b></summary>

```
finding-unknowns-skill/
├── .claude-plugin/          Plugin and marketplace manifests
├── commands/                /fu-brief (holds the card template) · /fu-catch-up · /fu-debrief · /fu-view
├── skills/finding-unknowns/
│   ├── SKILL.md             The card, the four stop-points, always-on rules (≤ 700 words)
│   └── references/          card (schema) · brief · debrief · results · view
├── agents/                  mechanism-auditor (fresh-context grader, used narrowly)
├── scripts/                 fu.py (lint, freeze, integrity, log, list, render, guard) · validate.py · diagrams/
├── hooks/hooks.json         The guard hook (plugin install only)
├── bin/fu                   Optional wrapper to put fu on PATH
├── tests/                   Tier 0 tests and fixture cards
├── docs/                    design/, evals/, field-notes/, ARCHITECTURE, GLOSSARY, TUTORIAL (+ .zh)
├── assets/                  Diagrams (SVG) and the HTML view screenshot; assets/zh/ = Chinese versions
├── CLAUDE.md                The measured 56 words · CLAUDE.next.md: the untested 82-word candidate
├── install.sh               Installer without the hook; sets aside, never deletes
├── AGENTS.md · EXAMPLES.md · CONTRIBUTING.md · CHANGELOG.md · LICENSE (MIT)
└── README.md (English, canonical) · README.zh.md (简体中文)
```

</details>

## License & Credits

Released under the [MIT License](LICENSE).

- Discovery: Thariq Shihipar, _"A Field Guide to Fable: Finding Your Unknowns"_ ([@trq212](https://x.com/trq212/status/2073100352921215386)).
- The handoff, "what the checks did not prove", and grading without the builder's reasoning: Addy Osmani, _"Critical thinking when agents do the work"_ ([source](https://x.com/addyosmani/status/2117512471930167377)).
- *Cognitive surrender*: Shaw & Nave, _Thinking—Fast, Slow, and Artificial_ (SSRN 6097646); cognitive debt: Margaret-Anne Storey.
- Theory → Measured → Consistent? → Mechanism: the author's own empirical research practice.
- The Debrief's field rules (the verb matches the evidence tier, a three-part bottom line, a rewrite changes words only) paraphrase writing principles from [nature-skills](https://github.com/Yuan1z0825/nature-skills) by Yuan Yizhe (Apache-2.0); no text is copied. For paper-bound write-ups, use its `nature-polishing` and `nature-figure` skills directly.
- What 5.2 borrowed from other projects: asking only what only the person can decide, and dropping the forced reconnaissance agent, from the pre-registered question-effectiveness evaluation of gateguard (everything-claude-code); recording answered decisions (`decisions.md`) from Matt Pocock's ADR habit in his skills; a cost-if-wrong on every decision made for you from the ruling line in superpowers (Jesse Vincent); the learn-mode stop rule from pstack's `teach` (Lauren Tan).
- The 5.2 design follows an advisor answer by Fable 5.2 ([design](docs/design/5.2.md)); the 5.0 reviews are in [docs/design/5.0-advisors](docs/design/5.0-advisors/fable.md).

**Disclaimer.** This is an independent community project. It is not affiliated with, authorised by, or endorsed by Anthropic.
