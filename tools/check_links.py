"""Offline check of relative links in Markdown files.

Finds [text](target) links and checks that relative targets exist on disk. External links (http, https,
mailto) and pure anchors are skipped, because CI runs offline. Code blocks are ignored.

Usage: python tools/check_links.py [ROOT]
Exit code 0 when all links resolve, 1 otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", ".pytest_cache", "__pycache__"}


def broken_links(root: Path) -> list[str]:
    problems: list[str] = []
    for md in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in md.relative_to(root).parts):
            continue
        in_code = False
        for number, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            line = re.sub(r"`[^`]*`", "", line)
            for target in LINK_RE.findall(line):
                if target.startswith(SKIP_PREFIXES):
                    continue
                path_part = target.split("#", 1)[0]
                if not path_part:
                    continue
                if not (md.parent / path_part).exists():
                    problems.append(f"{md.relative_to(root)}:{number}: broken link '{target}'")
    return problems


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0] if args else ".").resolve()
    problems = broken_links(root)
    for problem in problems:
        print(problem)
    if problems:
        return 1
    print("all relative links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
