#!/usr/bin/env bash
# Tier 1 graded runs: 4 arms x 5 scenarios x 2 runs = 40 runs. NOT executed when written (2026-11-12).
# Order: scenario-major (T2, T1, T3, P, C6); within a scenario run 1 then run 2; the arm order rotates by one
# position per (scenario, run) block, so no arm is always first. Up to 4 runs in parallel (one block at a time
# in practice). A job whose run dir already has meta.json is skipped (resume). Before each job, and inside
# run_task.py before every subject turn, the cumulative subject cost from cost-ledger.jsonl is checked against
# FU_COST_CAP (default 30 USD); over it, jobs are skipped and running ones end with "budget_abort".
# Required: FU_PLUGIN_COMMIT (the plugin must have been cut at that commit with scripts/cut_plugin.sh).
# Afterwards: python3 scripts/aggregate_tier1.py
set -euo pipefail
R=${FU_ROOT:-/tmp/fu-tier1}
export FU_ROOT=$R FU_COST_CAP=${FU_COST_CAP:-30}
: "${FU_PLUGIN_COMMIT:?set FU_PLUGIN_COMMIT (and run scripts/cut_plugin.sh) first}"
export FU_PLUGIN_COMMIT
cd "$R"
python3 -c "import sys; sys.path.insert(0, 'scripts'); import run_task as rt; print('plugin ok:', rt.plugin_commit())"

python3 - > jobs.txt <<'EOF'
ARMS = ["w56", "w82", "placebo", "plugin"]
TASKS = ["T2", "T1", "T3", "P", "C6"]
k = 0
for t in TASKS:
    for run in (1, 2):
        rot = k % len(ARMS)
        k += 1
        for a in ARMS[rot:] + ARMS[:rot]:
            print(a, t, run)
EOF

spent() {
  python3 -c "
import json, pathlib
p = pathlib.Path('$R/cost-ledger.jsonl')
print(round(sum(json.loads(l).get('cost', 0) or 0 for l in p.read_text().splitlines() if l.strip()) if p.is_file() else 0.0, 4))"
}
run_one() {
  local arm=$1 task=$2 run=$3 id="$2-$1-$3" s
  if [ -f "$R/runs/$id/meta.json" ]; then echo "SKIP exists $id" >> "$R/runs.log"; return 0; fi
  s=$(spent)
  if python3 -c "import sys; sys.exit(0 if $s > $FU_COST_CAP else 1)"; then
    echo "SKIP budget $id (spent \$$s > \$$FU_COST_CAP)" >> "$R/runs.log"; return 0
  fi
  echo "START $(date '+%F %T') $id (spent \$$s)" >> "$R/runs.log"
  python3 "$R/scripts/run_task.py" "$arm" "$task" "$run" >> "$R/runs.log" 2>&1 || echo "FAIL $id" >> "$R/runs.log"
}
export R
export -f spent run_one
echo "BEGIN $(date '+%F %T') plugin=$FU_PLUGIN_COMMIT cap=\$$FU_COST_CAP" >> runs.log
xargs -P 4 -L 1 bash -c 'run_one "$0" "$1" "$2"' < jobs.txt
echo "ALL-DONE $(date '+%F %T') spent=\$$(spent)" >> runs.log
