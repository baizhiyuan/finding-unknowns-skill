#!/usr/bin/env bash
# grade.sh GRADER(claude|gpt) TASK
R=/tmp/fu-eval3; g=$1; t=$2; G=$R/grade-$g/$t
fix=$(awk -F'\t' -v t=$t '$1==t{print $2}' $R/scripts/tasks.tsv)
rm -rf $G/fixture; cp -a $R/fixtures/$fix $G/fixture; rm -rf $G/fixture/.git
ids=$(ls $G/packets | sed 's/\.md$//' | tr '\n' ' '); n=$(wc -w <<<"$ids")
P=$(sed -e "s|{N}|$n|" -e "s|{PACKETS}|$(sed 's/ *$//; s/ /.md, /g' <<<"$ids").md|" -e "s|{DIR}|$G/packets|" -e "s|{FIXTURE}|$G/fixture|" /tmp/fu-eval2/scripts/grader-prompt.txt)
if [ $g = gpt ]; then
  CODEX_HOME=/tmp/fu-eval2/homes/codex-A timeout 2400 codex exec --skip-git-repo-check --ephemeral -s read-only -C $G --json -o $G/result.json "$P" </dev/null > $G/events.jsonl 2> $G/stderr.txt
else
  H=$R/grade-homes/$g-$t; rm -rf $H; mkdir -p $R/grade-homes; cp -a $R/homes/A $H
  timeout 2400 $R/scripts/cbox.sh $H $G ro -- claude -p --model claude-opus-5-5 --effort high --permission-mode bypassPermissions \
    --disallowedTools WebSearch WebFetch Edit Write NotebookEdit --no-session-persistence --output-format json "$P" </dev/null > $G/out.json 2> $G/stderr.txt
  python3 -c "import json;print(json.load(open('$G/out.json'))['result'])" > $G/result.json
fi
echo "graded $g $t rc=$?"
