#!/usr/bin/env bash
# run.sh MODEL(gpt|sonnet) TASK ARM(A|B|C) RUN(1|2)
set -u
M=$1; T=$2; ARM=$3; N=$4; R=/tmp/fu-eval2
line=$(awk -F'\t' -v t="$T" '$1==t' $R/scripts/tasks.tsv)
FIX=$(cut -f2 <<<"$line"); MODE=$(cut -f3 <<<"$line"); PROMPT=$(cut -f4- <<<"$line")
D=$R/runs/$M-$T-$ARM-$N; rm -rf "$D"; mkdir -p "$D"
cp -a $R/fixtures/$FIX "$D/$FIX"; W="$D/$FIX"
start=$(date +%s)
if [ "$M" = gpt ]; then
  SB=read-only; [ "$MODE" = rw ] && SB=workspace-write
  CODEX_HOME=$R/homes/codex-$ARM timeout 2400 codex exec --skip-git-repo-check --ephemeral \
    -s $SB -C "$W" --json -o "$D/final.md" "$PROMPT" </dev/null >"$D/events.jsonl" 2>"$D/stderr.txt"
  rc=$?
else
  H="$D/home"; cp -a $R/homes/claude-$ARM "$H"; mkdir -p "$H/tmp"
  DIS="WebSearch WebFetch"; [ "$MODE" = ro ] && DIS="$DIS Edit Write NotebookEdit"
  BOXMODE=rw; [ "$MODE" = ro ] && BOXMODE=ro
  timeout 2400 $R/scripts/cbox.sh "$H" "$W" $BOXMODE -- claude -p --model claude-sonnet-5-5 --effort high \
    --permission-mode bypassPermissions --disallowedTools $DIS --no-session-persistence \
    --output-format stream-json --verbose "$PROMPT" </dev/null >"$D/events.jsonl" 2>"$D/stderr.txt"
  rc=$?
  python3 - "$D" <<'PY'
import json, sys, pathlib
d = pathlib.Path(sys.argv[1]); res = ""
for ln in open(d / "events.jsonl", encoding="utf-8"):
    try: e = json.loads(ln)
    except ValueError: continue
    if e.get("type") == "result": res = e.get("result", "") or ""
(d / "final.md").write_text(res, encoding="utf-8")
PY
fi
echo "{\"model\":\"$M\",\"task\":\"$T\",\"arm\":\"$ARM\",\"run\":$N,\"rc\":$rc,\"seconds\":$(( $(date +%s) - start ))}" > "$D/meta.json"
(cd "$W" && git status --porcelain > "$D/changes.txt"; git diff --stat > "$D/diffstat.txt"; git diff > "$D/diff.txt")
echo "done $M-$T-$ARM-$N rc=$rc"
