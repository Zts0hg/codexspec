# Implementation Plan: Specs Context Recall

## Context

Deliver [design.md](design.md) components C1-C4 against the confirmed requirements
and [spec.md](spec.md). The Python package supports Python 3.11+. The relevant
integration surfaces are installed project context, the existing plugin startup
hook, and maintainer-authored command sources with complete generated outputs.

## Goals / Non-Goals

Deliver consistent active historical recall with correct decision authority,
scenario depth, targeted questioning, and background reuse. Mandatory recall for
purely mechanical edits is excluded. Follow the design's instruction-based
approach; this plan adds no search service or persistent history database.

## Plan-Level Decisions

### P-D1: Verify Python delivery before regenerating distributed instructions

**Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008; Design: C1, C2, C3, C4**

Write failing tests for context installation and plugin output, implement the
shared block and wiring, then regenerate template and self-bootstrap artifacts.
The existing plugin-output equality test must deliberately adopt the combined
output while continuing to verify the unchanged commit block. This sequence
distinguishes an expected contract extension from lost commit behavior.

### P-D2: Use the feature workspace's own environment

**Covers: REQ-001; Design: C4 (verification support)**

Create `.venv` with Python 3.11 and `uv sync --extra dev --extra docs`; use that
interpreter and CLI, with its bin directory first on PATH, throughout validation.
Keep tests' temporary repositories outside the real checkout. Run focused tests
first, then the complete required quality gates after the diff stabilizes.

## Implementation Phases

### P1: Shared guidance and project context delivery

**Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, NFR-001; Design: C1, C2**

Add `tests/test_specs_context.py` to verify bounded rendering, fresh and repeat
injection, replacement without damage to adjacent content, all integration modes,
and semantic policy coverage. Observe failures, then add `specs_context.py` and
wire both context installers. Preserve unrelated project prose and managed blocks.

### P2: Plugin startup composition

**Covers: REQ-001 through REQ-008, NFR-001; Design: C2, C4**

Extend `tests/test_plugin_commit_guidance.py` to require both exact guidance
blocks, test the hook without a persistent CLI, and preserve nonmutation checks.
Implement composition in `commit_guidance.py` with the existing quoting and path
checks. Keep the existing commit guidance renderer and hook entry point compatible.

### P3: Workflow reminders and complete distribution

**Covers: REQ-001, REQ-004, REQ-005, REQ-006, REQ-008, NFR-001; Design: C3, C4**

Author `specs-recall.md` under the internal fragments directory and include it in
the 15 sources listed by C3. Tests verify those distributed commands retain
current-feature authority, targeted review/staged-input boundaries, and background
reuse. Render with `internal/command_template_fragments.py --write`; run
`codexspec init . --force --ai both` in this feature workspace. Never manually edit
derived commands or skills. Add concise user documentation for recall behavior.

### P4: Distribution and scenario validation

**Covers: REQ-001 through REQ-008, NFR-001; Design: C4; D1-D4**

Add package assertions for the new runtime module, relying on existing byte checks
for complete templates and exclusion of internal authoring. Execute the eight
design scenarios as direct reasoning against the installed policy and document
their outcomes and limitations. Run focused tests, full pytest, lint/format,
fragment distribution verification, strict documentation build, and wheel/sdist
inspection. Use the implementation review gate after the changes stabilize.

## Verification Strategy

- TDD for Python runtime/integration behavior; direct implementation plus
  consistency checks for prose and generated artifacts.
- Installation matrix: claude, codex, both; existing content; repeated init.
- Plugin matrix: marketplace tree and freshly installed command tree; repository
  and non-repository working directories; CLI absent; awkward plugin path quoting.
- Policy coverage: unchanged old requirements, additions, explicit later changes,
  latest user decision, ambiguity, plans versus implementation, reuse/supplement,
  and mechanical/empty-history cases.
- Report unit/integration results separately from scenario reasoning. Do not claim
  a measured LLM recall rate from string or injection tests.

## Risks / Trade-offs

| Risk | Delivery implication | Mitigation |
|---|---|---|
| Drift between startup and project context | Different behavior across installations | Share C1 renderer and test exact emitted block |
| Historical context overrides selected authority | Reopened decisions or expanded review scope | Explicit scope/authority reminders and semantic cases |
| Stale derived artifacts | Installed behavior differs from source | Regenerate through existing tools and check distribution |
| Full-history loading or repeated scans | Higher latency and redundant questions | Explicit sufficiency/reuse rules and scenario validation |

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|---|---|---|
| REQ-001 | C1-C4 | P1-P4 |
| REQ-002 | C1, C2, C4 | P1, P2, P4 |
| REQ-003 | C1, C2, C4 | P1, P2, P4 |
| REQ-004 | C1-C4 | P1-P4 |
| REQ-005 | C1-C4 | P1-P4 |
| REQ-006 | C1-C4 | P1-P4 |
| REQ-007 | C1, C2, C4 | P1, P2, P4 |
| REQ-008 | C1-C4 | P1-P4 |
| NFR-001 | C1-C4 | P1-P4 |
