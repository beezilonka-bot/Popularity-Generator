"""Deterministic World Book retrieval.

World Book is a context source, not the Context Engine itself. Retrieval is
cheap and explainable: direct matching, conditions, bounded recursion, then
deterministic selection.
"""

import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import yaml

from .engine import estimate_tokens, unique_ids
from .types import Match, ResolvedContext, WorldBookEntry


def _norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def load_registry(path: str | Path) -> Tuple[dict, Path]:
    path = Path(path)
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}, path.parent


def load_entries(registry_path: str | Path) -> List[WorldBookEntry]:
    registry, base = load_registry(registry_path)
    raw_entries = registry.get("entries", [])
    if isinstance(raw_entries, dict):
        raw_entries = [{"id": key, **value} for key, value in raw_entries.items()]

    entries: List[WorldBookEntry] = []
    seen = set()
    for item in raw_entries:
        entry_id = item["id"]
        if entry_id in seen:
            raise ValueError(f"duplicate World Book entry ID: {entry_id}")
        seen.add(entry_id)
        if not item.get("enabled", True):
            continue
        content = (base / item["path"]).read_text(encoding="utf-8")
        entries.append(
            WorldBookEntry(
                entry_id=entry_id,
                name=item.get("name", entry_id),
                keys=[str(x) for x in item.get("keys", [])],
                aliases=[str(x) for x in item.get("aliases", [])],
                skills=[str(x) for x in item.get("skills", [])],
                resources=[str(x) for x in item.get("resources", [])],
                priority=int(item.get("priority", 0)),
                content=content,
                entry_type=item.get("type", "context"),
                scope=[str(x) for x in item.get("scope", ["global"])],
                conditions=item.get("conditions", {}) or {},
                recursive_activation=bool(item.get("recursive_activation", False)),
                placement=item.get("placement", "RELEVANT_WORLD_BOOK"),
                required=bool(item.get("required", False)),
            )
        )
    return entries


def _conditions_pass(entry: WorldBookEntry, scan_text: str, scope: str) -> bool:
    if scope not in entry.scope and "global" not in entry.scope:
        return False
    text = _norm(scan_text)
    conditions = entry.conditions
    required = [_norm(x) for x in conditions.get("all", [])]
    any_of = [_norm(x) for x in conditions.get("any", [])]
    excluded = [_norm(x) for x in conditions.get("not_any", [])]
    if required and not all(x and x in text for x in required):
        return False
    if any_of and not any(x and x in text for x in any_of):
        return False
    if any(x and x in text for x in excluded):
        return False
    return True


def _match(entry: WorldBookEntry, scan_text: str, *, reason: str, depth: int):
    text = _norm(scan_text)
    best = None
    for raw in entry.keys + entry.aliases:
        trigger = _norm(raw)
        if trigger and trigger in text and (best is None or len(trigger) > len(best)):
            best = trigger
    if best is None:
        return None
    return Match(
        entry_id=entry.entry_id,
        trigger=best,
        score=entry.priority + min(len(best), 40),
        reason=reason,
        depth=depth,
        match_type="direct" if depth == 0 else "recursive",
    )


def resolve_worldbook(
    task: str,
    entries: Iterable[WorldBookEntry],
    *,
    scope: str = "global",
    scan_text: str | None = None,
    max_entries: int = 8,
    token_budget: int = 1800,
    max_recursive_depth: int = 2,
    max_recursive_steps: int = 16,
    allow_regex: bool = False,
) -> ResolvedContext:
    entry_list = list(entries)
    by_id: Dict[str, WorldBookEntry] = {e.entry_id: e for e in entry_list}
    source_text = scan_text if scan_text is not None else task
    matches: Dict[str, Match] = {}

    def add_match(match: Match):
        current = matches.get(match.entry_id)
        if current is None or (
            (match.depth < current.depth)
            or (match.depth == current.depth and match.score > current.score)
        ):
            matches[match.entry_id] = match

    for entry in entry_list:
        if _conditions_pass(entry, source_text, scope):
            match = _match(entry, source_text, reason="direct keyword/alias", depth=0)
            if match:
                add_match(match)
            if allow_regex:
                for raw in entry.keys + entry.aliases:
                    try:
                        if re.search(raw, source_text, flags=re.IGNORECASE):
                            add_match(Match(entry.entry_id, raw, entry.priority + min(len(raw), 40),
                                            "regex match", 0, "direct"))
                            break
                    except re.error:
                        continue

    frontier = [matches[eid] for eid in sorted(matches)]
    steps = 0
    for depth in range(1, max_recursive_depth + 1):
        if not frontier:
            break
        next_frontier = []
        for parent in frontier:
            parent_entry = by_id[parent.entry_id]
            if not parent_entry.recursive_activation:
                continue
            for target in entry_list:
                if target.entry_id in matches or not _conditions_pass(target, parent_entry.content, scope):
                    continue
                if steps >= max_recursive_steps:
                    break
                match = _match(target, parent_entry.content, reason=f"recursive from {parent.entry_id}", depth=depth)
                steps += 1
                if match:
                    add_match(match)
                    next_frontier.append(match)
            if steps >= max_recursive_steps:
                break
        frontier = next_frontier
        if steps >= max_recursive_steps:
            break

    ordered = sorted(
        matches.values(),
        key=lambda m: (-int(by_id[m.entry_id].required), m.depth, -m.score, m.entry_id),
    )

    selected: List[WorldBookEntry] = []
    selected_matches: List[Match] = []
    omitted: List[str] = []
    used = 0

    for match in ordered:
        if len(selected) >= max_entries:
            omitted.append(match.entry_id)
            continue
        entry = by_id[match.entry_id]
        cost = estimate_tokens(entry.content)
        if used + cost > token_budget:
            omitted.append(entry.entry_id)
            continue
        selected.append(entry)
        selected_matches.append(match)
        used += cost

    skills = unique_ids(skill for e in selected for skill in e.skills)
    resources = unique_ids(resource for e in selected for resource in e.resources)

    return ResolvedContext(
        entries=selected,
        skills=skills,
        resources=resources,
        matches=selected_matches,
        estimated_tokens=used,
        omitted=omitted,
    )
