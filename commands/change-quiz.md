---
description: "Generate a change report and a must-pass comprehension quiz before merging."
---

# change-quiz

Direct entry into Technique 8 (quiz) — comprehension is the merge gate.

## Dispatch

1. Read `skills/finding-unknowns/SKILL.md` from this plugin (or
   `~/.claude/skills/finding-unknowns/SKILL.md` for manual installs).
2. Run **Technique 8 — Quiz** exactly as specified: report first (Context, What changed,
   How it interacts, Intuition), then 5–8 questions weighted toward deviations and
   interaction effects, honest grading with miss classification, and the two-round stop
   rule. Delegate to the `quiz-master` agent when installed — an examiner that did not
   write the change asks harder questions.
3. Treat the user's arguments as the change to examine (branch, diff range, or session
   description; default: working tree vs merge base):

```text
$ARGUMENTS
```
