#!/usr/bin/env bash
# Renders the speaker notes and defence questions to PDF.
set -euo pipefail
python3 build_notes.py
./build.sh notes.html out/DevOps_Presentation_Notes.pdf "Presentation Notes — Nimbus (Scenario B)"
