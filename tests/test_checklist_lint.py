import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import checklist_lint as cl  # noqa: E402
import check_links  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def test_clean_items():
    text = (
        "- [x] Evals pass | status: PASS | evidence: https://ci.example.org/run/1\n"
        "- [x] Not used | status: N/A | evidence: no tools in this release\n"
        "- [ ] Latency | status: FAIL | evidence: reports/latency.md\n"
    )
    items, problems = cl.lint_text(text)
    assert items == 3
    assert problems == []


@pytest.mark.parametrize("line,fragment", [
    ("- [x] A | evidence: https://x.org", "missing 'status:'"),
    ("- [x] A | status: DONE | evidence: https://x.org", "not one of"),
    ("- [x] A | status: PASS | evidence:", "missing evidence"),
    ("- [x] A | status: PASS | evidence: trust me", "not a link"),
    ("- [x] A | status: FAIL | evidence: https://x.org", "ticked but status is FAIL"),
    ("- [ ] A | status: PASS | evidence: https://x.org", "not ticked"),
])
def test_problems(line, fragment):
    _, problems = cl.lint_text(line)
    assert any(fragment in str(p) for p in problems), problems


def test_code_blocks_ignored():
    text = "```\n- [ ] example | status: | evidence:\n```\n"
    assert cl.lint_text(text) == (0, [])


def test_blank_template_fails():
    _, problems = cl.lint_file(ROOT / "checklists" / "go-no-go.md")
    assert problems


@pytest.mark.parametrize("name", ["go-no-go.md", "rollout.md", "review-checklist.md"])
def test_filled_examples_are_clean(name):
    items, problems = cl.lint_file(ROOT / "examples" / name)
    assert items > 0
    assert problems == [], problems


def test_main_exit_codes(tmp_path):
    good = tmp_path / "good.md"
    good.write_text("- [x] A | status: PASS | evidence: https://x.org\n", encoding="utf-8")
    bad = tmp_path / "bad.md"
    bad.write_text("- [x] A | status: PASS | evidence:\n", encoding="utf-8")
    empty = tmp_path / "empty.md"
    empty.write_text("# nothing\n", encoding="utf-8")
    assert cl.main([str(good)]) == 0
    assert cl.main([str(bad)]) == 1
    assert cl.main([str(empty)]) == 1
    assert cl.main([str(tmp_path / "missing.md")]) == 2
    assert cl.main([]) == 2


def test_repo_links_resolve():
    assert check_links.broken_links(ROOT) == []


def test_link_checker_finds_broken(tmp_path):
    (tmp_path / "a.md").write_text("[x](missing.md) [y](https://x.org) [z](#top)\n", encoding="utf-8")
    problems = check_links.broken_links(tmp_path)
    assert len(problems) == 1 and "missing.md" in problems[0]
