#!/usr/bin/env bash
set -euo pipefail

mkdir -p docs/fuzz/appendix/reports/hypothesis
mkdir -p docs/fuzz/appendix/logs

LOG_FILE="docs/fuzz/appendix/logs/hypothesis.log"

python3 -m pytest tests/fuzz/test_hypothesis_auth.py \
  -s \
  --disable-warnings \
  --cov=src \
  --cov-branch \
  --cov-report=term-missing \
  --cov-report=html:docs/fuzz/appendix/reports/hypothesis/html \
  --cov-report=xml:docs/fuzz/appendix/reports/hypothesis/coverage.xml \
  > "$LOG_FILE" 2>&1 || true

echo "[*] Hypothesis fuzzing finished"
echo "[*] Log saved to $LOG_FILE"