from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class Match:
    entry_id: str
    trigger: Optional[str]
    score: int
    reason: str
    depth: int = 0
    match_type: str = "direct"


@dataclass(frozen=True)
class WorldBookEntry:
    entry_id: str
    name: str
    keys: List[str] = field(default_factory=list)
    aliases: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    priority: int = 0
    enabled: bool = True
    content: str = ""
    entry_type: str = "context"
    scope: List[str] = field(default_factory=lambda: ["global"])
    conditions: dict = field(default_factory=dict)
    recursive_activation: bool = False
    placement: str = "RELEVANT_WORLD_BOOK"
    required: bool = False


@dataclass(frozen=True)
class ResolvedContext:
    entries: List[WorldBookEntry]
    skills: List[str]
    resources: List[str]
    matches: List[Match]
    estimated_tokens: int
    omitted: List[str] = field(default_factory=list)
