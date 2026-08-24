#!/usr/bin/env python3
"""Assembles report.html from template.html plus the files in parts/.

Two passes: the parts are inserted, the assessed word count is measured on the
result, and the count is then substituted into the cover page so the declared
figure is always accurate.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PART_FILES = [f"part{n}.html" for n in range(1, 7)]


def load(name: str) -> str:
    path = ROOT / "parts" / name
    return path.read_text(encoding="utf-8") if path.exists() else ""


def main() -> int:
    template = (ROOT / "template.html").read_text(encoding="utf-8")

    parts = "\n".join(load(name) for name in PART_FILES if load(name))
    appendix = load("appendix.html")

    html = template.replace("<!-- PARTS_PLACEHOLDER -->", parts)
    html = html.replace("<!-- APPENDIX_PLACEHOLDER -->", appendix)

    out = ROOT / "report.html"
    out.write_text(html, encoding="utf-8")

    # Second pass: measure and stamp the real word count onto the cover.
    result = subprocess.run(
        [sys.executable, str(ROOT / "wordcount.py"), str(out)],
        capture_output=True, text=True, check=True,
    )
    total = "0"
    for line in result.stdout.splitlines():
        if line.startswith("TOTAL_WORDS="):
            total = line.split("=", 1)[1]
    out.write_text(html.replace("WORDCOUNT_PLACEHOLDER", f"{int(total):,}"), encoding="utf-8")

    print("\n".join(l for l in result.stdout.splitlines() if not l.startswith("TOTAL_WORDS=")))
    print(f"assembled: report.html ({total} assessed words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
