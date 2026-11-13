#!/usr/bin/env bash
# Install finding-unknowns 6.0 into the Claude Code config directory:
#   - the skill (skills/finding-unknowns/SKILL.md) and the commands /fu-interview, /fu-lookback;
#   - the always-on text (CLAUDE.md), appended to the user-level CLAUDE.md inside marker comments
#     (skip with --no-claude-md);
#   - retires the 4.x pieces that 6.0 removed, but only files that carry this project's marker.
#
# Safety rules:
#   - A same-name file that is not ours is copied to <file>.<timestamp>.bak before it is replaced.
#   - Retired files are moved, never deleted, into finding-unknowns-backup-<timestamp>/ in the
#     config directory. A file without our marker is left where it is.
#   - CLAUDE.md is copied to CLAUDE.md.<timestamp>.bak before any change; text outside our
#     marker comments is never edited. A stray or duplicate marker stops the script unchanged.
#   - An existing backup is never overwritten; a second run in the same second adds -1, -2.
set -euo pipefail

CONFIG_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$CONFIG_DIR/finding-unknowns-backup-$STAMP"
BEGIN='<!-- finding-unknowns:always-on -->'
END='<!-- /finding-unknowns:always-on -->'
WITH_CLAUDE_MD=1

# unused PREFIX SUFFIX  -> PREFIX SUFFIX, or PREFIX-1 SUFFIX, ... whichever does not exist yet
unused() {
  local name="$1$2" i=1
  while [ -e "$name" ]; do name="$1-$i$2"; i=$((i + 1)); done
  printf '%s' "$name"
}
BACKUP="$(unused "$BACKUP" "")"

for arg in "$@"; do
  case "$arg" in
    --no-claude-md) WITH_CLAUDE_MD=0 ;;
    -h|--help) awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) echo "Unknown option: $arg (try --help)" >&2; exit 2 ;;
  esac
done

# has_all FILE PATTERN...  -> true when FILE exists and matches every extended regex
has_all() {
  local file="$1"; shift
  [ -f "$file" ] || return 1
  for pattern in "$@"; do grep -qE -- "$pattern" "$file" || return 1; done
}

# install_file SRC DEST MARKER  -> copy SRC to DEST; back up a same-name file that is not ours
install_file() {
  local src="$1" dest="$2" marker="$3"
  mkdir -p "$(dirname "$dest")"
  if [ -f "$dest" ] && cmp -s "$src" "$dest"; then
    echo "Unchanged        $dest"; return
  fi
  if [ -e "$dest" ] && ! has_all "$dest" "$marker"; then
    local bak; bak="$(unused "$dest.$STAMP" .bak)"
    cp -p "$dest" "$bak"
    echo "Backed up        $dest -> $bak (not ours)"
  fi
  cp "$src" "$dest"
  echo "Installed        $dest"
}

# retire PATH CHECK_FILE PATTERN...  -> move PATH into the backup directory if CHECK_FILE is ours
retire() {
  local path="$1" check="$2"; shift 2
  [ -e "$path" ] || return 0
  if has_all "$check" "$@"; then
    local rel="${path#"$CONFIG_DIR"/}"
    mkdir -p "$BACKUP/$(dirname "$rel")"
    mv "$path" "$BACKUP/$rel"
    echo "Retired (4.x)    $path -> $BACKUP/$rel"
  else
    echo "Left alone       $path (no finding-unknowns marker)"
  fi
}

# 1. Install the 6.0 files.
install_file "$SRC/skills/finding-unknowns/SKILL.md" "$CONFIG_DIR/skills/finding-unknowns/SKILL.md" '^name: finding-unknowns$'
for cmd in fu-interview fu-lookback; do
  install_file "$SRC/commands/$cmd.md" "$CONFIG_DIR/commands/$cmd.md" 'finding-unknowns'
done

# 2. Retire the 4.x pieces that 6.0 removed (they remain on branch v4).
FU="$CONFIG_DIR/skills/finding-unknowns"
retire "$FU/references/cartographer.md" "$FU/references/cartographer.md" 'ledger' 'Workflow'
retire "$FU/references/workflows.md" "$FU/references/workflows.md" 'ledger' 'Workflow'
rmdir "$FU/references" 2>/dev/null || true
retire "$CONFIG_DIR/skills/keep-the-reasoning" "$CONFIG_DIR/skills/keep-the-reasoning/SKILL.md" \
  '^name: keep-the-reasoning$' 'finding-unknowns'
for agent in blindspot-scout ledger-keeper prototype-smith quiz-master; do
  retire "$CONFIG_DIR/agents/$agent.md" "$CONFIG_DIR/agents/$agent.md" "^name: $agent\$" 'finding-unknowns'
done
for cmd in blindspot cartographer change-quiz; do
  retire "$CONFIG_DIR/commands/$cmd.md" "$CONFIG_DIR/commands/$cmd.md" '^description:' 'finding-unknowns'
done
for cmd in finding-unknowns keep-the-reasoning theory-vs-result; do   # pass-throughs before 4.3.0
  retire "$CONFIG_DIR/commands/$cmd.md" "$CONFIG_DIR/commands/$cmd.md" '^description:' 'Skill tool|SKILL\.md'
done

# 3. The always-on text, inside marker comments in the user-level CLAUDE.md.
if [ "$WITH_CLAUDE_MD" = 1 ]; then
  TARGET="$CONFIG_DIR/CLAUDE.md"
  STAMP="$STAMP" BEGIN="$BEGIN" END="$END" python3 - "$TARGET" "$SRC/CLAUDE.md" <<'PY'
import os, shutil, sys
target, source = sys.argv[1], sys.argv[2]
begin, end, stamp = os.environ["BEGIN"], os.environ["END"], os.environ["STAMP"]
text = None
if os.path.exists(target):
    with open(target, encoding="utf-8", newline="") as f:   # newline="": keep CRLF as it is
        text = f.read()
nl = "\r\n" if text and "\r\n" in text else "\n"
with open(source, encoding="utf-8") as f:
    block = nl.join([begin, f.read().strip(), end])
if text is not None:
    lines = text.splitlines()
    b = [i + 1 for i, s in enumerate(lines) if begin in s]
    e = [i + 1 for i, s in enumerate(lines) if end in s]
    if len(b) > 1 or len(e) > 1 or len(b) != len(e) or (b and e[0] < b[0]):
        print(f"Error: {target} has a stray or duplicate always-on marker (begin on lines {b or 'none'}, "
              f"end on lines {e or 'none'}). Leave exactly one begin/end pair or none, then rerun. "
              "CLAUDE.md was not changed.", file=sys.stderr)
        sys.exit(1)
    if b and block in text:
        print(f"Unchanged        {target} (always-on block)")
        sys.exit(0)
    bak, i = f"{target}.{stamp}.bak", 1
    while os.path.exists(bak):
        bak, i = f"{target}.{stamp}-{i}.bak", i + 1
    shutil.copy2(target, bak)
    print(f"Backed up        {target} -> {bak}")
if text is not None and begin in text:
    # Replace our block in place; text outside the markers is kept byte for byte.
    head, rest = text.split(begin, 1)
    new, action = head + block + rest.split(end, 1)[1], "Updated          {} (always-on block replaced)"
else:
    sep = "" if not text else (nl if text.endswith("\n") else nl * 2)
    new, action = (text or "") + sep + block + nl, "Appended         {} (always-on block)"
with open(target, "w", encoding="utf-8", newline="") as f:
    f.write(new)
print(action.format(target))
PY
  # Look only outside our markers: a hand-pasted copy of the current text counts too.
  if sed "\#$BEGIN#,\#$END#d" "$TARGET" | grep -qE 'ask me (once )?to predict|\.finding-unknowns/|# finding-unknowns \(passive drop-in\)|show me the unknowns|Before non-trivial work, show `fu:before`|Before non-trivial changes \(reading is fine\)'; then
    echo "Note: $TARGET still holds an older finding-unknowns text or a hand-pasted copy of this one (outside the markers)."
    echo "      Remove it by hand; both texts would apply."
  fi
fi

echo
[ -d "$BACKUP" ] && echo "Retired 4.x files are in $BACKUP (delete it when you no longer need them)."
if [ -e "$CONFIG_DIR/skills/theory-vs-result/SKILL.md" ] || [ -e "$CONFIG_DIR/agents/mechanism-auditor.md" ]; then
  echo "Kept: theory-vs-result and mechanism-auditor (4.x). 6.0 does not use them; they still work"
  echo "on their own. Remove them by hand if you no longer want them; they remain on branch v4."
fi
echo "Done. finding-unknowns 6.0: the always-on text, /fu-interview and /fu-lookback."
