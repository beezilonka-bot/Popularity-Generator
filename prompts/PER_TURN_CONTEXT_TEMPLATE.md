# PER-TURN CONTEXT TEMPLATE

This template defines the context package that the runtime must construct for **every** model invocation.

## Required Package

```text
=== MODEL_PRESET ===
<exact contents of prompts/MODEL_PRESET.md>

=== FRESH_PROJECT_CONTEXT ===
Project: <from PROJECT_STATE.md>
Version: <current version>
Active Stage: <active stage ID and name>
Active Loop: <active loop ID and name>
Current Status: <current status>
In Progress: <current in-progress items>
Relevant Modules: <resolved module IDs>
Relevant Decisions: <resolved ADR IDs>
Relevant Release History: <resolved release record(s)>
Current Constraints: <documented constraints relevant to this task>
Next Documented Action: <next action from current state>

=== CURRENT_TASK ===
<current user/task input>
```

## Construction Rules
- The preset is always included verbatim.
- The project context is refreshed for every turn.
- Only task-relevant records should be included beyond the core state/registry.
- Do not carry forward stale dynamic context from a previous turn.
- If a field cannot be established from repository records, write `UNKNOWN`.
- Do not invent missing values.

## Minimum Recovery Snapshot
At minimum, every turn must contain:
- project identity,
- current version,
- active stage,
- active loop,
- current status,
- in-progress work,
- relevant IDs,
- documented constraints,
- next documented action.

## Runtime Requirement
The eventual model adapter/middleware must construct this package before each model request. Loading it once at application startup is insufficient.
