# Implementation Plan: HTML Distill Review

**Related Spec**: `.codexspec/specs/2026-0927-2310d6-html-distill-review/spec.md`<br>
**Related Design**: `.codexspec/specs/2026-0927-2310d6-html-distill-review/design.md`<br>
**Confirmed Requirements**: `.codexspec/specs/2026-0927-2310d6-html-distill-review/requirements.md`<br>
**Created**: 2026-09-28<br>
**Status**: Draft

## Context

This plan implements the approved design for deterministic HTML-based `distill` review. The current repository provides a Typer CLI, Rich terminal output, dynamic interaction-language translation, generated distributed command templates, a one-record-per-file profile, and tested cross-platform file locking and atomic single-file writes. It does not provide a browser review runtime or a deterministic profile-review operation engine.

Implementation proceeds from pure data and validation boundaries outward to storage, adapters, and generated distribution artifacts. This ordering keeps irreversible filesystem work behind a tested operation model and lets HTML/text parity be verified against the same core before command-template integration.

## Goals and Non-Goals

**Goals:**

- Implement the design's lossless profile codec, typed operation model, vetted gate, recoverable draft, single-writer ownership, journaled application, loopback API, packaged frontend, text adapter, and hidden CLI bridge.
- Make manual HTML review the default while leaving auto-distill non-interactive.
- Prove offline behavior, authentication, cross-platform compatibility, transaction recovery, adapter parity, package completeness, and generated-template synchronization.

**Non-Goals:**

- Remote or LAN review, remote authentication, TLS, telemetry, CDN assets, or a frontend build toolchain.
- Changes to profile categories, record identity, candidate/vetted policy, evolve eligibility, or the one-record-per-file model.
- Editing derived `.claude/commands/codexspec/` or `.agents/skills/codexspec-*` files as sources.

## Tech Stack

- **Runtime**: Python 3.11+
- **CLI and terminal UI**: Existing Typer and Rich dependencies
- **HTTP and browser integration**: Python standard-library `http.server`, `webbrowser`, `secrets`, `hashlib`, and `json`
- **Frontend**: Packaged framework-free HTML, CSS, and JavaScript under `src/codexspec`
- **Persistence**: Profile Markdown plus versioned JSON runtime state under `.codexspec/.runtime/distill-review/`
- **Concurrency and atomic I/O**: Existing cross-platform `FileLock` and atomic replacement patterns in `src/codexspec/automation.py`, factored or reused without adding a dependency
- **Tests**: pytest, Typer `CliRunner`, standard-library HTTP clients where sufficient, wheel/sdist archive inspection, and platform CI

## Existing Repository Constraints

- Distributed command edits originate in `internal/command_templates/sources/distill.md`, render into `templates/commands/distill.md`, and then regenerate self-bootstrap artifacts. Derived command copies are never hand-edited.
- User-runtime Python and packaged assets belong under `src/codexspec`; maintainer-only generators remain under `internal/`.
- Maintainer generation and packaging errors must fail repository/release gates before `codexspec init` or first user execution.
- All supported behavior must work on macOS, Linux, and Windows with Python 3.11+.

## Plan-Level Decisions

### Decision 1: Build and test the pure review core before either adapter

**Context**: HTML and text review must share exact semantics, and filesystem mutation must not depend on UI behavior.

**Options Considered**:

1. Implement the browser flow end to end, then extract shared logic.
2. Define fixtures and implement codec/domain/transaction contracts first, then attach both adapters.

**Decision**: Use option 2. Start with representative profile fixtures and pure typed operations; add adapters only after preview, validation, and transaction behavior are stable.

**Rationale**: This makes parity demonstrable and keeps security-sensitive HTTP code separate from knowledge mutation rules.

**Covers**: REQ-003, REQ-004, REQ-005, REQ-013, REQ-014; Design: Profile document codec, Review domain service, Text review adapter, Loopback HTTP server and browser adapter

**Decision Level**: Plan-level build ordering; it does not change the confirmed architecture.

### Decision 2: Treat every transaction boundary as a fault-injection point

**Context**: Journaled multi-file application only satisfies the design when every interrupted state recovers deterministically.

**Options Considered**:

1. Test representative success and one rollback failure.
2. Parameterize failures before and after every journal transition, backup move, target installation, commit marker, and cleanup operation.

**Decision**: Use option 2 for the transaction suite, including restart recovery from each persisted intermediate state.

**Rationale**: The failure matrix is the implementation evidence for all-or-nothing semantics across ordinary exceptions and process interruption.

**Covers**: REQ-006, REQ-008, REQ-009, REQ-010; Design: Recoverable profile transaction engine

**Decision Level**: Plan-level verification strategy.

### Decision 3: Integrate generated artifacts only after runtime contracts pass

**Context**: The distill command source, rendered template, init behavior, self-bootstrap trees, and package archives form a lockstep distribution surface.

**Options Considered**:

1. Change the command prompt first and implement its helper incrementally.
2. Complete and test the hidden helper contract first, then update the source template and regenerate all derived outputs once.

**Decision**: Use option 2 and run the fragment renderer, `codexspec init` regeneration, distribution checks, and archive inspection together in the final integration phase.

**Rationale**: Users never receive a prompt that references a missing or incompatible runtime helper.

**Covers**: REQ-001, REQ-015, NFR-005; Design: Distill command integration, Hidden review CLI bridge, Distribution and verification integration

**Decision Level**: Plan-level sequencing consistent with project constraint `C-2026-0902-054178-1`.

### Decision 4: Use shared behavioral fixtures as the adapter parity oracle

**Context**: Comparing screenshots or prompt text cannot prove semantic parity.

**Options Considered**:

1. Maintain separate browser and terminal expected-output tests.
2. Feed equivalent decisions from both adapters into one fixture corpus and compare normalized drafts, validation errors, application results, and final bytes.

**Decision**: Use option 2 while keeping carrier-specific rendering and accessibility tests separate.

**Rationale**: The common operation/result model is the stable parity boundary defined by the design.

**Covers**: REQ-014, NFR-004; Design: Review domain service, Text review adapter, Loopback HTTP server and browser adapter

**Decision Level**: Plan-level test organization.

## Risks and Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Lossless Markdown editing mishandles unfamiliar records | Medium | High | Build a broad fixture corpus, preserve opaque spans, fail on ambiguity, and assert byte identity for untouched material |
| Transaction recovery differs on Windows rename/locking behavior | Medium | High | Reuse verified lock behavior, stage on the same filesystem, avoid open target handles, and require Windows CI fault/recovery coverage |
| Browser API is reachable by another local origin | Medium | High | Fragment-delivered bearer capability, exact Origin validation, bounded JSON-only mutations, CSP, and negative HTTP tests |
| Runtime ignore handling dirties existing projects | Low | Medium | Make `.codexspec/.gitignore` update idempotent and test clean Git status before and after session creation |
| Generated command and installed forms drift | Medium | High | Render once after runtime completion and run `--check-distribution`, init regeneration, and byte/archive checks |
| Plain JavaScript interface misses keyboard or error states | Medium | Medium | Add DOM-level state tests where practical plus a manual keyboard/focus/accessibility verification checklist |

## Implementation Phases

### Phase 1: Contract fixtures and lossless profile codec

- [ ] Add profile fixtures for all six categories, candidate/vetted/conflict states, consolidation markers, unknown fields, non-ASCII content, ambiguous/invalid records, symlinks, and filename/ID edge cases. — **Covers**: REQ-002, REQ-003, REQ-009, REQ-010; Design: Profile document codec
- [ ] Implement discovery, ID/path confinement, SHA-256 snapshots, recognized-field spans, category-specific schemas, opaque-span preservation, exact-byte rendering, and Markdown preview. — **Covers**: REQ-002, REQ-003, REQ-009, REQ-010, NFR-006; Design: Profile document codec
- [ ] Test that untouched records round-trip byte-for-byte, protected identity fields cannot change, malformed records fail closed, and edited records retain unknown content. — **Covers**: REQ-003, REQ-009, NFR-006; Design: Profile document codec

### Phase 2: Shared review domain and proposal-manifest validation

- [ ] Define versioned models for manifests, snapshots, verification attestations, operations, drafts, summaries, and application results. — **Covers**: REQ-002 through REQ-007, REQ-013, REQ-015; Design: Review domain service, Distill command integration
- [ ] Implement vet, replace, remove, merge, and defer transitions, including the outcome-verification gate and consolidation result validation. — **Covers**: REQ-003 through REQ-007, REQ-010; Design: Review domain service
- [ ] Validate Agent-authored suggestions as untrusted optional proposals tied to the helper's own snapshot; reject stale, mismatched, or identity-changing proposals. — **Covers**: REQ-002, REQ-006, REQ-013; Design: Distill command integration, Review domain service
- [ ] Add summary and diagnostic tests proving exact changed/deferred IDs and no profile writes from any staging operation. — **Covers**: REQ-007, REQ-015; Design: Review domain service

### Phase 3: Recoverable session state and single-writer ownership

- [ ] Add idempotent `.codexspec/.gitignore` management for `.runtime/` to init; for older Git projects, add the runtime path to the repository-local exclude file resolved by Git before creating state, without creating a new untracked worktree file. — **Covers**: REQ-011, NFR-005, NFR-006; Design: Project-scoped session store
- [ ] Implement atomic versioned draft storage, resume/discard rules, draft revisions, cleanup, and corrupt-draft diagnostics under `.codexspec/.runtime/distill-review/`. — **Covers**: REQ-007, REQ-011; Design: Project-scoped session store
- [ ] Implement lifetime-held non-blocking project locking, atomic active-service metadata, reconnect detection, and stale-process recovery using the existing cross-platform lock primitive. — **Covers**: REQ-012; Design: Single-writer lease
- [ ] Verify crash/restart recovery, stale metadata, two-process contention, clean Git status, and supported-platform permission behavior. — **Covers**: REQ-011, REQ-012, NFR-006; Design: Project-scoped session store, Single-writer lease

### Phase 4: Recoverable all-or-nothing profile transaction

- [ ] Implement full-batch preflight for schema validity, target confinement, symlink rejection, base hashes, absence preconditions, and duplicate targets before any mutation. — **Covers**: REQ-008, REQ-009, REQ-010; Design: Recoverable profile transaction engine
- [ ] Implement same-filesystem staging, backup moves, atomic journal transitions, ordered installation, committed marker, reverse rollback, and repeatable cleanup. — **Covers**: REQ-006, REQ-008, REQ-009, REQ-010, NFR-006; Design: Recoverable profile transaction engine
- [ ] Implement mandatory startup recovery for every nonterminal journal state before review can create or resume a session. — **Covers**: REQ-008, REQ-009; Design: Recoverable profile transaction engine, Hidden review CLI bridge
- [ ] Run the parameterized fault-injection matrix across add/replace/remove/merge batches and assert old-or-new final states, retained drafts on failure, and exact result summaries. — **Covers**: REQ-006, REQ-008, REQ-009, REQ-010, REQ-015; Design: Recoverable profile transaction engine

### Phase 5: Authenticated loopback API

- [ ] Implement OS-assigned IPv4 loopback binding, fragment capability generation, browser launch/fallback URL, active metadata, graceful shutdown, and size/time bounds. — **Covers**: REQ-001, REQ-011, REQ-012, NFR-001, NFR-003; Design: Loopback HTTP server and browser adapter
- [ ] Implement static-shell and authenticated JSON routes for snapshot, draft, preview, apply, cancel, resume, and discard over the shared domain service. — **Covers**: REQ-002 through REQ-009, REQ-011, REQ-013, REQ-015; Design: Loopback HTTP server and browser adapter, Review domain service
- [ ] Enforce bearer authorization, exact loopback Origin, method/content restrictions, schema versions, body limits, path isolation, CSP, and security headers. — **Covers**: REQ-013, NFR-001, NFR-002; Design: Loopback HTTP server and browser adapter
- [ ] Add positive and negative HTTP tests for missing/wrong tokens, foreign origins, malformed bodies, stale draft revisions, duplicate apply, unauthorized data reads, and zero outbound dependencies. — **Covers**: REQ-008, REQ-009, NFR-001, NFR-002; Design: Loopback HTTP server and browser adapter

### Phase 6: Packaged HTML interface

- [ ] Build framework-free candidate and consolidation views, category-specific editors, verification-evidence flow, defer/discard choices, exact Markdown source preview, conflict display, and final application summary. — **Covers**: REQ-002 through REQ-007, REQ-015; Design: Packaged review frontend
- [ ] Implement fragment-token capture and immediate history cleanup, in-memory authorization, draft-revision synchronization, reconnect guidance, apply/cancel/discard flows, and explicit error states. — **Covers**: REQ-007 through REQ-009, REQ-011, NFR-001; Design: Packaged review frontend, Loopback HTTP server and browser adapter
- [ ] Add packaged interaction-language catalogs and verify interface translation/fallback without translating record content. — **Covers**: NFR-004; Design: Packaged review frontend
- [ ] Verify keyboard operation, focus movement, readable validation errors, no external resources, and correct packaged-asset loading on supported browsers available in test/manual environments. — **Covers**: NFR-002, NFR-003, NFR-004; Design: Packaged review frontend

### Phase 7: Text adapter and hidden CLI bridge

- [ ] Implement explicit text-mode rendering/input over the same domain service, draft store, transaction engine, and result schema. — **Covers**: REQ-003 through REQ-015; Design: Text review adapter
- [ ] Add the hidden Typer bridge with project/language resolution, manifest-version validation, transaction recovery, session lifecycle, mode dispatch, localized diagnostics, and machine-readable result output. — **Covers**: REQ-001, REQ-011, REQ-012, REQ-014, REQ-015, NFR-003, NFR-004; Design: Hidden review CLI bridge
- [ ] Run shared parity fixtures through HTTP and text adapters and assert equal drafts, validation outcomes, final bytes, and summaries. — **Covers**: REQ-014, NFR-004; Design: Review domain service, Text review adapter, Loopback HTTP server and browser adapter
- [ ] Test nothing-to-review, browser-open failure, invalid manifest, active-session reconnect, corrupt draft, and failed recovery diagnostics through `CliRunner`. — **Covers**: REQ-001, REQ-011, REQ-012, REQ-015, NFR-003; Design: Hidden review CLI bridge

### Phase 8: Distill, init, packaging, and documentation integration

- [ ] Update the authoritative distill command source so manual review prepares validated proposals and invokes the helper, while all auto-distill paths remain non-interactive and non-blocking. — **Covers**: REQ-001, REQ-002, REQ-006, REQ-013; Design: Distill command integration
- [ ] Render `templates/commands/distill.md`, regenerate `.claude/commands/` and `.agents/skills/` through `codexspec init`, and update contract tests without hand-editing derived artifacts. — **Covers**: REQ-001, NFR-005; Design: Distill command integration, Distribution and verification integration
- [ ] Update maintainer/user documentation describing HTML default, explicit text fallback, offline/local security, resume/discard behavior, and unchanged auto-distill semantics. — **Covers**: REQ-001, REQ-011, REQ-014, NFR-001, NFR-002; Design: Distribution and verification integration
- [ ] Inspect wheel and sdist contents for all runtime assets and absence of maintainer-only material, then execute fragment distribution checks and install into an isolated project for end-to-end review. — **Covers**: NFR-005; Design: Distribution and verification integration

### Phase 9: Final verification

- [ ] Run focused codec, domain, session, transaction, HTTP, frontend-contract, adapter-parity, CLI, init, template, and archive tests on the development platform. — **Covers**: REQ-001 through REQ-015, NFR-001 through NFR-006; Design: All design components
- [ ] Run formatting, lint, the complete pytest suite, command-fragment distribution validation, and Git whitespace checks. — **Covers**: NFR-005; Design: Distribution and verification integration
- [ ] Verify the full platform CI matrix, with particular attention to Windows file handles, rename behavior, browser-open fallback, and lock recovery. — **Covers**: REQ-008, REQ-009, REQ-012, NFR-003, NFR-005; Design: Recoverable profile transaction engine, Single-writer lease, Distribution and verification integration

## Verification Strategy

- **Unit**: Record parsing/rendering, protected fields, category schemas, operation transitions, vetting evidence, summaries, draft revisions, token checks, and path confinement.
- **Property/fixture matrix**: All categories and operation combinations preserve untouched bytes and yield deterministic previews/results.
- **Fault injection**: Every transaction journal and filesystem boundary, followed by same-process rollback and fresh-process recovery.
- **Concurrency**: Competing process locks, stale metadata, stale browser revisions, and concurrent disk changes after snapshot.
- **HTTP security**: Token, Origin, method, content type, body bounds, CSP, unauthorized read/mutation, and no outbound requests.
- **Adapter parity**: Equivalent HTML API and text decisions yield the same normalized draft, errors, result, and file bytes.
- **Packaging**: Wheel/sdist asset inspection plus isolated installed-runtime execution with network disabled.
- **Regression**: Existing distill extraction, onboard, evolve, init, profile, blueprint, i18n, and command-template suites.
- **Platform**: macOS, Linux, and Windows CI; host-specific locking, permissions, and replace behavior receive explicit coverage.

## Assumptions

- Repository CI remains capable of exercising Windows, macOS, and Linux even if local development verifies only the current host.
- Browser DOM automation is not an existing project dependency; deterministic API/asset tests plus a documented manual browser checklist are sufficient unless implementation exposes a defect that requires a browser-test dependency decision.

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|---|---|---|
| REQ-001 | Distill integration; CLI bridge; loopback server | Phases 5, 7, 8 |
| REQ-002 | Distill integration; codec; frontend | Phases 1, 2, 5, 6, 8 |
| REQ-003 | Codec; domain; frontend | Phases 1, 2, 5, 6, 7 |
| REQ-004 | Domain; frontend | Phases 2, 5, 6, 7 |
| REQ-005 | Domain; frontend | Phases 2, 5, 6, 7 |
| REQ-006 | Domain; transaction engine | Phases 2, 4, 5, 6, 8 |
| REQ-007 | Domain; session store; frontend | Phases 2, 3, 5, 6, 7 |
| REQ-008 | Transaction engine; HTTP contract | Phases 4, 5, 6, 7, 9 |
| REQ-009 | Codec; transaction engine | Phases 1, 4, 5, 6, 9 |
| REQ-010 | Codec; transaction engine | Phases 1, 2, 4, 7 |
| REQ-011 | Session store; CLI bridge | Phases 3, 5, 6, 7, 8 |
| REQ-012 | Single-writer lease; CLI bridge | Phases 3, 5, 7, 9 |
| REQ-013 | Distill integration; domain service | Phases 2, 5, 7, 8 |
| REQ-014 | Text adapter; shared domain service | Phases 7, 8 |
| REQ-015 | Domain; transaction engine; CLI bridge | Phases 2, 4, 5, 6, 7 |
| NFR-001 | Loopback server; frontend | Phases 5, 6, 8 |
| NFR-002 | Loopback server; frontend | Phases 5, 6, 8 |
| NFR-003 | CLI bridge; loopback server | Phases 5, 6, 7, 9 |
| NFR-004 | CLI bridge; frontend; text adapter | Phases 6, 7 |
| NFR-005 | Distribution integration | Phases 3, 8, 9 |
| NFR-006 | Codec; session store; transaction engine | Phases 1, 3, 4 |

## Design Component Coverage

| Design Component | Plan Coverage |
|---|---|
| Distill command integration | Phases 2 and 8 |
| Hidden review CLI bridge | Phases 4 and 7 |
| Profile document codec | Phase 1 |
| Review domain service | Phase 2 and shared fixtures in Phase 7 |
| Project-scoped session store | Phase 3 |
| Single-writer lease | Phase 3 |
| Loopback HTTP server and browser adapter | Phase 5 |
| Packaged review frontend | Phase 6 |
| Text review adapter | Phase 7 |
| Recoverable profile transaction engine | Phase 4 |
| Distribution and verification integration | Phases 8 and 9 |
