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
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 1: /codexspec.review-spec ★                        ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Spec to Plan  ──►  Create technical plan                             │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 2: /codexspec.review-plan ★                        ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  5. Plan to Tasks  ─►  Generate atomic tasks                             │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ REVIEW GATE 3: /codexspec.review-tasks ★                       ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
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

## Core Commands

| Stage | Command | Purpose |
|-------|---------|---------|
| 1 | `/codexspec.constitution` | Define project principles |
| 2 | `/codexspec.specify` | Interactive Q&A for requirements |
| 3 | `/codexspec.generate-spec` | Create specification document |
| - | `/codexspec.review-spec` | ★ Validate specification |
| 4 | `/codexspec.spec-to-plan` | Create technical plan |
| - | `/codexspec.review-plan` | ★ Validate plan |
| 5 | `/codexspec.plan-to-tasks` | Break down into tasks |
| - | `/codexspec.review-tasks` | ★ Validate tasks |
| 6 | `/codexspec.implement-tasks` | Execute implementation |

## Two-Phase Specification

### specify vs clarify

| Aspect | `/codexspec.specify` | `/codexspec.clarify` |
|--------|----------------------|----------------------|
| **Purpose** | Initial exploration | Iterative refinement |
| **When** | No spec.md exists | spec.md exists, needs gaps filled |
| **Input** | Your initial idea | Existing spec.md |
| **Output** | None (dialogue only) | Updates spec.md |

## Conditional TDD

Implementation follows conditional TDD:

- **Code tasks**: Test-first (Red → Green → Verify → Refactor)
- **Non-testable tasks** (docs, config): Direct implementation
