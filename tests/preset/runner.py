"""Evaluation runner that connects cases to a model adapter."""

from dataclasses import dataclass
from pathlib import Path

from .adapter import ModelAdapter, TurnRequest
from .evaluator import EvaluationResult, PresetCase, build_turn_input


@dataclass(frozen=True)
class EvaluationRun:
    case: PresetCase
    result: EvaluationResult
    response_text: str


def run_case(
    case: PresetCase,
    *,
    preset: str,
    project_context: str,
    adapter: ModelAdapter,
) -> EvaluationRun:
    request = TurnRequest(
        case_id=case.case_id,
        task=case.task,
        preset=build_turn_input(
            preset,
            case.task,
            project_context=project_context,
        ),
        project_context=project_context,
    )
    response = adapter.run(request)
    status = "NOT_RUN" if response.text.startswith("NOT_RUN:") else "UNJUDGED"
    result = EvaluationResult(
        case_id=case.case_id,
        status=status,
        notes=(f"adapter={response.metadata.get('adapter', 'unknown')}",),
    )
    return EvaluationRun(case=case, result=result, response_text=response.text)
