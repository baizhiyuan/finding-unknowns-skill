#!/usr/bin/env bash
cd /tmp/fu-eval
printf '%s\n' T1 T2 T3 T4 T5 T6 | xargs -P 3 -I{} bash -c 'scripts/run.sh {} A & scripts/run.sh {} B & wait'
echo ALL-DONE
