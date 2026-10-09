# Tasks: Remove orphaned nested script copies

## Ordered Tasks

- [x] T1 — Audit exact and normalized nested-path references, dynamic installer source
  selection, script-relative common imports, and package allowlists; classify the two
  historical requirements mentions in verification.md. Dependencies: none.
  Covers: REQ-001; Plan: P1.
- [x] T2 — Integrate `7fdfe17` and verify that only the six listed script files are
  deleted outside this feature's evidence. Check source/flat script and packaging
  bytes remain unchanged against `d7f0533`. Dependencies: T1.
  Covers: REQ-002; Plan: P2.
- [x] T3 — Complete executable verification and record results in verification.md;
  preserve native-platform limitations. Dependencies: T2.
  Covers: REQ-001, REQ-002, REQ-003; Plan: P3.
- [x] T4 — Prepare the evidence and review/delivery procedure in verification.md.
  The independent complete-feature review, merge, and push are post-implementation
  gates; their actual results must be reported at delivery. Dependencies: T3.
  Covers: REQ-003; Plan: P4.

T1/T2 are deterministic maintenance checks, not new runtime implementations. They
require no artificial failing unit test for deletion alone. T3 reuses real existing
behavioral tests plus a temporary installed-script smoke probe.

## T3 Test Scenarios

| ID | Expected behavior | Verification mapping |
| --- | --- | --- |
| S1 | Unix init installs supported flat Bash scripts | `tests/test_cli.py::TestInitScripts` and installed smoke probe |
| S2 | Windows-path init installs flat PowerShell scripts | `tests/test_cli.py::TestInitScripts::test_init_copies_powershell_scripts_on_windows` |
| S3 | Installed helpers load common, create a feature, and resolve prerequisites; missing tasks remain an error | installed Bash probe plus `tests/scripts/bash/test_check_prerequisites.py` and `test_create_new_feature.py` |
| S4 | Wheel/sdist retain supported script bytes and exclude nested project copies | fresh archive inspection plus `tests/test_package_contents.py` with `CODEXSPEC_DIST_DIR` |
| S5 | Existing behavior remains green | full pytest suite and applicable pre-commit/distribution checks |

## Coverage and Completion

| Requirement / plan | Tasks | Scenarios |
| --- | --- | --- |
| REQ-001 / P1 | T1 | reference audit |
| REQ-002 / P2, P3 | T2, T3 | S1–S4 |
| REQ-003 / P3, P4 | T3, T4 | S5; review and Git integration evidence |

No unmapped tasks. No parallel task dependencies. Gate results belong in verification.md;
post-gate merge/push outcomes are reported with actual commit identities at handoff.
