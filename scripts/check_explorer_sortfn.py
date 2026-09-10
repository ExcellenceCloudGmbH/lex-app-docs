#!/usr/bin/env python3
"""Fail if the Explorer's `sortFn` would not survive being serialised.

Explorer does not call `sortFn` directly. It writes `sortFn.toString()` into a
data attribute and the browser runs `new Function("return " + str)()`, which
evaluates in GLOBAL scope. Anything the body references that is not defined
there throws on the first comparison, `trie.sort()` dies, and the sidebar
renders completely empty — with no error on the page and nothing in the build
output.

That happened. The body contained

    const rank = (n) => { ... }

which esbuild, running with --keep-names, rewrote to

    const rank = __name((n) => { ... }, "rank")

`__name` is a bundle-scope helper and does not exist where the string is
evaluated, so every page shipped with an empty Explorer.

The rule this enforces is therefore stricter than "no closures": the body must
contain **no inner function of any kind**, because declaring one is what makes
the compiler inject the helper. Straight-line code only.

    python scripts/check_explorer_sortfn.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LAYOUT = Path(__file__).resolve().parents[1] / "quartz.layout.ts"

# Constructs that make esbuild emit a `__name(...)` wrapper INSIDE the body.
INNER_FUNCTION = re.compile(
    r"""
    (\bfunction\b)                    # function declaration or expression
  | (=>)                              # any arrow beyond the signature
    """,
    re.VERBOSE,
)


def sortfn_body(source: str) -> str | None:
    """The text between `sortFn:`'s arrow and its matching closing brace."""
    at = source.find("sortFn:")
    if at == -1:
        return None
    arrow = source.find("=>", at)
    brace = source.find("{", arrow)
    if arrow == -1 or brace == -1:
        return None
    depth, i = 0, brace
    while i < len(source):
        if source[i] == "{":
            depth += 1
        elif source[i] == "}":
            depth -= 1
            if depth == 0:
                return source[brace + 1 : i]
        i += 1
    return None


def main() -> int:
    if not LAYOUT.exists():
        print(f"{LAYOUT} not found", file=sys.stderr)
        return 2

    body = sortfn_body(LAYOUT.read_text(encoding="utf-8"))
    if body is None:
        print("No `sortFn:` in quartz.layout.ts — nothing to check.")
        return 0

    # Comments legitimately contain arrows in prose ("install → model → ship").
    code = re.sub(r"//[^\n]*", "", body)
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.S)

    offenders = [m.group(0) for m in INNER_FUNCTION.finditer(code)]
    if offenders:
        print(
            "::error title=Explorer sortFn is not self-contained::"
            "`sortFn` contains an inner function "
            f"({', '.join(sorted(set(offenders)))}). esbuild's --keep-names wraps it "
            "in a `__name(...)` call, and `__name` does not exist where Explorer "
            "evaluates the serialised function — the sidebar renders empty, with no "
            "error anywhere. Inline it as straight-line code.",
            file=sys.stderr,
        )
        return 1

    print("OK: Explorer sortFn is straight-line and self-contained.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
