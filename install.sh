#!/usr/bin/env bash
# Install the finding-unknowns skill and its companion agents into the global
# Claude Code configuration directory.
set -euo pipefail

CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Skill
SKILL_DEST="$CONFIG_DIR/skills/finding-unknowns"
mkdir -p "$SKILL_DEST"
cp "$SRC/skills/finding-unknowns/SKILL.md" "$SKILL_DEST/SKILL.md"
echo "Installed skill  -> $SKILL_DEST/SKILL.md"

# Companion agents
AGENT_DEST="$CONFIG_DIR/agents"
mkdir -p "$AGENT_DEST"
for agent in "$SRC"/agents/*.md; do
  cp "$agent" "$AGENT_DEST/$(basename "$agent")"
  echo "Installed agent  -> $AGENT_DEST/$(basename "$agent")"
done

# Slash commands
CMD_DEST="$CONFIG_DIR/commands"
mkdir -p "$CMD_DEST"
for cmd in "$SRC"/commands/*.md; do
  cp "$cmd" "$CMD_DEST/$(basename "$cmd")"
  echo "Installed command -> $CMD_DEST/$(basename "$cmd")"
done

echo
echo "Done. Invoke the skill via the Skill tool: finding-unknowns"
echo "Agents (blindspot-scout, prototype-smith, ledger-keeper, quiz-master)"
echo "are available to the Agent tool and are delegated to automatically by the skill."
