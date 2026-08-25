#!/usr/bin/env bash
# Builds the reusable blank Assignment Cover Sheet in both formats.
set -euo pipefail
VENV_PY="$HOME/.ctf-tools/venv/bin/python3"
PY="$([ -x "$VENV_PY" ] && echo "$VENV_PY" || command -v python3)"
./build.sh blank-cover.html out/Assignment_Cover_Sheet_BLANK.pdf
"$PY" build_blank_cover.py
