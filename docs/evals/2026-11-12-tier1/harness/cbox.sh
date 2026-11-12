#!/usr/bin/env bash
# cbox.sh HOME WORKDIR MODE(rw|ro) -- cmd...   : run cmd with / read-only, only WORKDIR (+HOME) writable, ~/.ssh hidden
# Stage 0b changes: CBOX_NO_CRED=1 skips the OAuth credentials bind (qwen subject uses its own token from env,
# inherited by bwrap); ~/.config/fu-eval (holds the qwen env file) is hidden from the sandbox when it exists.
H=$1; W=$2; MODE=$3; shift 4
WB=--bind; [ "$MODE" = ro ] && WB=--ro-bind
CRED=(); [ -z "$CBOX_NO_CRED" ] && CRED=(--bind "$HOME/.claude/.credentials.json" "$HOME/.claude/.credentials.json")
HIDE=(); [ -d "$HOME/.config/fu-eval" ] && HIDE=(--tmpfs "$HOME/.config/fu-eval")
exec bwrap --unshare-pid --unshare-ipc --die-with-parent --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp \
  --bind "$H" "$H" $WB "$W" "$W" \
  "${CRED[@]}" \
  --tmpfs "$HOME/.ssh" --tmpfs "$HOME/.codex" --tmpfs "$HOME/.config/gh" --tmpfs "$HOME/project" "${HIDE[@]}" \
  --ro-bind /dev/null "$HOME/.claude/CLAUDE.md" --tmpfs "$HOME/.claude/projects" \
  ${CBOX_RO:+--ro-bind "$CBOX_RO" "$CBOX_RO"} \
  --setenv CLAUDE_CONFIG_DIR "$H" --setenv TMPDIR "$H/tmp" --chdir "$W" "$@"
