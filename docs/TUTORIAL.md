# 5-minute tutorial

One task card from start to finish: brief, a stop, a catch-up in the next session, a
debrief. [中文版](TUTORIAL.zh.md)

> **An illustration, not a recorded run.** The task, the numbers and the output are
> invented to show the shape. Your wording will differ; check the shape. Whether this
> loop helps people is untested ([README](../README.md#what-the-evals-show)).

## 1. Install (1 minute)

In Claude Code:

```
/plugin marketplace add baizhiyuan/finding-unknowns-skill
```

```
/plugin install finding-unknowns@finding-unknowns-skill
```

You get one skill, three agents and three commands: `/fu-brief`, `/fu-catch-up`,
`/fu-debrief`. Other install routes are in the [README](../README.md#quick-start).

## 2. Brief (2 minutes)

The task: a nightly job exports the `orders` table to CSV in 10,000-row batches. When it
crashes, it starts over. You want it to resume.

```
/fu-brief make the nightly order export resumable after a crash
```

On first use in a project the agent asks once: `ship` or `learn`. Choose `learn`. Then,
before it reads any code, it asks for your prediction:

```
Before I look: if the export crashes halfway and resumes, how long will the resumed
run take, compared with today's full run? Give a confidence, or say "no idea".
```

You answer: "A full run is about 6 minutes, so roughly 3. 70 %." That is your prior. Only
now does the agent map the territory, report what contradicts your prior, and give its
own prediction. After your yes, the card is frozen and committed. Abridged:

```
# Make the nightly order export resumable
Goal: a crashed export resumes where it stopped · State: building
Next decision that needs you: none
Mode: learn · Last seen by you: 2026-11-12, at the Brief
Timing: Brief frozen 2026-11-12, commit 3f9c2ab

## Brief (frozen 2026-11-12)
Approach: checkpoint the last exported (created_at, id) after each batch, because the
  job already writes in batches
Your predictions:  P1 resuming at the halfway point takes about half of today's 6 min
  (70 %) · falsifier: resume ≥ 6 min on the 5M-row fixture · should not change: an
  uninterrupted run's row count and checksum
Agent predictions: A1 created_at repeats across batch boundaries; the importer stamps
  a whole import with one time (importer.py:88) · falsifier: no repeat at any boundary
  in the fixture · should not change: rows with unique timestamps keep today's order
Stop-points: irreversible action · scope change · dead premise · budget > 2× 1 h
Contract:
| claim | check (can fail) | does NOT prove | lane |
| each row exported exactly once after a crash | tests/test_export_resume.py kills the
  job at 3 batch boundaries, compares ID sets with a full run | a crash between writing
  a batch and writing its checkpoint | reversible |
```

P1 is about something the agent does not control: how the database behaves. "The tests
pass" is something the agent makes true, so it sits in the contract, with what it does
not prove.

## 3. A stop-point (30 seconds)

The build is quiet: small choices become one-line deltas on the card. Late in the session
the agent stops:

```
Stopped: scope change, production (irreversible lane).
D4 surprise: resume from 50 % took 9 min 40 s on the fixture (3 runs, ±20 s)
  → logs/export-resumable-resume.txt
No index matches ORDER BY created_at, id. With that index on the fixture: 3 min 05 s.
The fix is an index on production, outside the Brief. Run this yourself, or say yes
to this exact command:
  CREATE INDEX CONCURRENTLY orders_created_at_id ON orders (created_at, id);
Post-check: EXPLAIN on the batch query shows an Index Scan.
```

Two stop-points fired at once: the change is outside the Brief, and it touches
production, which is irreversible. The agent only prepared the exact command; you run it
or say yes to that one command. You leave. Nothing ran on production; the card reads
`waiting on you`.

## 4. Next session: `/fu-catch-up` (1 minute)

```
/fu-catch-up
```

Recall comes before the card (learn mode: two or three questions; ship mode: one,
skippable):

```
1. What does the checkpoint store, and why not created_at alone?
2. Your P1 expected about 3 minutes; the resume took longer than a full run.
   Where would you look first?
```

A two-sentence teach-back counts instead; there is no pass mark. Then you see only what
changed since you last looked: deltas D1 to D4 and the next decision, the index. You
reply "Not now; I'll run it in Thursday's maintenance window." It goes to Open,
unexecuted, and Last seen moves to D4.

## 5. `/fu-debrief` (1 minute)

```
/fu-debrief
```

A fresh context (`mechanism-auditor`) receives the frozen card and the artifact paths,
not the build transcript. Your prediction is graded first:

```
Evidence: `pytest tests/test_export_resume.py -q` → 3 passed · `bench/resume.sh` →
  9:41, 9:22, 9:58
Graded by: fresh context.

| ID | Prediction (quoted) | Measured | Consistent? | Mechanism [tier] |
|----|---------------------|----------|-------------|------------------|
| P1 | "resuming at the halfway point takes about half of today's 6 min" | 9 min 40 s, 3 runs ±20 s; full-run checksum unchanged | inconsistent; should-not-change half held | each batch is its own query and sorts the table [verified: with the index, 3 min 05 s] |
| A1 | "created_at repeats across batch boundaries" | at 37 of 499 boundaries | consistent | one timestamp per import [supported] |

Why P1 missed: today's job reads the table once, through one cursor. A resumable job
asks "rows after this key" for every batch; with no index matching the sort, each of
the 250 remaining queries scans and sorts all 5M rows. Resuming skips batches, but each
batch became far more expensive.

Did NOT prove: a crash between a batch write and its checkpoint; the resume test was
  written in the same context as the code
Not checked: the production row count and its existing indexes
Model changes: you expected resume ≈ half a full run → without the index it is slower
  than a full run, because each batch re-sorts the table [shown, not confirmed]
Bottom line: resume is correct (no duplicates or gaps in 3 kill tests) and slow until
  the index exists.
Needs you: the production index (Open)
```

Read the table as Theory → Measured → Consistent? → Mechanism: P1 is inconsistent and A1
consistent; their mechanisms are tagged verified and supported. The explanation sits on
the row that missed, not in a lecture up front. Each graded
prediction adds one line to your personal prediction log, and the card is committed
again. Say the model change back in your own words and it becomes `confirmed`.

## When not to use it

Typos and one-liners get no card and no question. A task with nothing honestly
predictable gets a card that says "No real prediction here; contract only".

## Next

[README](../README.md) · [Glossary](GLOSSARY.md) · [Architecture](ARCHITECTURE.md) ·
[EXAMPLES.md](../EXAMPLES.md) (copy-paste prompts) · [5.0 design](design/5.0.md)
