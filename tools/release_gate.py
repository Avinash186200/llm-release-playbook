"""Release gate: read eval results JSON and return pass, fail or unsure.

The decision uses a 95% Wilson interval for the pass rate:
  pass    the low end of the interval is at or above the threshold
  fail    the high end of the interval is below the threshold
  unsure  the interval contains the threshold (add cases; do not lower the bar)

Accepted JSON shapes:
  {"passed": 45, "total": 50}
  {"cases": [{"id": "q1", "passes": 3, "runs": 3}, ...]}   # pass^k: a case passes only if every run passed
  {"cases": [{"id": "q1", "passed": true}, ...]}

Optional keys: "threshold" (used when --threshold is not given).

Usage: python tools/release_gate.py RESULTS.json [--threshold 0.9] [--z 1.96] [--split dev]
Exit code: 0 pass, 1 fail, 2 unsure, 3 bad input.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

EXIT_CODES = {"pass": 0, "fail": 1, "unsure": 2}


def wilson_interval(passed: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if total <= 0:
        raise ValueError("total must be positive")
    if not 0 <= passed <= total:
        raise ValueError("passed must be between 0 and total")
    p = passed / total
    denom = 1 + z * z / total
    centre = (p + z * z / (2 * total)) / denom
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def decide(passed: int, total: int, threshold: float, z: float = 1.96) -> str:
    if not 0 < threshold <= 1:
        raise ValueError("threshold must be in (0, 1]")
    low, high = wilson_interval(passed, total, z)
    if low >= threshold:
        return "pass"
    if high < threshold:
        return "fail"
    return "unsure"


def sign_test(only_a: int, only_b: int) -> float:
    """Two-sided exact sign test p-value on the disagreements of a paired comparison."""
    n = only_a + only_b
    if n == 0:
        return 1.0
    k = min(only_a, only_b)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2**n
    return min(1.0, 2 * tail)


def _case_passed(case: dict) -> bool:
    if "passes" in case and "runs" in case:
        runs, passes = int(case["runs"]), int(case["passes"])
        if runs <= 0 or not 0 <= passes <= runs:
            raise ValueError(f"case {case.get('id', '?')}: bad passes/runs")
        return passes == runs
    if "passed" in case:
        if not isinstance(case["passed"], bool):
            raise ValueError(f"case {case.get('id', '?')}: 'passed' must be true or false")
        return case["passed"]
    raise ValueError(f"case {case.get('id', '?')}: needs 'passes' and 'runs', or 'passed'")


def count(results: dict, split: str | None = None) -> tuple[int, int]:
    """Return (passed, total) from a results object."""
    if "cases" in results:
        cases = results["cases"]
        if not isinstance(cases, list):
            raise ValueError("'cases' must be a list")
        if split is not None:
            cases = [c for c in cases if c.get("split") == split]
        if not cases:
            raise ValueError("no cases to score")
        passed = sum(1 for c in cases if _case_passed(c))
        return passed, len(cases)
    if split is not None:
        raise ValueError("--split needs a 'cases' list")
    if "passed" in results and "total" in results:
        return int(results["passed"]), int(results["total"])
    raise ValueError("results need 'cases', or 'passed' and 'total'")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Wilson-interval release gate")
    parser.add_argument("results", type=Path)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--z", type=float, default=1.96)
    parser.add_argument("--split", default=None, help="score only cases with this split value")
    args = parser.parse_args(argv)

    try:
        results = json.loads(args.results.read_text(encoding="utf-8"))
        if not isinstance(results, dict):
            raise ValueError("top level must be an object")
        threshold = args.threshold if args.threshold is not None else results.get("threshold")
        if threshold is None:
            raise ValueError("no threshold: pass --threshold or set 'threshold' in the JSON")
        passed, total = count(results, args.split)
        decision = decide(passed, total, float(threshold), args.z)
        low, high = wilson_interval(passed, total, args.z)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    print(f"{passed}/{total} = {passed / total:.1%}  interval {low:.1%} to {high:.1%}  "
          f"threshold {float(threshold):.1%}  -> {decision}")
    return EXIT_CODES[decision]


if __name__ == "__main__":
    sys.exit(main())
