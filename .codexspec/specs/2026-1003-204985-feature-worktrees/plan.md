# Implementation Plan: Feature Worktrees

**Related Spec**: [spec.md](spec.md)
**Related Design**: [design.md](design.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-03
**Status**: Reviewed — PASS

## Context and Goals

Implement design components C1–C6 for default-enabled feature and maintenance isolation, preserving
checkout-local configuration, the fixed automatic-development model, installation exceptions, and
all confirmed failure/lifecycle behavior. This plan consumes the design's helper/state interfaces;
it introduces no additional user-facing workflow or product policy.

Non-goals are old-directory compatibility/migration, automatic integration back to main, automatic
completion-time deletion, and repository-wide configuration overrides.

## Tech Stack and Repository Constraints

Python 3.11+, Typer/Rich, Git, Bash, PowerShell, pytest, Ruff, and the existing maintainer command
fragment renderer. No new runtime dependency is required. Runtime Python ships from `src/codexspec`;
only existing Bash/PowerShell script directories and complete command templates are distributed.
Edit opted-in internal template sources/fragments and regenerate distribution/self-bootstrap copies.

Implementation uses the task skill's red-green workflow for behavior changes and direct editing
with deterministic verification for documentation. No source edits occur in the main checkout.

## Plan-Level Decisions

### P1. Establish deterministic workspace behavior before routing command writers

Implement configuration parsing, repository discovery, and the workspace manager before adapting
CLI/agent entry points. Test their behavior with temporary repositories and local remotes. This
avoids routing production writers through an incomplete service or relying on network availability.
Existing checks of legacy in-place creation must explicitly disable isolation when they intend to
exercise that preserved behavior; new default-enabled cases must assert external placement.

**Covers**: REQ-001 through REQ-010, REQ-014, REQ-016, NFR-001, NFR-002; **Design**: C1–C4

### P2. Complete all source changes before distribution regeneration

Author the common workspace fragment and command-specific adaptations, then render and regenerate
complete command copies once the source contract is coherent. Validate the renderer and installer
read-only checks after regeneration. Do not hand-edit a derived command to fix a test.

**Covers**: REQ-005, REQ-006, REQ-011, REQ-012, REQ-013; **Design**: C5, C6

### P3. Verify caller isolation through before/after evidence

Tests compare the caller's HEAD/branch, index contents, and working files around workspace creation,
configuration writes, and failure cases. A passing helper return code alone cannot prove isolation.
Use actual Git ancestry and merge outcomes rather than proxy commit counts.

**Covers**: REQ-007 through REQ-010, REQ-014, REQ-016, NFR-001, NFR-003; **Design**: C3, C4, C5

## Implementation Phases

### Phase 1: Configuration and repository foundation

- Add the checkout-local worktree setting parser/writer in the shipping workspace service, with
  default-enabled opt-out semantics and surgical preservation of unrelated config.
- Refine the existing repository locator/shared parent behavior for normal and bare layouts,
  preserving auto-dev's fixed branch and basename. Reject ambiguous main-branch identity rather
  than selecting an arbitrary caller feature branch.
- Add focused tests in new `tests/test_worktrees.py` and applicable existing
  `tests/test_automation_git.py` cases.

**Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-012, REQ-016, NFR-002; **Design**: C1, C2, C6

### Phase 2: Workspace creation, reuse, and baseline readiness

- Implement `src/codexspec/worktrees.py` using the design's role, identity, and preparation contracts.
- Cover ordinary and maintenance creation/reuse, occupied paths and branch mismatches, short
  creation locking, durable preparation metadata, and no-reset continuation.
- Implement fetch warning/fallback/retry, ancestry selection, divergent merge preparation, verified
  continuation, and explicit non-ready failure results without destructive cleanup.
- Publish the requirements skeleton only after feature readiness. Use existing template lookup
  and preserve an already existing requirements record.

**Covers**: REQ-004 through REQ-011, REQ-014, REQ-015, NFR-001, NFR-002, NFR-003; **Design**: C3, C4

### Phase 3: CLI and platform entry points

- Expose the hidden workspace helper and `config --worktrees` interface in
  `src/codexspec/__init__.py`, including effective setting display and precise destination reporting.
- Route config setters before any setting write or command-frontmatter regeneration. Preserve
  display-only behavior, local switch scope, and both installation exemptions.
- Route mutable distill-review session setup before runtime/profile files are created.
- Adapt `scripts/bash/create-new-feature.sh` and `scripts/powershell/create-new-feature.ps1` to the
  helper contract when enabled, retaining explicit opt-out behavior and existing argument forms.
- Add `tests/test_worktrees_cli.py` and update script/config/interface tests only where the new
  default changes the premise. Preserve existing behavior checks under explicit opt-out.

**Covers**: REQ-001, REQ-002, REQ-005, REQ-006, REQ-011, REQ-013, REQ-014, REQ-016, NFR-001, NFR-003;
**Design**: C2, C3, C5, C6

### Phase 4: Agent workflow and user documentation

- Add a literal workspace-routing fragment and include it in distributed command sources.
- Adapt creation/continuation, project-maintenance, fixed auto-dev delegation, read-only input
  provenance, and state-dependent commands consistently. Remove contradictory in-place fallback
  instructions while preserving them only for explicit disabled mode.
- Update configuration documentation and the maintainer architecture description for the new
  directory, checkout-local toggle behavior, lifecycle, and initial baseline policy. Update existing
  documented auto-dev path examples; add no old-path migration guidance.
- Regenerate complete templates and installed command copies through the existing renderer and
  installers. Add focused semantic template-contract tests in `tests/test_worktrees_template.py`.

**Covers**: REQ-001 through REQ-016, NFR-001, NFR-002, NFR-003; **Design**: C5, C6

### Phase 5: Integrated verification and complete-feature review

- Run focused Git/config/CLI/script/template tests, Ruff, distribution consistency, and the full
  pytest suite. Exercise supported PowerShell checks when the runtime is available; report actual
  unavailable-platform limitations rather than claiming a pass.
- Build archives and verify new runtime code ships while internal authoring sources remain excluded.
- Map every task scenario to a real asserting test and close coverage gaps before review.
- Once a green full-suite baseline exists, invoke the isolated complete-feature defect gate per
  `implement-tasks`, repair independently verified defects, and re-establish the baseline before
  any re-review. Completion requires its valid PASS envelope.

**Covers**: REQ-001 through REQ-016, NFR-001, NFR-002, NFR-003; **Design**: C1–C6

## Verification Strategy

Tests use temporary Git repositories with controlled local remotes; inherited caller Git environment
is removed through the existing runner. Cases cover default/disabled config, different source and
destination settings, normal/bare/nested callers, independent features, reuse, preserved dirty caller
state, equal/ahead/diverged histories, timestamps that disagree with ancestry, failed fetch and retry,
no remote or valid baseline, occupied paths, incomplete preparation, and successful/failed baseline
verification. CLI/script tests assert returned absolute paths and actual write locations. Template
checks cover every distributed command's write routing and existing special-case contracts.

Documentation and generated artifacts receive deterministic source/output and packaging checks.
Verification does not rely on the main checkout or require remote publication.

## Risks and Delivery Controls

| Risk | Control |
|---|---|
| Default-on changes existing non-Git or in-place fixture assumptions | Preserve explicit opt-out tests and add new default-on cases; do not globally hide the new default |
| Partial workspace creation is mistaken for successful reuse | Exercise interruptions and persist preparation state before mutation |
| Configuration mutation routes correctly but reports the wrong scope | Test source and destination settings independently and assert diagnostic destination |
| Existing template prose overrides common routing | Sweep all source templates and verify creation/delegation/state-dependent exceptions |
| Shared changes affect unrelated automation | Full Git/blueprint/config suites and final complete-feature review |

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|---|---|---|
| REQ-001 | C2, C6 | Phases 1, 3, 4, 5 |
| REQ-002 | C2, C6 | Phases 1, 3, 4, 5 |
| REQ-003 | C1 | Phases 1, 5 |
| REQ-004 | C1, C3 | Phases 1, 2, 5 |
| REQ-005 | C3, C5 | Phases 2, 3, 4, 5 |
| REQ-006 | C1, C3, C5 | Phases 2, 3, 4, 5 |
| REQ-007 | C4 | Phases 2, 5 |
| REQ-008 | C4 | Phases 2, 5 |
| REQ-009 | C4 | Phases 2, 5 |
| REQ-010 | C4 | Phases 2, 5 |
| REQ-011 | C2, C3, C5 | Phases 2, 3, 4, 5 |
| REQ-012 | C1, C5, C6 | Phases 1, 4, 5 |
| REQ-013 | C6 | Phases 3, 4, 5 |
| REQ-014 | C3, C4, C5 | Phases 2, 3, 4, 5 |
| REQ-015 | C3 | Phases 2, 4, 5 |
| REQ-016 | C2, C6 | Phases 1, 3, 4, 5 |
| NFR-001 | C3–C6 | Phases 2, 3, 4, 5 |
| NFR-002 | C1 | Phases 1, 2, 5 |
| NFR-003 | C4, C5 | Phases 2, 3, 4, 5 |

## Open Questions

None. The design's configuration-authority question is resolved by confirmed DEC-007.
