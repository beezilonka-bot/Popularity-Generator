# Popularity-Generator Architecture

## 1. Core Principle

The project separates five concerns:

1. **Identity** — what project/version is running.
2. **Preset** — rules the model must receive every turn.
3. **World Book** — decides what dynamic context is relevant to the current task.
4. **Skills** — reusable methods that change how work is performed.
5. **Resources** — external/internal material used as evidence, reference, examples, or implementation support.

They must not duplicate each other.

## 2. Runtime Context Flow

```text
PROJECT_ID + RELEASE_VERSION
        |
        v
MODEL_PRESET
        |
        v
FRESH_PROJECT_CONTEXT
        |
        v
WORLD_BOOK MATCHING
        |
        +--> relevant SKILL IDs
        |
        +--> relevant RESOURCE IDs
        |
        +--> relevant STYLE / CONSTRAINT entries
        |
        v
RELEVANT_CONTEXT
        |
        v
CURRENT_TASK
```

The runtime should select data, not rewrite the data layer.

## 3. Responsibility Boundaries

### Project Identity
Source: `project.yaml`

Contains stable project identity and current release/stage pointers.

Does not contain skill text, world-book entries, or research notes.

### Version
The repository release version describes changes to the software/project architecture.

Entry-level updates are tracked by their own IDs and update metadata; they do not create a new project release for every text edit.

### Preset
Source: `prompts/`

The preset is the model's mandatory operating baseline. It is included every turn.

Preset answers: **"How must the model work?"**

It must not contain large domain knowledge or a large skill library.

### World Book
Source: `worldbook/`

The World Book is a routing/index layer.

It answers: **"Which context should be loaded for this task?"**

It should contain triggers, conditions, priority, references, and small activation instructions. Large knowledge belongs elsewhere.

### Skill Library
Source: `skills/`

A skill is a reusable procedure, heuristic, checklist, decision process, or writing method.

It answers: **"How should this task be performed?"**

Skills should be independently addressable and composable.

### Resource Library
Source: `resources/`

A resource is supporting material: source URLs, repositories, documentation, research notes, examples, datasets, or internal reference material.

It answers: **"What material can support the work?"**

Resources are not automatically trusted facts. Their provenance and status must be explicit.

## 4. ID Model

IDs are permanent and never reused.

| Entity | Format | Example | Purpose |
|---|---|---|---|
| Project | `PG` | `PG` | Project identity |
| Release | `vMAJOR.MINOR.PATCH` | `v0.1.2` | Project/repository change |
| Stage | `STAGE-NNN` | `STAGE-001` | Lifecycle phase |
| Module | `MOD-NNN` | `MOD-011` | Stable capability |
| Loop | `LOOP-NNN` | `LOOP-003` | End-to-end workflow |
| Preset | `PRESET-NNN` | `PRESET-001` | Stable model operating profile |
| World Book | `WB-NNN` / domain form | `WB-X-001` | Triggered context entry |
| Skill | `SKILL-<DOMAIN>-NNN` | `SKILL-X-001` | Reusable method |
| Resource | `RES-<DOMAIN>-NNN` | `RES-WI-001` | Supporting resource |
| ADR | `ADR-NNN` | `ADR-003` | Architecture decision |

A domain suffix is descriptive, not a new versioning system.

## 5. Three-Layer Data Model

Every reusable item should fit into one of three layers:

### Layer A — Always-On
Small, stable instructions.

- model preset;
- critical safety/integrity rules;
- minimal project identity.

### Layer B — Triggered
Loaded only when a task needs it.

- World Book entries;
- relevant skills;
- style rules;
- hard constraints;
- resource pointers.

### Layer C — On-Demand
Fetched only when execution needs the underlying material.

- long documents;
- external web pages;
- repositories;
- large examples;
- datasets;
- historical research.

This prevents prompt bloat.

## 6. Retrieval Priority

The default resolution strategy is:

1. exact keyword/alias;
2. structured filters;
3. priority/specificity;
4. skill/resource references;
5. bounded recursive activation;
6. optional fuzzy/semantic retrieval;
7. on-demand resource fetch.

Cheap deterministic retrieval is the default. Expensive retrieval is a fallback.

## 7. Context Budget

Do not optimize for the maximum amount of context loaded.

Optimize for the minimum context that materially changes the result.

The runtime should track:

- selected entry count;
- estimated tokens;
- priority;
- trigger reason;
- skill IDs;
- resource IDs;
- omitted candidates when useful for debugging.

## 8. Source-of-Truth Rules

- Project identity/current pointers → `project.yaml` + `PROJECT_STATE.md`
- Global entity index → `REGISTRY.yaml`
- Model behavior → `prompts/`
- Trigger routing → `worldbook/`
- Reusable methods → `skills/`
- Supporting material → `resources/`
- History → `CHANGELOG.md` + `docs/releases/`
- Architectural rationale → `docs/decisions/`

If two layers contain the same fact, one is redundant and should be removed or converted into a reference.

## 9. Growth Rule

Adding more knowledge must not increase every model turn's prompt size.

Growth happens mainly in Layer B and Layer C. The always-on preset stays small and stable.

## 10. Current Project Direction

The current implementation remains in STAGE-001.

The next engineering task is to implement the runtime resolver that composes:

```text
PRESET
+ PROJECT STATE
+ MATCHED WORLD BOOK
+ RESOLVED SKILLS
+ RESOLVED RESOURCE POINTERS
+ CURRENT TASK
```

No content-generation engine should be coupled to these storage concerns.
