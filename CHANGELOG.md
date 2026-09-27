# Changelog

All notable project changes are recorded here. Detailed release records live under docs/releases/.

## [v0.1.0] — 2026-09-27

### Added
- Persistent project context entry point.
- Current-state record.
- Machine-readable registry for stages, modules, loops, and releases.
- Context recovery protocol.
- Stage/module/loop documentation structure.
- Architecture decision record structure.

### Solved
- Loss of project context caused by conversation truncation or session changes.
- Ambiguity about the current development stage and module status.
- Difficulty tracing a capability back to its stage and release.

### Current State
STAGE-001 is active. LOOP-001 is the current recovery loop. The project repository is now initialized with its documentation/state foundation.

### Next
Implement and validate the persistent context workflow before starting the product-generation engine.
