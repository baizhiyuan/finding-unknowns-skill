---
description: "Catch up on a task card: recall questions first, then only what changed since you last looked, and the next decision that needs you."
argument-hint: "[slug]"
---

# fu-catch-up

## Dispatch

1. Invoke the `finding-unknowns` skill with the Skill tool and run its **/fu-catch-up**
   steps on the card named by the argument, or list the open cards under
   `.finding-unknowns/tasks/` and suggest the most recently changed.
2. Recall questions before showing the card (`references/debrief.md`; `quiz-master` may
   draft them). Then reconcile the card with the files and runs, show only what changed
   after "Last seen", and update "Last seen".
