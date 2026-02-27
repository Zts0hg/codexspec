---
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md
scripts:
  sh: .codexspec/scripts/check-prerequisites.sh --json --require-tasks --include-tasks
  ps: .codexspec/scripts/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
---

# Cross-Artifact Analyzer

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This command MUST run only after `/codexspec.plan-to-tasks` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report only.

**Constitution Authority**: The project constitution (`.codexspec/memory/constitution.md`) is **non-negotiable**. Constitution conflicts are automatically CRITICAL.

## Execution Steps

### 1. Initialize Analysis Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - Feature directory path
- `AVAILABLE_DOCS` - List of available documents

Derive absolute paths:
- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort if any required file is missing.

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context:

**From spec.md:**
- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases

**From plan.md:**
- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**
- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution:**
- Load `.codexspec/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations:
- **Requirements inventory**: Each requirement with a stable key
- **User story inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to requirements or stories
- **Constitution rule set**: Extract MUST/SHOULD normative statements

### 4. Detection Passes

#### A. Duplication Detection
- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection
- Flag vague adjectives (fast, scalable, secure) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???)

#### C. Underspecification
- Requirements with verbs but missing measurable outcome
- User stories missing acceptance criteria
- Tasks referencing undefined components

#### D. Constitution Alignment
- Requirements conflicting with MUST principles
- Missing mandated sections or quality gates

#### E. Coverage Gaps
- Requirements with zero associated tasks
- Tasks with no mapped requirement
- Non-functional requirements not reflected in tasks

#### F. Inconsistency
- Terminology drift
- Data entities referenced but not defined
- Task ordering contradictions
- Conflicting requirements

### 5. Severity Assignment

- **CRITICAL**: Violates constitution MUST, missing core artifact, requirement with zero coverage
- **HIGH**: Duplicate/conflicting requirement, ambiguous security attribute
- **MEDIUM**: Terminology drift, missing non-functional task coverage
- **LOW**: Style/wording improvements

### 6. Produce Analysis Report

```markdown
## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120 | Two similar requirements | Merge phrasing |

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

**Metrics:**
- Total Requirements
- Total Tasks
- Coverage % (requirements with >=1 task)
- Critical Issues Count
```

### 7. Next Actions

- If CRITICAL issues: Recommend resolving before `/codexspec.implement-tasks`
- If only LOW/MEDIUM: User may proceed with improvement suggestions
- Provide explicit command suggestions

### 8. Offer Remediation

Ask: "Would you like me to suggest concrete remediation edits?" (Do NOT apply automatically)

## Operating Principles

- **Minimal high-signal tokens**: Focus on actionable findings
- **NEVER modify files** (read-only analysis)
- **Prioritize constitution violations** (always CRITICAL)
- **Report zero issues gracefully** (emit success report with coverage statistics)

> [!NOTE]
> This command runs AFTER `/codexspec.plan-to-tasks` and BEFORE `/codexspec.implement-tasks`.
