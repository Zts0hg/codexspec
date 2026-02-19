# Welcome to CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A Spec-Driven Development (SDD) toolkit for Claude Code**

CodexSpec is a toolkit that helps you build high-quality software using a structured, specification-driven approach. It flips the script on traditional development by making specifications executable artifacts that directly guide implementation.

## Why CodexSpec?

### Human-AI Collaboration

CodexSpec is built on the belief that **effective AI-assisted development requires active human participation at every stage**.

| Problem | Solution |
|---------|----------|
| Unclear requirements | Interactive Q&A to clarify before building |
| Incomplete specifications | Dedicated review commands with scoring |
| Misaligned technical plans | Constitution-based validation |
| Vague task breakdowns | TDD-enforced task generation |

### Key Features

- **Constitution-Based** - Establish project principles that guide all decisions
- **Interactive Clarification** - Q&A-based requirement refinement
- **Review Commands** - Validate artifacts at each stage
- **TDD-Ready** - Test-first methodology built into tasks
- **i18n Support** - 13+ languages via LLM translation

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

```
Idea -> Clarify -> Review -> Plan -> Review -> Tasks -> Review -> Implement
            ^              ^              ^
         Human checks    Human checks    Human checks
```

Every artifact has a corresponding review command to validate AI output before proceeding.

[Learn the Workflow](user-guide/workflow.md)

## License

MIT License - see [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE) for details.
