#!/usr/bin/env bash
# Install the skills (finding-unknowns, keep-the-reasoning), their references, the
# companion agents, and the slash commands into the global Claude Code config directory.
set -euo pipefail

CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Skills (each with optional references/)
for skill_dir in "$SRC"/skills/*/; do
  name="$(basename "$skill_dir")"
  dest="$CONFIG_DIR/skills/$name"
  mkdir -p "$dest"
  cp "$skill_dir/SKILL.md" "$dest/SKILL.md"
  echo "Installed skill  -> $dest/SKILL.md"
  if [ -d "$skill_dir/references" ]; then
    mkdir -p "$dest/references"
    cp "$skill_dir"/references/*.md "$dest/references/"
    echo "Installed refs   -> $dest/references/"
  fi
done

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
echo "Done. Skills: finding-unknowns, keep-the-reasoning (invoke via the Skill tool)."
echo "Agents (blindspot-scout, prototype-smith, ledger-keeper, quiz-master)"
echo "are available to the Agent tool and are delegated to automatically by the skill."
