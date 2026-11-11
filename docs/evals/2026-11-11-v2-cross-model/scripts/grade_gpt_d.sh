#!/usr/bin/env bash
R=/tmp/fu-eval2; t=$1; G=$R/gpt-grade-D/$t; ids=$(cat $G/ids.txt); n=$(wc -w <<<"$ids")
P=$(sed -e "s|{N}|$n|" -e "s|{PACKETS}|$(sed 's/ /.md, /g' <<<"$ids").md|" -e "s|{DIR}|$G/packets|" -e "s|{FIXTURE}|$G/fixture|" $R/scripts/grader-prompt.txt)
CODEX_HOME=$R/homes/codex-A timeout 2400 codex exec --skip-git-repo-check --ephemeral -s read-only -C $G --json -o $G/result.json "$P" </dev/null > $G/events.jsonl 2> $G/stderr.txt
echo "graded $t rc=$?"
