<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns v6.0.0-rc.1: keep your own map of what you know and do not know, and update it only on evidence. A terminal card shows fu:before for a bug fix (your quoted expectation, a premise marked ✗, a question that needs you, with a recommended answer), the reply &quot;go&quot;, then fu:after (what the checks did not prove, what is still unknown)" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-D97757?style=for-the-badge&labelColor=F0EEE6" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/version-6.0.0--rc.1-C15F3C?style=for-the-badge&labelColor=F0EEE6" alt="version 6.0.0-rc.1">
  <img src="https://img.shields.io/badge/status-release_candidate-B8860B?style=for-the-badge&labelColor=F0EEE6" alt="status: release candidate">
  <img src="https://img.shields.io/badge/license-MIT-788C5D?style=for-the-badge&labelColor=F0EEE6" alt="MIT license">
</p>

<p align="center"><strong>Keep your own map of what you know and do not know, and update it only on evidence.</strong></p>

<p align="center"><em>6.0 release candidate (<code>v6.0.0-rc.1</code>). Tested only in wording tests with a simulated user, where it missed one pre-registered condition and was adopted by the owner; not yet compared with the earlier 82-word text; no one has measured learning.</em></p>

<p align="center">
  <a href="#what-it-looks-like">Example</a> ·
  <a href="#the-four-quadrants">The map</a> ·
  <a href="#how-it-runs">How it runs</a> ·
  <a href="#install">Install</a> ·
  <a href="#what-the-evals-show">Evidence</a> ·
  <a href="README.zh.md">中文</a>
</p>

---

- **What happens:** before a non-trivial change, the assistant prints `fu:before`, a map of
  what the work rests on and what is still open, and ends its turn. Your reply starts the
  work, which ends with `fu:after`: what moved on the map.
- **What it looks like:** a nested list in the terminal ([example below](#what-it-looks-like)).
- **What it costs:** one extra round per non-trivial task. "Just do it" or "直接做" in the
  request skips the wait; only an irreversible step still waits, for an explicit yes ("go
  ahead" or "继续" is not one). In tests, "直接做" still stopped too often
  ([details](#how-it-runs)).
- **What it is:** 130 words of always-on text in your `CLAUDE.md`, plus an optional skill with
  two commands. No hooks, no agents; nothing is written to disk unless you say "save".
- **How sure anyone is:** the text was tested in pre-registered wording tests with a simulated
  user, one model and 3 runs per task. It failed one of its 11 conditions (safeguard notices in
  3 of 24 runs, limit 1), and the owner adopted it for the release candidate regardless. It has not been compared with the 82-word text it would
  replace, and no one has measured whether it helps a person learn.

To install, paste the always-on text into `CLAUDE.md` or run `install.sh`: see
[Install](#install).

## What it looks like

You write: *"I think the 500s on /export come from the new CSV encoder; fix it."* The assistant
reads the code and the logs, then replies:

```
fu:before · fix the 500s on /export
- You expect: "the 500s on /export come from the new CSV encoder"
- KK · relying on
  - the encoder changed on 5 Nov — git log src/export/csv.py
  - ✗ the 500s started with that change — the logs show them from 3 Nov
- KU · open
  - which requests fail — I will find out by replaying yesterday's failures
  - may empty fields change from "" to nothing? — needs you; I would pick "no" because a client parses them
- UU · you did not ask, but it matters
  - export runs inside the request; a large account times out, and a timeout is also a 500
- I expect: mostly timeouts on large accounts; wrong if small exports fail too
```

You reply *"go"*, which accepts "no" on the empty fields. The work runs and ends with:

```
fu:after · fix the 500s on /export
- Expected → found
  - You: "the 500s on /export come from the new CSV encoder" → 2 of 14 failures are encoder errors · partly
    - why: the encoder fails only on NUL bytes; the other 12 are exports over 30 s [verified]
  - Me: mostly timeouts on large accounts → 12 of 14 · held
- Now known
  - the gateway cuts requests at 30 s — gateway.yaml:41
- Not proved
  - the new test covers NUL bytes → leaves open other control characters
- Still unknown
  - whether export should move to a background job — cheapest way to find out: count exports over 10 s last month · you
- Decided for you
  - NUL bytes are escaped — instead of dropping the row · if wrong: one client sees "\0" in a cell
  - left the 12 timeout 500s unfixed — instead of moving export to a background job · if wrong: /export still fails for large accounts
```

The `✗` refutes your premise but not the request (the 500s still need fixing), so the work
continues and the miss is reported afterwards. A `✗` that changes what you asked for is a stop.

<details>
<summary><b>A work decision</b></summary>

You write: *"We log about 40 million events a day and run Postgres today. Postgres or ClickHouse for our event analytics? One page for the team."*

```
fu:before · recommend a store for event analytics
- You expect: not stated
- KK · relying on
  - about 40 million events a day; the team runs Postgres today — you said
- KU · open
  - what the current dashboards query — I will find out by reading the dashboard SQL
  - is a second database acceptable to operate? — needs you; I would pick "only if Postgres fails a measured test"
- UK · I assume you want
  - numbers before opinions, written for engineers — you said "for the team"
- UU · you did not ask, but it matters
  - retention: a year at this rate is about 15 billion rows, which decides more than query speed
- I expect: Postgres with monthly partitions is enough for 90 days; wrong if the slowest dashboard query takes over 2 s on a 90-day copy
```

You reply *"go"*, which accepts "only if Postgres fails a measured test". The work runs and ends with:

```
fu:after · recommend a store for event analytics
- Expected → found
  - Me: Postgres is enough for 90 days → slowest query 1.4 s on a 90-day sample · held
- Now known
  - 3 of 11 dashboards scan the full history — dashboards/*.sql
- Not proved
  - the timing ran one query at a time → leaves open concurrent load
- Still unknown
  - how long raw events must be kept — cheapest way to find out: ask legal · you
- Decided for you
  - timed a 10 % sample of the 90 days — instead of a full 90-day copy · if wrong: the 1.4 s does not hold at full volume
```

</details>

**Real maps run longer than this one.** The example follows the skill's template (at most 12
lines; templates in [`SKILL.md`](skills/finding-unknowns/SKILL.md)). Everyday runs do not load
the skill: in the one test of the shipped text (v6f4d), which asks for at most 150 words, the
12 maps on the four core tasks had 145 to 281 words (median 174.5; 2 of 12 within 150), counted
from the heading to the end of the message. Labels and layout may also differ from the
template.

## The four quadrants

<p align="center">
  <img src="assets/quadrants.svg" alt="The four quadrants: known knowns (what you rely on), known unknowns (a question you can name), unknown knowns (what you know but did not say), unknown unknowns (what you did not know to ask); fu:before shows the map, fu:after shows what moved" width="88%">
</p>

You hand work and decisions to an assistant every day. Each exchange can leave you knowing
more, or it can quietly replace your judgment with the assistant's output. finding-unknowns
keeps one thing in view: **your own map of what you know and do not know.** The assistant
shows that map before non-trivial changes, waits once for your reply, and shows what moved on
the map afterwards.

An unknown lives in one of four places, and each needs a different move:

| Quadrant | What it is for you | What the assistant does before the work |
|---|---|---|
| **KK** known knowns | What you rely on. The danger is a false known | Lists the few facts and beliefs the work rests on, each with its source; checks what can be checked; marks a contradicted one `✗` |
| **KU** known unknowns | A question you can name | Finds it out itself, or, if only you can answer, asks with a recommended answer |
| **UK** unknown knowns | What you know but did not say: taste, constraints, context | Guesses it out loud ("I assume you want X because Y"). Reacting costs you less than specifying |
| **UU** unknown unknowns | What you did not know to ask | Names up to three things that matter, each with why. "None found" is a valid answer |

After the work, the same map is updated: expectations against evidence, what is now known,
what each check did not prove, what is still unknown, and the choices and changes you did not
ask for.

## How it runs

<p align="center">
  <img src="assets/lifecycle.svg" alt="How it runs: before any change, fu:before shows the four quadrants and both expectations; then a pause: the turn ends and your reply starts the work (&quot;go&quot; accepts the recommended answers; &quot;just do it&quot; skips the wait, except that an irreversible step still waits for an explicit yes, and a bare &quot;go&quot; is not one); after your reply, the work stops only for a scope change, a falsified premise that changes the task or an irreversible step; after the result, fu:after shows expected against found, now known, not proved, still unknown and what you did not ask for; the look-back runs only when you ask. The conversation is the record." width="100%">
</p>

This applies to non-trivial work in the Claude Code terminal: coding, research, writing, a
decision at work. Trivial requests, lookups and casual talk get nothing.

- **Why the pause:** without it, the map was mostly announced and not shown, above all on
  non-coding work. With it, the map appeared before the first change in almost every core test
  run ([evidence](#what-the-evals-show)).
- **How to skip:** put "just do it" or "直接做" in the request, and the assistant does not
  wait; only an irreversible step still waits for your explicit yes. In the test of the
  shipped text, "直接做" on a request that itself asked for an irreversible step, replacing a
  live table (6 runs): no run replaced the live table (0 of 6), but all 6 ended their first
  turn without changing anything. 5 ended there with questions and held back the reversible
  part too, which the grader judged unjustified; the sixth did it only after a second message,
  "继续" (1 of 6 completed). With "Just do it, I'm in a hurry." the map came before the first
  change in 0 of 3 runs.

**The rules.** Everyday runs see only the always-on text. The labels, the layout and the finer
rules (size limits, `why` lines only where an expectation failed) live in the skill, which
loads only when you ask for it.

- **Your expectation is quoted, never written for you.** If you gave none, the slot says
  `not stated` and nobody asks. The empty slot is the nudge: put your guess in the request
  ("I think X; do Y"), or add it at the pause.
- **Only what only you can answer comes to you,** with a recommended answer worded so that
  "yes" accepts it. Facts are the assistant's job.
- **After your reply, few stops:** a scope change, a falsified premise that changes the task,
  or an irreversible step. A `✗` that only refutes your expectation is reported, not a stop.
- **An irreversible step** (in code, or sending, paying, publishing, deleting) is shown as the
  exact command or message, as the only question; it runs once, only after your explicit yes,
  and never as a check. A generic "go ahead" or "继续" is not a yes: approve the step by
  naming it. Under an earlier variant without that clause (F4c), the one run that got "Go
  ahead." took it as the yes. Under the shipped text, the one run that got "继续" asked for an
  explicit yes instead, but in the same turn ran the migration code on a temporary copy of the
  table, which goes against "never as a check".
- **Nothing follows `fu:after`,** no menu and no question. Nothing is written to disk unless
  you say "save"; the conversation is the record.

**The tradeoff: one pause, then few stops.** The price is reading the map before you say go and
reading `fu:after` at the end: above all, what each check did not prove. If you would rather be
asked before each assumption as it comes up, this is the wrong default for you.

## Install

**The always-on text is the product.** It runs on every non-trivial request. The skill and the
two commands load only when you ask for an interview or a look-back; the plugin alone changes
nothing until you ask.

**This is a release candidate.** Until the own-use week and the comparison with the 82 words
are done, `main` and the plugin marketplace stay on 4.3.2 with the 82 words. Install 6.0 by
cloning branch `v6` (tag `v6.0.0-rc.1`). Using 4.x (Cartographer, `keep-the-reasoning`, the
agents)? Stay on 4.x: see [how](docs/HISTORY.md#how-to-stay-on-4x).

### The always-on text

Append the text of [`CLAUDE.md`](CLAUDE.md) (130 words) to your user-level `~/.claude/CLAUDE.md`,
or to a project's `CLAUDE.md`, or let `install.sh` do it:

> Before non-trivial changes (reading is fine), show `fu:before` (≤150 words, terse) in your reply, then end your turn: relied on, sourced; open questions; assumed want; only-I-can-answer (recommend answers); what I should've asked. Quote my expectation or "not stated"; never invent one. Give yours and what would disprove it. After my reply, stop only for scope changes, falsified premises changing the task (refuted expectation: report only), or an irreversible step: show its exact command or message as your only question; run once, only after my explicit yes ("go ahead" isn't one), never as a check. End with `fu:after`, asking nothing: each expectation against evidence; what became known; what checks didn't prove; what stays unknown. Omit empty fields. "Just do it"/"直接做" etc.: only irreversible steps wait. Skip trivial requests; ignore `fu-note:` lines.

Keep only one finding-unknowns text in your `CLAUDE.md`, and remove any older one:

- the 56 words beginning "Before building, ask me to predict";
- the 82 words beginning "Before non-trivial work, ask me once to predict";
- a pre-release 6.0 draft beginning "Before non-trivial work, show `fu:before`";
- an earlier 6.0 text (127 words) beginning "Before non-trivial changes (reading is fine), show
  `fu:before` in your reply";
- the 4.x drop-in headed `# finding-unknowns (passive drop-in)`;
- a 4.x "Personal Skills: finding-unknowns" line, which `install.sh` does not detect; remove
  it by hand.

### The skill and the two commands

`install.sh` installs the skill, the two commands and the always-on text in one step:

```bash
git clone -b v6 https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && bash install.sh            # add --no-claude-md to skip CLAUDE.md
```

If you pasted the always-on text by hand, remove it first or run with `--no-claude-md`.

<details>
<summary><b>What <code>install.sh</code> does</b></summary>

- copies `SKILL.md`, `fu-interview.md` and `fu-lookback.md` into `~/.claude` (or
  `$CLAUDE_CONFIG_DIR`), saving a same-name file that is not ours as `<file>.<timestamp>.bak`;
- appends the always-on text to `~/.claude/CLAUDE.md` between
  `<!-- finding-unknowns:always-on -->` markers (after saving `CLAUDE.md.<timestamp>.bak`), or
  replaces the text between them on a later run; it never edits text outside the markers and
  stops without changes on a stray or duplicate marker;
- moves the 4.x pieces that 6.0 removed into `~/.claude/finding-unknowns-backup-<timestamp>/`,
  but only files that carry this project's marker.

</details>

<details>
<summary><b>Installing as a plugin instead</b></summary>

During the release candidate the GitHub marketplace serves 4.3.2, so add your clone as a local
marketplace (if you added the GitHub marketplace before, first run
`/plugin marketplace remove finding-unknowns-skill`). Enter these slash commands **one at a
time**, with the path to your clone:

```
/plugin marketplace add ./finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

The plugin cannot edit your `CLAUDE.md`; append the always-on text yourself. Use the plugin or
`install.sh` for the skill, not both.

</details>

<details>
<summary><b>Updating and checking what is installed</b></summary>

With a clone: `git pull && bash install.sh` (running it twice changes nothing). With the
plugin: `/plugin marketplace update finding-unknowns-skill`, then
`/plugin update finding-unknowns@finding-unknowns-skill`. To check what is installed:

```bash
C="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
ls "$C/plugins/cache/finding-unknowns-skill/finding-unknowns/" 2>/dev/null \
  || grep -l 'fu:before' "$C/skills/finding-unknowns/SKILL.md"
# expect: 6.0.0 (plugin), or the path of the 6.0 SKILL.md
```

</details>

## Two commands you choose

**`/fu-interview <topic>`** interviews you before work you are unsure about.

1. You speak first: what you want, what you expect, what you are least sure of.
2. The assistant finds out what it can, prints the map, then asks rounds of up to three
   independent questions, most costly-if-wrong first, each shaped by its quadrant. After each
   round it prints one line of counts, no clarity score:
   `Map: known 4 · open 3 (1 needing you) · assumed 2 · blind spots 1`.
3. It stops when the rest is cheaper to learn by doing, when the assistant can predict your
   next three answers, or when you say stop, and prints a `fu:interview` map without starting
   the work.

**`/fu-lookback [7d | session id]`** looks back over this session. With `7d`, it filters the
last seven days of Claude Code transcripts in the current project for `fu:` blocks and
`fu-note:` lines. It quotes what it finds, does not reconstruct, and never reads a transcript
whole. It prints what you expected against what turned out, what became known, what is still
open, and, from five graded expectations, your pattern.

**`fu-note:`** Type a line starting `fu-note:` when a block taught you something, annoyed you
or missed something (`fu-note: noise`, `fu-note: missed that the API is rate-limited`). The
assistant ignores it; the look-back finds it.

**Limits.** A look-back reaches only as far back as Claude Code keeps transcripts
(`cleanupPeriodDays`). After a long session is compacted, `fu:after` re-reads `fu:before` from
the transcript or marks the quote `from memory`.

## Principles

**The map is yours.** The four quadrants come from Thariq Shihipar's field guide. Showing them
is not a score: you see where your unknowns are before the work starts, and decide which to
chase.

<p align="center">
  <img src="assets/slide.svg" alt="The slide, after Addy Osmani: offloading (delegate the work, keep ownership), then deferral (the output becomes the next input), then cognitive surrender (the output quietly becomes your own belief). Under each step, what is meant to interrupt it: the pause after fu:before; You expect (predict before you look); Not proved and Still unknown. Why these fields exist; whether they slow the slide is not measured." width="100%">
</p>

**Critical thinking is the rule for updating the map.** Addy Osmani describes a slide across
many handoffs: **offloading** (you delegate and keep ownership), then **deferral** (the output
becomes the next input), then **cognitive surrender** (the output quietly becomes your own
belief). Three habits interrupt it, and each has a field: **predict before you look**
(`You expect`), **say what a check did not prove** (`Not proved`), and **say what is still
unknown** (`Still unknown`).

**Theory before result.** The owner's research practice reports every measured result as
theory → measured → consistent? → mechanism. In `fu:after` this is one row: expected → found →
verdict → why.

| Habit | The field that trains it |
|---|---|
| Say your guess when you ask | `You expect`, including its empty state |
| Know what your plan rests on | `KK · relying on`, with sources and `✗` |
| Ask "what would change my mind?" | `wrong if …` on every expectation |
| Answer what only you can answer, and notice what you had not said | `needs you` and `UK` |
| Read what a check leaves open before accepting the result | `Not proved` |
| Choose on purpose which unknown to chase | `Still unknown`, with the cheapest way to find out |

No quiz, no recall questions, no lecture. When you ask to be taught, the assistant stops when
you can predict the behaviour.

## What the evals show

| | |
|---|---|
| **What was tested** | Whether the 6.0 always-on text makes the map appear before the first change, pauses once, lets the work finish and keeps its guards |
| **With whom** | A simulated user whose second reply was a fixed "Go ahead." ("继续" in one v6f4d task); one model (`claude-sonnet-5-5`); 3 runs per task; eight pre-registered tests on 2026-11-12 and 2026-11-13 |
| **Result** | The shipped text (the current `CLAUDE.md`, F4d) showed the map before the first change in 12 of 12 runs on the four core tasks and completed the work in 12 of 12. It failed one of its 11 pre-registered conditions (safeguard notices in 3 of 24 runs, limit 1); the owner adopted it regardless |
| **What it does not show** | Anything about a real person, a comparison with the 82-word text, or learning |

- **Why the pause is believed to work:** one result moves between sessions by about 4 runs in
  12 (one earlier text showed the map first in 8, then 5, then 4 of 12). The pause's 11 of 12
  under two earlier texts, and 12 of 12 under the shipped text, are above that spread.
- **Maps are long, and bounding them has only partly worked:** the first text with the pause
  (F4b) gave a median map of 534 words, and a variant capping it at 12 lines a median of 279
  (limit 250). The shipped text asks for at most 150 words and reached a median of 174.5,
  within the limit of 250, but only 2 of 12 maps were within 150.

**What these tests do not show:**

- **The reply after the pause was simulated:** always a fixed generic go ("Go ahead."; "继续"
  in one v6f4d task), with no answers or corrections. Completion means only that the assistant continues after an uninformative go.
- **One model, 3 runs per task.** The rules are screening rules, not significance tests; one
  run either way could have changed several verdicts, including the safety condition, which
  the shipped text failed (3 of 24 against a limit of 1) and an earlier text passed with no
  slack (1 of 18). The shipped text was tested in a single-arm test that did not confirm it;
  its comparison with the earlier texts is across sessions and not randomised.
- **Grading of the earlier tests was weaker than pre-registered:** up to v6f4b, some graders
  could see which text a run used, and later ones lacked the task key and inferred beliefs
  from the prompt. The test of the shipped text was graded blind, with the key. The
  visibility, pause, completion and safety counts are mechanical and not affected.
- **Under "just do it" the text is weaker:** with "Just do it, I'm in a hurry." the map
  appeared before the first change in 0 of 3 runs, and 2 of 3 completed (the third stopped
  over a premise, which the grader judged justified). With "直接做" on a request that asked
  for an irreversible step, all 6 runs ended their first turn without changing anything; 5
  ended there without the reversible part (judged unjustified), and the sixth did it only
  after a second message, "继续"; 1 of 6 completed.

**Known limits of the release candidate:**

- **Subagents and headless runs** load a user-level `CLAUDE.md` too, with nobody to reply to
  `fu:before`; whether they end their turn on the map is untested (a check is planned before
  6.0.0).
- **The API's safeguards** flagged 3 of 24 runs of the shipped text, on the vendor-choice and
  customer-reply tasks, against a pre-registered limit of 1: the one condition it failed. All
  three were notices, and each run continued and completed. With 3 runs per task it is not
  known whether the wording raises the rate (the earlier texts: 1 of 18 and 0 of 21).
- **"Non-trivial"** was tested only at its edges; small changes in between are where the
  pause may feel like friction.

**Against the 82 words, 6.0 is unmeasured.** The new text is 48 words longer; it drops the file
of predictions, "ask me once to predict" and the budget-overrun stop. **Nobody has measured
whether any of this helps a person learn or understand more.** Every number here comes from
simulated users.

**What decides the final release:**

- **One week of the owner's own use,** with decision rules written in advance
  ([PLAN.md](docs/evals/2026-11-12-6.0-own-use/PLAN.md)).
- **A planned comparison of three texts:** none, the 82 words and the 6.0 text.

Every test, the replication spread, Stage 0, Tier 1 and the changes against the 82 words:
[docs/EVIDENCE.md](docs/EVIDENCE.md).

## Compared with

**The 82-word text on `main`.** It asks you once to predict the outcome, writes both
predictions to a file and grades them afterwards; it shows no four-quadrant map. It is the text
Tier 1 checked, and it stays on `main` until the comparison above.

**The Karpathy-style `CLAUDE.md`** in
[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) asks when
uncertain; this one gathers its questions into `fu:before`, asks once, then proceeds. Use one,
or say in your `CLAUDE.md` which one wins. The skill's `Decided for you` field takes one idea
from it, as disclosure rather than a prohibition. Its evidence is thin: the one
placebo-controlled audit we found (skill-receipts Audit #4) measured only its simplicity
rules, which produced 4.8 % fewer lines than no instructions, within noise; accuracy was
unchanged.

**OMC's `deep-interview`** is the better tool when you want a gated specification that feeds
an execution pipeline; `/fu-interview` ends with a map and does not start the work.

## History

- **4.x, the classic line,** lives on branch
  [`v4`](https://github.com/baizhiyuan/finding-unknowns-skill/tree/v4) (last release v4.3.2)
  and gets bug fixes only. Stay on it if you use Cartographer, `keep-the-reasoning`,
  `theory-vs-result` or the agents.
- **5.0 to 5.2: designed and evaluated, never released.** A task card on disk, with a script,
  a guard hook and an HTML view; interruptions and cost held them back.
- **6.0: a redesign from first principles** that puts the four quadrants back in front of the
  person ([design](docs/design/6.0.md)).

How to stay on 4.x and the 5.x detail: [docs/HISTORY.md](docs/HISTORY.md).

<details>
<summary><b>Repository layout</b></summary>

```
finding-unknowns-skill/
├── CLAUDE.md                     The always-on text (130 words)
├── skills/finding-unknowns/
│   └── SKILL.md                  Templates, interview, look-back with the transcript filter
├── commands/                     fu-interview.md, fu-lookback.md
├── .claude-plugin/               Plugin and marketplace manifests
├── install.sh                    Installer (skill, commands, always-on text; retires 4.x files)
├── assets/                       Diagrams (SVG); assets/zh/ holds the Chinese versions
├── docs/                         EVIDENCE, HISTORY, GLOSSARY, design/, evals/, field-notes/
├── scripts/                      validate.py (CI checks), Chinese-diagram and diagram scripts
└── tests/                        install.sh and the look-back filter
```

</details>

## License & Credits

Released under the [MIT License](LICENSE).

- **The four quadrants and the idea of interviewing for unknowns:** Thariq Shihipar,
  _"A Field Guide to Fable: Finding Your Unknowns"_
  ([@trq212](https://x.com/trq212/status/2073100352921215386)).
- **Offloading → deferral → cognitive surrender, and the habits that interrupt it** (predict
  before you look, say what a check did not prove, the "can you predict my next answers?"
  stop test): Addy Osmani's posts on critical thinking when agents do the work
  ([source](https://x.com/addyosmani/status/2117512471930167377)).
- **The interview** borrows two things from Matt Pocock's `grill-me`: a recommended answer
  worded so that "yes" accepts it, and batches of independent questions. It also borrows,
  and changes, one from the `deep-interview` skill in
  [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode): a progress line every
  round, shown here as counts, with no clarity score.
- **Expected → found → verdict → why:** the owner's own empirical research practice
  (`theory-vs-result`, on branch `v4`).
- **Reporting the choices and changes you did not ask for** (`Decided for you`) adapts one idea from the
  Karpathy-style `CLAUDE.md` by Jiayuan Zhang ([andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)), written
  from Andrej Karpathy's [post of 2026-01-26](https://x.com/karpathy/status/2015883857489522876).

**Disclaimer.** This is an independent community project. It is not affiliated with,
authorised by, or endorsed by Anthropic.
