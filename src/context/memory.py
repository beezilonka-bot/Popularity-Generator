"""Long Memory source loader and deterministic relevance filter."""

from pathlib import Path
from typing import List

import yaml

from .engine import Candidate


def load_memories(
    registry_path: str | Path,
    *,
    task: str = "",
) -> List[Candidate]:
    path = Path(registry_path)
    registry = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    base = path.parent
    result: List[Candidate] = []

    for item in registry.get("entries", []):
        if not item.get("enabled", True):
            continue
        content = item.get("content")
        if content is None and item.get("path"):
            content = (base / item["path"]).read_text(encoding="utf-8")
        if not content:
            continue

        trigger = _best_trigger(item, task)
        if trigger is None:
            continue

        result.append(
            Candidate(
                candidate_id=item["id"],
                source="long_memory",
                content=str(content),
                priority=int(item.get("priority", 0)),
                required=bool(item.get("required", False)),
                match_type="memory",
                trigger=trigger,
                reason="explicit memory trigger",
                placement=item.get("placement", "LONG_MEMORY"),
            )
        )
    return result


def _best_trigger(item: dict, task: str):
    text = task.lower()
    triggers = [str(x) for x in item.get("keys", [])] + [
        str(x) for x in item.get("aliases", [])
    ]
    matches = [x for x in triggers if x.lower() in text]
    return max(matches, key=len) if matches else None
