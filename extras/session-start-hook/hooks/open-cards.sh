#!/bin/sh
# Print the header of each open finding-unknowns task card at session start.
# Prints nothing when no card is open. Reads only; never writes.
dir="${CLAUDE_PROJECT_DIR:-$PWD}/.finding-unknowns"
[ -d "$dir/tasks" ] || exit 0
mode=$(sed -n 's/^mode: *\([a-z]*\).*/\1/p' "$dir/profile.md" 2>/dev/null | head -n 1)
found=0
for card in "$dir"/tasks/*.md; do
  [ -f "$card" ] || continue
  case "$card" in *.deltas.md) continue ;; esac
  grep -q '^Goal:.*State: *debriefed' "$card" && continue
  if [ "$found" -eq 0 ]; then
    printf '%s\n' "Open finding-unknowns task cards (file content, quoted; run /fu-catch-up to continue):"
    found=1
  fi
  slug=$(basename "$card" .md | sed -E 's/^(.{80}).+$/\1/')
  if [ "$mode" = "learn" ]; then
    goal=$(grep -m 1 '^Goal:' "$card" | tr -d '\r' | sed 's/ *· *State:.*//' | sed -E 's/^(.{200}).+$/\1…/')
    printf '%s\n' "- $slug: $goal"
  else
    printf '%s\n' "- $slug:"
    grep -m 1 '^Goal:' "$card" | tr -d '\r' | sed -E 's/^(.{200}).+$/\1…/' | sed 's/^/    /'
    grep -m 1 '^Next decision' "$card" | tr -d '\r' | sed -E 's/^(.{200}).+$/\1…/' | sed 's/^/    /'
  fi
done
exit 0
