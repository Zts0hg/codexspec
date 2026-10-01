# Design Document: HTML Distill Review

**Related Spec**: `.codexspec/specs/2026-0927-2310d6-html-distill-review/spec.md`<br>
**Confirmed Requirements**: `.codexspec/specs/2026-0927-2310d6-html-distill-review/requirements.md`<br>
**Created**: 2026-09-28<br>
**Status**: Draft

## Context

`distill` is currently an Agent-operated command template. It reads the one-record-per-file profile and performs manual review through conversational terminal prompts. The new review surface needs executable local infrastructure because a browser cannot safely and portably mutate project files on its own.

The design keeps semantic proposal generation in the `distill` command, introduces one hidden CLI bridge into deterministic Python code, and gives HTML and terminal adapters the same domain model, validation, draft store, and transaction engine. Runtime state stays under `.codexspec/.runtime/distill-review/`, outside `.codexspec/profile/` and ignored by Git. No new third-party dependency is required: the server, browser launcher, hashing, JSON handling, and cryptographic token generation use the Python standard library; the existing cross-platform file-lock implementation is reused.

## Architecture and Components

### Distill command integration

- **Responsibility**: Distinguish extraction from manual review, scan the current profile, prepare optional Agent-authored revision and consolidation proposals, and invoke the hidden review helper only for manual review entry points. Auto-distill retains its early-exit, non-interactive path and never calls the helper.
- **Interface**: The source template `internal/command_templates/sources/distill.md` produces the distributed `templates/commands/distill.md`. For review, it supplies a versioned proposal manifest containing record IDs, optional suggested field values, and consolidation proposals; the helper treats all supplied content as untrusted input and validates it against its own disk snapshot.
- **Covers**: REQ-001, REQ-002, REQ-006, REQ-013

### Hidden review CLI bridge

- **Responsibility**: Expose executable review lifecycle operations to the slash command without adding a documented user command. Resolve the project root and interaction language, acquire the single-writer lock, recover interrupted transactions, create or resume the draft, and select HTML or explicit text mode.
- **Interface**: A hidden Typer command in `src/codexspec/__init__.py` delegates to `src/codexspec/distill_review/`. It accepts a versioned proposal manifest and a mode (`html` by default or explicit `text`), returns localized diagnostics, and emits a machine-readable final summary for the Agent to report. Invalid arguments and malformed manifests fail before a server starts or a profile file changes.
- **Covers**: REQ-001, REQ-011, REQ-012, REQ-014, REQ-015, NFR-003, NFR-004

### Profile document codec

- **Responsibility**: Discover candidate files and consolidation clusters, parse record headings and known structured fields, preserve unrecognized Markdown losslessly, validate category-specific required fields, apply field-level edits, and render the exact preview bytes that would be persisted.
- **Interface**: Reads only files directly under the six known category directories. A parsed document contains immutable identity/category/provenance/file-path data, editable recognized fields, ordered opaque source spans, source bytes, and SHA-256. Rendering modifies only fields represented by a validated operation and preserves all other material. It rejects ambiguous IDs, duplicate fields, path escapes, symlink targets, and schema-invalid results.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-009, REQ-010, NFR-006

### Review domain service

- **Responsibility**: Own the state machine shared by browser and terminal modes: candidate decisions, structured revisions, vetted-gate validation, consolidation decisions, deferral, preview generation, change-summary generation, and application eligibility.
- **Interface**: Accepts typed operations (`vet`, `replace`, `remove`, `merge`, `defer`) against a session snapshot. A request identifies a record or cluster and carries only allowed editable fields. It returns a normalized draft projection and validation diagnostics. It never writes profile files directly; application is delegated to the transaction engine.
- **Covers**: REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-013, REQ-014, REQ-015

### Project-scoped session store

- **Responsibility**: Persist the review snapshot and unapplied structured decisions across process restarts, maintain active-service metadata, and ensure runtime files never enter the profile or Git history.
- **Interface**: Stores versioned JSON and transaction material under `.codexspec/.runtime/distill-review/`. `codexspec init` installs an idempotent `.codexspec/.gitignore` rule for `.runtime/`. For an older Git project without that tracked rule, the helper adds the runtime path to the repository-local exclude file resolved by `git rev-parse --git-path info/exclude`, which keeps compatibility state outside the worktree; a non-Git project needs no Git exclusion. Draft writes use atomic replacement. Session tokens and active-service metadata use owner-only permissions where the host supports them. Applying or explicitly discarding a completed draft removes its runtime state; canceling the current UI without discarding retains the recoverable draft only when it contains staged work.
- **Covers**: REQ-007, REQ-011, REQ-012, NFR-006

### Single-writer lease

- **Responsibility**: Guarantee one writable session per canonical project root and distinguish a live service from recoverable state after a process exits.
- **Interface**: Holds the existing cross-platform `FileLock` for the server or text session lifetime and writes atomic active-service metadata containing protocol version, PID, port, start time, and a reconnect capability. A second invocation reads metadata only after non-blocking lock acquisition fails: it may reconnect to a responsive matching service but cannot create another writer. OS lock release after process death permits recovery; stale metadata alone never proves ownership.
- **Covers**: REQ-012

### Loopback HTTP server and browser adapter

- **Responsibility**: Serve packaged static assets and a narrow authenticated JSON API, open the system browser, and translate browser actions into review-domain calls.
- **Interface**: A standard-library threaded HTTP server binds an OS-assigned port on IPv4 `127.0.0.1`. The opened URL places a `secrets.token_urlsafe` capability in the URL fragment; the fragment is not sent in the initial HTTP request. JavaScript reads it into memory, removes it from visible history, and sends it in an `Authorization: Bearer` header. API requests also require the exact loopback `Origin`, JSON content type for mutations, bounded request bodies, and allowed methods. Static responses set a restrictive Content Security Policy and do not expose profile data. API routes cover snapshot retrieval, draft replacement, preview, apply, cancel, resume, and discard. If browser launch fails, the same fragment URL is printed.
- **Covers**: REQ-001, REQ-002, REQ-007, REQ-008, REQ-013, NFR-001, NFR-002, NFR-003, NFR-004

### Packaged review frontend

- **Responsibility**: Present candidate cards, consolidation clusters, structured category-specific editors, Markdown source previews, verification-evidence prompts, decision state, conflicts, and the final application summary.
- **Interface**: Plain versioned HTML, CSS, and JavaScript under the `src/codexspec` package; no build step, CDN, remote font, telemetry, or dynamic code download. All strings come from a packaged interaction-language catalog with the same fallback rules as the CLI. The frontend never receives arbitrary filesystem paths outside normalized record display data and cannot issue a profile mutation except through the authenticated apply endpoint.
- **Covers**: REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-015, NFR-002, NFR-004, NFR-005

### Text review adapter

- **Responsibility**: Provide the explicit headless/accessibility fallback without duplicating business rules.
- **Interface**: Renders the same normalized snapshot and invokes the same review-domain operations and transaction engine. It stages decisions, prints the same summary model, and requires explicit Apply all confirmation. Mode-specific input/output code cannot change validation or persistence behavior.
- **Covers**: REQ-014, NFR-004

### Recoverable profile transaction engine

- **Responsibility**: Validate the complete change set against base hashes and apply additions, replacements, and removals with all-or-nothing logical semantics across supported platforms.
- **Interface**: Under the project writer lock, it performs a complete preflight before mutation: validate every rendered record, resolve and confine every target path, verify all base hashes and absence preconditions, and prepare new bytes plus same-filesystem backups in a transaction directory. It then writes an atomic recovery journal and applies each step with `os.replace`; removals move originals into the backup area instead of unlinking them. On an ordinary failure it restores every prior file in reverse order. On process restart, journal recovery completes rollback before any new session is served. A committed marker is written only after every target is installed; cleanup occurs afterward and is safely repeatable.
- **Covers**: REQ-006, REQ-008, REQ-009, REQ-010, REQ-015, NFR-006

### Distribution and verification integration

- **Responsibility**: Ship the Python module and static assets, keep generated command forms synchronized, and prove packaging and runtime behavior before release.
- **Interface**: Source-package assets live under `src/codexspec` so wheel and sdist packaging include them with the module. Maintainer edits target the internal distill source and renderer output, never `.claude/commands/` or `.agents/skills/` directly. Contract, unit, HTTP, transaction fault-injection, cross-platform, init, distribution-fragment, and archive-content tests cover both source and installed forms.
- **Covers**: NFR-005

## Key Design Decisions

### Decision 1: One domain service for HTML and text review

- **Context**: The two interaction carriers must produce identical decisions and files.
- **Decision**: Both adapters call the same typed operation, validation, draft, preview, summary, and transaction APIs. Interaction layers contain no status-transition or file-mutation policy.
- **Alternatives**: Keeping the existing Agent-interpreted text path beside a deterministic HTML path would create two different semantics and make parity untestable.
- **Trade-offs**: The existing terminal behavior must be re-expressed through the domain service, but every rule then has one implementation.
- **Covers**: REQ-013, REQ-014

### Decision 2: Capability in the URL fragment, authorization in API headers

- **Context**: A reconnectable loopback page needs an unguessable capability without leaking it in HTTP request logs, Referer headers, or ordinary browser history.
- **Decision**: Put the token in the initial URL fragment, remove it from the address after JavaScript loads, retain it only in page memory, and require it as a bearer token on every data or mutation API request.
- **Alternatives**: A query-string token is sent to the server and retained more broadly; cookie authentication adds CSRF and persistence concerns; unauthenticated loopback relies incorrectly on localhost trust.
- **Trade-offs**: A full page reload after fragment removal needs a reconnect URL from the active invocation, but token exposure is materially reduced.
- **Covers**: NFR-001, NFR-002

### Decision 3: Persist drafts in a Git-ignored project runtime area

- **Context**: Drafts must survive process termination, remain project-scoped, stay outside the profile, and never become repository knowledge.
- **Decision**: Use `.codexspec/.runtime/distill-review/`. New and re-initialized projects receive an idempotent `.codexspec/.gitignore` rule for `.runtime/`; older Git projects use the repository-local exclude file for compatibility so first review does not dirty the worktree.
- **Alternatives**: Browser storage drifts from project files and is browser-specific; OS-global caches weaken project locality and cleanup; profile storage violates the profile model.
- **Trade-offs**: The installer gains one managed ignore artifact, while the helper must resolve Git's repository-local exclude path for projects initialized before this feature.
- **Covers**: REQ-011, NFR-005, NFR-006

### Decision 4: Journaled rollback for portable multi-file application

- **Context**: Filesystems do not provide one portable atomic primitive for replacing and deleting several independent files, especially across Windows and POSIX.
- **Decision**: Treat Apply all as a recoverable transaction: preflight everything, stage on the same filesystem, journal intended steps, move originals to backups, atomically install each target, and roll back any incomplete journal before serving more work.
- **Alternatives**: Best-effort sequential writes permit partial state; replacing the entire profile directory is not a portable atomic replacement of a non-empty directory and would widen conflict scope; relying on Git rollback requires a repository and changes Git state.
- **Trade-offs**: External readers not honoring the project lock could briefly observe an applying transaction, but any completed call or recovered restart exposes either the full old state or full new state. The design remains portable and does not require Git.
- **Covers**: REQ-008, REQ-009, REQ-010, NFR-006

### Decision 5: Lossless field-aware Markdown editing

- **Context**: Profile categories have structured fields but may contain forward-compatible or hand-authored Markdown that the current version does not recognize.
- **Decision**: Parse recognized field spans for structured editing while preserving all unmodified and unknown spans byte-for-byte. Preview and validation operate on the exact rendered bytes that application will install.
- **Alternatives**: Re-rendering an entire normalized document risks silently dropping unknown content; raw Markdown editing permits identity and schema corruption.
- **Trade-offs**: The codec is more careful than a simple key/value parser and must reject ambiguous documents rather than guessing.
- **Covers**: REQ-003, REQ-009, NFR-006

### Decision 6: No frontend build system or new runtime dependency

- **Context**: The interface must be offline, portable, and validated before packaging; the project currently has no JavaScript toolchain.
- **Decision**: Ship a small framework-free frontend and use standard-library HTTP/browser facilities with existing Python locking and i18n patterns.
- **Alternatives**: A framework build introduces Node-based generation and additional release failure modes; CDN assets violate offline and supply-chain constraints.
- **Trade-offs**: UI components and accessibility behavior are implemented directly, but packaging is transparent and deterministic.
- **Covers**: NFR-002, NFR-003, NFR-005

## Data Models and Key Entities

| Entity | Key fields and constraints | Covers |
|---|---|---|
| Review manifest | `schema_version`, canonical project identity, optional candidate suggestions, consolidation proposals; untrusted and validated against disk | REQ-002, REQ-006, REQ-013 |
| Record snapshot | record ID, category, relative path, SHA-256, immutable fields, editable fields, opaque spans, rendered source; IDs and paths unique | REQ-002, REQ-003, REQ-009 |
| Review draft | schema version, snapshot identity, staged operations, deferred IDs, updated timestamp; atomically persisted and Git-ignored | REQ-007, REQ-011 |
| Structured operation | tagged union of `vet`, `replace`, `remove`, `merge`, `defer`; target identity plus allowed payload and base hash | REQ-003 through REQ-010 |
| Verification attestation | outcome/evidence text, human endorsement marker, affected record; non-empty outcome required for new vetting | REQ-004, REQ-006 |
| Active service record | protocol version, PID, port, start time, reconnect capability; informative only while OS lock is held | REQ-012, NFR-001 |
| Transaction journal | transaction ID, state, ordered operations, source hashes, staged paths, backup paths, completion markers; writes are atomic | REQ-008, REQ-009 |
| Application result | transaction status and exact added/replaced/promoted/removed/merged/deferred IDs or complete conflict/error set | REQ-015 |

## API and Interface Contracts

### Hidden CLI contract

- The helper accepts only an explicit project root, interaction mode, and optional versioned proposal manifest.
- It resolves all paths beneath the canonical project root and rejects unsupported manifest versions before acquiring a session.
- Its final machine-readable result distinguishes `applied`, `cancelled`, `nothing_to_review`, `active_session`, `conflict`, and `invalid_input`; human diagnostics use `language.interaction`.
- Auto-distill never invokes this contract.
- **Covers**: REQ-001, REQ-011, REQ-012, REQ-014, REQ-015, NFR-004

### Local HTTP contract

- Static shell requests disclose no review data and carry restrictive security headers.
- Data and mutation endpoints require the bearer capability; mutation endpoints additionally require exact loopback Origin, JSON content type, allowed method, schema version, and bounded body length.
- Draft updates are idempotent replacements with a draft revision precondition so stale tabs cannot overwrite newer staged decisions.
- Apply accepts the current draft revision only and returns either the complete application result or a complete set of conflicts/validation failures; it never reports partial success.
- Cancel stops the interactive service without applying. Explicit discard removes the recoverable draft only after confirmation.
- **Covers**: REQ-007, REQ-008, REQ-009, REQ-011, REQ-015, NFR-001

### Profile transaction contract

- Input is a fully rendered and validated target set plus base hashes, never raw UI text.
- All target paths must be regular files directly within an allowed profile category; symlinks and path traversal fail closed.
- The engine returns success only after the committed journal state is durable. Any other outcome leaves or restores the old profile and retains enough journal state for deterministic startup recovery.
- **Covers**: REQ-008, REQ-009, REQ-010, NFR-006

## Sequence and Data Flow

### Start or resume manual HTML review

1. The Agent identifies manual review, scans candidate semantics, and prepares optional suggestions.
2. The hidden helper canonicalizes the project, recovers any incomplete transaction, and attempts the non-blocking project writer lock.
3. If another live service owns the lock, the helper reports or opens its reconnect URL. Otherwise it validates a recoverable draft or creates a snapshot from current profile files.
4. The helper binds `127.0.0.1` on an OS-assigned port, writes active metadata, creates a fresh capability, and opens the fragment URL.
5. The browser authenticates API calls, renders the snapshot/draft, and atomically persists every staged draft revision without touching the profile.

- **Covers**: REQ-001, REQ-002, REQ-007, REQ-011, REQ-012, NFR-001, NFR-003

### Apply all

1. The browser displays the normalized application summary and submits the current draft revision.
2. The domain service validates decisions, category schemas, vetting evidence, and exact preview bytes.
3. The transaction engine checks every base hash and target-absence precondition before any mutation.
4. If preflight fails, it returns all detected blockers and keeps the draft. Otherwise it stages bytes and backups, writes the recovery journal, and applies the ordered operations.
5. On success it marks the journal committed, returns the exact result, and removes completed draft/runtime material. On error it rolls back; on process death the next invocation rolls back before review resumes.

- **Covers**: REQ-004, REQ-006, REQ-008, REQ-009, REQ-010, REQ-015

## Cross-Cutting Design

- **Security**: Loopback-only binding is combined with an unguessable capability, Origin checks, method/content restrictions, size limits, path confinement, symlink rejection, CSP, no external resources, and no remote Agent calls during live review. Covers NFR-001 and NFR-002.
- **Integrity**: Snapshot hashes, draft revisions, schema validation, exact-byte previews, single-writer locking, atomic draft/journal writes, and recoverable rollback protect profile contents. Covers REQ-008, REQ-009, REQ-012, and NFR-006.
- **Internationalization**: Server and frontend consume the existing normalized interaction language with embedded catalogs and English fallback; record bytes are not translated. Covers NFR-004.
- **Packaging**: Static assets reside inside the Python package, and distribution tests inspect both wheel and sdist contents. Generated distill templates are checked through the existing maintainer-only fragment gate. Covers NFR-005.

## Risks and Trade-offs

| Risk | Impact | Mitigation |
|---|---|---|
| Process termination during multi-file apply | Profile may be transiently mixed on disk | Same-filesystem backups, durable journal, project lock, and mandatory recovery before any new session |
| Loose Markdown admits unknown fields | Naive rendering could lose knowledge | Lossless span preservation and fail-closed ambiguity checks |
| Token exposure through copied reconnect URLs | Another local process or user could access review data | Fragment delivery, in-memory bearer use, owner-only active metadata, token rotation on resume, loopback binding, no external resources |
| Stale browser tab overwrites newer draft state | User decisions could be lost | Monotonic draft revision precondition on every update and apply |
| Existing projects lack the runtime ignore rule | Drafts could appear in Git status | Init-managed `.codexspec/.gitignore`; repository-local Git exclude compatibility for older projects before draft creation |
| HTML and text interactions drift | Equivalent decisions produce different files | Shared domain service and cross-adapter contract fixtures |

## Assumptions

- Existing profile records continue to use the Markdown field conventions defined by the distributed `distill` command; ambiguous deviations are rejected rather than normalized silently.
- The existing internal `FileLock` behavior remains available on supported Python and operating-system versions. This is a repository implementation fact, not a new user-visible requirement.

## Requirements Coverage

| Spec Requirement | Design Coverage |
|---|---|
| REQ-001 | Distill command integration; hidden CLI bridge; loopback server |
| REQ-002 | Distill integration; document codec; frontend |
| REQ-003 | Document codec; domain service; frontend; Decision 5 |
| REQ-004 | Domain service; frontend; verification model |
| REQ-005 | Domain service; frontend |
| REQ-006 | Distill integration; domain service; transaction engine |
| REQ-007 | Domain service; session store; frontend; HTTP contract |
| REQ-008 | Transaction engine; Decision 4; transaction contract |
| REQ-009 | Document codec; transaction engine; Decision 4 |
| REQ-010 | Document codec; transaction engine; transaction contract |
| REQ-011 | CLI bridge; session store; Decision 3 |
| REQ-012 | CLI bridge; single-writer lease; start/resume flow |
| REQ-013 | Distill integration; domain service; Decision 1 |
| REQ-014 | CLI bridge; text adapter; Decision 1 |
| REQ-015 | CLI bridge; domain service; transaction engine; result model |
| NFR-001 | Loopback server; Decision 2; HTTP contract; security design |
| NFR-002 | Loopback server; frontend; Decision 6; security design |
| NFR-003 | CLI bridge; loopback server; Decision 6 |
| NFR-004 | CLI bridge; frontend; text adapter; i18n design |
| NFR-005 | Distribution integration; Decision 3; Decision 6; packaging design |
| NFR-006 | Document codec; session store; transaction engine; Decision 4; integrity design |
