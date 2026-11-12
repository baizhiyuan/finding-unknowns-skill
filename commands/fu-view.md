---
description: "Render a task card, or the task list, as a local HTML page."
argument-hint: "[slug | --list]"
---

# fu-view

1. Invoke the `finding-unknowns` skill with the Skill tool and read `references/view.md`.
2. Run `fu render {slug}` (or `fu render --list`); with no argument, the most recently
   changed card (say which in one line).
3. On lint FAILs, fix the card, never the HTML, and re-run. Report the path in one line.
