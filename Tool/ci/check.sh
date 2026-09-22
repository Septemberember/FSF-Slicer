#!/usr/bin/env sh
set -eu
TOOL_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$TOOL_DIR"
python -m pytest
python -m fsf_tool doctor
python -m build
