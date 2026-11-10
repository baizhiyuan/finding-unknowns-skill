---
description: "Enter Cartographer mode directly — coverage-gated, regret-weighted discovery with a persistent unknowns ledger and a per-round clarity display."
argument-hint: "[--quick|--standard|--deep] <task>"
---

# cartographer

Direct entry into Cartographer mode, skipping lightweight-lane routing.

## Dispatch

1. Read `skills/finding-unknowns/SKILL.md` in this plugin (or
   `~/.claude/skills/finding-unknowns/SKILL.md` for manual installs), then read
   `references/cartographer.md` next to it in full — that file is the normative protocol.
2. Follow **Cartographer mode** exactly — resolve and announce the depth (first line),
   run the Round 0 topology gate, seed the ledger (C0), run the regret-ordered clearing
   loop (C1) with the standard round-report template (four-quadrant clarity display
   every round), enforce the six-condition gate and the irreversibility floor (C2), write
   the spec with its verification contract (C2.5), then stop and offer the next step
   (§ E1: consensus-refine plan or keep refining). Workflow execution (§ E2) is
   experimental and runs only on explicit request. In any build from the spec,
   irreversible steps are prepared, not executed: the user runs each one or gives a
   per-command yes (C2.5 build rule). Delegate ledger bookkeeping and quadrant scoring to
   the `ledger-keeper` agent when installed.
3. Depth flags (see the depth table in `references/cartographer.md`): `--quick` =
   single-lens blind-spot pass, soft check at round 5 and every 5 rounds after ·
   `--standard` (default) = one blind-spot pass (full report), escalating to a
   multi-lens sweep when the task spans more than one risk domain (e.g. money + data +
   infra); soft check at round 10 and every 10 after · `--deep` = always a multi-lens
   sweep, plus UU loop-until-dry before the gate. Announce the depth and its source;
   `findingUnknowns.ambiguityThreshold` is ignored since 4.2.0.
4. Treat the user's remaining arguments as the task under investigation:

```text
$ARGUMENTS
```

If no arguments were given, ask for the task first; do not seed a ledger for an unstated
goal.
