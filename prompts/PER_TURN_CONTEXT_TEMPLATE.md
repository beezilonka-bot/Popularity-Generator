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

=== RELEVANT_WORLD_BOOK ===
Activation Trace: <entry IDs + matched triggers + selection reasons>
Selected Entries: <minimal entry contents>
Resolved Skills: <skill IDs only unless full text is required>
Resolved Resources: <resource IDs/links>
Budget: <used>/<configured token budget>

=== CURRENT_TASK ===
<current user/task input>
```

## Construction Rules

- The preset is always included verbatim.
- Project context is refreshed for every turn.
- World Book resolution is performed for every turn.
- Only task-relevant records should be included beyond the core state/registry.
- Do not carry forward stale dynamic context from a previous turn.
- If no World Book entry matches, write `NONE`.
- If a field cannot be established from repository records, write `UNKNOWN`.
- Do not invent missing values.

## World Book Resolution Order

1. Exact keywords and aliases.
2. Optional regex rules.
3. Optional filters and exclusions.
4. Priority/specificity ranking.
5. Deduplication.
6. Bounded recursive activation.
7. Token-budget enforcement.
8. Final trace and injection.

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
