# STAGE-001 — Persistent Project Memory & Context Recovery

## Purpose
Create a durable project memory layer independent of model conversation history and define how that memory is supplied to the model on every turn.

## Scope
- Version governance
- Stage/module/loop identity
- Current project state
- Context recovery protocol
- Mandatory model operating preset
- Per-turn context injection contract
- World Book task-to-context routing
- Changelog and release records
- Architecture decision records

## Modules
MOD-001 through MOD-011

## Loops
- LOOP-001 — Project Context Recovery
- LOOP-002 — Per-Turn Model Context Injection
- LOOP-003 — World Book Task-to-Context Resolution

## Completion Criteria
- A new session can recover current project state from repository files.
- Every stable capability has a permanent module ID.
- Every completed release records additions, solved problems, and current state.
- Architecture decisions are traceable through ADR IDs.
- Every model turn receives the mandatory preset and a fresh project-context snapshot.
- Every model turn resolves a bounded, relevant World Book subset before task execution.
- World Book retrieval is deterministic, budgeted, deduplicated, and traceable.
- The runtime cannot silently bypass the per-turn context contract.
