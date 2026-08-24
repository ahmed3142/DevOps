#!/usr/bin/env bash
# Renders the presentation deck to a 16:9 PDF, one slide per page.
set -euo pipefail
export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$HOME/Library/Caches/ms-playwright}"
PW_DIR="$(find "$HOME/.npm/_npx" -maxdepth 3 -type d -name playwright 2>/dev/null | head -1)"
[ -n "$PW_DIR" ] || { echo "playwright not found" >&2; exit 1; }
python3 assemble.py >/dev/null
mkdir -p out
PLAYWRIGHT_PKG="$PW_DIR" node build-slides.mjs
