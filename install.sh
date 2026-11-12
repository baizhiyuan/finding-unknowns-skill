#!/usr/bin/env bash
# Install the finding-unknowns skill (with its references), the mechanism-auditor agent,
# the slash commands and, once it exists, the fu script into the global Claude Code config
# directory. Removes files of earlier versions only when they carry a marker of this
# project; a file of the same name that is not ours is kept as .bak (an existing .bak is
# never overwritten; a timestamped name is used instead).
# No guard hook: the PreToolUse/PostToolUse guard ships with the plugin only, so with this
# install the irreversible step's yes is a chat yes to the exact command.
set -euo pipefail

CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Skill and references
dest="$CONFIG_DIR/skills/finding-unknowns"
mkdir -p "$dest/references"
cp "$SRC/skills/finding-unknowns/SKILL.md" "$dest/SKILL.md"
cp "$SRC"/skills/finding-unknowns/references/*.md "$dest/references/"
echo "Installed skill  -> $dest (SKILL.md + references/)"

# Copy a file; if a file of the same name exists and is not ours, keep it as .bak first
# (or .bak.{timestamp} when a .bak already exists).
install_file() {  # <src> <dest>
  if [ -f "$2" ] && ! grep -qE 'finding-unknowns|theory-vs-result|keep-the-reasoning' "$2"; then
    bak="$2.bak"
    [ -e "$bak" ] && bak="$2.bak.$(date +%Y%m%d-%H%M%S)"
    cp "$2" "$bak"
    echo "Kept your own $(basename "$2") as $bak"
  fi
  cp "$1" "$2"
}

# Agent
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

# The fu script. The skill calls it as {skill dir}/../../scripts/fu.py, which is
# $CONFIG_DIR/scripts/fu.py in this layout (docs/design/fu-cli.md). An existing fu.py is
# ours when it contains the marker string "finding-unknowns".
if [ -f "$SRC/scripts/fu.py" ]; then
  mkdir -p "$CONFIG_DIR/scripts"
  install_file "$SRC/scripts/fu.py" "$CONFIG_DIR/scripts/fu.py"
  echo "Installed script -> $CONFIG_DIR/scripts/fu.py"
fi

# Earlier versions. Each file is removed only if it carries a marker of this project.
remove_if_ours() {  # <file> <marker regex>
  if [ -f "$1" ] && grep -qE "$2" "$1"; then
    rm "$1"
    echo "Removed old file -> $1"
  fi
}
# 4.x
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
# Structured mode and the agents cut in 5.2 (they live on branch v4)
remove_if_ours "$dest/references/structured.md" '^# Structured mode'
remove_if_ours "$dest/references/cartographer.md" '^# Cartographer Mode'
remove_if_ours "$dest/references/handoff-full.md" '^# The full handoff packet'
remove_if_ours "$dest/references/results-examples.md" '^# Results: examples and anti-patterns'
f="$CMD_DEST/fu-cartographer.md"
if [ -f "$f" ] && grep -q 'finding-unknowns' "$f"; then
  remove_if_ours "$f" 'Cartographer'
fi
for old in blindspot-scout ledger-keeper prototype-smith quiz-master; do
  f="$AGENT_DEST/$old.md"
  if [ -f "$f" ] && grep -qE "^name: $old\$" "$f"; then
    remove_if_ours "$f" 'finding-unknowns'
  fi
done

echo
echo "Done. Skill: finding-unknowns. Commands: /fu-brief, /fu-catch-up, /fu-debrief, /fu-view."
echo "Agent: mechanism-auditor (used for irreversible-lane cards, measured results, or on request)."
echo "Cards live in .finding-unknowns/tasks/ in each project; see the skill's references/card.md."
echo "No guard hook with install.sh (plugin only): irreversible steps need your chat yes to the exact command."
