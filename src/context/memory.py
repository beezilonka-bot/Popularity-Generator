"""Long Memory source loader and deterministic relevance filter."""

from pathlib import Path
from typing import List

import yaml

from .engine import Candidate, select_budgeted


def load_memories(registry_path: str | Path) -> List[Candidate]:
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
        result.append(
            Candidate(
                candidate_id=item["id"],
                source="long_memory",
                content=str(content),
                priority=int(item.get("priority", 0)),
                required=bool(item.get("required", False)),
                match_type="memory",
                trigger=_best_trigger(item, ""),
                reason="memory source",
                placement=item.get("placement", "LONG_MEMORY"),
            )
        )
    return result


def _best_trigger(item: dict, task: str):
    text = task.lower()
    triggers = [str(x) for x in item.get("keys", [])] + [str(x) for x in item.get("aliases", [])]
    matches = [x for x in triggers if x.lower() in text]
    return max(matches, key=len) if matches else None


def resolve_memories(
    task: str,
    candidates: List[Candidate],
    *,
    max_entries: int,
    token_budget: int,
) -> tuple[List[Candidate], List[str]]:
    """Select only explicitly triggered memories.

    A memory without keys/aliases is not injected automatically. This keeps
    Long Memory from becoming an always-on transcript.
    """
    matched = []
    for candidate in candidates:
        # Candidate.trigger is only a marker; load_memories keeps raw trigger
        # metadata on the object in future schema revisions. For v1, IDs and
        # content are matched as a conservative fallback.
        if candidate.trigger:
            matched.append(candidate)
    result = select_budgeted(matched, max_items=max_entries, token_budget=token_budget)
    return result.selected, [x.candidate_id for x in result.omitted]
