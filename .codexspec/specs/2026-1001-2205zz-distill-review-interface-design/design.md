# Design Document: Distill Review Interface Design

**Related Spec**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/spec.md`<br>
**Confirmed Requirements**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/requirements.md`<br>
**Created**: 2026-10-01<br>
**Status**: Draft

## Context

The manual distill review workspace is served by a loopback HTTP server from three static assets — `src/codexspec/distill_review/assets/index.html`, `styles.css`, and `app.js` — plus thirteen per-language catalogs under `assets/i18n/`. The server's `do_GET` allowlist admits exactly those paths and `/i18n/<lang>.json`; everything else returns `not_found`. Its response headers set `Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; …`, and `tests/test_distill_review_interfaces.py::test_frontend_is_offline_and_uses_fragment_bearer` asserts that the three assets concatenated contain neither `http://` nor `https://`.

The review state machine lives in `distill_review/domain.py` (`ReviewService`) and is carrier-independent: the HTTP server and the terminal fallback both drive it. The server holds one piece of state the domain does not: `ReviewHTTPServer.previewed_operations`, a set of keys built as `f"{draft.revision}:{json.dumps(operation, sort_keys=True)}"`. Staging a revision, a vetting, or a merge is refused with `preview_required` unless that exact key is present, and the key is discarded once its operation is staged or when a refresh clears the set.

This design replaces the workspace's presentation and interaction layer. It keeps every review safety property as delivered, adds two additive read-only projections to the backend where the page provably cannot determine what it must display, and introduces no new served path, asset file, dependency, or persisted state.

## Architecture & Components

### Page shell — `assets/index.html`

- **Responsibility**: The static skeleton of the three regions and the two chrome bars. Carries the element identities the controller and the test suite depend on: `#page-title`, `#records`, `#editor`, `#summary-title`, `#summary`, `#status`, `#refresh`, `#apply`, `#cancel`, `#discard`. `#status` keeps `role="status"`, `aria-live="polite"`, `aria-atomic="true"`, and `tabindex="-1"`. Adds a header slot for the project name, a `<progress>` element for the review progress, a labeled checkbox for the automatic advance, and a `hidden` region for the keyboard hint. `#summary` changes from `<pre>` to a container element because the ledger is now structured content rather than serialized text.
- **Interface**: Markup only. No inline `<style>`, no `style` attribute, no vector graphics.
- **Covers**: REQ-001, REQ-004, REQ-018, REQ-020, REQ-022, NFR-006

### Design token layer — `assets/styles.css` `:root` and its dark-scheme override

- **Responsibility**: Declares every colour, type step, spacing step, and radius as a custom property on `:root`, and redeclares the colour set inside `@media (prefers-color-scheme: dark)`. Nothing else in the stylesheet uses a literal colour.
- **Interface**: The token table under **API / Interface Contracts**.
- **Covers**: NFR-001, NFR-002

### Layout and responsive grid — `assets/styles.css`

- **Responsibility**: The three-region grid and its two degradations; the working surface's action bar fixed to the bottom of its own region; the global footer as the only viewport-fixed bar. All directional spacing, alignment, and borders expressed with logical properties (`padding-inline`, `margin-block`, `border-inline-start`, `text-align: start`).
- **Interface**: At 1240px and wider, three columns — `minmax(220px, 260px)`, `minmax(0, 1fr)`, `minmax(240px, 300px)`. From 880px to 1239px, two columns with the ledger below the working surface as a horizontal strip. Below 880px, one column with the queue above the working surface. No horizontal page scrolling at any width down to the narrowest supported one.
- **Covers**: REQ-001, NFR-003, NFR-004

### Queue renderer

- **Responsibility**: Renders `#records` as four labeled groups — awaiting review, staged, deferred, consolidation clusters — each with a count, from the staged draft and the record set. Each entry is a button carrying a decorative state mark, the record title, and a meta line with the category and the record identifier. The entry open in the working surface carries `aria-current="true"` and a selected appearance.
- **Interface**: Reads the session snapshot's `records` and `clusters` for the item set, and `draft.decisions` and `draft.deferred` for each entry's decision state — a decision carries its `action`, which is what distinguishes a discarded record from a record that a merge will replace. Group counts and the progress figure come from the backend `summary` instead; see the single-accounting decision below. Emits a selection change.
- **Covers**: REQ-002, REQ-021, NFR-001

### Working surface renderer — record form and cluster form

- **Responsibility**: Renders the selected item: its title at the largest type step, a compact definition list of identifier, category, current status, provenance, and relative file path, then one adaptive control per editable field, then the final-content panel, then the action bar. The cluster form additionally renders its member records above the proposal fields. Re-renders completely on every selection change; no form state is cached across selections.
- **Interface**: For a record, `record.editable_fields`, `record.fields`, `record.title`, and any Agent proposal in `state.proposals[record.id]`, overlaid with the staged decision in `state.draft.decisions[record.id]`. For a cluster, the consolidation proposal's `fields` overlaid with `staged.field_changes`. Keeps `renderRecordContext` and `renderConsolidation` as the entry points those names denote today.
- **Covers**: REQ-005, REQ-014, REQ-023, NFR-001

### Final-content panel and preview gate indicator

- **Responsibility**: Presents the exact Markdown that will be written, under its own heading, in the monospaced face, soft-wrapped, scrollable within a bounded height, on the sunken surface, its heading tinted from the sage second voice when the preview matches and from the terracotta accent when the edits have moved past it. Beside the heading it shows the gate state in words, and beside the record's decision controls it shows whether the stored evidence already satisfies the verification requirement.
- **Interface**: Gate state is one of three values computed as described under **Sequence & Data Flow**. Verification state reads `record.outcome_verified`, which the session snapshot already exposes through `RecordDocument.to_public_dict`; no backend change is needed for it.
- **Covers**: REQ-005, REQ-006, REQ-007, REQ-008

### Decision action bar and destructive confirmation

- **Responsibility**: Groups the routine decisions and separates the file-removing ones. On a record: keep as candidate, vet, and defer are grouped; discard is separated in position, weight, and colour. On a cluster: keeping the records separate is routine; merging as candidate and merging as vetted are file-removing and carry the same separation. While the gate is unsatisfied, the primary control is "preview final content". Every file-removing action, and discarding the draft, passes through a confirmation that states its consequence before the action proceeds.
- **Interface**: Confirmation messages are catalog strings interpolated with the affected count — the number of member records a merge replaces, or the number of staged decisions a draft discard would drop. Ordering is fixed: the preview gate is evaluated **before** the confirmation, so a destructive confirmation is never raised for an action the backend would refuse. Raising it first would state a consequence that then does not occur, which is the kind of surprise this surface exists to remove; while the gate is unsatisfied the control routes to previewing instead, as the gate indicator already advertises. Discarding the draft is not gated by a preview and goes straight to its confirmation.
- **Covers**: REQ-006, REQ-012, REQ-013, REQ-023

### Staged-change ledger and progress

- **Responsibility**: Renders `#summary` as labeled groups with a count and the affected record identifiers, each identifier selecting its record or cluster. Omits empty groups except the undecided group. Feeds the header's `<progress>` and its numeric reading from the same accounting, so the two can never disagree.
- **Interface**: Reads the backend `summary` object returned by `/api/session`, `/api/draft`, and `/api/refresh` — the seven groups `added`, `replaced`, `promoted`, `removed`, `merged`, `deferred`, `undecided`. Decided count is total in-scope records minus `undecided`. Each listed identifier resolves to a selection target: an identifier in `replaced`, `promoted`, `removed`, `deferred`, or `undecided` is a record in the item set and selects that record; an entry in `merged` is a cluster name and selects that cluster. An identifier in `added` is the record a merge will create and therefore does **not** exist in the item set — it resolves to the cluster whose staged merge declares it, found by matching the `record_id` of the `cluster:`-keyed decisions, so the entry stays navigable rather than becoming a control that does nothing.
- **Covers**: REQ-004, REQ-010, REQ-011

### Adaptive field control

- **Responsibility**: One control type for every editable structured field, with height following content and no line break possible. Preserves the label-to-control association and the field-error channel.
- **Interface**: A `<textarea rows="1">` styled with `field-sizing: content`; where that property is unsupported, a fallback sets the `rows` attribute from the measured scroll height. A `beforeinput` handler cancels `insertLineBreak`, and an `input` handler collapses any carriage return or line feed arriving by paste into a single space. `appendField`, `clearFormErrors`, and `reportFormError` keep their current contracts, including `label.htmlFor`, `aria-invalid`, `aria-describedby`, and the focus move.
- **Covers**: REQ-014, REQ-015, REQ-022

### Keyboard controller

- **Responsibility**: Binds the key map, renders the discoverable hint, and enforces the safety rules: inert while focus is inside an editable control or while a modifier is held, and no key bound to batch application, cancellation, or draft discarding.
- **Interface**: The key map table under **API / Interface Contracts**, declared once as data and used both to dispatch and to render the hint.
- **Covers**: REQ-016, REQ-017

### Status and feedback channel

- **Responsibility**: Two destinations instead of one. Field-level validation failures stay on the field. Results of a decision control — staged, refused, gate explanation — render next to that control. The header status region keeps its live announcements for session-level outcomes and fatal errors, with multi-line error text preserved.
- **Interface**: `setStatus`, `setErrorStatus`, and `formatError` keep their current contracts, including the rule code, detail, record list, and failure list that `formatError` renders.
- **Covers**: REQ-009, REQ-019, REQ-022, NFR-009

### Localization layer

- **Responsibility**: Loads the catalog for the configured interaction language with the existing English fallback, resolves every user-visible string, and interpolates counts.
- **Interface**: `t(key, fallback)` unchanged; a new `format(key, values)` replacing `{name}` placeholders. Twenty new keys, listed under **API / Interface Contracts**, added to all thirteen catalogs. The `fieldLabels` key set is unchanged.
- **Covers**: NFR-008, NFR-009

### Session snapshot extension — `distill_review/domain.py`

- **Responsibility**: `ReviewService.snapshot()` gains one read-only field, `project_name`, carrying `project_root.name`. It is a carrier-independent fact about the session, so it belongs in the domain snapshot rather than in the HTTP layer.
- **Interface**: `"project_name": str`. Additive; no existing field changes; the draft schema and the request schema version are untouched.
- **Covers**: REQ-020, NFR-007

### Preview gate authority — `distill_review/server.py`

- **Responsibility**: Projects the server's existing `previewed_operations` set into the responses the page already receives, so the page displays the gate rather than inferring it, and establishes the invariant that makes the projection trustworthy: **the set only ever holds keys for the current draft revision.** The matching logic that enforces the gate is unchanged.
- **Interface**: `/api/preview` responses gain `gate_token`, the SHA-256 hex digest of the operation key just stored. `/api/session`, `/api/draft`, and `/api/refresh` responses gain `gate_tokens`, the sorted digests of every key the set holds. The set is cleared whenever the draft revision advances — that is, after a staged decision, in place of discarding only the key just consumed, and on a refresh, which already clears it. Clearing is exact rather than conservative: a key is stored under the revision current at preview time, and the enforcement lookup composes the revision current at staging time, so once the revision advances no stored key is reachable and keeping it would only misreport the gate. This state lives on the HTTP server object, so the projection is applied in the request handler and not in the carrier-independent domain.
- **Covers**: REQ-007, NFR-007

## Key Design Decisions

### Decision 1: Project the preview gate from server state as opaque tokens

- **Context**: REQ-007 requires the displayed gate state to agree with what the backend will accept. The backend's key embeds the draft revision, and the page's current check compares only the operation payload. That difference is reachable: open a cluster, preview its merge at revision 3, activate "keep records separate" — which stages a `keep_separate` operation, advancing the revision to 4 without re-rendering the open form or clearing its recorded preview — then activate "merge as candidate". The page reports the preview as matching while the stored key is `3:…` and the server refuses with `preview_required`. That is exactly the false-ready state REQ-007 forbids.
- **Decision**: Keep `previewed_operations` as the sole enforcement authority, add a read-only projection of it, and clear it whenever the draft revision advances so the projection can only ever describe keys the backend would actually accept. `/api/preview` returns the digest of the key it stored; the session, draft, and refresh responses return the digests the set holds. The page shows the gate as satisfied only when its recorded digest is still present **and** the form is unchanged since that preview. "Changed since preview" stays a page-side comparison because the page can determine it; "will the backend still accept this" comes from the backend because the page cannot.
- **Alternatives**: Project the set without clearing it, so a key stored at an earlier revision stays listed — rejected because that is the defect this decision exists to remove: the key is unreachable but still present, so the page would read its own digest as valid and report a gate the backend refuses. Scope the projection with a revision filter while leaving the stale keys in the set — equivalent in observable behavior, rejected only because clearing is one statement instead of a filter at every projection site and additionally bounds the set's growth. Remove the revision from the server's key, which would let the page decide alone — rejected because it widens what the gate accepts and NFR-007 forbids weakening a safety invariant. Reproduce the server's key in the page by sorting object keys and matching Python's separators — rejected as a serialization contract that would break silently on any formatting difference. Re-preview automatically before every stage — rejected because that is today's behavior and REQ-006 requires the state to be visible before the attempt, not discovered through a bounced action.
- **Trade-offs**: Two additive response fields and a hash computation per preview. Clearing on every revision advance means a reviewer who previewed one item, then decided a different item, must preview again — which is the behavior the backend already enforces and the delivered page already triggers, now reported in advance instead of discovered through a refusal. The change is strictly stricter than today's single-key discard and therefore weakens no invariant. The digest is opaque, derived from an operation the session owner authored, and served only behind the existing per-session bearer token.
- **Covers**: REQ-006, REQ-007, NFR-007

### Decision 2: No dynamic inline styles — every dynamic visual is an attribute or a native element

- **Context**: The response sets `style-src 'self'` with no `unsafe-inline`, so a `style` attribute written into the markup is refused; whether a given browser also refuses a particular CSSOM write is a detail this design should not depend on. Yet progress, field height, selection, visibility, and gate state all change at runtime.
- **Decision**: Express every dynamic visual through something that is not a style: the review progress through a native `<progress value max>`; field height through `field-sizing: content` in the stylesheet with the `rows` attribute as the fallback; selection through `aria-current` and a class; visibility through the `hidden` attribute; gate and decision state through class names resolved against the token layer. The automatic-advance control is a native checkbox with a label, and the keyboard hint is toggled with `hidden`.
- **Alternatives**: Write dynamic values with `element.style.setProperty`, which most engines permit under this policy — rejected because it makes the page's correctness depend on a CSP nuance for no benefit. Add `'unsafe-inline'` to the policy — rejected outright; it weakens a delivered security property for presentation.
- **Trade-offs**: A native `<progress>` is less freely styleable than a custom bar. In exchange it is accessible without extra attributes, needs no dynamic style, and cannot drift from its numeric reading.
- **Covers**: REQ-004, REQ-014, REQ-021, NFR-006

### Decision 3: The platform confirmation dialog carries the second confirmation

- **Context**: REQ-013 requires an explicit second confirmation, stating the consequence, for discarding a record, staging a merge, and discarding the draft. The purpose is preventing an accidental activation.
- **Decision**: Use the browser's own confirmation dialog, with the consequence as its message, interpolated with the affected count. No new widget, no focus-trap implementation, and no additional strings beyond the three messages.
- **Alternatives**: An inline two-step control where the destructive button becomes confirm-or-cancel — rejected because a fast double activation confirms it, which defeats the requirement's purpose. A custom in-page modal — rejected as the largest addition for the smallest gain: it would need its own focus management, escape handling, and two more strings, all to restate what the platform dialog already does correctly.
- **Trade-offs**: The dialog is not styleable, so it sits outside the visual system. If a browser suppresses repeated dialogs, the call returns false and the destructive action does not proceed, which fails closed and is the safe direction.
- **Covers**: REQ-013, REQ-023

### Decision 4: State marks are decorative; state is always carried in text

- **Context**: NFR-006 rules out vector graphics, and a queue entry must still show its decision state at a glance. Geometric characters render inconsistently across platforms and fonts, and a mark alone would not reach assistive technology.
- **Decision**: Each queue entry carries a text character in the state's colour, marked `aria-hidden="true"`, inside a fixed-width slot. The state itself is always also present as text — in the group heading the entry sits under, and in the entry's meta line. Characters are chosen from the geometric ranges that default to text presentation rather than emoji.
- **Alternatives**: Marks drawn purely with stylesheet shapes — viable and free of font risk, but more rules for no legibility gain once the mark is decorative. Marks as the sole state carrier — rejected: it fails REQ-021 and breaks when a glyph is missing.
- **Trade-offs**: A missing glyph degrades to a blank slot, and nothing is lost because the state is already in text.
- **Covers**: REQ-002, REQ-021, NFR-001, NFR-006

### Decision 5: Progress and the ledger are computed from one accounting source

- **Context**: REQ-004 requires the progress figure and REQ-010 the ledger. A cluster staged as a single merge covers several member records, so counting queue entries and counting the backend's groups give different answers.
- **Decision**: The backend `summary` object is the only accounting for every number the interface shows. The ledger renders its seven groups directly, and the decided count is the in-scope record total minus its `undecided` group. No count is computed from the rendered list. Per-entry decision state is a separate question and comes from `draft.decisions` and `draft.deferred`, because `summary` deliberately cannot answer it: its `removed` group holds both discarded records and the member records a merge replaces, so it cannot tell the queue which mark and which colour an entry takes. Both sources arrive in the same response and are projections of the same draft, so counts and per-entry marks cannot disagree.
- **Alternatives**: Count queue entries, which is simpler to write — rejected because it produces a progress figure that disagrees with the ledger on any cluster, which is the inconsistency this decision exists to prevent. Derive per-entry state from `summary` as well, for a single source — rejected on the verified shape of `summary()`: a discarded record and a merge's member records share its `removed` group, so the queue would mark a record a merge will replace as discarded.
- **Trade-offs**: Every render depends on a fresh `summary`, so each mutating response must carry one. All three mutating endpoints already return it. The queue reads two parts of the same response rather than one, which is the cost of showing a distinction the accounting groups intentionally collapse.
- **Covers**: REQ-004, REQ-010, REQ-002

### Decision 6: One state-change entry point drives one render pass

- **Context**: REQ-003 requires the queue and the ledger to match the staged draft as soon as a decision is staged or withdrawn. Today each mutation path re-renders only the summary, which is how the displayed state drifts.
- **Decision**: Every mutation applies its response to the page state and then runs one render pass over the queue, the ledger, the progress, and the gate indicator. The working surface is re-rendered only when the selection changes, so a reviewer's in-progress edits are never discarded by someone else's accounting update.
- **Alternatives**: Re-render everything including the open form — rejected because it would destroy unsaved edits. Re-render selectively at each call site — rejected because that is the current arrangement and the source of the drift.
- **Trade-offs**: The open form can briefly show edits for an item whose queue entry already reads as staged. That is correct: the staged decision is what the draft holds, and the gate indicator reports the difference.
- **Covers**: REQ-003, REQ-018

### Decision 7: The keyboard map is declared once as data, with its conflict recorded

- **Context**: REQ-016 requires reusing the text review mode's letters where they exist, and OUT-002 forbids changing that mode. The text mode prompts with `[v]et [e]dit [d]rop [s]kip [q]uit` for a record and `[m]erge [k]eep separate [q]uit` for a cluster.
- **Decision**: Declare the map once as a table that both dispatches keys and renders the discoverable hint. Reuse `v`, `e`, `d`, `s`, and `m`. Do not reuse `k` for keeping records separate, because `k` is the upward movement key in a list-driven browser interface; use `x` instead and record the reason here. Do not bind `q`, because the text mode's `q` ends the session and REQ-017 forbids a single key doing that.
- **Alternatives**: Reuse `k` and choose another movement key — rejected because `j`/`k` movement is the stronger convention in a queue and movement is used far more often than one cluster decision. Bind `q` to cancel for symmetry with the text mode — rejected: REQ-017 prohibits it.
- **Trade-offs**: Two letters differ between the carriers. Both are visible in the page's hint, and the text mode is unchanged as OUT-002 requires.
- **Covers**: REQ-016, REQ-017

### Decision 8: Nothing is added to the persisted draft

- **Context**: The gate projection and the new display state could plausibly be stored with the draft so they survive a reload.
- **Decision**: Keep all of it ephemeral — server-side for the previewed-operation set, page-side for the recorded digest and the pre-edit snapshot. The draft file, its schema version, and the session store are untouched.
- **Alternatives**: Persist the gate state in the draft — rejected on a verified repository fact: `ReviewDraft.from_dict` validates each decision with exact key-set equality (`set(decision) == required`), so any added field makes a saved draft unloadable, and the recovery path that REQ-023's workflow depends on would reject drafts written by a newer build.
- **Trade-offs**: A page reload returns every item's gate to "not previewed". That is the conservative direction and matches the server, which also holds no previewed key for a revision the reviewer has not previewed in this page session.
- **Covers**: REQ-007, NFR-007

## API / Interface Contracts

### Backend response additions

All additive; no field changes meaning, no request shape changes, and the request `schema_version` stays `1` because the page and the server ship together as one artifact.

| Endpoint | Added field | Type | Meaning | Covers |
|---|---|---|---|---|
| `GET /api/session` | `project_name` | string | Name of the project directory whose profile this session will modify | REQ-020 |
| `GET /api/session` | `gate_tokens` | array of string | Digests of the previewed-operation keys the server holds, all of them for the current draft revision | REQ-007 |
| `POST /api/preview` | `gate_token` | string | Digest of the key stored for the operation just previewed | REQ-007 |
| `POST /api/draft` | `gate_tokens` | array of string | As above; the revision has advanced, so the array is empty | REQ-007 |
| `POST /api/refresh` | `project_name`, `gate_tokens` | string, array of string | As above; the refresh clears the set, so the array is empty | REQ-007, REQ-020 |

### Design tokens

Light-scheme and dark-scheme values for each token, taken from the design system DEC-006 adopts. Every text and mark colour meets a contrast ratio of at least 4.5 to 1 against the surface it is used on, and may be tuned at implementation only while that holds.

| Token | Light | Dark | Use |
|---|---|---|---|
| `--paper` | `#f5ead8` | `#201e1d` | Page background |
| `--surface` | `#ebddc5` | `#2e2b25` | Region panels |
| `--sunken` | `#f9f4ed` | `#474238` | Final-content panel, field controls |
| `--ink` | `#201e1d` | `#f9f4ed` | Primary text |
| `--muted` | `#645c50` | `#c0b6a5` | Labels, metadata |
| `--stamp` | `#c67139` | `#f6a06b` | Primary accent: marks, edges, progress fill |
| `--stamp-ink` | `#8c491a` | `#ffc6a5` | The accent at label size, where the base step is too light to reach 4.5 to 1 |
| `--stamp-fill` | `#8c491a` | `#f6a06b` | Filled primary control |
| `--stamp-fill-hover` | `#b2622d` | `#ffc6a5` | Filled primary control, hovered and pressed |
| `--stamp-on-fill` | `#f9f4ed` | `#2e2b25` | Label on a filled primary control |
| `--stamp-soft` | `#fff2eb` | `#643312` | Selected queue entry |
| `--pass` | `#56633f` | `#aebf92` | Sage second voice: vetted state, and a preview that matches |
| `--hold` | `#645c50` | `#a19786` | Deferred state |
| `--drop` | `#a3301f` | `#f09a8c` | Discarded state, errors — the one value added to the reference palette |

Dividers and tints are derived rather than fixed, so they follow the ground in either scheme: `--divider` is the ink at 16 per cent, `--tint-soft` and `--tint-firm` are the ink at 6 and 12 per cent, and `--tint-accent` is the accent at 12 per cent. Elevation is a three-step set of soft ink-tinted shadows on the light scheme and deeper ambient shadows on the dark one; region panels carry no border and are separated by elevation instead.

Spacing follows the reference's 1.10× scale — `4.4px` / `8.8px` / `13.2px` / `17.6px` / `26.4px` / `35.2px` — with one `2px` step added for a state rule the scale does not carry. Radii differ by hierarchy: `32px` for region panels, `28px` for the final-content panel and member cards, `16px` for field controls and queue entries, `8px` available below that, and a pill radius for buttons and chips. Type steps `0.8125rem` / `0.9375rem` / `1.125rem` / `1.5rem`; the record title takes the largest step and the page heading takes the body step at a heavier weight, so chrome does not outrank content.

The reference pairs a rounded display face with a soft geometric sans, both loaded from a font service. CON-001 forbids a network request, so both fall back to the platform stack — sans `system-ui, -apple-system, "Segoe UI Variable", "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans Arabic", sans-serif`, monospace `ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace` — and the display voice is carried by weight and size. This is the one deviation in DEC-006 that cannot be closed.

### New catalog keys

Twenty keys, added to all thirteen catalogs (`ar`, `de`, `en`, `es`, `fr`, `hi`, `it`, `ja`, `ko`, `pt`, `ru`, `zh-CN`, `zh-TW`) with translated text. Braces mark interpolation handled by `format`.

| Key | Purpose | Covers |
|---|---|---|
| `queue.pending` | Queue group heading: awaiting review | REQ-002 |
| `queue.staged` | Queue group heading: staged | REQ-002 |
| `queue.deferred` | Queue group heading: deferred | REQ-002 |
| `queue.clusters` | Queue group heading: consolidation clusters | REQ-002 |
| `queue.empty` | Nothing is awaiting review | REQ-002 |
| `progress` | `{done}` of `{total}` decided | REQ-004 |
| `finalText` | Final-content panel heading | REQ-005 |
| `gate.none` | Gate state: not previewed | REQ-006 |
| `gate.fresh` | Gate state: preview matches the current edits | REQ-006 |
| `gate.stale` | Gate state: edits changed after the preview | REQ-006 |
| `previewFinal` | Primary action label while the gate is unsatisfied | REQ-006 |
| `verification.satisfied` | The stored evidence already establishes verification | REQ-008 |
| `verification.required` | Vetting this record requires verification evidence | REQ-008 |
| `members` | Cluster member records heading | REQ-023 |
| `allDecided` | Nothing is left undecided; apply when ready | REQ-019 |
| `confirmDiscardRecord` | Applying will delete this record file; continue | REQ-013 |
| `confirmMerge` | Applying will delete the `{count}` member records this merge replaces; continue | REQ-013 |
| `confirmDiscardDraft` | `{count}` staged decisions will be dropped; continue | REQ-013 |
| `shortcuts` | The discoverable key hint | REQ-016 |
| `autoAdvance` | Label for the automatic-advance switch | REQ-018 |

### Keyboard map

Declared once as data; dispatch and the rendered hint read the same table. Every binding is inert while focus is inside an editable control or while a modifier key is held.

| Key | Surface | Action | Text-mode letter |
|---|---|---|---|
| `j`, `ArrowDown` | any | Next queue entry | — |
| `k`, `ArrowUp` | any | Previous queue entry | — |
| `e` | record, cluster | Focus the first editable field | `e` (edit) |
| `p` | record, cluster | Preview the final content | — |
| `v` | record | Vet | `v` (vet) |
| `r` | record | Keep as candidate | — |
| `d` | record | Discard, through the confirmation | `d` (drop) |
| `s` | record | Defer | `s` (skip) |
| `m` | cluster | Merge as candidate, through the confirmation | `m` (merge) |
| `x` | cluster | Keep the records separate | `k` in the text mode, remapped — see Decision 7 |
| `?` | any | Show or hide the key hint | — |
| `Escape` | inside a field | Return focus to the current queue entry | — |

No key is bound to batch application, session cancellation, or draft discarding.

## Sequence & Data Flow

The preview gate's lifecycle is the one flow where page state, server state, and the draft revision interact, so it is stated in full.

1. The page loads and requests the session. The response carries the records, the clusters, the draft, the summary, `project_name`, and `gate_tokens`, which is empty. Every item's gate reads "not previewed".
2. The reviewer edits fields. The form's operation changes; the gate still reads "not previewed".
3. The reviewer previews. The server renders the exact final bytes, stores the operation key for the current revision, and returns the Markdown plus `gate_token`. The page records that digest and a snapshot of the operation it previewed. The gate reads "preview matches the current edits".
4. The reviewer edits again. The current operation no longer equals the recorded snapshot, so the gate reads "edits changed after the preview" — computed in the page, which can determine it.
5. The reviewer stages the decision. The server finds the key for the current revision, stages, and — because the revision has now advanced and no stored key is reachable any more — clears the set, returning the draft, a fresh summary, and an empty `gate_tokens`. The page applies the response, drops every recorded digest, runs one render pass, and advances to the next undecided item when the automatic advance is on.
6. Any other mutation — deferring a record, keeping a cluster separate, staging a different item — also advances the draft revision and therefore also clears the set. The digest the page recorded for the item still open is absent from the new `gate_tokens`, so its gate falls back to "not previewed" *before* the reviewer can attempt a decision. This is the case the delivered page reports incorrectly: it keeps its own record of the preview, the server's key is unreachable under the new revision, and the reviewer is refused after being told the decision was ready.
7. A conflict refresh clears the set as it already does. The response's `gate_tokens` is empty and every gate returns to "not previewed".

## Cross-Cutting Design

**Accessibility.** The status region keeps `role="status"`, `aria-live="polite"`, `aria-atomic="true"`, and `tabindex="-1"`. Field errors keep the delivered behavior: `aria-invalid="true"`, `aria-describedby` pointing at the message, and focus moved to the control. The selected queue entry carries `aria-current="true"`; the state mark beside it is `aria-hidden="true"` and never the sole carrier of meaning. Focus indication comes from one `:focus-visible` rule using an accent-derived token, so it is visible in both schemes. Progress is a native `<progress>`; the automatic-advance control is a labeled checkbox; the key hint is toggled with `hidden`. Keyboard bindings never capture a key while focus is inside a field, and `Escape` returns focus to the queue.

**Internationalization and direction.** Every user-visible string resolves through the catalog layer with the existing English fallback; counts interpolate through `format`. The stylesheet uses only logical properties, so the right-to-left direction the page already sets for Arabic mirrors the layout without a second rule set. Logical properties alone are not sufficient, because they govern box geometry and not the bidirectional reordering of text: a record identifier, a file path and the bytes of a record are literal text whose reading order is left-to-right whatever the interface language, and left to the paragraph direction a right-to-left interface renders each Markdown line with its leading marker at the far edge and truncates an identifier from its start. Those elements therefore set an explicit left-to-right direction, while a record title and a field value — user content in an unknown language — resolve their direction from the content itself. The sans stack carries Simplified and Traditional Chinese, Japanese, and Arabic fallbacks ahead of the generic family.

**Security and delivery.** No served path is added, so the allowlist and its refusal of every other path are unchanged. No `<style>` element, no `style` attribute, no vector graphics, no external reference of any kind, which keeps the policy satisfied and keeps the three assets free of any absolute URL scheme. The gate digest is derived from an operation the session owner authored and travels only over the authenticated loopback channel.

**Verification.** The existing front-end contract tests remain the gate for the offline property, the absent URL schemes, the accessibility attributes, and catalog key parity. The new behavior adds assertions in the same file: the queue's `aria-current`, the three gate states, the confirmation path for each file-removing action, and the two response projections.

## Risks & Trade-offs

| Risk | Impact | Mitigation |
|---|---|---|
| `field-sizing: content` is not available in every browser a reviewer may use | Field heights would not follow content, re-introducing the inconsistency REQ-014 removes | Stylesheet declares it as the primary mechanism; the controller detects support and falls back to setting the `rows` attribute from the measured scroll height — both avoid dynamic inline styles |
| Geometric state characters render differently across platforms and fonts | A mark could be blank or render with emoji presentation | Marks are decorative and `aria-hidden`; the state is always also in text, so a missing glyph loses nothing (Decision 4) |
| A browser suppresses repeated confirmation dialogs | The second confirmation would not be shown | Suppression makes the call return false, so the destructive action does not proceed — the failure direction is safe (Decision 3) |
| Twenty new strings across thirteen catalogs is bulk translation work | A missing or untranslated key could ship | The existing catalog-parity assertion fails on any key-set difference, and the field-label key set is asserted separately; NFR-008 forbids an English-only string |
| Two bars at the bottom of the viewport could read as one strip | A reviewer could mistake a record decision for a batch action | The global footer is the only viewport-fixed bar; the action bar is fixed within the working-surface region, carries that region's surface colour, and a full-width rule separates the two |
| The working surface is not re-rendered on another item's mutation | An open form could show edits for an item whose queue entry already reads as staged | Intended and reported: the gate indicator states the difference, and in-progress edits are never destroyed by an unrelated update (Decision 6) |

### Design Assumptions

- The narrowest supported viewport width used to verify the layout is 420 logical pixels, carried from the specification's stated assumption. It is not a confirmed requirement; a different figure changes no requirement.
- The page and the server ship together in one artifact, so additive response fields need no request schema version change. If the two were ever versioned independently, the projections would need a negotiated version.
- `CSS.supports` is available for the `field-sizing` capability check; if it were absent the fallback path runs, which is the safe default.

## Requirements Coverage

| Spec Requirement | Design Coverage |
|---|---|
| REQ-001 | Page shell; Layout and responsive grid |
| REQ-002 | Queue renderer; Decision 4; catalog keys `queue.*` |
| REQ-003 | Decision 6 (one state-change entry point, one render pass) |
| REQ-004 | Staged-change ledger and progress; Decision 2 (native progress element); Decision 5 (single accounting) |
| REQ-005 | Final-content panel; Working surface renderer |
| REQ-006 | Final-content panel and gate indicator; Decision 1; catalog keys `gate.*`, `previewFinal` |
| REQ-007 | Preview gate authority; Decision 1; Sequence & Data Flow |
| REQ-008 | Final-content panel and gate indicator, reading the existing `outcome_verified` field; catalog keys `verification.*` |
| REQ-009 | Status and feedback channel |
| REQ-010 | Staged-change ledger and progress; Decision 5 |
| REQ-011 | Staged-change ledger and progress |
| REQ-012 | Decision action bar and destructive confirmation |
| REQ-013 | Decision action bar and destructive confirmation; Decision 3; catalog keys `confirm*` |
| REQ-014 | Adaptive field control; Decision 2 (`rows` fallback) |
| REQ-015 | Adaptive field control (`beforeinput` cancellation, paste normalization) |
| REQ-016 | Keyboard controller; Decision 7; catalog key `shortcuts` |
| REQ-017 | Keyboard controller; Decision 7 (no binding for terminal operations) |
| REQ-018 | Decision 6; Page shell (switch); catalog key `autoAdvance` |
| REQ-019 | Status and feedback channel; catalog key `allDecided` |
| REQ-020 | Session snapshot extension; Page shell header slot |
| REQ-021 | Queue renderer (`aria-current`); Decision 4; Cross-Cutting Design — Accessibility |
| REQ-022 | Page shell; Adaptive field control; Status and feedback channel; Cross-Cutting Design — Accessibility |
| REQ-023 | Working surface renderer (cluster form); Decision action bar; catalog key `members` |
| NFR-001 | Design token layer; token table; Decision 4 |
| NFR-002 | Design token layer (`prefers-color-scheme` override only; no in-page switch, no stored preference) |
| NFR-003 | Layout and responsive grid |
| NFR-004 | Layout and responsive grid (logical properties); Cross-Cutting Design — Internationalization and direction |
| NFR-005 | Cross-Cutting Design — Security and delivery; no component adds a served path, asset, or dependency |
| NFR-006 | Decision 2; Decision 4; Cross-Cutting Design — Security and delivery |
| NFR-007 | Decision 1; Decision 8; Session snapshot extension and Preview gate authority, both additive and read-only |
| NFR-008 | Localization layer; new catalog key table |
| NFR-009 | Localization layer; Status and feedback channel |
| NFR-010 | Cross-Cutting Design — Verification |
