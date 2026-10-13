# Design Document: Comprehensive English README Audit

**Related Spec**: [spec.md](spec.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-12
**Status**: Ready for Planning

## Context

This documentation feature changes the English README and maintains audit
evidence in its own feature records. It adds no runtime component or dependency.

## Architecture & Components

### Capability inventory and audit record

- **Responsibility**: An audit.md table accounts for every public CLI command,
  distributed agent command, and shared user mechanism. Each row records source
  evidence, baseline coverage, and the final README resolution.
- **Interface**: Read current source, command templates, related confirmed
  requirements, release history, and the baseline README. Publish evidence only
  inside this feature directory.
- **Covers**: REQ-001, REQ-002, REQ-005, NFR-001.

### README introduction and navigation

- **Responsibility**: Explain Requirements-First SDD, both host integrations,
  user benefits, and navigation to installation and major capability groups.
  Keep the new desktop installation guide reachable.
- **Interface**: Existing GitHub-friendly Markdown/HTML, relative documentation
  links, and in-page anchors.
- **Covers**: REQ-003, REQ-004, REQ-005, NFR-001.

### Workflow and feature introductions

- **Responsibility**: Present the standard requirements → spec → design → plan →
  tasks chain; Quick; blueprint/auto-dev; existing-code workflows; review and
  debugging; profile knowledge/manual review; historical recall; and Git
  delivery commands with purpose, invocation, and relevant default behavior.
- **Interface**: Use slash commands for Claude and dollar-prefixed skills for
  Codex. Treat detailed existing guides as reference material rather than
  copying hidden helper protocols into the README.
- **Covers**: REQ-001, REQ-003, REQ-004, NFR-001.

### Configuration, workspace, and contributor reference

- **Responsibility**: Document the public command/options inventory, language
  dimensions, workflow defaults, review decision mode, checkout-local worktree
  effects, actual initialized directories, upgrade refresh, and correct
  development dependency installation.
- **Interface**: Current CLI signatures, initialization source, pyproject.toml,
  and existing user-guide/reference links.
- **Covers**: REQ-001, REQ-003, REQ-004, REQ-005, NFR-001.

### Verification evidence

- **Responsibility**: Verify command/option coverage, local links and anchors,
  Markdown, whitespace, product-file scope, and the completed audit.
- **Interface**: Temporary read-only checks and existing repository quality
  tooling; record real commands/results in verification.md.
- **Covers**: REQ-002, REQ-004, REQ-005, NFR-001.

## Key Design Decisions

### Decision 1: Preserve a readable README with complete discovery coverage

- **Context**: Coverage must include functionality absent from the baseline,
  without requiring a complete command reference for every argument.
- **Decision**: Use feature-oriented introductions and complete command tables.
  Each introduction gives useful entry examples and important defaults; link
  existing detailed guides for full contracts.
- **Alternatives**: Merely add missing rows (insufficient usage explanation);
  reproduce all command/helper instructions (large and difficult to maintain).
- **Trade-offs**: Some parameter details remain in reference guides. No capability
  may disappear solely because it is absent from the old README.
- **Covers**: REQ-001, REQ-002, REQ-003, NFR-001.

### Decision 2: Keep audit evidence separate from product prose

- **Context**: Maintainers need coverage and provenance; new users need a coherent
  guide to current capabilities.
- **Decision**: Put the detailed inventory, baseline issue assessment, resolution
  links, and verification in this feature's audit.md and verification.md. README
  explains present behavior without narrating the editing session.
- **Trade-offs**: Reviewers consult the feature record for audit evidence.
- **Covers**: REQ-002, REQ-004, REQ-005, NFR-001.

### Decision 3: Verify documentation without changing runtime behavior

- **Context**: Installation and autonomous development examples can mutate files.
- **Decision**: Establish contracts from current source and confirmed history;
  use read-only help, source-based coverage, Markdown and link checks. Report
  runtime discrepancies separately. No new product test files or program fixes.
- **Trade-offs**: Documentation checks establish accuracy and navigability, not
  live-model effectiveness or end-to-end autonomous execution.
- **Covers**: REQ-002, REQ-004, REQ-005, NFR-001.

## Requirements Coverage

| Spec Requirement | Design Coverage |
|------------------|-----------------|
| REQ-001 | Capability inventory; workflow introductions; configuration reference |
| REQ-002 | Capability inventory; verification evidence; Decisions 2 and 3 |
| REQ-003 | Introduction; workflow introductions; configuration reference; Decision 1 |
| REQ-004 | Introduction/navigation; configuration/reference; verification evidence |
| REQ-005 | Inventory and verification boundaries; Decisions 2 and 3 |
| NFR-001 | Evidence-backed inventory; all prose components; all decisions |
