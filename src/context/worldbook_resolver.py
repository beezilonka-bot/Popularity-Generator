"""Deterministic World Book resolver for per-turn context.

The resolver intentionally uses a cheap local path first. It converts
World Book matches into a minimal set of Skill and Resource references.
"""

import re
from pathlib import Path
from typing import Iterable, List, Dict, Tuple

import yaml

from .types import Match, ResolvedContext, WorldBookEntry


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def _estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4)


def load_registry(path: str | Path) -> Tuple[dict, Path]:
    path = Path(path)
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}, path.parent


def load_entries(registry_path: str | Path) -> List[WorldBookEntry]:
    registry, base = load_registry(registry_path)
    entries: List[WorldBookEntry] = []
    raw_entries = registry.get("entries", [])

    # Current schema is a list. Keep a small compatibility path for the
    # previous mapping schema so repository migrations do not break runtime.
    if isinstance(raw_entries, dict):
        raw_entries = [
            {"id": key, **value} for key, value in raw_entries.items()
        ]

    for item in raw_entries:
        if not item.get("enabled", True):
            continue
        content = (base / item["path"]).read_text(encoding="utf-8")
        entries.append(WorldBookEntry(
            entry_id=item["id"],
            name=item.get("name", item["id"]),
            keys=[str(x) for x in item.get("keys", [])],
            aliases=[str(x) for x in item.get("aliases", [])],
            skills=[str(x) for x in item.get("skills", [])],
            resources=[str(x) for x in item.get("resources", [])],
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
    entry_list = list(entries)
    text = _norm(task)
    candidates: List[Match] = []

    for entry in entry_list:
        best_trigger = None
        for raw in entry.keys + entry.aliases:
            trigger = _norm(raw)
            if trigger and trigger in text:
                if best_trigger is None or len(trigger) > len(best_trigger):
                    best_trigger = trigger
        if best_trigger:
            candidates.append(Match(
                entry_id=entry.entry_id,
                trigger=best_trigger,
                score=entry.priority + min(len(best_trigger), 40),
                reason="exact substring match",
            ))

    by_id: Dict[str, Match] = {}
    for match in candidates:
        old = by_id.get(match.entry_id)
        if old is None or match.score > old.score:
            by_id[match.entry_id] = match

    ordered = sorted(by_id.values(), key=lambda m: (-m.score, m.entry_id))
    lookup = {e.entry_id: e for e in entry_list}
    selected: List[WorldBookEntry] = []
    selected_matches: List[Match] = []
    used = 0
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
