# Feature Specification: Distill Review Interface Design

<!--
Language: Generated in the language specified in .codexspec/config.yml (language.document).
Compiled from requirements.md. Confirmed entries in requirements.md are the authority.
-->

**Feature ID**: `2026-1001-2205zz`<br>
**Feature Directory**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/`<br>
**Branch**: `2026-0927-2310d6-html-distill-review` — this feature deliberately shares the branch of the carrier feature it refines (DEC-005)<br>
**Created**: 2026-10-01<br>
**Status**: Draft<br>
**Requirements Source**: `requirements.md`, confirmed 2026-10-01 22:26:56 +0800

## Context and Goals

Feature `2026-0927-2310d6-html-distill-review` delivered the offline browser workspace for manual distill review: a loopback server with a per-session token, a staged-decision draft, a rule that refuses to stage a revision until a byte-identical preview of it exists, all-or-nothing batch application, and base-hash conflict detection. Its confirmed requirements govern the workflow and its safety properties and say nothing about how the workspace presents itself.

The delivered page carries no design system: no colour tokens, no type or spacing scale, native control styling, and a dark appearance left to browser defaults. The consequences are not cosmetic. A reviewer cannot see which records already carry a decision, cannot see how much of the queue remains, and cannot see that a decision will be refused until a matching preview exists — so a decision control appears to do nothing and the explanation arrives in a status line far from the control that was used. The record of what batch application will write is rendered as serialized JSON. Routine and destructive controls share one visual weight, and the control that destroys every staged decision acts with no confirmation. A field is rendered as a single-line or a multi-line control depending on how long its stored value happens to be, and the multi-line form invites a line break that the record codec rejects.

**Goal**: make the browser workspace legible and safe to operate — the state of every record visible, the bytes that will be written presented as the object of the decision, the gates visible before they refuse, destructive actions separated and confirmed, and one coherent visual system in both colour schemes — while every review safety property stays exactly as delivered.

**Non-goal**: changing what the review workflow does. No decision action is added, and no staging, application, conflict, or vetting rule changes.

## User Scenarios and Testing

### User Story 1: Work through a queue and know where you are (Priority: P1)

A reviewer opens the workspace with several candidate records and one consolidation cluster pending. The queue shows them grouped by what has been decided, with a count per group, each entry naming its record and category. The entry being edited is marked as current. After each decision the queue updates and the workspace moves to the next record with no decision yet, and the reviewer can see at a glance how many of the pending records are already settled.

**Why this priority**: Orientation is the precondition for every other improvement; without it the reviewer cannot tell whether work remains or whether a decision registered.

**Independent Test**: Open a session with a mixed set of records, stage one decision of each kind, and confirm the queue grouping, counts, current-selection marking, progress figure, and the advance to the next undecided record.

**Acceptance Scenarios**:

1. **Given** a session with four pending records and one cluster, **When** the page opens, **Then** the queue lists them grouped as awaiting review, staged, deferred, and clusters with a count on each group, each entry shows its decision state, category, identifier, and title, and the entry shown in the working surface is marked as the current selection.
2. **Given** a record open in the working surface, **When** a decision is staged for it, **Then** the queue and the staged-change ledger both update to show that decision without a page reload, and the working surface moves to the next record that has no decision yet.
3. **Given** the automatic advance is switched off, **When** a decision is staged, **Then** the queue and the ledger still update and the working surface stays on the record just decided.

---

### User Story 2: Decide with the exact bytes in view and the gates visible (Priority: P1)

The reviewer edits a record's fields and sees the exact Markdown that will be written, in a titled panel that dominates the working surface. Next to the decision controls an indicator says whether that content has been previewed, and whether edits were made since. While a preview is outstanding, previewing is the primary action. If the record's stored evidence does not yet satisfy the verification requirement, the reviewer sees that before choosing to vet, not after being refused.

**Why this priority**: This is the decision itself. The gate is the only mechanism standing between an edit and a staged write, and it is currently invisible.

**Independent Test**: Edit a field, observe the gate indicator change to the stale state, preview, observe it change to the matching state, stage the decision, and confirm no refusal occurs; separately attempt to vet a record whose stored verification state is not established and confirm the requirement was visible beforehand.

**Acceptance Scenarios**:

1. **Given** a record open with no preview taken, **When** the working surface renders, **Then** the final-content panel is titled, set in a monospaced face, wrapped rather than horizontally scrolled, and the gate indicator reads that the content has not been previewed, with previewing presented as the primary action.
2. **Given** a previewed revision, **When** the reviewer edits any field afterwards, **Then** the gate indicator changes to state that the edits no longer match the preview, before any decision is attempted.
3. **Given** the gate indicator states that the preview matches the current edits, **When** the reviewer stages that revision, **Then** the backend accepts it and the result is reported next to the control that was used.
4. **Given** a record whose stored verification state is not established, **When** the reviewer looks at the decision controls, **Then** the interface shows that vetting requires verification evidence before the control is used.

---

### User Story 3: Do not destroy anything by accident (Priority: P1)

Discarding a record, staging a merge, and discarding the whole review draft are reachable but set apart from routine decisions, and each states its consequence before it takes effect. The page header names the project directory whose profile this session will write, so a reviewer with more than one workspace open cannot apply a batch to the wrong one.

**Why this priority**: Applying a batch deletes and rewrites files irreversibly, and discarding the draft destroys every staged decision. Discarding a record and merging a cluster both delete record files. All three are currently one unconfirmed activation away, on a page that does not say which project it is attached to.

**Independent Test**: Attempt to discard a record, to stage a merge over several members, and to discard a draft holding several staged decisions, and confirm each states its consequence and requires a second confirmation; open two sessions in different project directories and confirm each page names its own.

**Acceptance Scenarios**:

1. **Given** routine and destructive controls in the working surface, **When** the decision controls render, **Then** keeping as candidate, vetting, and deferring are grouped together and discarding the record is separated from them in position, weight, and colour.
2. **Given** a draft holding three staged decisions, **When** the reviewer activates discard draft, **Then** the interface states that three staged decisions will be dropped and requires a second confirmation before anything is discarded.
3. **Given** a session on a project directory, **When** the page renders, **Then** the header names that directory and does not show its absolute path.
4. **Given** a cluster whose merge would replace three member records, **When** the reviewer stages the merge, **Then** the interface states that applying the batch will delete those three member records and requires a second confirmation before the merge is staged.

---

### User Story 4: Edit a field without fighting the control (Priority: P2)

Every editable field uses the same control, whose height follows its content. A long claim and a short scope line look like the same kind of field. Pressing Return in a field does not insert a line break, and pasting multi-line text does not produce a value the backend will reject.

**Why this priority**: It removes a class of avoidable rejection and a visible inconsistency, but a reviewer can complete a review without it.

**Independent Test**: Open records whose stored values are both short and long, confirm one control type with content-driven height, then attempt to enter and to paste a line break and confirm neither reaches the staged value.

**Acceptance Scenarios**:

1. **Given** two records whose same field holds a short and a long value, **When** each is opened, **Then** both render the same control type and the height follows the content rather than switching form.
2. **Given** a field with focus, **When** the reviewer presses Return or pastes text containing line breaks, **Then** no line break is entered and the pasted text is normalized to a single line.

---

### User Story 5: Review from the keyboard (Priority: P2)

A reviewer moves through the queue, previews, jumps into the fields, and takes routine decisions without a pointer, using the letters the text review mode already uses where they exist. The available keys are discoverable from the page. No single key applies the batch, cancels the session, or discards the draft.

**Why this priority**: It speeds up batch review substantially but is an accelerator, not a precondition.

**Independent Test**: Complete one record's full cycle — select, read, preview, decide — using only the keyboard, then confirm the keys do nothing while focus is inside a field and that no key triggers a terminal operation.

**Acceptance Scenarios**:

1. **Given** the page with focus outside any field, **When** the reviewer uses the movement, preview, field-focus, and routine-decision keys, **Then** each performs its action and the available keys are discoverable from the page itself.
2. **Given** focus inside an editable field, **When** the reviewer types a letter bound to a decision, **Then** the letter is entered as text and no decision is taken, and the field remains reachable and escapable by keyboard.
3. **Given** either colour scheme, **When** focus moves to any interactive control, **Then** that control shows a visible focus indicator.

---

### User Story 6: Review with assistive technology, in a narrow window, or in a right-to-left language (Priority: P2)

The workspace keeps its live status region, its label-to-control associations, and its field-error behavior, and additionally exposes which queue entry is current. It degrades from three regions to two and then one as the window narrows, without horizontal page scrolling, and reads correctly when the interaction language is right-to-left.

**Why this priority**: These are the delivered accessibility contract plus the corrections the redesign must not regress; they apply to every scenario above.

**Independent Test**: Drive the page with a screen reader to confirm the status region, label associations, field-error announcement, and current-queue-entry exposure; then resize to the narrowest supported width and switch the interaction language to a right-to-left one.

**Acceptance Scenarios**:

1. **Given** a field-level validation failure, **When** the backend rejects a decision for that field, **Then** the control is marked invalid, is linked to its message, receives focus, and the message is announced.
2. **Given** the narrowest supported width, **When** the page renders, **Then** there is no horizontal page scrolling and the decision controls are reachable.
3. **Given** a right-to-left interaction language, **When** the page renders, **Then** spacing, alignment, and borders follow the text direction.

### Edge Cases and Expected Errors

- **Every pending record has been decided**: the interface states that nothing is left undecided and offers batch application as the next step, instead of leaving the last reviewed record on screen (REQ-019).
- **A cluster has no generalized proposal**: the existing blocking notice remains, stays legible in the redesign, and merge controls are not offered for that cluster. The underlying rule is unchanged (NFR-007).
- **Staging is refused because the preview no longer matches the edits**: the gate indicator must already be in its stale state before the attempt, and the refusal is reported next to the control that was used (REQ-006, REQ-007, REQ-009).
- **Vetting is refused for missing verification**: the requirement is visible before the control is used (REQ-008); the backend rule and its message are unchanged (NFR-007).
- **Batch application is refused by a base-hash conflict**: the affordance that refreshes the conflicted records stays reachable, the conflicting records are identified, and neither the ledger nor the status region may state that anything was applied (NFR-007).
- **The page's draft revision is stale**: the existing refusal is surfaced as an actionable refresh next to the control that was used, not as an unexplained failure (REQ-009, NFR-007).
- **A stored field value is very long**: the field control grows with its content and the page still does not scroll horizontally (REQ-014, NFR-003).
- **The operating system colour scheme changes while the page is open**: the interface follows it without requiring a reload (NFR-002).
- **No catalog exists for the configured interaction language**: the carrier's existing fallback to the English catalog applies unchanged, so no string is left unrendered (NFR-007, OUT-001). This is preserved behavior, not new work; NFR-008 governs only the obligation that every shipped catalog carry every key.

## Requirements

### Functional Requirements

- **REQ-001**: The workspace MUST present three regions: the record queue, a working surface whose decision controls stay at the bottom of its own region, and a staged-change ledger that is visible without an additional interaction.
  - Sources: DEC-001, NEED-001, NEED-005
- **REQ-002**: The queue MUST group in-scope items as awaiting review, staged, deferred, and consolidation clusters, show a count per group, and show for each entry its decision state, category, record identifier, and title. The entry open in the working surface MUST be marked as the current selection. Whether the category is rendered as its stored directory name or as a localized label is a design-stage choice; a localized label is a new user-visible string and therefore falls under NFR-008.
  - Sources: NEED-001, DEC-001
- **REQ-003**: The queue and the staged-change ledger MUST re-render as soon as a decision is staged or withdrawn, so that what they display always matches the staged draft.
  - Sources: NEED-001, NEED-005
- **REQ-004**: The interface MUST show how many in-scope records already carry a staged or deferred decision, out of the total in scope. The figure MUST be derived from the same accounting the staged-change ledger uses, so the two can never disagree; in particular a cluster staged as one merge counts its member records exactly as the ledger counts them, rather than counting queue entries.
  - Sources: NEED-002, NEED-005
- **REQ-005**: The Markdown that will be written to the record MUST be presented as a titled panel that is visually dominant over the editable fields, set in a monospaced face, soft-wrapped rather than horizontally scrolled, and scrollable without pushing the decision controls out of reach.
  - Sources: NEED-003, DEC-001
- **REQ-006**: The interface MUST display the preview gate state next to the decision controls, distinguishing three states: not previewed; the preview matches the current edits; the edits changed after the preview. While the gate is unsatisfied, previewing MUST be presented as the primary action.
  - Sources: NEED-004, DEC-007
- **REQ-007**: The displayed gate state MUST agree with what the backend will accept. Where the page cannot determine that for itself, the backend MUST report it rather than let the page infer it.
  - Sources: NEED-004, CON-003
- **REQ-008**: The interface MUST show whether a record's stored evidence already satisfies the verification requirement, so that the reviewer knows before choosing to vet whether verification evidence must be supplied.
  - Sources: NEED-004, CON-003
- **REQ-009**: Feedback produced by a decision control — staged, refused, or a field-level validation failure — MUST appear next to that control. It MUST NOT be reachable only through the status region at the top of the page.
  - Sources: NEED-004
- **REQ-010**: The staged-change ledger MUST be presented as labeled groups with a count and the affected record identifiers, not as serialized data. Empty groups MUST be omitted, except the group of records with no decision yet, which MUST always be shown because it is the remaining work.
  - Sources: NEED-005
- **REQ-011**: Selecting a record identifier in the ledger MUST open that record or cluster in the working surface.
  - Sources: NEED-005
- **REQ-012**: Keeping as candidate, vetting, and deferring MUST be grouped together as routine decisions, and discarding a record MUST be separated from them in position, weight, and colour.
  - Sources: NEED-006, DEC-006
- **REQ-013**: Every action that removes record files MUST require an explicit second confirmation that states its consequence. Discarding a record states that batch application will delete that record file. Staging a merge states that batch application will delete the member records the merge replaces, and how many there are. Discarding the whole review draft states how many staged decisions will be dropped.
  - Sources: NEED-006, NEED-014
- **REQ-014**: Every editable structured field MUST use one control type whose height follows its content, so control height does not depend on the length of the stored value.
  - Sources: NEED-007
- **REQ-015**: A field control MUST prevent a line break from being typed and MUST normalize a line break arriving by paste, so the reviewer cannot compose a value the record codec will reject.
  - Sources: NEED-007, CON-003
- **REQ-016**: The interface MUST provide keys to move between queue entries, to preview, to focus the first editable field, and to take each routine decision, reusing the letters the text review mode already uses where they exist; letters for actions the text review mode has no key for are chosen at design stage. The available keys MUST be discoverable from the page.
  - Sources: NEED-008, OUT-002
- **REQ-017**: Keys MUST be inert while focus is inside an editable control, and that control MUST stay reachable and escapable by keyboard. No single key may trigger batch application, session cancellation, or draft discarding.
  - Sources: NEED-008, NEED-012
- **REQ-018**: After a decision is staged, the working surface MUST move to the next item with no decision yet. The advance MUST be active when the page opens and MUST be switchable off from a visible control.
  - Sources: NEED-009
- **REQ-019**: When no undecided item remains, the interface MUST state so and offer batch application as the next step, instead of leaving the last reviewed record on screen.
  - Sources: NEED-009
- **REQ-020**: The page header MUST show the name of the project directory whose profile this session will modify, supplied by the backend session snapshot rather than inferred in the page. The absolute path MUST NOT be shown.
  - Sources: NEED-013, CON-003
- **REQ-021**: The queue's current selection MUST be exposed to assistive technology, not conveyed by visual styling alone.
  - Sources: NEED-012
- **REQ-022**: The redesign MUST preserve the live, focusable status region, the association between every label and its control, and the field-error behavior that marks the control invalid, links it to its message, and moves focus to it. Every interactive control MUST present a focus indicator that is visible in both colour schemes.
  - Sources: NEED-012, CON-006
- **REQ-023**: The consolidation-cluster surface is governed by the same working-surface rules as the record surface: REQ-005 for the final content of the generalized record, REQ-006 through REQ-009 for its preview gate and its adjacent feedback, and REQ-012's separation of routine decisions from file-removing ones. Merging as candidate and merging as vetted are file-removing decisions and MUST therefore be separated as REQ-012 requires and confirmed as REQ-013 requires; keeping the records separate removes nothing and is a routine decision. The arrangement of the three within that separation is determined at design stage.
  - Sources: NEED-001, NEED-004, NEED-005, NEED-006, NEED-014

### Non-Functional Requirements

- **NFR-001**: The interface MUST be defined by a documented token set — page and panel surfaces, primary and secondary text, divider, one accent that carries emphasis, selection, and the candidate state, a second accent, and one colour each for the vetted, discarded, and deferred states — with a complete counterpart for the dark colour scheme, plus a type scale, a spacing scale, corner radii that differ by element hierarchy, and an elevation set. The preview gate MUST be signalled from those same voices rather than from an additional hue. Colour MUST encode state rather than decorate. The record title MUST be the largest text on the page and page chrome MUST NOT outrank content. A monospaced face MUST be used only where the text is literally file content or a file identifier: record identifiers, file paths, and the final-content panel.
  - Sources: NEED-010, DEC-006, DEC-007
- **NFR-002**: The active colour scheme MUST follow the operating system preference. The page MUST NOT offer an in-page light and dark switch and MUST NOT store a per-viewer scheme preference.
  - Sources: NEED-010
- **NFR-003**: The layout MUST degrade from three regions to two and then to one as width decreases, with no horizontal page scrolling and with the decision controls reachable at the narrowest supported width.
  - Sources: NEED-011
- **NFR-004**: All directional spacing, alignment, and borders MUST use logical properties, so the interface reads correctly when an interaction language sets right-to-left direction.
  - Sources: NEED-011
- **NFR-005**: The interface MUST ship as the existing page document, single stylesheet, single script, and per-language catalogs. It MUST NOT add an asset file, a content delivery network reference, a web font, or any network request, and MUST NOT widen the server's served-path allowlist. Loopback binding, the per-session token, and offline operation remain binding.
  - Sources: CON-001, OUT-003, OUT-004
- **NFR-006**: The page MUST NOT use a style element or a style attribute; dynamic state MUST be carried by class names. It MUST NOT use vector graphics: the page builds its content from script, where creating an SVG node requires the SVG namespace URL, and referencing an SVG from the stylesheet as a `data:` URI requires that namespace to be declared — either route would place an absolute URL scheme into assets that are asserted to contain none. State marks and indicators MUST be drawn with stylesheet rules or text characters.
  - Sources: CON-002
- **NFR-007**: The review safety properties MUST NOT be weakened: a revision, vetting, or merge decision cannot be staged until a byte-identical preview of that exact revision exists; a record becomes vetted only with outcome-based verification and explicit human endorsement; decisions are staged and applied as one all-or-nothing batch; every affected file is verified against its base content hash and any mismatch aborts the entire batch without writing; a project has at most one writable review session; record identity and protected fields remain read-only; record bytes are never rewritten for display. Backend extension is permitted only where the interface needs data or an operation it cannot derive for itself, and only if the extension is additive, weakens none of these properties, and is covered by repository tests.
  - Sources: CON-003, OUT-001
- **NFR-008**: Every new user-visible string MUST be added to every language catalog shipped with the review interface, with identical top-level keys across all of them and translated text in each. The structured field label set MUST keep exactly its current keys. No string may be introduced in English only.
  - Sources: CON-004, DEC-004
- **NFR-009**: Interface text, diagnostics, and completion messages MUST follow the configured interaction language. Record content MUST be displayed in the language it was written in and MUST NOT be translated as a display side effect.
  - Sources: CON-005
- **NFR-010**: Repository and release gates MUST validate the changed assets before distribution; neither `codexspec init` nor an end user's first review may be the first place a packaging or generation error appears. Where a repository test currently guards an offline, accessibility, or front-end contract, that guarantee MUST remain guarded — by satisfying the existing assertion, or by deliberately updating the assertion when a guarded name genuinely changes — and MUST NOT be removed.
  - Sources: CON-006

### Key Entities

- **Decision state**: what the staged draft currently holds for one record or cluster, as the queue marks it — awaiting review, staged as revised, staged as vetted, staged as discarded, or deferred. These are the states NFR-001's state colours cover; the accent carries awaiting review, and staged as revised shares it.
- **Ledger group**: one of the seven accounting groups the backend already reports — added, replaced, promoted, removed, merged, deferred, and undecided. Ledger groups are how the staged batch is counted and are not a second set of colours; several of them can describe one record's single decision state.
- **Queue group**: the four sections the queue presents — awaiting review, staged, deferred, and consolidation clusters. A queue group is a presentation grouping over decision state; it introduces no new state.
- **Preview gate state**: one of three values for the record open in the working surface — not previewed, preview matches the current edits, edits changed after the preview.
- **Verification requirement state**: whether a record's stored evidence already establishes outcome-based verification, which determines whether vetting needs supplementary evidence.
- **Design token**: a named value for a surface, text colour, hairline, accent, state colour, gate colour, type step, spacing step, or corner radius, each with a light-scheme and a dark-scheme value.
- **Project identity**: the name of the project directory whose profile the session will modify, supplied by the backend session snapshot.

## Success Criteria

### Measurable Outcomes

- **SC-001**: From the page alone, a reviewer can state for every in-scope record whether it is undecided, staged and as what, or deferred, without opening or expanding another panel.
- **SC-002**: The count of in-scope records already decided and the total are both readable without counting list entries.
- **SC-003**: Before using a decision control, a reviewer can tell whether it will be accepted; a decision the interface presents as available is not refused for a gate reason.
- **SC-004**: No action that removes record files, and no action that drops staged decisions, completes on a single unconfirmed activation; each states its consequence — which files batch application will delete and how many, or how many staged decisions will be dropped — before taking effect. This covers discarding a record, staging a merge, and discarding the draft.
- **SC-005**: For a given field, control height does not vary with the stored value's length, and no field value can be made to contain a line break.
- **SC-006**: One record's full decision cycle — select, read the final content, preview, decide — is completable from the keyboard with no pointer, the focused control is visibly indicated at every step in both colour schemes, and no key performs batch application, cancellation, or draft discarding.
- **SC-007**: The interface is usable with no horizontal page scrolling from the narrowest supported width upward, in both colour schemes, and in a right-to-left interaction language.
- **SC-008**: Every string the interface can display is present and translated in every shipped interaction-language catalog, with identical top-level keys across catalogs.
- **SC-009**: The page states which project directory a batch application will write to.
- **SC-010**: A defect introduced into the changed assets fails a repository or release gate before any user installation path runs it.

## Confirmed Constraints and Decisions

- **CON-001** → NFR-005: offline delivery as the existing page, stylesheet, script, and catalogs; the served-path allowlist is not widened for presentation.
- **CON-002** → NFR-006: no style element or attribute, no inline vector graphics; state marks drawn with stylesheet rules or text characters.
- **CON-003** → NFR-007, REQ-007, REQ-008, REQ-015, REQ-020: the review safety properties are invariant; the backend data surface may be extended additively, under test coverage, where the interface cannot derive what it needs.
- **CON-004** → NFR-008: every interaction language stays complete; no English-only string.
- **CON-005** → NFR-009: interface language from configuration; record content untranslated.
- **CON-006** → NFR-010, REQ-022: maintainer and release validation precede user installation; existing guarded guarantees stay guarded.
- **DEC-001** → REQ-001: three regions, with the ledger permanently visible. Rejected: two regions with the ledger collapsed into a header strip, which would give the working surface more width but put the record of what will be written behind an interaction.
- **DEC-006** → NFR-001, REQ-012: colour, spacing, radius and elevation follow the design system the user's other project already uses — a cream ground, a terracotta primary accent, a sage second voice, rounded geometry, soft elevation instead of hairline-only edges, and that system's spacing scale. Rejected: the neutral paper-and-ink direction with an indigo accent, superseded because the interface must match that project; and taking the palette's hues while keeping the previous sharp geometry, which was built first and rejected because the reference's softness comes from its radii, elevation and spacing rather than its hues. Four deviations are recorded in `requirements.md`: the reference's typefaces and icon set cannot be used because CON-001 forbids a network request and CON-002 forbids vector graphics, field controls take its medium rather than its pill radius, and one brick red is added because the palette carries no destructive hue.
- **DEC-007** → NFR-001, REQ-006: the preview gate is signalled by the adopted palette's own two accents — a neutral tint for not previewed, the sage second voice for a matching preview, the terracotta accent for edits made after it. Rejected: a dedicated fifth hue, which the superseded neutral palette needed and this one does not; reusing the discard colour, which would read as an error although nothing failed; reusing the defer grey, which would make the page's only safety signal recede.
- **DEC-004** → NFR-008: new interface strings are in scope. Rejected: a stylesheet-only change with no new strings, which would leave the invisible decision state, the invisible preview gate, and the serialized ledger in place.
- **DEC-005**: this work is recorded as its own feature directory while sharing the branch of the carrier feature, so both land together. This governs where the work is recorded, not what is built, and therefore produces no requirement.

## Out of Scope

- **OUT-001**: Review workflow and profile model changes — no decision action is added; no staging, application, or conflict rule changes; one-record-per-file storage, candidate and vetted semantics, the outcome-verification requirement, and eligibility for upstream contribution are untouched. Reason: the reported problem is the presentation of the existing workflow.
- **OUT-002**: The text review mode's presentation — the terminal fallback keeps its current prompts and output; its key letters are borrowed by the browser interface, not changed in it. Reason: the fallback's value is availability in headless environments, not appearance.
- **OUT-003**: Build tooling and third-party front-end dependencies — no bundler, build step, stylesheet or JavaScript framework, icon set, or web font. Reason: the page is served as static assets over loopback with no network access.
- **OUT-004**: Remote or network-accessible review — no public hosting, local-network binding, remote device access, external authentication, or telemetry. Reason: the confirmed workflow is private, local, and offline.

## Assumptions

- **A-001**: The narrowest supported viewport width used to verify NFR-003 and SC-007 is 420 logical pixels. The confirmed requirement states only "the narrowest supported width"; this figure comes from the design plan the user approved and exists so the criterion is testable. It is an assumption, not a confirmed requirement, and a different figure does not change any requirement above.
- **A-002**: "Awaiting review", "staged", "deferred", and "clusters" are the queue's grouping labels in this document; their final wording in each interaction language is chosen when the catalog strings are written, under NFR-008.

## Dependencies

- Feature `2026-0927-2310d6-html-distill-review` — its local server, review state machine, record codec, apply transaction, session store, and the repository tests that guard their contracts. Every requirement here is a change to how that feature's workspace presents itself.
- The repository's front-end contract tests, which assert the offline property, the absence of any absolute URL scheme in the front-end assets, the accessibility attributes, and catalog key parity across interaction languages.
- Project convention `Con-2026-0812-2114vj-1` — translation catalogs are updated in lockstep, with identical top-level keys.
- Vetted project constraint `C-2026-0902-054178-1` — maintainer-only mechanisms affecting user-facing distributed artifacts must fail at project and release gates, never first at a user's installation.

## Open Questions

None. Every question raised during requirement discovery and during specification review has been answered by the user and is carried as a requirement.

The three discovery questions are recorded in `requirements.md`: automatic advance is active at open with a visible switch (OPEN-001, REQ-018); the header shows the project directory name (OPEN-002, REQ-020); the colour scheme follows the operating system only (OPEN-003, NFR-002).

Specification review raised one further matter: a confirmed merge removes every superseded member record when the batch is applied, so merging removes files exactly as discarding does, while the confirmed confirmation rule named only discarding. The user extended the rule to merging, confirmed as NEED-014 and carried by REQ-013 and REQ-023.

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001, REQ-002, REQ-003, REQ-023 | Full — grouping and content, current selection, re-render, cluster surface in scope |
| NEED-002 | REQ-004 | Full |
| NEED-003 | REQ-005 | Full |
| NEED-004 | REQ-006, REQ-007, REQ-008, REQ-009, REQ-023 | Full — gate display, gate authority, verification visibility, adjacent feedback, merge gate |
| NEED-005 | REQ-001, REQ-003, REQ-004, REQ-010, REQ-011, REQ-023 | Full — ledger presence, re-render, shared accounting with the progress figure, readable groups, navigation, cluster surface |
| NEED-006 | REQ-012, REQ-013, REQ-023 | Full — routine and destructive separation, second confirmation, cluster surface |
| NEED-007 | REQ-014, REQ-015 | Full |
| NEED-008 | REQ-016, REQ-017 | Full |
| NEED-009 | REQ-018, REQ-019 | Full — advance with switch, end-of-queue state |
| NEED-010 | NFR-001, NFR-002 | Full — token system, scheme follows the operating system |
| NEED-011 | NFR-003, NFR-004 | Full |
| NEED-012 | REQ-017, REQ-021, REQ-022 | Full — keyboard reachability, selection semantics, preserved behavior, focus indicator in both schemes |
| NEED-013 | REQ-020 | Full |
| NEED-014 | REQ-013, REQ-023 | Full — merging carries the same second confirmation and the same separation as discarding |
| CON-001 | NFR-005 | Constraint preserved |
| CON-002 | NFR-006 | Constraint preserved |
| CON-003 | NFR-007, REQ-007, REQ-008, REQ-015, REQ-020 | Constraint preserved; its permitted extension is the source of REQ-007 and REQ-020 |
| CON-004 | NFR-008 | Constraint preserved |
| CON-005 | NFR-009 | Constraint preserved |
| CON-006 | NFR-010, REQ-022 | Constraint preserved |
| DEC-001 | REQ-001 | Decision preserved |
| DEC-002 | — | Superseded by DEC-006; retained in `requirements.md` under Superseded Entries |
| DEC-003 | — | Superseded by DEC-007; retained in `requirements.md` under Superseded Entries |
| DEC-006 | NFR-001, REQ-012 | Decision preserved |
| DEC-007 | NFR-001, REQ-006 | Decision preserved |
| DEC-004 | NFR-008 | Decision preserved |
| DEC-005 | Not applicable | Process decision: it governs where this work is recorded and on which branch it lands, not what is built. Recorded under Confirmed Constraints and Decisions. |
| OUT-001 | Out of Scope | Exclusion preserved |
| OUT-002 | Out of Scope, REQ-016 | Exclusion preserved; the browser interface borrows the text mode's key letters without changing that mode |
| OUT-003 | Out of Scope, NFR-005 | Exclusion preserved |
| OUT-004 | Out of Scope, NFR-005 | Exclusion preserved |
| OPEN-001 | REQ-018 | Resolved during discovery; recorded as a requirement, not an open item |
| OPEN-002 | REQ-020 | Resolved during discovery; recorded as a requirement, not an open item |
| OPEN-003 | NFR-002 | Resolved during discovery; recorded as a requirement, not an open item |
