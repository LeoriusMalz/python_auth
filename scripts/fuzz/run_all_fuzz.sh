#!/usr/bin/env bash
set -euo pipefail

mkdir -p docs/fuzz/appendix/{crashes,logs,reports}

echo "[*] Running Hypothesis..."
bash scripts/fuzz/run_hypothesis.sh | tee docs/fuzz/appendix/logs/hypothesis.log || true


echo "[*] Running HypoFuzz..."

(
  export PYTHONPATH="$(pwd)"

  pytest -q \
    --disable-warnings \
    --maxfail=1 \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html:docs/fuzz/appendix/reports/hypofuzz/html \
    --cov-report=xml:docs/fuzz/appendix/reports/hypofuzz/coverage.xml \
    tests/fuzz/test_hypofuzz_auth.py
) 2>&1 | tee docs/fuzz/appendix/logs/hypofuzz.log || true

echo "[*] HypoFuzz finished"


if command -v radamsa >/dev/null 2>&1; then
  echo "[*] Running Radamsa..."
  bash scripts/fuzz/run_radamsa.sh | tee docs/fuzz/appendix/logs/radamsa.log || true
else
  echo "[!] Radamsa is not installed. Skipping." | tee docs/fuzz/appendix/logs/radamsa.log
fi

echo "[*] All fuzzing tasks finished"