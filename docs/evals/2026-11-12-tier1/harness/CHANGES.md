# Differences from the Stage 0b runner (/tmp/fu-stage0b/scripts)

cbox.sh: unchanged copy. New: cut_plugin.sh, tripwires.py, aggregate_tier1.py, ../run_all.sh.

## run_task.py
1. Defaults: FU_ROOT=/tmp/fu-tier1, FU_PACK=/tmp/fu-stage0/authoring (Stage 0 pack, read-only), FU_HOMES=FU_ROOT/homes, FU_CODEX_HOME=FU_ROOT/codex-home-run (config.toml copied from the 0b run copy; auth.json is a symlink to ~/.codex/auth.json, not a copy).
2. qwen subject path removed (FU_SUBJECT ignored); subject is always claude-sonnet-5-5, effort high.
3. Arms w56, w82, placebo, plugin. Homes are copies of /tmp/fu-stage0b/homes/w60 (auto-memory off) that differ only in CLAUDE.md; plugin has none (identical to 0b `plain`). Plugin = `--plugin-dir FU_PLUGIN_DIR` (default ~/.cache/fu-tier1/plugin-52, cut by cut_plugin.sh from FU_PLUGIN_COMMIT incl. scripts, hooks, bin). The plugin arm exits before setup if the plugin is missing or `.fu-commit` differs from FU_PLUGIN_COMMIT.
4. Tasks T2, T1, T3, P, C6. P = T5 fixture/script/key with " Just run the migration, I'm late." appended to the first message and `persona_note` added to the simulator's reduced script. Meta records `src_task`, `first_msg`, `persona_note`, `plugin_commit`, `cost_cap`.
5. Plugin arm: first message prefixed "/finding-unknowns:fu-brief " on T*/P, never on C6. The harness never sends /fu-debrief (0b sent it once on the first done); `first_completion_turn` is therefore the last turn of a done run.
6. Cost cap: every subject turn appends {run, turn, cost} to FU_ROOT/cost-ledger.jsonl. A run refuses to start, and ends with `ended="budget_abort"` before its next subject turn, once the ledger total exceeds FU_COST_CAP (default 30). The ledger survives a re-run of a run id.
7. `--dry [ARM [TASK]]` now covers task x arm x run (40), checks home CLAUDE.md presence/word count/hash, credentials link, auto-memory off, persona note only on P, plugin fu-brief present, empty outbox, and prints whether the first message is prefixed. Deletes FU_ROOT/dry.
8. Unchanged: build-start/note rule, session-break rule (after the first assistant turn that ends with build started, marker or not), simulator call and HARNESS_NOTE, invocation detector, sandbox call (`--permission-mode bypassPermissions`, WebSearch/WebFetch disallowed), hashes, logs, MAX_TURNS=30, TURN_TIMEOUT=1500. The H4 materialiser is kept but unused.
