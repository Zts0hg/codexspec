# Confirmed Requirements: distill-review-interface-design

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-1001-2205zz`<br>
**Feature Directory**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/`<br>
**Status**: Confirmed<br>
**Last Confirmed**: 2026-10-02 00:02:01 +0800

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Context

Feature `2026-0927-2310d6-html-distill-review` delivered the offline HTML carrier for manual distill review: a loopback server, a staged-decision draft, a preview-before-stage gate, atomic batch application, and conflict detection. That feature's confirmed requirements cover the workflow and its safety properties; none of them covers how the workspace presents itself.

The delivered page is styled by 17 declarations with no design tokens, no type or spacing scale, and native browser control styling. As a result the reviewer cannot see which records already carry a decision, cannot see how much of the queue is left, cannot tell that the backend requires a byte-identical preview before a decision can be staged, and reads the staged-change ledger as serialized JSON. Routine and destructive actions share one visual weight, including a control that destroys every staged decision without confirmation. Field controls switch between a single-line and a multi-line form depending on how long the stored value happens to be, and the multi-line form invites a line break that the record codec rejects.

This feature changes presentation, information architecture, and interaction clarity. It changes no workflow semantics.

## Needs

### NEED-001: The queue shows every record's decision state

- **Status**: confirmed
- **Statement**: The record list MUST group in-scope items by decision state — awaiting review, staged, deferred, and consolidation clusters — and show a count per group. Each item MUST show its decision state, its category, its record identifier, and its title. The item being edited MUST be marked as the current selection. The list MUST re-render as soon as a decision is staged or a decision is withdrawn, so the displayed state always matches the staged draft.
- **Rationale**: Reviewing a batch requires knowing what is already decided and what is left; the delivered list shows only an identifier and a claim, carries no selection state, and is not re-rendered after a decision is staged.
- **User Evidence**: "布局和样式并不美观，也不够清晰友好"; the user chose the full scope (visual, information architecture, and interaction clarity) and the three-column layout whose first column is this queue.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-002: Review progress is visible without counting

- **Status**: confirmed
- **Statement**: The interface MUST show how many in-scope records already carry a staged or deferred decision out of the total in scope.
- **Rationale**: Progress through the queue is the single most useful orientation signal in a batch review and is currently absent.
- **User Evidence**: The user approved the design plan in which progress appears in the page header and above the staged-change ledger.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-003: The exact file content is the primary object of the working surface

- **Status**: confirmed
- **Statement**: The Markdown that will be written to the profile record MUST be presented as a titled panel that is visually dominant over the editable fields, set in a monospaced face, scrollable without pushing the decision controls out of reach, and wrapped rather than horizontally scrolled.
- **Rationale**: The decision the user signs is "these exact bytes"; the delivered page shows them as an untitled preformatted block between the fields and the buttons, with no indication of what it is.
- **User Evidence**: The user approved the design plan that names this panel the primary element of the page.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-004: The preview gate and action feedback are local to the controls

- **Status**: confirmed
- **Statement**: Because the backend refuses to stage a revision, vetting, or merge decision without a byte-identical preview of that exact revision, the interface MUST show the current gate state next to the decision controls, distinguishing: not previewed; the preview matches the current edits; the edits changed after the preview. While the gate is unsatisfied, previewing MUST be presented as the primary action. The displayed gate state MUST agree with what the backend will accept; where the page cannot determine that for itself, the backend MUST report it rather than let the page infer it. The interface MUST also show whether the stored record already satisfies the verification requirement, so that before choosing to vet the user knows whether supplying verification evidence is required. Feedback produced by a decision control — staged, rejected, or field-level validation failure — MUST appear next to that control, and MUST NOT be reachable only through the status line at the top of the page.
- **Rationale**: The gate is the page's only safety mechanism and is currently invisible: a decision silently does nothing and the explanation appears far from the control that was used. The page also tracks the gate on its own while the backend holds the authoritative record of which revision was previewed, so the two can disagree and present the user with a rejection that the interface said would not happen.
- **User Evidence**: The user approved the design plan that makes the gate an explicit three-state indicator, and confirmed that the backend may be extended to supply data the interface needs for clearer display.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-005: The staged-change ledger is readable and navigable

- **Status**: confirmed
- **Statement**: The staged-change summary MUST be presented as grouped, labeled counts with the affected record identifiers, not as serialized JSON. Empty groups MUST be omitted, except the group of records with no decision yet, which MUST always be shown because it is the remaining work. Selecting a listed identifier MUST open that record or cluster in the working surface.
- **Rationale**: This panel is the ledger of what batch application will write; as raw JSON with every empty group printed it cannot be scanned, and it offers no way to reach the records it names.
- **User Evidence**: The user chose the three-column layout in which this ledger is permanently visible rather than collapsed into a header strip.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-006: Destructive actions are separated and confirmed

- **Status**: confirmed
- **Statement**: Routine decisions (keep as candidate, vet, defer) MUST be grouped together, and discarding a record MUST be visually separated from them and distinct in weight and color. Discarding a record and discarding the whole review draft MUST each require an explicit second confirmation that states the consequence: that applying the batch will delete the record file, and how many staged decisions discarding the draft will drop.
- **Rationale**: Four identically weighted controls make a destructive choice as easy to hit as a routine one, and the control that destroys the entire staged draft currently acts with no confirmation.
- **User Evidence**: The user selected the destructive-action confirmation enhancement.
- **Extended By**: NEED-014, which applies the same second confirmation to merging. This entry's statement is unchanged and remains accurate; it did not cover merging because merging was not examined when it was confirmed.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-007: One field control, adaptive in height, that cannot hold a line break

- **Status**: confirmed
- **Statement**: Every editable structured field MUST use a single control type whose height follows its content, so that control height no longer depends on how long the stored value happens to be. Because the record codec rejects any field value containing a line break, the control MUST prevent a line break from being typed and MUST normalize a line break arriving by paste, so the user cannot compose a value the backend will refuse.
- **Rationale**: Choosing between a single-line and a multi-line control by value length makes the same field look different from record to record, and the multi-line control invites exactly the input the codec rejects.
- **User Evidence**: The user selected the uniform adaptive single-line field control enhancement.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-008: The queue and the decisions are operable from the keyboard

- **Status**: confirmed
- **Statement**: The interface MUST provide keys to move between queue items, to preview, to focus the first editable field, and to take each routine decision, reusing the letters already used by the text review mode where they exist. The available keys MUST be discoverable from the page. Keys MUST be inert while focus is inside an editable control, and MUST leave that control reachable by keyboard. No single key may trigger batch application, session cancellation, or draft discarding.
- **Rationale**: A queue reviewed in batches is faster from the keyboard, and consistency with the text mode's letters avoids teaching two key maps for one workflow; terminal operations must stay deliberate.
- **User Evidence**: The user selected the keyboard shortcut enhancement.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-009: Staging advances to the next undecided item

- **Status**: confirmed
- **Statement**: After a decision is staged, the working surface MUST move to the next item that has no decision yet. The advance MUST be active when the page opens, and MUST be switchable off from a visible control. When no undecided item remains, the interface MUST say so and offer batch application as the next step instead of leaving the last reviewed record on screen.
- **Rationale**: Advancing the queue is the expected continuation after a decision, and the end of the queue is currently an unmarked state with no exit. The switch exists because a reviewer who wants to re-read the record just decided otherwise has no way to stop the jump.
- **User Evidence**: The user selected the automatic-advance enhancement, and confirmed that it is on when the page opens and carries a visible switch.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-010: A deliberate visual system, complete in both color schemes

- **Status**: confirmed
- **Statement**: The interface MUST be defined by a documented token set — page and panel surfaces, primary and secondary text, hairline, one accent, and one colour per decision state — with a complete counterpart for the dark colour scheme, plus a type scale, a spacing scale, and corner radii that differ by element hierarchy. Colour MUST encode decision state rather than decorate. The record title MUST be the largest text on the page; page chrome MUST NOT outrank content. A monospaced face MUST be used only where the text is literally file content or a file identifier: record identifiers, file paths, and the final-content panel. The active colour scheme MUST follow the operating system preference; the page MUST NOT offer an in-page light and dark switch and MUST NOT store a per-viewer scheme preference.
- **Rationale**: The page currently has no colour system at all; the dark scheme is whatever the browser defaults produce, and one inherited rule renders every field value in semibold so editable text reads as a label.
- **User Evidence**: The user chose the "Ledger" direction from three palettes, each presented with its light and dark token values, and confirmed following the operating system scheme with no in-page switch.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-011: The layout holds up at narrow widths and in right-to-left languages

- **Status**: confirmed
- **Statement**: The three columns MUST degrade to two and then to one as width decreases, with no horizontal page scrolling and with the decision controls reachable at the narrowest supported width. All directional spacing, alignment, and borders MUST use logical properties so the interface reads correctly when an interaction language sets right-to-left direction.
- **Rationale**: The delivered layout stacks three fixed-proportion columns at one breakpoint, truncates the queue, and aligns queue text with a physical left edge although the page already switches to right-to-left for Arabic.
- **User Evidence**: The user approved the design plan including its three breakpoints and the right-to-left correction.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-012: The delivered accessibility behavior is preserved and extended

- **Status**: confirmed
- **Statement**: The redesign MUST preserve the live, focusable status region, the association between each label and its control, and the existing field-error behavior that marks the control invalid, links it to its message, and moves focus to it. It MUST additionally expose the current queue selection to assistive technology and give every control a focus indicator that is visible in both colour schemes.
- **Rationale**: These behaviors are the page's current accessibility contract and are guarded by repository tests; a visual rewrite must not drop them, and the new queue introduces a selection state that needs the same treatment.
- **User Evidence**: The user approved the design plan, which keeps every asserted accessibility attribute and adds queue selection semantics.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-013: The page identifies the project it will write to

- **Status**: confirmed
- **Statement**: The page header MUST show the name of the project directory whose profile this session will modify. The full absolute path MUST NOT be shown. The value MUST be supplied by the backend session snapshot rather than inferred in the page.
- **Rationale**: Applying a batch writes profile files irreversibly, and nothing on the delivered page identifies which project is being written: the record paths are relative and therefore identical in every project, and the page title is a constant. In a repository checked out as several Git worktrees, each worktree carries its own profile store, so two review pages open side by side are indistinguishable.
- **User Evidence**: The user asked what project context meant, then chose to show the project directory name rather than nothing or the full path.
- **Confirmed At**: 2026-10-01 22:26:56 +0800

### NEED-014: Merging carries the same second confirmation as discarding

- **Status**: confirmed
- **Statement**: Staging a merge MUST require the same explicit second confirmation that NEED-006 requires for discarding, stating the same kind of consequence: that applying the batch will delete the member records this merge replaces, and how many there are. This extends NEED-006 to the third action that removes record files; it changes nothing about what a merge does.
- **Rationale**: A confirmed merge creates the generalized record and removes every superseded member record when the batch is applied, so merging removes files exactly as discarding does. Protecting one file-removing action and leaving the other unprotected would contradict this feature's stated purpose of preventing accidental destruction.
- **User Evidence**: Specification review reported that merging removes files while the confirmed confirmation rule named only discarding a record and discarding the draft, and stated that extending it would be a new product decision. The user decided to extend it: "把二次确认扩到合并。"
- **Confirmed At**: 2026-10-01 22:42:17 +0800

## Constraints

### CON-001: The offline three-asset delivery surface does not change

- **Status**: confirmed
- **Statement**: The interface MUST ship as the existing page document, single stylesheet, single script, and per-language catalogs, and MUST NOT add an asset file, a content delivery network reference, a web font, or any network request. The loopback binding, per-session token, and offline operation confirmed for the delivered feature remain binding. The server's served-path allowlist therefore stays as narrow as it is today: although CON-003 permits backend extension, widening a security allowlist is not justified for presentation, and this redesign needs no additional file.
- **User Evidence**: Inherited from the delivered feature's confirmed constraint that assets ship with CodexSpec and use no network access; the user did not request any change to it.

### CON-002: No inline styling, and no inline vector graphics

- **Status**: confirmed
- **Statement**: The server's content-security policy admits only same-origin stylesheets, so the page MUST NOT use a style element or a style attribute; dynamic state MUST be carried by class names. A repository test asserts that the three front-end assets contain no absolute URL scheme, which rules out inline vector graphics because a vector root element declares a namespace URL. State marks and indicators MUST therefore be drawn with stylesheet rules or text characters.
- **User Evidence**: Both rules are existing properties of the shipped carrier and its test suite; the user approved a design plan that states them as hard boundaries.

### CON-003: Review safety semantics are invariant; the backend data surface may be extended

- **Status**: confirmed
- **Statement**: The following properties are invariant and MUST NOT be weakened: a revision, vetting, or merge decision cannot be staged until a byte-identical preview of that exact revision exists; a record becomes vetted only with outcome-based verification and explicit human endorsement; decisions are staged and applied as one all-or-nothing batch; every affected file is verified against its base content hash and any mismatch aborts the entire batch without writing; a project has at most one writable review session; record identity and protected fields remain read-only; record bytes are never rewritten for display. Within those invariants the backend MAY be extended where the interface needs data or an operation it cannot derive for itself — for example additional read-only fields in the session snapshot, or a read-only endpoint — provided the extension is additive, weakens no invariant above, and is covered by repository tests.
- **User Evidence**: "CON-003要求的后端零改动不是硬性规则，如果我们为了展示上更加清楚清晰，交互上更加便捷高效，而需要后端提供一些相应的数据，那么可以改动后端来匹配我们的改造。" The user also authorized the project-directory field when resolving the project-context question.

### CON-004: Every interaction language stays complete

- **Status**: confirmed
- **Statement**: Each new user-visible string MUST be added to every language catalog shipped with the review interface, with identical top-level keys across all of them and translated text in each, matching the repository's existing catalog-parity rule. The structured field label set MUST keep exactly its current keys. A new string MUST NOT be introduced in English only.
- **User Evidence**: The user chose the scope that explicitly includes new interface strings; project convention `Con-2026-0812-2114vj-1` requires translation catalogs to be updated in lockstep.

### CON-005: Human-facing language follows project configuration

- **Status**: confirmed
- **Statement**: The interface, its diagnostics, and its completion messages MUST use the configured interaction language. Profile record content MUST be displayed in the language it was written in and MUST NOT be translated for display.
- **User Evidence**: Inherited from the delivered feature's confirmed language constraint; unchanged by this feature.

### CON-006: Maintainer validation precedes user installation

- **Status**: confirmed
- **Statement**: The changed assets MUST be validated by repository and release gates before distribution. Neither `codexspec init` nor an end user's first review may be the first place a packaging or generation error appears. Where a repository test currently guards an offline, accessibility, or front-end contract, the redesign MUST keep that guarantee guarded — by satisfying the existing assertion, or by deliberately updating the assertion when a guarded name genuinely changes — and MUST NOT remove the guarantee.
- **User Evidence**: Vetted project constraint `C-2026-0902-054178-1` applies to user-facing distributed assets; the delivered feature carries the same constraint.

## Decisions

### DEC-001: Three columns — queue, working surface, staged-change ledger

- **Status**: confirmed
- **Decision**: Keep three regions and redefine their proportions: the grouped queue, the working surface with its decision controls fixed to the bottom of its own column, and the permanently visible staged-change ledger.
- **Alternatives Rejected**: Two columns with the ledger reduced to a summary strip in the page header, expandable on demand — this gives the working surface more width and more room for long field values, but puts the record of what will be written behind an interaction.
- **Reason**: During a batch review the ledger is consulted continuously, so it stays on screen; width for the working surface is recovered by removing the delivered layout's wasted vertical space instead.
- **User Evidence**: The user chose the three-column wireframe over the two-column one.

### DEC-006: The project's existing design-system palette, with its geometry and elevation

- **Status**: confirmed
- **Decision**: Colour, spacing, radius and elevation follow the design system the user's other project already uses: a cream ground with a terracotta primary accent and a sage second voice, each carrying a 100–900 tonal ramp; rounded geometry; soft ink-tinted elevation in place of hairline-only edges; and that system's 1.10× spacing scale. Adopting it means adopting its geometry and air, not only its hues.
- **Alternatives Rejected**: The neutral paper-and-ink direction with an indigo accent recorded in the superseded DEC-002 — rejected because the interface must look like the user's other project, which this system already defines. Taking only the palette's hues while keeping the previous sharp-cornered, hairline-bordered, tight-spacing geometry — built first and rejected: the system's softness comes from its radii, its soft shadows and its spacing rather than from its hues, and the system's own guidance forbids sharp corners, hairline-only geometry and crowding.
- **Reason**: Visual consistency with an existing project the user owns, taken from that project's own design-system tokens rather than approximated.
- **Accepted Deviations**: Four, each recorded because the reference cannot be followed literally here. The system's two typefaces load from a font service, which CON-001 forbids, so the platform stack carries the type and the display voice is carried by weight and size — this difference cannot be closed. The system's icon set is vector, which CON-002 forbids, so state marks remain text characters. Field controls take the system's medium radius rather than its pill radius, because a pill radius fights a control that grows to fit a long value. One brick red is added, because the palette carries no destructive hue and reusing the accent would make a file-removing control look like the primary action, contradicting NEED-006.
- **User Evidence**: "配色和样式跟我的预期不太符合，参考 ... 这个其他项目的设计稿使用的配色"; then, after only the hues had been taken, "还是不太对，为什么设计稿的配色和元素样式看起来很柔和，你模仿过来的元素就很生硬呢？"; then, after the geometry, elevation and spacing were adopted, "柔和度对了。"
- **Confirmed At**: 2026-10-02 00:02:01 +0800

### DEC-007: The preview gate signal comes from the palette's own two voices

- **Status**: confirmed
- **Decision**: The gate's three states are carried by the adopted palette without adding a hue: a neutral tint for not previewed, the sage second voice for a preview that matches the current edits, and the terracotta accent for edits made after the preview.
- **Alternatives Rejected**: Adding a dedicated fifth hue, as the superseded DEC-003 required — unnecessary here, because that decision existed only to escape a neutral palette in which neither the discard red nor the defer grey could carry the signal. Reusing the discard colour, which would read as an error although nothing failed. Reusing the defer grey, which would make the page's only safety signal recede.
- **Reason**: DEC-003's intent was a gate signal that is neither an error nor recessive. The adopted palette supplies two accents with exactly that division of meaning — sage for ready, terracotta for needs attention — so the intent is satisfied with no addition to the palette.
- **User Evidence**: Derived by the assistant from the palette the user supplied in DEC-006 and disclosed when it was applied; the user confirmed the resulting interface. The user did not separately rule on this mapping, so it rests on DEC-006.
- **Confirmed At**: 2026-10-02 00:02:01 +0800

### DEC-004: The scope includes new interface strings

- **Status**: confirmed
- **Decision**: Introduce the new user-visible strings this redesign needs, and translate them into every shipped interaction language.
- **Alternatives Rejected**: A stylesheet-only change introducing no new strings — the cheapest option, and the one the user was offered explicitly; it would leave the invisible decision state, the invisible preview gate, and the serialized ledger in place, which are the causes of the reported unclarity.
- **Reason**: The reported problem is clarity, not only appearance, and the clarity fixes require naming things the interface currently does not name.
- **User Evidence**: The user chose the full scope over the stylesheet-only option.

### DEC-005: A new feature workspace on the existing branch

- **Status**: confirmed
- **Decision**: Record this work as a new feature directory while continuing on the branch that carries the delivered carrier feature, so both land together.
- **Alternatives Rejected**: A new branch stacked on the current one, which would split one unreleased surface across two reviews; appending these entries to the delivered feature's requirements record, which would re-open a confirmed and fully reviewed artifact set and break the correspondence between its confirmed entries and what it delivered.
- **Reason**: The interface is not yet released, so shipping it and then redesigning it has no value; a separate requirements record keeps each feature's confirmed entries a faithful record of its own commitment.
- **User Evidence**: The user chose the new feature directory without a branch switch. The standard feature-creation script was therefore not used, because it always creates a branch; the directory and this record were created in the form that script produces.

## Out of Scope

### OUT-001: Review workflow and profile model changes

- **Status**: confirmed
- **Statement**: This feature adds no decision action, changes no staging, application, or conflict rule, and changes nothing about one-record-per-file storage, candidate and vetted semantics, the outcome-verification requirement, or eligibility for contribution upstream.
- **Reason**: The reported problem is the presentation of the existing workflow.
- **User Evidence**: The user described the page's layout, styling, and clarity, and asked for no behavioral change.

### OUT-002: The text review mode's presentation

- **Status**: confirmed
- **Statement**: The explicit terminal fallback keeps its current prompts and output. Only the browser carrier is redesigned, and the shared key letters are borrowed from the text mode rather than changed in it.
- **Reason**: The request concerns the HTML page; the fallback's value is its availability in headless environments, not its appearance.
- **User Evidence**: The user's request names the page and its asset files.

### OUT-003: Build tooling and third-party front-end dependencies

- **Status**: confirmed
- **Statement**: No bundler, build step, stylesheet or JavaScript framework, icon set, or web font is introduced.
- **Reason**: The page is served as three static assets over loopback with no network access; a dependency would violate that delivery model.
- **User Evidence**: Follows from the offline, three-asset constraint the user approved.

### OUT-004: Remote or network-accessible review

- **Status**: confirmed
- **Statement**: Unchanged from the delivered feature: no public hosting, no local-network binding, no remote device access, no external authentication, and no telemetry.
- **Reason**: The confirmed workflow is private, local, and offline.
- **User Evidence**: Inherited from the delivered feature's confirmed exclusion.

## Open Questions

No open questions block specification generation. The three questions raised during discovery were answered and are recorded below.

### OPEN-001: Is automatic advance always on, and does it need a visible switch?

- **Status**: resolved
- **Resolved By**: NEED-009 — on when the page opens, with a visible switch.
- **Owner**: User

### OPEN-002: Should the page header show which project is being reviewed?

- **Status**: resolved
- **Resolved By**: NEED-013 — show the project directory name, not the absolute path. Resolving this also prompted the user to replace the proposed backend-zero-change rule with the invariant-based rule now recorded in CON-003.
- **Owner**: User

### OPEN-003: Is a manual light and dark switch wanted?

- **Status**: resolved
- **Resolved By**: NEED-010 — follow the operating system scheme only, with no in-page switch and no stored per-viewer preference.
- **Owner**: User

## Superseded Entries

### DEC-002: The "Ledger" visual direction

- **Status**: superseded
- **Replaced By**: DEC-006
- **Decision as confirmed**: A neutral paper-and-ink base with a single indigo accent for emphasis and selection, one colour each for vetted, discarded, and deferred, and monospace restricted to record identifiers, file paths, and the final-content panel.
- **Alternatives Rejected at the time**: A dark-first console direction, visually continuous with the terminal next to it but weaker for long prose and making the light scheme a compromise; a neutral grey base with one blue accent, the safest option and the least recognizable.
- **Historical Note**: Confirmed 2026-10-01 22:26:56 +0800 from three palettes presented with their light and dark token values. Superseded 2026-10-02 00:02:01 +0800 when the user supplied the design system their other project already uses and required the interface to match it. The monospace restriction this entry introduced is not affected by the supersession: it is carried independently by NEED-010.

### DEC-003: One colour beyond the decision states encodes the preview gate

- **Status**: superseded
- **Replaced By**: DEC-007
- **Decision as confirmed**: Add a fifth hue, used only for the preview gate indicator and the edge of the final-content panel when the preview no longer matches the edits.
- **Alternatives Rejected at the time**: Reusing the discard colour, which would read as an error although nothing failed; reusing the defer grey, which would make the page's only safety signal recede.
- **Historical Note**: Confirmed 2026-10-01 22:26:56 +0800, having been raised as an assistant assumption with its alternatives. Superseded 2026-10-02 00:02:01 +0800: the replacement palette carries two accents whose meanings already divide into ready and needs-attention, so the signal this entry required no longer needs a hue of its own. Its intent — a gate signal that is neither an error nor recessive — is preserved in DEC-007.

## Confirmation Log

### Session 2026-10-01 22:26:56 +0800

- **Summary Presented**: Redesign of the delivered HTML distill review interface along three axes — visual system, information architecture, and interaction clarity — with the review workflow unchanged. Needs: a state-grouped queue that re-renders on every staged decision; visible progress; the exact final file content as the working surface's primary object; an explicit preview-gate state beside the decision controls that agrees with what the backend will accept, plus visibility of whether a record already satisfies the verification requirement; a readable and navigable staged-change ledger; destructive actions separated and confirmed with their consequence stated; one adaptive field control that cannot hold a line break; keyboard operation reusing the text mode's letters with no bare key bound to a terminal operation; automatic advance to the next undecided item, active at open with a visible switch; a documented token system complete in both colour schemes and following the operating system only; responsive, direction-correct layout; the delivered accessibility contract preserved and extended; and a header that identifies the project directory being written. Constraints: offline three-asset delivery with the served-path allowlist unchanged; no inline styling and no inline vector graphics; review safety invariants fixed while the backend data surface may be extended additively under test coverage; all interaction languages kept complete; interface language from configuration with record content untranslated; maintainer validation before user installation with existing guarantees kept guarded. Decisions: three-column layout; the Ledger visual direction; a fifth colour reserved for the preview gate; new interface strings in scope; a new feature workspace on the existing branch. Exclusions: workflow and profile model changes; the text mode's presentation; build tooling and third-party front-end dependencies; remote or network-accessible review.
- **User Confirmation**: The user replied "确认" to the final summary, which explicitly asked for a decision on DEC-003 — presented as an assistant assumption together with its rejected alternatives — before confirming the whole set. Earlier in the same session the user confirmed the automatic-advance and colour-scheme defaults ("确认OPEN-001/OPEN-003"), chose to display the project directory name, and replaced the proposed backend-zero-change rule with an invariant-based rule: "CON-003要求的后端零改动不是硬性规则，如果我们为了展示上更加清楚清晰，交互上更加便捷高效，而需要后端提供一些相应的数据，那么可以改动后端来匹配我们的改造。"
- **Entries Confirmed**: NEED-001 through NEED-013; CON-001 through CON-006; DEC-001 through DEC-005; OUT-001 through OUT-004.
- **Questions Resolved**: OPEN-001 by NEED-009; OPEN-002 by NEED-013; OPEN-003 by NEED-010.

### Session 2026-10-01 22:42:17 +0800

- **Summary Presented**: Specification review reported that a confirmed merge creates the generalized record and removes every superseded member record when the batch is applied, so merging removes files exactly as discarding does, while the confirmed second-confirmation rule in NEED-006 named only discarding a record and discarding the whole draft. The report stated that extending the rule to merging would be a new product requirement that could not be applied automatically, and raised it together with one other advisory: that the review-progress figure be derived from the same accounting the staged-change ledger uses, so a cluster staged as one merge cannot make the progress count disagree with the ledger.
- **User Confirmation**: "把二次确认扩到合并。风险提示按照你建议的实施。" The first sentence confirms the new requirement recorded as NEED-014. The second directs that the advisories be implemented as recommended; the progress-accounting advisory is a refinement of NEED-002 and NEED-005 rather than a new product requirement, and is recorded in `spec.md` at the progress requirement rather than as a new entry here.
- **Entries Confirmed**: NEED-014.
- **Entries Cross-Referenced**: NEED-006 gained an "Extended By" pointer to NEED-014; its confirmed statement is unchanged.

### Session 2026-10-02 00:02:01 +0800

- **Summary Presented**: The implemented interface was shown to the user, who rejected its visual direction and supplied the design system their other project already uses as the reference to match. A first pass took only that system's colour values and was rejected again as too hard-edged; the assistant identified the cause as having left the previous geometry, elevation and spacing in place, which that system's own guidance forbids, and adopted its radii, soft elevation and 1.10× spacing scale as well. Four deviations were stated and are recorded in DEC-006: the reference's two typefaces cannot be loaded because CON-001 forbids a network request, its icon set cannot be used because CON-002 forbids vector graphics, field controls take its medium radius rather than its pill radius, and one brick red is added because the palette carries no destructive hue. The preview-gate signal was remapped onto the reference's own two accents, which removes the need for the dedicated fifth hue the superseded DEC-003 required.
- **User Confirmation**: "配色和样式跟我的预期不太符合，参考 ... 这个其他项目的设计稿使用的配色" selected the reference. "还是不太对，为什么设计稿的配色和元素样式看起来很柔和，你模仿过来的元素就很生硬呢？" rejected the colour-only pass. "柔和度对了。" confirmed the result after the geometry, elevation and spacing were adopted. The user did not separately rule on the gate-signal mapping; DEC-007 records that it rests on DEC-006.
- **Entries Confirmed**: DEC-006, DEC-007.
- **Entries Superseded**: DEC-002 by DEC-006; DEC-003 by DEC-007. Both are retained in full under Superseded Entries with their original decisions, their alternatives, and the reason each was replaced.
- **Entries Unchanged**: NEED-010 carries the token-system requirement independently of any palette and is unaffected; its statement names no hue. CON-001 and CON-002 are what make two of DEC-006's deviations binding rather than optional.
