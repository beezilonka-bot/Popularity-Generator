# LOOP-002 — Per-Turn Model Context Injection

## Identity
- ID: LOOP-002
- Stage: STAGE-001
- Introduced: v0.1.1
- Status: active

## Purpose
Build the context supplied to every model turn so the model receives stable operating instructions plus current project memory on every invocation.

## Input
- `prompts/MODEL_PRESET.md`
- `PROJECT_STATE.md`
- `REGISTRY.yaml`
- Active stage/loop records
- Relevant module/release/ADR records
- Current user/task input

## Sequence
1. Load the mandatory model preset.
2. Read current project state.
3. Resolve active stage and loop from the registry.
4. Resolve the relevant modules and records for the current task.
5. Build a fresh context snapshot.
6. Append the current task input.
7. Send the complete package to the model.
8. After a material repository change, update durable state/history in the same change set.

## Required Context Order
```
MODEL_PRESET
↓
PROJECT_CONTEXT_SNAPSHOT
↓
CURRENT_TASK
```

## Recovery Rule
If prior chat context is unavailable, the model must recover from repository records before reasoning about project history.

## Integrity Rule
The context snapshot is disposable; the repository records are authoritative. Never persist a generated snapshot as if it were authoritative unless explicitly designated as a durable record.

## Failure Conditions
- Missing preset: do not treat the turn as a valid project-model turn.
- Missing current state: recover it from repository records before proceeding.
- Conflicting records: surface the conflict; do not silently choose an undocumented interpretation.
- Missing fact: mark it unknown.

## Output
A model-ready per-turn context package containing:
- mandatory operating preset,
- current authoritative project state,
- relevant scoped records,
- current task.
