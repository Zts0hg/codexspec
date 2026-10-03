# Tasks Review Report

## Summary

- **Overall Status**: PASS
- **Compatibility Score**: 100/100
- **Authority Mode**: Requirements-first
- **Readiness**: Ready for Implementation
- **Rounds**: 2 (round 1 found three Minor defects; round 2 found one further Minor; all four were remediated within the automatic fix budget)

Every plan deliverable maps to a task or a group checkpoint, every requirement maps to at least one task, every task carries a requirement and plan reference or an explicit statement of the authority that requires it, and the one task that realizes no requirement is declared as implementation support rather than left untraced. Dependencies are acyclic and every dependent appears after what it depends on. The two concurrency markers are safe: they name tasks that touch disjoint files.

All four defects were missing or imprecise verification rather than wrong work: two confirmed constraints had no check anywhere in the list, one launch command and one set of documentation paths were stated in a form the repository does not use, and one checkpoint contradicted a concurrency marker.

## Coverage

| Requirement / Plan Item | Task References | Result |
|---|---|---|
| REQ-001 | T009 | Covered |
| REQ-002 | T012, T024 | Covered |
| REQ-003 | T011 | Covered |
| REQ-004 | T009, T013 | Covered |
| REQ-005 | T016, T017 | Covered |
| REQ-006 | T017 | Covered |
| REQ-007 | T002, T003, T017 | Covered |
| REQ-008 | T017 | Covered |
| REQ-009 | T021 | Covered |
| REQ-010 | T013 | Covered |
| REQ-011 | T013 | Covered |
| REQ-012 | T018 | Covered |
| REQ-013 | T019, T027, manual matrix condition for the three confirmations | Covered |
| REQ-014 | T015 | Covered |
| REQ-015 | T015 | Covered |
| REQ-016 | T022, T027, manual matrix keyboard condition | Covered |
| REQ-017 | T022 | Covered |
| REQ-018 | T023, T027 | Covered |
| REQ-019 | T024 | Covered |
| REQ-020 | T001, T009, T014, T027 | Covered |
| REQ-021 | T012, T026 | Covered |
| REQ-022 | T008, T009, T016, T021, T026 | Covered |
| REQ-023 | T020 | Covered |
| NFR-001 | T005, T006 | Covered |
| NFR-002 | T005, manual matrix scheme condition | Covered |
| NFR-003 | T007, manual matrix width condition | Covered |
| NFR-004 | T007, manual matrix direction condition | Covered |
| NFR-005 | S025.5, S025.8, CP-C | Covered |
| NFR-006 | T005, T009, CP-C, S025.4, S025.9 | Covered |
| NFR-007 | T003 | Covered |
| NFR-008 | T004, T010 | Covered |
| NFR-009 | T004, T006 | Covered |
| NFR-010 | T025, CP-A, CP-B, CP-D, CP-F | Covered |
| Plan Phase 1 (seven units) | T001, T002, T003, CP-A | Covered |
| Plan Phase 2 (three units) | T004, CP-B | Covered — the two catalog units are one task because the parity assertion admits no partial state, as the plan's catalog decision fixes |
| Plan Phase 3 (five units) | T005, T006, T007, T008, CP-C | Covered |
| Plan Phase 4 (seven units) | T009 through T014, CP-D | Covered |
| Plan Phase 5 (seven units) | T015 through T021 | Covered |
| Plan Phase 6 (nine units) | T022 through T028, CP-F | Covered |

## Verified Defects

### Critical

None outstanding.

### Warnings

None outstanding.

### Minor

None outstanding.

## Remediated During Review

Each entry records a verified defect, the evidence that determined its remediation, and what changed. No remediation added or split a task to improve a score, and none expanded scope.

### Round 1

- **M-001 — a confirmed constraint had no verification anywhere in the list.** The specification requires that the server's served-path allowlist not be widened, and two tasks edit the module that holds it. The requirement-to-task table pointed that constraint at a stylesheet checkpoint and at the assertion that the three assets contain no absolute URL scheme; neither inspects the allowlist, so an added path would have shipped unverified. Remediated by adding a scenario to the contract-assertion task that asserts the allowlist is exactly the page at the root and at its own name, the script, the stylesheet, and the per-language catalog route, and updating both coverage tables.
- **M-002 — two repository-verified exact forms were stated in shapes the repository does not use.** The manual matrix told the reader to launch the review session with the installed command name, while this project's development invocation runs the tool through its package manager and does not depend on the tool being on the path. Separately, the documentation-translation task left its paths as a generic language pattern although the repository's documentation languages are `de`, `es`, `fr`, `ja`, `ko`, `pt-BR`, and `zh` — different codes from the review-interface catalogs, which use `pt`, `zh-CN`, and `zh-TW`, and with no Arabic, Hindi, Italian, or Russian documentation at all. Mirroring the catalog codes would have created directories the documentation site does not serve. Remediated by using the development invocation and by naming the seven documentation paths explicitly with the code difference stated at the point of use.
- **M-003 — a checkpoint contradicted a concurrency marker.** The catalog task is marked as runnable concurrently with the backend and stylesheet tasks, while its checkpoint asserted that a whole-tree diff shows exactly thirteen changed files and no other file. Run as marked, the checkpoint would have failed on the concurrent tasks' own files, so a correct state would read as a defect. Remediated by scoping the diff to the catalog directory and stating why.

### Round 2

- **M-004 — the policy that forbids inline styling was verified for the page but not for the controller.** The specification forbids a style element and a style attribute and requires dynamic state to be carried by class names; the design's corresponding decision exists precisely because the review progress, the field heights, the selection, and the gate state all change at runtime. The page-shell task verified the markup, but no task checked the controller, which is where a developer would most plausibly reach for an inline style — the progress bar's width being the obvious case, and the one the design redirects to a native progress element. Remediated by adding a scenario to the contract-assertion task that asserts neither the page nor the controller writes a style attribute or assigns an inline style, and recording it against that constraint in the coverage table.

## Risk Advisories

- **The contract-assertion task now carries nine scenarios and lands late.** Applicability: the final phase. Several of its scenarios guard work completed phases earlier — the current-selection attribute, the gate states, the confirmations — so a regression introduced in an earlier phase is caught only at the end. The group checkpoints run the existing contract tests after every asset phase, which limits the window, but moving a scenario next to the behavior it guards as each is implemented would narrow it further. This is a sequencing preference, not a correctness defect, and the plan's test-discipline decision deliberately keeps asset verification structural.
- **The documentation tasks depend on behavior rather than on the manual matrix.** Applicability: the English guide and its translations. They are ordered after the end-state task but before the matrix, so if the matrix uncovers a behavior change, the guide and its seven translations change again. Ordering them after the matrix would avoid rework at the cost of putting an eight-file documentation change at the very end of the feature. Either order is defensible; the risk is simply that documentation rework is multiplied by eight.

## Design Opportunities

- **The manual matrix's pass conditions could become a reusable checklist.** The matrix enumerates seven conditions covering two colour schemes, three widths, a right-to-left language, keyboard-only operation, three confirmations, the gate regression path, and both field-sizing paths. Since this interface will change again and no automated check in this repository renders a page, recording the matrix where it outlives this feature would make the next change's verification cheaper. This is a repository-practice improvement rather than a correction to the task list.

## Score Derivation

- Critical root causes: 0
- Warning root causes: 0
- Minor root causes: 0
- Formula: No outstanding defects = **100**. Round 1 scored 91 (three Minor: max(80, 100 − 3 × 3)); all three were remediated, round 2 found and remediated one further Minor, and the final list carries no verified defect. Advisories do not affect the score.
