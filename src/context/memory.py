"""Long Memory source loader.

The first implementation is deliberately file-backed and deterministic.
Memory entries are independent from World Book entries.
"""

from pathlib import Path
from typing import List

import yaml

from .engine import Candidate


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
                reason="memory source",
                placement=item.get("placement", "LONG_MEMORY"),
            )
        )
    return result
