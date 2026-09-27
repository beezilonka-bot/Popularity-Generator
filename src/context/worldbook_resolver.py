"""Small deterministic World Book resolver.

Fast path: exact keyword/alias matching.
No external services, embeddings, or network calls are required.
"""

import re
from pathlib import Path
from typing import Iterable, List, Dict, Tuple

import yaml

from .types import Match, ResolvedContext, WorldBookEntry


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _estimate_tokens(text: str) -> int:
    # Deliberately conservative rough estimate for budgeting.
    return max(1, (len(text) + 3) // 4)


def load_registry(path: str | Path) -> Tuple[dict, Path]:
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data, path.parent


def load_entries(registry_path: str | Path) -> List[WorldBookEntry]:
    registry, base = load_registry(registry_path)
    entries = []
    for item in registry.get("entries", []):
        if not item.get("enabled", True):
            continue
        entry_path = base / item["path"]
        content = entry_path.read_text(encoding="utf-8")
        entries.append(WorldBookEntry(
            entry_id=item["id"],
            name=item.get("name", item["id"]),
            keys=item.get("keys", []),
            aliases=item.get("aliases", []),
            skills=item.get("skills", []),
            resources=item.get("resources", []),
            priority=int(item.get("priority", 0)),
            enabled=True,
            content=content,
        ))
    return entries


def resolve_worldbook(
    task: str,
    entries: Iterable[WorldBookEntry],
    *,
    max_entries: int = 8,
    token_budget: int = 1800,
) -> ResolvedContext:
    text = _norm(task)
    candidates: List[Match] = []

    for entry in entries:
        triggers = list(entry.keys) + list(entry.aliases)
        for raw in triggers:
            trigger = _norm(str(raw))
            if not trigger:
                continue
            if trigger in text:
                candidates.append(Match(
                    entry_id=entry.entry_id,
                    trigger=trigger,
                    score=entry.priority + min(len(trigger), 40),
                    reason="exact substring match",
                ))
                break

    by_id: Dict[str, Match] = {}
    for match in candidates:
        old = by_id.get(match.entry_id)
        if old is None or match.score > old.score:
            by_id[match.entry_id] = match

    ordered = sorted(by_id.values(), key=lambda m: (-m.score, m.entry_id))
    selected: List[WorldBookEntry] = []
    selected_matches: List[Match] = []
    used = 0

    lookup = {e.entry_id: e for e in entries}
    skills: List[str] = []
    resources: List[str] = []

    for match in ordered:
        if len(selected) >= max_entries:
            break
        entry = lookup[match.entry_id]
        cost = _estimate_tokens(entry.content)
        if selected and used + cost > token_budget:
            continue
        if not selected and cost > token_budget:
            # A single oversized entry is truncated instead of breaking the
            # whole resolver contract.
            entry = WorldBookEntry(
                entry_id=entry.entry_id,
                name=entry.name,
                keys=entry.keys,
                aliases=entry.aliases,
                skills=entry.skills,
                resources=entry.resources,
                priority=entry.priority,
                content=entry.content[: token_budget * 4],
            )
            cost = token_budget
        selected.append(entry)
        selected_matches.append(match)
        used += cost
        skills.extend(entry.skills)
        resources.extend(entry.resources)

    return ResolvedContext(
        entries=selected,
        skills=_unique(skills),
        resources=_unique(resources),
        matches=selected_matches,
        estimated_tokens=used,
    )


def _unique(values: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
