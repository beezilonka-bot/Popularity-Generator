"""Build the per-turn context package.

The builder intentionally keeps project loading separate from World Book
selection so the retrieval layer can be tested independently.
"""

from pathlib import Path
from typing import Dict, Optional

from .worldbook_resolver import load_entries, resolve_worldbook


def build_context(
    *,
    project_root: str | Path,
    current_task: str,
    project_context: str,
    model_preset: str,
    max_worldbook_entries: int = 8,
    worldbook_token_budget: int = 1800,
) -> Dict[str, object]:
    root = Path(project_root)
    entries = load_entries(root / "worldbook" / "registry.yaml")
    resolved = resolve_worldbook(
        current_task,
        entries,
        max_entries=max_worldbook_entries,
        token_budget=worldbook_token_budget,
    )

    return {
        "MODEL_PRESET": model_preset,
        "FRESH_PROJECT_CONTEXT": project_context,
        "RELEVANT_WORLD_BOOK": {
            "activation_trace": [
                {
                    "entry_id": m.entry_id,
                    "trigger": m.trigger,
                    "score": m.score,
                    "reason": m.reason,
                }
                for m in resolved.matches
            ],
            "entries": [
                {
                    "id": e.entry_id,
                    "name": e.name,
                    "content": e.content,
                }
                for e in resolved.entries
            ],
            "skills": resolved.skills,
            "resources": resolved.resources,
            "estimated_tokens": resolved.estimated_tokens,
        },
        "CURRENT_TASK": current_task,
    }
