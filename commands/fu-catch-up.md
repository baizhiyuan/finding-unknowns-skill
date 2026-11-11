---
description: "Catch up on a task card: only what changed since you last looked, and the next decision that needs you (recall questions first in learn mode)."
argument-hint: "[slug]"
---

# fu-catch-up

## Dispatch

1. Invoke the `finding-unknowns` skill with the Skill tool and run its **/fu-catch-up**
   steps on the card named by the argument. With several open cards under
   `.finding-unknowns/tasks/` and no argument, take the most recently changed and say so
   in one line; do not ask.
2. Read the card's header, including its `Structured` flag: with `yes` or `cartographer`,
   also load `references/structured.md` (and, for `cartographer`, the ledger and
   `references/cartographer.md` § Resume).
3. In learn mode only, recall questions before showing the card (`references/debrief.md`;
   `quiz-master` may draft them). Then reconcile the card with the files and runs, show
   only what changed after "Last seen", and update "Last seen".
