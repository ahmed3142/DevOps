#!/usr/bin/env python3
"""Counts the assessed word total in the report.

The brief specifies 4000 words *excluding diagrams, code and appendices*, so
anything carrying class="no-count" (cover page, contents, appendix, references)
plus every <figure>, <pre>, <code> and <svg> element is stripped before counting.
Run: python3 wordcount.py [report.html]
"""
import re
import sys
from html.parser import HTMLParser

SKIP_TAGS = {"figure", "pre", "code", "svg", "script", "style", "head"}


class Counter(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0          # nesting depth inside a skipped element
        self.stack: list[str] = []
        self.section = None     # current part heading, for the breakdown
        self.words: dict[str, int] = {}
        self._pending_heading = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if self.depth or tag in SKIP_TAGS or "no-count" in classes:
            self.depth += 1
            self.stack.append(tag)
            return
        if tag == "section" and "part" in classes:
            self.section = attrs.get("data-part", "unnamed")
            self.words.setdefault(self.section, 0)
        if tag == "h2":
            self._pending_heading = True
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()
        if self.depth:
            self.depth -= 1
        if tag == "h2":
            self._pending_heading = False

    def handle_data(self, data):
        if self.depth or self.section is None:
            return
        n = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-/€%\.]*", data))
        self.words[self.section] = self.words.get(self.section, 0) + n


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else "report.html"
    with open(path, encoding="utf-8") as fh:
        parser = Counter()
        parser.feed(fh.read())

    total = sum(parser.words.values())
    print(f"{'Section':<52}{'Words':>7}")
    print("-" * 59)
    for name, count in parser.words.items():
        print(f"{name:<52}{count:>7}")
    print("-" * 59)
    print(f"{'TOTAL (excl. diagrams, code, appendices)':<52}{total:>7}")

    low, high = 3900, 4100
    if total < low:
        print(f"\n⚠  {low - total} words under the 4000 target band ({low}-{high}).")
    elif total > high:
        print(f"\n⚠  {total - high} words over the 4000 target band ({low}-{high}).")
    else:
        print(f"\n✓  Within the {low}-{high} target band.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
