# CLAUDE.md - CodexSpec Development Guide

This document provides comprehensive context and guidelines for Claude Code when working on the CodexSpec project itself.

## Project Overview

**CodexSpec** is a Spec-Driven Development (SDD) toolkit for Claude Code. It is a Python CLI tool that can be installed via `uv tool install` and provides structured slash commands for AI-assisted software development.

### Purpose

CodexSpec helps developers:
- Establish project principles through a constitution
- Create detailed specifications focused on "what" and "why"
- Generate technical implementation plans
- Break down plans into actionable tasks
- Execute implementations systematically
- Validate quality through checklists and analysis

### Technology Stack

- **Language**: Python 3.11+
- **CLI Framework**: Typer (with Rich for formatting)
- **Package Manager**: uv
- **Build System**: Hatchling
- **Testing**: pytest
- **Linting**: ruff

## Project Structure

```
codexspec/
├── src/
│   └── codexspec/
│       ├── __init__.py        # Main CLI implementation
│       └── i18n.py            # Internationalization utilities
├── templates/
│   └── commands/              # Slash command templates
│       ├── constitution.md
│       ├── specify.md
│       ├── clarify.md         # NEW
│       ├── analyze.md         # NEW
│       ├── checklist.md       # NEW
│       ├── generate-spec.md
│       ├── spec-to-plan.md
│       ├── plan-to-tasks.md
│       ├── review-spec.md
│       ├── review-plan.md
│       ├── review-tasks.md
│       ├── implement-tasks.md
│       └── tasks-to-issues.md # NEW
├── scripts/
│   ├── bash/                  # Bash helper scripts
│   └── powershell/            # PowerShell scripts (NEW)
├── extensions/                # Extension system (NEW)
│   ├── catalog.json
│   ├── EXTENSION-DEVELOPMENT-GUIDE.md
│   └── template/
│       ├── extension.yml
│       └── commands/example.md
├── pyproject.toml             # Project configuration
├── README.md                  # User documentation
└── CLAUDE.md                  # This file
```

## Architecture

### CLI Architecture

The CLI is built using Typer and follows a modular structure:

```python
# Main entry point
app = typer.Typer(
    name="codexspec",
    help="CodexSpec - A Spec-Driven Development (SDD) toolkit for Claude Code",
)

# Commands
@app.command()
def init(...): ...

@app.command()
def check(...): ...

@app.command()
def version(...): ...

@app.command()
def config(...): ...  # NEW: Configuration management
```

### Internationalization (i18n) Architecture

CodexSpec uses **LLM-based dynamic translation** for internationalization instead of maintaining multiple template translations.

**Core Concept**: Keep templates in English, let Claude translate at runtime based on user's language preference.

**Implementation**:
1. `src/codexspec/i18n.py` - Language utilities (normalization, validation)
2. `.codexspec/config.yml` - Per-project language configuration
3. Template `## Language Preference` section - Instructs Claude to check config

**Language Configuration**:
```yaml
# .codexspec/config.yml
version: "1.0"
language:
  output: "zh-CN"  # Output language
  commit: "zh-CN"  # Commit message language (defaults to output)
  templates: "en"  # Always "en"
project:
  ai: "claude"
  created: "2025-02-15"
```

**Template Pattern**:
```markdown
## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
```

**Benefits**:
- Zero translation maintenance overhead
- Template updates benefit all languages immediately
- Context-aware translations via Claude
- Supports any language Claude understands

### Constitution Language

The `constitution.md` file is generated in the language specified by `language.output` configuration. This is an intentional design decision:

- Claude can understand constitution files in any major language (English, Chinese, Japanese, Korean, etc.)
- A single file avoids synchronization issues between multiple language versions
- Teams should use a consistent working language for collaboration

**Design Rationale**:
1. Prevents content inconsistency across multiple file versions
2. Claude and other major AI models have sufficient multilingual understanding capabilities
3. Reduces maintenance overhead by eliminating the need to manage multiple translations

If an English reference version is needed for international teams, a manual translation copy can be created.

### Slash Command System

Slash commands are Markdown files with YAML frontmatter:

```yaml
---
description: Command description
handoffs:
  - agent: claude
    step: Description of what the agent should do
---

# Command Title

## User Input
$ARGUMENTS

## Instructions
...
```

### Template Processing

When `codexspec init` is run:
1. Creates `.codexspec/` directory structure
2. Creates `.claude/commands/` directory
3. Copies slash command templates
4. Creates default constitution
5. Creates project CLAUDE.md
6. Copies helper scripts (bash and powershell)
7. Initializes git (optional)

## Available Slash Commands

### Core Commands (9)

| Command | Description |
|---------|-------------|
| `/codexspec.constitution` | Create/update project constitution |
| `/codexspec.specify` | Create feature specification |
| `/codexspec.generate-spec` | Generate detailed spec from requirements |
| `/codexspec.spec-to-plan` | Convert spec to technical plan |
| `/codexspec.plan-to-tasks` | Break down plan into tasks |
| `/codexspec.review-spec` | Review specification |
| `/codexspec.review-plan` | Review technical plan |
| `/codexspec.review-tasks` | Review task breakdown |
| `/codexspec.implement-tasks` | Execute implementation |

### Enhanced Commands (4) - NEW

| Command | Description |
|---------|-------------|
| `/codexspec.clarify` | Ask clarification questions before planning |
| `/codexspec.analyze` | Cross-artifact consistency analysis |
| `/codexspec.checklist` | Generate requirements quality checklists |
| `/codexspec.tasks-to-issues` | Convert tasks to GitHub issues |

### Git Workflow Commands

| Command | Description |
|---------|-------------|
| `/codexspec.commit` | Generate Conventional Commits messages |
| `/codexspec.commit-staged` | Generate commit from staged changes |
| `/codexspec.pr` | Generate PR/MR descriptions |

## Development Guidelines

### Code Style

- **Line Length**: 120 characters max
- **Formatting**: Follow PEP 8
- **Imports**: Use absolute imports
- **Type Hints**: Use type hints for public functions
- **Docstrings**: Use docstrings for public functions and classes

### Naming Conventions

- **CLI Commands**: lowercase with hyphens (e.g., `spec-to-plan`)
- **Python Functions**: snake_case (e.g., `get_templates_dir`)
- **Python Classes**: PascalCase (e.g., `Console`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `__version__`)

### Error Handling

- Use Typer's `Exit` for CLI errors
- Provide clear, actionable error messages
- Use Rich for formatted output

### Testing

- Write tests for all public functions
- Use pytest fixtures for common setup
- Test edge cases and error conditions

### Script Testing

Scripts are tested via pytest subprocess calls:

- **Bash scripts**: `tests/scripts/bash/`
- **PowerShell scripts**: `tests/scripts/powershell/`

Run script tests:

```bash
# All script tests
uv run pytest tests/scripts/ -v

# Bash only
uv run pytest tests/scripts/bash/ -v

# PowerShell only (requires pwsh installed)
uv run pytest tests/scripts/powershell/ -v
```

**Prerequisites for PowerShell tests:**

- Install PowerShell: https://learn.microsoft.com/powershell/
- Tests are automatically skipped if pwsh is not available

## Commands Implementation Status

| Command | Status | Notes |
|---------|--------|-------|
| `init` | ✅ Complete | Initializes project structure, supports --lang |
| `check` | ✅ Complete | Checks for installed tools |
| `version` | ✅ Complete | Displays version info |
| `config` | ✅ Complete | View/modify project configuration (NEW) |
| `/codexspec.constitution` | ✅ Template | Template complete |
| `/codexspec.specify` | ✅ Template | Template complete |
| `/codexspec.generate-spec` | ✅ Template | Template complete |
| `/codexspec.spec-to-plan` | ✅ Template | Template complete |
| `/codexspec.plan-to-tasks` | ✅ Template | Template complete |
| `/codexspec.review-spec` | ✅ Template | Template complete |
| `/codexspec.review-plan` | ✅ Template | Template complete |
| `/codexspec.review-tasks` | ✅ Template | Template complete |
| `/codexspec.implement-tasks` | ✅ Template | Template complete |
| `/codexspec.clarify` | ✅ Template | NEW - Template complete |
| `/codexspec.analyze` | ✅ Template | NEW - Template complete |
| `/codexspec.checklist` | ✅ Template | NEW - Template complete |
| `/codexspec.tasks-to-issues` | ✅ Template | NEW - Template complete |
| `/codexspec.commit` | ✅ Template | Generate commit messages |
| `/codexspec.commit-staged` | ✅ Template | Generate commit from staged |
| `/codexspec.pr` | ✅ Template | NEW - Generate PR/MR descriptions |

## Extension System

CodexSpec supports a plugin architecture for custom commands.

### Extension Structure

```
my-extension/
├── extension.yml          # Manifest
├── commands/              # Custom commands
└── README.md
```

### Extension Manifest

```yaml
schema_version: "1.0"

extension:
  id: "my-extension"
  name: "My Extension"
  version: "1.0.0"
  description: "What it does"

requires:
  codexspec_version: ">=0.1.0"

provides:
  commands:
    - name: "codexspec.my-extension.command"
      file: "commands/command.md"
      description: "Description"
```

See `extensions/EXTENSION-DEVELOPMENT-GUIDE.md` for details.

## Future Development Reference

### Multi-AI Agent Support (Not Yet Implemented)

Spec-kit supports 15+ AI agents. CodexSpec currently focuses on Claude Code but could be extended to support:

| Agent | Notes |
|-------|-------|
| Gemini CLI | Google's AI assistant |
| GitHub Copilot | VS Code integration |
| Cursor | AI-powered IDE |
| Windsurf | Codeium's IDE |
| Codex CLI | OpenAI's CLI |
| Amazon Q Developer | AWS AI assistant |
| Others | See spec-kit for full list |

**Implementation Considerations:**
1. Different command directory structures:
   - Claude: `.claude/commands/`
   - Gemini: `.gemini/commands/`
   - Copilot: `.github/agents/`
2. Different command formats:
   - Most use Markdown with YAML frontmatter
   - Some use TOML or other formats
3. Different argument handling
4. Agent-specific features and limitations

**Reference:** See `spec-kit/` directory for implementation details.

### Other Future Enhancements

1. **Interactive Mode**: Guided workflow with prompts
2. **Validation Framework**: Automated validation of artifacts
3. **Template Customization**: User-defined templates
4. **Extension CLI Commands**: `codexspec extension list/add/remove`
5. **Web UI**: Browser-based workflow management

## Key Implementation Details

### UV Tool Installation

The project is designed to work with `uv tool install`:

```bash
uv tool install codexspec --from git+https://github.com/Zts0hg/codexspec.git
```

This requires:
1. Proper `pyproject.toml` configuration
2. Entry point in `[project.scripts]`
3. Correct package structure

### Template Directory Resolution

Templates must be found both in development and when installed:

```python
def get_templates_dir() -> Path:
    # When installed via uv/pip
    package_dir = Path(__file__).parent.parent.parent / "templates"
    if package_dir.exists():
        return package_dir
    # Fallback
    return Path(__file__).parent.parent / "templates"
```

### Cross-Platform Compatibility

- Use `pathlib` for all path operations
- Handle Windows vs Unix command differences
- Support both Bash and PowerShell scripts

## When Working on This Project

### Before Making Changes

1. Read this CLAUDE.md file
2. Understand the current implementation status
3. Check existing code for patterns to follow
4. Ensure changes align with project goals

### When Adding Features

1. Update this CLAUDE.md if architecture changes
2. Add tests for new functionality
3. Update README.md for user-facing changes
4. Follow existing code patterns

### When Fixing Bugs

1. Write a test that reproduces the bug
2. Fix the bug
3. Ensure all tests pass
4. Update documentation if needed

## Quick Reference

### Common Commands

```bash
# Install for development
uv sync --dev

# Run CLI locally
uv run codexspec --help

# Run tests
uv run pytest

# Lint code
uv run ruff check src/

# Build package
uv build

# Install locally for testing
uv tool install --force .
```

### Important Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project configuration, dependencies, entry points |
| `src/codexspec/__init__.py` | Main CLI implementation |
| `src/codexspec/i18n.py` | Internationalization utilities |
| `templates/commands/*.md` | Slash command templates |
| `scripts/bash/*.sh` | Bash helper scripts |
| `scripts/powershell/*.ps1` | PowerShell helper scripts |
| `extensions/` | Extension system |
| `README.md` | User documentation |
| `CLAUDE.md` | This file - AI development context |

---

*This file is the source of truth for AI assistants working on CodexSpec. Keep it updated as the project evolves.*
