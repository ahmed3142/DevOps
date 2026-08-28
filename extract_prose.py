#!/usr/bin/env python3
"""Writes the report's prose to a plain-text file for reading and proofing.

Tables, figures, captions and code are left out, so what remains is exactly the
written argument.
"""
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).parent
SKIP = {"table", "figure", "svg", "pre", "caption"}  # inline <code> is part of the sentence
VOID = {"br", "img", "meta", "link", "hr", "input"}


class Prose(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.skip, self.buf, self.out = [], 0, [], []
        self.kind = None

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        cls = dict(attrs).get("class", "")
        if self.skip or tag in SKIP:
            self.skip += 1
            self.stack.append(tag)
            return
        self.stack.append(tag)
        if tag in ("h2", "h3", "p", "li"):
            self.kind = "note" if "title" in cls else tag
            self.buf = []

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.skip:
            self.skip -= 1
            if self.stack:
                self.stack.pop()
            return
        if self.stack:
            self.stack.pop()
        if tag in ("h2", "h3", "p", "li"):
            text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
            if text:
                self.out.append((tag, text))
            self.buf = []

    def handle_data(self, data):
        if not self.skip:
            self.buf.append(data)


def main() -> int:
    lines, total = [], 0
    for n in range(1, 7):
        parser = Prose()
        parser.feed((ROOT / "parts" / f"part{n}.html").read_text(encoding="utf-8"))
        for tag, text in parser.out:
            words = len(re.findall(r"[A-Za-z0-9][\w'’\-/€%\.]*", text))
            if tag == "h2":
                lines += ["", "=" * 78, text.upper(), "=" * 78, ""]
            elif tag == "h3":
                lines += ["", text, "-" * len(text)]
            elif tag == "li":
                lines += [f"  • {text}", ""]
                total += words
            else:
                lines += [text, ""]
                total += words

    out = ROOT / "out" / "report_prose.txt"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"written: out/report_prose.txt  ({total} words of prose, excluding tables and figures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
