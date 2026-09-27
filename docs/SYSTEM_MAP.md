# System Map

## One Sentence

**Preset defines how the model works; World Book decides what to load; Skills define how to perform a task; Resources provide supporting material; Project/Version records define what system state is active.**

## Component Relationship

```text
                         PROJECT PG
                             |
                     RELEASE v0.1.2
                             |
               +-------------+-------------+
               |                           |
        PROJECT STATE                 REGISTRY
               |                           |
               +-------------+-------------+
                             |
                       MODEL PRESET
                       PRESET-001
                             |
                             v
                       WORLD BOOK
                             |
             +---------------+---------------+
             |               |               |
           SKILLS          RESOURCES      CONSTRAINTS
             |               |
             +-------+-------+
                     |
               CURRENT TASK
                     |
                     v
              MODEL EXECUTION
```

## Separation Rules

**Preset**
- always loaded;
- small;
- stable.

**World Book**
- triggered;
- selective;
- routing-focused.

**Skill**
- procedural;
- reusable;
- task-specific.

**Resource**
- supportive;
- source-backed;
- on-demand where possible.

**Project/Version**
- identity/state;
- not writing guidance.

## Why this structure

The system can grow horizontally without making the model read everything.

For example, adding 100 new X skills should mostly add 100 indexed entries. It should not enlarge the always-on preset or the base project context.

The World Book is the bridge between a large library and a small runtime context.
