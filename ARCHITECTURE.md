# Popularity-Generator Architecture

## Core principle

- Preset: how the model must work.
- World Book: which stable knowledge/rules/context should activate.
- Long Memory: durable facts learned from prior work.
- Skills: how a task should be performed.
- Resources: supporting evidence/material.
- Project State: authoritative current system state.

These layers must not duplicate each other.

## Runtime

CURRENT_TASK + PROJECT_STATE
→ context sources
→ candidates
→ filters/conditions
→ bounded recursion
→ ranking
→ local budgets
→ Skill/Resource references
→ global budget
→ placement
→ Prompt Assembly
→ model

## Context sources

### World Book
Keyword/alias routing is the deterministic default. Entries support scope, conditions, priority, bounded recursive activation, traceability, and placement metadata.

### Long Memory
Separate from World Book. Memory is not a transcript and is never injected merely because it exists in the registry. It must be explicitly relevant to the task.

### Skills
Resolved by ID. Full skill text is loaded only when required.

### Resources
Resolved as pointers by default. Large external material is fetched on demand.

## Context Engine

The source-neutral Context Engine owns candidate ranking and budget selection.

- src/context/engine.py — common candidate primitives
- src/context/worldbook_resolver.py — World Book source adapter
- src/context/memory.py — Long Memory source adapter
- src/context/assembler.py — final section ordering and global budget
- src/context/context_builder.py — per-turn orchestration

## Canonical prompt order

MODEL_PRESET → FRESH_PROJECT_CONTEXT → LONG_MEMORY → RELEVANT_WORLD_BOOK → CURRENT_TASK

Mandatory task input is never silently displaced by dynamic context.

## Retrieval policy

Deterministic retrieval is the default. Semantic retrieval is optional and should be introduced only after keyword recall is measured to be insufficient.

## ID policy

IDs are permanent and never reused.

- Project: PG
- Release: vMAJOR.MINOR.PATCH
- Stage: STAGE-NNN
- Module: MOD-NNN
- Loop: LOOP-NNN
- Preset: PRESET-NNN
- World Book: WB-*
- Skill: SKILL-*
- Resource: RES-*
- ADR: ADR-NNN

## Current direction

STAGE-001 remains active. v0.2.0 establishes the Context Engine foundation. Current work is verification and hardening before semantic retrieval or the product-generation stages are started.
