# Pilot eval: plain Codex vs Codex with these skills (2026-11-10)

The first comparative evaluation of the plugin. The question was whether the three
skills change what a strong model catches, at what cost. The plan, the traps and a
prediction were written in [PREREG.md](PREREG.md) before any run, and the file was
left unchanged afterwards. This page reads the results against it.

**Short answer:** no detectable effect on detection at this scale. Both arms caught
nearly every pre-registered trap; the skill arm caught +0.75 of 25 on average, all on
one task, which is inside the noise for one run per cell. The skill arm cost 47 % more
input tokens and 28 % more wall time. The prediction (a 4–5 trap gain) was wrong: the
baseline was far stronger than expected.

## Setup

- **Subject model:** gpt-6.1-sol through `codex exec` (codex-cli 0.164.0), reasoning
  effort high. It is a different model family from the one the skills were written
  with, so the skills are tested on a model they were not tuned for.
- **Arm A (plain):** an isolated `CODEX_HOME` holding only the model and provider settings, plus Codex's built-in system skills.
- **Arm B (skills):** the same, plus `finding-unknowns`, `keep-the-reasoning` and
  `theory-vs-result` at v4.3.1. The prompt never names a skill, so the eval measures
  natural activation and effect together.
- **Runs:** one per task per arm, each on a fresh copy of the fixture, non-interactive
  (the first response is scored). Read-only sandbox, except workspace-write for the
  typo task.
- **Grading:** blinded. Outputs were labelled X/Y at random, with the key held in
  [scores/blind-key.json](scores/blind-key.json). Graders (Claude) scored each
  pre-registered trap 1 / 0.5 / 0 with a quoted sentence, counted false claims, and
  stated a preference. A second grader then re-scored all five tasks with X and Y
  swapped.

## Tasks

| Task | Fixture | What it tests | Traps (abridged) |
|---|---|---|---|
| T1 | pallets/itsdangerous @ 672971d | wrong prior | key rotation already exists; key order; Flask `SECRET_KEY_FALLBACKS`; other `SECRET_KEY` users; key retirement |
| T2 | baizhiyuan/home-nas @ 797d98c | remote device, late prior | Jetson no longer the NAS; versions recorded in a draft; the OS-upgrade prior is wrong; 6.7 GB shared memory / CUDA 11.4; no recorded access path |
| T3 | [fixtures/tokbench](fixtures/tokbench) | measured result | gain inside noise; different machines; 3 % cache hit rate; no pre-agreed rule; the discriminating rerun |
| T4 | [fixtures/durations](fixtures/durations) | agent handoff | a failing test was deleted; `except Exception: return 0`; the CLI caller breaks; the reported bug is untested; the fix path |
| T5 | psf/requests @ 3c7baaa | wrong prior | retries already supported; feature freeze; POST replay risk; zero-retry and no-timeout defaults; retry policy |
| T6 | [fixtures/tinydoc](fixtures/tinydoc) | negative control | fix one typo, nothing else |

## Results

Trap scores, out of 5 per task (round 1 / round 2 swapped):

| Task | A (plain) | B (skills) | Preferred in both orders |
|---|---|---|---|
| T1 | 4.5 / 4.0 | 4.5 / 4.0 | B |
| T2 | 4.5 / 4.5 | 4.5 / 4.5 | none |
| T3 | 3.5 / 4.0 | 4.5 / 4.5 | B |
| T4 | 5 / 5 | 5 / 5 | none |
| T5 | 4.5 / 4.5 | 4.5 / 4.5 | none |
| **T1–T5 /25** | **22 / 22** | **23 / 22.5** | B 2, none 3, A 0 |
| T6 control | pass | pass | — |

Cost and behaviour ([scores/usage.json](scores/usage.json)):

| T1–T5 | A | B | Δ |
|---|---|---|---|
| Input tokens | 1.10 M | 1.61 M | +47 % |
| Output tokens (incl. reasoning) | 11.7 k | 19.6 k | +69 % |
| Wall time | 24.5 min | 31.2 min | +28 % |
| Output words | 1173 | 1500 | +28 % |

Arm B read a matching `SKILL.md` on all five of T1–T5 and on none of T6. T6 changed
only the typo in both arms, and B spent fewer tokens than A on it. Round 1 counted two
minor false claims for A (a wrong test line number; "available memory" for total
memory) and none for B; round 2 counted none for either.

## Reading

- **Primary prediction (A 13–16, B 17–21): inconsistent.** A scored 22/25, close to the
  ceiling. The +0.75 difference comes entirely from T3 and is inside the noise for
  n = 1, so the verdict on detection is can't tell. The pre-registered falsification
  criteria were not met either (B was not below A, and the cost ratio of 1.47 is under
  2×). The effect is not shown, but it is not disproved.
- **Activation, control and cost: consistent with the prediction.** The +47 % input
  cost sits at the top of the predicted 10–50 % band.
- **Where B was better (supported on T3, inferred elsewhere).** On T3 both graders gave
  B full credit and A half credit for the "no pre-agreed decision rule" trap, which is
  `theory-vs-result`'s core rule. The graders' reasons for preferring B on T1 and T3
  concern calibration rather than coverage: a concrete first check, a caveat on
  version-specific advice, and what the checks did not establish. Trap counting does
  not measure this.
- **Grader bias.** In round 1 the grader preferred the second output five times out of
  five. Preferences are therefore read only where they survive the swap. Trap scores
  were stable across the two rounds (|Δ| ≤ 0.5 per task).

## What this changed in the skills (v4.3.2)

These fixes come from this pilot and have **not** been re-run:

- **Access to a remote device (field note F3).** On T2, arm B read
  `finding-unknowns/SKILL.md`, which in v4.3.1 had the access rule in Technique 1 and
  Technique 5. It still did not make "confirm you can log in" a first step: 0.5 in both
  arms, from both graders. The rule is now one always-on Execution_Policy bullet: state
  the recorded access path, or say that none is recorded, and make logging in step 1 of
  any plan that touches the target.
- **Noise floor computed from the data (T3).** Arm B led with "the recorded p50
  improvement is 5.6 %" and called the variability substantial, but it never estimated
  the noise from the five and three reruns it had. The trap scored 0.5 in both rounds.
  `theory-vs-result` now says: when the data already holds reruns, compute the noise
  floor from them before the headline, and lead with the verdict.
- **Field note F1 (absence claims).** Neither arm called the versions unknown. Arm B
  cited the draft that records JetPack 5.1.5 and flagged it as historical. Arm A cited
  versions from other repo files. This is consistent with the 4.3.1 fix but does not
  test it, because A did not make the mistake either.

## Limitations

- One run per cell. The grader (Claude) is from the skill author's model family, and
  the trap lists were written by the skill author. Blinding, quotes and the order swap
  reduce these biases; they do not remove them.
- The tasks were single-turn, so the interview techniques could only appear as
  questions. Most traps could be found by reading one or two obvious files, which suits
  a strong model.
- The next eval needs traps that only surface by joining several files, multi-turn
  tasks, a weaker model (gpt-5.5) as a second subject, and two runs per cell. It also
  needs a rubric for calibration (claims matched to evidence, unproven checks named),
  not only for coverage.

## Files and reproduction

- [PREREG.md](PREREG.md): the plan as written before the runs.
- `outputs/`: every final answer, verbatim (absolute paths are left as written;
  `T6-*.diff` are the edits).
- `scores/`: each grader's reply verbatim (`round1-T*.json`,
  `round2-swapped-T1-T5.json`), the blinding key, and token, time and word usage per run.
- `scripts/`:
  - `make_homes.py <repo>` builds the two isolated `CODEX_HOME` directories. It copies
    only the model and provider keys from `~/.codex/config.toml`, links `auth.json`,
    and prints key names, never values.
  - `run.sh` and `all.sh` run the 12 runs.
  - `blind.py` builds the X/Y grading packets.
  - The scripts assume `/tmp/fu-eval` as the working root, with the fixtures under
    `fixtures/` (the public repos cloned at the commits above).
