# LOOP-001 — Project Context Recovery

## Purpose
Recover enough authoritative project context to continue work after context-window truncation or session changes.

## Sequence
AI_CONTEXT → PROJECT_STATE → REGISTRY → active STAGE → relevant MODULE/LOOP → relevant release log → relevant ADR.

## Output
A restored working context containing current version, stage, loop, module status, constraints, decisions, and next action.

## Integrity Rule
Unknown information must remain unknown; the recovery process must not invent missing history.

## Status
Completed as the repository recovery procedure. Runtime per-turn injection is handled by LOOP-002.
