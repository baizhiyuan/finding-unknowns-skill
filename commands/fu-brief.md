---
description: "Start a task with a task card: you predict first, the territory is mapped, then the agent predicts; agree the four stop-points and the contract; freeze and commit the card."
argument-hint: "[--structured] <task>"
---

# fu-brief

## Dispatch

1. Invoke the `finding-unknowns` skill with the Skill tool and run its **/fu-brief** steps:
   mode once per project; the person's prediction first (their prior); the territory,
   using the instruments in `references/brief.md` as the gap needs; then the agent's
   prediction; the Brief (approach with one-line whys, both sides' predictions, the four
   stop-points with a budget multiple, the contract); freeze on the person's yes and
   commit per `references/card.md`.
2. If an open card already covers this task, offer to continue it instead (`/fu-catch-up`).
3. With `--structured`, also load `references/structured.md`. It adds quadrant routing and
   the eight numbered techniques, and offers Cartographer at high stakes.
4. Then build quietly: stop only at the four stop-points; log everything else on the card.
