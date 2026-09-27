# Changelog

All notable project changes are recorded here. Detailed release records live under docs/releases/.

## [Unreleased] — 2026-09-27

### Changed
- Refined `PRESET-001` into a compact turn-level operating protocol.
- Added an explicit understand → classify → context check → action → execute → verify → persist → respond loop.
- Clarified source authority, uncertainty handling, research/evidence behavior, completion criteria, and project/code change discipline.
- Kept World Book, Long Memory, Skills, and Resources outside the baseline preset.

### Added
- ADR-005 — Model Operating Preset as a Turn-Level Operating Protocol.
- PRESET-001 behavioral evaluation suite with 10 machine-readable scenarios.
- Model adapter protocol, deterministic MockAdapter, and evaluation runner.
- OpenAI-compatible runtime adapter using environment-only credentials.

### Verification
- Static AST smoke checks passed.
- Full repository pytest execution passed: 20 tests.
- Authenticated Tierflow model-list request succeeded.
- Authenticated Tierflow chat-completion smoke request succeeded.
- Full 10-case real-model behavioral evaluation remains pending.

## [v0.2.0] — 2026-09-27

### Added
- MOD-012 — Context Engine & Prompt Assembly.
- LOOP-004 — Context Retrieval & Prompt Assembly.
- ADR-004 — Source-Neutral Context Engine.
- Source-neutral candidate, ranking, and budget primitives.
- Scoped World Book retrieval, conditions, bounded recursive activation, and traceable selection.
- Separate Long Memory registry and task-triggered retrieval boundary.
- Canonical Prompt Assembly and global context-budget enforcement.
- v0.2.0 release record.

### Solved
- Prevents World Book from becoming the general-purpose context orchestrator.
- Separates Long Memory from World Book.
- Separates retrieval from ranking, budgeting, and placement.
- Removes duplicated runtime defaults from the Python hot path.

### Not Yet Complete
- Full repository test-suite execution/verification.
- Production model adapter.
- Automatic memory promotion.
- Semantic retrieval.
- Full Skill content expansion.

## [v0.1.2] — 2026-09-27

### Added
- MOD-011 — World Book Retrieval & Context Injection.
- LOOP-003 — World Book Task-to-Context Resolution.
- Initial X-focused World Book registry and entries.
- Separate Preset, World Book, Skill, and Resource registries.
- Architecture map and three-layer context model.
- ADR-003 documenting keyword-routed adaptive context.

### Solved
- Avoids injecting the complete skill library on every turn.
- Establishes deterministic task-to-context routing.
- Makes semantic retrieval optional.

## [v0.1.1] — 2026-09-27

### Added
- MOD-010 — Model Operating Preset & Per-Turn Model Context Injection.
- LOOP-002 — Per-Turn Model Context Injection.
- Mandatory model operating preset and per-turn context contract.

## [v0.1.0] — 2026-09-27

### Added
- Persistent project context entry point.
- Current-state record.
- Machine-readable registry for stages, modules, loops, and releases.
- Context recovery protocol.
