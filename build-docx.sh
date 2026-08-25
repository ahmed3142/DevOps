#!/usr/bin/env bash
# Builds the Word version of the report.
# python-docx lives in the toolchain virtualenv rather than the system python.
set -euo pipefail
VENV_PY="$HOME/.ctf-tools/venv/bin/python3"
PY="$([ -x "$VENV_PY" ] && echo "$VENV_PY" || command -v python3)"
"$PY" -c "import docx" 2>/dev/null || { echo "python-docx not available to $PY" >&2; exit 1; }
python3 assemble.py >/dev/null
"$PY" build_docx.py
