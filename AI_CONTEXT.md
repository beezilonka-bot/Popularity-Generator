# AI Context Recovery

This is the canonical recovery entry point after conversation truncation, session changes, or model changes.

## Recovery protocol

1. Read PROJECT_STATE.md.
2. Read REGISTRY.yaml.
3. Identify the active STAGE, LOOP, and in-progress MODs.
4. Read only the relevant stage/module/loop documents.
5. Read relevant release records and ADRs.
6. Never infer undocumented history.

## Mandatory per-turn contract

Every model turn receives:

MODEL_PRESET → FRESH_PROJECT_CONTEXT → LONG_MEMORY → RELEVANT_WORLD_BOOK → CURRENT_TASK

The preset is injected every turn. Dynamic context is rebuilt every turn; previous dynamic context is stale.

## Source of truth

- Current state: PROJECT_STATE.md
- Entity index: REGISTRY.yaml
- Project/runtime settings: project.yaml
- Presets: prompts/
- World Book: worldbook/
- Long Memory: memory/
- Skills: skills/
- Resources: resources/
- History: CHANGELOG.md and docs/releases/
- Architecture rationale: docs/decisions/

Registries are indexes. Do not load entire catalogs into the prompt.

## Context layering

Always-on:
- model preset
- minimal project state

Triggered:
- relevant Long Memory
- relevant World Book
- relevant Skill IDs
- Resource pointers

On-demand:
- large resource contents and external material only when execution requires them.

## Current recovery target

Read PROJECT_STATE.md and follow the active LOOP. For v0.2.0 the active loop is LOOP-004 — Context Retrieval & Prompt Assembly.
