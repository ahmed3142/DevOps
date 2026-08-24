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

# Some institutions also exclude tabulated display material alongside figures;
# pass --exclude-tables to report that convention.
TABLE_TAG = "table"

# Elements that never have a closing tag and so must not affect nesting depth.
VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’\-/€%\.]*")


class Counter(HTMLParser):
    def __init__(self, exclude_tables: bool = False) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_tags = SKIP_TAGS | ({TABLE_TAG} if exclude_tables else set())
        self.stack: list[tuple[str, bool]] = []   # (tag, is_skipped)
        self.section: str | None = None
        self.words: dict[str, int] = {}

    @property
    def skipping(self) -> bool:
        return any(skipped for _, skipped in self.stack)

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        skipped = tag in self.skip_tags or "no-count" in classes
        if not self.skipping and tag == "section" and "part" in classes:
            self.section = attrs.get("data-part", "unnamed")
            self.words.setdefault(self.section, 0)
        self.stack.append((tag, skipped))

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        # Unwind to the matching open tag, tolerating unclosed elements.
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        if self.skipping or self.section is None:
            return
        self.words[self.section] = self.words.get(self.section, 0) + len(WORD_RE.findall(data))


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    exclude_tables = "--exclude-tables" in sys.argv
    path = args[0] if args else "report.html"
    parser = Counter(exclude_tables=exclude_tables)
    with open(path, encoding="utf-8") as fh:
        parser.feed(fh.read())

    total = sum(parser.words.values())
    print(f"{'Section':<50}{'Words':>7}{'Target':>8}")
    print("-" * 65)
    targets = {"1": 600, "2": 400, "3": 700, "4": 750, "5": 800, "6": 750}
    for name, count in parser.words.items():
        key = next((k for k in targets if name.startswith(f"Part {k}")), None)
        target = f"{targets[key]}" if key else "—"
        print(f"{name:<50}{count:>7}{target:>8}")
    print("-" * 65)
    label = "TOTAL (excl. diagrams, code, tables, appendices)" if exclude_tables \
        else "TOTAL (excl. diagrams, code, appendices)"
    print(f"{label:<50}{total:>7}{4000:>8}")

    low, high = 3900, 4100
    if total < low:
        print(f"\n⚠  {low - total} words under the 4000 target band ({low}-{high}).")
    elif total > high:
        print(f"\n⚠  {total - high} words over the 4000 target band ({low}-{high}).")
    else:
        print(f"\n✓  Within the {low}-{high} target band.")

    # Machine-readable line consumed by assemble.py.
    print(f"TOTAL_WORDS={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
