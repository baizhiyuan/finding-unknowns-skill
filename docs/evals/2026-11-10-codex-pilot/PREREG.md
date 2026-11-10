# Pilot eval: plain Codex vs Codex + finding-unknowns skills (pre-registered)

Written 2026-11-10, before any eval run. Not edited after runs start; any later change is
appended under "Amendments" with a reason.

## Setup

- Model: gpt-6.1-sol via `codex exec` (codex-cli 0.164.0), reasoning effort high (user default).
- Arm A (plain): isolated CODEX_HOME, auth + model/provider only; Codex built-in system
  skills only (imagegen, openai-docs, skill-creator, skill-installer). No AGENTS.md, no OMX.
- Arm B (skills): identical, plus `finding-unknowns`, `keep-the-reasoning`,
  `theory-vs-result` from finding-unknowns-skill v4.3.1 (tag v4.3.1) in CODEX_HOME/skills.
  The prompt never names a skill: this measures natural activation + effect together.
- One run per task per arm (pilot). Fresh copy of the fixture per run. Non-interactive:
  the first response is what gets scored.
- Sandbox: read-only for T1–T5, workspace-write for T6. No network in the sandbox.
- Captured: final message, JSONL events (token usage, commands run, files read), wall time.

## Scoring (blinded)

For each task, a grader that did not produce either output receives the two final
messages labelled X/Y in random order (mapping kept in a separate file), the task prompt,
and the trap list with evidence below. Per output:

- **Traps caught**: each trap 1 (clearly surfaced, with reason), 0.5 (hinted, or
  surfaced without the key reason), 0 (missed). Quote the sentence that earns the score.
- **False claims**: statements contradicted by the fixture or by the listed facts.
- **Territory questions**: questions put to the user whose answer is in the fixture.
- **Actionable**: would the user's next step be right if they followed the output? (yes/partly/no)
- **Preference**: which output would you rather receive, and why (one line).
- Cost: output words (computed), tokens and wall time (from logs, not shown to grader).

Primary metric: traps caught, summed over T1–T5 (max 25 per arm).
Negative control T6: pass = typo fixed, nothing else changed, no discovery ceremony
(no routing announcement, no blind-spot report, no questions); also compare words/tokens.

## Tasks and traps

### T1 itsdangerous key rotation (fixture: pallets/itsdangerous @ 672971d)
Prompt: "I'm a grad student new to this library. I want to add secret-key rotation to
itsdangerous so our Flask app can change its SECRET_KEY without logging everyone out. I
think I'll need to add a new parameter to Signer and change how signatures are verified.
Where should I start?"
Traps:
1. Rotation already exists: `secret_key` accepts a list (signer.py:68-73, 143); verify
   tries every key (signer.py:236-240); CHANGES.rst:92-94; docs/concepts.rst:101-125.
2. Order: oldest → newest, the last key signs (signer.py:176-180).
3. Flask side: configure via Flask (`SECRET_KEY_FALLBACKS`, Flask ≥ 3.1) rather than patching the library.
4. Scope: other SECRET_KEY consumers (Flask-WTF CSRF, Flask-Login remember-me, own HMAC) do not rotate through this.
5. Retirement: old keys stay valid until removed; drop after max session lifetime; keep salt/algorithm unchanged.

### T2 Jetson small LLM (fixture: baizhiyuan/home-nas @ 797d98c, Chinese prompt)
Prompt: "我想在家里这台 Jetson Xavier NX 上部署一个小型大模型，给 home-nas 用。platform/jetson
已经有了，我想应该就是在 stacks 里加一个 aarch64 的 CUDA 容器。另外能不能把 Jetson 升级到
Ubuntu 24.04，或者用 Anaconda，这样就能跑最新的模型？帮我出个方案。"
Traps:
1. The Jetson is no longer the NAS: Orange Pi 5B took over on 11-03 (README.md:131, 179);
   `stacks/` deploy to the NAS; the Jetson is planned as a separate AI node reached over
   Tailscale (README.md:211).
2. Versions are recorded: JetPack 5.1.5 = CUDA 11.4 / Ubuntu 20.04 / Python 3.8
   (docs/_drafts/Immich-GPU-可行性.md:14). Calling them unknown without citing = miss.
3. Upgrade prior is wrong: Xavier NX officially tops out at JetPack 5.x / Ubuntu 20.04
   (JetPack 6 is Orin-only); Anaconda doesn't change the driver/CUDA; model support comes
   from the runtime (e.g. llama.cpp), not the OS version.
4. Resources: ~6.7–6.8 GB memory shared CPU/GPU (README.md:38; drafts:9); CUDA-12-only
   images won't run on CUDA 11.4 (the Immich GPU attempt failed on exactly this,
   drafts:14) → small quantized model, native/L4T-matched build.
5. Access: no recorded SSH entry/login for the Jetson (README only documents `ssh opi`);
   reachability (Tailscale `jetson-nas` 100.125.87.97) must be checked first.

### T3 tokenizer cache benchmark (fixture: synthetic `tokbench`)
Prompt: "We added an lru_cache to the tokenizer. p50 latency went from 41.2 ms to 38.9 ms
(results in bench/). Write up the result for the team and tell me whether we should ship
it as a performance win."
Traps:
1. Inside the noise: baseline p50 mean 40.9 (sd ≈ 1.8, n=5), cache 39.1 (sd ≈ 1.6, n=3);
   Δ ≈ 1.8 ms, Welch t ≈ 1.5; the headline compares run 1 vs run 1.
2. Not like-for-like: different machines (ci-runner-1 vs -2) and dates.
3. Mechanism unsupported: hit rate 1187/(1187+38412) ≈ 3 % on a unique-word corpus
   (bench/cache_stats.txt) — the cache can't plausibly explain the gain.
4. No prediction before the data / post-hoc framing; claim should be "can't tell".
5. Names the discriminating check: same machine, interleaved runs, more repetitions
   (and/or a corpus with realistic repetition).

### T4 agent PR handoff (fixture: synthetic `durations`, PR already applied)
Prompt: "My coding agent finished this PR — see pr.diff and agent-summary.md. Tests pass.
Can I merge it?"
Traps:
1. A failing test was deleted (`test_rejects_garbage`), described as "obsolete".
2. `except Exception: return 0` swallows the ValueError the docstring promises; bad input
   now silently returns 0.
3. Caller breaks: cli.py relies on ValueError for exit code 2 → now prints 0, exits 0.
4. The reported bug (`parse_duration(None)`) isn't tested; "3 passed" doesn't prove the fix
   or the edge cases — what the check did not prove.
5. Recommends a concrete path: don't merge as is; restore the test, handle None explicitly
   (TypeError/ValueError), add a test for None and for garbage.

### T5 requests retries (fixture: psf/requests @ 3c7baaa)
Prompt: "Our services call requests.get/post everywhere and flaky upstreams cause errors.
I want to contribute a `retries=` keyword to requests.get()/post() upstream so everyone
gets retries. I think it's a small change in api.py. Where do I start?"
Traps:
1. Already supported: `HTTPAdapter(max_retries=Retry(...))` mounted on a Session
   (src/requests/adapters.py:168-211; docs/user/advanced.rst:1032-1051).
2. Upstream is in a perpetual feature freeze (docs/dev/contributing.rst:155) → PR unlikely.
3. Retrying POST / non-idempotent requests is unsafe; urllib3 Retry excludes POST by default.
4. Defaults: DEFAULT_RETRIES = 0 with read=False (adapters.py:81, 208-209); requests has no
   default timeout, so retries without timeouts don't fix hangs.
5. Policy choices: backoff, status_forcelist, Retry-After; put it in one shared Session.

### T6 negative control (fixture: synthetic `tinydoc`, workspace-write)
Prompt: "Fix the typo 'recieve' in README.md."
Pass: README.md shows "receive", no other file changed, no discovery ceremony or questions.

## Prediction (written before any run)

- Primary: B catches more traps than A over T1–T5: A ≈ 13–16 / 25, B ≈ 17–21 / 25.
  Largest gaps on T2 (access, recorded versions, late prior) and T4 (what the check did
  not prove); smallest on T1 and T5, where a strong model reading the code finds the
  existing feature anyway (expected gap ≤ 1 trap each).
- Activation: B uses a skill on T1–T5 in at least 3 of 5 tasks; on T6 it does not.
- Cost: B spends 10–50 % more tokens on T1–T5; T6 within ±20 % of A.
- What would prove us wrong: B ≤ A on traps (skills add no detection), or B triggers
  ceremony on T6, or B's extra cost > 2× for ≤ 1 extra trap.
- Noise: one run per arm, so a difference of ≤ 1 trap on a single task is inside the
  noise; only the T1–T5 total (and direction across tasks) is read as signal. This pilot
  can show the method works and give a direction; it cannot establish an effect size.

## Known limitations

- n = 1 per cell; grader is Claude (the skill author's model family) — mitigated by
  blinding and a fixed trap list with quotes, not eliminated.
- Trap lists were written by the skill author, who knows what the skill looks for.
- Single-turn: interview techniques can only show up as questions, not answered rounds.

## Amendments
(none)
