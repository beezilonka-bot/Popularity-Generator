"""Core deterministic context-engine primitives.

Retrieval sources produce candidates; filters, ranking, budgeting, and
placement are handled separately so new sources do not require a new engine.
"""

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Sequence, Tuple


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    source: str
    content: str
    priority: int = 0
    required: bool = False
    depth: int = 0
    match_type: str = "direct"
    trigger: Optional[str] = None
    reason: str = ""
    skills: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    placement: str = "RELEVANT_CONTEXT"


@dataclass(frozen=True)
class SelectionResult:
    selected: List[Candidate]
    omitted: List[Candidate]
    estimated_tokens: int


def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4)


def rank_candidates(candidates: Iterable[Candidate]) -> List[Candidate]:
    return sorted(
        candidates,
        key=lambda c: (
            -int(c.required),
            0 if c.match_type == "direct" else 1,
            -c.priority,
            -len(c.trigger or ""),
            c.depth,
            c.candidate_id,
        ),
    )


def select_budgeted(
    candidates: Sequence[Candidate],
    *,
    max_items: int,
    token_budget: int,
) -> SelectionResult:
    selected: List[Candidate] = []
    omitted: List[Candidate] = []
    used = 0

    for candidate in rank_candidates(candidates):
        if len(selected) >= max_items:
            omitted.append(candidate)
            continue
        cost = estimate_tokens(candidate.content)
        if used + cost > token_budget:
            omitted.append(candidate)
            continue
        selected.append(candidate)
        used += cost

    return SelectionResult(selected=selected, omitted=omitted, estimated_tokens=used)


def unique_ids(values: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
