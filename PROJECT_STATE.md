# Project State

## Identity
- Project: Popularity-Generator
- Repository: beezilonka-bot/Popularity-Generator
- Default branch: main

## Current Version
v0.2.0

## Active Stage
STAGE-001 — Persistent Project Memory & Context Recovery

## Active Loop
LOOP-004 — Context Retrieval & Prompt Assembly

## Status
The source-neutral Context Engine foundation is implemented. World Book supports scoped matching, conditions, bounded recursion, traceability, and budgeted selection. Long Memory is a separate task-triggered source. Final Prompt Assembly enforces canonical ordering and a global context budget. PRESET-001 now has a machine-readable 10-case behavioral evaluation suite and a model-adapter contract; no real LLM behavioral run has yet been executed.

## Completed
- Context Engine candidate/ranking/budget primitives.
- Scoped/conditional/bounded World Book retrieval.
- Separate Long Memory registry and explicit task-triggered retrieval.
- Final Prompt Assembly integration.
- Architecture/module/loop/ADR/release records for v0.2.0.
- Tests added for ranking, budgeting, World Book scope, conditions, recursion, assembly, and end-to-end builder behavior.
- Refined PRESET-001 as the baseline turn-level operating protocol.
- PRESET-001 behavioral test specification with 10 cases.
- Machine-readable PRESET evaluator contract, runner, and deterministic MockAdapter.

## In Progress
- Execute and verify the repository test suite.
- Run the PRESET evaluator against a real model adapter.
- Validate configured World Book scan fields and bounded recent-context scanning.
- Resolve any implementation/schema mismatches found by execution.
- Evaluate keyword recall before introducing semantic retrieval.
- Define automatic Long Memory promotion only after the retrieval layer is stable.

## Not Started
- Production model adapter.
- Popularity analysis engine.
- Trend detection.
- Content generation engine.
- Publishing integrations.
- Feedback/data-learning loop.
- Semantic retrieval.

## Verification Notes
- Static Python AST smoke check of the new evaluator/adapter/runner modules: passed.
- 10-case schema smoke check: passed.
- Full pytest execution: not yet verified.
- Real LLM behavioral evaluation: not yet run.

## Last Verified
2026-09-27
