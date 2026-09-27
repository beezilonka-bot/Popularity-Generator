"""Minimal PRESET-001 behavioral evaluation framework.

This module intentionally does not call a model API. It defines the stable
input/output contract for future model adapters and deterministic checks.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable
import yaml


@dataclass(frozen=True)
class PresetCase:
    case_id: str
    name: str
    task: str
    checks: tuple[str, ...]


@dataclass(frozen=True)
class EvaluationResult:
    case_id: str
    status: str
    checks: dict[str, bool] = field(default_factory=dict)
    notes: tuple[str, ...] = ()


def load_cases(path: str | Path) -> list[PresetCase]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    if data.get("preset_id") != "PRESET-001":
        raise ValueError("unexpected preset_id")
    return [
        PresetCase(
            case_id=item["id"],
            name=item["name"],
            task=item["task"],
            checks=tuple(item.get("checks", [])),
        )
        for item in data.get("cases", [])
    ]


def build_turn_input(
    preset: str,
    task: str,
    *,
    project_context: str = "",
) -> str:
    parts = [
        "=== MODEL_PRESET ===",
        preset,
        "=== FRESH_PROJECT_CONTEXT ===",
        project_context,
        "=== CURRENT_TASK ===",
        task,
    ]
    return "\n\n".join(parts)


def summarize_results(results: Iterable[EvaluationResult]) -> dict[str, Any]:
    items = list(results)
    return {
        "total": len(items),
        "passed": sum(x.status == "PASS" for x in items),
        "failed": sum(x.status == "FAIL" for x in items),
        "not_run": sum(x.status == "NOT_RUN" for x in items),
        "results": [
            {
                "id": x.case_id,
                "status": x.status,
                "checks": x.checks,
                "notes": list(x.notes),
            }
            for x in items
        ],
    }
