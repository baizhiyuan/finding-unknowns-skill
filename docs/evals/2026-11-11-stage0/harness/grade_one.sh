#!/usr/bin/env bash
# grade_one.sh PACKET_ID GRADER(opus|astra)
S=/tmp/fu-stage0; P=$S/grade/packets/$1; O=$S/grade/out; mkdir -p $O
PROMPT="$(cat $S/scripts/grader-prompt.txt)"
if [ "$2" = opus ]; then
  mkdir -p $S/grade/homes; H=$S/grade/homes/$1; rm -rf $H; cp -a $S/homes/plain $H; mkdir -p $H/tmp
  timeout 1500 $S/scripts/cbox.sh $H $P ro -- claude -p --model claude-opus-5-5 --effort high --no-session-persistence \
    --allowedTools Read Grep Glob "Bash(cat:*)" "Bash(ls:*)" "Bash(git log:*)" "Bash(git show:*)" "Bash(git diff:*)" "Bash(head:*)" "Bash(sed:*)" "Bash(grep:*)" "Bash(wc:*)" \
    --disallowedTools WebSearch WebFetch Edit Write NotebookEdit --output-format json "$PROMPT" </dev/null > $O/$1.opus.raw 2> $O/$1.opus.err
  python3 -c "import json,sys;d=json.load(open('$O/$1.opus.raw'));open('$O/$1.opus.txt','w').write(d.get('result',''));print(d.get('total_cost_usd',0))" > $O/$1.opus.cost 2>/dev/null
else
  CODEX_HOME=$S/codex-home timeout 1500 codex exec -m gpt-6-astra -s read-only --skip-git-repo-check --ephemeral -C $P -o $O/$1.astra.txt "$PROMPT" </dev/null > $O/$1.astra.events 2> $O/$1.astra.err
fi
echo "graded $1 $2"
