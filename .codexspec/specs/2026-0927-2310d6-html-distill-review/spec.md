# Feature Specification: HTML Distill Review

**Feature Branch**: `2026-0927-2310d6-html-distill-review`<br>
**Created**: 2026-09-28<br>
**Status**: Draft<br>
**Input**: Confirmed requirements in `requirements.md`

## Context and Goals

Manual profile review currently relies on sequential terminal text. This feature makes a local HTML workspace the default carrier for reviewing candidate records and consolidation proposals while preserving the existing profile model and quality gate.

The goals are to let users inspect related evidence, revise structured content, make or defer review decisions, preview the complete change set, and apply that set safely without hand-editing profile files. Agent judgment may prepare content proposals, but persistent changes remain deterministic, locally validated, private, offline-capable, and recoverable.

## User Scenarios and Testing

### User Story 1: Review and revise candidate records (Priority: P1)

A user manually starts distill review, sees all pending candidates in a browser, and vets, revises, discards, or defers each record. Revised records are previewed as Markdown before the decision is staged.

**Why this priority**: This replaces the inefficient terminal interaction that motivated the feature.

**Independent Test**: Start manual review with candidates from multiple profile categories, exercise every decision, and verify that no profile file changes before explicit batch application.

**Acceptance Scenarios**:

1. **Given** pending candidate records, **when** the user invokes `/distill review`, **then** the default browser opens a local page that shows every in-scope candidate with its content, evidence, verification state, and provenance.
2. **Given** a candidate, **when** the user revises editable structured fields, **then** the page shows the resulting Markdown while keeping the ID, category, provenance, and file identity read-only.
3. **Given** a revised candidate, **when** the user chooses to retain it as a candidate, **then** the revision is staged without changing its status to vetted.
4. **Given** a candidate with recorded outcome verification, **when** the user selects Vetted, **then** the promotion is staged with the user's endorsement.
5. **Given** a candidate without recorded outcome verification, **when** the user selects Vetted, **then** the interface requires verification results or evidence before it can stage the promotion.
6. **Given** a candidate the user does not want to decide, **when** the user defers it, **then** it remains unchanged and appears as deferred in the summary.

### User Story 2: Review a consolidation proposal (Priority: P1)

A user inspects the members of a consolidation cluster and the proposed generalized record, revises the proposal when needed, then merges the cluster or keeps its members separate.

**Why this priority**: Consolidation is part of the existing manual review surface; leaving it in the terminal would make the new workflow incomplete.

**Independent Test**: Review one marked cluster, revise its generalized record, apply the merge, and verify that the new record and removal of superseded members occur together.

**Acceptance Scenarios**:

1. **Given** records sharing a consolidation cluster key, **when** review opens, **then** the page groups the members and presents the Agent-prepared generalized proposal.
2. **Given** a proposed generalized record, **when** the user revises its structured content, **then** the final Markdown and intended source-record removals are visible before staging the merge.
3. **Given** a generalized record that satisfies the vetted gate, **when** the user confirms and applies the merge, **then** the generalized record is created and all superseded members are removed in the same batch.
4. **Given** a user who declines consolidation, **when** the decision is applied, **then** the source records remain separate and no generalized record is created.

### User Story 3: Preview and safely apply a partial review (Priority: P1)

A user processes any subset of records, reviews a summary, and applies the selected changes as one logical transaction. Concurrent changes never get overwritten.

**Why this priority**: Safe deterministic write-back is required for the HTML interface to replace manual file handling.

**Independent Test**: Stage mixed operations, mutate one source file externally, attempt application, and verify that the entire batch is rejected with no profile changes and the draft remains recoverable.

**Acceptance Scenarios**:

1. **Given** staged vet, replace, remove, and merge operations, **when** the user opens the final summary, **then** it shows every planned change and every deferred record.
2. **Given** unchanged source files and a valid batch, **when** the user selects Apply all, **then** all staged operations are applied and the result exactly matches the summary.
3. **Given** one affected file changed after the review loaded, **when** the user selects Apply all, **then** no profile file is modified, the conflict is identified, and the draft is retained.
4. **Given** a staged operation that fails validation, **when** application is attempted, **then** the whole batch is rejected without partial writes and the failure identifies the record and violated rule.
5. **Given** an open review, **when** the user cancels or abandons it, **then** no staged operation changes the profile.

### User Story 4: Resume a private local review (Priority: P2)

A user can recover an interrupted project review, while a second invocation cannot create a competing writable session.

**Why this priority**: Recovery prevents lost review effort and single-writer ownership prevents conflicting drafts.

**Independent Test**: Stage decisions, terminate the review process, start review again, resume the draft, and separately verify that concurrent invocation does not create another writer.

**Acceptance Scenarios**:

1. **Given** an unapplied persisted draft, **when** manual review starts again, **then** the user may resume it or explicitly discard it.
2. **Given** an active writable review, **when** another manual review starts for the same project, **then** it reconnects to or reports the existing session and does not create another writer.
3. **Given** no graphical browser can be opened, **when** HTML review starts, **then** the command prints the token-protected loopback URL.

### User Story 5: Use equivalent terminal review when needed (Priority: P2)

A user in a headless or accessibility-constrained environment explicitly selects terminal review and receives the same decision, validation, staging, and application semantics.

**Why this priority**: HTML is the preferred experience but must not remove manual review where a browser is unavailable or unsuitable.

**Independent Test**: Run the explicit text mode against the same fixture as HTML mode and compare the resulting structured operations, validation failures, and applied files.

**Acceptance Scenarios**:

1. **Given** explicit text-mode selection, **when** the user reviews candidates and consolidation clusters, **then** all HTML decision types and vetted-gate checks remain available.
2. **Given** identical starting files and equivalent decisions, **when** HTML and text sessions are applied separately, **then** they produce equivalent profile contents and summaries.

### Edge Cases and Expected Errors

- If no candidates or consolidation clusters are pending, manual review reports that there is nothing to review and does not leave an active session or draft.
- If a saved draft refers to a file that was deleted, renamed, or changed, application fails closed, names the stale record, preserves the draft, and writes nothing.
- If the persisted draft is malformed or cannot be read, review reports its location and validation failure and does not mutate the profile; the user may explicitly discard it.
- If the project-level writer lock is held but its service is unreachable, recovery must distinguish a live owner from a stale lock before permitting a new writer.
- If no loopback port can be bound or required assets cannot be loaded, review reports the failed prerequisite and does not modify the profile.
- If the session token is absent or incorrect, the local service rejects the request without revealing review data or performing operations.
- Closing a browser tab does not apply changes. The service and recoverable draft remain governed by explicit resume, discard, or apply actions.
- Candidate records in different document languages are displayed and edited without automatic content translation; only interface text follows `language.interaction`.

## Requirements

### Functional Requirements

- **REQ-001**: Manual `/distill review` and a manually invoked `/distill` with no new segment MUST start HTML review by default; auto-distill MUST never start or wait for manual review.
  - Sources: NEED-001, CON-006
- **REQ-002**: The review view MUST enumerate all in-scope candidate records and consolidation clusters with their content, evidence, verification state, provenance, and relationship information needed for a decision.
  - Sources: NEED-001, NEED-003
- **REQ-003**: Candidate review MUST support vet, revise, discard, and defer, and MUST render the final Markdown preview for structured revisions while preventing changes to ID, category, provenance, and file identity.
  - Sources: NEED-002
- **REQ-004**: Promotion to `vetted` MUST require both explicit human endorsement and recorded outcome-verification evidence; if evidence is missing, the interface MUST collect and validate it before staging promotion.
  - Sources: NEED-002, CON-001, OUT-002
- **REQ-005**: A revised record MUST allow an explicit choice between remaining a candidate and becoming vetted when REQ-004 is satisfied.
  - Sources: NEED-002, CON-001
- **REQ-006**: Consolidation review MUST support inspection and structured revision of a generalized proposal, confirmation of a merge, and retention of separate source records; a merge MUST create the generalized record and remove superseded members in the same batch.
  - Sources: NEED-003, CON-001, DEC-004
- **REQ-007**: Decisions MUST be staged without modifying profile files, and the final summary MUST enumerate staged additions, replacements, promotions, removals, merges, and deferred records.
  - Sources: NEED-004, DEC-004
- **REQ-008**: Apply all MUST validate and commit the entire staged set as one logical transaction; cancel or abandon MUST leave every profile file unchanged.
  - Sources: NEED-004, CON-003, DEC-004
- **REQ-009**: Application MUST compare every affected file with its session base hash and MUST reject the whole batch, retain the draft, and identify all detected conflicts when any precondition fails.
  - Sources: CON-003, DEC-004
- **REQ-010**: Discard MUST use the existing `remove` semantics by deleting the candidate file; review MUST NOT create rejected records, archives, or a central profile index.
  - Sources: CON-005, OUT-002
- **REQ-011**: Unapplied session decisions MUST persist outside `.codexspec/profile/`, remain excluded from Git tracking, and be resumable or explicitly discardable after process termination.
  - Sources: NEED-005
- **REQ-012**: The project MUST permit no more than one writable manual review session; another invocation MUST connect to or report the active session, and stale-owner recovery MUST not create simultaneous writers.
  - Sources: NEED-005
- **REQ-013**: The browser MUST communicate only structured review operations to a deterministic local backend. Live review MUST NOT invoke a remote Agent or submit the interaction transcript for free-form file mutation.
  - Sources: CON-002, DEC-002
- **REQ-014**: An explicit text fallback MUST provide the same candidate and consolidation decisions, vetting gate, draft semantics, validation, atomic application, error behavior, and result summaries as HTML review.
  - Sources: DEC-003
- **REQ-015**: Successful application MUST report the records added, replaced, promoted, removed, merged, and deferred; failed application MUST identify each blocking conflict or validation rule without claiming any change was applied.
  - Sources: NEED-004, CON-003

### Non-Functional Requirements

- **NFR-001**: The review server MUST bind only to `127.0.0.1`, use a non-conflicting port and an unguessable per-session token, and reject unauthorized requests.
  - Sources: CON-004, DEC-001, OUT-001
- **NFR-002**: Review MUST operate without network access. All HTML, CSS, JavaScript, and other runtime assets MUST ship with CodexSpec; no CDN, telemetry, remote hosting, or LAN binding is permitted.
  - Sources: CON-004, OUT-001
- **NFR-003**: The workflow MUST support macOS, Linux, and Windows, SHOULD open the default browser, and MUST print the local URL when automatic opening fails.
  - Sources: CON-004, DEC-003
- **NFR-004**: Interface text, diagnostics, and summaries MUST follow `language.interaction`; record content MUST not be translated as a display side effect.
  - Sources: CON-007
- **NFR-005**: Distribution and release validation MUST prove that required assets, generated artifacts, and package contents are complete before an end user runs `codexspec init` or manual review.
  - Sources: CON-008
- **NFR-006**: The solution MUST preserve the one-record-per-file profile store and Git history as the audit ledger.
  - Sources: CON-005, OUT-002

### Key Entities

- **Review Session**: A single-writer, project-scoped review with an unguessable token, base file hashes, lifecycle state, and reference to its recoverable draft.
- **Review Draft**: Git-ignored persisted state containing structured pending decisions and user revisions, but no applied profile mutation.
- **Candidate View**: A normalized presentation of a profile record, including immutable identity fields, editable category-specific fields, verification state, evidence, and Markdown preview.
- **Consolidation Proposal**: A cluster of source records plus a proposed generalized record, its verification state, and the source removals that confirmation would stage.
- **Structured Operation**: A validated `vet`, `replace`, `remove`, or `merge` request tied to record identity and base hashes.
- **Application Summary**: The complete user-visible projection of staged operations, deferred records, and final success or failure results.

## Success Criteria

- **SC-001**: Every pending candidate and consolidation cluster can be reviewed through HTML without hand-editing a profile file.
- **SC-002**: No profile file changes before Apply all, and canceling, abandoning, validation failure, or any base-hash conflict results in zero profile mutations.
- **SC-003**: An interrupted review with staged decisions can be resumed after restarting the command, and concurrent invocation never creates a second writable session.
- **SC-004**: A complete HTML review runs with external network access disabled and makes no outbound request.
- **SC-005**: Equivalent HTML and explicit text-mode decisions produce equivalent validated operations, resulting profile contents, and completion summaries.
- **SC-006**: Automated distribution checks fail before release if any required runtime asset or generated user-facing artifact is absent or inconsistent.

## Confirmed Constraints and Decisions

- HTML review uses a token-protected loopback web service rather than browser filesystem permissions or result-file import. (DEC-001)
- Agent semantic proposals are separated from deterministic application of user-approved operations. (CON-002, DEC-002)
- HTML is the default and explicit terminal review remains supported with semantic parity. (DEC-003)
- Operations are staged and applied all-or-nothing; forced overwrite and partial application are prohibited. (CON-003, DEC-004)
- Candidate identity, category, provenance, and file identity are immutable in structured revision. (NEED-002)
- The vetted gate, one-record-per-file store, Git audit ledger, and non-interactive auto-distill behavior remain unchanged. (CON-001, CON-005, CON-006)

## Out of Scope

- Public hosting, LAN or remote-device access, TLS termination, external authentication, CDN dependencies, and telemetry. (OUT-001)
- Redesign of profile storage, candidate/vetted status semantics, outcome-verification policy, or `evolve` eligibility. (OUT-002)
- Any workflow requiring users to edit profile Markdown, draft state, or structured operation payloads by hand. (OUT-003)

## Open Questions

None.

## Requirements Traceability

| Confirmed Entry | Spec Coverage | Result |
|---|---|---|
| NEED-001 | REQ-001, REQ-002 | Full |
| NEED-002 | REQ-003, REQ-004, REQ-005 | Full |
| NEED-003 | REQ-002, REQ-006 | Full |
| NEED-004 | REQ-007, REQ-008, REQ-015 | Full |
| NEED-005 | REQ-011, REQ-012 | Full |
| CON-001 | REQ-004, REQ-005, REQ-006 | Full |
| CON-002 | REQ-013 | Full |
| CON-003 | REQ-008, REQ-009, REQ-015 | Full |
| CON-004 | NFR-001, NFR-002, NFR-003 | Full |
| CON-005 | REQ-010, NFR-006 | Full |
| CON-006 | REQ-001 | Full |
| CON-007 | NFR-004 | Full |
| CON-008 | NFR-005, SC-006 | Full |
| DEC-001 | NFR-001; Confirmed Constraints and Decisions | Full |
| DEC-002 | REQ-013; Confirmed Constraints and Decisions | Full |
| DEC-003 | REQ-014, NFR-003 | Full |
| DEC-004 | REQ-006, REQ-008, REQ-009 | Full |
| OUT-001 | NFR-001, NFR-002; Out of Scope | Full |
| OUT-002 | REQ-004, REQ-010, NFR-006; Out of Scope | Full |
| OUT-003 | SC-001; Out of Scope | Full |
