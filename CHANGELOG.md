# Changelog

All notable project changes are recorded here. Detailed release records live under docs/releases/.

## [v0.1.2] — 2026-09-27

### Added
- MOD-011 — World Book Retrieval & Context Injection.
- LOOP-003 — World Book Task-to-Context Resolution.
- `worldbook/registry.yaml` with keyword/alias routing, priority, budget, and bounded recursion settings.
- Initial X-focused World Book entries for posts, threads, style, research/resources, and factuality.
- World Book operating rules in the mandatory model preset.
- World Book section in the per-turn context contract.
- ADR-003 documenting the keyword-routed adaptive-context architecture.

### Solved
- Avoids injecting the complete skill library into every model turn.
- Creates a deterministic fast path from task keywords to relevant skills/resources.
- Establishes a place for resources and writing guidance to be activated only when relevant.
- Defines semantic retrieval as an optional later fallback instead of a mandatory dependency.

### Current State
STAGE-001 remains active. LOOP-003 is the current implementation focus. The runtime context builder/middleware has not yet been implemented.

### Next
Implement the runtime resolver so every model invocation produces:
`MODEL_PRESET + FRESH_PROJECT_CONTEXT + RELEVANT_WORLD_BOOK + CURRENT_TASK`.

## [v0.1.1] — 2026-09-27

### Added
- MOD-010 — Model Operating Preset & Per-Turn Context Injection.
- LOOP-002 — Per-Turn Model Context Injection.
- Mandatory model operating preset at prompts/MODEL_PRESET.md.
- Per-turn context package template at prompts/PER_TURN_CONTEXT_TEMPLATE.md.
- ADR-002 documenting the mandatory per-turn injection contract.

### Solved
- Prevented the model operating rules from depending on session-start-only instructions.
- Defined a fresh project-context snapshot for every model turn.
- Made memory recovery a repeatable runtime contract rather than only a documentation procedure.

### Current State
STAGE-001 remains active. LOOP-002 is active. The runtime context builder/middleware has not yet been implemented.

### Next
Implement runtime enforcement so every model invocation receives MODEL_PRESET + FRESH_PROJECT_CONTEXT + CURRENT_TASK.

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
