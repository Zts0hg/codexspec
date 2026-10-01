# Tasks: HTML Distill Review

**Input**: `requirements.md`, `spec.md`, `design.md`, and `plan.md` in `.codexspec/specs/2026-0927-2310d6-html-distill-review/`<br>
**Prerequisites**: Approved plan and design<br>
**Test policy**: Code tasks use conditional TDD: add the enumerated failing scenario tests before implementation, then implement to green. Documentation-only work uses deterministic link/content verification.

## Task Format

Each task states its outcome, exact paths, dependencies, verification, traceability, and individually identifiable test scenarios when behavior is testable. `[P]` means the task can execute concurrently after its declared dependencies.

## Phase 1: Lossless Profile Codec

### T001 — Implement lossless profile record discovery, parsing, editing, and preview

- **Outcome**: `src/codexspec/distill_review/records.py` discovers valid profile records, produces hash-addressed structured snapshots, protects identity fields, preserves unknown Markdown spans, and renders exact preview bytes. Category and malformed-record fixtures live under `tests/fixtures/distill_review/`; behavior tests live in `tests/test_distill_review_records.py`.
- **Dependencies**: None.
- **Verification**: Run `uv run pytest tests/test_distill_review_records.py` and verify every untouched fixture round-trips byte-for-byte.
- **Covers**: REQ-002, REQ-003, REQ-009, REQ-010, NFR-006; **Plan**: Phase 1 — Contract fixtures and lossless profile codec
- **Test Scenarios**:
  - **T001-S01**: Discover candidate records across all six category directories and exclude vetted/non-candidate records from the ordinary candidate set.
  - **T001-S02**: Group records sharing a valid consolidation cluster key while retaining each member snapshot.
  - **T001-S03**: Round-trip every unedited category fixture byte-for-byte, including non-ASCII content and unknown fields.
  - **T001-S04**: Edit each allowed common and category-specific field and render the exact Markdown preview without changing opaque spans.
  - **T001-S05**: Reject attempts to change ID, category, provenance, or file identity.
  - **T001-S06**: Reject duplicate fields, ambiguous IDs, heading/filename mismatches, path traversal, symlinks, and files outside direct category children.
  - **T001-S07**: Produce stable SHA-256 values from source bytes and different hashes after any source-byte change.

## Phase 2: Shared Review Domain

### T002 — Define versioned review models and validate Agent proposal manifests

- **Outcome**: `src/codexspec/distill_review/models.py` defines versioned snapshots, proposals, verification attestations, operations, drafts, summaries, and results; `src/codexspec/distill_review/manifest.py` validates optional Agent suggestions against codec-owned snapshots. Tests live in `tests/test_distill_review_models.py` and `tests/test_distill_review_manifest.py`.
- **Dependencies**: T001.
- **Verification**: Run both focused test files and confirm stale or identity-changing suggestions never enter a draft.
- **Covers**: REQ-002, REQ-006, REQ-007, REQ-013, REQ-015; **Plan**: Phase 2 — Shared review domain and proposal-manifest validation
- **Test Scenarios**:
  - **T002-S01**: Parse and round-trip the current manifest and draft schema versions without information loss.
  - **T002-S02**: Reject unsupported schema versions, unknown operation tags, missing required fields, and duplicate record targets.
  - **T002-S03**: Accept a suggestion whose record ID, category, path, and base hash match the helper snapshot.
  - **T002-S04**: Reject a stale-hash suggestion and a suggestion that changes protected identity or targets a missing record.
  - **T002-S05**: Accept a complete cross-category consolidation proposal without allowing later edits to change its chosen output category or identity.

### T003 — Implement candidate and consolidation decision semantics

- **Outcome**: `src/codexspec/distill_review/domain.py` implements `vet`, `replace`, `remove`, `merge`, and `defer`, verification-evidence enforcement, exact previews, draft revisions, and complete change summaries without writing profile files. Tests live in `tests/test_distill_review_domain.py`.
- **Dependencies**: T002.
- **Verification**: Run `uv run pytest tests/test_distill_review_domain.py` and assert the profile fixture tree remains byte-identical after every staging test.
- **Covers**: REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-010, REQ-013, REQ-015; **Plan**: Phase 2 — Shared review domain and proposal-manifest validation
- **Test Scenarios**:
  - **T003-S01**: Stage vetting for an already outcome-verified candidate and record human endorsement.
  - **T003-S02**: Refuse vetting without outcome verification, then accept it after a non-empty verification attestation is added.
  - **T003-S03**: Revise editable fields and separately choose candidate or vetted status, with the vetted branch enforcing T003-S02.
  - **T003-S04**: Stage discard as `remove` and defer as an unchanged record listed in the summary.
  - **T003-S05**: Revise and stage a valid generalized record plus all source removals as one merge operation.
  - **T003-S06**: Keep a consolidation cluster separate without creating or removing records.
  - **T003-S07**: Reject a merge with missing members, invalid generalized fields, duplicate targets, or unsatisfied vetted evidence.
  - **T003-S08**: Produce a summary containing every add, replace, promote, remove, merge, and defer exactly once.
  - **T003-S09**: Reject a draft update based on a stale draft revision.

## Phase 3: Recoverable Session and Single Writer

### T004 — Persist recoverable Git-excluded review drafts

- **Outcome**: `src/codexspec/distill_review/session.py` atomically persists, loads, resumes, discards, and cleans versioned state under `.codexspec/.runtime/distill-review/`; init support in `src/codexspec/__init__.py` manages `.codexspec/.gitignore`, while legacy Git projects use the repository-local exclude file. Tests live in `tests/test_distill_review_session.py` and extend `tests/test_cli.py` for init.
- **Dependencies**: T002.
- **Verification**: Run the focused session/init tests and verify `git status --short` remains unchanged when an older project creates its first draft.
- **Covers**: REQ-007, REQ-011, NFR-005, NFR-006; **Plan**: Phase 3 — Recoverable session state and single-writer ownership
- **Test Scenarios**:
  - **T004-S01**: Atomically save and reload a staged draft with the same revision and decisions after a simulated process restart.
  - **T004-S02**: Explicitly discard a saved draft and leave every profile file unchanged.
  - **T004-S03**: Report a malformed or unsupported draft without changing or silently deleting it.
  - **T004-S04**: Initialize a new project with an idempotent `.codexspec/.gitignore` rule for `.runtime/`.
  - **T004-S05**: In a legacy Git project without that rule, resolve and update the repository-local exclude file before draft creation without dirtying the worktree.
  - **T004-S06**: In a non-Git project, persist runtime state without requiring Git metadata.
  - **T004-S07**: Retain a staged draft on cancel/abandon and remove completed runtime state after successful application or explicit discard.

### T005 — Enforce one writable review session per project

- **Outcome**: `src/codexspec/distill_review/lease.py` holds a cross-platform process-lifetime lock, atomically records active-service metadata, reconnects to a responsive owner, and recovers after lock release without trusting stale metadata. Tests live in `tests/test_distill_review_lease.py`.
- **Dependencies**: T002.
- **Verification**: Run multi-process lease tests on the current host and retain the same focused test in every platform CI leg.
- **Covers**: REQ-012; **Plan**: Phase 3 — Recoverable session state and single-writer ownership
- **Test Scenarios**:
  - **T005-S01**: Acquire one writable lease and reject a second writer for the same canonical project root.
  - **T005-S02**: Report reconnect metadata only when the lock owner responds with the matching protocol and capability.
  - **T005-S03**: Ignore stale metadata after the OS releases a crashed process's lock and permit recovery.
  - **T005-S04**: Treat two different canonical project roots as independent sessions.
  - **T005-S05**: Preserve owner-only metadata permissions where supported without using file mode as the authentication decision.

## Phase 4: Recoverable Profile Transaction

### T006 — Implement whole-batch transaction preflight

- **Outcome**: `src/codexspec/distill_review/transaction.py` converts a validated draft into a confined target set and checks all record schemas, base hashes, target-absence rules, symlinks, duplicate targets, and staging prerequisites before mutation. Tests live in `tests/test_distill_review_transaction.py`.
- **Dependencies**: T003, T004, T005.
- **Verification**: Run the focused transaction tests and assert every preflight failure leaves the complete profile fixture tree byte-identical.
- **Covers**: REQ-008, REQ-009, REQ-010, NFR-006; **Plan**: Phase 4 — Recoverable all-or-nothing profile transaction
- **Test Scenarios**:
  - **T006-S01**: Accept a mixed add/replace/remove/merge batch when all hashes, absence rules, paths, and rendered records are valid.
  - **T006-S02**: Report all changed-source hash conflicts in one result and write nothing.
  - **T006-S03**: Reject an unexpected existing add target, missing replace/remove target, duplicate target, symlink, or path escape and write nothing.
  - **T006-S04**: Reject any schema-invalid rendered record and identify its record and violated rule.
  - **T006-S05**: Reject staging on a different filesystem or an unwritable runtime area before moving any profile file.

### T007 — Apply and recover journaled profile transactions

- **Outcome**: `src/codexspec/distill_review/transaction.py` stages exact bytes and backups, atomically journals the operation sequence, uses same-filesystem replacements, commits or reverses the full batch, and recovers every nonterminal journal before new review. Parameterized failure tests live in `tests/test_distill_review_transaction_recovery.py`.
- **Dependencies**: T006.
- **Verification**: Run transaction and recovery tests with injected failure at every durable transition and file move; each case must end at the complete old or complete new profile, never an unrecoverable partial state.
- **Covers**: REQ-006, REQ-008, REQ-009, REQ-010, REQ-015, NFR-006; **Plan**: Phase 4 — Recoverable all-or-nothing profile transaction
- **Test Scenarios**:
  - **T007-S01**: Apply a valid mixed batch and return exact added, replaced, promoted, removed, merged, and deferred IDs.
  - **T007-S02**: On an ordinary exception at each backup/install boundary, reverse completed steps and retain the draft with the old profile restored.
  - **T007-S03**: After simulated process death at each journal state, a fresh invocation deterministically restores the old profile before serving review.
  - **T007-S04**: Recover a transaction whose operations include consolidation creation and multiple member removals.
  - **T007-S05**: Repeat recovery and cleanup safely after a second interruption without duplicating or losing records.
  - **T007-S06**: Refuse new review while recovery cannot complete and report the journal location and failed step.
  - **T007-S07**: Mark success only after the committed journal state is durable, then clean backups and the applied draft idempotently.

## Phase 5: Authenticated Loopback Service

### T008 — Implement the token-protected loopback HTTP API

- **Outcome**: `src/codexspec/distill_review/server.py` binds an OS-selected IPv4 loopback port, manages fragment-delivered capabilities, opens or prints the browser URL, serves a non-sensitive static shell, and exposes authenticated snapshot/draft/preview/apply/cancel/resume/discard JSON endpoints over the shared domain service. Tests live in `tests/test_distill_review_server.py`.
- **Dependencies**: T007.
- **Verification**: Run the HTTP suite with external networking disabled and confirm no endpoint bypasses the domain or transaction engine.
- **Covers**: REQ-001, REQ-002, REQ-007, REQ-008, REQ-009, REQ-011, REQ-012, REQ-013, REQ-015, NFR-001, NFR-002, NFR-003; **Plan**: Phase 5 — Authenticated loopback API
- **Test Scenarios**:
  - **T008-S01**: Bind only `127.0.0.1` on an available OS-selected port and serve a static shell that contains no profile data.
  - **T008-S02**: Accept a correct bearer token and exact loopback Origin for each data and mutation route.
  - **T008-S03**: Reject missing/wrong tokens, foreign/null origins on mutations, wrong methods, wrong content types, oversized bodies, and unsupported schema versions.
  - **T008-S04**: Persist a draft update and reject a stale revision from a second browser tab.
  - **T008-S05**: Return complete success or complete conflict/validation errors from Apply all and never partial success.
  - **T008-S06**: Cancel without applying, resume a saved draft, and explicitly discard only after the corresponding request.
  - **T008-S07**: Generate a fragment URL, avoid receiving the fragment in the initial HTTP request, and print it when `webbrowser.open` fails.
  - **T008-S08**: Set restrictive CSP and security headers and make no outbound HTTP/DNS request while serving and applying a review.

## Phase 6: Packaged HTML Interface

### T009 — Build the complete offline review frontend

- **Outcome**: `src/codexspec/distill_review/assets/index.html`, `app.js`, and `styles.css` implement candidate and cluster navigation, structured editors, verification prompts, Markdown source previews, staging/defer/discard choices, conflict states, application summary, resume/cancel/discard flows, fragment-token handling, and keyboard/focus behavior without external resources. Frontend contract tests live in `tests/test_distill_review_assets.py`.
- **Dependencies**: T008.
- **Verification**: Run asset contract tests, serve the packaged UI against fixture sessions, and complete the documented keyboard/manual browser checklist on the development host.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-011, REQ-015, NFR-001, NFR-002, NFR-003; **Plan**: Phase 6 — Packaged HTML interface
- **Test Scenarios**:
  - **T009-S01**: Render all candidate categories and consolidation clusters from the authenticated snapshot without exposing protected fields as editable controls.
  - **T009-S02**: Edit structured fields, request exact preview, choose candidate or vetted, and require evidence before unverified vetting.
  - **T009-S03**: Stage discard, defer, keep-separate, and merge decisions and show each exactly once in the final summary.
  - **T009-S04**: Apply a valid draft, display exact success results, and prevent duplicate Apply submission.
  - **T009-S05**: Display every conflict/validation error while preserving staged decisions for correction.
  - **T009-S06**: Resume or discard a recovered draft and cancel without applying profile changes.
  - **T009-S07**: Read the fragment capability into memory, remove it from visible history, and send it only in authorization headers.
  - **T009-S08**: Complete the workflow using keyboard navigation with visible focus and error association.
  - **T009-S09**: Load every asset with network access disabled and contain no CDN, remote font, telemetry, or dynamic external import.

### T010 — Localize browser and fallback diagnostics

- **Outcome**: Packaged catalogs under `src/codexspec/distill_review/assets/i18n/` and Python integration use `language.interaction` with English fallback for UI, server, and text diagnostics while preserving record bytes. Tests extend `tests/test_distill_review_assets.py` and `tests/test_i18n.py`.
- **Dependencies**: T009.
- **Verification**: Run focused i18n tests across configured supported language values and byte-compare records before and after display-only flows.
- **Covers**: NFR-004; **Plan**: Phase 6 — Packaged HTML interface
- **Test Scenarios**:
  - **T010-S01**: Select the configured interaction-language catalog for browser labels, errors, summaries, and CLI fallback diagnostics.
  - **T010-S02**: Fall back to English for an absent catalog or missing message key without breaking the review.
  - **T010-S03**: Display and edit a record in a different language without translating unchanged record content.

## Phase 7: Text Adapter and Hidden CLI

### T011 — Implement terminal review over the shared domain

- **Outcome**: `src/codexspec/distill_review/terminal.py` provides explicit text review with the same operations, evidence gate, draft revisions, summaries, application, conflicts, resume, and discard behavior as HTML. Tests live in `tests/test_distill_review_terminal.py` and shared parity fixtures.
- **Dependencies**: T007, T010.
- **Verification**: Run terminal tests and the shared adapter corpus, comparing normalized drafts, errors, application results, and final bytes with the HTTP adapter.
- **Covers**: REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, NFR-004; **Plan**: Phase 7 — Text adapter and hidden CLI bridge
- **Test Scenarios**:
  - **T011-S01**: Complete vet, revise, discard, defer, merge, and keep-separate decisions in text mode.
  - **T011-S02**: Enforce verification evidence and protected-field rules identically to the domain/API path.
  - **T011-S03**: Preview the full staged summary and require explicit Apply all before profile mutation.
  - **T011-S04**: Preserve and resume a draft after terminal cancellation or process restart.
  - **T011-S05**: Produce the same normalized draft, validation failures, resulting bytes, and summary as equivalent HTTP decisions.

### T012 — Add the hidden review helper command

- **Outcome**: `src/codexspec/__init__.py` exposes a hidden helper that resolves the project and interaction language, validates manifests, performs mandatory recovery, creates/resumes the single session, dispatches HTML or explicit text mode, and prints localized plus machine-readable final results. Tests live in `tests/test_distill_review_cli.py`.
- **Dependencies**: T008, T011.
- **Verification**: Run `uv run pytest tests/test_distill_review_cli.py` through Typer `CliRunner` and confirm the helper remains absent from normal documented command listings.
- **Covers**: REQ-001, REQ-011, REQ-012, REQ-014, REQ-015, NFR-003, NFR-004; **Plan**: Phase 7 — Text adapter and hidden CLI bridge
- **Test Scenarios**:
  - **T012-S01**: Start default HTML mode with a valid project/manifest and emit a valid terminal result envelope after completion.
  - **T012-S02**: Start explicit text mode and reach the same result schema.
  - **T012-S03**: Report `nothing_to_review` without leaving a service, lock, or empty draft.
  - **T012-S04**: Reject invalid project roots, unsupported manifests, and unrecoverable journals before opening a browser or changing profile files.
  - **T012-S05**: Reconnect to/report an active matching service and never start a second writer.
  - **T012-S06**: Resume or explicitly discard a saved draft according to user choice.
  - **T012-S07**: Remain hidden from `codexspec --help` and `list-commands` while callable by the distributed command template.

## Phase 8: Command, Init, Packaging, and Documentation Integration

### T013 — Update the authoritative distill command and regenerate distributed forms

- **Outcome**: `internal/command_templates/sources/distill.md` defines HTML-default manual review, proposal preparation, helper invocation, explicit text fallback, and unchanged auto-distill behavior; renderer output updates `templates/commands/distill.md`, and `codexspec init . --force --ai both` regenerates derived forms. Contract tests update `tests/test_distill_template.py` and `tests/test_command_template_fragments.py`.
- **Dependencies**: T012.
- **Verification**: Run the two focused template suites and `uv run python internal/command_template_fragments.py --check-distribution`; verify derived files match generated sources without hand edits.
- **Covers**: REQ-001, REQ-002, REQ-006, REQ-013, NFR-005; **Plan**: Phase 8 — Distill, init, packaging, and documentation integration
- **Test Scenarios**:
  - **T013-S01**: Manual `/distill review` prepares proposals and invokes HTML mode by default.
  - **T013-S02**: Manual `/distill` with no new segment enters the same review path.
  - **T013-S03**: Explicit text selection invokes the text adapter with the same validated manifest.
  - **T013-S04**: Auto-distill and near-moment extraction never invoke the helper, open a browser, prompt, wait, or gate their caller.
  - **T013-S05**: Malformed Agent proposals are rejected by the helper rather than directly mutating profile files.
  - **T013-S06**: Generated template and both self-bootstrap forms remain synchronized with the authoritative source.

### T014 — Verify init compatibility and package every runtime asset

- **Outcome**: Packaging/init changes in `src/codexspec/__init__.py`, `pyproject.toml` only if required by verified package-data behavior, and relevant tests ensure runtime assets and ignore rules reach users while maintainer-only files do not. Tests extend `tests/test_cli.py`, add `tests/test_distill_review_packaging.py`, and inspect built wheel/sdist archives.
- **Dependencies**: T010, T012, T013.
- **Verification**: Build wheel and sdist, inspect archive names/content, install into an isolated project, run init, and launch a network-disabled fixture review.
- **Covers**: REQ-001, REQ-011, NFR-002, NFR-003, NFR-005; **Plan**: Phase 8 — Distill, init, packaging, and documentation integration
- **Test Scenarios**:
  - **T014-S01**: A fresh init installs the runtime ignore rule and regenerated distill command for the selected AI integrations.
  - **T014-S02**: Force re-init updates managed artifacts idempotently without deleting user-owned files.
  - **T014-S03**: Wheel and sdist contain every Python module, HTML/CSS/JS asset, and locale catalog required for review.
  - **T014-S04**: Archives exclude `internal/`, `scripts/python/`, secrets, logs, and other maintainer-only material.
  - **T014-S05**: An isolated installed package completes candidate review with external network disabled.
  - **T014-S06**: Windows, macOS, and Linux package paths resolve the same embedded assets.

### T015 — Document the manual review workflow and security boundary

- **Outcome**: `CLAUDE.md` maintainer architecture notes and `docs/en/user-guide/commands.md` describe HTML default, explicit text fallback, local/offline security, draft recovery/discard, deterministic application, and unchanged auto-distill behavior; translated-doc workflow remains responsible for other site languages.
- **Dependencies**: T014.
- **Verification**: Run repository documentation link/structure checks and search for stale statements that describe manual review as terminal-only.
- **Covers**: REQ-001, REQ-011, REQ-014, NFR-001, NFR-002, NFR-005; **Plan**: Phase 8 — Distill, init, packaging, and documentation integration

## Phase 9: Full Verification

### T016 — Pass all focused, repository, distribution, and platform quality gates

- **Outcome**: The complete feature passes formatting, lint, focused suites, full pytest, fragment distribution validation, Git whitespace checks, archive inspection, isolated installed-runtime testing, manual browser checklist, and the full macOS/Linux/Windows CI matrix; failures are fixed within upstream scope rather than waived.
- **Dependencies**: T001 through T015.
- **Verification**: Preserve command outputs or CI run references in the implementation handoff and verify the exact commit under review is green.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, NFR-001, NFR-002, NFR-003, NFR-004, NFR-005, NFR-006; **Plan**: Phase 9 — Final verification
- **Test Scenarios**:
  - **T016-S01**: Run every new focused test module with all enumerated scenarios passing.
  - **T016-S02**: Run `ruff` formatting/lint and the complete pytest suite with no regression.
  - **T016-S03**: Run command-fragment distribution validation and confirm source, template, and self-bootstrap byte consistency.
  - **T016-S04**: Build and inspect wheel/sdist, then exercise the installed runtime offline in an isolated project.
  - **T016-S05**: Complete the manual keyboard/browser checklist for candidate review, consolidation, conflicts, recovery, and fallback URL.
  - **T016-S06**: Complete the macOS, Linux, and Windows CI matrix, including lock, rename, permissions, and browser-open fallback coverage.

## Dependencies and Execution Order

```text
T001
  -> T002
      -> T003
      -> T004 [P]
      -> T005 [P]
T003 + T004 + T005
  -> T006
      -> T007
          -> T008
              -> T009
                  -> T010
          -> T011 (after T010 for final localization/parity)
T008 + T011
  -> T012
      -> T013
T010 + T012 + T013
  -> T014
      -> T015
T001..T015
  -> T016
```

- T004 and T005 may run in parallel after T002 because they use separate modules and fixtures.
- HTTP server work starts only after transaction recovery is complete; neither UI can bypass the shared domain and application engine.
- T011 waits for T010 so final adapter-parity fixtures compare localized diagnostics as well as operations.
- Generated command and package integration waits for the runtime helper contract to be stable.

## Checkpoints

- **Core checkpoint after T003**: All decisions and previews are deterministic and profile files remain untouched during staging.
- **Persistence checkpoint after T007**: Draft recovery, one-writer ownership, atomic preflight, rollback, and restart recovery are proven without UI code.
- **HTML checkpoint after T010**: The browser workflow completes locally and offline through authenticated API calls.
- **Parity checkpoint after T012**: HTML and explicit text modes produce identical domain outcomes and files.
- **Distribution checkpoint after T014**: Fresh and legacy projects receive a complete, Git-clean installed runtime.
- **Release checkpoint after T016**: All local and remote quality gates pass for the exact implementation commit.

## Coverage

| Requirement / Plan Deliverable | Tasks | Scenario Evidence |
|---|---|---|
| REQ-001 manual entry and auto isolation | T008, T012, T013, T014, T016 | T008-S01/S07, T012-S01/S03, T013-S01..S04, T014-S01/S05, T016-S04 |
| REQ-002 complete candidate/cluster view | T001, T002, T008, T009, T013 | T001-S01/S02, T002-S03/S05, T008-S02, T009-S01, T013-S01 |
| REQ-003 structured decisions/protected identity | T001, T003, T009, T011 | T001-S04..S06, T003-S03/S04, T009-S01/S02, T011-S01/S02 |
| REQ-004 vetted evidence gate | T003, T009, T011 | T003-S01/S02, T009-S02, T011-S02 |
| REQ-005 post-revision status choice | T003, T009, T011 | T003-S03, T009-S02, T011-S01 |
| REQ-006 consolidation | T002, T003, T007, T009, T013 | T002-S05, T003-S05..S07, T007-S04, T009-S01/S03, T013-S01 |
| REQ-007 staging and summary | T003, T004, T008, T009, T011 | T003-S08/S09, T004-S01/S07, T008-S04, T009-S03, T011-S03 |
| REQ-008 all-or-nothing application | T006, T007, T008, T009, T011 | T006-S01..S05, T007-S01..S07, T008-S05, T009-S04/S05, T011-S03 |
| REQ-009 hash conflicts | T001, T006, T007, T008, T009 | T001-S07, T006-S02, T007-S02/S03, T008-S05, T009-S05 |
| REQ-010 delete/store rules | T001, T003, T006, T007 | T001-S06, T003-S04, T006-S01/S03, T007-S01 |
| REQ-011 recoverable draft | T004, T008, T009, T011, T012, T014 | T004-S01..S07, T008-S06, T009-S06, T011-S04, T012-S06, T014-S01 |
| REQ-012 one writer | T005, T008, T012, T016 | T005-S01..S05, T008-S01, T012-S05, T016-S06 |
| REQ-013 deterministic backend/no live Agent | T002, T003, T008, T013 | T002-S04, T003-S09, T008-S03, T013-S05 |
| REQ-014 text parity | T011, T012, T013, T015 | T011-S01..S05, T012-S02, T013-S03 |
| REQ-015 exact results/errors | T003, T007, T008, T009, T011, T012 | T003-S08, T007-S01/S06, T008-S05, T009-S04/S05, T011-S05, T012-S01/S02 |
| NFR-001 loopback authentication | T008, T009, T015 | T008-S01..S08, T009-S07 |
| NFR-002 offline/no external resources | T008, T009, T014, T015 | T008-S08, T009-S09, T014-S05 |
| NFR-003 platforms/browser fallback | T008, T009, T012, T014, T016 | T008-S07, T009-S08, T012-S01, T014-S06, T016-S06 |
| NFR-004 interaction language | T010, T011, T012 | T010-S01..S03, T011-S05, T012-S02 |
| NFR-005 pre-install validation | T004, T013, T014, T016 | T004-S04/S05, T013-S06, T014-S01..S06, T016-S03/S04/S06 |
| NFR-006 profile/audit preservation | T001, T004, T006, T007 | T001-S03..S07, T004-S05/S06, T006-S01..S05, T007-S01..S07 |
| Plan Phases 1–9 | T001–T016 | All scenarios above |

## Unmapped Tasks

None. Every task implements or verifies an approved plan deliverable.
