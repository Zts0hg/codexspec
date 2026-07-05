<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# Welcome to CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A Requirements-First SDD toolkit for Claude Code**

CodexSpec helps you build high-quality software through **Requirements-First Spec-Driven Development (SDD)** — confirmed requirements are the highest-priority authority, and nothing is binding until you explicitly confirm it. Instead of jumping straight to code, you confirm **what** to build and **why** before deciding **how** to build it.

## Why CodexSpec?

Why use CodexSpec on top of Claude Code? Here's the comparison:

| Aspect | Claude Code Only | CodexSpec + Claude Code |
|--------|------------------|-------------------------|
| **Multi-language Support** | Default English interaction | Configure team language for smoother collaboration and reviews |
| **Traceability** | Hard to trace decisions after session ends | All specs, plans, and tasks saved in `.codexspec/specs/` |
| **Session Recovery** | Plan mode interruptions are hard to recover from | Multi-command split + persisted docs = easy recovery |
| **Team Governance** | No unified principles, inconsistent styles | `constitution.md` enforces team standards and quality |

### What is Requirements-First SDD?

**Requirements-First SDD** is the Spec-Driven Development (SDD) methodology with one upgrade: **confirmed requirements are the highest-priority authority**. You define and confirm *what* to build and *why* before deciding *how* — and nothing becomes binding until you explicitly confirm it.

```
Traditional:  Idea → Code → Debug → Rewrite
SDD:          Idea → Confirmed Requirements → Spec → Plan → Tasks → Code
```

### Key Features

- **Constitution-Based Development** - Establish project principles that guide all decisions
- **Persistent Requirement Capture** - `/specify` records confirmed discussion in `requirements.md` before document generation
- **Automatic Reviews** - Every generated spec, plan, and task artifact includes built-in quality checks
- **Interactive Clarification** - Q&A-based requirement refinement
- **Cross-Artifact Analysis** - Detect inconsistencies before implementation
- **Traceable Tasks** - Task breakdowns preserve requirement and plan coverage, applying **Conditional TDD** (test-first ordering only where plan, constitution, or risk requires; non-testable tasks like docs/config are implemented directly)
- **Native Claude Code Integration** - Slash commands work seamlessly
- **Multi-Language Support** - 13+ languages via LLM dynamic translation
- **Cross-Platform** - Bash and PowerShell scripts included
- **Extensible** - Plugin architecture for custom commands

## Quick Start

```bash
# Install
uv tool install codexspec

# Create a new project
codexspec init my-project

# Or initialize in existing project
codexspec init . --ai claude
```

[Full Installation Guide](getting-started/installation.md)

## Workflow Overview

CodexSpec structures development into **reviewable checkpoints**. Confirmed requirements flow through specs, plans, and tasks into code, with a review at every stage.

```
Idea → Confirmed Requirements → Spec → Plan → Tasks → Code
```

Every artifact is produced by a dedicated command and validated before the next stage begins:

```
Idea → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                   │                         │                            │
                                              Review spec               Review plan                  Review tasks
```

### The Confirmation Gate

The defining differentiator is the **Confirmation Gate**: requirements, specs, plans, and tasks become binding only after your explicit human confirmation. Confirmed requirements are the highest-priority feature authority, so AI cannot silently lock in decisions — derived artifacts carry explicit source links, and conflicts get traced back instead of propagated.

### Iterative Quality Loop

Every generation command includes an **automatic, evidence-based review**: defects require concrete evidence, advisory suggestions never trigger automatic changes, and verified defects may be fixed and re-reviewed for at most two rounds. This loop keeps quality rising without you babysitting every detail.

[Learn the Workflow](user-guide/workflow.md)

## License

MIT License - see [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) for details.
