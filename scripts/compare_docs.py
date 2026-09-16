#!/usr/bin/env python3
"""Measure two revisions of the docs on the same ruler.

    python scripts/compare_docs.py --before f1feb34 --after main
    python scripts/compare_docs.py --before v1 --after v2 --gates ../lex-app/.github/scripts
    python scripts/compare_docs.py --before f1feb34 --after main --markdown > report.md

"Is the rewrite actually better?" is not answerable by reading it -- the person
who rewrote it is the worst available judge, and a reviewer cannot hold 70 pages
of before and after in their head at once. So this measures both trees the same
way and prints the difference.

Link resolution is delegated to `check_links.py` rather than reimplemented, and
that is load-bearing. A hand-rolled resolver was tried first and reported 41
broken links in a tree the real checker passes clean -- it did not know about
`aliases:` frontmatter or Quartz's shortest-path matching, so it invented
defects. A comparison that reports false defects is worse than no comparison,
because the numbers look authoritative either way.

The checker is COPIED INTO each extracted tree and run there, which is what
makes it the same ruler: it derives its content root from its own location, so
one version of one checker judges both revisions. Whichever `check_links.py` is
in your working tree is the ruler -- change it and both sides move together.

What this cannot tell you is whether a sentence is any good. It counts, resolves,
and runs the correctness gates -- prose quality still needs a reader.

What it cannot tell you is whether a sentence is any good. It counts, resolves,
and runs the correctness gates -- prose quality still needs a reader.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
MDIMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
VIDEO = re.compile(r"<video|\.mp4")
# Counted from the RAW page, before fences are stripped: a mermaid diagram
# is a fenced block, and stripping code to count words also deletes every
# diagram in the tree. Missing this said 42 pages carried no visual when
# 30 of them carried a rendered diagram.
MERMAID = re.compile(r"^\s*```mermaid", re.M)
CODEFENCE = re.compile(r"^\s*```")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
DRAFT = re.compile(r"^draft:\s*true\s*$", re.M)


@dataclass
class Metrics:
    rev: str
    pages: int = 0
    words: int = 0
    sections: list[str] = field(default_factory=list)
    figures: int = 0            # distinct image files referenced
    figure_refs: int = 0        # embeds, so a figure used twice counts twice
    videos: int = 0
    diagrams: int = 0           # mermaid blocks, which Quartz renders natively
    illustrated: int = 0        # pages carrying at least one figure or video
    broken_links: int = 0
    ambiguous: int = 0
    missing_images: int = 0
    image_style: str = "-"
    gates: dict = field(default_factory=dict)

    @property
    def illustrated_pct(self) -> float:
        return 100.0 * self.illustrated / self.pages if self.pages else 0.0

    @property
    def words_per_page(self) -> int:
        return round(self.words / self.pages) if self.pages else 0


def export(repo: Path, rev: str, dest: Path) -> Path:
    """Lay `rev`'s content/ tree out on disk. Raises if the rev has none."""
    dest.mkdir(parents=True, exist_ok=True)
    tar = subprocess.run(
        ["git", "-C", str(repo), "archive", rev, "content"],
        capture_output=True,
    )
    if tar.returncode != 0:
        raise SystemExit(
            f"`git archive {rev} content` failed: {tar.stderr.decode().strip()}"
        )
    subprocess.run(["tar", "-x", "-C", str(dest)], input=tar.stdout, check=True)
    return dest / "content"


def strip(text: str) -> str:
    """Frontmatter, HTML comments and fenced code removed.

    All three carry `[[…]]` and `![…]` that never render, and a commented-out
    figure is precisely the thing a placeholder is -- counting it would report
    the gap as filled.
    """
    text = FRONTMATTER.sub("", text)
    text = HTML_COMMENT.sub("", text)
    out, fenced = [], False
    for line in text.splitlines():
        if CODEFENCE.match(line):
            fenced = not fenced
            continue
        if not fenced:
            out.append(line)
    return "\n".join(out)


def measure(content: Path, rev: str) -> Metrics:
    m = Metrics(rev=rev)
    pages = [p for p in sorted(content.rglob("*.md"))]
    slugs: set[str] = set()
    for p in pages:
        raw = p.read_text(encoding="utf-8", errors="replace")
        if DRAFT.search(FRONTMATTER.search(raw).group(0) if FRONTMATTER.search(raw) else ""):
            continue
        rel = p.relative_to(content).with_suffix("").as_posix()
        slugs.add(rel)
        slugs.add(rel.rsplit("/", 1)[-1])
        if rel.endswith("/index"):
            slugs.add(rel[: -len("/index")])

    files: set[str] = set()
    relative_style = rootward_style = 0

    for p in pages:
        raw = p.read_text(encoding="utf-8", errors="replace")
        fm = FRONTMATTER.search(raw)
        if fm and DRAFT.search(fm.group(0)):
            continue
        m.pages += 1
        # Before strip(), which removes fenced blocks.
        mermaid = len(MERMAID.findall(raw))
        m.diagrams += mermaid
        body = strip(raw)
        m.words += len(body.split())
        if content.joinpath(p.relative_to(content)).parent != content:
            pass

        has_visual = False
        for ref in MDIMAGE.findall(body):
            if ref.startswith(("http://", "https://", "data:")):
                continue
            m.figure_refs += 1
            has_visual = True
            bare = ref.split("#")[0]
            if bare.startswith("../") or bare.startswith("./"):
                relative_style += 1
                target = (p.parent / bare).resolve()
            else:
                rootward_style += 1
                target = (content / bare).resolve()
            files.add(bare.lstrip("./").lstrip("/").replace("../", ""))
            if not target.is_file():
                # Accept the other convention before calling it missing: the
                # question here is whether the FILE exists, not whether the
                # path matches today's rule.
                other = (
                    (content / bare.replace("../", "")).resolve()
                    if bare.startswith("../")
                    else (p.parent / bare).resolve()
                )
                if not other.is_file():
                    m.missing_images += 1

        if VIDEO.search(body):
            m.videos += len(re.findall(r"<video", body)) or 1
            has_visual = True
        if mermaid:
            has_visual = True
        if has_visual:
            m.illustrated += 1

    m.figures = len(files)
    m.sections = sorted(
        d.name for d in content.iterdir() if d.is_dir() and d.name != "images"
    )
    if relative_style and rootward_style:
        m.image_style = f"mixed ({rootward_style} root, {relative_style} relative)"
    elif relative_style:
        m.image_style = "relative to the page"
    elif rootward_style:
        m.image_style = "from the content root"
    return m


GATES = {
    "check_doc_imports.py": ("imports", r"(\d+) unresolvable import"),
    "check_doc_commands.py": (
        "commands",
        r"(\d+) `lex <command>` reference\(s\) that do not exist",
    ),
    "check_doc_env_vars.py": ("env vars", r"(\d+) environment variable"),
}


LINKS_SUMMARY = re.compile(
    r"(\d+) pages, (\d+) wikilinks .*?(\d+) broken, (\d+) ambiguous, (\d+) missing"
)


def run_link_checker(tree: Path, checker: Path) -> tuple[int, int]:
    """(broken, ambiguous) from this repo's own checker, run inside `tree`.

    Copied in rather than imported: the checker locates content relative to its
    own file, so a copy at `<tree>/scripts/` checks `<tree>/content/`. One
    version of one checker then judges both revisions, which is the whole point
    -- a resolver written here instead got 41 broken links out of a tree the
    real one passes clean, because it knew nothing about `aliases:` frontmatter
    or Quartz's shortest-path matching.
    """
    dest = tree / "scripts"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / checker.name).write_bytes(checker.read_bytes())
    r = subprocess.run(
        [sys.executable, str(dest / checker.name), "--quiet"],
        capture_output=True, text=True,
    )
    hit = LINKS_SUMMARY.search(r.stdout + r.stderr)
    if not hit:
        return (-1, -1)
    return (int(hit.group(3)), int(hit.group(4)))


def run_gates(content: Path, scripts: Path) -> dict:
    """The lex-app correctness gates, pointed at an arbitrary content tree."""
    out: dict[str, str] = {}
    for script, (label, _pattern) in GATES.items():
        path = scripts / script
        if not path.is_file():
            continue
        r = subprocess.run(
            [sys.executable, str(path), str(content)], capture_output=True, text=True
        )
        text = (r.stdout + r.stderr).strip().splitlines()
        # Two kinds of line come back. `::error file=` is one per OCCURRENCE --
        # the old tree emits 34 of them for `lex Init` alone, which buries the
        # answer in the evidence. `OK:` and `::error title=` are the per-check
        # verdicts. Keep the verdicts, count the occurrences.
        verdicts = []
        for line in text:
            if line.startswith("OK:"):
                verdicts.append(line[len("OK:"):].strip().rstrip("."))
            elif line.startswith("::error title="):
                body = re.sub(r"^::error title=[^:]*::", "", line)
                # The gates name every offender so the person who broke the
                # build can fix it. Here the count IS the answer -- a list of
                # 341 variable names buries it.
                head = body.split(":")[0].strip()
                verdicts.append(head or body.split(". ")[0])
        occurrences = sum(1 for l in text if l.startswith("::error file="))
        if occurrences:
            verdicts.append(f"{occurrences} occurrence(s) flagged in the pages")
        out[label] = verdicts or ["(no output)"]
    return out


def fmt(before: int | float, after: int | float, higher_is_better: bool = True) -> str:
    if isinstance(before, float) or isinstance(after, float):
        b, a = f"{before:.0f}%", f"{after:.0f}%"
        delta = after - before
        arrow = "" if abs(delta) < 0.5 else (" ↑" if delta > 0 else " ↓")
        return f"{b} → **{a}**{arrow}"
    delta = after - before
    sign = f"+{delta}" if delta > 0 else str(delta)
    if delta == 0:
        return f"{before} → **{after}**"
    good = (delta > 0) == higher_is_better
    mark = "✅" if good else "⚠️"
    return f"{before} → **{after}**  ({sign}) {mark}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--before", required=True, help="git revision of the older tree")
    ap.add_argument("--after", default="HEAD", help="git revision of the newer tree")
    ap.add_argument("--repo", default=".", help="the lex-app-docs checkout")
    ap.add_argument("--gates", help="path to lex-app/.github/scripts, to run the correctness gates")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    with tempfile.TemporaryDirectory(prefix="docs-compare-") as tmp:
        root = Path(tmp)
        before_tree, after_tree = root / "before", root / "after"
        b = measure(export(repo, args.before, before_tree), args.before)
        a = measure(export(repo, args.after, after_tree), args.after)

        checker = repo / "scripts" / "check_links.py"
        if checker.is_file():
            b.broken_links, b.ambiguous = run_link_checker(before_tree, checker)
            a.broken_links, a.ambiguous = run_link_checker(after_tree, checker)
        if args.gates:
            scripts = Path(args.gates).resolve()
            b.gates = run_gates(export(repo, args.before, root / "before"), scripts)
            a.gates = run_gates(export(repo, args.after, root / "after"), scripts)

        if args.json:
            print(json.dumps({"before": b.__dict__, "after": a.__dict__}, indent=2, default=str))
            return 0

        print(f"\n# Docs comparison — `{args.before}` → `{args.after}`\n")
        print("| | before | after |")
        print("|---|---|---|")
        rows = [
            ("Published pages", b.pages, a.pages, True),
            ("Words", b.words, a.words, True),
            ("Words per page", b.words_per_page, a.words_per_page, True),
            ("Top-level sections", len(b.sections), len(a.sections), True),
            ("Distinct figures", b.figures, a.figures, True),
            ("Figure embeds", b.figure_refs, a.figure_refs, True),
            ("Videos", b.videos, a.videos, True),
            ("Mermaid diagrams", b.diagrams, a.diagrams, True),
            ("Broken wikilinks", b.broken_links, a.broken_links, False),
            ("Ambiguous wikilinks", b.ambiguous, a.ambiguous, False),
            ("Missing image files", b.missing_images, a.missing_images, False),
        ]
        for label, bv, av, higher in rows:
            print(f"| {label} | {bv} | {av} |")
        print()
        print("## Change\n")
        for label, bv, av, higher in rows:
            print(f"- **{label}** — {fmt(bv, av, higher)}")
        print(f"- **Pages carrying a visual** — {fmt(b.illustrated_pct, a.illustrated_pct)}"
              f"  ({b.illustrated}/{b.pages} → {a.illustrated}/{a.pages})")
        print(f"- **Image path convention** — {b.image_style} → **{a.image_style}**")

        print("\n## Sections\n")
        gone = [s for s in b.sections if s not in a.sections]
        new = [s for s in a.sections if s not in b.sections]
        kept = [s for s in a.sections if s in b.sections]
        if new:
            print(f"- added: {', '.join('`' + s + '`' for s in new)}")
        if gone:
            print(f"- removed: {', '.join('`' + s + '`' for s in gone)}")
        if kept:
            print(f"- unchanged: {', '.join('`' + s + '`' for s in kept)}")

        if b.gates or a.gates:
            print("\n## Correctness gates\n")
            for label in sorted(set(b.gates) | set(a.gates)):
                print(f"\n**{label}**\n")
                for tag, res in (("before", b.gates.get(label, [])), ("after", a.gates.get(label, []))):
                    for line in res:
                        print(f"  - _{tag}_ — {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
