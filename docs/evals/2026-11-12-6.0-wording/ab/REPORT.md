# v6ab: always-on text A (design draft) vs F (revised): report

> **Reconstructed.** The report agent was not allowed to write files, so no `REPORT.md` was saved during the test, and its full English report was lost. This file is rebuilt from the agent's final message in the workflow journal of 2026-11-12 (a Chinese summary with every number used below), checked against `runs/*/meta.json` (M1, costs, `fu:before` word counts) and `grades.json`. Wording is new; numbers are the agent's. Nothing was re-graded.

Date: 2026-11-12. The rule in `PREREG.md` was applied as frozen; no amendment. 30 of 30 runs completed (no failures, no reruns) and all 30 were graded. Both arm files match the sha256 values in `PREREG.md`. The statistics were computed by hand from the grades and `meta.json`; `aggregate.py` was not run. The graders' M1 agrees with `meta.json` `M1_pass` on all 30 runs.

## Verdict: SHIP F

- Step 1 (F worse, ship A) did not fire: Δ1 = −2, Δ3 = −1, Δ4 = −2, Δ6 = −5; none is ≥ 2.
- Step 2 fired on M2: 1.333 − 0.500 = 0.833 ≥ 0.5.
- The M5 branch did not fire: U(A) − U(F) = 1, J(F) − J(A) = −1.
- All 30 runs were run and graded, as SHIP F requires.

## Measures (A vs F)

| measure | A | F | Δ (F − A) |
|---|---|---|---|
| M1 fails: `fu:before` not before the first change (of 15) | 10 | 8 | −2 |
| M1 passes on non-trivial tasks (of 12) | 2 (both T5) | 4 (T6 ×3, T5 ×1) | |
| M1 on C6 (trivial control) | 3/3 | 3/3 | |
| M1 on T1 and W1 | 0/6 | 0/6 | |
| M2 mean quadrant coverage (of 12) | 0.500 (T5-A-2, T5-A-3: 3 each) | 1.333 (four runs with 4 each) | +0.833 |
| M3 fails: wrong belief not named before the first change (of 12) | 9 | 8 | −1 |
| M4 fails: expectation handling (of 12) | 10 | 8 | −2 |
| M5 justified / unjustified stops | 1 (T5-A-3) / 1 (T5-A-2) | 0 / 0 (12 proceeded) | |
| M6 fails: question or offer after `fu:after` (of 15) | 7 | 2 (T1-F-1 borderline, T1-F-2) | −5 |
| M7 (reported only) | 12/12 | 12/12 | |
| mean `fu:before` words (runs with one) | 389 (n = 2) | 346.5 (n = 4) | |
| announced `fu:before`, then changed files without showing it | 3 | 7 | |
| cost of runs (USD) | 0.9078 (0.0605 per run) | 0.9598 (0.0640 per run) | total 1.8676 of the $10 cap |

Other observations: no run had `fu:after` on C6; no run executed `publish.py` or `migrate.py`; all six W1 runs chose vendor X and included the 400-day retention in the cost; dropping T1 does not change M5. Grading cost was not recorded (`grade/out` did not exist; grades came from the workflow, not from `grade.py`).

## Limits

- **The verdict rests on M2 alone, and M2 is close to M1.** Only runs that showed `fu:before` can score, so the gap is mostly F's two extra M1 passes plus the UK quadrant, which `PREREG.md` notes favours F by construction. Sensitivity (not a rule input): without UK scoring the gap is exactly 0.5, still at the threshold; if T5-F-3's UU entry is rescored as KU, as the grader's own caveat suggests, the gap falls to 0.417 and would not pass.
- **Both texts were weak on the core behaviour:** across T1 and W1, 0 of 12 runs showed `fu:before` before the first change. Neither text solves it. This motivated v6f2.
- **In F's favour:** M6 has 5 fewer failures, consistent with "then ask nothing"; F is not worse than A on any of the four guard measures.
- **Procedure deviations:** grading did not go through `grade.py`; some grader notes cite run directories that carry the arm letter (for example `runs/T1-F-1`, `runs/W1-A-3`), so blinding failed for at least those runs; the grader model and calls per run cannot be verified.
- **Sample:** 15 runs per arm, 3 per cell. Differences of one or two runs are within noise; the rule is a screening rule, not a significance test.
- **Setup:** single session per run with no user turn; one subject model; the neutralising sentence changes T1, T5 and T6; F's "not stated", `fu-note:` and "or message" clauses were not exercised.
- **Borderline grader calls:** M6 on T1-F-1, T5-A-2, T6-F-1 and T5-F-3; M5 stop reasons on T5-A-2 and T5-A-3. None changes step 1, but they affect the M2 margin.
