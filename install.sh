#!/usr/bin/env bash
# Install the finding-unknowns skill into your global Claude Code skills directory.
set -euo pipefail

DEST="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/finding-unknowns"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills/finding-unknowns"

mkdir -p "$DEST"
cp "$SRC/SKILL.md" "$DEST/SKILL.md"

echo "✅ Installed finding-unknowns → $DEST/SKILL.md"
echo "   Invoke it with the Skill tool: finding-unknowns"
