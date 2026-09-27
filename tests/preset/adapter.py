"""Model adapter contracts and an OpenAI-compatible runtime adapter for PRESET evaluation."""

from dataclasses import dataclass, field
import json
import os
from typing import Mapping, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


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
    """Deterministic adapter for testing the evaluator pipeline."""

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


class OpenAICompatibleAdapter:
    """Runtime adapter for OpenAI-compatible chat-completions APIs.

    Credentials are read only from environment variables and are never
    included in TurnResponse metadata or persisted by this module.
    """

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        timeout: float = 120.0,
        max_tokens: int = 2048,
        temperature: float = 0.0,
    ):
        self.base_url = (base_url or os.environ["MODEL_API_BASE_URL"]).rstrip("/")
        self.api_key = api_key or os.environ["MODEL_API_KEY"]
        self.model = model or os.environ["MODEL_API_MODEL"]
        self.timeout = timeout
        self.max_tokens = max_tokens
        self.temperature = temperature

    def run(self, request: TurnRequest) -> TurnResponse:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": request.preset}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        http_request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(http_request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(
                f"model API returned HTTP {exc.code}: {detail[:500]}"
            ) from exc
        except URLError as exc:
            raise RuntimeError(f"model API connection failed: {exc}") from exc

        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError("model API returned no choices")

        message = choices[0].get("message") or {}
        text = message.get("content") or ""
        if not text and message.get("reasoning_content"):
            text = message["reasoning_content"]

        usage = data.get("usage") or {}
        metadata = {
            "adapter": "openai-compatible",
            "model": str(data.get("model", self.model)),
            "finish_reason": str(choices[0].get("finish_reason", "")),
            "total_tokens": str(usage.get("total_tokens", "")),
        }
        return TurnResponse(text=text, metadata=metadata)
