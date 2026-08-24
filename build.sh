#!/usr/bin/env bash
# Renders an HTML source file to PDF.
#
# Primary path: Playwright's Chromium (adds a page-number footer).
# Fallback:     the Google Chrome CLI (no footer) if Playwright is unavailable.
#
# Usage: ./build.sh [source.html] [output.pdf] ["footer label"]
set -euo pipefail

SRC="${1:-report.html}"
OUT="${2:-out/DevOps_Delivery_Strategy.pdf}"
LABEL="${3:-DevOps Delivery Strategy — Nimbus (Scenario B)}"

export PLAYWRIGHT_BROWSERS_PATH="${PLAYWRIGHT_BROWSERS_PATH:-$HOME/Library/Caches/ms-playwright}"
PW_DIR="$(find "$HOME/.npm/_npx" -maxdepth 3 -type d -name playwright 2>/dev/null | head -1)"

mkdir -p "$(dirname "$OUT")"

# Regenerate report.html from template.html + parts/ before rendering.
if [ "$SRC" = "report.html" ] && [ -f assemble.py ]; then
  python3 assemble.py
fi

if [ -n "$PW_DIR" ] && PLAYWRIGHT_PKG="$PW_DIR" node build.mjs "$SRC" "$OUT" "$LABEL"; then
  exit 0
fi

echo "Playwright unavailable — falling back to Chrome CLI (no page-number footer)." >&2
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || { echo "Google Chrome not found" >&2; exit 1; }
ABS_SRC="$(cd "$(dirname "$SRC")" && pwd)/$(basename "$SRC")"
"$CHROME" --headless --disable-gpu --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw --virtual-time-budget=10000 \
  --print-to-pdf="$OUT" "file://$ABS_SRC" 2>/dev/null
[ -s "$OUT" ] || { echo "PDF generation produced no output" >&2; exit 1; }
echo "built: $OUT (fallback renderer)"
