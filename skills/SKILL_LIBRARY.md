# Skill Library — X Content Generation

## Purpose
A curated, normalized library of reusable skills for producing high-quality X posts and threads.

This library is **not** a dump of external repositories. External material is research input. We extract principles, workflows, constraints, and patterns, then rewrite them into project-owned operational guidance.

## Research Sources
The first research pass inspected open-source X/social-writing skills and prompt collections, including:
- majiayu000/claude-skill-registry-data — writing-x-posts
- AR-92/zod-plugins — tweet-writer
- AutonoLabs/content-engine-final — X prompt
- itechmeat/llm-code — social-writer
- xu-xiang/awesome-top-skills — social-media skill index

These sources commonly emphasize hooks, brevity, one-idea-per-post, platform-specific formatting, niche research, anti-generic writing, and pre-publication checks. Individual repositories contain claims about algorithm behavior that may be outdated or insufficiently evidenced; such claims are not automatically treated as project facts.

## Library Design
Skills are split into small, composable units instead of one giant prompt.

### Core Skill IDs
- SKILL-X-001 — X Post Fundamentals
- SKILL-X-002 — Hook Engineering
- SKILL-X-003 — Thread Architecture
- SKILL-X-004 — Voice & Anti-AI Writing
- SKILL-X-005 — Specificity & Evidence
- SKILL-X-006 — Content Pattern Selection
- SKILL-X-007 — Research-to-Post Workflow
- SKILL-X-008 — Editing & Compression
- SKILL-X-009 — Quality Gate
- SKILL-X-010 — Content Repurposing

## Operating Principle
Load only the skills relevant to the current task. Do not inject the entire library into every model turn.

The per-turn preset remains mandatory. The skill resolver selects a minimal skill bundle after task classification.

## Research Discipline
For external examples:
1. Identify the source repository and file.
2. Extract reusable method, not identity or unsupported claims.
3. Separate observed pattern from causal claim.
4. Prefer multiple independent sources for a technique.
5. Preserve source attribution in research records.
6. Do not copy long passages or proprietary text into the library.
7. Update skills when evidence or platform behavior changes.

## Anti-Bloat Rule
A skill should exist only if it changes model behavior in a repeatable way.

Reject:
- generic motivational advice,
- duplicated prompt text,
- unsupported algorithm folklore,
- long examples that add no reusable rule,
- platform claims without a source/date,
- code that exists only to wrap static text.

Prefer:
- short operational rules,
- decision trees,
- checklists,
- reusable templates,
- measurable constraints,
- explicit inputs/outputs,
- source-backed research notes.

## Resolution Pipeline
CURRENT_TASK
→ classify content task
→ select relevant SKILL-* IDs
→ load only those skills
→ generate
→ run quality gate
→ return output
