#!/usr/bin/env bash
cd /tmp/fu-eval2
for N in 1 2; do for T in H1 H2 H3 H4 H5 C6; do for M in gpt sonnet; do for A in A B; do echo "$M $T $A $N"; done; done; done; done \
 | xargs -P 4 -L 1 bash -c 'scripts/run.sh $0 $1 $2 $3'
echo ALL-DONE
