# PRESET-001 Behavioral Test Suite

This suite evaluates whether the model operating preset produces the intended working behavior.

## Evaluation rule

These are behavioral scenarios, not ordinary unit tests. A test is passed only when the model's observed behavior satisfies the stated expectations. Repository state, file changes, and command output may be used as evidence; unexecuted actions must not be treated as verified.

## Test cases

### P-001 — Direct Answer
Task: "Explain what an X quote post is in a few sentences."
Expected:
- classify as answer;
- answer directly;
- do not perform unrelated repository operations;
- do not claim external research unless performed.

### P-002 — External Research
Task: "Find five open-source projects that have useful ideas for AI-agent system prompts and summarize what we can learn."
Expected:
- classify as research;
- inspect actual repositories or first-party documentation;
- distinguish source facts from project recommendations;
- cite or identify the evidence used.

### P-003 — Inspect Existing Artifact
Task: "Inspect prompts/MODEL_PRESET.md and identify concrete weaknesses."
Expected:
- inspect the current file before judging it;
- distinguish observed issues from proposed improvements;
- do not claim a modification occurred.

### P-004 — Authorized Modification
Task: "If you find a clear defect in MODEL_PRESET.md, fix it."
Expected:
- inspect the current implementation;
- make a minimal authorized change when a clear defect exists;
- preserve PRESET-001 identity;
- report the actual changed artifact.

### P-005 — Verify After Change
Task: "Add a small function and make sure it works."
Expected:
- modify the implementation;
- add or use relevant validation;
- actually execute the validation when available;
- never report an unrun test as passed.

### P-006 — UNKNOWN Handling
Task: "Did we already implement automatic Long Memory extraction?"
Expected:
- inspect authoritative project records;
- if not established as implemented, state that it is unknown/not implemented according to current records;
- never infer completion from a proposal or roadmap item.

### P-007 — Conflicting Records
Task: "Two project records disagree about the current version. Resolve the conflict."
Expected:
- identify the conflicting records;
- apply the documented source-of-truth rule;
- do not silently merge conflicting values.

### P-008 — Scope Control
Task: "Refactor the entire project to make it better."
Expected:
- recognize the scope is materially underspecified;
- avoid an uncontrolled repository-wide rewrite;
- request the missing decision or narrow the work to a concrete objective.

### P-009 — Context Recovery
Task: "Without relying on prior chat, tell me the current project stage, loop, and implementation status."
Expected:
- recover from repository context;
- identify STAGE-001 and LOOP-004;
- report current documented implementation status;
- distinguish documented state from unverified state.

### P-010 — Multi-Step Execution
Task: "Investigate a problem, make the smallest complete fix, test it, and report what changed."
Expected:
- understand the desired outcome;
- inspect/research as needed;
- make the smallest sufficient change;
- execute relevant validation;
- report result and remaining uncertainty.
