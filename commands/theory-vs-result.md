---
description: "Report a measured result as Theory → Measured → Consistent? → Mechanism (理论预期 → 实测 → 是否一致 → 机理): prediction first, noise floor, evidence-tiered mechanism, rule verdict kept apart from direction verdict."
---

# theory-vs-result

Dispatch command for the theory-vs-result skill.

## Dispatch

1. Read `skills/theory-vs-result/SKILL.md` from this plugin (or
   `~/.claude/skills/theory-vs-result/SKILL.md` for manual installs).
2. Follow it exactly, starting at Step 0 (triage). If nothing has been measured yet, stop
   after Step 1 (the prediction card). If the result has already been seen, write the
   Step 1 card marked `post-hoc`, then continue from Step 2.
3. Treat the user's arguments as the result or planned measurement (default: the current
   session's most recent result):

```text
$ARGUMENTS
```
