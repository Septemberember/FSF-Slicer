#!/usr/bin/env sh
set -eu
TOOL_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TOOL_PYTHON="$TOOL_DIR/.venv/bin/python"
if [ ! -x "$TOOL_PYTHON" ]; then TOOL_PYTHON=python3; fi
"$TOOL_PYTHON" -m fsf_tool analyze \
  --java "$TOOL_DIR/examples/Calculator.java" \
  --fsf "$TOOL_DIR/examples/calculator_full.fsf.yaml" \
  --output "$TOOL_DIR/demo-output"
