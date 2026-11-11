---
description: "Structured mode, high stakes: Cartographer — a coverage-gated, regret-ordered unknowns ledger with a per-round clarity display, a six-condition gate and a spec with a verification contract, on top of the task card."
argument-hint: "[--quick|--standard|--deep] <task>"
---

# fu-cartographer

Direct entry into Cartographer mode (structured mode, high stakes).

## Dispatch

1. Invoke the `finding-unknowns` skill with the Skill tool, then read its
   `references/structured.md` and `references/cartographer.md` in full;
   `cartographer.md` is the normative protocol.
2. The task card still applies: the person predicts first, the spec's verification
   contract becomes the card's contract, and the card's Brief freezes on the person's
   approval of the spec.
3. Follow Cartographer mode exactly:
   - announce the depth on the first line;
   - run the Round 0 topology gate;
   - seed the ledger (C0);
   - run the regret-ordered clearing loop (C1), with the four-quadrant clarity display
     every round;
   - enforce the six-condition gate and the irreversibility floor (C2);
   - write the spec with its verification contract (C2.5);
   - stop and offer the next step (§ E1).
4. In any build from the spec, irreversible steps are prepared, not executed (the build
   rule). Delegate ledger bookkeeping and quadrant scoring to `ledger-keeper` when
   available.
5. Depth flags (see the depth table in `references/cartographer.md`):
   - `--quick`: a single-lens pass, with a soft check every 5 rounds;
   - `--standard` (the default): one blind-spot pass, escalating to a multi-lens sweep
     when the task spans several risk domains;
   - `--deep`: a multi-lens sweep, plus loop-until-dry on unknown unknowns before the gate.
6. Treat the remaining arguments as the task:

```text
$ARGUMENTS
```

If no arguments were given, ask for the task first; do not seed a ledger for an unstated
goal.
