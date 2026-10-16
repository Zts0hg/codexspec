<!--
SYNC IMPACT REPORT
==================
Version: 1.1.0 -> 1.2.0
Bump Rationale: MINOR: add the repository-only workflow-diagram maintenance entry

Changes:
- Extend the existing authored Claude / derived Codex maintenance exception with
  update-workflow-diagrams and its single shared update handbook.
- Preserve public templates, the installed command set and init/package boundaries.

Consistency:
- AGENTS.md, CLAUDE.md and docs/internal/repository-layout.md describe the entry.
- internal/maintainer_doc_skills.py and the distribution checker include its exact name.
- No downstream constitution or public command/template changes are required.

Deferred TODOs: None.
-->

> ⚠️ **SUPREME AUTHORITY**: This constitution defines the governing principles for this project. All code changes and decisions must comply with these principles.

> 🎯 **SCOPE — READ THIS FIRST**: This file governs the **CodexSpec project itself** — i.e. the repository you are working in right now. It is **NOT** a template, default, or reference document for downstream users of CodexSpec.
>
> The default constitution shipped to end-user projects lives entirely separately, as a hardcoded string in `_get_default_constitution()` inside `src/codexspec/__init__.py`. That function provides a **generic baseline** that end users then customize for their own projects via the `/codexspec:constitution` slash command.
>
> **These two artifacts serve completely different purposes and must not be kept in sync**:
>
> - Updating a CodexSpec-project-specific rule here (e.g. the Self-bootstrap rule, Slash Command Template Modification Rules) should **never** be propagated into `_get_default_constitution()`. Those rules are meaningless for end users.
> - Conversely, if you edit `_get_default_constitution()` to improve the generic baseline shipped to users, that change does **not** need to be mirrored here. This project's constitution is an independent governance document, not a copy of the default.
>
> When in doubt: ask "is this rule about how to develop *CodexSpec itself*, or is it a generic principle every CodexSpec end user would want?" The former belongs here; the latter belongs in `_get_default_constitution()`.

# Project Constitution

This document defines the governing principles and development guidelines for this project.

- **Version**: 1.2.0
- **Ratified**: 2026-04-10
- **Last Amended**: 2026-10-17

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

### 4. Clear and Standard Terminology

- Requirements, questions, documentation, and user-facing communication MUST use established
  terms that software developers commonly understand when suitable terms exist.
- Authors and agents MUST NOT invent abbreviations, compressed labels, or compound jargon merely
  to shorten or categorize a concept.
- Explanations MUST state the concrete behavior, problem, or decision before introducing a label.
- A necessary project-specific term MUST be defined in plain language on first use and then used
  consistently.
- Stable identifiers required for traceability MAY be used, but they MUST accompany a clear,
  descriptive statement and MUST NOT replace the explanation.

**Rationale**: Concise wording is useful only when it preserves shared understanding. Familiar,
precise language reduces ambiguity and prevents terminology from obstructing requirements work.

### 5. Architecture

- Follow separation of concerns
- Design for extensibility and maintainability
- Use established architectural patterns
- Keep dependencies minimal and well-managed

### 6. Performance

- Consider performance implications of design decisions
- Profile and optimize critical paths
- Avoid premature optimization
- Use appropriate data structures and algorithms

### 7. Security

- Follow security best practices
- Validate all inputs
- Protect sensitive data
- Keep dependencies updated

### 8. Remote Push Gate

- Before pushing any branch to the remote, confirm that CI/CD fully passes for the exact commit being pushed: every required check green, including the full platform matrix.
- Run and pass the equivalent local quality gates first (tests, lint, documentation checks) so the push is expected to be green; after pushing, watch the remote run to completion instead of assuming success.
- When a remote check fails, stop: fix the defect, or rerun to rule out a proven flake before pushing again. A red `main` blocks all subsequent work and must be repaired or reverted with top priority.
- A push is never "done" because the command returned; it is done when the remote pipeline is green.

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
| `templates/commands/` | **Complete distribution directory** - Templates are copied from here when users run `codexspec init` | ✅ **MODIFY HERE** for distributed commands without a same-named internal source; generated output for a command with a same-named internal source |
| `internal/command_templates/sources/` | Optional maintainer-only sources for commands that explicitly opt into shared fragments | ✅ **MODIFY HERE** instead of the matching generated complete template |
| `internal/command_templates/fragments/` | Maintainer-only literal shared fragments | ✅ **MODIFY HERE** for opted-in shared text; never shipped |
| `.claude/commands/codexspec/` | **Active command directory** - Commands currently in use by this project | ❌ **DO NOT MODIFY** for distributed commands; ✅ **MODIFY HERE** for internal maintenance commands listed below |

### Why This Matters

1. **Source of Truth**: A command without a same-named internal source is authored directly in `templates/commands/`; an opted-in command is authored in its same-named `internal/command_templates/sources/` file and rendered to `templates/commands/`
2. **Distribution**: When users install/update CodexSpec, templates are copied from `templates/commands/`
3. **Consistency**: The maintainer fragment check ensures opted-in sources and their complete distribution outputs cannot drift
4. **Version Control**: Changes to source templates are tracked in git and can be reviewed
5. **Self-bootstrap**: CodexSpec uses itself — `.claude/commands/codexspec/` in this repo is an **install artifact** produced by running `codexspec init` (or equivalent) on the CodexSpec project itself. It is not a source file. Any fix made directly there would be silently overwritten the next time CodexSpec is reinstalled, and would never reach end users. The correct flow is: edit `templates/commands/` → publish a new CodexSpec version → re-run `codexspec init` to sync.

**Rule of thumb**: If you catch yourself about to edit a file under `.claude/commands/codexspec/` for a distributed command, stop. For an opted-in command, edit its internal source or fragment and run `uv run python internal/command_template_fragments.py --write`; otherwise edit `templates/commands/` directly. Automated checks and release paths use `--check-distribution` and never rewrite files.

### Internal Maintenance Commands (Exception)

The following commands are **intentionally absent from templates/commands/**.
They serve CodexSpec maintainers, using root README variants, workflow diagrams,
the documentation site layout and docs/i18n/glossary.yml. Claude commands and native Codex
skills MUST remain outside user-project installation through codexspec init.

- translate-docs translates selected root README or site documentation.
- check-i18n-semantics reviews the corresponding translations' fidelity.
- update-workflow-diagrams maintains the shared diagram sources and all eight
  languages in both themes using internal/workflow_diagrams/README.md.

The authored entries remain .claude/commands/codexspec/{translate-docs,
check-i18n-semantics,update-workflow-diagrams}.md and MUST be edited there. Shared
translation rules live in internal/references/doc-translation.md; the diagram
procedure lives in internal/workflow_diagrams/README.md. Their native Codex entries
under .agents/skills/codexspec-<command>/SKILL.md MUST be
derived with python -m internal.maintainer_doc_skills --write, never hand-edited.
The helper's --check mode and the repository's --check-distribution gate MUST
detect missing/stale maintainer entries. No public command/template registration
or packaging allowlist is widened for these tools.

The canonical repo glossary remains docs/i18n/glossary.yml; the deprecated
.codexspec/i18n/glossary.yml path MUST NOT be reintroduced.

The pre-existing plugin-only `review-python-code.md` and `review-react-code.md` files are separate compatibility artifacts. They also have no `templates/commands/` counterpart and must be preserved unchanged by fragment synchronization and distribution checks; they are not fragment-authoring sources.

### Workflow for Command Modifications

**For distributed commands** (default case):

1. If `internal/command_templates/sources/<command>.md` exists, modify that source and/or its literal fragments, then run `uv run python internal/command_template_fragments.py --write`; do not edit its generated `templates/commands/<command>.md` directly.
2. Otherwise modify `templates/commands/<command>.md` directly.
3. Run `uv run python internal/command_template_fragments.py --check-distribution` and test by running `codexspec init` in a test project (or reinstall with `uv tool install --force .`).
4. Commit the editable source and any changed complete distribution output together.
5. Users receive only the complete templates when they reinstall or run `codexspec init`; fragment sources never ship and `init` never interprets them.

**For internal maintenance commands** (listed above):

1. Edit the authored Claude entries and shared internal documentation rules.
2. Generate native Codex entries with `python -m internal.maintainer_doc_skills --write`.
3. Pass maintainer `--check`, distribution consistency and relevant tests.
4. Verify no corresponding public template or CLI fallback was introduced.
5. For an authorized commit, include the authored/internal sources and their
   changed generated Codex entries together.

## Decision Guidelines

When making technical decisions, prioritize:

1. **Maintainability** over optimization
2. **Clarity** over cleverness
3. **Stability** over features
4. **Security** over convenience

---

*This constitution should be updated as the project evolves and new guidelines are established.*
