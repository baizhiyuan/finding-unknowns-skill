#!/usr/bin/env bash
# usage: run.sh TASK ARM   (fixture name and prompt read from tasks.tsv)
set -u
T=$1; ARM=$2
ROOT=/tmp/fu-eval
line=$(awk -F'\t' -v t="$T" '$1==t' $ROOT/scripts/tasks.tsv)
FIX=$(cut -f2 <<<"$line"); SB=$(cut -f3 <<<"$line"); PROMPT=$(cut -f4- <<<"$line")
D=$ROOT/runs/$T-$ARM; rm -rf "$D"; mkdir -p "$D"
cp -r $ROOT/fixtures/$FIX "$D/$FIX"
start=$(date +%s)
CODEX_HOME=$ROOT/homes/base-$ARM timeout 1800 codex exec --skip-git-repo-check --ephemeral \
  -s "$SB" -C "$D/$FIX" --json -o "$D/final.md" "$PROMPT" </dev/null >"$D/events.jsonl" 2>"$D/stderr.txt"
rc=$?
echo "{\"task\":\"$T\",\"arm\":\"$ARM\",\"rc\":$rc,\"seconds\":$(( $(date +%s) - start ))}" > "$D/meta.json"
(cd "$D/$FIX" && git status --porcelain > "$D/changes.txt"; git diff > "$D/diff.txt")
echo "done $T-$ARM rc=$rc"
