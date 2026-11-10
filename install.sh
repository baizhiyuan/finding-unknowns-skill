#!/usr/bin/env bash
# Install the skills (finding-unknowns, keep-the-reasoning, theory-vs-result), their references, the
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

# Remove our old pass-through commands (pre-4.3.0): they shared a name with a skill and
# shadowed it. Only files that look like our pass-through are removed.
for old in finding-unknowns keep-the-reasoning theory-vs-result; do
  stale="$CMD_DEST/$old.md"
  if [ -f "$stale" ] && grep -q 'description:' "$stale" \
      && grep -qE 'Skill tool|SKILL\.md' "$stale"; then
    rm "$stale"
    echo "Removed stale command -> $stale (the /$old skill now answers to /$old)"
  fi
done

echo
echo "Done. Skills: finding-unknowns, keep-the-reasoning, theory-vs-result (invoke as /finding-unknowns,"
echo "/keep-the-reasoning, /theory-vs-result, or via the Skill tool)."
echo "Commands: /blindspot, /cartographer, /change-quiz."
echo "Agents (blindspot-scout, prototype-smith, ledger-keeper, quiz-master, mechanism-auditor)"
echo "are available to the Agent tool and are delegated to automatically by the skill."
