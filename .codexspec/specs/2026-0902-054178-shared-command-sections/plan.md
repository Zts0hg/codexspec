# Implementation Plan: Shared Command Sections

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.

This is the implementation-planning stage AFTER design.md. It describes HOW to build the
confirmed design in phases — NOT what the system is.
-->

**Related Spec**: `.codexspec/specs/2026-0902-054178-shared-command-sections/spec.md`
**Related Design**: `.codexspec/specs/2026-0902-054178-shared-command-sections/design.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0902-054178-shared-command-sections/requirements.md`
**Created**: 2026-09-02
**Status**: Draft

## Context

This plan implements the confirmed maintainer-only fragment mechanism described in `design.md`. Existing user-facing command consumers remain untouched: complete files under `templates/commands/` continue to feed `codexspec init`, frontmatter translation, Codex skill generation, packaging, and plugin self-bootstrap. The implementation adds an incremental internal authoring path, deterministic byte rendering, and two pre-distribution validation layers without selecting or extracting any real command content.

## Goals / Non-Goals

**Goals:**

- Add a generic byte-preserving renderer for literal, non-parameterized, non-nested fragments.
- Let individual commands opt into internal fragment-managed sources without migrating unrelated commands.
- Provide explicit write and read-only check workflows for maintainers.
- Gate ordinary CI and official distribution paths against invalid, stale, or incompletely distributed command content.
- Update maintainer governance so generated and directly maintained templates have unambiguous ownership.

**Non-Goals:**

- Choosing, creating, or extracting any actual shared command fragment.
- Migrating any existing command into fragment management.
- Adding fragment behavior to runtime package code, `codexspec init`, or command execution.
- Supporting fragment parameters or nested fragments.

## Relevant Repository Constraints

- `templates/commands/` is currently the complete distributed-command boundary copied by `src/codexspec/commands/installer.py` and read by `src/codexspec/integrations/codex.py`.
- `internal/` is maintainer-only and excluded from wheel and sdist contents; final rendered templates must therefore remain under `templates/commands/`.
- Distributed command source rules in the constitution and `CLAUDE.md` currently direct all edits to `templates/commands/` and must be refined for opted-in generated files.
- CI runs on Python 3.11 and 3.12 across Linux, macOS, and Windows, allowing byte and newline behavior to be verified cross-platform.

## Plan-Level Decisions

### Decision 1: Implement the maintainer renderer with the Python standard library

**Context**: The mechanism is repository-local tooling, must operate consistently on all supported development platforms, and needs exact byte behavior.

**Options Considered**:

1. A small Python module and CLI using `pathlib`, byte I/O, and atomic `os.replace`.
2. Separate Bash and PowerShell renderers.
3. A third-party text-template engine.

**Decision**: Implement one Python module under `internal/` with a thin CLI and no new runtime or development dependency.

**Rationale**: Python is already mandatory for CodexSpec development, is portable across the CI matrix, and can preserve bytes without introducing a general templating language.

**Covers**: REQ-001, REQ-002, REQ-003, REQ-004; Design: Maintainer renderer and verifier, Fragment directive contract

**Decision Level**: Plan-level tooling choice; it does not change the confirmed design or user behavior.

### Decision 2: Build tests from isolated temporary authoring trees before repository integration

**Context**: The user explicitly retains responsibility for extracting real fragments, so the mechanism must be proven without modifying current command content.

**Options Considered**:

1. Test renderer behavior using temporary source, fragment, and output roots.
2. Extract an existing command section merely to exercise the feature.

**Decision**: Use temporary test fixtures for all rendering and failure cases, then run repository-level check mode against an initially empty opt-in source set.

**Rationale**: This validates the generic mechanism while respecting the confirmed exclusion of content selection and extraction.

**Covers**: REQ-001, REQ-005, NFR-001; Design: Maintainer command-source store, Literal fragment store, Project validation gate

**Decision Level**: Plan-level test sequencing; it does not select production content.

### Decision 3: Keep all automated gates read-only

**Context**: Tests or releases that silently rewrite generated files can hide stale committed output and produce unreviewed artifacts.

**Options Considered**:

1. Invoke check mode in automation and require maintainers to run write mode explicitly.
2. Regenerate automatically during CI or packaging.

**Decision**: CI, package inspection, and release scripts use only read-only checks; only the explicit maintainer write command may synchronize outputs.

**Rationale**: A stale tree fails deterministically and must be corrected in a visible source change plus generated-output diff.

**Covers**: REQ-004, REQ-005, REQ-006; Design: Project validation gate, Distribution gate, Decision 4

**Decision Level**: Plan-level automation policy implementing the design's synchronization boundary.

## Implementation Phases

### Phase 1: Specify the renderer contract with failing tests

**Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001; **Design**: Maintainer command-source store, Literal fragment store, Fragment directive contract, Maintainer renderer and verifier

- [ ] Add temporary-tree tests for one fragment referenced by one command, one fragment referenced repeatedly and from multiple commands, multiple fragments in one source, exact raw-byte and newline preservation, and preservation of all non-directive source bytes. — **Covers**: REQ-001, REQ-002, NFR-001; Design: Literal fragment store, Fragment directive contract, Maintainer renderer and verifier
- [ ] Add failure tests for a missing fragment, a directive inside a fragment, empty/absolute/traversing/escaping or Windows-aliased paths, symlinked sources/fragments/outputs, malformed standalone directive lines, an absent tracked output in check mode, and a rendered-versus-tracked byte mismatch; prove inline syntax examples remain literal. — **Covers**: REQ-003, REQ-005; Design: Fragment directive contract, Maintainer renderer and verifier, Check-mode result
- [ ] Add write-mode tests proving complete prevalidation, atomic per-output replacement, no writes on validation failure, and no modification of command templates without an opted-in source. — **Covers**: REQ-004, NFR-001; Design: Maintainer command-source store, Write-mode result

### Phase 2: Implement maintainer-only rendering and synchronization

**Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-007, NFR-001, NFR-002; **Design**: Maintainer command-source store, Literal fragment store, Fragment directive contract, Maintainer renderer and verifier, Existing command consumers

- [ ] Add the internal source and fragment scaffold without adding an opted-in command or real fragment; retain empty directories with repository-standard keep files where needed. — **Covers**: REQ-001; Design: Maintainer command-source store, Literal fragment store, Decision 2
- [ ] Implement byte-based directive parsing and safe fragment-path resolution for the exact standalone directive grammar. — **Covers**: REQ-001, REQ-002, REQ-003; Design: Fragment directive contract, Decision 3
- [ ] Implement deterministic render-set prevalidation, explicit write mode, and read-only check mode with source/reference/output diagnostics and meaningful nonzero exit status. — **Covers**: REQ-003, REQ-004, REQ-005, NFR-001; Design: Maintainer renderer and verifier, Check-mode result, Write-mode result
- [ ] Run the isolated tests across the existing test suite without changing `src/codexspec/commands/installer.py`, `src/codexspec/integrations/codex.py`, or any existing complete command bytes. — **Covers**: REQ-007, NFR-001, NFR-002; Design: Existing command consumers

### Phase 3: Add ordinary project validation

**Covers**: REQ-002, REQ-004, REQ-005, NFR-001, NFR-003; **Design**: Project validation gate, Maintainer renderer and verifier

- [ ] Add a repository contract test that invokes read-only check mode against the actual internal source/fragment roots and tracked complete templates. — **Covers**: REQ-004, REQ-005; Design: Project validation gate
- [ ] Extend CI trigger paths so changes to the exact maintainer source, fragment, and renderer paths always enter the cross-platform test workflow. — **Covers**: REQ-005, NFR-003; Design: Project validation gate
- [ ] Verify Linux, macOS, and Windows semantics through matrix-compatible tests, especially LF/CRLF and non-ASCII fragment bytes, portable path rejection, canonical self-bootstrap generation independent of the ambient host, and raw-byte drift detection. — **Covers**: REQ-002, REQ-005, NFR-001; Design: Project validation gate, Decision 3

### Phase 4: Add independent distribution validation

**Covers**: REQ-006, REQ-007, NFR-001, NFR-003; **Design**: Distribution gate, Existing command consumers

- [ ] Add a read-only self-bootstrap check that generates expected distributed Claude commands and Codex skills in temporary roots using the existing generators, then compares them with tracked distributed artifacts while excluding documented maintainer-only commands. — **Covers**: REQ-006, REQ-007, NFR-001, NFR-003; Design: Distribution gate, Existing command consumers, Decision 5
- [ ] Expand built-archive tests to enumerate every distributed command in both wheel and sdist, compare its bytes with the complete tracked template, and reject the fragment directive marker in packaged commands. — **Covers**: REQ-006, NFR-001, NFR-003; Design: Distribution gate, Decision 5
- [ ] Invoke fragment check mode and self-bootstrap validation explicitly in the CI package-build job before archive creation. — **Covers**: REQ-006, NFR-003; Design: Distribution gate
- [ ] Invoke the same read-only preflight in `publish.sh` before `uv build`, so the official release path aborts before upload on invalid or stale state. — **Covers**: REQ-006, NFR-003; Design: Distribution gate, Decision 4

### Phase 5: Document ownership and verify compatibility

**Covers**: REQ-004, REQ-005, REQ-006, REQ-007, NFR-001, NFR-002, NFR-003; **Design**: Maintainer guidance, Project validation gate, Distribution gate, Existing command consumers

- [ ] Update the project constitution's distributed-command source rule to state that opted-in outputs under `templates/commands/` are generated from their same-named internal source and must not be edited directly; retain the existing direct-edit rule for commands without a same-named internal source. — **Covers**: REQ-004, REQ-007, NFR-002; Design: Maintainer guidance, Decision 2
- [ ] Update `CLAUDE.md` and `docs/internal/repository-layout.md` with the maintainer workflow, internal/distribution boundary, write/check commands, and the prohibition on shipping fragment sources. — **Covers**: REQ-004, REQ-007, NFR-002; Design: Maintainer guidance, Decision 1
- [ ] Verify that no command has been opted in or had content extracted, all existing `templates/commands/*.md` bytes are unchanged, and installer/Codex integration behavior tests remain green. — **Covers**: REQ-007, NFR-001, NFR-002; Design: Existing command consumers, Decision 2
- [ ] Run lint, focused renderer/distribution tests, the complete test suite, archive inspection, and `git diff --check`. — **Covers**: REQ-005, REQ-006, NFR-001, NFR-002, NFR-003; Design: Project validation gate, Distribution gate

## Verification Strategy

- **Unit tests**: Directive recognition, path safety, raw-byte substitution, no parameters, no nesting, prevalidation, atomic write behavior, and diagnostics.
- **Repository contract test**: Read-only comparison of every opted-in internal source with its complete tracked output.
- **Compatibility tests**: Capture pre-feature hashes of every `templates/commands/*.md` file and assert the implementation-only change leaves them unchanged because no extraction is in scope.
- **Consumer regression tests**: Existing installer, translation, and Codex integration suites run unchanged against complete templates.
- **Distribution tests**: Prebuild source/output and self-bootstrap checks plus post-build enumeration and byte comparison across wheel and sdist.
- **Cross-platform tests**: Existing CI matrix validates byte handling on Ubuntu, macOS, and Windows with Python 3.11 and 3.12.

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Split authoring rules confuse maintainers | Medium | A generated output is edited directly | Same-basename ownership, actionable check diagnostics, and explicit governance updates |
| Byte directive parser mishandles CRLF or non-ASCII content | Medium | Cross-platform drift violates compatibility | Byte-only implementation and dedicated matrix-compatible fixtures |
| CI does not run for fragment-only changes | Medium | Stale output reaches review or release | Add exact `internal/command_templates/**` and renderer paths to workflow filters |
| Package validation covers PyPI but misses plugin artifacts | Medium | Distribution channels diverge | Compare temporary existing-generator outputs with tracked Claude and Codex artifacts before release |
| Automation repairs stale files silently | Low | Unreviewed generated changes enter a release | Keep all automated gates read-only; reserve write mode for explicit maintainer use |

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|------------------|------------------|---------------|
| REQ-001 | Source store, fragment store, directive contract | Decisions 1-2; Phases 1-2 |
| REQ-002 | Fragment store, directive contract | Decision 1; Phases 1-3 |
| REQ-003 | Directive contract, renderer/check mode | Phases 1-2 |
| REQ-004 | Renderer, source mapping, guidance | Decision 3; Phases 1-3 and 5 |
| REQ-005 | Project validation gate | Phases 1-3 and final verification |
| REQ-006 | Distribution gate | Decision 3; Phase 4 and final verification |
| REQ-007 | Existing consumers, maintainer guidance | Phases 2, 4, and 5 |
| NFR-001 | Byte renderer and distribution comparisons | Decisions 1-2; all implementation and verification phases |
| NFR-002 | Existing consumers remain unchanged | Phases 2 and 5 |
| NFR-003 | Project and distribution gates | Phases 3-5 |
