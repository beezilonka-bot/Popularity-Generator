from tests.preset.adapter import MockAdapter, TurnRequest, TurnResponse
from tests.preset.evaluator import load_cases
from tests.preset.runner import run_case


def test_mock_adapter_is_deterministic():
    adapter = MockAdapter({
        "P-001": TurnResponse(
            text="A quote post republishes another post with your own commentary.",
            metadata={"adapter": "mock"},
        )
    })
    request = TurnRequest("P-001", "task", "preset")
    assert adapter.run(request).text.startswith("A quote post")


def test_runner_does_not_mark_mock_response_as_passed():
    case = load_cases("tests/preset/cases.yaml")[0]
    adapter = MockAdapter({
        case.case_id: TurnResponse("sample", metadata={"adapter": "mock"})
    })
    run = run_case(
        case,
        preset="PRESET",
        project_context="PG",
        adapter=adapter,
    )
    assert run.result.status == "UNJUDGED"
    assert run.result.status != "PASS"
