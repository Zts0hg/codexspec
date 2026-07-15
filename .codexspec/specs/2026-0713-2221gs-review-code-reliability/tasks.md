# Tasks: Reliable Change-Scoped Code Review

<!--
Language: English, as configured by .codexspec/config.yml.
Tasks preserve the approved plan and confirmed requirement boundaries.
-->

**Input**: `.codexspec/specs/2026-0713-2221gs-review-code-reliability/{requirements.md,spec.md,plan.md}`
**Prerequisites**: Confirmed `requirements.md`, reviewed `spec.md`, and reviewed `plan.md`

**Tests**: Test-first ordering is required for resolver and evaluation-runner code and is used for command-template contracts before source edits. Documentation and translation updates are implemented directly after their consistency tests define the expected syntax.

**Organization**: Tasks follow the five approved implementation phases. Every task has one verifiable outcome, exact paths, dependencies, and upstream traceability.

## Format: `### [ ] [ID] [P?] Description`

- **[P]**: May run concurrently after its declared dependencies because it writes different files.
- Every task includes `Covers:` and `Plan:`.
- A task remains incomplete until its listed verification passes.

## Phase 1: Resolver Contract and TDD Fixtures

**Purpose**: Establish one versioned review-context contract and equivalent native implementations before the review template depends on it.

### [x] T001 Define shared review-context scenarios and normalized assertions

- **Outcome**: `tests/review_context_cases.py` can create temporary repositories for every selector, Git state, base/parent case, feature match, unusual path, and error condition and can normalize a manifest for platform-independent comparison.
- **Paths**: `tests/review_context_cases.py`
- **Work**:
  - Define schema-v1 required keys and stable enum expectations.
  - Provide repository builders for local/bare remotes, committed/staged/unstaged/untracked/ignored changes, rename/delete/symlink/binary/submodule entries, normal/root/merge commits, and empty/error cases.
  - Provide immutable before/after repository snapshots and expected inventory merging by path and segment.
  - Keep fixtures source-independent and network-free.
- **Dependencies**: None
- **Verify**: The helper imports cleanly, fixture-only unit checks pass, and no production script is implemented in this task.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-007, REQ-011, REQ-022, REQ-027, NFR-003; **Plan**: Component A / Component E / Phase 1 / PLD-003 / PLD-005

### [x] T002 [P] Add failing Bash resolver contract tests

- **Outcome**: `tests/scripts/bash/test_review_context.py` defines the complete Bash-facing contract and fails because `scripts/bash/review-context.sh` does not yet exist.
- **Paths**: `tests/scripts/bash/test_review_context.py`
- **Work**:
  - Parameterize shared scenarios for default, base-branch default, committed, uncommitted, and commit selectors.
  - Assert explicit/symbolic/remote/fallback base resolution, merge bases, parent selection, empty trees, feature matching, counts, merged segment provenance, and non-ignored inventory.
  - Assert stable error JSON for invalid options, bare paths, conflicts, unresolved refs, and invalid parents.
  - Assert NUL-safe handling of spaces and shell metacharacters and no branch/ref/index/worktree mutation.
- **Dependencies**: T001
- **Verify**: `uv run pytest tests/scripts/bash/test_review_context.py -q` fails only because the resolver is absent or unimplemented.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-011, REQ-022, REQ-027, NFR-003; **Plan**: Component A / Component E / Phase 1

### [x] T003 Implement the Bash review-context resolver

- **Outcome**: `scripts/bash/review-context.sh` emits schema-v1 success/error JSON for every shared scenario without third-party JSON tools or repository mutation.
- **Paths**: `scripts/bash/review-context.sh`
- **Work**:
  - Implement strict option parsing and JSON escaping.
  - Resolve repository, selected remote, default/explicit base, merge base, root/normal/merge parent, feature context, and target completeness.
  - Consume NUL-delimited Git output and merge inventory contributions by path while retaining rename provenance.
  - Emit only JSON on stdout; route diagnostics safely; return nonzero for error manifests.
- **Dependencies**: T002
- **Verify**: `uv run pytest tests/scripts/bash/test_review_context.py -q` passes and `bash -n scripts/bash/review-context.sh` is clean.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-011, REQ-022, NFR-003; **Plan**: Component A / Phase 1 / PLD-001 / PLD-003

### [x] T004 [P] Add failing PowerShell resolver contract tests

- **Outcome**: `tests/scripts/powershell/test_review_context.py` applies the same normalized scenarios to PowerShell and fails because `scripts/powershell/review-context.ps1` does not yet exist.
- **Paths**: `tests/scripts/powershell/test_review_context.py`
- **Work**:
  - Reuse T001 builders and expected manifests rather than duplicate expected semantics.
  - Cover the same selectors, refs, parents, inventory sources, error manifests, special paths, and no-mutation snapshots as T002.
  - Skip only when PowerShell is genuinely unavailable locally; retain mandatory execution on Windows CI.
- **Dependencies**: T001
- **Verify**: On a PowerShell-capable host, the focused test fails only because the resolver is absent or unimplemented; on other hosts, pytest reports the documented skip.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-011, REQ-022, REQ-027, NFR-003; **Plan**: Component A / Component E / Phase 1 / PLD-005

### [x] T005 Implement the PowerShell review-context resolver

- **Outcome**: `scripts/powershell/review-context.ps1` produces manifests semantically equivalent to Bash for the shared contract.
- **Paths**: `scripts/powershell/review-context.ps1`
- **Work**:
  - Implement native parameter parsing, Git invocation, feature resolution, inventory merging, and `ConvertTo-Json` serialization.
  - Preserve paths and error codes exactly after normalization.
  - Avoid writes, external modules, fetches, and persisted resolver state.
- **Dependencies**: T004
- **Verify**: `uv run pytest tests/scripts/powershell/test_review_context.py -q` passes on a PowerShell-capable host and Windows CI; normalized fixture results match T002 expectations.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-011, REQ-022, NFR-003; **Plan**: Component A / Phase 1 / PLD-001 / PLD-003 / PLD-005

### [x] T006 Verify resolver installation and package distribution

- **Outcome**: Existing init and packaging mechanisms demonstrably install exactly the applicable resolver and preserve its content.
- **Paths**: `tests/test_cli.py`, `tests/test_package_contents.py`, `pyproject.toml` only if the new archive test proves the existing inclusion rule insufficient
- **Work**:
  - Extend `TestInitScripts` to assert `review-context.sh` on Unix and `review-context.ps1` on Windows, opposite-platform exclusion, and byte-preserved copies.
  - Assert project-local review operation has no installed CodexSpec CLI dependency.
  - Add an archive-content assertion or final-build check for both source scripts under packaged `codexspec/scripts/`.
- **Dependencies**: T003, T005
- **Verify**: Focused init tests pass on available platforms; package configuration includes both platform directories.
- **Covers**: REQ-007, REQ-027, NFR-003; **Plan**: Component D / Component E / Phase 1

**Checkpoint**: Schema-v1 target construction is deterministic, cross-platform, installed project-locally, and read-only.

## Phase 2: Defect-Gate Command Contract

**Purpose**: Replace default scorecard behavior with the four-stage defect gate while retaining the scorecard only behind `--audit`.

### [x] T007 Add failing review-code command contract tests

- **Outcome**: `tests/test_review_code_templates.py` expresses every defect-gate and audit invariant and fails against the old path-oriented template.
- **Paths**: `tests/test_review_code_templates.py`
- **Work**:
  - Assert the new frontmatter description, target-oriented argument hint, and Bash/PowerShell resolver declarations.
  - Assert default/committed/uncommitted/commit/base/parent/feature/focus syntax and mutual exclusion; reject bare paths and bypass flags.
  - Assert Scope, Behavior, Risk, and Verification stages; all ten profiles; semantic activation; inventory dispositions; requirements-depth branches; isolation/specialist topology; instruction/evidence trust; test-gap admission; verification-safety protocol; and PASS invariants.
  - Include a mutating project-check example and assert the command contract requires disposable-mirror execution or rejection before it can run in the project tree.
  - Assert exactly the six human report sections and required result-envelope fields/enums.
  - Assert audit retains the existing score dimensions/statuses and does not emit or feed the defect envelope.
- **Dependencies**: T006
- **Verify**: `uv run pytest tests/test_review_code_templates.py -q` fails for the old template contract, not for test setup errors.
- **Covers**: REQ-001, REQ-003, REQ-006, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016, REQ-017, REQ-018, REQ-019, REQ-020, REQ-021, REQ-022, REQ-023, REQ-024, REQ-027, NFR-001, NFR-004; **Plan**: Component B / Component E / Phase 2 / PLD-002 / PLD-004

### [x] T008 Rewrite the distributed review-code template

- **Outcome**: `templates/commands/review-code.md` passes T007 and implements a strict mode dispatcher, defect coordinator, retained audit branch, and fail-closed envelope contract.
- **Paths**: `templates/commands/review-code.md`
- **Work**:
  - Add project-local script metadata and early argument/mode dispatch.
  - Invoke and validate resolver schema v1 before defect review; provide migration errors for bare paths.
  - Encode target-dependent requirements coverage, complete inventory accounting, four stages, risk profiles, fresh reviewer/specialist delegation, project-first read-only verification, finding admission, and strict terminal verdicts.
  - Encode cache/report redirection, disposable-mirror routing, and mutation detection for verification safety.
  - Preserve existing quality scorecard behavior under a self-contained `--audit` branch and remove audit-only language from defect reports.
- **Dependencies**: T007
- **Verify**: `uv run pytest tests/test_review_code_templates.py -q` passes; `rg` confirms no legacy bare-path success example remains in the template.
- **Covers**: REQ-001, REQ-003, REQ-006, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016, REQ-017, REQ-018, REQ-019, REQ-020, REQ-021, REQ-022, REQ-023, REQ-024, NFR-001, NFR-004; **Plan**: Component B / Phase 2 / PLD-001 / PLD-002 / PLD-004

### [x] T009 Verify Claude and Codex rendering of the new review command

- **Outcome**: Both supported integrations render the updated command with the correct project-local platform resolver and unchanged behavioral contract.
- **Paths**: `tests/test_codex_integration.py`, `tests/commands/test_installer.py`
- **Work**:
  - Add focused rendering assertions for both `scripts:` choices, argument text conversion, invocation syntax conversion, and frontmatter removal/preservation as appropriate.
  - Initialize temporary Claude-only, Codex-only, and combined projects and inspect installed review artifacts without editing current generated copies.
  - Assert an absent or incompatible installed resolver leads to the documented fail-closed instructions.
- **Dependencies**: T008
- **Verify**: `uv run pytest tests/test_codex_integration.py tests/commands/test_installer.py -q` passes.
- **Covers**: REQ-006, REQ-007, REQ-008, REQ-020, REQ-027, NFR-003, NFR-004; **Plan**: Component B / Component D / Component E / Phase 2

**Checkpoint**: Installed `review-code` has deterministic scope, strict defect semantics, isolated audit semantics, and stable output on both integrations.

## Phase 3: Implement-Tasks Strict Review Loop

**Purpose**: Make workflow completion consume only a verified complete-feature PASS.

### [x] T010 Replace legacy final-loop tests with failing strict-gate tests

- **Outcome**: `tests/test_sdd_workflow_templates.py` rejects the old filtered-path, score, deferral, fallback, and two-round behavior and specifies the new loop.
- **Paths**: `tests/test_sdd_workflow_templates.py`
- **Work**:
  - Replace old assertions for analyzable extensions, `no code to review`, score thresholds, severity deferral, and fixed rounds.
  - Assert invocation is `review-code --feature <feature-dir>` with the complete default target.
  - Assert envelope schema/topology validation, independent finding verification, functional TDD, non-code checks, fresh full re-review, only-PASS success, exact progress guards, and two transient-INCONCLUSIVE retries.
- **Dependencies**: T009
- **Verify**: The focused test fails against the old `implement-tasks.md` only for expected contract mismatches.
- **Covers**: REQ-009, REQ-018, REQ-020, REQ-021, REQ-024, REQ-025, REQ-026, REQ-027, NFR-001, NFR-004; **Plan**: Component C / Component E / Phase 3

### [x] T011 Rewrite the implement-tasks final review loop

- **Outcome**: `templates/commands/implement-tasks.md` validates and consumes the defect envelope, verifies findings before edits, and reaches success only after a fresh complete-feature PASS.
- **Paths**: `templates/commands/implement-tasks.md`
- **Work**:
  - Preserve feature authority, per-task TDD, issue recording, and green baseline sections.
  - Remove source filtering, audit fallback, score parsing, low-severity deferral, and fixed two-round completion.
  - Add strict target/feature/context/reviewer/envelope validation and exact repair/retry/stop rules.
  - Keep commits outside verdict logic and report blocked evidence without converting it to success.
- **Dependencies**: T010
- **Verify**: `uv run pytest tests/test_sdd_workflow_templates.py -q` passes and no legacy final-loop markers remain.
- **Covers**: REQ-009, REQ-018, REQ-020, REQ-021, REQ-024, REQ-025, REQ-026, NFR-001, NFR-004; **Plan**: Component C / Phase 3

**Checkpoint**: `implement-tasks` cannot complete from an audit score, malformed output, shared final-gate context, incomplete specialist review, or any P0-P3 finding.

## Phase 4: Distribution and User Migration

**Purpose**: Update all installed metadata and user-facing syntax atomically.

### [x] T012 Add failing metadata and documentation consistency tests

- **Outcome**: Automated checks identify every old path-oriented syntax/description across translations and supported documentation locales.
- **Paths**: `tests/test_translation_files.py`, `tests/test_review_code_docs.py`
- **Work**:
  - Assert all translation JSON files expose the new change-gate description and selector-oriented argument hint.
  - Assert every `docs/<locale>/user-guide/commands.md` uses defect-gate syntax, explicit `--audit` path examples, strict verdict language, and a labeled breaking-change migration block.
  - Assert README command summaries no longer describe the default as the broad scorecard.
- **Dependencies**: T011
- **Verify**: Focused tests fail against the current translations/docs for expected legacy text.
- **Covers**: REQ-001, REQ-006, REQ-027, NFR-002; **Plan**: Component D / Component E / Phase 4 / PLD-007

### [x] T013 [P] Update command metadata and translation caches

- **Outcome**: Installer metadata and all eight translation caches describe the change-scoped gate and its target/audit syntax consistently.
- **Paths**: `src/codexspec/commands/installer.py`, `templates/translations/en.json`, `templates/translations/zh-CN.json`, `templates/translations/ja.json`, `templates/translations/ko.json`, `templates/translations/de.json`, `templates/translations/es.json`, `templates/translations/fr.json`, `templates/translations/pt-BR.json`
- **Dependencies**: T012
- **Verify**: Translation JSON parses, key parity tests pass, and installed command lists show the updated localized description.
- **Covers**: REQ-001, REQ-006, REQ-027, NFR-002; **Plan**: Component D / Phase 4

### [x] T014 [P] Update localized command guides and README summaries

- **Outcome**: Every supported locale documents the new default gate, selectors, audit migration, report/verdict semantics, and next-release breaking changes; README summaries align.
- **Paths**: `docs/en/user-guide/commands.md`, `docs/zh/user-guide/commands.md`, `docs/ja/user-guide/commands.md`, `docs/ko/user-guide/commands.md`, `docs/de/user-guide/commands.md`, `docs/es/user-guide/commands.md`, `docs/fr/user-guide/commands.md`, `docs/pt-BR/user-guide/commands.md`, `README.md`, `README.zh-CN.md`, `README.ja.md`, `README.ko.md`, `README.de.md`, `README.es.md`, `README.fr.md`, `README.pt-BR.md`
- **Dependencies**: T012
- **Verify**: Documentation consistency tests pass; examples contain no successful `review-code <path>` invocation; localized migration blocks identify both breaking changes.
- **Covers**: REQ-001, REQ-006, NFR-002; **Plan**: Component D / Phase 4 / PLD-007

### [x] T015 Extend CI triggers and verify built distributions

- **Outcome**: Template changes trigger normal CI, and built wheel/sdist archives contain both resolver scripts and the updated command template.
- **Paths**: `.github/workflows/ci.yml`, `tests/test_package_contents.py`
- **Work**:
  - Add `templates/**` to push and pull-request CI path filters.
  - Build wheel and sdist from the workspace and inspect archive contents.
  - Run `twine check` without publishing.
- **Dependencies**: T006, T013, T014
- **Verify**: CI YAML parses, archive assertions pass, and both distributions pass `twine check`.
- **Covers**: REQ-006, REQ-007, REQ-027, NFR-002, NFR-003; **Plan**: Component D / Component E / Phase 4

**Checkpoint**: New and updated projects receive the resolver and command contract, and all documented invocations migrate atomically.

## Phase 5: Evaluation and Acceptance

**Purpose**: Prove deterministic contracts, exercise actual reviewer behavior, and record acceptance evidence.

### [x] T016 Add failing evaluation corpus and runner contract tests

- **Outcome**: `tests/test_review_code_eval.py` defines source-independent case schema, temporary repository setup, host adapter interface, result-envelope parser, minimum/forbidden finding matching, and recorded-result schema before the runner exists.
- **Paths**: `tests/test_review_code_eval.py`
- **Dependencies**: T008
- **Verify**: The focused test fails only because the runner/corpus modules are absent.
- **Covers**: REQ-018, REQ-020, REQ-021, REQ-023, REQ-028, NFR-001, NFR-002; **Plan**: Component F / Phase 5 / PLD-006

### [x] T017 Implement the development-only evaluation runner

- **Outcome**: `tests/evals/review_code/run_eval.py` can create a temporary initialized project, apply one case, invoke a selected supported host, parse the actual result, evaluate expectations, and write a credential-free aggregate record.
- **Paths**: `tests/evals/review_code/run_eval.py`, `tests/evals/review_code/__init__.py`, `tests/evals/review_code/README.md`
- **Work**:
  - Implement explicit Claude and Codex host adapters using subprocess argument arrays, not shell interpolation.
  - Add a canned-output mode for normal tests and a live mode requiring existing host authentication.
  - Record host/version/time/case/verdict/profile/finding outcomes without prompt contents or credentials.
- **Dependencies**: T016
- **Verify**: Canned adapter, parser, expectation, failure, and recording tests pass without network/model access.
- **Covers**: REQ-020, REQ-021, REQ-023, REQ-028, NFR-001, NFR-002; **Plan**: Component F / Phase 5 / PLD-006

### [x] T018 [P] Add authorization through persistence evaluation cases

- **Outcome**: Synthetic cases cover authorization/trust, command/process, filesystem/path, parsing/configuration, and persistence/state profiles with concrete expected defects and no reused external source.
- **Paths**: `tests/evals/review_code/cases/authorization-bypass/`, `tests/evals/review_code/cases/command-quoting/`, `tests/evals/review_code/cases/filesystem-traversal/`, `tests/evals/review_code/cases/parsing-invalid-default/`, `tests/evals/review_code/cases/persistence-roundtrip/`
- **Dependencies**: T017
- **Verify**: Corpus schema/setup tests pass and each case declares expected profiles, minimum findings, forbidden speculation, and verdict.
- **Covers**: REQ-013, REQ-014, REQ-018, REQ-023, REQ-028, NFR-002; **Plan**: Component F / Phase 5

### [x] T019 [P] Add network through build and clean evaluation cases

- **Outcome**: Synthetic cases cover network/provider, concurrency/lifecycle, public API/CLI, secrets/injection, build/dependency, verification mutation safety, plus clean patches with adequate direct or indirect evidence.
- **Paths**: `tests/evals/review_code/cases/network-retry/`, `tests/evals/review_code/cases/concurrency-cancellation/`, `tests/evals/review_code/cases/api-compatibility/`, `tests/evals/review_code/cases/secrets-redaction/`, `tests/evals/review_code/cases/build-manifest-drift/`, `tests/evals/review_code/cases/verification-mutation/`, `tests/evals/review_code/cases/clean-refactor/`, `tests/evals/review_code/cases/clean-indirect-test/`
- **Dependencies**: T017
- **Verify**: Corpus schema/setup tests pass; the mutation case requires mirror/rejection evidence and an unchanged project tree; clean cases prohibit speculative findings and expect PASS where all evidence is available.
- **Covers**: REQ-013, REQ-014, REQ-017, REQ-018, REQ-023, REQ-028, NFR-001, NFR-002, NFR-003; **Plan**: Component B / Component F / Phase 5

### [x] T020 Run targeted deterministic verification

- **Outcome**: Resolver, template, workflow, installer, translation, docs, and evaluation-harness tests all pass before broad validation.
- **Dependencies**: T003, T005, T009, T011, T013, T014, T015, T018, T019
- **Verify**:
  - `uv run pytest tests/scripts/bash/test_review_context.py tests/scripts/powershell/test_review_context.py -q`
  - `uv run pytest tests/test_review_code_templates.py tests/test_sdd_workflow_templates.py tests/test_codex_integration.py tests/commands/test_installer.py -q`
  - `uv run pytest tests/test_translation_files.py tests/test_review_code_docs.py tests/test_review_code_eval.py -q` using the actual selected docs-test path
  - `uv run ruff check src/ tests/`
- **Covers**: REQ-001 through REQ-028, NFR-001 through NFR-004; **Plan**: Component E / Component F / Phase 5

### [x] T021 Run full project and packaging verification

- **Outcome**: The complete repository remains green after the feature.
- **Dependencies**: T020
- **Verify**:
  - `uv run pytest`
  - `uv run ruff check .`
  - `uv run mkdocs build --strict`
  - Build wheel/sdist, inspect required files, and run `twine check`.
  - Confirm `git diff --check` is clean.
- **Covers**: REQ-006, REQ-007, REQ-027, NFR-001, NFR-002, NFR-003; **Plan**: Component D / Component E / Phase 5

### [x] T022 Execute and record the complete live model evaluation

- **Outcome**: One supported authenticated host runs every synthetic case successfully, and `.codexspec/specs/2026-0713-2221gs-review-code-reliability/review-code-eval-results.json` records complete per-case evidence.
- **Path**: `.codexspec/specs/2026-0713-2221gs-review-code-reliability/review-code-eval-results.json`
- **Dependencies**: T021
- **Work**:
  - Initialize temporary projects from current sources and invoke the real installed review command.
  - Require every case to meet expected profile, minimum finding, forbidden finding, and verdict constraints.
  - Investigate and fix only verified protocol defects through the owning prior task, rerun deterministic gates, then rerun the complete corpus.
  - Do not mark complete with skipped, missing, or selectively rerun cases.
- **Verify**: Runner exits zero; record schema is valid; case count equals corpus count; all cases pass; no credential or external-source detail is present.
- **Covers**: REQ-013, REQ-014, REQ-018, REQ-020, REQ-021, REQ-023, REQ-028, NFR-001, NFR-002; **Plan**: Component F / Phase 5 / PLD-006

**Final Checkpoint**: Deterministic CI contracts are green, distributions contain the required artifacts, documentation is migrated, and real reviewer behavior passes the complete recorded corpus.

## Dependencies and Execution Order

```text
T001 -> T002 -> T003 --+
  |                     +-> T006 -> T007 -> T008 -> T009 -> T010 -> T011
  +-> T004 -> T005 -----+                                      |
                                                                +-> T012 -> T013 --+
                                                                |       +-> T014 --+-> T015
                                                                |
T008 -> T016 -> T017 -> T018 --+                                |
                         T019 --+--------------------------------+-> T020 -> T021 -> T022
```

- T002 and T004 can run in parallel after T001.
- T003 and T005 can run in parallel after their respective failing tests.
- T013 and T014 can run in parallel after T012 because they edit disjoint metadata and documentation files.
- T018 and T019 can run in parallel after T017 because they own disjoint case directories.
- T020 is the convergence point for all implementation and deterministic evidence.
- The graph is acyclic; no task depends on live model output before deterministic gates pass.

## Plan Component Coverage

| Plan Component / Decision | Tasks | Result |
|---|---|---|
| Component A: Cross-Platform Resolver | T001-T006 | Full |
| Component B: Review Coordinator | T007-T009 | Full |
| Component C: Implement-Tasks Loop | T010-T011 | Full |
| Component D: Distribution/Migration | T006, T009, T012-T015 | Full |
| Component E: Deterministic Tests | T001-T002, T004, T006-T007, T009-T010, T012, T015, T020-T021 | Full |
| Component F: Model Evaluation | T016-T019, T022 | Full |
| PLD-001: Two JSON contracts | T001-T005, T007-T011, T016-T017 | Full |
| PLD-002: Separated command branches | T007-T008 | Full |
| PLD-003: Merged inventory records | T001-T005 | Full |
| PLD-004: Capability-aware delegation | T007-T009 | Full |
| PLD-005: Shared parity fixtures | T001-T005 | Full |
| PLD-006: Development-only evaluation | T016-T019, T022 | Full |
| PLD-007: Localized migration note | T012-T014 | Full |

## Requirements Coverage

| Requirement | Tasks | Result |
|---|---|---|
| REQ-001 | T007-T008, T012-T014, T020 | Full |
| REQ-002 | T001-T005, T020 | Full |
| REQ-003 | T001-T005, T007-T008, T020 | Full |
| REQ-004 | T001-T005, T020 | Full |
| REQ-005 | T001-T005, T020 | Full |
| REQ-006 | T002-T005, T007-T009, T012-T015, T020-T021 | Full |
| REQ-007 | T001-T006, T009, T015, T020-T021 | Full |
| REQ-008 | T002-T005, T007-T009, T020 | Full |
| REQ-009 | T002-T005, T007-T008, T010-T011, T020 | Full |
| REQ-010 | T007-T008, T020 | Full |
| REQ-011 | T001-T005, T007-T008, T020 | Full |
| REQ-012 | T007-T008, T020 | Full |
| REQ-013 | T007-T008, T018-T020, T022 | Full |
| REQ-014 | T007-T008, T018-T020, T022 | Full |
| REQ-015 | T007-T008, T020 | Full |
| REQ-016 | T007-T008, T020 | Full |
| REQ-017 | T007-T008, T019-T020 | Full |
| REQ-018 | T007-T008, T010-T011, T016, T018-T020, T022 | Full |
| REQ-019 | T007-T008, T020 | Full |
| REQ-020 | T007-T011, T016-T017, T020, T022 | Full |
| REQ-021 | T007-T011, T016-T017, T020, T022 | Full |
| REQ-022 | T001-T005, T007-T008, T020 | Full |
| REQ-023 | T007-T008, T016-T020, T022 | Full |
| REQ-024 | T007-T008, T010-T011, T020 | Full |
| REQ-025 | T010-T011, T020 | Full |
| REQ-026 | T010-T011, T020 | Full |
| REQ-027 | T001-T002, T004, T006-T007, T009-T010, T012, T015, T020-T021 | Full |
| REQ-028 | T016-T019, T022 | Full |
| NFR-001 | T007-T008, T010-T011, T016-T022 | Full |
| NFR-002 | T012-T019, T021-T022 | Full |
| NFR-003 | T001-T006, T009, T015, T020-T021 | Full |
| NFR-004 | T007-T011, T016-T017, T020 | Full |

## Unmapped Tasks

None. T020 and T021 are required convergence gates for the approved verification strategy rather than optional polish.

## Unresolved Items

None. If T022 exposes a behavior that cannot be corrected from confirmed requirements and the approved plan, stop for a new decision rather than weakening an expectation or recording a partial pass.

## Implementation Log

- **T001-T006**: Bash resolver contract: 20 passed. Combined resolver/install/package gate: 30 passed, 12 skipped. All skips are native PowerShell execution cases on a host without `pwsh`; source presence and installation contracts pass locally, and the native suite remains mandatory on Windows CI.
- **T007-T008**: The old scorecard template failed all 13 new defect-gate contract tests. The rewritten default gate now passes all 13; legacy bare-path audit examples were removed and the scorecard remains isolated behind `--audit`.
- **T009**: Review template and integration verification: 54 passed across source-contract, Claude command, Codex skill, Claude-only, Codex-only, and combined installation paths.
- **T010-T011**: The legacy final-loop contract failed five strict-gate tests. The complete-feature invocation, envelope/topology validation, evidence-first repair flow, progress guards, and only-PASS completion contract now pass all six focused implement-tasks tests; no legacy loop marker remains.
- **T012-T014**: All 24 expected legacy metadata/documentation checks failed before migration. After updating command metadata, eight translation caches, eight command guides, and eight README summaries, 110 translation/docs/workflow tests pass.
