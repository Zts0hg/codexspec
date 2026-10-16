# Tasks: Multilingual Workflow Diagrams

## P-01: Sources

- [x] **T-001** — Import approved light/dark pages and author eight-language catalog and locale layout data under `internal/workflow_diagrams/`.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-005, NFR-001, NFR-002; **Plan**: P-01.
  - **Dependencies**: none.
  - **Verification**: label/edge inventory preserved; Chinese wording retained except excluded private-photo reference; idiomatic complete translations; protected command/path inventory unchanged; no embedded photo.

## P-02: Generation and validation

- [x] **T-002** — Implement tested generation, checking and export in `internal/workflow_diagrams.py`, with `tests/test_workflow_diagrams.py`.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-005, REQ-006, NFR-001; **Plan**: P-02.
  - **Dependencies**: T-001.
  - **Outcome**: deterministic eight editable files, explicit validation errors, 16 PNG exports and input/output freshness manifest.
  - **Test Scenarios**:
    - TS-01: complete catalog generates all locales with native nodes/edges and theme geometry parity.
    - TS-02: missing or unknown translation keys report locale/label and fail.
    - TS-03: changed English source with unreviewed translation reports stale translation.
    - TS-04: altered protected token is rejected.
    - TS-05: modified generated draw.io or PNG/input hash is detected as stale.
    - TS-06: invalid layout target/geometry is rejected; intended container nesting is allowed but independent rectangle overlap is reported.
    - TS-07: renderer failure/timeout produces error and no successful manifest update.
    - TS-08: missing/wrong locale README asset reference is reported.

- [x] **T-003** — Render and inspect every variant; refine only necessary local layout overrides.
  - **Covers**: REQ-001, REQ-003, REQ-006, NFR-002; **Plan**: P-02.
  - **Dependencies**: T-002.
  - **Paths**: `assets/workflow/`, `internal/workflow_diagrams/generated/`, feature `visual-review.md`.
  - **Verification**: inspect full-size and scaled exports for all 16 variants; check text fit, collisions, arrows, font glyphs, contrast and seven review pillars. Use a maintainer browser helper to measure text and report limitations; export remains authoritative.

## P-03: Integration and acceptance

- [x] **T-004** — Add localized picture/full-size links to eight README files and document maintenance/classification.
  - **Covers**: REQ-004, NFR-001, NFR-002; **Plan**: P-03.
  - **Dependencies**: T-003.
  - **Paths**: root `README*.md`, `internal/workflow_diagrams/README.md`, `docs/internal/repository-layout.md`.
  - **Verification**: all eight picture blocks resolve correct theme/locale assets; alt text is natural; no site/public-template/init changes; no packaging allowlist changes.

- [x] **T-005** — Complete deterministic checks and the full test baseline; prepare the complete-feature review.
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, NFR-001, NFR-002; **Plan**: P-03.
  - **Dependencies**: T-004.
  - **Verification**: tests TS-01–08, source/output check, lint/diff check, distribution consistency, full suite and scenario-to-test self-check; hand off the unchanged complete target to the separate final review gate below. No commit/push is authorized by this task list.

## Coverage

| Plan / requirements | Tasks |
|---|---|
| P-01 / REQ-001/002/003/005, NFR-001/002 | T-001 |
| P-02 / REQ-001/002/003/005/006, NFR-001/002 | T-002, T-003 |
| P-03 / REQ-004/006, NFR-001/002; complete verification | T-004, T-005 |
| TS-01–08 | T-002, verified again by T-005 |

Dependencies are sequential and acyclic. No unmapped tasks or blocking open decisions.

## Scenario self-check and final gate

| Scenario | Tests in tests/test_workflow_diagrams.py |
| --- | --- |
| TS-01 | test_ts01_generate_all_native_graphs_and_theme_parity |
| TS-02 | test_ts02_catalog_keys_are_exact (missing, unknown) |
| TS-03 | test_ts03_stale_translation |
| TS-04 | test_ts04_protected_tokens |
| TS-05 | test_ts05_stale_generated_file; test_ts05_asset_hash_and_source_drift |
| TS-06 | test_ts06_bad_layout_target; test_ts06_overlap_not_intentional_containment; test_ts06_theme_graph_mismatch; test_ts06_negative_width |
| TS-07 | test_ts07_renderer_failure_preserves_manifest (failure, timeout) |
| TS-08 | test_ts08_wrong_readme_locale; test_ts08_theme_source_must_be_in_workflow_block |

The additional output-symlink test verifies the workspace isolation contract.
All 22 targeted tests passed, including non-UTF-8 default encoding, portable source
fingerprints, shared-layout isolation and rejection of unresolved parent/source/target references. The full-suite baseline before these
bounded integration repairs was 2459 passed, 59 skipped. Distribution,
maintainer entry consistency, README translation verification and targeted lint
checks passed. Visual evidence and scaled-view limitations are in visual-review.md.

Implementation tasks are complete. Feature acceptance additionally requires a fresh
complete `review-code --feature` result with PASS, no P0–P3 findings or blocking gaps,
validated isolated reviewer topology and maintenance assessment. The target-bound
review report/envelope is stored outside the repository by that gate; completing
the implementation checkboxes does not itself assert a review verdict. No commit,
merge, push or release is authorized by this task list.

## Accepted visual refinement

DEC-003 requests balanced review cards without fixing text direction. The accepted layout
shortens non-Chinese cards to their rendered text, preserves font sizes and
connections, and tightens the implementation and lower knowledge sections together.
The initial complete-feature PASS applies to the earlier fingerprint, not this
subsequent revision. The user explicitly accepted the visual result and authorized
commit, local main integration and remote push. A final complete-feature review
must target these revised files before integration.

## Maintenance handoff extension

- [x] T-006: Complete the shared update procedure and authored Claude/derived Codex
  maintenance entries (REQ-007; P-04; D-05). Verify derivation/drift, distribution
  separation, representative update requests and existing diagram checks before
  marking this task complete. Final feature review must cover the extended target.

The extended maintenance/fragment/diagram suites pass with 241 passed and 6 skipped.
Both hosts' normal template installation excludes all three maintainer entries;
source changes and stale/missing derived entries are checked. Maintainer `--check`
and `--check-distribution` pass. Four in-memory walkthroughs cover a single-locale
wording change, stale translations after an English edit, a shared connector change
and a locale-only layout change. They do not claim new rendered visual acceptance.
The handbook/entry extension leaves the accepted diagram source and image bytes
unchanged. The generic external skill validator rejects the project's established
`codexspec:` namespace for both the new entry and the unchanged translate-docs
baseline; the repository's native derivation/distribution checks are authoritative.
