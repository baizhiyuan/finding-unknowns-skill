---
description: "Enter Cartographer mode directly — ambiguity-scored, coverage-gated, regret-weighted discovery with a persistent unknowns ledger."
argument-hint: "[--quick|--standard|--deep] <task>"
---

# cartographer

Direct entry into Cartographer mode, skipping lightweight-lane routing.

## Dispatch

1. Read the full skill instructions from `skills/finding-unknowns/SKILL.md` in this plugin
   (or `~/.claude/skills/finding-unknowns/SKILL.md` for manual installs).
2. Jump to **Phase C: Cartographer mode** and follow it exactly — resolve and announce the
   clarity threshold (first line), run the Round 0 topology gate, seed the ledger (C0),
   run the score-gated clearing loop (C1) with the standard round-report template
   (four-quadrant score table every round), enforce the dual coverage+ambiguity gate (C2),
   and end at the approval-gated execution bridge (Phase E). Delegate ledger bookkeeping
   and quadrant scoring to the `ledger-keeper` agent when installed.
3. Depth flags map to threshold presets: `--quick` 0.35 · `--standard` 0.25 (default) ·
   `--deep` 0.15. A flag overrides any settings value; announce the source accordingly.
4. Treat the user's remaining arguments as the task under investigation:

```text
$ARGUMENTS
```

If no arguments were given, ask for the task first; do not seed a ledger for an unstated
goal.
