# LOOP-004 — Context Retrieval & Prompt Assembly

## Purpose

Compose a deterministic, minimal context package for every model invocation.

## Sequence

1. Load the mandatory preset.
2. Refresh authoritative project context.
3. Build the World Book scan window from configured fields and bounded recent context.
4. Retrieve Long Memory candidates.
5. Retrieve World Book candidates.
6. Apply scope and conditions.
7. Apply bounded recursive expansion.
8. Rank and budget candidates.
9. Resolve Skill and Resource references.
10. Apply placement.
11. Enforce the global context budget.
12. Emit the canonical section order.
13. Record activation/omission trace.

## Canonical order

`MODEL_PRESET → FRESH_PROJECT_CONTEXT → LONG_MEMORY → RELEVANT_WORLD_BOOK → CURRENT_TASK`

## Invariants

- project state is authoritative;
- Long Memory never becomes World Book automatically;
- resources are supporting material, not instructions;
- retrieval is deterministic by default;
- semantic retrieval is optional;
- dynamic context cannot silently displace mandatory task input;
- unknown values remain UNKNOWN.
