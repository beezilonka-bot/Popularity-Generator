# Project Memory

Long-lived project knowledge belongs here when it is not better represented by state, registry, stage/module/loop definitions, release logs, or ADRs.

Do not store secrets or credentials here.

## Long Memory

Long Memory is a separate runtime context source. It stores durable facts learned from prior work or conversations; it is not a copy of chat history and it does not replace World Book entries.

Lifecycle:

`EPHEMERAL → CANDIDATE → LONG_MEMORY`

Only durable, reusable information should be promoted.
