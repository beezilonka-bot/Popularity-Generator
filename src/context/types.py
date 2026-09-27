from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class Match:
    entry_id: str
    trigger: str
    score: int
    reason: str

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

@dataclass(frozen=True)
class ResolvedContext:
    entries: List[WorldBookEntry]
    skills: List[str]
    resources: List[str]
    matches: List[Match]
    estimated_tokens: int
