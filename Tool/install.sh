#!/usr/bin/env sh
set -eu
TOOL_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 -m venv "$TOOL_DIR/.venv"
"$TOOL_DIR/.venv/bin/python" -m pip install -r "$TOOL_DIR/requirements-lock.txt"
"$TOOL_DIR/.venv/bin/python" -m pip install --no-deps "$TOOL_DIR"
echo "Installed. Run: $TOOL_DIR/.venv/bin/fsf-tbfv doctor"
