#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH="$(pwd)"

mkdir -p docs/fuzz/appendix/crashes/radamsa
mkdir -p docs/fuzz/appendix/logs

SEED_DIR="tests/fuzz/seeds"
HARNESS="tests/fuzz/test_radamsa_auth.py"
LOG_FILE="docs/fuzz/appendix/logs/radamsa.log"

for i in $(seq 1 1000); do
  seed=$(find "$SEED_DIR" -type f | python3 -c "import sys,random; print(random.choice([l.strip() for l in sys.stdin if l.strip()]))")
  mutated="/tmp/radamsa_input_$i.txt"

  radamsa "$seed" > "$mutated"

  if ! python3 "$HARNESS" "$mutated" > /tmp/radamsa_out.txt 2> /tmp/radamsa_err.txt; then
    cp "$mutated" "docs/fuzz/appendix/crashes/radamsa/crash_$i.txt"
    cp /tmp/radamsa_err.txt "docs/fuzz/appendix/logs/radamsa_crash_$i.log"
    echo "[!] Crash found: crash_$i.txt"
  fi
done

echo "[*] Radamsa fuzzing finished"
echo "[*] Log saved to $LOG_FILE"