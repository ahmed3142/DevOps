#!/usr/bin/env python3
"""Renders PRESENTATION_NOTES.md to HTML for printing.

The notes use a deliberately small slice of Markdown — headings, horizontal
rules, bold, italic and inline code — so a full parser is not warranted.
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "PRESENTATION_NOTES.md"
OUT = ROOT / "notes.html"

# Matches a paragraph that opens with a bold lead-in, e.g. "**3 · Value stream.** …"
LEAD_RE = re.compile(r"^\*\*(.+?)\*\*\s*(.*)$", re.S)
QUESTION_RE = re.compile(r"^\*\*(\d+)\.\s*(.+?)\*\*$", re.S)


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def blocks(md: str):
    for raw in re.split(r"\n\s*\n", md.strip()):
        block = raw.strip()
        if block:
            yield block


def convert(md: str) -> str:
    out, pending_q, first_h2 = [], None, True

    for block in blocks(md):
        if block.startswith("# "):
            out.append(f"<h1>{inline(block[2:])}</h1>")
            continue
        if block.startswith("## "):
            cls = ' class="first"' if first_h2 else ""
            first_h2 = False
            out.append(f"<h2{cls}>{inline(block[3:])}</h2>")
            continue
        if set(block) <= {"-"} and len(block) >= 3:
            continue  # horizontal rules are handled by the section borders

        q = QUESTION_RE.match(block)
        if q:
            pending_q = f"{q.group(1)}. {inline(q.group(2))}"
            continue

        if pending_q is not None:
            out.append(
                f'<div class="qa"><p class="q">{pending_q}</p>'
                f'<p class="a">{inline(block)}</p></div>'
            )
            pending_q = None
            continue

        lead = LEAD_RE.match(block)
        if lead and lead.group(2).strip():
            out.append(
                f'<div class="slidenote"><p><span class="lead">{inline(lead.group(1))}</span> '
                f"{inline(lead.group(2))}</p></div>"
            )
            continue

        out.append(f"<p>{inline(block)}</p>")

    return "\n".join(out)


def main() -> int:
    body = convert(SRC.read_text(encoding="utf-8"))
    # The opening title and standfirst get their own block.
    body = body.replace(
        "<h1>Presentation notes &amp; defence preparation</h1>",
        '<div class="titleblock"><h1>Presentation Notes and Defence Preparation</h1>'
        '<p class="subtitle">A DevOps Delivery Strategy for Nimbus Ltd. · Scenario B · Imran Hossain Chowdhury</p></div>',
        1,
    )
    OUT.write_text(
        "<!doctype html>\n<html lang=\"en-GB\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<title>Presentation Notes — Nimbus</title>\n"
        "<link rel=\"stylesheet\" href=\"notes.css\">\n</head>\n<body>\n"
        f"{body}\n</body>\n</html>\n",
        encoding="utf-8",
    )
    print(f"built: {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
