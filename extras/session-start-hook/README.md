# SessionStart hook (not shipped)

At session start this hook prints the header of each open task card: its goal, state
and the next decision that needs you. In learn mode it prints only the goal line, so
that `/catch-up` can still ask its recall questions before you see the rest. It prints
nothing when no card is open.

It is **not** part of the plugin. The 5.0 design ([§8](../../docs/design/5.0.md)) ships
it only if the Stage 0 evaluation shows that a fresh session reads the card first in at
least 5 of 6 runs with the hook and in at most 3 of 6 without it. Until then it lives
here, outside the plugin's `hooks/` directory, so Claude Code does not load it.

To try it yourself, copy `hooks/` into the installed plugin's root.
