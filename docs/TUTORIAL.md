# 5-minute tutorial

One task card from start to finish: the Brief, a stop, a catch-up in the next session,
and the completion report. [中文版](TUTORIAL.zh.md)

> **An illustration, not a recorded run.** The task, the numbers and the replies are
> invented to show the shape; the card itself passes `fu lint`. Your wording will differ;
> check the shape. Whether this loop helps people is untested
> ([README](../README.md#what-the-evals-showed)). If you only want the habit, the 56 words
> in [`CLAUDE.md`](../CLAUDE.md) are the measured setup and need no install.

## 1. Install (1 minute)

Until v5.2.0 is released, install 5.2 from branch `v5` (the marketplace still serves
v4.3.2):

```bash
git clone https://github.com/baizhiyuan/finding-unknowns-skill.git
cd finding-unknowns-skill && git checkout v5 && bash install.sh
```

After the release, the plugin route also installs the guard hook:

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

You get one skill, one agent (`mechanism-auditor`), the `fu` script and four commands:
`/fu-brief`, `/fu-catch-up`, `/fu-debrief` and `/fu-view`. The script needs `python3`.

## 2. Brief (2 minutes)

The task: a nightly job exports the `orders` table to CSV in 10,000-row batches. When it
crashes, it starts over. You want it to resume.

```
/fu-brief make the nightly order export resumable after a crash; I'd like to learn this part
```

The agent reads the repository silently. Then it sends **one** message with at most three
questions. Your prediction comes with no suggested answer, so nothing anchors it; a
decision only you can make comes with a recommendation worded so "yes" accepts it:

```
1. If the export crashes halfway and resumes, how long will the resumed run take,
   compared with today's full run? Confidence: low, medium, high, or no idea.
2. Where should the checkpoint live? A local file next to the CSV, or a row in the
   database. Recommendation: the local file (easiest to undo). Yes?
```

You answer: "A full run is about 6 minutes, so roughly 3. Medium. And yes." Your words go
on the card verbatim, and your answer to question 2 goes into
`.finding-unknowns/decisions.md`, so it is never asked again. Only then does the agent
write its own prediction. It shows the Brief in full and ends with one approval ask
(open decisions, and here, because you may stop and resume, an offer of the HTML view).
On your yes, `fu freeze` commits it:

```
# export-resumable
Goal: a crashed nightly export resumes where it stopped · State: building
Needs you: nothing
Mode: learn · Last seen by you: never
Timing: Brief frozen 2026-11-12 09:10, commit 3f9c2ab

## Brief (frozen 2026-11-12 09:10)
Approach:
  - checkpoint the last exported (created_at, id) after each batch because the job already writes in batches
  - keep the checkpoint in a local file because you chose the most reversible place
P1 (you · medium) "a full run is about 6 minutes, so resuming from halfway takes roughly 3"
  - falsifier: resuming from halfway takes 6 min or more on the 5M-row fixture
  - should not change: an uninterrupted run's row count and checksum
A1 (agent · medium) "created_at repeats across batch boundaries, because the importer stamps a whole import with one time"
  - falsifier: no repeated created_at at any batch boundary in the fixture
  - should not change: rows with unique timestamps keep today's order
Stop-points: irreversible · scope · dead-premise · budget > 2× 1 h
C1 each row is exported exactly once after a crash
  - check: `pytest tests/test_export_resume.py -q` kills the job at 3 batch boundaries and compares ID sets with a full run
  - does NOT prove: a crash between writing a batch and writing its checkpoint
  - lane: reversible
Check files: tests/test_export_resume.py
```

P1 is about something the agent does not control: how the database behaves. "The tests
pass" is something the agent makes true, so it is a contract check (C1), with what it
does not prove. Nothing on this Brief is irreversible, so there is no `Irreversible:`
line; if there were, the guard hook would ask before that exact command ran.

## 3. A stop-point (30 seconds)

The build is quiet: small choices become one line each in `export-resumable.deltas.md`,
and a decision made for you says what it costs if wrong. Late in the session the agent
stops:

```
Stop (scope): resume from 50 % took 9 min 40 s on the fixture (D4); an index on
(created_at, id) brings it to 3 min 05 s, but that index is on production, outside the
Brief · `CREATE INDEX CONCURRENTLY orders_created_at_id ON orders (created_at, id);`
· recommend: run it in the next maintenance window
```

The index is a scope change and also irreversible (production). It was not on the frozen
Brief, so the guard has no line to match: the agent stops, and only your chat yes to that
exact command would run it. You reply: "Not now; I'll run it in Thursday's maintenance
window." It goes to Open, unexecuted. Had you said yes, the agent would add it under a dated
Amendment with an `Irreversible:` line, and the guard would then ask before it runs.

## 4. Next session: `/fu-catch-up` (30 seconds)

```
/fu-catch-up
```

```
export-resumable · building
  - since you last looked: D1–D4 (checkpoint format, a lock retry, the fixture, the slow resume)
  - needs you: nothing; the production index is in Open for Thursday
```

You see only what changed since you last looked, and Last seen moves to D4. There are no
recall questions unless you ask for them.

## 5. The completion report is the Debrief (1 minute)

When the work is done, the completion report is the Debrief. You asked for a fresh grade
when you approved the Brief, so `mechanism-auditor` grades from the frozen card and the
artifacts; it never sees the transcript or the builder's claims. Evidence comes first,
then your prediction:

```
Evidence:
  - `pytest tests/test_export_resume.py -q` → 3 passed
  - `bench/resume.sh` → 9:41, 9:22, 9:58
P1 (you · medium) "a full run is about 6 minutes, so resuming from halfway takes roughly 3"
  - measured: 9 min 40 s over 3 runs, ±20 s (logs/resume.txt)
  - consistent?: inconsistent
  - mechanism: each batch is a separate query that sorts the table, since no index matches the sort [verified]
A1 (agent · medium) "created_at repeats across batch boundaries, because the importer stamps a whole import with one time"
  - consistent?: consistent
Integrity:
  - Brief vs freeze: unchanged
  - Check files: unchanged
  - Unlogged hunks: none
Did NOT prove:
  - C1 kill tests → leaves open: a crash between a batch write and its checkpoint · still holds: no duplicates or gaps at 3 boundaries
Not checked:
  - the production row count and its existing indexes
Model changes:
  - You expected resuming from halfway to take half a full run → without an index it is slower than a full run, because each batch re-sorts the table [shown, not confirmed]
Bottom line:
  - holds: the checkpoint needs the id as well as created_at (A1)
  - did not hold: resuming from halfway is faster than a full run (P1)
  - stops at: the fixture; nothing ran on production
Needs you: the production index (recommendation: run it in Thursday's maintenance window; settles whether resume is fast in production)
```

Consistent rows are one line; the explanation sits on the row that missed. Because you
asked to learn, the miss also gets a short why with one example: today's job reads the
table once through one cursor, while a resumable job asks "rows after this key" for each
of the 250 remaining batches, and with no index matching the sort, each of those queries
sorts all 5M rows.

`fu integrity` wrote the three Integrity lines; `fu log` added one line per graded
prediction to your local prediction log; `fu freeze` committed the card again. Say the
model change back in your own words and it becomes `confirmed`. `/fu-view` (or the view
you accepted at the Brief) renders the same card as a page.

## When not to use it

Typos and one-liners get no card and no question. A task with nothing honestly
predictable gets a card that says so; "no real prediction here" is a valid answer.

## Next

[README](../README.md) · [Glossary](GLOSSARY.md) · [Architecture](ARCHITECTURE.md) ·
[EXAMPLES.md](../EXAMPLES.md) (copy-paste prompts) · [5.2 design](design/5.2.md)
