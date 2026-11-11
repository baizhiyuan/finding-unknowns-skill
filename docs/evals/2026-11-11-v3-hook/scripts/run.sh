#!/usr/bin/env bash
# run.sh TASK ARM(A|C|E|R) RUN
set -u
T=$1; ARM=$2; N=$3; R=/tmp/fu-eval3
line=$(awk -F'\t' -v t="$T" '$1==t' $R/scripts/tasks.tsv)
FIX=$(cut -f2 <<<"$line"); MODE=$(cut -f3 <<<"$line"); PROMPT=$(cut -f4- <<<"$line")
D=$R/runs/$T-$ARM-$N; rm -rf "$D"; mkdir -p "$D"; cp -a $R/fixtures/$FIX "$D/$FIX"; W="$D/$FIX"
H="$D/home"; cp -a $R/homes/$ARM "$H"
DIS="WebSearch WebFetch"; [ "$MODE" = ro ] && DIS="$DIS Edit Write NotebookEdit"
BOX=rw; [ "$MODE" = ro ] && BOX=ro
PLUG=(); RO=""
[ "$ARM" = C ] && { PLUG=(--plugin-dir $R/plugin-C); RO=$R/plugin-C; }
[ "$ARM" = E ] && { PLUG=(--plugin-dir $R/plugin-E); RO=$R/plugin-E; }
start=$(date +%s)
CBOX_RO="$RO" timeout 2400 $R/scripts/cbox.sh "$H" "$W" $BOX -- claude -p --model claude-sonnet-5-5 --effort high \
  --permission-mode bypassPermissions --disallowedTools $DIS --no-session-persistence "${PLUG[@]}" \
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
echo "{\"task\":\"$T\",\"arm\":\"$ARM\",\"run\":$N,\"rc\":$rc,\"seconds\":$(( $(date +%s) - start ))}" > "$D/meta.json"
(cd "$W" && git status --porcelain > "$D/changes.txt"; git diff > "$D/diff.txt")
echo "done $T-$ARM-$N rc=$rc"
