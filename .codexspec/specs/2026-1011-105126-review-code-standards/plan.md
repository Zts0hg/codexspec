# Implementation Plan: Evidence-Based Review with On-Demand Standards

**Related Spec**: [spec.md](spec.md)
**Related Design**: [design.md](design.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Created**: 2026-10-11
**Status**: Ready for task expansion

## Context and Goals

Implement the confirmed runtime standards library, behavior/evidence discipline, default incremental maintenance and independent persistent configuration. Preserve existing resolver scope, strict schema-v3 defect gate, review isolation, incremental convergence and advisory scoring. No new dependencies, per-run maintenance option, preceding-stage propagation or speculative product requirements.

## Tech Stack and Constraints

Python 3.11+, Typer/Rich, PyYAML, pytest, Ruff; English Markdown source/templates and documents, Chinese interaction. Use the selected feature worktree for all writes/checks. Author opted-in commands in internal sources and regenerate complete templates and installed integrations through normal tooling. Shipping standards live only in templates; internal authoring tools never become user runtime dependencies. Use byte-preserving resource copies and the existing surgical YAML writer.

## Plan-Level Decisions

### Decision 1: Verify executable boundaries test-first

Configuration, companion validation and installation are testable Python behavior. Add concrete regression tests, observe failures, then implement. Author checklist/protocol/documentation directly and validate their loading graph, mode contracts, source mapping and related existing tests. Do not introduce a selector engine simply to make prompt behavior unit-testable.

Covers: REQ-005, REQ-007, REQ-010, REQ-011, REQ-012; Design: Persistent configuration and repair callers; Maintenance report and validation; Resource installation and plugin delivery.

### Decision 2: Relocate mode bodies before adapting consumers

Extract existing procedure/scoring/appendix content into the confirmed resources, add common discipline and dimensions, then update the coordinator and repair consumer together. Update contract-test readers to follow the selected resource tree rather than concatenate unrelated resources into the runtime command. Preserve legacy defect fixtures and validate companions when present; new maintenance evaluations explicitly require them.

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-008, REQ-009, REQ-013, REQ-014; Design: Coordinating command; Shared standards; Maintenance report and validation.

## Implementation Phases

### Phase 1: Executable boundaries

- Implement policy parsing/reading/writing and CLI set/toggle/display/default configuration using existing routing/writer behavior. Paths: `src/codexspec/__init__.py`, `src/codexspec/review_maintenance.py`, `src/codexspec/i18n.py`, `tests/test_config_auto_maintenance.py`.
- Implement strict maintenance companion validation in the same shipping maintenance module and test exact shape, target correlation, evidence and affected-path safety.
- Implement byte-preserving shared resource installation in `src/codexspec/review_standards.py`, wire initialization/update outside integration branches, and test via `tests/test_review_standards.py`.

Covers: REQ-007, REQ-009, REQ-010, REQ-011, REQ-012, REQ-014, NFR-002; Design: Persistent configuration and repair callers; Maintenance report and validation; Resource installation and plugin delivery.

### Phase 2: Runtime standards and integration

- Create the compact `templates/review-code/` library and retain existing mode/scoring/language intent subject to common applicability rules.
- Produce a source-item mapping in the feature references accounting for every original bullet and concrete destination.
- Reduce `internal/command_templates/sources/review-code.md` to coordination with runtime resource loading.
- Update `internal/command_templates/sources/implement-tasks.md` to validate the companion, read policy, verify/apply maintenance, retain unfinished work and require complete enabled maintenance before terminal success.
- Update config instructions/config examples and audit default consumer calls across supported workflows where applicable; quick/auto-dev delegate to implement-tasks rather than parse/forward maintenance.
- Adjust marketplace root/command location to include standards without altering release/version ownership.

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, NFR-001, NFR-002; Design: Coordinating command; Shared standards; Resource installation and plugin delivery; Persistent configuration and repair callers; Maintenance report and validation.

### Phase 3: Behavior evaluation and documentation

- Adapt existing mode/template/documentation tests to read reachable resources while retaining strict gate/scoring assertions.
- Add semantic evaluation pairs for existing guarantees versus reachable bypasses, missing required implementation, late cross-language expansion, current-benefit maintenance and rejected speculative refactoring. Assertions must bind the concrete case evidence.
- Extend package archive tests to assert complete standards bytes in wheel/sdist and absence of internal authoring paths.
- Update `README.md`, `docs/en/reference/cli.md`, `docs/en/user-guide/commands.md`, repository layout guide and maintainer guide; synchronize affected localized docs/catalogs through existing project requirements where needed.

Covers: REQ-001, REQ-003, REQ-004, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-014, NFR-001, NFR-002; Design: Validation and Risks; Shared standards; Persistent configuration and repair callers; Resource installation and plugin delivery.

### Phase 4: Distribution, verification and independent review

Render command outputs, initialize the selected worktree normally for both integrations, and verify resource bytes and derived entries. Run targeted tests, full pytest, Ruff, Markdown checks, fragment distribution checks, wheel/sdist archive checks, and relevant docs gates. Keep temporary fixture roots outside Git checkouts. Establish a green baseline, freeze target evidence and invoke a fresh non-fork isolated review, with fresh specialists for actual high-impact domains. Independently verify/repair admitted defects and enabled maintenance; repeat applicable checks and review until the strict complete gate passes. Run configured non-blocking distill at that stable completion boundary. Retain the worktree; no automatic merge, deletion, publication or push.

Covers: REQ-002, REQ-003, REQ-004, REQ-007, REQ-010, REQ-011, REQ-012, REQ-014, NFR-001, NFR-002; Design: Validation and Risks; Sequence & Data Flow.

## Verification Strategy

Test default/aliases/surgical persistence and routing through real configuration consumers. Test valid/empty companions plus malformed/duplicate/mismatched/unsafe evidence cases. Test initialization and updates under both integrations with complete byte-identical standards and protected unrelated project content. Validate actual resource link targets and per-item mappings rather than only counts. Preserve all current mode argument, resolver/schema/isolation, incremental and scoring checks after relocation.

Semantic evaluations distinguish reachable defects from guaranteed-safe paths and admitted maintenance from unsupported speculative changes. Deterministic evaluations test the evidence contract; live LLM results require a separate actual reviewer run and are never inferred from template text alone.

## Requirements Coverage

| Requirement | Design Component | Plan Coverage |
|-------------|------------------|---------------|
| REQ-001 | Coordinator; standards | Phases 2, 3 |
| REQ-002 | Standards; sequence | Phases 2, 4 |
| REQ-003 | Standards; validation | Phases 2, 3, 4 |
| REQ-004 | Standards; validation | Phases 2, 3, 4 |
| REQ-005 | Coordinator; standards; delivery | Phases 1, 2 |
| REQ-006 | Coordinator; standards | Phases 2, 3 |
| REQ-007 | Standards; companion; delivery | Phases 1, 2, 3, 4 |
| REQ-008 | Standards | Phases 2, 3 |
| REQ-009 | Policy; companion; standards | Phases 1, 2, 3 |
| REQ-010 | Policy; companion | Phases 1, 2, 3, 4 |
| REQ-011 | Persistent configuration | Phases 1, 2, 3, 4 |
| REQ-012 | Coordinator; delivery | Phases 1, 2, 3, 4 |
| REQ-013 | Standards | Phase 2 |
| REQ-014 | Standards; companion; sequence | Phases 1, 2, 3, 4 |
| NFR-001 | Standards; validation | Phases 2, 3, 4 |
| NFR-002 | Coordinator; delivery | Phases 1, 2, 3, 4 |
