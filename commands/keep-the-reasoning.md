---
description: "Hand off agent work without surrendering judgment — evidence first, decisions listed, what the checks did NOT prove, what went unchecked."
---

# keep-the-reasoning

Dispatch command for the keep-the-reasoning skill.

## Dispatch

1. Read `skills/keep-the-reasoning/SKILL.md` from this plugin (or
   `~/.claude/skills/keep-the-reasoning/SKILL.md` for manual installs).
2. Follow it exactly, starting at Step 0 (stakes triage). If the work is already done,
   go straight to Step 3 (the handoff packet) and state that verification was defined
   after the fact.
3. Treat the user's arguments as the work or decision being handed off (default: the
   current session's most recent deliverable):

```text
$ARGUMENTS
```
