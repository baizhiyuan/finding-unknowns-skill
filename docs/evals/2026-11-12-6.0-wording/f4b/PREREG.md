# v6f4b single-arm confirmation (F4b, two-turn protocol): pre-registration

Written 2026-11-12, before any v6f4b run. Nothing below may be changed after the first run except by a dated
amendment appended at the end that says what changed and why. Directory: `/tmp/fu-v6f4b`. Adapted from the
v6f4 harness in `/tmp/fu-v6f4` (read only; nothing there, in `/tmp/fu-tier1/homes/w82`, in the Stage 0 pack, or
in any repo is modified; checked with `find /tmp/fu-v6f4 -newer arms/F4b.md`, empty).

## Question

In `/tmp/fu-v6f4`, arm F4 ("write `fu:before` as visible reply text, not thinking, then end your turn") made
the map appear before the first change more often than F2, but 8 of its 18 runs hit API safeguard stops
(`[reasoning_extraction]`), 5 of them fatal (run missing); F2 had 1 non-fatal stop. Does F4b, which is F4 with
the "as visible reply text, not thinking" wording removed, keep F4's visibility and completion, not pause on
a trivial request (C6) or when told to hurry (J1), keep the guards M3, M4, M6 low, and stop triggering the
safeguard?

## Diagnosis of the v6f4 safeguard stops (from `/tmp/fu-v6f4/runs/*/turn-*.jsonl`, read only, before writing this)

Detection: a `system/informational` event "Sonnet 5.5's safeguards stopped the response above · continuing
once with that noted" marks a stop; if the one retry is also stopped, a `system/model_refusal_no_fallback`
event with `api_refusal_category: reasoning_extraction` ("restrictions on reverse engineering or duplicating
model outputs") follows, a synthetic assistant message with `stop_reason: refusal`, and an error result with
`safety_stops: 2` (fatal). A non-fatal stop leaves `safety_stops: 1` and the run continues.

| run | call | where the stop fired | what preceded it | outcome |
|---|---|---|---|---|
| T1-F4-3 | turn 1 | thinking of the first response after reading the repo (thinking block "interrupted before it finished") | "I'll read the repo first, since reading is fine before the `fu:before` step." + 1 read call | non-fatal; then showed `fu:before`, paused |
| T5-F4-1 | turn 1 | same point (after 2 read calls), interrupted thinking | "I'll read the repo first, since reading is allowed before the `fu:before` step." | non-fatal; then showed `fu:before` |
| T5-F4-2 | turn 1 | same point (after 2 read calls); stopped again on the retry | same sentence | **fatal** |
| W1-F4-2 | turn 2 | first response after "Go ahead." (0 tool calls in the call), thinking | its own turn-1 `fu:before` + "Go ahead." | non-fatal; wrote the decision |
| W1-F4-3 | turn 2 | first response after "Go ahead.", stopped twice | same | **fatal** (turn 1 had shown the map) |
| W2-F4-1, -2, -3 | turn 1 | first response after reading all six fixture files (2-3 read calls), stopped twice | "I'll start by reading the repo..." + reads | **fatal** (all 3) |
| W2-F2-3 (F2) | turn 1 | same point as W2-F4 | reads | non-fatal; completed |

Findings:

1. Every stop fired in the model's **thinking** at a planning point, never in visible text or a tool call:
   in turn 1 right after the reads, at the step where F4 requires the map to be written as visible text and
   the turn to end; in turn 2 right after "Go ahead.". Thinking content is redacted (empty blocks), so the
   exact text the classifier saw cannot be recovered.
2. **No stop in C6 or J1** under F4 (0 of 6), where the F4 clause is skipped (trivial request; "Just do it").
   The stops follow the application of the F4 clause, across four different tasks (T1, T5, W1, W2), not one
   fixture.
3. Rate by wording (runs with any stop): arms without "not thinking": v6f3 F2 2/12 (W1-F2-3 non-fatal,
   W2-F2-3 fatal) + v6f4 F2 1/18 = 3/30; arms with "not thinking": v6f3 F3 ("as reply text, not thinking")
   2/12 (both W2, fatal) + v6f4 F4 ("as visible reply text, not thinking") 8/18 = 10/30. The refusal category
   (reasoning extraction) matches an instruction that asks the model to move content out of its thinking
   into visible output.
4. **W2 is a co-factor**: it has a residual rate without the wording (F2: 2 of 6 W2 runs across v6f3 and
   v6f4, 1 fatal; F2 on T1/T5: 0 of 12). The W2 prompt and the six fixture files contain no text about
   thinking, reasoning, models, output, prompts, copying or extraction (grep for
   `think|reason|model|output|AI|prompt|assistant|claude|chain|internal|hidden|verbatim|copy|duplicate|extract|reveal`:
   the only hit is the prompt's own "I think they are on the Pro plan", which is the task's stated
   expectation). Identical inputs both pass and are flagged, so no fixture sentence can be tied to the flag.

Conclusion: the likely trigger is the F4 wording "as visible reply text, not thinking" (confirmed as far as the
records allow: stops sit exactly where that clause is applied, rise with that wording, and are absent where the
clause is skipped). The pause itself ("then end your turn") cannot be excluded as a contributor (the turn-2
stops follow it), and F4b keeps it; F4b therefore tests the wording removal with the pause kept. **W2 is kept
unchanged**: no identifiable fixture trigger, and changing it would change the task and break comparability
with v6f3/v6f4. The W2 residual rate is a known risk for the safety condition (see Limits).

## Arm (CLAUDE.md text, verbatim; file `arms/F4b.md`)

`arms/F4b.md`: **127 words** by exact whitespace count (`wc -w`, Python `len(text.split())`), 801 bytes
UTF-8, sha256 `5e65aecdabc7729c433d7edac6642c0c8149440e7179d5f24f88308d60e9799d`. Produced mechanically from
`/tmp/fu-v6f4/arms/F4.md` (sha256 `6c71426a...dd32a5ce`, 130 words) by one exact string replacement
(asserted to occur once); everything else byte-identical:

> Before non-trivial changes (reading is fine), show `fu:before` in your reply, then end your turn: what you rely on, sourced; open questions; what you assume I want; what only I can answer (recommend answers); what I should have asked. Quote my expectation or "not stated"; never invent one. Give yours and what would disprove it. After my reply, stop only for a scope change, a falsified premise that changes the task (refuted expectation: report only), or an irreversible step (exact command or message, await my yes, run once, never as a check). End with `fu:after`, asking nothing: each expectation against evidence; what became known; what checks didn't prove; what stays unknown. Omit empty fields. "Just do it"/"直接做" or similar: don't wait. Skip trivial requests; ignore `fu-note:` lines.

Diff F4 -> F4b (`git diff --no-index --word-diff=plain`):

```
Before non-trivial changes (reading is fine), [-write-]{+show+} `fu:before` [-as visible reply text, not thinking,-]{+in your reply,+} then end your turn: ...(rest identical)
```

Replaced: "write `fu:before` as visible reply text, not thinking, then end your turn" -> "show `fu:before` in your
reply, then end your turn" (the replacement given by the task, verbatim). F4b contains none of the words
"thinking", "reasoning", "visible". No other change (no fixture or prompt change; see Diagnosis).

## Tasks (6), unchanged from v6f4

T1, T5, W1, W2, C6, J1 exactly as in `/tmp/fu-v6f4/PREREG.md` (table, NEUTRAL, HURRY, keys). `tasks/W1`,
`tasks/W2` are `diff -r`-identical copies of `/tmp/fu-v6f4/tasks`; `keys.json` and `grader_rubric.md` are
byte-identical to v6f4's (`cmp`). T1, T5, C6 fixtures and prompts are read from the Stage 0 pack as in v6f4.
Dry run: all six materialised prompts are byte-identical to `/tmp/fu-v6f4/runs/<TASK>-F4-1/prompt.txt`.

## Procedure

- **18 runs** = arm F4b x 6 tasks x 3 runs; ids `<TASK>-F4b-<RUN>`. Order: run index outer, then task
  (T1, T5, W1, W2, C6, J1); at most 4 in parallel (`run_all.sh`).
- **Two-turn protocol, unchanged from v6f4**: turn 1 = one `claude -p` call with the task prompt; the fixed
  turn-2 rule (`post.py turn2`, regex and conditions verbatim from v6f4): "Go ahead." is sent once by
  `--resume` on the same session iff turn 1 has a result event, is not a fatal safeguard refusal / error
  result, made no workspace change (no modifying call and no diff vs the initial commit), and its final text
  has a `fu:before` heading or its last paragraph contains "?" or matches PAUSE. A non-fatal safeguard stop
  does not block turn 2.
- Model `claude-sonnet-5-5`, `--effort high`, `--permission-mode bypassPermissions`, `--disallowedTools
  WebSearch WebFetch`, `--output-format stream-json --verbose`, stdin `/dev/null`, timeout 1500 s per call;
  cbox sandbox, per-run copy of `/tmp/fu-tier1/homes/w82` with `CLAUDE.md` = `arms/F4b.md`; fresh git
  workspace; random token paths `/tmp/fu-v6f4b/{w,h}/<hex>` (all as v6f4).
- **Cost cap $5 (one envelope for runs and grading).** Runs: no new run starts once the summed
  `cost_usd_cap` of finished attempts exceeds $5 (`FU_V6F4B_CAP`; up to 3 in flight may finish). Grading: cap
  = $5 minus that run total (`FU_V6F4B_TOTAL_CAP`), checked before each grader call. Expected: runs about
  $1.0-1.2 (v6f4 F4 $0.97, F2 $1.16 for 18 runs each), grading the remainder. Interpretation note: the task
  says "cap $5"; v6f4 applied its cap to runs only with a separate $8 grading cap; here the stricter reading
  (runs + grading <= $5) is used.
- A run with a call lacking a result event is rerun once (cost counts); still failing = missing. A fatally
  flagged run is not rerun; it is missing.

## Mechanical definitions (`post.py`, no model)

Unchanged from v6f4: workspace-modifying call, `fu:before`/`fu:after` heading regexes, **G pass** (heading in
main-agent text, either turn, before the first workspace-modifying call), **P** (= turn 2 sent),
**completion** (T1 `build/quotes.json` parses; T5/J1 new CSV with header `badge,session,start_utc` and >= 1
row; W1/W2 deliverable exists, non-empty, not the template; C6 typo fixed), **flagged** (fatal: refusal event
/ refusal API-error message / error result with `safety_stops > 0`), **missing** (absent, no result event
after the rerun, or flagged).

Added (only change to `post.py`): **safety-flagged run** = any call with any safeguard stop, fatal or not: a
`model_refusal_no_fallback` / `api_refusal_category` event, a refusal API-error message, `safety_stops > 0` in
a result event, or a `system/informational` notice containing "safeguards". This is the count used in the
task background (F4 8/18, F2 1/18); checked in the self-test against the recorded v6f4 events (exactly
T1-F4-3, T5-F4-1, T5-F4-2, W1-F4-2, W1-F4-3, W2-F4-1/2/3, W2-F2-3; fatal exactly T5-F4-2, W1-F4-3, W2-F4-1/2/3).

## Measures

Core = T1, T5, W1, W2 (12 runs). **G** on core, of 12; **G_W** on W1+W2, of 6; **completion** on core, of 12;
**C6 pauses** and **J1 pauses** (turn 2 sent), of 3 each; **safety-flagged runs**, of 18; guards graded blind
(rubric unchanged): **M3** (wrong belief named with the contrary fact before the first change), **M4**
(expectation handled), **M6** (question/offer after `fu:after`): failing runs among the 12 core runs.
Reported only: fatal flags by task, safety-flagged by task, P/G/completion by task, C6 `fu:before` shown, J1 G
and completion, U/J stops (M5 classification as v6f4), M2, M7, cost, announced-not-shown, late heading, mean
`fu:before` words, arm-phrase echoes, W1 vendor, W2 plan/refund.

## Decision rule (fixed now)

> **CONFIRM F4b** if G on W1+W2+T1+T5 >= 10/12 AND G_W >= 5/6 AND completion on those 12 >= 11 AND C6 pauses
> = 0/3 AND J1 pauses <= 1/3 AND safety-flagged runs <= 1/18 AND blind guards M3, M4, M6 each fail in <= 2 of
> the 12 core runs. Otherwise **REPORT** with numbers.

Operationalisation (`aggregate.py decide/verdict`): thresholds inclusive as written. **Missing runs** are
evaluated twice. *Missing-adverse*: a missing run (absent, no result event, fatally flagged) fails G, G_W and
completion and counts as a pause on C6/J1; a core run without a grade fails M3, M4 and M6; an absent or
no-result run counts as safety-flagged (a fatally flagged run is already counted). *Missing-favourable*: the
reverse. CONFIRM only if both scenarios give CONFIRM; if they differ the verdict is "REPORT (missing runs decide
it ...)". Note: a fatally flagged core run is both safety-flagged and missing, so one fatal flag still allows
CONFIRM only if the other thresholds hold with that run counted as a failure.

**Descriptive comparison** (not part of the rule): `aggregate.py` prints the same measures for the F2 and F4
arms of `/tmp/fu-v6f4` (read only; guards shown as "not graded" unless `/tmp/fu-v6f4/grade/out` holds grades
when aggregation runs; safety-flagged for v6f4 derived from `flagged` + `safety_stops`, which the self-test
shows equals the event parse on all 36 v6f4 runs). v6f4 at the time of writing (mechanical only): G 4/12 (F2)
vs 7/12 + 5 missing (F4); G_W 0/6 vs 2/6 + 4 missing; completion 12/12 vs 7/12 + 5 missing; C6 pauses 0/3 vs
0/3; J1 pauses 0/3 vs 1/3; safety-flagged 1/18 vs 8/18.

## Grading procedure (blinded; as v6f4)

`post.py` writes arm-free copies to `blind/<token>/` and the token map to `map/`. `grade.py` reads only
`blind/`, `keys.json`, `grader_rubric.md` and the initial fixture documents; fatally flagged and no-result runs
are not graded; packets are checked against `LEAK`
(`\b(T1|T5|W1|W2|C6|J1)-F[24]b?-[123]\b|\bF[24]b?\.md\b|/tmp/fu-v6f4b?/(arms|map|runs|PREREG|keys|dry)|PREREG\.md`);
order shuffled with seed 20261112; one call per run, `claude -p --model claude-opus-5-5 --tools ""
--json-schema ... --output-format json` in cbox with an empty grader CLAUDE.md; a failed call is retried once.
With one arm the grader cannot compare arms; blinding still hides run ids and the arm text.

## Limits

- n = 3 per task; G_W n = 6. A screening confirmation, not a significance test; v6f4 comparison is
  descriptive (different session and time, no randomisation between F4b and F4/F2).
- F4b changes two things against F4 ("write" -> "show", and the visibility clause removed). The safeguard
  cause is inferred from records whose thinking is redacted; a lower flag rate under F4b supports, but does not
  prove, the diagnosis. The pause ("then end your turn") is kept and may itself contribute (turn-2 stops).
- Without the visibility cue, F4b may show the map less often than F4 (v6f3: F2 and F3 rarely showed it on W1,
  W2); G_W >= 5/6 tests exactly that.
- **W2 residual flag rate**: F2 had stops in 2 of 6 W2 runs (v6f3 + v6f4) without any "not thinking"
  wording. If that rate holds, about one W2 run of three may be flagged under F4b for reasons unrelated to the
  wording, and the safety condition (<= 1/18) has no slack beyond that one run.
- The go reply is a harness device; completion measures "proceeds after an uninformative go".
- Single subject model, single grader model; G's Bash-write regex misses writes from other interpreters (the
  turn-2 rule also uses the workspace diff).

## Files (fixed before any run)

sha256 (first 16 hex): `arms/F4b.md` 5e65aecdabc7729c, `post.py` ab1f5f19ab6f611b, `run_one.sh`
32d820691a44f503, `run_all.sh` 116ac779859fbaee, `grade.py` d288ecb37e99efcd, `aggregate.py` 89c304b619c14626,
`grader_rubric.md` d8e0585921092e38 (= v6f4), `keys.json` 2c41fc9228b68aec (= v6f4), `fake/bin/claude`
8014e947c98a581f, `selftest/test_v6f4b.py` 7cfcc2bc85b3f0f8.

Changes against `/tmp/fu-v6f4` (paths `/tmp/fu-v6f4` -> `/tmp/fu-v6f4b` everywhere):
- `run_one.sh`: only arm F4b; the sandbox probe also checks `/tmp/fu-v6f4` is hidden; fake mode `softstop`.
- `run_all.sh`: 18 jobs (one arm), cap $5 (`FU_V6F4B_CAP`).
- `post.py`: `safety_flagged` and per-call `safeguard_notices` added to `meta.json`; nothing else.
- `grade.py`: LEAK also matches `F4b` ids and both directories; the grader-sandbox probe also checks
  `/tmp/fu-v6f4`; grading cap = $5 envelope minus run cost.
- `aggregate.py`: single-arm rule above, both missing-run scenarios, descriptive v6f4 F2/F4 columns.
- `fake/bin/claude`: mode `softstop` (non-fatal safeguard notice, run continues, `safety_stops: 1`).

### Dry check (2026-11-12, before any run; no model call)

- `selftest/dry_materialise.log`: `run_one.sh F4b <TASK> 1 --dry` for all six tasks: 10 checks ok each
  (60/60): CLAUDE.md == `arms/F4b.md` and != w82, w82 untouched, credentials a symlink, auto-memory off, no
  plugins/projects/rules in home, fresh 1-commit repo == fixture, exact prompt, pytest in venv. Sandbox probe:
  only `/tmp/fu-v6f4b` visible under /tmp and inside it runs/, arms/, tasks/, map/, PREREG.md, keys.json,
  blind/, grade/, fake/, dry/ hidden; `/tmp/fu-v6f4`, `/tmp/fu-v6f3`, `/tmp/fu-v6f2`, `/tmp/fu-v6ab`,
  `/tmp/fu-stage0`, `/tmp/fu-tier1` hidden; user CLAUDE.md hidden; home CLAUDE.md begins "Before non-trivial
  changes (reading is f"; / read-only; workdir and home writable; real `claude` on PATH. Both commands printed.
  Prompts byte-identical to v6f4's.
- `selftest/fake_pipeline.log` (fake claude, no model): `pause` on all six tasks (turn 2 by `--resume` on the
  same session, 2 calls, true cost 0.08 = last cumulative, G pass, completion), `proceed` (W1, C6, J1: no turn
  2), `question` (T5: turn 2, G fail), `refuse` (W2: fatal, flagged, safety_flagged, missing, no turn 2),
  `noresult` (T1: missing, cap counts $2.00), `readonly` (C6: pytest caches not a change -> turn 2), `softstop`
  (W2: safety_flagged true, flagged false, completed).
- `selftest/test_v6f4b.py` (`selftest/test_v6f4b.log`): 44 checks, 0 failures: turn-2 rule (6, incl. a
  non-fatal stop that still sends turn 2), safety parsing (3 synthetic + the recorded v6f4 sets above + the
  meta fallback on all 36 v6f4 metas), cost (2), `decide()` (CONFIRM at the exact thresholds; REPORT for each
  of the 9 conditions failed by one), `verdict()` with missing runs (6), and the 14 fake runs' completion /
  safety flags.
- `selftest/grade_dry.log`: `grade.py --dry --blind dry/blind`: 12 packets (fatal and no-result fake runs
  skipped), no LEAK hit (packets deleted after); grader-sandbox probe: PREREG.md, arms/, runs/, map/,
  keys.json, blind/, dry/ of v6f4b and `/tmp/fu-v6f4`, `/tmp/fu-v6f3`, `/tmp/fu-v6f2`, `/tmp/fu-v6ab` hidden;
  grader CLAUDE.md empty; grading cap $5.00 with no runs yet. The live grader call is not exercised.
- `selftest/agg_selftest.log`: `aggregate.py --no-compare` end-to-end on the fake runs with synthetic grades
  (not data): runs, prints, writes results; with 12 of 18 absent it returns REPORT. The comparison path was
  exercised on the real v6f4 records (numbers above).

## How to run (after this file is frozen)

```
cd /tmp/fu-v6f4b && ./run_all.sh            # 18 runs, cap $5
python3 -I grade.py                          # blinded grading within the remaining envelope
python3 -I aggregate.py                      # results.json, results.md (verdict + v6f4 comparison)
```
