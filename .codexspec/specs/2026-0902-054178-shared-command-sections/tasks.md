# Tasks: Shared Command Sections

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Input**: `.codexspec/specs/2026-0902-054178-shared-command-sections/`
**Prerequisites**: `requirements.md`, `spec.md`, `design.md`, `plan.md`

## 1. Byte-Preserving Fragment Renderer

### T001 — Define the renderer contract with failing tests

- [x] Add `tests/test_command_template_fragments.py` with isolated temporary source, fragment, and output roots. Verify the exact directive grammar, raw-byte rendering, validation failures, and write/check behavior before implementation.
  **Outcome**: A failing executable contract covers the complete generic renderer behavior without extracting any project command content.
  **Paths**: `tests/test_command_template_fragments.py`
  **Dependencies**: None
  **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001; **Plan**: Phase 1

**Test Scenarios:**

- `T001-S01`: One command source references one fragment and renders the exact expected bytes.
- `T001-S02`: Multiple command sources and repeated directives reuse the same fragment without special-case configuration.
- `T001-S03`: One command source references multiple distinct fragments in source order.
- `T001-S04`: UTF-8 content, LF, CRLF, and a directive at end of file are preserved according to the byte-replacement contract.
- `T001-S05`: A missing fragment fails with the source and requested fragment identified.
- `T001-S06`: A directive or malformed reserved line inside any fragment, including an unused fragment, is rejected as forbidden nesting or malformed content.
- `T001-S07`: Empty, POSIX/Windows absolute or drive-qualified, stream-qualified, forbidden-character, device-name, non-UTF-8, Unicode-normalization/case-colliding, case- or spelling-aliased, non-lowercase-extension, dot-segment, parent-traversal, backslash-traversal, resolved-outside-root, and symlinked source/fragment/output paths are rejected consistently across platforms, including unused fragment entries and the complete output namespace.
- `T001-S08`: Standalone reserved-comment text that does not match the complete grammar—including indentation, case, or misspelling variants—is rejected rather than partially expanded, while inline syntax examples remain literal bytes.
- `T001-S09`: Check mode fails for an absent matching output and for a byte-stale output without modifying either tree.
- `T001-S10`: Write mode prevalidates the full render set and complete portable output namespace, rechecks source/fragment state, and writes nothing when any source or output is invalid, colliding, changed, or symlinked.
- `T001-S11`: Write mode atomically replaces changed opted-in outputs, preserves existing permissions, and leaves byte-identical outputs untouched.
- `T001-S12`: Complete command templates with no same-named internal source remain outside renderer ownership and are never modified.

### T002 — Implement the maintainer renderer and CLI

- [x] Implement the tested byte renderer in `internal/command_template_fragments.py`, including safe path resolution, non-nesting validation, full render-set prevalidation, atomic write mode, read-only check mode, diagnostics, and nonzero failure status.
  **Outcome**: The T001 contract passes using only the Python standard library.
  **Paths**: `internal/command_template_fragments.py`
  **Dependencies**: T001
  **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001; **Plan**: Phase 2, Decision 1

**Test Scenarios:**

- `T002-S01`: Implementation passes `T001-S01` through `T001-S04` for literal, ordered, byte-exact rendering.
- `T002-S02`: Implementation passes `T001-S05` through `T001-S08` for missing, nested, unsafe, and malformed references.
- `T002-S03`: Implementation passes `T001-S09` through `T001-S12` for read-only checking, prevalidation, atomic replacement, and opt-in ownership.

### T003 — Add the empty opt-in scaffold and repository check

- [x] Add `internal/command_templates/sources/.gitkeep` and `internal/command_templates/fragments/.gitkeep`, then add a repository-level test that runs check mode against these roots and `templates/commands/`. Do not add a command source or real fragment.
  **Outcome**: The repository has a usable but content-neutral opt-in mechanism and its actual state is validated by the normal test suite.
  **Paths**: `internal/command_templates/sources/.gitkeep`, `internal/command_templates/fragments/.gitkeep`, `tests/test_command_template_fragments.py`
  **Dependencies**: T002
  **Covers**: REQ-001, REQ-004, REQ-005, NFR-001; **Plan**: Phases 2-3, Decision 2

**Test Scenarios:**

- `T003-S01`: Repository check succeeds with no opted-in command sources and does not treat `.gitkeep` as a command source or fragment.
- `T003-S02`: Repository check is read-only and leaves every existing `templates/commands/*.md` byte unchanged.

## 2. Independent Distribution Validation

### T004 — Define self-bootstrap distribution checks with failing tests

- [x] Extend `tests/test_command_template_fragments.py` with temporary-output comparisons that exercise the existing Claude installer and Codex skill generator against tracked self-bootstrap artifacts.
  **Outcome**: Failing tests specify how distributed artifacts are checked without adding fragment logic to existing consumers.
  **Paths**: `tests/test_command_template_fragments.py`
  **Dependencies**: T002
  **Covers**: REQ-006, REQ-007, NFR-001, NFR-003; **Plan**: Phase 4

**Test Scenarios:**

- `T004-S01`: Expected Claude distributed commands generated in a temporary root match every tracked distributed `.claude/commands/codexspec/` artifact.
- `T004-S02`: Documented maintainer-only commands and the two pre-existing plugin-only review-command compatibility artifacts are excluded without deletion, rewriting, or masking a missing distributed command.
- `T004-S03`: Expected Codex skills generated in a temporary root match every tracked distributed `.agents/skills/codexspec-*` artifact.
- `T004-S04`: A stale, missing, unexpected, or CRLF-only byte-drifted distributed Claude command causes the distribution check to fail.
- `T004-S05`: A stale, missing, unexpected, or CRLF-only byte-drifted distributed Codex skill causes the distribution check to fail, and expected generation is deterministic when the ambient platform is Windows.

### T005 — Implement the read-only self-bootstrap preflight

- [x] Add the maintainer-side distribution-check interface to `internal/command_template_fragments.py` or a tightly scoped sibling under `internal/`, using existing installer/integration functions and temporary directories.
  **Outcome**: T004 passes, and maintainers have one non-mutating preflight for source/output integrity plus Claude/Codex self-bootstrap synchronization.
  **Paths**: `internal/command_template_fragments.py` and, only if separation is required, `internal/check_command_distribution.py`
  **Dependencies**: T004
  **Covers**: REQ-006, REQ-007, NFR-001, NFR-003; **Plan**: Phase 4, Decision 5

**Test Scenarios:**

- `T005-S01`: Preflight passes `T004-S01` through `T004-S03` for current synchronized distributed artifacts.
- `T005-S02`: Preflight passes `T004-S04` and `T004-S05` by reporting channel-specific stale, missing, and unexpected artifacts without modifying them.

### T006 — Verify every packaged distributed command

- [x] Expand `tests/test_package_contents.py` so built wheel and sdist archives enumerate every `templates/commands/*.md` file, match the tracked complete-template set and bytes exactly, and contain no unresolved fragment directive marker.
  **Outcome**: Post-build archive inspection independently proves that all published commands are complete and current.
  **Paths**: `tests/test_package_contents.py`
  **Dependencies**: T002
  **Covers**: REQ-006, NFR-001, NFR-003; **Plan**: Phase 4, Decision 5

**Test Scenarios:**

- `T006-S01`: A freshly built wheel contains exactly the tracked distributed command set with byte-identical contents.
- `T006-S02`: A freshly built sdist contains exactly the tracked distributed command set with byte-identical contents.
- `T006-S03`: Archive verification fails when a packaged command is missing, unexpected, byte-stale, duplicated, aliased, or stored beneath a nested command path.
- `T006-S04`: Archive verification fails when any packaged command contains a valid or malformed standalone fragment directive, while inline syntax examples remain literal command content.

## 3. CI and Release Gates

### T007 — Wire the normal project-validation gate

- [x] Update `.github/workflows/ci.yml` path filters so changes beneath `internal/command_templates/` or to `internal/command_template_fragments.py` trigger CI, and ensure the ordinary test job executes the repository check from T003.
  **Outcome**: Fragment-only maintenance changes cannot bypass the cross-platform project test gate.
  **Paths**: `.github/workflows/ci.yml`
  **Dependencies**: T003
  **Covers**: REQ-005, NFR-003; **Plan**: Phase 3

**Verification:**

- Validate workflow YAML and confirm both internal paths appear in push and pull-request filters.
- Confirm the existing test job reaches `tests/test_command_template_fragments.py` without a fragment-specific runtime installation step.

### T008 — Wire the package-build and official-release gates

- [x] Invoke the read-only fragment/self-bootstrap preflight before archive creation in both `.github/workflows/ci.yml` and `publish.sh`; keep the existing post-build package-content test after archive creation.
  **Outcome**: Official build and release paths abort before packaging/upload when fragment or self-bootstrap state is invalid or stale.
  **Paths**: `.github/workflows/ci.yml`, `publish.sh`
  **Dependencies**: T005, T006, T007
  **Covers**: REQ-006, NFR-003; **Plan**: Phase 4, Decision 3

**Verification:**

- Validate workflow YAML and run ShellCheck or the repository's existing shell validation on `publish.sh`.
- Confirm both paths call read-only preflight before `python -m build` or `uv build` and never call write mode.
- Confirm package-content tests still run against freshly built archives.

## 4. Maintainer Guidance and Compatibility

### T009 — Document the opt-in ownership rule

- [x] Update `.codexspec/memory/constitution.md`, `CLAUDE.md`, and `docs/internal/repository-layout.md` to explain internal fragment sources, explicit write/check workflows, same-basename ownership, direct editing for commands without a same-named internal source, generated-output handling, and the prohibition on shipping internal authoring sources.
  **Outcome**: Maintainers can identify the correct editable source for every command without changing user-facing documentation or presenting fragments as an end-user feature.
  **Paths**: `.codexspec/memory/constitution.md`, `CLAUDE.md`, `docs/internal/repository-layout.md`
  **Dependencies**: T003, T005
  **Covers**: REQ-004, REQ-007, NFR-002; **Plan**: Phase 5

**Verification:**

- Confirm all three documents agree that `internal/` authoring files never ship and `templates/commands/` remains the complete distribution boundary.
- Confirm guidance distinguishes opted-in generated templates from directly maintained templates for commands without a same-named internal source.
- Confirm no end-user `codexspec init` instruction or behavior is added.

### T010 — Run final compatibility and distribution verification

- [x] Run formatting/lint checks, focused fragment and package tests, the complete test suite, a fresh wheel/sdist build with archive inspection, self-bootstrap preflight, and `git diff --check`; verify no existing command was opted in and no `templates/commands/*.md` bytes changed.
  **Outcome**: The implementation is proven complete without extracting content or changing `codexspec init` behavior or output.
  **Paths**: Repository-wide verification only; no new production path
  **Dependencies**: T001-T009
  **Covers**: REQ-005, REQ-006, REQ-007, NFR-001, NFR-002, NFR-003; **Plan**: Phase 5

**Test Scenarios:**

- `T010-S01`: Focused renderer tests pass for every scenario `T001-S01` through `T006-S04` applicable without built archives.
- `T010-S02`: Full pytest and lint suites pass on the completed tree.
- `T010-S03`: Fresh wheel and sdist pass all archive-content scenarios `T006-S01` through `T006-S04`.
- `T010-S04`: Self-bootstrap preflight passes for both Claude commands and Codex skills.
- `T010-S05`: Git comparison shows no opted-in real command source, no real fragment, and no byte change under `templates/commands/`.
- `T010-S06`: Existing installer, translation, and Codex integration tests demonstrate unchanged consumer behavior.

## Dependencies

```text
T001 -> T002 -> T003 -> T007 --+
          |                     |
          +----> T004 -> T005 --+--> T008
          |                     |
          +----> T006 ----------+

T003 + T005 -> T009
T001-T009 -> T010
```

## Coverage and Scenario Mapping

| Requirement / Plan Component | Tasks | Scenario Coverage |
|------------------------------|-------|-------------------|
| REQ-001 / Generic source and fragment reuse | T001, T002, T003 | T001-S01 to T001-S03; T002-S01; T003-S01 |
| REQ-002 / Literal byte insertion | T001, T002 | T001-S01 to T001-S04; T002-S01 |
| REQ-003 / No nesting and safe references | T001, T002 | T001-S05 to T001-S08; T002-S02 |
| REQ-004 / Synchronization and ownership | T001, T002, T003, T009 | T001-S09 to T001-S12; T002-S03; T003-S01 to T003-S02 |
| REQ-005 / Project validation | T001, T002, T003, T007, T010 | T001-S05 to T001-S10; T002-S02 to T002-S03; T003-S01; T010-S01 to T010-S02 |
| REQ-006 / Distribution validation | T004, T005, T006, T008, T010 | T004-S01 to T004-S05; T005-S01 to T005-S02; T006-S01 to T006-S04; T010-S03 to T010-S04 |
| REQ-007 / Existing consumers remain fragment-unaware | T004, T005, T009, T010 | T004-S01 to T004-S05; T005-S01 to T005-S02; T010-S04 to T010-S06 |
| NFR-001 / Byte-for-byte compatibility | T001-T006, T010 | T001-S01 to T001-S04; T001-S09 to T001-S12; T002-S01 to T002-S03; T003-S02; T004-S01 to T004-S05; T006-S01 to T006-S04; T010-S03 to T010-S05 |
| NFR-002 / Unchanged `codexspec init` behavior | T009, T010 | T010-S05 to T010-S06 |
| NFR-003 / Pre-user detection | T004-T008, T010 | T004-S01 to T004-S05; T005-S01 to T005-S02; T006-S01 to T006-S04; T010-S03 to T010-S04 |

## Unmapped Tasks

None.
