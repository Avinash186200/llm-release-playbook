"""Lint a filled checklist: every item needs a status and an evidence link.

Item format:
    - [x] Item text | status: PASS | evidence: https://example.org/run/42

Rules:
  * status is one of PASS, FAIL, N/A
  * evidence is not empty
  * a ticked box must have status PASS or N/A
  * an unticked box must not claim PASS
  * N/A evidence is a reason; other evidence must look like a link or a path

Usage: python tools/checklist_lint.py FILE [FILE ...]
Exit code 0 when clean, 1 when problems are found, 2 on usage errors.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ITEM_RE = re.compile(r"^\s*[-*]\s+\[(?P<box>[ xX])\]\s+(?P<rest>.*)$")
FIELD_RE = re.compile(r"\|\s*(?P<key>status|evidence)\s*:\s*(?P<value>[^|]*)", re.IGNORECASE)
VALID_STATUS = {"PASS", "FAIL", "N/A"}
LINK_RE = re.compile(r"(https?://\S+|\]\([^)]+\)|[\w.\-]+/[\w./\-#]+|[\w\-]+\.(md|json|txt|log|html)\b)")


@dataclass
class Problem:
    line: int
    message: str

    def __str__(self) -> str:
        return f"line {self.line}: {self.message}"


def lint_text(text: str) -> tuple[int, list[Problem]]:
    """Return (number of items, problems)."""
    problems: list[Problem] = []
    items = 0
    in_code = False
    for number, line in enumerate(text.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        match = ITEM_RE.match(line)
        if not match:
            continue
        items += 1
        ticked = match.group("box").lower() == "x"
        fields = {m.group("key").lower(): m.group("value").strip() for m in FIELD_RE.finditer(match.group("rest"))}
        status = fields.get("status", "").upper()
        evidence = fields.get("evidence", "")

        if "status" not in fields:
            problems.append(Problem(number, "missing 'status:' field"))
        elif status not in VALID_STATUS:
            problems.append(Problem(number, f"status '{fields['status']}' is not one of PASS, FAIL, N/A"))
        if not evidence:
            problems.append(Problem(number, "missing evidence"))
        elif status != "N/A" and not LINK_RE.search(evidence):
            problems.append(Problem(number, f"evidence '{evidence}' is not a link or path"))
        if ticked and status == "FAIL":
            problems.append(Problem(number, "box is ticked but status is FAIL"))
        if not ticked and status == "PASS":
            problems.append(Problem(number, "status is PASS but box is not ticked"))
    return items, problems


def lint_file(path: Path) -> tuple[int, list[Problem]]:
    return lint_text(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print(__doc__.strip().splitlines()[-2], file=sys.stderr)
        return 2
    failed = False
    for name in args:
        path = Path(name)
        if not path.is_file():
            print(f"{name}: not a file", file=sys.stderr)
            return 2
        items, problems = lint_file(path)
        if items == 0:
            print(f"{name}: no checklist items found")
            failed = True
            continue
        for problem in problems:
            print(f"{name}: {problem}")
        if problems:
            failed = True
        else:
            print(f"{name}: {items} items OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
