#!/usr/bin/env python3
"""Fail when a link in `content/` points at a page that is not there.

Written for the 2026-09 restructure, where 252 of 272 wikilinks carry an
explicit path and every one of them had to survive a move. It is worth keeping
afterwards: a broken wikilink renders as plain text in Quartz, so nothing about
the built site says it happened.

    python scripts/check_links.py            # report and exit non-zero
    python scripts/check_links.py --quiet    # only the summary

Three details that a first attempt gets wrong, each of them once produced a
false report here:

* `\\|` inside a table cell still separates target from label. The pipe has to
  be escaped there or it ends the cell, so `[[a/b\\|Label]]` is a link to `a/b`
  — treat the escape as literal and every table link looks broken with its
  label welded to the path.
* Fenced code blocks — and HTML comments — contain `[[…]]` and `![…]` that
  are sample or deliberately-disabled text, not live links.
* Quartz resolves a bare `[[installation]]` by shortest unique path, and
  `aliases:` in frontmatter add more names a page answers to. Both are real
  targets and neither is a file path.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CONTENT = Path(__file__).resolve().parents[1] / "content"

# Mirrors quartz.config.ts `ignorePatterns`. Kept as a literal list rather than
# parsed out of the TypeScript: a checker that silently stopped covering a
# directory because a parse failed would be worse than one that needs editing.
IGNORE = (
    "private", "templates", ".obsidian", "workshop", "quartz_style_docs",
)
IGNORE_FILES = ("DOCS_AUDIT_", "DOCS_PLAN_", "PFE - ")

FENCE = re.compile(r"^\s*(```|~~~)")
WIKILINK = re.compile(r"(?<!\\)\[\[([^\]]+)\]\]")
MDLINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def is_ignored(path: Path) -> bool:
    rel = path.relative_to(CONTENT)
    if any(part in IGNORE for part in rel.parts):
        return True
    return any(rel.name.startswith(p) for p in IGNORE_FILES)


def strip_noise(text: str) -> str:
    """Blank out fenced blocks and HTML comments, keeping line numbers intact.

    Comments matter as much as fences here: a screenshot placeholder is
    commented out precisely so it does NOT render, and reporting its `![…]`
    as a missing file sends someone to fix a link nobody can see.
    """
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else line)
    return "\n".join(out)


def frontmatter_aliases(text: str) -> list[str]:
    if not text.startswith("---"):
        return []
    end = text.find("\n---", 3)
    if end == -1:
        return []
    block = text[3:end]
    out: list[str] = []
    m = re.search(r"^aliases:\s*(.*)$", block, re.M)
    if not m:
        return out
    inline = m.group(1).strip()
    if inline.startswith("["):
        out += [a.strip().strip("\"'") for a in inline.strip("[]").split(",") if a.strip()]
    elif inline:
        out.append(inline.strip("\"'"))
    else:  # a block list under the key
        for line in block[m.end():].splitlines():
            if re.match(r"^\s*-\s+", line):
                out.append(re.sub(r"^\s*-\s+", "", line).strip().strip("\"'"))
            elif line.strip() and not line.startswith(" "):
                break
    return [a for a in out if a]


def target_of(link: str) -> str:
    """The path part of a wikilink body, with label, anchor and block dropped.

    `\\|` and `|` both separate target from label. Inside a markdown table the
    pipe MUST be written `\\|` or it ends the cell, so the escaped form is the
    normal spelling there — not, as a first pass assumed, a literal pipe in the
    target. Treating it as literal made every table link in this repo look
    broken, with the label still stuck on the end of the path.

    A trailing `.md` is dropped: some links carry it, and Quartz resolves
    either spelling.
    """
    body = re.split(r"\\\||\|", link, maxsplit=1)[0]
    body = body.split("#")[0].split("^")[0].strip()
    return body[:-3] if body.endswith(".md") else body


def build_index(pages: list[Path]) -> tuple[set[str], dict[str, int]]:
    """Every name a link may legitimately use, and how many pages claim each."""
    # Distinct PAGES per name, not occurrences. Counting occurrences makes a
    # root-level page ambiguous with itself: `installation.md` contributes the
    # name "installation" twice, once as its full path and once as its bare
    # name, and every bare link to it then reads as pointing at two pages.
    owners: dict[str, set[str]] = {}

    for p in pages:
        rel = p.relative_to(CONTENT).with_suffix("")
        page_id = str(rel)

        def add(name: str, _id: str = page_id) -> None:
            owners.setdefault(name, set()).add(_id)

        add(str(rel))                       # full path
        add(rel.name)                       # bare name, Quartz "shortest"
        if rel.name == "index":
            add(str(rel.parent))            # a folder resolves to its index
            add(rel.parent.name)
        for alias in frontmatter_aliases(p.read_text(encoding="utf-8")):
            add(alias.strip("/"))
    return set(owners), {k: len(v) for k, v in owners.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    pages = sorted(p for p in CONTENT.rglob("*.md") if not is_ignored(p))
    known, counts = build_index(pages)

    broken: list[tuple[str, int, str]] = []
    ambiguous: list[tuple[str, int, str]] = []
    missing_assets: list[tuple[str, int, str]] = []
    total = 0

    for page in pages:
        raw = page.read_text(encoding="utf-8")
        text = strip_noise(raw)
        rel = str(page.relative_to(CONTENT))
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in WIKILINK.finditer(line):
                total += 1
                t = target_of(m.group(1)).strip("/")
                if not t:
                    continue            # [[#anchor]] — same page
                if t not in known:
                    broken.append((rel, lineno, t))
                elif "/" not in t and counts.get(t, 0) > 1:
                    ambiguous.append((rel, lineno, t))
            for m in MDLINK.finditer(line):
                href = m.group(1).split()[0].strip("<>")
                if href.startswith(("http://", "https://", "mailto:", "#", "data:")):
                    continue
                target = (page.parent / href.split("#")[0]).resolve()
                if not target.exists():
                    missing_assets.append((rel, lineno, href))

    def report(title: str, rows: list[tuple[str, int, str]]) -> None:
        if rows and not args.quiet:
            print(f"\n{title} ({len(rows)}):")
            for f, n, t in rows:
                print(f"  {f}:{n}  {t}")

    report("Broken wikilinks", broken)
    report("Ambiguous bare wikilinks (resolve to more than one page)", ambiguous)
    report("Missing local files referenced from markdown", missing_assets)

    print(
        f"\n{len(pages)} pages, {total} wikilinks — "
        f"{len(broken)} broken, {len(ambiguous)} ambiguous, "
        f"{len(missing_assets)} missing files."
    )
    return 1 if (broken or missing_assets) else 0


if __name__ == "__main__":
    raise SystemExit(main())
