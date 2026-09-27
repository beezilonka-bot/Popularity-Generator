# AI Context Recovery

> This file is the canonical entry point for recovering project context after conversation truncation, session changes, or model changes.

## Recovery Protocol
1. Read PROJECT_STATE.md.
2. Read REGISTRY.yaml.
3. Identify the active STAGE, active LOOP, and in-progress MODs.
4. Read the active STAGE document and only the referenced module/loop documents needed for the current task.
5. Read the latest relevant release log and ADRs referenced by the active module.
6. Do not infer missing history. If the repository does not document a fact, mark it as unknown.

## Mandatory Per-Turn Injection
The model preset at prompts/MODEL_PRESET.md MUST be injected on every model turn.

Every turn MUST also receive a fresh project-context snapshot built from the authoritative repository records. A previous turn's snapshot is stale and does not satisfy this requirement.

Required order:

MODEL_PRESET → FRESH_PROJECT_CONTEXT → CURRENT_TASK

## Source-of-Truth Rules
- Current state: PROJECT_STATE.md
- Entity index: REGISTRY.yaml
- Historical changes: CHANGELOG.md and docs/releases/
- Stage scope: docs/stages/
- Module definitions: docs/modules/
- Loop definitions: docs/loops/
- Architecture decisions: docs/decisions/
- Model operating rules: prompts/MODEL_PRESET.md
- Per-turn package contract: prompts/PER_TURN_CONTEXT_TEMPLATE.md

## Update Rule
Any completed stage, module, loop, release, or architecture decision must update the relevant state/index/log records in the same change set.

## Current Recovery Target
See PROJECT_STATE.md, then follow LOOP-002 when constructing a model turn.
