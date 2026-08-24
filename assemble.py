#!/usr/bin/env python3
"""Assembles report.html from template.html plus the files in parts/.

Two passes: the parts are inserted, the assessed word count is measured on the
result, and the count is then substituted into the cover page so the declared
figure is always accurate.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PART_FILES = [f"part{n}.html" for n in range(1, 7)]


FIGURE_RE = re.compile(r"<!--\s*FIGURE:([a-z0-9\-]+)\s*-->")


def inline_figures(html: str) -> str:
    """Replaces <!-- FIGURE:name --> markers with figures/name.html."""

    def replace(match: re.Match) -> str:
        path = ROOT / "figures" / f"{match.group(1)}.html"
        if not path.exists():
            raise SystemExit(f"missing figure: {path}")
        return path.read_text(encoding="utf-8")

    return FIGURE_RE.sub(replace, html)


def load(name: str) -> str:
    path = ROOT / "parts" / name
    if not path.exists():
        return ""
    return inline_figures(path.read_text(encoding="utf-8"))


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
