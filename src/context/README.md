# Context Runtime

The runtime context layer converts repository catalogs into a per-turn package.

## Contract

```text
MODEL_PRESET
+ FRESH_PROJECT_CONTEXT
+ RELEVANT_WORLD_BOOK
+ CURRENT_TASK
```

World Book resolution is deterministic and local:

1. load registry;
2. scan exact keywords and aliases;
3. score by priority and trigger specificity;
4. deduplicate;
5. enforce entry count and token budget;
6. expose activation trace;
7. return Skill and Resource IDs.

Semantic retrieval is intentionally not implemented in this first version. It can be added later if keyword routing demonstrates a measurable gap.

## Run

```bash
pip install -r requirements.txt
pytest -q
```
