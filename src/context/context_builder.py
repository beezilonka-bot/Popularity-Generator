"""Assemble the deterministic per-turn context package."""

from pathlib import Path
from typing import Dict

import yaml

from .engine import select_budgeted
from .memory import load_memories
from .worldbook_resolver import load_entries, resolve_worldbook


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def build_context(
    *,
    project_root: str | Path,
    current_task: str,
    project_context: str,
    model_preset: str,
) -> Dict[str, object]:
    root = Path(project_root)
    project = _load_yaml(root / "project.yaml")
    wb_registry = _load_yaml(root / "worldbook" / "registry.yaml")
    memory_registry = _load_yaml(root / "memory" / "registry.yaml")

    wb_defaults = wb_registry.get("defaults", {})
    mem_defaults = memory_registry.get("defaults", {})
    policy = project.get("context", {}).get("retrieval_policy", {})

    entries = load_entries(root / "worldbook" / "registry.yaml")
    resolved = resolve_worldbook(
        current_task,
        entries,
        max_entries=int(policy.get("max_worldbook_entries", wb_defaults.get("max_entries", 8))),
        token_budget=int(policy.get("worldbook_token_budget", wb_defaults.get("token_budget", 1800))),
        max_recursive_depth=int(wb_defaults.get("max_recursive_depth", 2)),
        max_recursive_steps=int(wb_defaults.get("max_recursive_steps", 16)),
        allow_regex=bool(wb_defaults.get("allow_regex", False)),
    )

    memory_candidates = load_memories(root / "memory" / "registry.yaml")
    memory_result = select_budgeted(
        memory_candidates,
        max_items=int(mem_defaults.get("max_entries", 4)),
        token_budget=int(mem_defaults.get("token_budget", 800)),
    )

    return {
        "MODEL_PRESET": model_preset,
        "FRESH_PROJECT_CONTEXT": project_context,
        "LONG_MEMORY": {
            "entries": [
                {"id": c.candidate_id, "content": c.content, "placement": c.placement}
                for c in memory_result.selected
            ],
            "estimated_tokens": memory_result.estimated_tokens,
        },
        "RELEVANT_WORLD_BOOK": {
            "activation_trace": [
                {
                    "entry_id": m.entry_id,
                    "trigger": m.trigger,
                    "score": m.score,
                    "reason": m.reason,
                    "depth": m.depth,
                    "match_type": m.match_type,
                }
                for m in resolved.matches
            ],
            "entries": [
                {
                    "id": e.entry_id,
                    "name": e.name,
                    "content": e.content,
                    "placement": e.placement,
                }
                for e in resolved.entries
            ],
            "skills": resolved.skills,
            "resources": resolved.resources,
            "estimated_tokens": resolved.estimated_tokens,
            "omitted": resolved.omitted,
        },
        "CURRENT_TASK": current_task,
    }
