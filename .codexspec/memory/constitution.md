> ⚠️ **SUPREME AUTHORITY**: This constitution defines the governing principles for this project. All code changes and decisions must comply with these principles.

# Project Constitution

This document defines the governing principles and development guidelines for this project.

## Core Principles

### 1. Code Quality

- Write clean, readable, and maintainable code
- Follow established coding standards and conventions
- Use meaningful variable and function names
- Keep functions focused and single-purpose

### 2. Testing Standards

- Write tests for all new functionality
- Maintain high test coverage
- Use appropriate testing strategies (unit, integration, e2e)
- Test edge cases and error conditions

### 3. Documentation

- Document public APIs and interfaces
- Keep documentation up-to-date with code changes
- Use clear and concise language
- Include examples where appropriate

### 4. Architecture

- Follow separation of concerns
- Design for extensibility and maintainability
- Use established architectural patterns
- Keep dependencies minimal and well-managed

### 5. Performance

- Consider performance implications of design decisions
- Profile and optimize critical paths
- Avoid premature optimization
- Use appropriate data structures and algorithms

### 6. Security

- Follow security best practices
- Validate all inputs
- Protect sensitive data
- Keep dependencies updated

## Development Workflow

1. **Planning**: Define clear requirements before implementation
2. **Specification**: Document what needs to be built and why
3. **Design**: Create technical implementation plans
4. **Implementation**: Write clean, tested code
5. **Review**: Review code and documentation
6. **Deploy**: Follow established deployment procedures

## Slash Command Template Modification Rules

**CRITICAL**: When modifying CodexSpec slash command templates, follow these rules:

### Directory Structure

| Directory | Purpose | Modification Policy |
|-----------|---------|---------------------|
| `templates/commands/` | **Source template directory** - Templates are copied from here when users run `codexspec init` | ✅ **MODIFY HERE** for distributed commands |
| `.claude/commands/codexspec/` | **Active command directory** - Commands currently in use by this project | ❌ **DO NOT MODIFY** for distributed commands; ✅ **MODIFY HERE** for internal maintenance commands listed below |

### Why This Matters

1. **Source of Truth**: `templates/commands/` is the authoritative source for all distributed command templates
2. **Distribution**: When users install/update CodexSpec, templates are copied from `templates/commands/`
3. **Consistency**: Modifying source templates ensures all users receive the same updates
4. **Version Control**: Changes to source templates are tracked in git and can be reviewed
5. **Self-bootstrap**: CodexSpec uses itself — `.claude/commands/codexspec/` in this repo is an **install artifact** produced by running `codexspec init` (or equivalent) on the CodexSpec project itself. It is not a source file. Any fix made directly there would be silently overwritten the next time CodexSpec is reinstalled, and would never reach end users. The correct flow is: edit `templates/commands/` → publish a new CodexSpec version → re-run `codexspec init` to sync.

**Rule of thumb**: If you catch yourself about to edit a file under `.claude/commands/codexspec/` for a distributed command, stop. Edit `templates/commands/` instead.

### Internal Maintenance Commands (Exception)

The following commands are **intentionally absent from `templates/commands/`** because they are tightly coupled to CodexSpec's own repository (MkDocs i18n, fixed `docs/{lang}/` structure, project-specific glossary). They live **only** in `.claude/commands/codexspec/`, are not shipped to user projects via `codexspec init`, and must be edited there directly:

- `/codexspec:translate-docs` — translates CodexSpec's own documentation
- `/codexspec:check-i18n-semantics` — verifies CodexSpec's own translated docs

Both reference `docs/i18n/glossary.yml` (the canonical, repo-only glossary). The path `.codexspec/i18n/glossary.yml` is **deprecated** and must not be reintroduced.

### Workflow for Command Modifications

**For distributed commands** (default case):

1. Modify files in `templates/commands/`
2. Test by running `codexspec init` in a test project (or reinstall with `uv tool install --force .`)
3. Commit changes to the source templates
4. Users receive updates when they reinstall or run `codexspec init`

**For internal maintenance commands** (the two listed above):

1. Modify files in `.claude/commands/codexspec/` directly
2. Verify the corresponding template does NOT exist in `templates/commands/`
3. Verify the corresponding fallback function does NOT exist in `src/codexspec/__init__.py`
4. Commit changes to `.claude/commands/codexspec/`

## Decision Guidelines

When making technical decisions, prioritize:

1. **Maintainability** over optimization
2. **Clarity** over cleverness
3. **Stability** over features
4. **Security** over convenience

---

*This constitution should be updated as the project evolves and new guidelines are established.*
