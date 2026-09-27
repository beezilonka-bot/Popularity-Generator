# LOOP-003 — World Book Task-to-Context Resolution

## Purpose

Convert a user's current task into a minimal, relevant context bundle using World Book entries.

## Inputs

- CURRENT_TASK
- FRESH_PROJECT_CONTEXT
- `worldbook/registry.yaml`
- relevant World Book entry files
- available skill IDs and resource references

## Sequence

1. Classify the task at a coarse level:
   - post writing
   - thread writing
   - research
   - editing
   - style imitation/analysis
   - content repurposing
   - project maintenance
   - other
2. Scan the current task and permitted context text for triggers.
3. Activate exact keywords and aliases.
4. Apply optional filters and exclusions.
5. Rank matches by specificity and priority.
6. Resolve referenced skills/resources.
7. Run bounded recursive activation when explicitly allowed.
8. Deduplicate.
9. Enforce the World Book token budget.
10. Produce a compact `RELEVANT_WORLD_BOOK` block.
11. Append the result after the fresh project snapshot and before CURRENT_TASK execution details.

## Required Per-Turn Order

`MODEL_PRESET → FRESH_PROJECT_CONTEXT → RELEVANT_WORLD_BOOK → CURRENT_TASK`

The World Book is therefore an adaptive layer inside the existing per-turn contract, not a replacement for the mandatory preset or authoritative project state.

## Selection Rules

- Prefer the smallest bundle that can materially improve the task.
- A high match count does not justify loading redundant entries.
- Hard constraints outrank style suggestions.
- Skills should be loaded by ID; their full text should be injected only when needed.
- Resources should normally be represented by concise metadata and links, not copied wholesale.
- Semantic retrieval is a fallback, not a mandatory dependency.
- If no entry matches, inject an explicit empty result rather than guessing.

## Trace

Each resolved entry should expose:
- entry ID;
- matched trigger(s);
- selection reason;
- priority;
- token estimate;
- source/reference;
- whether activation was direct or recursive.

## Failure Conditions

- Registry missing or invalid.
- Entry ID not unique.
- Activated content exceeds budget with no deterministic truncation policy.
- A required hard constraint is excluded by a lower-priority entry.
- Recursive activation exceeds configured depth.
- The resolver silently falls back to invented context.

## Completion

LOOP-003 is complete when the runtime context builder can deterministically produce the World Book subset for a task and include it in every model request without bypassing LOOP-002.
