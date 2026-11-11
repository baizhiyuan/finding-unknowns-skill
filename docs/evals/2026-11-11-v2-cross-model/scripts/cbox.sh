#!/usr/bin/env bash
# cbox.sh HOME WORKDIR MODE(rw|ro) -- cmd...   : run cmd with / read-only, only WORKDIR (+HOME) writable, ~/.ssh hidden
H=$1; W=$2; MODE=$3; shift 4
WB=--bind; [ "$MODE" = ro ] && WB=--ro-bind
exec bwrap --unshare-pid --unshare-ipc --die-with-parent --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind "$H" "$H" $WB "$W" "$W" \
  --bind "$HOME/.claude/.credentials.json" "$HOME/.claude/.credentials.json" \
  --tmpfs "$HOME/.ssh" --tmpfs "$HOME/.codex" --tmpfs "$HOME/.config/gh" --tmpfs "$HOME/project" \
  --ro-bind /dev/null "$HOME/.claude/CLAUDE.md" --tmpfs "$HOME/.claude/projects" \
  --setenv CLAUDE_CONFIG_DIR "$H" --setenv TMPDIR "$H/tmp" --chdir "$W" "$@"
