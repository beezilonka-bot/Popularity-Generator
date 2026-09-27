"""Final prompt assembly with one global context budget."""

from typing import Dict, Iterable

from .engine import estimate_tokens


SECTION_ORDER = (
    "MODEL_PRESET",
    "FRESH_PROJECT_CONTEXT",
    "LONG_MEMORY",
    "RELEVANT_WORLD_BOOK",
    "CURRENT_TASK",
)


def _section_text(name: str, value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if name == "LONG_MEMORY":
            return "\n".join(
                f"[{x['id']}] {x['content']}" for x in value.get("entries", [])
            )
        if name == "RELEVANT_WORLD_BOOK":
            return "\n".join(
                f"[{x['id']}] {x['content']}" for x in value.get("entries", [])
            )
    return str(value)


def assemble_prompt(
    context: Dict[str, object],
    *,
    max_total_tokens: int = 6000,
) -> str:
    """Build the canonical section order.

    Mandatory sections are never silently removed. Dynamic sections are
    truncated only as a last resort to respect the global budget.
    """
    rendered = []
    for name in SECTION_ORDER:
        text = _section_text(name, context.get(name, ""))
        rendered.append((name, text))

    total = sum(estimate_tokens(text) for _, text in rendered)
    if total > max_total_tokens:
        dynamic = {"LONG_MEMORY", "RELEVANT_WORLD_BOOK"}
        remaining = max_total_tokens - sum(
            estimate_tokens(text) for name, text in rendered if name not in dynamic
        )
        remaining = max(0, remaining)
        for index, (name, text) in enumerate(rendered):
            if name not in dynamic:
                continue
            if remaining <= 0:
                rendered[index] = (name, "")
                continue
            allowed_chars = remaining * 4
            rendered[index] = (name, text[:allowed_chars])
            remaining -= estimate_tokens(rendered[index][1])

    return "\n\n".join(
        f"=== {name} ===\n{text}" for name, text in rendered
    )
