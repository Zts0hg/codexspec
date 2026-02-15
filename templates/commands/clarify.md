---
description: Identify underspecified areas in the current feature spec by asking targeted clarification questions and encoding answers back into the spec
handoffs:
  - agent: claude
    step: Ask clarification questions and update spec
scripts:
   sh: .codexspec/scripts/check-prerequisites.sh --json --paths-only
   ps: .codexspec/scripts/check-prerequisites.ps1 -Json -PathsOnly
---

# Specification Clarifier

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Goal

Detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

Note: This clarification workflow is expected to run (and be completed) BEFORE invoking `/codexspec.spec-to-plan`. If the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

## Execution Steps

### 1. Initialize Context

Run `{SCRIPT}` from repo root and parse JSON for:
- `FEATURE_DIR` - The feature directory path
- `FEATURE_SPEC` - Path to spec.md

If parsing fails, abort and instruct user to run `/codexspec.specify` first.

### 2. Load Specification

Load the current spec file from `FEATURE_SPEC`. Perform a structured ambiguity & coverage scan using this taxonomy:

**Functional Scope & Behavior:**
- Core user goals & success criteria
- Explicit out-of-scope declarations
- User roles / personas differentiation

**Domain & Data Model:**
- Entities, attributes, relationships
- Identity & uniqueness rules
- Lifecycle/state transitions

**Interaction & UX Flow:**
- Critical user journeys / sequences
- Error/empty/loading states
- Accessibility requirements

**Non-Functional Quality Attributes:**
- Performance targets
- Scalability considerations
- Security & privacy requirements

**Edge Cases & Failure Handling:**
- Negative scenarios
- Rate limiting / throttling
- Conflict resolution

### 3. Generate Clarification Questions

Generate a prioritized queue of candidate clarification questions (maximum 5). Constraints:
- Each question must be answerable with multiple-choice (2-5 options) OR a short answer (≤5 words)
- Only include questions whose answers materially impact architecture or implementation
- Ensure category coverage balance
- Favor clarifications that reduce downstream rework risk

### 4. Sequential Questioning Loop

Present EXACTLY ONE question at a time:

For multiple-choice questions:
```
**Recommended:** Option [X] - <reasoning>

| Option | Description |
|--------|-------------|
| A | <Option A description> |
| B | <Option B description> |
| Short | Provide a different short answer |
```

For short-answer style:
```
**Suggested:** <proposed answer> - <brief reasoning>
Format: Short answer (<=5 words).
```

### 5. Integration After Each Answer

After each accepted answer:
1. Ensure a `## Clarifications` section exists in the spec
2. Create `### Session YYYY-MM-DD` subheading for today
3. Append: `- Q: <question> → A: <final answer>`
4. Apply the clarification to appropriate sections (Functional Requirements, Data Model, etc.)
5. Save the spec file immediately

### 6. Completion Report

Report:
- Number of questions asked & answered
- Path to updated spec
- Sections touched
- Coverage summary
- Suggested next command

## Behavior Rules

- If no meaningful ambiguities found: "No critical ambiguities detected."
- Never exceed 5 total questions
- Respect user early termination signals ("stop", "done", "proceed")
- If quota reached with unresolved high-impact categories, flag them under Deferred

> [!NOTE]
> This command is designed to run BEFORE `/codexspec.spec-to-plan`.
