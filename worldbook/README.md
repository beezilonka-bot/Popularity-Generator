# World Book

The World Book is the project's dynamic context-routing layer.

It is inspired by the World Info/Lorebook pattern documented by SillyTavern: entries expose trigger keys and only relevant entry content is inserted into the prompt. SillyTavern also documents filters, priorities, token budgets, and bounded recursion. citeturn0search0

## Purpose

Use keywords from the current task to automatically attach the smallest useful combination of:

- skills;
- project/domain context;
- writing style guidance;
- resources;
- examples;
- hard constraints.

## Runtime Position

`MODEL_PRESET → FRESH_PROJECT_CONTEXT → RELEVANT_WORLD_BOOK → CURRENT_TASK`

The World Book never replaces the mandatory preset or authoritative project state.

## Files

- `registry.yaml` — machine-readable entry index.
- `entries/` — standalone entry content.
- `README.md` — operating contract.

## Entry Rule

An entry must be useful when viewed alone. Metadata such as title, trigger keys, and internal notes are not assumed to be visible to the model unless they are explicitly included in the injected content.

## Token Discipline

Do not load the whole World Book. Resolve only relevant entries and stop at the configured budget.

## Retrieval Evolution

Phase 1: exact keywords and aliases.

Phase 2: filters, regex, priority, deduplication, bounded recursion.

Phase 3: fuzzy/semantic candidate retrieval when keyword matching is insufficient.

The semantic layer is optional and must not become a prerequisite for basic operation.
