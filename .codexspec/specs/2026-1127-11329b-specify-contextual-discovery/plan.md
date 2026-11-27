# Implementation Plan: Context-Aware Requirement Discovery

**Feature**: 2026-1127-11329b
**Inputs**: requirements.md, spec.md, design.md
**Status**: Reviewed — PASS (see review-plan.md)

## Context and Goals

Implement design components D1-D4 in specify's existing authored source and generated forms. Deliver current-functionality verification, autonomous fact collection, bounded investigation, early automation-aware clarification, and preserved authority/confirmation boundaries.

Do not change other command entry points, shared fragments, CLI runtime, configuration schemas, frontmatter descriptions, or command registration. Do not add full design/planning output to specify.

## Repository Constraints

The authoritative file is internal/command_templates/sources/specify.md. Render templates/commands/specify.md with the existing maintainer renderer; generate .claude/commands/codexspec/specify.md and .agents/skills/codexspec-specify/SKILL.md through existing installers. Never hand-edit those generated forms.

Use the selected feature workspace for all edits and checks. Validate output containment and reject symlinks/multiply linked destinations before writes. Preserve caller-owned changes. Source readers/writers use UTF-8 and preserve expected LF bytes.

The relevant existing tests are tests/test_sdd_workflow_templates.py and tests/test_command_template_fragments.py. Existing user documentation describes the overall workflow accurately; this change adds no command, configuration, or public runtime interface.

## Plan-Level Decisions

### PD-001: Verify instruction contracts before changing the authored source

- **Decision**: Add focused instruction-contract regressions first, observe expected failures against the original template, then implement and regenerate.
- **Rationale**: The behavior is delivered as agent instructions. Tests must protect placement and complete obligations, not merely the presence of keywords.
- **Trade-off**: Static contracts do not prove live-model compliance. Review source scenarios and disclose that limitation.

### PD-002: Reuse the established generation and verification tools

- **Decision**: Use the installed Python 3.11 environment with uv sync --extra dev --python 3.11, the existing fragment renderer, and the existing integration installation APIs. Run the complete suite and required relevant deterministic checks before final independent review.
- **Rationale**: This follows repository conventions and avoids creating a parallel generation or verification mechanism.

## Implementation Phases

### P1: Protect the instruction contract and update the source

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008; Design: D1, D2, D4

1. Extend tests/test_sdd_workflow_templates.py with identifiable contract cases for preparation order, actual functionality and dependencies, independent factual collection, uncertain/missing evidence, bounded/reused investigation, automation modes, decision boundaries, and final completion.
2. Apply the behavior checks to the distributed template and both installed forms where practical. Keep source/generated fidelity under the existing renderer/distribution checks.
3. Observe failures caused by the missing obligations in the original instructions.
4. Edit internal/command_templates/sources/specify.md only: add preparation and mode-aware clarification before questioning, integrate the rules with Discussion Rules, and add the enabled-mode completion condition. Preserve existing final-confirmation and single-successor semantics.
5. Keep the added instructions proportionate; do not duplicate the complete historical recall/profile rules or downstream design procedure.

### P2: Regenerate and verify the delivered forms

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009; Design: D3, D4

1. Render the complete template with uv run --extra dev python internal/command_template_fragments.py --write --root <workspace>.
2. Regenerate installed forms via ClaudeIntegration.install and CodexIntegration.install_skills, force=True, language matching the checkout's interaction language.
3. Inspect Git changes to confirm that only specify's authored/generated forms, the related test file, and this feature's SDD artifacts changed.
4. Run focused tests, source/output/installation distribution checks, Ruff checks for changed Python tests, Markdown checks for changed documents/templates, and whitespace/link checks as applicable.
5. Establish a green complete pytest baseline, including the unchanged generation/install boundary. Do not claim skipped native-platform tests ran.
6. Record scenario-to-test coverage and verification outcomes in tasks.md and verification.md before freezing the implementation for final review.

### P3: Independent complete-feature review

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009; Design: D1, D2, D3, D4

Invoke the existing review-code complete-feature gate from a fresh isolated reviewer after source edits, generation, scenario self-check, and all verification are complete. Validate the schema-v3 defect envelope, independent maintenance companion, target identity, and required coverage. Keep review state outside the repository. Repair only verified obligations under the existing implement-tasks loop; no new approval gate or product behavior is introduced.

## Verification Strategy

- Instruction scenarios: general question premises and implementation-status classification only after inspection (including the frontend removal example); accessible facts; missing/inaccessible/contradictory evidence; finite investigation and reuse; literal-true automation semantics; foreseeable downstream blockers; equivalent engineering choices; intermediate/final confirmation; later unforeseen decisions.
- Focused regression suite: tests/test_sdd_workflow_templates.py, tests/test_profile_templates.py, tests/test_worktrees_template.py, tests/test_command_template_fragments.py.
- Distribution: internal/command_template_fragments.py --check-distribution --root <workspace>.
- Python quality: Ruff lint and format check for the changed test file.
- Document quality: repository Markdown rules and link/whitespace checks for authored feature documents and changed command forms.
- Complete baseline: uv run --extra dev pytest.
- Final independent gate: review-code --feature <absolute-feature-directory>, default complete-feature selector.

## Risks and Delivery Limits

| Risk | Control |
|---|---|
| Instructions are abbreviated and lose a required clause | Clause-level coverage and independent review against requirements.md |
| The source changes but installed forms remain stale | Existing renderer/install APIs and exact distribution checks |
| Frontloading becomes an exhaustive technical questionnaire | Material-outcome boundary, equivalent implementation autonomy, bounded investigation |
| Static tests are mistaken for live-agent evaluation | Explicitly report the contract-test limitation |

## Requirements Coverage

| Requirement | Design Component | Plan Coverage |
|---|---|---|
| REQ-001 | D1, D4 | P1, P2, P3 |
| REQ-002 | D1, D4 | P1, P2, P3 |
| REQ-003 | D1, D4 | P1, P2, P3 |
| REQ-004 | D1, D4 | P1, P2, P3 |
| REQ-005 | D1, D2, D4 | P1, P2, P3 |
| REQ-006 | D2, D4 | P1, P2, P3 |
| REQ-007 | D2, D4 | P1, P2, P3 |
| REQ-008 | D2, D4 | P1, P2, P3 |
| REQ-009 | D3, D4 | P2, P3 |

## Open Items

None. Dependencies are limited to the existing tooling and confirmed design.
