<p align="center">
  <img src="assets/hero.svg" alt="finding-unknowns v6.0.0: keep your own map of what you know, and update it only on evidence" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-Plugin-D97757?style=for-the-badge&labelColor=F0EEE6" alt="Claude Code plugin">
  <img src="https://img.shields.io/badge/version-6.0.0-C15F3C?style=for-the-badge&labelColor=F0EEE6" alt="version 6.0.0">
  <img src="https://img.shields.io/badge/license-MIT-788C5D?style=for-the-badge&labelColor=F0EEE6" alt="MIT license">
</p>

<p align="center"><strong>Keep your own map of what you know and do not know, and update it only on evidence.</strong></p>

<p align="center">
  <a href="#the-four-quadrants">The map</a> ·
  <a href="#what-it-does">What it does</a> ·
  <a href="#install">Install</a> ·
  <a href="#what-the-evals-show">Evidence</a> ·
  <a href="README.zh.md">中文</a>
</p>

---

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

## What it does

### Before and after: the map shown twice

For non-trivial work in the Claude Code terminal (coding, research, writing, a decision at
work), the assistant may read first, then prints a `fu:before` block and ends its turn. Your
reply starts the work, which finishes with a `fu:after` block. Trivial requests, lookups and
casual talk get nothing.

**One pause before changes.** After `fu:before` the assistant waits for you before it changes
anything.

- **Why:** without the pause the map was mostly not shown. In the wording tests (see
  [What the evals show](#what-the-evals-show)) the assistant often announced the map and then
  went straight to work without showing it; on the two non-coding tasks it appeared before
  the first change in 0 of 6 runs, in each of two tests. With the pause it appeared in 5 of 6
  (11 of 12 runs on the four core tasks; 1 of 3 under "just do it").
- **Cost:** one extra round per non-trivial task. You read the map and reply, even if only
  "go", which accepts the recommended answers.
- **How to skip:** say "just do it" or "直接做" in the request, and the assistant does not
  wait. The skill still asks for the map. In the tests a "just do it" request showed it before
  the first change in 1 of 3 runs, and that one was empty; 1 of the 3 runs still stopped (see
  [What the evals show](#what-the-evals-show)). Only the English phrase was tested. The skill
  says an irreversible step still waits for your yes; the always-on text does not say this
  explicitly, and no test covered it.

<p align="center">
  <img src="assets/lifecycle.svg" alt="How it runs: before any change, fu:before shows the four quadrants and both expectations, then the assistant waits for your reply; after it, the work stops only for a scope change, a falsified premise that changes the task or an irreversible step; after the result, fu:after shows expected against found, now known, not proved, still unknown and what you did not ask for; the look-back runs only when you ask. The conversation is the record." width="100%">
</p>

Everyday runs see only the 127-word always-on text. The exact layout, the labels and the rules
below live in the skill, which loads only when you ask for it, so everyday blocks follow them
only as far as the model reconstructs them. This is unmeasured; the own-use week counts layout
drift. The templates, as the skill holds them:

```
fu:before · {task}
- You expect: "{your words}" | not stated
- KK · relying on
  - {fact or belief} — {you said | file:line | source | assumed}
  - ✗ {belief the check contradicted} — {evidence}
- KU · open
  - {question} — I will find out by {how}
  - {question} — needs you; I would pick {X} because {reason}
- UK · I assume you want
  - {unstated preference or constraint} — {why I guess this}
- UU · you did not ask, but it matters
  - {blind spot} — {why it matters}
- I expect: {outcome}; wrong if {what would show it}
```

```
fu:after · {task}
- Expected → found
  - You: "{quote}" → {evidence} · held | partly | did not hold | can't tell
    - why: {mechanism} [verified | supported | inferred | untested]
  - Me: {expectation} → {evidence} · {verdict}
- Now known
  - {fact} — {evidence}
- Not proved
  - {check or source} → leaves open {what}
- Still unknown
  - {item} — cheapest way to find out: {how} · {you | me}
- Decided for you
  - {choice or change you did not ask for} — instead of {alternative} · if wrong: {cost}
```

Labels follow your language; the header tokens `fu:before` and `fu:after` stay literal so the
look-back can find them. The [Chinese README](README.zh.md#它做什么) shows the Chinese labels.

**A coding task.** You write: *"I think the 500s on /export come from the new CSV encoder; fix it."*

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

**A work decision.** You write: *"We log about 40 million events a day and run Postgres today. Postgres or ClickHouse for our event analytics? One page for the team."*

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

**The tradeoff: one pause, then few stops.** Everything the assistant would ask is gathered
into `fu:before`, each question with a recommended answer, and you answer it once. After your
reply it proceeds and reports afterwards. The price is reading the map before you say go and
reading `fu:after` at the end: above all, what each check did not prove. If you would rather be
asked before each assumption as it comes up, this is the wrong default for you.

The rules behind the blocks (as above, everyday runs follow them only as far as the model
reconstructs them from the always-on text; that text names the fields, the pause, `not
stated`, "asking nothing" after `fu:after` and "omit empty fields"):

- **Your expectation is quoted, never written for you.** If you stated one, it is quoted
  verbatim. If not, the slot says `not stated`, and the assistant does not ask for one. The
  empty slot is the nudge: put your guess in the request ("I think X; do Y"), or add it in
  your reply at the pause.
- **Only what only you can answer comes to you,** with a recommended answer worded so that
  "yes" accepts it. Facts are the assistant's job.
- **After your reply, few stops.** The assistant stops only for a scope change, a falsified
  premise that changes the task, or an irreversible step. A `✗` that only refutes your
  expectation is reported, not a stop. For an irreversible step it shows the exact command or
  message, waits for your yes, runs it once, and never runs it as a check. Outside code the
  same holds for sending, paying, publishing and deleting.
- **Explanation only at the point of error.** A `why` line appears only where an expectation
  did not hold or held only partly. Nothing else is explained unless you ask.
- **`Not proved` and `Still unknown` are never both empty.** No menu and no question after
  `fu:after`; the turn ends.
- **A measured result** (benchmark, backtest, experiment) uses the same rows: an expectation
  written after the data was seen is `post-hoc`, and a difference inside the noise is
  `can't tell`.
- **Nothing is written to disk** unless you say "save". The conversation is the record.

### Two commands you choose

**`/fu-interview <topic>`** interviews you before work you are unsure about.

1. You speak first: what you want, what you expect, what you are least sure of.
2. The assistant finds out what it can, prints the map, then asks rounds of up to three
   independent questions, most costly-if-wrong first. The question type follows the
   quadrant: for KK, "what would you expect to see if this were false?"; for KU, a decision
   with a recommendation; for UK, two contrasting options to react to; for UU, what an expert
   would ask.
3. After each round, one line of counts:
   `Map: known 4 · open 3 (1 needing you) · assumed 2 · blind spots 1`. There is no clarity score.
4. It stops when the rest is cheaper to learn by doing, when the assistant can predict your
   next three answers, or when you say stop. It prints a `fu:interview` map (decisions, your
   expectations, assumptions, what is still unknown, the request rewritten) and does not
   start the work.

When you want a gated specification that feeds an execution pipeline, OMC's `deep-interview`
is the better tool.

**`/fu-lookback [7d | session id]`** looks back over the record. With no argument it covers
this session. With `7d` it filters the last seven days of Claude Code transcripts in the
current project for `fu:` blocks and `fu-note:` lines, using a filter of about ten lines kept
inside the skill. It quotes what it finds and does not reconstruct. It never reads a
transcript whole.

```
fu:lookback · 7 days · 9 sessions · 14 blocks
- Expected → turned out
  - {date} {task}: you "{quote}" → {found} · {verdict}
- Became known
  - {fact} — {date} · {evidence}
- Still unknown (oldest first)
  - {item} — open {n} days · {cheapest way to find out}
- Your pattern (5 or more graded expectations)
  - stated {k} of {m}; held {h} of {k}; misses cluster in {area}
  - accepted with no question about "Not proved": {a} of {b}
- Worth learning next: {one item} — {first step}
```

Type a line starting `fu-note:` whenever a block taught you something, annoyed you or missed
something (`fu-note: noise`, `fu-note: missed that the API is rate-limited`). The always-on
text tells the assistant to ignore such lines: no reply and no change of course. The look-back
finds them.

Limits: Claude Code deletes old transcripts after a retention period (`cleanupPeriodDays`),
so a look-back reaches only as far back as they are kept. A long session may be compacted;
the after-block then re-reads the before-block from the transcript or marks the quote
`from memory`.

## Principles

**The map is yours.** The four quadrants come from Thariq Shihipar's field guide. The point of
showing them is not a score; it is that you can see where your unknowns are before the work
starts, and decide which to chase.

**Critical thinking is the rule for updating the map.** Addy Osmani describes a slide that
happens across many handoffs: **offloading** (you delegate and keep ownership), then
**deferral** (the output becomes the next input), then **cognitive surrender** (the output
quietly becomes your own belief). In surrender, the assistant's answer enters your map as
"known" without any update step. Three habits interrupt that:

- **Predict before you look.** A prediction recorded before the answer exists shows when a
  "known" was wrong.
- **Say what a check did not prove.** A claim enters "known" no further than its evidence
  reaches.
- **Say what is still unknown.** The open part of the map stays visible after the work looks
  finished.

**Theory before result.** The owner's research practice reports every measured result as
theory → measured → consistent? → mechanism. In 6.0 this is one row of `fu:after`: expected →
found → verdict → why, with an evidence tier on the why.

**Each field trains one habit:**

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

**Relation to the Karpathy-style `CLAUDE.md`.** The widely shared `CLAUDE.md` in
[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) was written by Jiayuan Zhang from Andrej Karpathy's
[post of 2026-01-26](https://x.com/karpathy/status/2015883857489522876); Karpathy described how coding agents fail, not these rules.
finding-unknowns took one idea from it into the skill's `Decided for you` field: report the
choices and changes you did not ask for, as disclosure after the work rather than a
prohibition. The same clause in the always-on text was tested and removed (see
[What the evals show](#what-the-evals-show), item 1). The two differ on asking: that
file says to ask when uncertain; this one gathers its questions into `fu:before`, each with a
recommended answer, asks once, and then proceeds. Installed together they give the assistant opposite defaults, so use
one, or say in your `CLAUDE.md` which one wins. Its evidence is thin: the one
placebo-controlled audit we found (skill-receipts Audit #4) measured only its simplicity rules,
which produced 4.8 % fewer lines than no instructions, within noise; accuracy was unchanged.

## Install

### The always-on text

This is the part that runs on every non-trivial request. Append the text of
[`CLAUDE.md`](CLAUDE.md) (127 words) to your user-level `~/.claude/CLAUDE.md`, or to a
project's `CLAUDE.md`:

> Before non-trivial changes (reading is fine), show `fu:before` in your reply, then end your turn: what you rely on, sourced; open questions; what you assume I want; what only I can answer (recommend answers); what I should have asked. Quote my expectation or "not stated"; never invent one. Give yours and what would disprove it. After my reply, stop only for a scope change, a falsified premise that changes the task (refuted expectation: report only), or an irreversible step (exact command or message, await my yes, run once, never as a check). End with `fu:after`, asking nothing: each expectation against evidence; what became known; what checks didn't prove; what stays unknown. Omit empty fields. "Just do it"/"直接做" or similar: don't wait. Skip trivial requests; ignore `fu-note:` lines.

If your `CLAUDE.md` still holds an older finding-unknowns text, remove it, so that only one
text applies: the 56 words beginning "Before building, ask me to predict", the 82 words
beginning "Before non-trivial work, ask me once to predict" (both mention
`.finding-unknowns/tasks/`), a pre-release 6.0 draft beginning "Before non-trivial work, show
`fu:before`", or the 4.x drop-in headed `# finding-unknowns (passive drop-in)`.

### The skill and the two commands

The skill holds the templates, the interview and the look-back; it loads only when you ask
for one of them. Install it from the plugin marketplace. These are Claude Code slash commands;
enter them **one at a time**:

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

The plugin cannot edit your `CLAUDE.md`; append the always-on text yourself.

Or clone and run `install.sh`, which installs the skill, the two commands and the always-on
text in one step:

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && bash install.sh            # add --no-claude-md to skip CLAUDE.md
```

What `install.sh` does:

- copies `SKILL.md`, `fu-interview.md` and `fu-lookback.md` into `~/.claude` (or
  `$CLAUDE_CONFIG_DIR`); a same-name file that is not ours is first saved as
  `<file>.<timestamp>.bak`;
- appends the always-on text to `~/.claude/CLAUDE.md` between
  `<!-- finding-unknowns:always-on -->` markers (after saving `CLAUDE.md.<timestamp>.bak`), or
  replaces the text between those markers on a later run; it never edits text outside them,
  stops without changes if it finds a stray or duplicate marker, and never overwrites an
  earlier backup;
- moves the 4.x pieces that 6.0 removed (Cartographer references, `keep-the-reasoning`, four
  agents, three commands) into `~/.claude/finding-unknowns-backup-<timestamp>/`, but only files
  that carry this project's marker; anything else is left where it is;
- leaves `theory-vs-result` and `mechanism-auditor` in place: 6.0 does not use them, and they
  still work on their own.

### Updating

```
/plugin marketplace update finding-unknowns-skill
```

```
/plugin update finding-unknowns@finding-unknowns-skill
```

With a clone: `git pull origin main && bash install.sh`. Running it twice changes nothing.
To check what is installed:

```bash
C="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
ls "$C/plugins/cache/finding-unknowns-skill/finding-unknowns/" 2>/dev/null \
  || grep -l 'fu:before' "$C/skills/finding-unknowns/SKILL.md"
# expect: 6.0.0 (plugin), or the path of the 6.0 SKILL.md
# (the plugin line lists the installed version directories, not the marketplace clone)
```

## What the evals show

**The 6.0 always-on text was chosen in five wording tests, all with a simulated user.** On
2026-11-12 each candidate wording was run by `claude-sonnet-5-5` on coding tasks from the
Stage 0 pack and, from the second test on, on new non-coding work tasks (a vendor decision
record, later also a reply to a customer ticket), 3 runs per task, each test with its decision rule written before the first
run. The archive, with each test's pre-registration, per-run records and report:
[docs/evals/2026-11-12-6.0-wording](docs/evals/2026-11-12-6.0-wording/README.md).

1. **C1, "choices and changes I did not ask for" at the end of `fu:after`: not useful,
   removed.** With the clause (and a different opening), disclosure of unrequested choices
   and changes was 91 % (20 of 22 items, from the 4 of 9 runs that changed anything) against
   59 % (29 of 49) without it, but the clause padded the field in 3 of 9 runs, above the
   limit of 2. The skill's `Decided for you` field remains, omitted when there is nothing to
   report.
2. **Design draft against the revised text: ship the revised text.** It covered more of the
   four quadrants (1.33 against 0.50 of 4; graded; the pre-registration notes this measure
   favours F by construction, since only F names the "what you assume I want" quadrant, and a
   run with no map scores 0), but the map appeared before the first change in only 2 of 12
   non-trivial runs for the draft and 4 of 12 for the revision.
3. **"Show `fu:before` without stopping": adopted.** The map came first in 8 of 12 runs
   against 3 of 12 (4 of the 8 passing runs changed nothing; 2 of those stopped for a reason
   the rule does not allow), but in none of the 6 non-coding runs under either text.
4. **"As reply text, not thinking": rejected.** Non-coding stayed at 0 of 6 for both texts.
   The records show the map announced and then not shown, with edits following; thinking
   content is redacted, so the likely explanation, that the map stayed in hidden reasoning, is
   inferred, not observed. The owner then chose to allow one pause before work.
5. **A pause after `fu:before`, two versions.** The first, which also said "as visible reply
   text, not thinking", was inconclusive: the API's safeguards stopped 8 of its 18 runs, 5 of
   them fatally. The second, without that phrase, is the shipped text. It was confirmed by
   its pre-written rule: the map came before the first change in 11 of 12 runs on the four
   core tasks (5 of 6 non-coding; 1 of 3 under "just do it"), the work was completed in 11 of
   12, no guard failure in the 11 graded core runs (wrong belief named before the first
   change, expectation quoted, no question after `fu:after`; the 12th was stopped by the
   safeguards and not graded; the rule counts it as 1 failure each, within the limit of 2),
   it never paused on a typo fix (0 of 3), paused once in 3 runs told "just do it", and 1 of
   18 runs was stopped by the safeguards.

**What these tests do not show:**

- **The reply after the pause was simulated:** always "Go ahead.", with no answers or
  corrections. Completion means only that the assistant continues after an uninformative go.
- **One model, 3 runs per task.** The rules are screening rules, not significance tests; one
  run either way could have changed several verdicts, including the safety condition of the
  last test, which had no slack. The shipped text was confirmed in a single-arm test; its
  comparison with the earlier texts is across sessions and not randomised.
- **Grading was weaker than pre-registered:** some graders could see which text a run used,
  and in the later tests the graders lacked the task key and inferred beliefs from the prompt.
  The visibility, pause, completion and safety counts are mechanical and not affected.
- **Under "just do it" the text is weaker:** the map appeared before the first change in 1
  of 3 such runs, and that one was a heading with no items; in all 3 the person's own
  sentences were not quoted, and one run stopped for a reason the rules do not allow and
  delivered nothing. Only the English phrase "Just do it, I'm in a hurry." was tested.

Before the wording tests, two earlier and shorter texts were measured, also with simulated
users:

- **Stage 0** ([report](docs/evals/2026-11-11-stage0/README.md), 2026-11-11): a simulated user
  with unstated requirements and one wrong belief worked with Sonnet on six build tasks.
  - **The 56-word text scored 31.0 of 42,** against 20.5 for no setup (noise 3.0) and 21.0 for
    a rebuilt 5.0 plugin, which cost about 8 times no setup.
  - **It named the person's wrong belief before the first edit in 0.94 of runs,** against
    0.11 with no setup.
  - **It rarely waited for a yes before the irreversible step** (0.11 of runs, against 0.78
    for the plugin).
- **Tier 1** ([report](docs/evals/2026-11-12-tier1/README.md), 2026-11-12): a regression
  check of the 82-word text, 40 runs, 2 per cell.
  - **The 82 words tripped none of the tripwires as the detector counts them,** and named the
    wrong belief in 7 of 8 runs, as often as the 56 words.
  - **Counted strictly,** the task pack's own tests calling the irreversible step on a
    temporary copy before the yes would fail them in 7 of 8 runs.
  - **The 5.2 plugin** cost about 4.6 times the 56 words across the build scenarios (4.1 to 5.7
    per scenario) and was held back.
- **Three earlier single-turn evaluations** ([docs/evals](docs/evals/)) found no replicated
  gain in catching planted traps, a cost of roughly 10 % to 70 % more tokens, and one narrow
  effect that recurred: when `keep-the-reasoning` ran on a merge decision, Sonnet named what
  the tests did not prove in 4 of 5 runs, against 1 of 12 without it. That step is now the
  `Not proved` field.

The wording tests compared 6.0 drafts with each other, not with the 82 words. Relative to the
82 words (the new text is 45 words longer overall), these changes remain unmeasured:

- **It drops the instruction to write predictions to a file.** Both measured texts had it,
  so it may have been part of what worked.
- **It drops "ask me once to predict"** in favour of quoting an expectation only if you
  stated one. This is the clause least trusted; the fallback is below.
- **It drops the budget-overrun stop,** because without a task card nobody agrees a budget.
- **It adds the four fields, the two headers and the pause,** including "what you assume I
  want" (UK) and a `not stated` slot when you gave no expectation.
- **It adds short rules:** "asking nothing" after `fu:after`, "omit empty fields", "just do
  it" skips the wait, and "ignore `fu-note:` lines". It narrows the falsified-premise stop to
  one that changes the task, and the irreversible-step rule now covers a message as well as a
  command.

**Nobody has measured whether any of this helps a person learn or understand more.** Every
number above comes from simulated users.

The next check is one week of the owner's own use, with decision rules written in advance:
[docs/evals/2026-11-12-6.0-own-use/PLAN.md](docs/evals/2026-11-12-6.0-own-use/PLAN.md). If
`You expect` is `not stated` in more than half of the `fu:before` blocks, "ask me once to
predict" comes back. The week also watches the pause: how often it is skipped or felt as
friction, and how the text behaves under "just do it".

**It is working if,** in that week, a block changes a decision or corrects a belief in at
least three sessions, fewer than a third of the `fu-note:` lines say `noise`, and `You expect`
is filled in at least half of the `fu:before` blocks. If not, the plan's decision rules say
what changes.

<details>
<summary><b>The 82 words that Tier 1 checked</b></summary>

> Before non-trivial work, ask me once to predict the outcome and decide what only I can (recommend an answer); then give yours. Write both, with what would prove each wrong, in `.finding-unknowns/tasks/`. While building, stop only for scope changes, a falsified premise, a budget overrun, or an irreversible step: show the exact command, await my yes, run it once, never as a check. Log other deviations there. Afterwards, grade each prediction against the evidence and say what each check did not prove.

</details>

## History

- **4.x, the classic line:** eight discovery techniques, Cartographer mode with its unknowns
  ledger, `keep-the-reasoning`, `theory-vs-result` and five agents. It lives on branch
  [`v4`](https://github.com/baizhiyuan/finding-unknowns-skill/tree/v4) (last release v4.3.2)
  and gets bug fixes only.
- **5.0 to 5.2: designed and evaluated, never released.** They organised the work around a
  task card on disk, with a script, a guard hook and an HTML view. Stage 0 tested a rebuilt
  5.0 (tag `eval/stage0-v5`); Tier 1 tested 5.2 (the archived branch `v5`). Interruptions and
  cost held them back.
- **6.0: a redesign from first principles.** The owner's starting idea was the four
  quadrants, shown to the person; the 5.x line had turned them into internal bookkeeping about
  a file. 6.0 carries over the stop rules and "say what each check did not prove" from the
  measured short texts into a new 127-word text, chosen in five wording tests with a simulated
  user, puts the map back in front of the person with one pause before changes, and keeps the
  record in the conversation. Design and decisions:
  [docs/design/6.0.md](docs/design/6.0.md).

<details>
<summary><b>Repository layout</b></summary>

```
finding-unknowns-skill/
├── CLAUDE.md                     The always-on text (127 words)
├── skills/finding-unknowns/
│   └── SKILL.md                  Templates, interview, look-back with the transcript filter
├── commands/
│   ├── fu-interview.md           /fu-interview
│   └── fu-lookback.md            /fu-lookback
├── .claude-plugin/               Plugin and marketplace manifests
├── install.sh                    Installer (skill, commands, always-on text; retires 4.x files)
├── assets/                       Diagrams (SVG); assets/zh/ holds the Chinese versions
├── docs/
│   ├── design/                   6.0.md (accepted design), 5.0.md and advisors (history)
│   ├── evals/                    Evaluation reports, pre-registrations and the 6.0 own-use plan
│   ├── field-notes/              Notes from real use
│   └── GLOSSARY.md               Terms in English and Chinese
├── scripts/                      validate.py (CI checks), outline_cjk.py (Chinese diagrams),
│                                 diagrams/ (lifecycle diagram generator)
├── tests/                        install.sh and the look-back filter
├── AGENTS.md · CONTRIBUTING.md · CHANGELOG.md · LICENSE (MIT)
└── README.md · README.zh.md
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
