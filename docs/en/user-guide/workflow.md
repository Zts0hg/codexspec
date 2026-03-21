# Workflow

CodexSpec structures development into **reviewable checkpoints** with human validation at each stage.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec Human-AI Collaboration Workflow             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  Define project principles                         │
│         │                                                                │
│         ▼                                                                │
│  2. Specify  ───────►  Interactive Q&A to clarify requirements           │
│         │                                                                │
│         ▼                                                                │
│  3. Generate Spec  ─►  Create spec.md document                           │
│         │               ✓ Auto Review: generates review-spec.md          │
│         ▼                                                                │
│  4. Spec to Plan  ──►  Create technical plan                             │
│         │               ✓ Auto Review: generates review-plan.md          │
│         ▼                                                                │
│  5. Plan to Tasks  ─►  Generate atomic tasks                             │
│         │               ✓ Auto Review: generates review-tasks.md         │
│         ▼                                                                │
│  6. Implement  ─────►  Execute with conditional TDD workflow             │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## Why Review Matters

| Without Review | With Review |
|---------------|-------------|
| AI makes incorrect assumptions | Human catches misinterpretations early |
| Incomplete requirements propagate | Gaps identified before implementation |
| Architecture drifts from intent | Alignment verified at each stage |
| **Result: Rework** | **Result: Right first time** |

## Auto Review

Each generation command now **automatically runs a review**:

- `/codexspec:generate-spec` → automatically invokes `review-spec`
- `/codexspec:spec-to-plan` → automatically invokes `review-plan`
- `/codexspec:plan-to-tasks` → automatically invokes `review-tasks`

Review reports are generated alongside artifacts, allowing you to immediately see issues.

## Iterative Quality Loop

When issues are found in review reports, describe fixes in natural language and the system will update both the artifact and report:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Iterative Quality Loop                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Artifact (spec/plan/tasks.md)                                        │
│         │                                                             │
│         ▼                                                             │
│  Auto Review  ──────►  Review Report (review-*.md)                    │
│         │                      │                                      │
│         │                      ▼                                      │
│         │               Issues found?                                 │
│         │                      │                                      │
│         │                ┌─────┴─────┐                                │
│         │                │           │                                │
│         │               Yes         No                                │
│         │                │           │                                │
│         │                ▼           ▼                                │
│         │      Describe fix in   Continue to                          │
│         │      conversation       next step                           │
│         │                │                                            │
│         │                ▼                                            │
│         │      Simultaneously update:                                 │
│         │        • Artifact (spec/plan/tasks.md)                      │
│         │        • Review report (review-*.md)                        │
│         │                │                                            │
│         └────────────────┘                                            │
│              (Repeat until satisfied)                                 │
│                                                                       │
│  Manual Re-review: Run /codexspec:review-* anytime for fresh analysis │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

**How it works**:

1. **Auto Review**: Each generation command automatically runs the corresponding review
2. **Review Report**: Generates `review-*.md` files containing issues found
3. **Iterative Fix**: Describe what needs fixing in conversation, artifact and report update together
4. **Manual Re-review**: Run `/codexspec:review-spec|plan|tasks` anytime for a fresh analysis

## Core Commands

| Stage | Command | Purpose |
|-------|---------|---------|
| 1 | `/codexspec:constitution` | Define project principles |
| 2 | `/codexspec:specify` | Interactive Q&A for requirements |
| 3 | `/codexspec:generate-spec` | Create specification document (★ Auto Review) |
| - | `/codexspec:review-spec` | Auto-invoked, or manually re-validate |
| 4 | `/codexspec:spec-to-plan` | Create technical plan (★ Auto Review) |
| - | `/codexspec:review-plan` | Auto-invoked, or manually re-validate |
| 5 | `/codexspec:plan-to-tasks` | Break down into tasks (★ Auto Review) |
| - | `/codexspec:review-tasks` | Auto-invoked, or manually re-validate |
| 6 | `/codexspec:implement-tasks` | Execute implementation |

## Two-Phase Specification

### specify vs clarify

| Aspect | `/codexspec:specify` | `/codexspec:clarify` |
|--------|----------------------|----------------------|
| **Purpose** | Initial exploration | Iterative refinement |
| **When** | No spec.md exists | spec.md exists, needs gaps filled |
| **Input** | Your initial idea | Existing spec.md |
| **Output** | None (dialogue only) | Updates spec.md |

## Conditional TDD

Implementation follows conditional TDD:

- **Code tasks**: Test-first (Red → Green → Verify → Refactor)
- **Non-testable tasks** (docs, config): Direct implementation
