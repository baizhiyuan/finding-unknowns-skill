---
description: "Start a task with a task card: you predict first, the territory is mapped, then the agent predicts; agree the four stop-points and the contract; freeze and commit the card."
argument-hint: "[--structured] <task>"
---

# fu-brief

## Dispatch

1. Invoke the `finding-unknowns` skill with the Skill tool. Its base directory is shown
   when it loads; every `references/…` path below is relative to that directory.
2. With `--structured`, read `references/structured.md` before anything else. It adds
   quadrant routing and the eight numbered techniques, and offers Cartographer at high
   stakes. Phase 0 and Techniques 1–5 run inside the Brief; Technique 5's Definition of
   verified becomes the card's contract. Record `Structured: yes` on the card.
3. Run the skill's **/fu-brief** steps: ship mode unless the person asks to learn; the
   person's prediction first (their prior); the territory, using the instruments in
   `references/brief.md` as the gap needs; then the agent's prediction; the Brief
   (approach with one-line whys, both sides' predictions, the four stop-points with a
   budget multiple, the contract); freeze on the person's yes and commit per
   `references/card.md`.
4. If an open card already covers this task, say so in the first message; pointing to
   `/fu-catch-up` is the offer (it counts toward the three questions), and the Brief
   continues with a new card only if the person asks for one. Other offers go in the first
   message and count toward its three questions; the plan's decisions and any
   reference-extraction confirmation are bundled into the single Brief-approval ask.
5. Then build quietly: stop only at the four stop-points; log everything else on the card.
   Each turn ends with a completion report or a stop-point request.
