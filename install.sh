#!/usr/bin/env bash
# Install the finding-unknowns skill (with its references), the companion agents and the
# slash commands into the global Claude Code config directory. Removes 4.x leftovers only
# when they match files this project installed.
set -euo pipefail

CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Skill and references
dest="$CONFIG_DIR/skills/finding-unknowns"
mkdir -p "$dest/references"
cp "$SRC/skills/finding-unknowns/SKILL.md" "$dest/SKILL.md"
cp "$SRC"/skills/finding-unknowns/references/*.md "$dest/references/"
echo "Installed skill  -> $dest (SKILL.md + references/)"

# Copy a file; if a file of the same name exists and is not ours, keep it as .bak first.
install_file() {  # <src> <dest>
  if [ -f "$2" ] && ! grep -qE 'finding-unknowns|theory-vs-result|keep-the-reasoning' "$2"; then
    cp "$2" "$2.bak"
    echo "Kept your own $(basename "$2") as $2.bak"
  fi
  cp "$1" "$2"
}

# Companion agents
AGENT_DEST="$CONFIG_DIR/agents"
mkdir -p "$AGENT_DEST"
for agent in "$SRC"/agents/*.md; do
  install_file "$agent" "$AGENT_DEST/$(basename "$agent")"
  echo "Installed agent  -> $AGENT_DEST/$(basename "$agent")"
done

# Slash commands
CMD_DEST="$CONFIG_DIR/commands"
mkdir -p "$CMD_DEST"
for cmd in "$SRC"/commands/*.md; do
  install_file "$cmd" "$CMD_DEST/$(basename "$cmd")"
  echo "Installed command -> $CMD_DEST/$(basename "$cmd")"
done

# 4.x leftovers. Each is removed only if it carries a marker of this project.
remove_if_ours() {  # <file> <marker regex>
  if [ -f "$1" ] && grep -qE "$2" "$1"; then
    rm "$1"
    echo "Removed 4.x file -> $1"
  fi
}
remove_if_ours "$dest/references/workflows.md" 'fu-execute|Workflow'
for old in keep-the-reasoning theory-vs-result; do
  remove_if_ours "$CONFIG_DIR/skills/$old/SKILL.md" "^name: $old\$"
  rmdir "$CONFIG_DIR/skills/$old" 2>/dev/null || true
done
for old in blindspot cartographer change-quiz finding-unknowns keep-the-reasoning theory-vs-result; do
  f="$CMD_DEST/$old.md"
  if [ -f "$f" ] && grep -qE 'Skill tool|SKILL\.md' "$f"; then
    remove_if_ours "$f" 'finding-unknowns|keep-the-reasoning|theory-vs-result'
  fi
done

echo
echo "Done. Skill: finding-unknowns. Commands: /fu-brief, /fu-catch-up, /fu-debrief, /fu-cartographer."
echo "Agents (blindspot-scout, mechanism-auditor, quiz-master; ledger-keeper and prototype-smith for structured mode)"
echo "are delegated to by the skill."
echo "Cards live in .finding-unknowns/tasks/ in each project; see the skill's references/card.md."
