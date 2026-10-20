# Tasks: Command Descriptions

These are content/configuration tasks, including metadata string literals in
Python; no new runtime behavior is introduced. Use direct editing and existing
checks. No new implementation test scenarios are needed.

## P1: Current behavior and English descriptions

- [x] T001 Read all 28 command bodies and necessary referenced resources; record
  per-command evidence and purpose/result distinctions in inventory.md.
  Covers: REQ-001, REQ-002, REQ-004, NFR-001; Plan: P1.
  Dependencies: none.
  Verify: inventory has exactly the registered command set and source sections.
- [x] T002 Apply approved English/Chinese strings; rewrite description scalars in
  internal/command_templates/sources/*.md.
  Covers: REQ-001, REQ-002, REQ-004, NFR-001; Plan: P1.
  Dependencies: T001.
  Verify: read all new English descriptions against inventory; body and hint
  bytes match the baseline.

## P2: Language catalogs and fallback descriptions

- [x] T003 Update all eight templates/translations/*.json description fields and
  src/codexspec/commands/installer.py fallback description strings.
  Covers: REQ-003, NFR-001; Plan: P2.
  Dependencies: T002.
  Verify: read every locale for semantic fidelity and naturalness; English matches
  source extraction and Chinese matches fallback values; all other fields match baseline.

## P3: Generated artifacts and delivery checks

- [x] T004 Render templates and regenerate tracked Claude/Codex entries using
  existing renderer and installer functions.
  Covers: REQ-003; Plan: P3.
  Dependencies: T003.
  Verify: distribution check passes; derived changes contain only descriptions.
- [x] T005 Run relevant existing tests and required baseline checks; install in a
  temporary project and inspect listing output; verify scope preservation.
  Covers: REQ-001, REQ-002, REQ-003, NFR-001; Plan: P3.
  Dependencies: T004.
  Verify: record actual commands/results in verification.md; all 28 descriptions
  appear correctly in both installed integrations; no body/argument/version change.
- T006 (final gate; completion recorded in external review state): Run independent
  final feature review, resolve supported findings, and
  provide a concise completion report.
  Covers: REQ-001, REQ-002, REQ-003, NFR-001; Plan: P3.
  Dependencies: T005.
  Verify: valid clean review result and no unresolved blocking findings.

## Coverage

| Requirement / Plan | Tasks |
| --- | --- |
| REQ-001 / P1, P3 | T001, T002, T005, T006 |
| REQ-002 / P1, P3 | T001, T002, T005, T006 |
| REQ-003 / P2, P3 | T003, T004, T005, T006 |
| REQ-004 / P1, P2, P3 | T001, T002, T003, T005, T006 |
| NFR-001 / P1, P2, P3 | T001, T002, T003, T005, T006 |

No unmapped tasks. Dependencies form the linear sequence T001 through T006.

The T006 gate result is stored outside the repository under the reviewed target
fingerprint. This keeps its evidence unchanged after review; a successful handoff
requires a validated complete PASS, independently of the implementation checkboxes.
