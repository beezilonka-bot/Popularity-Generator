from pathlib import Path

from tests.preset.evaluator import load_cases, summarize_results


def test_loads_all_preset_cases():
    path = Path("tests/preset/cases.yaml")
    cases = load_cases(path)
    assert len(cases) == 10
    assert [x.case_id for x in cases] == [f"P-{i:03d}" for i in range(1, 11)]


def test_summary_distinguishes_not_run():
    result = summarize_results([
        __import__("tests.preset.evaluator", fromlist=["EvaluationResult"]).EvaluationResult(
            "P-001", "NOT_RUN"
        )
    ])
    assert result["total"] == 1
    assert result["not_run"] == 1
    assert result["passed"] == 0
