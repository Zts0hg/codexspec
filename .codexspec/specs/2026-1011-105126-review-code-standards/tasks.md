# Implementation Tasks: Evidence-Based Review with On-Demand Standards

**Authority**: [requirements.md](requirements.md) → [spec.md](spec.md) → [design.md](design.md) → [plan.md](plan.md)
**Workspace**: `2026-1011-105126-review-code-standards`
**Status**: Implementation and verified repair work complete; terminal acceptance is recorded in the external review state

## Phase 1: Executable boundaries

- [x] **T001 — Persist and read independent maintenance policy.** Add test-first coverage in `tests/test_config_auto_maintenance.py`; implement policy helpers in `src/codexspec/review_maintenance.py`, config option/normalization/display/routing in `src/codexspec/__init__.py`, and fresh default in `src/codexspec/i18n.py`. Use existing token parsing and surgical writer. Outcome: config persists a boolean, reads missing as true, and repair policy is independent of auto-next.
  - Dependencies: none.
  - Covers: REQ-010, REQ-011; Plan: Phase 1.
  - Test Scenarios:
    - **P01**: absent file/key defaults true; explicit YAML true/false resolve accurately.
    - **P02**: confirmed on/off aliases, case and whitespace normalize; invalid setter input fails without writes.
    - **P03**: block/flow YAML and CRLF/Unicode comments preserve unrelated bytes and auto-next through set/toggle.
    - **P04**: real CLI set, bare toggle and display use destination configuration; routed writes preserve the source checkout.
    - **P05**: invalid explicit policy, YAML or workflow shape refuses automatic maintenance rather than guessing.
    - **P06**: genuinely absent configuration defaults on; present dangling/cyclic links refuse optional maintenance; readable linked true/false policies preserve their value and content.

- [x] **T002 — Validate target-bound maintenance reports.** Add test-first companion tests in `tests/test_review_maintenance.py` and implement strict parser/validator in `src/codexspec/review_maintenance.py`. Outcome: only one complete, target-correlated companion can supply suggestions.
  - Dependencies: T001.
  - Covers: REQ-007, REQ-009, REQ-010, REQ-014; Plan: Phase 1.
  - Test Scenarios:
    - **M01**: valid empty and evidenced nonempty companions parse.
    - **M02**: absent/duplicate blocks, malformed JSON, unknown fields and unsupported versions fail.
    - **M03**: mismatched fingerprint, duplicate IDs, empty benefit/evidence, unsafe affected paths and null identity with suggestions fail.

- [x] **T003 — Install shared standards for both integrations.** Add test-first `tests/test_review_standards.py`; implement `src/codexspec/review_standards.py` and wire normal init/update in `src/codexspec/__init__.py`. Outcome: complete byte-identical resources are shared without overwriting unrelated project extensions.
  - Dependencies: none; installation tests use a small valid source tree until T004.
  - Covers: REQ-005, REQ-007, REQ-012, NFR-002; Plan: Phase 1.
  - Test Scenarios:
    - **D01**: initial copy supplies all source resources byte-for-byte.
    - **D02**: nonforced update preserves existing edits; forced update refreshes distributed files and preserves unrelated extension files.
    - **D03**: unsafe symlink/hardlink destinations are refused before copies.
    - **D04**: real initialization under claude, codex and both supplies the same usable tree.

## Phase 2: Runtime standards and integration

- [x] **T004 — Author compact standards and source-item mapping.** Create `templates/review-code/` with the confirmed index/common/mode/dimension/language/framework organization. Move existing mode/scoring/appendix intent into applicable resources. Add `references/checklist-integration.md` beside the original snapshot with every source bullet's concrete destination, treatment and rationale.
  - Dependencies: none.
  - Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-013, REQ-014, NFR-001, NFR-002; Plan: Phase 2.
  - Verification: index paths resolve; all seven dimensions carry applicability/evidence/false-positive/completion guidance; every source bullet maps to a real checkpoint; language-bound examples stay specialized; technical topics remain sections; existing score weights/rubrics remain.

- [x] **T005 — Coordinate runtime loading and plugin delivery.** Update `internal/command_templates/sources/review-code.md` and `.claude-plugin/marketplace.json`. Outcome: one selected root supplies common plus selected-mode procedures, detailed standards follow semantic applicability, and plugin resources are contained in its existing package.
  - Dependencies: T004.
  - Covers: REQ-001, REQ-005, REQ-006, REQ-007, REQ-012, NFR-002; Plan: Phase 2.
  - Verification: mutually exclusive arguments/resolver remain; mode bodies and language checklists are not re-inlined; project root is preferred, partial trees do not silently mix versions; marketplace declares a contained commands directory and full resource root.

- [x] **T006 — Consume maintenance policy in automatic repair.** Update `internal/command_templates/sources/implement-tasks.md`, `config.md` and relevant configuration guidance. Inspect `quick.md`/`auto-dev.md`/other review callers and ensure repair reaches the same policy. Outcome: default review always reports maintenance; callers independently verify and apply enabled suggestions, retain unfinished work, recheck edits and require completion without adding invocation flags.
  - Dependencies: T001, T002, T004, T005.
  - Covers: REQ-007, REQ-009, REQ-010, REQ-011, REQ-014; Plan: Phase 2.
  - Verification: companion validation matches shipping validator; disabled policy affects application only; actual defects/verification remain mandatory; no auto-next coupling, per-run override or preceding-stage forwarding; no pending enabled maintenance at terminal success.

## Phase 3: Evaluation and documentation

- [x] **T007 — Verify relocated mode and package contracts.** Adapt `tests/test_review_code_templates.py` and related template tests to inspect reachable selected-mode resources. Extend `tests/test_package_contents.py` and standards integration checks. Outcome: existing argument, resolver, strict schema, isolation, incremental and scoring behavior remains protected after relocation.
  - Dependencies: T003, T004, T005, T006.
  - Covers: REQ-005, REQ-007, REQ-010, REQ-011, REQ-012, NFR-002; Plan: Phase 3.
  - Test Scenarios:
    - **C01**: runtime entry points resolve the selected resources; every index path is contained and available.
    - **C02**: mode contracts, strict defect envelope and scoring survive relocation, while repair caller validates required companion/policy.
    - **C03**: wheel/sdist contain exact resource bytes and exclude maintainer-only authoring.

- [x] **T008 — Evaluate discovery and restraint using concrete evidence.** Extend `tests/evals/review_code/run_eval.py`, its case fixtures and `tests/test_review_code_eval.py`. Outcome: evidence-specific checks reject hollow responses and support compatible legacy defect fixtures.
  - Dependencies: T002, T004, T005, T006.
  - Covers: REQ-001, REQ-003, REQ-004, REQ-006, REQ-007, REQ-009, REQ-010, REQ-014, NFR-001; Plan: Phase 3.
  - Test Scenarios:
    - **E01**: a real triggering input is distinguished from the same candidate prevented by an evidenced upstream guarantee.
    - **E02**: missing required behavior activates coverage despite absent implementation.
    - **E03**: tracing an unchanged cross-language dependency activates relevant detail and excludes unrelated detail.
    - **E04**: substantiated present maintenance is reported separately; speculative future refactoring is rejected; hollow benefit/trace evidence fails evaluation.

- [x] **T009 — Document current user behavior and maintainer boundaries.** Update `README.md`, `docs/en/reference/cli.md`, `docs/en/user-guide/commands.md`, `CLAUDE.md`, `docs/internal/repository-layout.md` and corresponding localized references where project gates require parity. Outcome: users understand configuration, default advice/application, mode selection, resource paths and loading.
  - Dependencies: T005, T006.
  - Covers: REQ-005, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, NFR-002; Plan: Phase 3.
  - Verification: documented commands execute; on/off is canonical and YAML boolean; maintainer versus initialized paths are explicit; frontmatter catalogs remain consistent.

## Phase 4: Distribution and independent acceptance

- [x] **T010 — Regenerate distribution and establish green baseline.** Run renderer, normal worktree initialization for both integrations, targeted/full pytest, Ruff, Markdown, fragment, archive and applicable docs gates. Outcome: complete sources, distributions and installed assets agree and mandated checks pass.
  - Dependencies: T001–T009.
  - Covers: REQ-007, REQ-010, REQ-011, REQ-012, REQ-014, NFR-002; Plan: Phase 4.
  - Verification: actual command outcomes recorded; main checkout unchanged; tests import selected worktree; temporary fixtures outside Git roots.

- [x] **T011 — Complete fresh isolated review and configured distillation.** Freeze selected target evidence, invoke the complete feature gate with a fresh non-fork reviewer and required specialists. Independently verify and repair admitted defects/enabled maintenance, repeat relevant checks and fresh reviews until terminal rules pass. Run non-blocking distill at successful completion; retain worktree.
  - Dependencies: T010.
  - Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-007, REQ-010, REQ-014, NFR-001; Plan: Phase 4.
  - Verification: complete isolated review, current fingerprint, full coverage, green checks, zero admitted defects, no blocking gaps or unfinished enabled maintenance. No publication, push or merge is required.

## Coverage

| Plan Unit / Requirements | Tasks |
|--------------------------|-------|
| Phase 1 / REQ-007, REQ-009–REQ-012, REQ-014, NFR-002 | T001, T002, T003 |
| Phase 2 / REQ-001–REQ-014, NFR-001, NFR-002 | T004, T005, T006 |
| Phase 3 / REQ-001, REQ-003–REQ-012, REQ-014, NFR-001, NFR-002 | T007, T008, T009 |
| Phase 4 / REQ-001–REQ-004, REQ-007, REQ-010–REQ-012, REQ-014, NFR-001, NFR-002 | T010, T011 |
| P01–P06 | T001 |
| M01–M03 | T002 |
| D01–D04 | T003 |
| C01–C03 | T007 |
| E01–E04 | T008 |

No unmapped tasks. Dependencies are ordered and acyclic; no parallel marker is needed.

## Execution Evidence

Record completed checks, scenario-to-test mapping and review repairs here as execution proceeds.

### Boundary verification

Initial red run: three expected missing-module collection failures. After executable implementation, 48 checks passed with three expected missing-library init failures. After standards and installation wiring, all 51 targeted configuration/report/installation tests passed. T004 maps every one of the 87 original bullets to concrete standard checkpoints; T005 preserves defect schema-v3 and the existing resolver. T006 adds separate maintenance validation/application without a new implementation invocation option.

### Runtime, evaluation and documentation verification

The offline relocated-mode/package contracts and evaluator checks passed: 98 combined tests, followed by 60 evaluator tests including concrete positive and mutated hollow-evidence responses. The corpus checks evidence-specific expectations; this is not a live-model recall benchmark. The public guarantee/bypass fixture was executed to establish its premise. After retaining the host-rendered explicit-path usage example, 126 integration/installer/evaluator/resource tests passed.

Scenario mapping: P01–P06 → `tests/test_config_auto_maintenance.py`; M01–M03 → `tests/test_review_maintenance.py`; D01–D04 and C01/C02 → `tests/test_review_standards.py` plus `tests/test_review_code_templates.py`; C03 → `tests/test_package_contents.py`; E01–E04 → concrete case fixtures and the positive/negative checks in `tests/test_review_code_eval.py`.

Full Python suite: 2071 passed, 54 skips for platform-dependent or opt-in checks (88.30 seconds). Wheel and sdist built successfully; explicit archive verification passed all 18 package/resource checks after formatter outputs were incorporated into fresh archives. Ruff, format, mypy, Bandit, whitespace/EOF, merge-conflict and Markdown hooks passed. Full pytest ran separately from duplicate hook execution. Normal `init . --force --ai both` regenerated derived commands and installed byte-identical runtime resources. Fragment distribution verification, diff whitespace checks, selected-worktree imports, original checklist SHA-256 and protected-main cleanliness passed.

Eight-language MkDocs strict build passed. The structure checker passed with zero errors/warnings against an external temporary view containing the eight locale directories, excluding maintainer directories. The existing completeness heuristic reports technical tokens and non-English Latin text as untranslated, and is not treated as semantic translation evidence. All new policy/load guidance was authored in each locale. Dependency audit is being checked against the selected development environment rather than the separate `uv tool` environment; environment-only preparation does not change the feature's manifests or lockfile.

### Acceptance preparation

The final selected-workspace environment passed the full suite again (2071 passed, 54 skips for platform-dependent or opt-in checks; 89.86 seconds). The final eight-language strict documentation build passed. `uv pip check --python .venv/bin/python` confirmed all 62 installed packages are compatible. The dependency audit against this complete environment passed with no known vulnerabilities outside the two exceptions already covered by the repository's existing CVE-2026-4539 policy.

Environment preparation updated development-environment packages only: anyio 4.14.2, idna 3.15, pytest 9.0.3, requests 2.33.0, pymdown-extensions 11.0.1, urllib3 2.8.0, mkdocs-material 9.7.7, virtualenv 21.7.13 and python-discovery 1.6.2. The two large wheels fetched through a mirror were checked against their official PyPI SHA-256 values before installation. The feature's dependency declarations and uv.lock remain unchanged. Earlier vulnerability and network-failure logs are retained outside the repository alongside the final successful checks.

The original complete-review manifest became stale when origin/main moved externally; the merge-base, selected entry bytes and raw diffs were unchanged. That frozen round is retained as nonterminal evidence. A new complete gate must bind its result to a freshly resolved manifest, include the required independent filesystem/configuration specialist, and reproduce the current target fingerprint before acceptance.

T010's implementation, generation, test, type, security-lint, Markdown, archive, documentation and dependency checks are complete. Independent acceptance is the remaining T011 work. The source checkout remains clean, and all implementation/artifact writes stay in the selected feature workspace.

### Independent review and verified maintenance

The completed isolated primary and filesystem/configuration specialist assessed all 131 entries, 15 contracts and 11 partitions. Their complete defect result is PASS with zero P0–P3 findings; O-001 and O-002 are verified. External base-reference movement changed only manifest metadata: all selected source/dependency bytes, modes and raw diffs were unchanged, and the final result was reproduced within a stable continuous validation window. Superseded identity snapshots remain in the external review store.

M-001 was independently substantiated: the standalone React resource pointed to language exemplars "above" that exist in separate files. With the selected project's maintenance policy resolving to true, the source now links to the applicable TypeScript or JavaScript resource. Normal initialization refreshed the installed copy. Both links resolve; all 26 installed resources equal their sources; the language applicability, scoring and admission rules remain unchanged. A bounded search found no other stale positional resource reference.

Post-repair verification passed: the full suite has 2071 passed and 54 skips (100.02 seconds); freshly rebuilt wheel/sdist resource checks have 15 passed with the installing smoke deselected; Ruff check/format, the configured mypy hook, Bandit, Markdown, fragment distribution, diff checks and the eight-language strict documentation build pass. The ad-hoc local mypy invocation lacked PyYAML stubs; the project's declared hook environment includes them and passes without a product change. Earlier raw logs are preserved outside the repository.

The checked task entries record completed implementation, independent assessment and verified repair work. The remaining acceptance execution, current fingerprint and maintenance verification are recorded in the external review state for this frozen task record; successful delivery still requires the final complete isolated PASS and the configured non-blocking closing distillation. No terminal success is inferred from task checkboxes.

### Resource-destination regression and guide clarification

The later complete isolated review substantiated one P2 installation defect: a directory occupying a required Markdown destination was preserved as though it were a regular file, or caused a forced installation to fail after earlier copies. The caller independently reproduced both public installer paths. D05 covers root/nested destinations with force off/on; D06 covers the real both-host CLI error and preservation of existing directory content. All five new cases failed before the fix. The installer's existing all-destination preflight now rejects non-file destinations before any resource copy; generic directory-path validation, regular-file preservation and unrelated extensions retain their contracts.

The independently verified documentation maintenance updates all eight localized guide paragraphs to state substantive-progress continuation, existing stop guards, no fixed round cap and fresh complete final review. It changes neither runtime behavior nor the independent automatic-maintenance configuration.

Post-repair checks passed: 60 targeted tests; 2076 full-suite tests with 54 platform/opt-in skips; Ruff check/format; the configured mypy environment; Bandit; 112 selected Markdown files; fragment distribution; diff checks; and the eight-language strict documentation build. Standard isolated wheel/sdist construction passed; 15 archive checks and a separate installed-wheel/worktree initialization smoke passed. All 26 resources and the four selected runtime modules are byte-identical in fresh archives. The optional non-isolated build attempt lacked the local hatchling backend; normal isolated construction succeeds without any product or dependency-declaration change. Dependency audit explicitly targeting the selected environment passed with only the two vulnerabilities covered by the existing CVE-2026-4539 exception.

A cross-feature file-installer preflight lesson is captured in the project profile as an outcome-verified candidate. Current external review records retain the installation behavior obligation and the separately keyed documentation-maintenance obligation until fresh independent verification. The implementation remains frozen during the next review; task checkboxes and these verification results do not substitute for terminal complete-feature acceptance.

### Policy-source regression and language-specific scoring clarity

A complete isolated review established that a present dangling or cyclic configuration link was treated as an absent policy source, enabling optional maintenance. Independent caller probes confirmed both cases. The P06 regression tests produced two expected failures and two passing readable-link compatibility cases before repair. The policy reader now inspects the entry with `lstat()`, defaults on only for true absence, and retains the existing actionable error and strict value validation for unreadable or invalid existing sources. Valid linked policies remain supported. The fix is confined to the new maintenance policy reader.

The separately verified Java/Kotlin maintenance clarifies seven current scoring examples using the selected language's mechanisms or explicit Java-interoperation conditions. All heading sequences and numerical deductions are preserved. Normal both-host initialization refreshed the corresponding installed resources. A bounded examination of related paired-language resources found no additional attributable repair obligation.

Post-repair checks passed: 64 targeted tests; 2084 full-suite tests with 50 platform/host skips, including the optional archive and isolated installed-wheel/worktree checks; Ruff check/format; configured mypy; Bandit; 113 selected Markdown files; fragment distribution; diff checks; the eight-language strict documentation build; and the dependency audit using the existing CVE-2026-4539 exception. Fresh wheel/sdist construction passed. All 26 resources and all 24 Python modules equal current source bytes in the archives; installed resources also equal their sources. Native Windows/PowerShell checks and live-model evaluation are not claimed by these results.

The project profile records the filesystem-absence lesson as an outcome-verified candidate. The caller independently maps all 20 enumerated task scenarios to tests asserting their expected behavior. Fresh review must re-establish the retained policy behavior and separate language-resource compatibility obligations; the external review state records the final current fingerprint and terminal acceptance.

### Delivery integration and Windows fixture verification

Integration with the current main branch retains version 0.7.23 and its guarded commit, project-history context and design-to-plan behavior. The repository-level marketplace root now declares its nested commands and startup hooks explicitly; the distributed commit command resolves its standalone helper under that same root. Both CLI-free plugin regression cases failed before the helper reference was corrected. All 118 affected integration tests and 18 current-package checks subsequently passed; the integration commit passed the full repository hooks. Plugin component-path propagation is recorded as a reusable candidate in the project profile.

PR CI run 38192250056 passed Linux, macOS, lint and documentation checks, but both Windows jobs rejected test assumptions: a UTF-8 command was read using the platform codec, and four link-preservation assertions compared Windows extended-length paths with their creation arguments. The command reader now selects UTF-8; link tests compare the observed target before and after reading while retaining policy behavior and target-content assertions. All 54 affected policy/plugin suites pass locally. Native Windows and complete updated-head CI remain required before merge; the interrupted old-fingerprint review supplies no acceptance for this changed target.
