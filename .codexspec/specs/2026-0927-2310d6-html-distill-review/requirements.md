# Confirmed Requirements: HTML Distill Review

**Feature ID**: `2026-0927-2310d6`<br>
**Feature Directory**: `.codexspec/specs/2026-0927-2310d6-html-distill-review/`<br>
**Status**: Confirmed<br>
**Last Confirmed**: 2026-09-27 23:59:18 +0800

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain with `Status: superseded` and link to their replacement.
- AI inferences require user confirmation before becoming binding.

## Context

The current manual `distill` review presents candidate records through terminal text prompts. This is inefficient when users need to inspect evidence, revise structured knowledge, vet or discard records, and review consolidation proposals. Manual review needs a browser workspace without weakening profile quality, conflict-free storage, Git-backed auditability, or non-interactive auto-distill behavior.

## Needs

### NEED-001: Browser-based manual review

- **Status**: confirmed
- **Statement**: A manual `/distill review`, and a manually invoked `/distill` with no new content to distill, MUST open a local HTML review interface by default. The interface MUST present every pending candidate record and consolidation-candidate cluster in scope for the session.
- **Rationale**: Reviewing structured content, evidence, and related records is more efficient in a browser than through sequential terminal prompts.
- **User Evidence**: The user requested HTML in place of the inefficient and unfriendly text interaction and confirmed that ordinary candidates and consolidation review should both move to HTML.
- **Confirmed At**: 2026-09-27 23:59:18 +0800

### NEED-002: Complete candidate decision workflow

- **Status**: confirmed
- **Statement**: For each candidate, the interface MUST let the user vet it, revise it, discard it, or defer it. Revision MUST use structured fields for record content, applicability, evidence, verification state, and category-specific fields, with a preview of the final Markdown. After revision, the user MUST be able either to keep the record as a candidate or to vet it when the vetting gate is satisfied. Record ID, category, provenance, and file identity MUST remain read-only.
- **Rationale**: Users need to correct knowledge without hand-editing profile files or damaging identity and traceability.
- **User Evidence**: The user selected structured editing with protected identity fields and chose to decide candidate versus vetted status after revision.
- **Confirmed At**: 2026-09-27 23:59:18 +0800

### NEED-003: Consolidation review in HTML

- **Status**: confirmed
- **Statement**: The HTML workflow MUST display consolidation-candidate clusters. It MUST let the user inspect member records and the proposed generalized record, revise the generalized content, confirm the merge, or keep source records separate. A confirmed merge MUST create the finalized generalized record and remove superseded members as one batch operation. The generalized record MUST satisfy the same verification-evidence and human-endorsement gate as any other vetted record.
- **Rationale**: Leaving consolidation in terminal prompts would preserve a fragmented review experience.
- **User Evidence**: The user chose to migrate both ordinary and consolidation review to HTML and confirmed that consolidated records follow the existing vetting gate.
- **Confirmed At**: 2026-09-27 23:59:18 +0800

### NEED-004: Staged decisions and explicit batch application

- **Status**: confirmed
- **Statement**: Each decision MUST be staged in the review session instead of immediately changing profile files. The interface MUST provide a final change summary and apply operations only when the user selects "Apply all." The user MAY apply decisions for only part of the pending set; deferred or undecided candidates MUST remain unchanged and be listed in the summary. Canceling or abandoning a session MUST NOT modify profile files.
- **Rationale**: Users need to compare and revise decisions before destructive or cross-record changes become durable.
- **User Evidence**: The user chose staged batch application, allowed deferral, and confirmed that canceling leaves the profile unchanged.
- **Confirmed At**: 2026-09-27 23:59:18 +0800

### NEED-005: Recoverable, single-writer review sessions

- **Status**: confirmed
- **Statement**: Unapplied decisions MUST be persisted as a project-scoped review draft outside the profile store and excluded from Git tracking. After the browser or command closes unexpectedly, a later manual review MUST let the user resume or explicitly discard that draft. A project MUST have at most one writable review session at a time; another invocation MUST reconnect to or report the active session rather than create a competing writer.
- **Rationale**: A long review must survive accidental closure without conflicts between browser sessions.
- **User Evidence**: The user selected persistent cross-process recovery and one active writable session per project.
- **Confirmed At**: 2026-09-27 23:59:18 +0800

## Constraints

### CON-001: Existing vetted quality gate remains binding

- **Status**: confirmed
- **Statement**: A record becomes `vetted` only when it has both outcome-based verification and explicit human endorsement. When the stored record does not establish verification, selecting Vetted MUST require the user to enter the verification result or evidence before promotion. Approval alone MUST NOT bypass this gate.
- **User Evidence**: The user chose to require supplementary verification evidence.

### CON-002: Semantic assistance and file mutation have separate owners

- **Status**: confirmed
- **Statement**: The Agent MAY analyze candidates and prepare revision or consolidation proposals before the page opens. The user determines final content and operations in HTML. A deterministic local backend MUST validate and apply structured operations such as `vet`, `replace`, `remove`, and `merge`; it MUST NOT send the interaction transcript back to an Agent for free-form interpretation before writing files. The live page MUST NOT invoke a remote model.
- **User Evidence**: The user confirmed Agent-generated semantic suggestions with deterministic code-controlled persistence.

### CON-003: Batch application is atomic and conflict-safe

- **Status**: confirmed
- **Statement**: The session MUST retain a base content hash for every affected profile file. Before applying, the backend MUST verify all affected files and staged operations. If any file changed or operation fails validation, the entire batch MUST stop without modifying any profile file, retain the draft, and identify each conflict or validation failure. Partial application and silent overwrite are prohibited.
- **User Evidence**: The user selected whole-batch failure with session retention on concurrent change.

### CON-004: The browser surface is local, private, and offline-capable

- **Status**: confirmed
- **Statement**: The server MUST listen only on `127.0.0.1`, select a non-conflicting local port, and require an unguessable per-session token. HTML, CSS, JavaScript, and other assets MUST ship with CodexSpec and MUST NOT use a CDN, telemetry, or network access. The workflow SHOULD open the default browser and MUST print the local URL when automatic opening fails. It MUST support the project's macOS, Linux, and Windows environments.
- **User Evidence**: The user selected a fully local, offline-capable interface and confirmed cross-platform support.

### CON-005: Profile storage and audit semantics remain unchanged

- **Status**: confirmed
- **Statement**: The profile MUST remain a one-record-per-file store with Git history as its audit ledger. Discarding a candidate MUST delete its record file during batch application, matching `remove`. This feature MUST NOT add a `rejected` status, archive directory, or central profile index or manifest.
- **User Evidence**: The user chose deletion; profile decision `D-2026-0812-14054p-2` requires one record per file and no central index.

### CON-006: Auto-distill remains non-interactive and non-blocking

- **Status**: confirmed
- **Statement**: Auto-distill MUST never open a browser, enter text review, wait for a human, or be gated by an unfinished manual review session. The UI applies only to manual review entry points.
- **User Evidence**: The user preserved existing manual entry points while keeping auto-distill non-interactive.

### CON-007: Human-facing language follows project configuration

- **Status**: confirmed
- **Statement**: The HTML interface, fallback diagnostics, conflict messages, and completion summaries MUST use `language.interaction`. Profile record content MUST retain its established language and semantic content rather than being translated merely for display.
- **User Evidence**: The user confirmed that the interface follows `language.interaction`.

### CON-008: Maintainer validation precedes user installation

- **Status**: confirmed
- **Statement**: Generated assets, local-server code, and synchronization needed by this feature MUST be validated by repository and release gates before distribution. `codexspec init` and an end user's first review MUST NOT be the first point where maintainer-generation or packaging errors surface.
- **User Evidence**: Vetted project constraint `C-2026-0902-054178-1` applies to new user-facing distributed artifacts.

## Decisions

### DEC-001: Use a local temporary web service

- **Status**: confirmed
- **Decision**: Manual HTML review runs through a temporary local web service bound to loopback. Browser actions call its local API, which controls the review draft and deterministic profile mutation.
- **Alternatives Rejected**: A static page using the File System Access API has browser compatibility and permission friction. Exporting an HTML result for later import does not provide direct automatic write-back.
- **Reason**: A local backend provides reliable filesystem access, validation, transaction control, and cross-platform behavior while remaining private.
- **User Evidence**: The user selected the local temporary web-service option.

### DEC-002: Use a hybrid semantic/deterministic architecture

- **Status**: confirmed
- **Decision**: Agent judgment prepares semantic proposals; structured forms establish final content; fixed backend logic alone applies file changes.
- **Alternatives Rejected**: Replaying the interaction for an Agent to reinterpret and mutate files is non-deterministic and difficult to audit or test.
- **Reason**: This split retains semantic assistance while making destructive and persistent operations predictable.
- **User Evidence**: The user explicitly confirmed this boundary.

### DEC-003: HTML is the default with an explicit terminal fallback

- **Status**: confirmed
- **Decision**: Manual review defaults to HTML, while an explicit text mode remains available for headless environments, accessibility needs, or user choice. The fallback MUST enforce the same status transitions, verification gate, staging semantics, and mutation validation.
- **Alternatives Rejected**: HTML-only review prevents use without a browser. Automatic environment-based switching relies on unreliable graphical-environment detection.
- **Reason**: The browser provides the preferred experience without removing a dependable fallback.
- **User Evidence**: The user selected HTML by default with an explicit text fallback.

### DEC-004: Apply staged operations with all-or-nothing semantics

- **Status**: confirmed
- **Decision**: Apply all validated staged decisions as one logical transaction. A conflict or validation failure aborts the whole batch, and users retry after resolving or refreshing affected records.
- **Alternatives Rejected**: Immediate writes and partial application create accidental intermediate states. Forced overwrite can destroy concurrent work.
- **Reason**: Whole-batch application makes the reviewed summary correspond exactly to the resulting profile state.
- **User Evidence**: The user chose staged application and whole-batch failure on conflicts.

## Out of Scope

### OUT-001: Remote or network-accessible review

- **Status**: confirmed
- **Statement**: This feature does not provide public hosting, LAN binding, remote-device access, TLS termination, external authentication, CDN resources, or telemetry.
- **Reason**: The confirmed workflow is private, local, and offline-capable.
- **User Evidence**: The user selected the fully local option instead of CDN or LAN variants.

### OUT-002: Profile model or vetting-policy redesign

- **Status**: confirmed
- **Statement**: This feature does not change the one-record-per-file model, candidate/vetted semantics, outcome-verification requirement, or `evolve` eligibility rules.
- **Reason**: It improves the review carrier and persistence workflow, not the knowledge-quality model.
- **User Evidence**: The user preserved the existing vetted gate and deletion semantics.

### OUT-003: User-managed profile file editing

- **Status**: confirmed
- **Statement**: The workflow does not require users to locate or hand-edit profile Markdown files, session JSON, or backend operation payloads.
- **Reason**: Removing manual file manipulation is part of the usability improvement.
- **User Evidence**: The user requested automatic write-back from the HTML interaction.

## Open Questions

No open questions block specification generation.

## Confirmation Log

### Session 2026-09-27 23:59:18 +0800

- **Summary Presented**: HTML review for candidates and consolidation clusters; structured revision; verification evidence before vetting; staged partial-scope decisions with explicit atomic application; deterministic local persistence; conflict hashes; recoverable single-writer sessions; local offline security; compatible manual entry points; text fallback; unchanged profile storage and auto-distill behavior.
- **User Confirmation**: The user explicitly replied "确认" to the final summary, including its four labeled assumptions.
- **Entries Confirmed**: NEED-001 through NEED-005; CON-001 through CON-008; DEC-001 through DEC-004; OUT-001 through OUT-003.
