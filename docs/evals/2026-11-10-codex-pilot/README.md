# Pilot eval: plain Codex vs Codex with these skills (2026-11-10)

The first comparative evaluation of the plugin. The question was whether the three
skills change what a strong model catches, at what cost. The plan, the traps and a
prediction were written in [PREREG.md](PREREG.md) before any run. The sections written
then are unchanged; two corrections found in review are appended under its Amendments.
This page reads the results against it.

**Short answer:** no detectable effect on detection at this scale. Both arms caught
nearly every pre-registered trap; the skill arm caught +0.75 of 25 on average, all on
one task, which is inside the noise for one run per cell. The skill arm used 47 % more
input tokens (22 % more uncached) and 28 % more wall time. The prediction (a 4–5 trap
gain) was wrong: the baseline was far stronger than expected.

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
  typo task. Shell commands ran in Codex's sandbox, whose network is off by default (not
  checked in the logs), but Codex's `web_search` tool was available
  and both arms used it on T1, T2 and T5 (completed searches A 1 / 5 / 2, B 2 / 7 / 3).
  PREREG said "no network"; see its Amendments.
- **Grading:** blinded. Outputs were labelled X/Y at random, with the key held in
  [scores/blind-key.json](scores/blind-key.json). Graders (Claude) scored each
  pre-registered trap 1 / 0.5 / 0 with a quoted sentence, counted false claims, and
  stated a preference. A second grader then re-scored all five tasks with X and Y
  swapped.

## Tasks

| Task | Fixture | What it tests | Traps (abridged) |
|---|---|---|---|
| T1 | pallets/itsdangerous @ 672971d | wrong prior | key rotation already exists; key order; Flask `SECRET_KEY_FALLBACKS`; other `SECRET_KEY` users; key retirement |
| T2 | baizhiyuan/home-nas @ 797d98c | remote device, late prior | Jetson no longer the NAS; versions recorded in a draft; the OS-upgrade prior is wrong; 6.7 GB shared memory / CUDA 11.4; access (trap wording was wrong, see below) |
| T3 | [fixtures/tokbench](fixtures/tokbench) | measured result | gain inside noise; different machines; 3 % cache hit rate; no prediction before the data (post-hoc); the discriminating rerun |
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
| of which uncached | 154 k | 189 k | +22 % |
| Output tokens (incl. reasoning) | 11.7 k | 19.6 k | +69 % |
| Wall time (6 runs shared the machine) | 24.5 min | 31.2 min | +28 % |
| Output words | 1173 | 1500 | +28 % |

Arm B read a matching `SKILL.md` on all five of T1–T5 and on none of T6. T6 changed
only the typo in both arms, and B spent fewer tokens than A on it. Round 1 counted two
minor false claims for A (a wrong test line number; "available memory" for total
memory) and none for B; round 2 counted none for either.

## Reading

- **Primary prediction (A 13–16, B 17–21): inconsistent.** A scored 22/25, close to the
  ceiling. The +0.75 difference comes entirely from T3 and is inside the noise for
  n = 1, so the verdict on detection is can't tell. The predicted largest gaps, on T2
  and T4, were zero.
- **Falsification criteria.** The "B ≤ A" falsifier is can't tell for the same reason:
  +0.75 is inside the noise. The cost falsifier (> 2× for ≤ 1 extra trap) was not met
  (1.47× input tokens).
- **Activation and control: consistent.** B read a matching skill on 5 of 5 tasks and
  on no T6 run; T6 was a clean one-line edit in both arms.
- **Cost: roughly consistent, and noisy.** +47 % input tokens sits at the top of the
  predicted 10–50 % band, but the cached share differs (+22 % uncached). The T6 control
  shows how large single-run noise is: on an identical one-line edit B used 24 % fewer
  input tokens than A, outside the predicted ±20 %.
- **Preferences that survived the swap: T1 and T3, both B.** On T1 both graders cited a
  warning about a Flask 3.1.0 key-selection advisory (use 3.1.1 or later) and an
  integration test as the first step. Round 1 also cited correct citations (A had one
  wrong line number). On T3 the reason that held in both rounds was the missing
  pre-agreed decision rule (full credit to B and half to A from both graders; that rule is
  `theory-vs-result`'s core). Round 1 also credited B alone with tying the 3 % hit rate
  to doubt that the cache caused the gain; round 2 gave both arms full credit there.
- **What A did better.** On T2, A found the repo's allow-all Tailscale ACL (both
  graders credited it), and round 1 preferred A for that and for stating that JetPack
  6/7 do not support Xavier. On T3, round 1 noted that A came closer to the noise trap
  by reporting means instead of the run-1 headline.
- **Grader bias.** In round 1 the grader preferred the second output five times out of
  five. Preferences are therefore read only where they survive the swap. Trap scores
  were stable across the two rounds (|Δ| ≤ 0.5 per task).

## What this changed in the skills (v4.3.2)

These fixes come from this pilot and have **not** been re-run:

- **Access to a remote device (field note F3).** The pre-registered T2 trap said "no
  recorded access path". That was wrong: the fixture records `ssh nas` (user `hero`) in
  the Jetson-era history note (`docs/admin/现状与路线图.md:103`), and both arms cited the
  line. The alias predates the 11-03 migration that moved the NAS address to the Orange
  Pi, so it probably no longer reaches the Jetson. Neither arm said so, and neither made
  "confirm the login reaches the Jetson" a first step. Arm B read
  `finding-unknowns/SKILL.md`, including the 4.3.1 rule in Technique 5, and still missed
  it. The rule is now one always-on Execution_Policy bullet:
  - cite the recorded access path, or say that none is recorded;
  - never read key material, and make no network probe unless asked;
  - because a record can predate a migration, step 1 of any plan that touches the target
    is to confirm the login reaches the intended machine.
- **Noise floor computed from the data (T3).** Arm B opened with "the recorded p50
  improvement is 5.6 %, but the benchmark does not establish that caching caused it". It
  called the variability substantial, but it never estimated the noise from the five and
  three reruns it had. The trap scored 0.5 in both arms and both rounds. The skill
  already asked for this: a noise floor from rerun spread, the interval governs, and a
  bottom line first. B read the whole file but did not use the Report order. The 4.3.2
  sentence makes the rule more prominent rather than adding a missing one: when the data
  holds reruns, compute the spread and an interval for the difference before any
  headline, and make the headline the verdict.
- **Field note F1 (absence claims).** Neither arm called the versions unknown. Both cited
  `docs/admin/现状与路线图.md:103`. B also mentioned the older research recording JetPack
  5.1.5 and flagged it as historical. Both also cited a build script for CUDA 11.4. This is
  consistent with the 4.3.1 fix, but it does not test the fix, because A did not make the
  mistake either.

## Limitations

- One run per cell. The grader (Claude) is from the skill author's model family, and
  the trap lists were written by the skill author; one trap (T2 #5) had wrong evidence.
  Blinding, quotes and the order swap reduce these biases; they do not remove them.
- Blinding is partial. B's answers carry the skills' own phrasing ("What the checks did
  not prove", "Packet size: compact", "Theory → measured → consistency → mechanism",
  "same-context review, weaker"), and a grader that knows these skills can tell the
  arms apart. Preferences especially are only weakly blinded.
- Web search was available, which partly explains the strong baseline. The extra
  searches in B add to its token cost.
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
    and prints key names, never values. The pilot's homes also carried
    `disable_response_storage = true`; Codex ignored it (logged as an unrecognized
    setting in every run), so the script leaves it out.
  - `run.sh` and `all.sh` run the 12 runs (from `tasks.tsv`).
  - `blind.py` builds the X/Y grading packets. It reads `/tmp/fu-eval/PREREG.md`, so copy
    PREREG.md there first.
  - `swap.py` builds the order-swapped round-2 packets.
  - `usage.py` produces `scores/usage.json`.
  - `grader-prompts.md` holds both grader prompts, verbatim.
  - The scripts assume `/tmp/fu-eval` as the working root, with the fixtures under
    `fixtures/`: the public repos cloned at the commits above, plus the three synthetic
    fixtures copied from here. Each synthetic fixture needs `git init`, `git add -A` and
    `git commit` first, because `run.sh` records `git status` and `git diff`.
- Before publishing a rerun, scrub `outputs/` for host entries or paths from the
  operator's machine. Since v4.3.2 the skill arm may cite recorded access paths.
