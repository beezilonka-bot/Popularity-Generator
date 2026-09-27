# Skills Library

The project skill library is modular and task-routed.

## How the Model Uses It
The model does NOT load every skill on every turn.

Per turn:
1. Receive MODEL_PRESET.
2. Receive fresh project context.
3. Classify the task.
4. Resolve the smallest useful skill bundle.
5. Execute.
6. Run the relevant quality gate.

## Skill Categories
- `skills/x/` — X writing and content generation
- Future categories may cover research, trend analysis, publishing, analytics, and feedback learning.

## Source Policy
External repositories are research sources. Their methods are evaluated, normalized, and rewritten into project-owned skills. Do not blindly copy external prompts or unverified platform folklore.
