#!/usr/bin/env bash
# cut_plugin.sh : extract the 5.2 plugin for the Tier 1 plugin arm from a fixed commit.
#   FU_PLUGIN_COMMIT (required)  commit/ref in the v5 worktree, e.g. the commit with the guard fix
#   FU_PLUGIN_DIR    (optional)  destination, default ~/.cache/fu-tier1/plugin-52
# Writes the resolved full SHA to $FU_PLUGIN_DIR/.fu-commit; run_task.py refuses the plugin arm when it
# differs from FU_PLUGIN_COMMIT.
set -euo pipefail
REPO=/home/bzyhero/project/skills-work/finding-unknowns-skill-v5
: "${FU_PLUGIN_COMMIT:?set FU_PLUGIN_COMMIT to the plugin commit}"
DEST=${FU_PLUGIN_DIR:-$HOME/.cache/fu-tier1/plugin-52}
SHA=$(git -C "$REPO" rev-parse --verify "${FU_PLUGIN_COMMIT}^{commit}")
rm -rf "$DEST"
mkdir -p "$DEST"
git -C "$REPO" archive "$SHA" .claude-plugin agents commands skills scripts hooks bin | tar -x -C "$DEST"
echo "$SHA" > "$DEST/.fu-commit"
test -f "$DEST/.claude-plugin/plugin.json" && test -f "$DEST/commands/fu-brief.md" && test -f "$DEST/hooks/hooks.json"
echo "plugin cut: $DEST @ $SHA"
