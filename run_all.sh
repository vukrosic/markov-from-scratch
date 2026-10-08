#!/bin/bash
# Runs the seven steps, then the checks. About 40 seconds on a laptop; nothing to install.
set -e
cd "$(dirname "$0")"
for step in step1_coin step2_weather step3_settle step4_count step5_break step6_rank step7_write; do
  echo
  echo "=== $step.py"
  python3 $step.py
done
echo
python3 tests.py
