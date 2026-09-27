# PER-TURN CONTEXT TEMPLATE

The runtime constructs this package for every model invocation.

## Required package

MODEL_PRESET
FRESH_PROJECT_CONTEXT
LONG_MEMORY
RELEVANT_WORLD_BOOK
CURRENT_TASK

## Construction rules

- The preset is always included verbatim.
- Project context is refreshed every turn.
- Long Memory is queried independently and only explicitly relevant memories are selected.
- World Book is queried independently with scope, conditions, bounded recursion, ranking, and budget.
- Skills are resolved by ID and expanded only when required.
- Resources are pointers unless execution requires their contents.
- Retrieval and placement are separate concerns.
- Final Prompt Assembly enforces the global context budget.
- If no dynamic entry matches, use NONE.
- If a value cannot be established from repository records, use UNKNOWN.
- Do not invent missing values.

## Resolution pipeline

sources → candidates → filters → recursion → ranking → local budgets → skill/resource resolution → global budget → placement → prompt

## Canonical order

MODEL_PRESET → FRESH_PROJECT_CONTEXT → LONG_MEMORY → RELEVANT_WORLD_BOOK → CURRENT_TASK

## Runtime requirement

The model adapter/middleware must construct this package before every model request. Loading it once at application startup is insufficient.
