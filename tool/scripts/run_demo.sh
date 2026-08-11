#!/usr/bin/env sh
set -eu
ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
python -m fsf_tool analyze \
  --java "$ROOT_DIR/examples/UserInputProgram.java" \
  --fsf "$ROOT_DIR/examples/cube_sum.fsf.yaml" \
  --output "$ROOT_DIR/demo-output"

