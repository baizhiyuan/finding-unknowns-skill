#!/usr/bin/env bash
# Install the finding-unknowns skill (with its references), the mechanism-auditor agent,
# the slash commands and the fu script into the global Claude Code config directory.
# A file counts as ours only when one of its first three lines starts with
# "# finding-unknowns:" or "#finding-unknowns:" (scripts/fu.py line 2, the agent's and
# commands' frontmatter line 2). A same-named file that is not ours is moved to a
# timestamped .bak, never deleted; files of earlier versions are moved to a .bak only
# when they carry the marker. A symlink at a destination is removed, never followed.
# No guard hook: the PreToolUse/PostToolUse guard ships with the plugin only, so with this
# install the irreversible step's yes is a chat yes to the exact command.
set -euo pipefail

CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"

is_ours() {  # <file>
  [ -f "$1" ] && [ ! -L "$1" ] && head -n 3 "$1" | grep -qE '^# ?finding-unknowns:'
}

# Move a file aside as {file}.bak.{timestamp} (never overwriting an existing name).
set_aside() {  # <file>
  local bak="$1.bak.$STAMP" n=0
  while [ -e "$bak" ] || [ -L "$bak" ]; do n=$((n + 1)); bak="$1.bak.$STAMP.$n"; done
  mv "$1" "$bak"
  echo "Moved aside -> $bak"
}

# Copy <src> to <dest>: a symlink at <dest> is removed (not followed); a regular file that
# is not ours is set aside first.
install_file() {  # <src> <dest>
  if [ -L "$2" ]; then
    rm -f "$2"
  elif [ -e "$2" ] && ! is_ours "$2"; then
    set_aside "$2"
  fi
  cp "$1" "$2"
}

# Skill and references (the skill directory is ours by name; only symlinks are guarded)
dest="$CONFIG_DIR/skills/finding-unknowns"
mkdir -p "$dest/references"
for f in "$SRC/skills/finding-unknowns/SKILL.md" "$SRC"/skills/finding-unknowns/references/*.md; do
  rel="${f#"$SRC/skills/finding-unknowns/"}"
  [ -L "$dest/$rel" ] && rm -f "$dest/$rel"
  cp "$f" "$dest/$rel"
done
echo "Installed skill  -> $dest (SKILL.md + references/)"

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
# $CONFIG_DIR/scripts/fu.py in this layout (docs/design/fu-cli.md).
mkdir -p "$CONFIG_DIR/scripts"
install_file "$SRC/scripts/fu.py" "$CONFIG_DIR/scripts/fu.py"
echo "Installed script -> $CONFIG_DIR/scripts/fu.py"

# Earlier versions: set aside only files that carry the marker. Files without it (all of
# 4.x, and any skill of the same name installed separately, e.g. keep-the-reasoning) stay.
retire_if_ours() {  # <file>
  if is_ours "$1"; then set_aside "$1"; fi
}
# References of 4.x/5.0 inside this skill's own directory carry no marker; they are
# recognised by their first heading and set aside, not deleted.
for pair in 'workflows:^# .*Workflow' 'structured:^# Structured mode' 'cartographer:^# Cartographer Mode' \
            'handoff-full:^# The full handoff packet' 'results-examples:^# Results: examples and anti-patterns'; do
  f="$dest/references/${pair%%:*}.md"
  if [ -f "$f" ] && [ ! -L "$f" ] && head -n 3 "$f" | grep -qE "${pair#*:}"; then set_aside "$f"; fi
done
for old in blindspot cartographer change-quiz finding-unknowns keep-the-reasoning theory-vs-result fu-cartographer; do
  retire_if_ours "$CMD_DEST/$old.md"
done
for old in blindspot-scout ledger-keeper prototype-smith quiz-master; do
  retire_if_ours "$AGENT_DEST/$old.md"
done

echo
echo "Done. Skill: finding-unknowns. Commands: /fu-brief, /fu-catch-up, /fu-debrief, /fu-view."
echo "Agent: mechanism-auditor (used for irreversible-lane cards, measured results, or on request)."
echo "Cards live in .finding-unknowns/tasks/ in each project; see the skill's references/card.md."
echo "No guard hook with install.sh (plugin only): irreversible steps need your chat yes to the exact command."
