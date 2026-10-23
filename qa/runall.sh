#!/bin/bash
# Runs every Forge regression suite in turn and writes a one-line summary per suite to full_summary.txt.
# Needs: python3 with playwright (and its chromium), node, and `npm i axe-core` run once inside this folder.
cd "$(dirname "$0")"; rm -f full_summary.txt
for t in qa_core qa_layout qa_axe qa_axe2 qa_map qa_map2 qa_13 qa_131 qa_14 qa_15 qa_17 qa_18 qa_181 qa_19 qa_20 qa_21 qa_22 qa_222 qa_223 qa_23 qa_24 qa_241 qa_242 qa_25 qa_251 qa_26 qa_27 qa_271 qa_28 qa_281 qa_29 qa_30 qa_301 qa_31 qa_32 qa_33 qa_34 qa_35 qa_351 qa_fit mo qa_odds qa_time qa_clock qa_mig; do
  timeout 400 python3 $t.py > full_$t.log 2>&1
  echo "$t pass=$(grep -c '^PASS' full_$t.log) fail=$(grep -c '^FAIL' full_$t.log) $(tail -1 full_$t.log | cut -c1-90)" >> full_summary.txt
done
JOURNEY_DAYS=125 JOURNEY_SEED=7 timeout 2400 python3 qa_journey.py > full_qa_journey.log 2>&1; echo "qa_journey pass=$(grep -c "^PASS" full_qa_journey.log) fail=$(grep -c "^FAIL" full_qa_journey.log) $(grep summary full_qa_journey.log)" >> full_summary.txt
for sd in 1 2 3 4 5 6; do timeout 400 python3 monkey.py $sd > full_monkey$sd.log 2>&1; echo "monkey seed $sd: $(grep -c '^PASS' full_monkey$sd.log) pass, $(grep -c '^FAIL' full_monkey$sd.log) fail" >> full_summary.txt; done
echo DONE >> full_summary.txt
