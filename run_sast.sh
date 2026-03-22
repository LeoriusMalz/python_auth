#!/bin/bash

set -e

PROJECT_DIR="./src"
REPORT_DIR="reports"

echo "=== Creating reports directory ==="
mkdir -p $REPORT_DIR

echo "=== Running \"Bandit\" ==="
bandit -r $PROJECT_DIR -f txt -o $REPORT_DIR/bandit_report.txt || true

echo "=== Running \"Flake8\" ==="
flake8 $PROJECT_DIR > $REPORT_DIR/flake8_report.txt || true

echo "=== Running \"Radon\" (complexity) ==="
radon cc $PROJECT_DIR -s -a > $REPORT_DIR/radon_complexity.txt || true

echo "=== Running \"Radon\" (maintainability index) ==="
radon mi $PROJECT_DIR > $REPORT_DIR/radon_mi.txt || true

echo "=== SAST analysis completed! ==="
echo "Reports saved in: $REPORT_DIR"
