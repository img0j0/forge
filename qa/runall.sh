#!/bin/bash
# Run from any directory; failures, crashes, empty runs and timeouts fail the gate.
set -u
cd "$(dirname "$0")" || exit 1
: > full_summary.txt
failed=0
run_suite() {
  local name="$1" limit="$2" rc passes failures
  shift 2
  timeout "$limit" "$@" > "full_${name}.log" 2>&1
  rc=$?
  passes=$(grep -c '^PASS' "full_${name}.log" || true)
  failures=$(grep -c '^FAIL' "full_${name}.log" || true)
  echo "$name exit=$rc pass=$passes fail=$failures" >> full_summary.txt
  if [ "$rc" -ne 0 ] || [ "$failures" -ne 0 ] || [ "$passes" -eq 0 ]; then failed=1; fi
}
# Optional suite names allow focused checks with the same failure handling.
if [ "$#" -gt 0 ]; then
  for t in "$@"; do run_suite "$t" 400 python3 "$t.py"; done
else
  for t in qa_core qa_layout qa_axe qa_axe2 qa_map qa_map2 qa_13 qa_131 qa_14 qa_15 qa_17 qa_18 qa_181 qa_19 qa_20 qa_21 qa_22 qa_222 qa_223 qa_23 qa_24 qa_241 qa_242 qa_25 qa_251 qa_26 qa_27 qa_271 qa_28 qa_281 qa_29 qa_30 qa_301 qa_31 qa_32 qa_33 qa_34 qa_35 qa_351 qa_36 qa_37 qa_38 qa_383 qa_384 qa_385 qa_386 qa_fit mo qa_odds qa_time qa_clock qa_mig; do run_suite "$t" 400 python3 "$t.py"; done
  run_suite qa_journey 2400 env JOURNEY_DAYS=125 JOURNEY_SEED=7 python3 qa_journey.py
  for sd in 1 2 3 4 5 6; do run_suite "monkey$sd" 400 python3 monkey.py "$sd"; done
fi
if [ "$failed" -eq 0 ]; then echo 'PASS ALL' >> full_summary.txt; else echo 'FAILED: inspect suite logs' >> full_summary.txt; fi
cat full_summary.txt
exit "$failed"
