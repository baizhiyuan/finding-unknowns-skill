---
#finding-unknowns:plugin-file
description: "Debrief a task card for late results or a re-grade: each frozen prediction quoted and graded, yours first; evidence, what the checks did not prove, what needs you."
argument-hint: "[slug]"
---

# fu-debrief

1. Invoke the `finding-unknowns` skill with the Skill tool and follow
   `references/debrief.md` on the named card, else the most recently changed card
   (say which in one line; do not ask).
2. Measured results follow `references/results.md`.
3. A re-grade adds a new Debrief; the earlier one stays. End with
   `fu freeze {slug} --stage debrief`.
