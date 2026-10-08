# Tasks Review Report

## Summary

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Authority Mode**: Requirements-first
- **Readiness**: Ready for Implementation
- **Review Rounds**: 3 reviews, 2 automatic fix rounds
  - Round 1: PASS_WITH_WARNINGS (4 Minor root causes; score 88). All fixes were deterministic and have been applied.
  - Round 2: 1 new Minor (T018's `-k en` selector also matches "documents", so it selects every locale). Fixed and verified by test collection.
  - Round 3: no defects.

## Coverage

| Requirement / Plan Item | Task References | Result |
|---|---|---|
| REQ-001 | T008, T013, T024 | Covered |
| REQ-002 | T008, T024 | Covered |
| REQ-003 | T007, T008, T011, T012, T013 | Covered |
| REQ-004 | T013, T024 | Covered |
| REQ-005 | T003, T005, T006, T007, T018 | Covered |
| REQ-006 | T006, T024 | Covered |
| REQ-007 | T006, T007, T011, T015 | Covered |
| REQ-008 | T006, T015, T024 | Covered |
| REQ-009 | T005, T013 | Covered |
| REQ-010 | T002, T003, T004, T018 | Covered |
| REQ-011 | T014, T016 | Covered |
| REQ-012 | T016, T017, T024 | Covered |
| REQ-013 | T009, T024 | Covered |
| REQ-014 | T008, T009 | Covered |
| REQ-015 | T009 | Covered |
| REQ-016 | T010, T023 | Covered |
| NFR-001 | T006, T008, T011, T012, T016 | Covered |
| NFR-002 | T006, T022, T024, T025 | Covered |
| NFR-003 | T013 | Covered |
| NFR-004 | T001, T018–T023 | Covered |
| Plan Phases 0–7 (all units) | T001–T025 | Covered (plan-unit table in tasks.md) |

Every task carries `Covers:` and a plan reference. Every testable task enumerates individually identifiable scenarios, each derived from spec acceptance scenarios, spec edge cases, or design rules. Documentation and verification tasks use deterministic checks. No task expands scope or hides a redesign. The dependency graph is acyclic.

## Verified Defects

### Critical

None.

### Warnings

None.

### Minor

None remaining. All of the following were found and fixed:

- **M1 — Unsafe `[P]` overlaps.**
  - **Evidence**: T004 appends tests to `tests/test_config_review_decided_by.py`, the module whose full run is T003's verification. T016 and T017 both add assertions to `tests/test_debug_template.py`. T020's verification ran the whole `tests/test_review_code_docs.py` while T019 is still rewriting locale guides.
  - **Location**: T004, T017, T020.
  - **Impact**: Concurrent edits to a shared test file, or verification runs that pick up unfinished work, give spurious red results or conflicting writes.
  - **Remediation applied**: T004 now depends on T003, and T017 on T016. Both keep `[P]` against the tasks they do not overlap with. T020's verification is scoped to `-k readme_summary`.
- **M2 — Documentation tasks could run before the scenario-decision flow was defined.**
  - **Evidence**: T018 documents scenario decisions, and T020 adds the CLAUDE.md architecture section. Both describe behavior defined by T015, but neither had T015 as an ancestor.
  - **Location**: T018, T020.
  - **Impact**: The documentation could describe the flow before it is final.
  - **Remediation applied**: T015 was added to both dependency lists, and the dependency summary was updated.
- **M3 — Missing design detail.**
  - **Evidence**: Design C3 requires the resolved decision mode to be reported in the Scope section.
  - **Location**: T006.
  - **Impact**: Users could not see which mode applied to a review.
  - **Remediation applied**: Added TS-6.8.
- **M4 — Two spec edge cases had no scenarios.**
  - **Evidence**: Spec edge cases "Incremental round finds a defect in an unchanged area" and "Root-cause class ambiguous".
  - **Location**: T008, T016.
  - **Impact**: Two NFR-001 safety properties went untested: carried coverage never suppresses an admitted finding, and classification never removes a finding from repair.
  - **Remediation applied**: Added TS-8.9 and TS-16.5, and updated the coverage table.
- **M5 (round 2) — Over-broad test selector.**
  - **Evidence**: `uv run pytest -k en` matches the substring "en" inside "documents", so it selects all eight locale parametrizations.
  - **Location**: T018 verification.
  - **Impact**: The check fails until T019 finishes, so T018 cannot be verified on its own.
  - **Remediation applied**: T018 now runs the two exact `[en-readme_and_term0]` node IDs. Collection confirmed exactly 2 tests are selected.

## Risk Advisories

- **T019 translation review effort**: `/codexspec:translate-docs` regenerates whole pages across seven locales. Review the diffs for unintended rewrites of unrelated sections; the test-enforced strings are necessary but do not prove the rest of the page is correct.
- **T024 is the only behavioral evidence**: record its per-scenario outcome, including which host ran each scenario, in the PR description so reviewers can see what was exercised live versus by string contract.

## Design Opportunities

None.

## Score Derivation

- Final round: Critical 0, Warning 0, Minor 0 → no defects → 100
- Round 1 (for the record): Minor 4 → max(80, 100 − 3×4) = 88
