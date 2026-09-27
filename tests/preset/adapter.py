"""Model adapter contracts for PRESET behavioral evaluation."""

from dataclasses import dataclass, field
from typing import Mapping, Protocol, Sequence


@dataclass(frozen=True)
class TurnRequest:
    case_id: str
    task: str
    preset: str
    project_context: str = ""


@dataclass(frozen=True)
class TurnResponse:
    text: str
    actions: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)


class ModelAdapter(Protocol):
    def run(self, request: TurnRequest) -> TurnResponse:
        """Execute one evaluation turn."""


class MockAdapter:
    """Deterministic adapter for testing the evaluator pipeline.

    It deliberately does not pretend to model real LLM behavior.
    """

    def __init__(self, responses: Mapping[str, TurnResponse] | None = None):
        self._responses = dict(responses or {})

    def run(self, request: TurnRequest) -> TurnResponse:
        response = self._responses.get(request.case_id)
        if response is None:
            return TurnResponse(
                text="NOT_RUN: no mock response configured",
                metadata={"adapter": "mock"},
            )
        return response
