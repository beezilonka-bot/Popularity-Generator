"""Build and assemble the deterministic per-turn context package."""

from pathlib import Path
from typing import Dict, Iterable

import yaml

from .assembler import assemble_prompt
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
    recent_context: Iterable[str] | None = None,
    scan_depth: int | None = None,
) -> Dict[str, object]:
    root = Path(project_root)
    project = _load_yaml(root / "project.yaml")
    wb_registry = _load_yaml(root / "worldbook" / "registry.yaml")
    memory_registry = _load_yaml(root / "memory" / "registry.yaml")

    wb_defaults = wb_registry.get("defaults", {})
    mem_defaults = memory_registry.get("defaults", {})
    context_policy = project.get("context", {})
    policy = context_policy.get("retrieval_policy", {})
    routing = wb_registry.get("routing", {})
    scan_fields = routing.get("scan_fields", ["CURRENT_TASK"])
    configured_depth = int(routing.get("scan_depth", 3))
    effective_depth = configured_depth if scan_depth is None else max(0, int(scan_depth))

    recent_items = list(recent_context or [])
    scan_parts = []
    if "CURRENT_TASK" in scan_fields:
        scan_parts.append(current_task)
    if "FRESH_PROJECT_CONTEXT" in scan_fields:
        scan_parts.append(project_context)
    if "RECENT_CONTEXT" in scan_fields and effective_depth:
        scan_parts.extend(recent_items[-effective_depth:])
    scan_text = "\n".join(part for part in scan_parts if part)

    resolved = resolve_worldbook(
        current_task,
        load_entries(root / "worldbook" / "registry.yaml"),
        scan_text=scan_text,
        max_entries=int(policy.get("max_worldbook_entries", wb_defaults.get("max_entries", 8))),
        token_budget=int(policy.get("worldbook_token_budget", wb_defaults.get("token_budget", 1800))),
        max_recursive_depth=int(wb_defaults.get("max_recursive_depth", 2)),
        max_recursive_steps=int(wb_defaults.get("max_recursive_steps", 16)),
        allow_regex=bool(wb_defaults.get("allow_regex", False)),
    )

    memory_candidates = load_memories(
        root / "memory" / "registry.yaml",
        task=current_task,
    )
    memory_result = select_budgeted(
        memory_candidates,
        max_items=int(mem_defaults.get("max_entries", 4)),
        token_budget=int(mem_defaults.get("token_budget", 800)),
    )

    context = {
        "MODEL_PRESET": model_preset,
        "FRESH_PROJECT_CONTEXT": project_context,
        "LONG_MEMORY": {
            "entries": [
                {"id": c.candidate_id, "content": c.content, "placement": c.placement}
                for c in memory_result.selected
            ],
            "estimated_tokens": memory_result.estimated_tokens,
            "omitted": [c.candidate_id for c in memory_result.omitted],
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

    context["PROMPT"] = assemble_prompt(
        context,
        max_total_tokens=int(policy.get("max_total_context_tokens", 6000)),
    )
    return context
