---
description: "Enter Cartographer mode directly — coverage-gated, regret-weighted discovery with a persistent unknowns ledger."
---

# cartographer

Direct entry into Cartographer mode, skipping lightweight-lane routing.

## Dispatch

1. Read the full skill instructions from `skills/finding-unknowns/SKILL.md` in this plugin
   (or `~/.claude/skills/finding-unknowns/SKILL.md` for manual installs).
2. Jump to **Phase C: Cartographer mode** and follow it exactly — announce entry, seed the
   ledger (C0), run the interview loop (C1) with the standard round-report template, and
   enforce the coverage gate (C2) before any implementation. Delegate ledger bookkeeping to
   the `ledger-keeper` agent when installed.
3. Treat the user's arguments as the task under investigation:

```text
$ARGUMENTS
```

If no arguments were given, ask for the task first; do not seed a ledger for an unstated
goal.
