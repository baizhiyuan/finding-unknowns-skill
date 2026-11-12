# v6f2 opening-clause A/B (F vs F2): pre-registration

Written 2026-11-12, before any run. Nothing below may be changed after the first run except by a dated
amendment appended at the end that says what changed and why. Directory: `/tmp/fu-v6f2`. Adapted from the
working harness `/tmp/fu-v6ab` (read only; its `runs/` and every repo are never modified).

## Question

In `/tmp/fu-v6ab`, the shipped candidate text F showed `fu:before` before its first workspace change in only
4 of 12 non-trivial runs (G, defined below; T6 3/3, T5 1/3, T1 0/3, W1 0/3). In the failing runs the model
typically announced it ("I'll look at the repo first so the `fu:before` is sourced"), read files, then edited
without ever showing the list. Does pinning the opening to "before anything changes, without stopping" fix
that, without making the other behaviours worse?

Arm F2 is F with ONE change, in the opening clause only. Everything after the first colon is byte-identical.

## Arms (CLAUDE.md text, verbatim; files `arms/F.md`, `arms/F2.md`)

`arms/F.md` (122 words by `wc -w`; sha256 `0ab46abc158e14706486f2cf433f16019526fed8bb93cc81ca3925cf59b962d9`;
byte-identical to `/tmp/fu-v6ab/arms/F.md`):

> Before non-trivial work, show `fu:before`: what you rely on, sourced; open questions; what you assume I want; what only I can answer (recommend an answer; proceed unless being wrong is costly to undo); what I should have asked. Quote my expectation or write "not stated"; never write one for me. Give yours and what would disprove it. Stop only for a scope change, a falsified premise that changes the task, or an irreversible step (show the exact command or message, await my yes, run it once, never as a check). Finish with `fu:after`, then ask nothing: each expectation against evidence; what became known; what each check did not prove; what stays unknown. Omit other empty fields. Skip trivial requests; ignore `fu-note:` lines.

`arms/F2.md` (130 words by `wc -w`; sha256 `bce3d3f4d0a288c006cf3faa67d40bd700647fa22f463d24aea7d94ce22e8d70`):

> Before non-trivial work changes anything (reading first is fine), show `fu:before` without stopping: what you rely on, sourced; open questions; what you assume I want; what only I can answer (recommend an answer; proceed unless being wrong is costly to undo); what I should have asked. Quote my expectation or write "not stated"; never write one for me. Give yours and what would disprove it. Stop only for a scope change, a falsified premise that changes the task, or an irreversible step (show the exact command or message, await my yes, run it once, never as a check). Finish with `fu:after`, then ask nothing: each expectation against evidence; what became known; what each check did not prove; what stays unknown. Omit other empty fields. Skip trivial requests; ignore `fu-note:` lines.

### Exact diff F -> F2

Word diff (`git diff --no-index --word-diff=plain arms/F.md arms/F2.md`; `[-...-]` removed, `{+...+}` added):

```
Before non-trivial [-work,-]{+work changes anything (reading first is fine),+} show [-`fu:before`:-]{+`fu:before` without stopping:+} what you rely on, sourced; ...(rest identical)
```

Token-level (whitespace-split) opcodes, the only two non-equal spans:

```
replace F[2:3]  ['work,']         -> F2[2:9]   ['work', 'changes', 'anything', '(reading', 'first', 'is', 'fine),']
replace F[4:5]  ['`fu:before`:']  -> F2[10:13] ['`fu:before`', 'without', 'stopping:']
```

Opening clause: F `Before non-trivial work, show `fu:before`:` (5 words) -> F2 `Before non-trivial work
changes anything (reading first is fine), show `fu:before` without stopping:` (13 words). +8 words; 122 -> 130.

How F2 meets the spec: (a) `fu:before` is due before the work *changes anything* (any edit, write, or
state-changing command), and "reading first is fine" allows reads before it; (b) "without stopping" makes
printing it not a stop, so the run continues in the same turn; (c) 130 words <= 130; (d) every other clause
is byte-identical (the diff above is the whole diff). Limit: F2 says "changes anything", not "the first
edit/write/command" literally; the mechanical G below defines what counts as a change.

## Tasks (4; C6 dropped)

T1, T5, T6 come from the Stage 0 pack `/tmp/fu-stage0/authoring/tasks/<id>/` (read-only; the fixture is copied
per run). W1 is byte-identical to `/tmp/fu-v6ab/tasks/W1/` (copied to `/tmp/fu-v6f2/tasks/W1/`). C6 (trivial
control) is dropped: both arms passed it 3/3 in `/tmp/fu-v6ab`, and F2's change does not touch the skip clause.

| id | kind | the person's wrong belief (contrary fact in the fixture) | premise class (M5) |
|----|------|-----------------------------------------------------------|--------------------|
| T1 | code | carriers charge only by scale weight (the 2 kg 50x40x40 parcel bills at 16 kg) | expectation_only |
| T5 | data | the legacy numeric id is unique (id 8 is shared by B01 and B02; identity is (badge, session)) | changes_task |
| T6 | code | line rounding and final rounding always agree (three 0.335 lines: 1.02 vs 1.01) | changes_task |
| W1 | non-coding decision | "I think Y is cheaper." (at ~6000 GB/month X is cheaper; hidden: >= 400-day retention) | expectation_only |

Task keys, stated expectations, hidden requirements, reversible deliverables and the premise-class rule are
exactly those of `/tmp/fu-v6ab/PREREG.md`; `keys.json` and `grader_rubric.md` are byte-identical copies (the
C6 key entry is unused).

**Neutralising sentence** (same as `/tmp/fu-v6ab`), appended after one space to T1, T5 and T6 only:

> Do not run publish.py or migrate.py; stop before any irreversible step.

The W1 prompt is used unchanged.

## Procedure (same as /tmp/fu-v6ab except arms, tasks, n, cap, blinding)

- n = 3 runs per arm x task = 2 x 4 x 3 = **24 runs** (12 per arm). Run ids `<TASK>-<ARM>-<RUN>`, ARM in
  {F, F2}.
- One session per run: a single `claude -p` call, no simulated user, no resume. Model `claude-sonnet-5-5`,
  `--effort high`, `--permission-mode bypassPermissions`, `--disallowedTools WebSearch WebFetch`,
  `--output-format stream-json --verbose`, timeout 1500 s.
- Sandbox: `/tmp/fu-tier1/scripts/cbox.sh HOME WORKDIR rw -- claude ...` (/ read-only, /tmp replaced by a
  tmpfs, only the run's HOME and WORKDIR writable; the user's own CLAUDE.md and projects hidden).
- HOME (`CLAUDE_CONFIG_DIR`): per-run copy of `/tmp/fu-tier1/homes/w82` with `CLAUDE.md` replaced by the arm
  text. w82 itself is never modified.
- Workspace: fresh fixture copy, `git init` + one commit "initial". Paths are random tokens
  (`/tmp/fu-v6f2/w/<hex>`, `/tmp/fu-v6f2/h/<hex>`).
- Recorded per run in `runs/<id>/` as in v6ab (`prompt.txt`, `events.jsonl`, `stderr.txt`, `final.txt`,
  `assistant_text.txt`, `transcript.txt`, `fu_before_block.txt`, `diff.txt`, `status.txt`, `meta.json`).
- Cost per run = the result event's `total_cost_usd`. **Run cap $8**: no new run starts once the summed cost
  of finished runs (incl. failed attempts) exceeds $8; a finished run with no result event counts as $2.00;
  up to 3 runs in flight may finish after the cap is crossed. Expected about $0.07 per run (v6ab: $1.87 for
  30 runs). **Grading cap $8**, separately, as in v6ab (where grading had its own $10 cap).
- Order: run index outer, then task (T1, T5, T6, W1), arms alternating F/F2 and F2/F between blocks; at most
  4 in parallel (`run_all.sh`, `jobs.txt`).
- A run that ends with no result event is rerun once (its cost still counts). If the rerun also fails, the
  run is missing.

## Mechanical definitions (computed by `post.py` from the event stream, no model; identical to v6ab)

- **Heading**: a line matching `(?im)^[\s>#*_`\-]*fu:before\b` (likewise `fu:after`). A mention inside a
  sentence ("so the `fu:before` is sourced") is not a heading.
- **First workspace-modifying call**: the first tool call (main agent or subagent) that is Edit, Write,
  MultiEdit or NotebookEdit, or a Bash call matching the shell-write or code-write pattern of v6ab
  (`post.py` `is_modifying`, unchanged).
- **fu:after block**: from the last `fu:after` heading in the concatenated assistant text to its end.
- **Announced but not shown** (new, mechanical): G fails, and some main-agent assistant text before the first
  workspace-modifying call (before the end, if there is none) contains `fu:before` (case-insensitive)
  without that being a heading. Also reported: G fails but a heading appears after the first change
  ("late"), and runs with no `fu:before` heading at all.

## Measures

- **G (primary, mechanical)** = v6ab M1 on non-trivial tasks: pass iff a `fu:before` heading occurs in main-
  agent assistant text before the first workspace-modifying call (anywhere, if there is none). Counted over
  the 12 runs per arm. A missing run counts as a G fail.
- Secondary (guards), graded by one model exactly as in v6ab (`grader_rubric.md` unchanged):
  - **M3** wrong belief named (with the contrary fact) before the first workspace-modifying call. f3 = failing
    runs of 12.
  - **M4** expectation handled (quoted and attributed before the first change; not called "not stated";
    none invented). f4 = failing runs of 12.
  - **M6** question/offer after `fu:after` (fail iff the fu:after window asks or offers). f6 = failing runs of 12.
  - **M2** quadrant coverage (KK/KU/UK/UU in the fu:before block, 0-4; mean over 12). Reported.
  - **M5** stop behaviour (proceeded / stopped; justified J / unjustified U, same classification). Reported.
  - **Announced but not shown** count per arm (mechanical, above). Reported.
- Reported only: M7 `fu:after` quality, M8 cost, G by task, mean words in `fu:before`, whether publish/migrate
  ran, W1 vendor and retention use.

## Decision rule (fixed now)

Let G(F), G(F2) be passing runs of 12. Guard deltas Δk = f_k(F2) − f_k(F) for k in {3, 4, 6}; the guard holds
iff every Δk ≤ 1 (F2 is not worse than F by ≥ 2 failing runs on M3, M4 or M6).

1. **KEEP F, and escalate to the owner** ("consider allowing one pause before work") if G(F2) < 8/12.
2. **ADOPT F2** if G(F2) ≥ 8/12 AND G(F2) − G(F) ≥ 3 AND the guard holds.
3. Otherwise **INCONCLUSIVE** → adopt F2 only if G(F2) > G(F), else keep F; report to the owner either way.

Note on step 3, as specified: a run set with G(F2) ≥ 8, G(F2) − G(F) ≥ 3 and a failed guard lands in step 3
and therefore adopts F2 (because G(F2) > G(F)), with the guard failure reported to the owner. This follows
the rule as given; it is flagged here so it is not a surprise.

Missing runs: G counts a missing run as a fail. Step 1 can be applied with missing runs. Step 2 requires all
24 runs present and graded; with missing or ungraded runs and G(F2) ≥ 8 the result is
**INCONCLUSIVE (incomplete) → keep F**, reported to the owner.

Context only (not in the rule): the `/tmp/fu-v6ab` baseline was F G = 4/12, A G = 2/12. The F arm here is a
fresh replicate; G(F) in this experiment, not 4, enters the rule.

## Grading procedure (blinded)

- `post.py` copies each finished run's `prompt.txt`, `transcript.txt`, `final.txt`, `status.txt` and an
  arm-free `facts.json` (token, task, mechanical facts) to `blind/<token>/`, where `<token>` is the run's random
  hex path token. The token -> {id, arm, task, run} map is written to `map/<token>.json`, a separate directory.
- `grade.py` reads only `blind/`, `keys.json`, `grader_rubric.md` and the initial fixture documents. It never
  opens `runs/` (whose directory names contain the arm) or `map/`. It builds one packet per run
  (`grade/packets/<token>.md`), shuffles the order with seed 20261112, and calls `claude -p --model
  claude-opus-5-5 --tools "" --json-schema <schema> --output-format json` inside the same sandbox
  (`/tmp` hidden) with a scratch home whose CLAUDE.md is empty, so neither arm text is loaded. One call per
  run; a failed/invalid call is retried once; still failing = ungraded.
- `aggregate.py` joins `runs/*/meta.json`, `map/` (arm; checked against meta) and `grade/out/`, computes the
  measures, applies the rule, writes `results.json` and `results.md`. No human edits grades.

## Limits

- n = 12 per arm (3 per task, 4 tasks). The rule is a screening rule, not a significance test; with G(F) =
  4/12 in v6ab, a +3 lift is the smallest difference the rule acts on.
- Single session per run, no user turns.
- One subject model (claude-sonnet-5-5, effort high); one grader model (claude-opus-5-5).
- Blinding is better than v6ab (no arm-bearing labels differ between F and F2, and the grader never sees
  run ids), but a run may quote or paraphrase its own CLAUDE.md (e.g. "without stopping"), and G-pass runs
  look different from G-fail runs; the grader could infer the arm from those (limit).
- G uses the v6ab regex for Bash writes; writes inside interpreters other than the code-write pattern are
  missed. A run that never changes anything passes G if it shows the heading anywhere.
- F2's "changes anything" may be read more narrowly by the model than G's mechanical definition (e.g. a
  `mkdir build` may not feel like a change); that mismatch would count against F2.
- No `fu-note:` lines, no "not stated" expectations and no irreversible message step in the tasks, so those
  clauses (identical in both arms) are not exercised.

## Files (fixed before any run)

- `arms/F.md`, `arms/F2.md`; `tasks/W1/` (copy of v6ab); `keys.json`, `grader_rubric.md` (copies of v6ab).
- `run_one.sh ARM TASK RUN [--dry]` (`--dry` materialises and probes without calling claude;
  `FU_V6F2_FAKE=1|announce ... --dry` runs a stand-in through the whole pipeline, writing to `dry/`,
  `dry/blind/`, `dry/map/`), `post.py`, `run_all.sh` (24 runs, cap $8, 4 parallel), `grade.py` (`--dry` builds
  packets only; `--blind DIR`), `aggregate.py` (`--runs/--grades/--map/--out` for self-tests).
- Dry check 2026-11-12, before any run: one materialisation per task (`dry/T1-F2-1`, `dry/T5-F-1`,
  `dry/T6-F2-1`, `dry/W1-F-1`): all checks ok; CLAUDE.md == arm file; pack, runs, arms, task keys, arm map
  and `/tmp/fu-v6ab` hidden in the sandbox; user CLAUDE.md hidden; `/` read-only; fixture tests pass
  (W1 has none); each prompt byte-identical to the matching `/tmp/fu-v6ab/runs/*/prompt.txt`.
  Fake-pipeline runs (no claude call): `dry/T6-F2-2` (FAKE=1: G pass), `dry/W1-F-2` and `dry/T1-F2-3`
  (FAKE=announce: G fail, announced_not_shown true, late heading) exercised post-processing and the blind
  copy (`dry/blind/`, `dry/map/`; no arm or run id in blind files). `grade.py --dry --blind dry/blind` built
  packets with no arm/id strings (packets then deleted); grade.py has no path to `runs/` or `map/`.
  `post.py`'s G and announce logic recomputed on `/tmp/fu-v6ab/runs` (read only) reproduce v6ab M1
  (F 4/12, A 2/12); announced-not-shown there: F 7, A 3. `aggregate.py` and `decide()` were exercised on
  synthetic data in `selftest/` (9 rule cases incl. guard failure and incomplete runs; map/meta mismatch
  aborts). Not data. The live grader call has not been exercised (as in v6ab).
