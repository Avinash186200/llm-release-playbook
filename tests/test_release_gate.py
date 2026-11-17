import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import release_gate as rg  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def test_wilson_ten_of_ten_is_not_certain():
    low, high = rg.wilson_interval(10, 10)
    assert high == 1.0
    assert 0.71 < low < 0.73


def test_wilson_known_value():
    low, high = rg.wilson_interval(45, 50)
    assert low == pytest.approx(0.7864, abs=1e-3)
    assert high == pytest.approx(0.9565, abs=1e-3)


@pytest.mark.parametrize("passed,total", [(0, 0), (-1, 10), (11, 10)])
def test_wilson_rejects_bad_input(passed, total):
    with pytest.raises(ValueError):
        rg.wilson_interval(passed, total)


def test_decide_pass_fail_unsure():
    assert rg.decide(195, 200, 0.90) == "pass"
    assert rg.decide(30, 50, 0.90) == "fail"
    assert rg.decide(45, 50, 0.90) == "unsure"


def test_decide_bad_threshold():
    with pytest.raises(ValueError):
        rg.decide(5, 10, 1.5)


def test_sign_test_values():
    assert rg.sign_test(0, 0) == 1.0
    assert rg.sign_test(2, 8) == pytest.approx(0.1094, abs=1e-3)
    assert rg.sign_test(4, 15) == pytest.approx(0.0192, abs=1e-3)


def test_count_pass_hat_k():
    results = {"cases": [{"id": "a", "passes": 3, "runs": 3}, {"id": "b", "passes": 2, "runs": 3}]}
    assert rg.count(results) == (1, 2)


def test_count_boolean_cases_and_split():
    results = {"cases": [
        {"id": "a", "passed": True, "split": "dev"},
        {"id": "b", "passed": False, "split": "dev"},
        {"id": "c", "passed": True, "split": "held_out"},
    ]}
    assert rg.count(results, "dev") == (1, 2)
    assert rg.count(results, "held_out") == (1, 1)


def test_count_rejects_bad_case():
    with pytest.raises(ValueError):
        rg.count({"cases": [{"id": "a"}]})
    with pytest.raises(ValueError):
        rg.count({"cases": [{"id": "a", "passes": 4, "runs": 3}]})


def _write(tmp_path, data):
    path = tmp_path / "r.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return str(path)


def test_main_exit_codes(tmp_path, capsys):
    assert rg.main([_write(tmp_path, {"passed": 195, "total": 200}), "--threshold", "0.9"]) == 0
    assert rg.main([_write(tmp_path, {"passed": 30, "total": 50}), "--threshold", "0.9"]) == 1
    assert rg.main([_write(tmp_path, {"passed": 45, "total": 50, "threshold": 0.9})]) == 2
    assert "unsure" in capsys.readouterr().out


def test_main_bad_input(tmp_path):
    assert rg.main([_write(tmp_path, {"passed": 1, "total": 2})]) == 3  # no threshold
    assert rg.main([_write(tmp_path, [1, 2]), "--threshold", "0.9"]) == 3
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    assert rg.main([str(bad), "--threshold", "0.9"]) == 3


def test_example_results_file_passes():
    assert rg.main([str(ROOT / "examples" / "eval-results.json")]) == 0
