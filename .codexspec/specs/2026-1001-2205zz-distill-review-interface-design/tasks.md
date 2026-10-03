# Implementation Tasks: Distill Review Interface Design

**Related Plan**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/plan.md`<br>
**Related Design**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/design.md`<br>
**Related Spec**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/spec.md`<br>
**Confirmed Requirements**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/requirements.md`<br>
**Created**: 2026-10-01<br>
**Status**: Draft

## How To Read This List

- Groups follow the plan's six phases; the plan's ordering decisions are preserved and not re-derived here.
- Every task carries `Covers: REQ-xxx; Plan: <phase>` or, where it realizes no requirement, an explicit statement of the authority that requires it.
- A task marked `[P]` can run concurrently with the other `[P]` tasks in the same position once its declared dependencies are met. Tasks that edit the same file are not marked `[P]` even when they are logically independent.
- Backend tasks are written test-first, per the plan's test-discipline decision: the enumerated scenarios become failing tests before the implementation in that same task.
- Asset, catalog, and documentation tasks are not testable in that sense and carry deterministic verification instead of scenarios, as the plan's test-discipline decision records.
- Group checkpoints are the plan's closing verification units. They gate the group and are not restated as tasks.

## Group A — Backend projections and the preview-gate invariant

Plan Phase 1. These three tasks are independently verifiable with pytest and land before any asset work, so a later regression is attributable to the phase that introduced it.

### T001 — Report the project directory name in the session snapshot

- **Status**: complete
- **Outcome**: `GET /api/session` carries the name of the project directory whose profile the session will modify, supplied by the backend rather than inferred in the page.
- **Paths**: `src/codexspec/distill_review/domain.py`, `tests/test_distill_review_interfaces.py`
- **Dependencies**: none
- **Covers**: REQ-020; Plan: Phase 1
- **Test Scenarios**:
  - **S001.1** A session opened on a fixture project reports that project directory's name.
  - **S001.2** The reported value is the directory name alone and contains no path separator, so an absolute path cannot be rendered from it.
  - **S001.3** Every field the session response carried before is still present and unchanged, because the addition must be additive.

### T002 — Project the preview-gate state into the responses the page receives

- **Status**: complete
- **Outcome**: a successful preview returns an opaque digest identifying the previewed-operation key the server stored, and the session, draft, and refresh responses report the digests the server holds, so the page can display the gate instead of inferring it.
- **Paths**: `src/codexspec/distill_review/server.py`, `tests/test_distill_review_interfaces.py`
- **Dependencies**: none
- **Covers**: REQ-007; Plan: Phase 1
- **Test Scenarios**:
  - **S002.1** A successful preview response carries a gate digest.
  - **S002.2** A session opened before any preview reports an empty digest list.
  - **S002.3** After a preview, the digest returned by that preview appears in the digest list the next response reports.
  - **S002.4** The digest for the same operation at the same draft revision is identical on repeat, and the digest for a different operation differs, so the page's comparison cannot produce a false match.
  - **S002.5** Every field the preview, draft, and refresh responses carried before is still present and unchanged, because the addition must be additive.

### T003 — Hold the previewed-operation set to the current draft revision

- **Status**: complete
- **Outcome**: the set of previewed operations is cleared whenever the draft revision advances, so the projected digests only ever describe operations the backend would still accept, and the state where the page reports a decision as ready while the backend refuses it cannot occur.
- **Paths**: `src/codexspec/distill_review/server.py`, `tests/test_distill_review_interfaces.py`
- **Dependencies**: T002
- **Covers**: REQ-007, NFR-007; Plan: Phase 1
- **Test Scenarios**:
  - **S003.1** Previewing an operation and then staging that same operation at the same revision is accepted, so the delivered gate still passes what it passed before.
  - **S003.2** Previewing a cluster merge, then staging a keep-separate decision so the revision advances, then attempting that merge is refused by the preview rule — and the digest list reported before the attempt already contains no digest for it.
  - **S003.3** After any staged decision the reported digest list is empty.
  - **S003.4** After a conflict refresh the reported digest list is empty, preserving the behavior the refresh path already had.
  - **S003.5** When persistence fails and the draft is rolled back to its previous revision, the previously stored key stays valid, so a failed save does not invalidate a preview the reviewer already took.

**Checkpoint CP-A**: `uv run pytest tests/test_distill_review_interfaces.py tests/test_distill_review_core.py` is green, including the delivered gate test that stages only after a matching preview and the two delivered persistence-rollback tests.

## Group B — Interaction-language catalogs

Plan Phase 2.

### T004 — Add the twenty interface strings to all thirteen catalogs `[P]`

- **Status**: complete
- **Outcome**: every new user-visible string the interface needs exists in all thirteen interaction-language catalogs with identical top-level keys and translated text, and the structured field-label key set is unchanged.
- **Paths**: `src/codexspec/distill_review/assets/i18n/{ar,de,en,es,fr,hi,it,ja,ko,pt,ru,zh-CN,zh-TW}.json`
- **Dependencies**: none
- **Covers**: NFR-008, NFR-009; Plan: Phase 2
- **Why one task**: the catalog-parity assertion compares every catalog's key set against the English one, so a partial addition is a red suite rather than an incremental step. The plan's catalog decision fixes this as one change.
- **Keys**: the twenty keys enumerated in the design's catalog table, applied per file with a JSON load, modify, and dump at `indent=2` and `ensure_ascii=False` so existing formatting and non-ASCII text survive.
- **Verification**: `uv run pytest tests/test_distill_review_interfaces.py -k catalogs` is green, which asserts key-set equality across all thirteen files, non-empty document title and navigation label, and the unchanged thirteen field-label keys with values that differ from their key. Each language's new text is reviewed against the documented purpose of its key, since no rendered page exists to check it against yet.

**Checkpoint CP-B**: catalog parity green; `git diff --stat -- src/codexspec/distill_review/assets/i18n/` shows exactly thirteen changed files. The diff is scoped to that directory because this task may run concurrently with the backend and stylesheet tasks, so a whole-tree diff would legitimately show their files too.

## Group C — Visual system

Plan Phase 3. The stylesheet is replaced in place; these tasks are sequential edits to one file.

### T005 — Establish the design token layer `[P]`

- **Status**: complete
- **Outcome**: every colour, type step, spacing step, and radius is declared once as a custom property, with a complete dark-scheme override, and no literal colour appears anywhere else in the stylesheet.
- **Paths**: `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: none
- **Covers**: NFR-001, NFR-002; Plan: Phase 3
- **Verification**: the token set matches the design's token table in both schemes; the dark scheme is produced only by a `prefers-color-scheme` override, with no in-page switch and no stored preference; a search of the stylesheet finds no colour literal outside the token declarations.

### T006 — Set base typography and the two font stacks

- **Status**: complete
- **Outcome**: the base type scale is applied, the inherited rule that renders field values in semibold is removed so editable text no longer reads as a label, and the sans and monospace stacks carry their CJK and Arabic fallbacks.
- **Paths**: `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T005
- **Covers**: NFR-001, NFR-009; Plan: Phase 3
- **Verification**: a field control's computed font weight is the normal body weight rather than the label weight; the monospace stack is applied only to record identifiers, file paths, and the final-content panel.

### T007 — Implement the three-region grid and its degradations

- **Status**: complete
- **Outcome**: the layout presents three regions at wide widths and degrades to two and then one as width decreases, with the working surface's action bar fixed within its own region and the global footer as the only viewport-fixed bar, using logical properties throughout.
- **Paths**: `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T005
- **Covers**: NFR-003, NFR-004; Plan: Phase 3
- **Verification**: the breakpoints match the design's layout contract; a search of the stylesheet finds no physical directional property — no `left`, `right`, `margin-left`, `padding-right`, or `text-align: left` — so the right-to-left direction the page already sets needs no second rule set.

### T008 — Implement the focus indicator

- **Status**: complete
- **Outcome**: one focus-visible rule derived from the accent token gives every interactive control a focus indicator that is visible in both colour schemes.
- **Paths**: `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T005
- **Covers**: REQ-022; Plan: Phase 3
- **Verification**: the rule applies to every control type the page renders — button, textarea, checkbox, and the queue entry buttons — and its colour is a token with a dark-scheme value.

**Checkpoint CP-C**: the stylesheet contains no style element, no style attribute, no vector graphic, and no absolute URL scheme; the offline assertion in `tests/test_distill_review_interfaces.py` is green.

## Group D — Page shell and render pipeline

Plan Phase 4. The page and its controller are replaced together, because the render pass is what keeps the regions consistent.

### T009 — Rewrite the page shell

- **Status**: complete
- **Outcome**: the markup provides the three regions and the two chrome bars, with header slots for the project name, a native progress element, a labeled automatic-advance checkbox, a hidden key-hint region, and a ledger container, preserving every element identity and accessibility attribute the repository asserts.
- **Paths**: `src/codexspec/distill_review/assets/index.html`
- **Dependencies**: T005
- **Covers**: REQ-001, REQ-004, REQ-020, REQ-022; Plan: Phase 4
- **Verification**: the identities `page-title`, `records`, `editor`, `summary-title`, `summary`, `status`, `refresh`, `apply`, `cancel`, and `discard` are present; the status region keeps its status role, its polite live setting, its atomic setting, and its negative tab index; the file contains no style element, no style attribute, and no absolute URL scheme.

### T010 — Implement the page state store and string interpolation

- **Status**: complete
- **Outcome**: one place holds the session snapshot, the selection, and the per-item gate record, and user-visible strings resolve through the catalog layer with count interpolation.
- **Paths**: `src/codexspec/distill_review/assets/app.js`
- **Dependencies**: T004, T009
- **Covers**: NFR-008; Plan: Phase 4
- **Verification**: the catalog lookup keeps its existing English fallback; interpolation replaces the brace placeholders the design's catalog table defines; the script still loads its catalog from the relative path the repository asserts.

### T011 — Implement the single state-change entry point and its render pass

- **Status**: complete
- **Outcome**: every mutation applies its response to the page state and then runs one render pass over queue, ledger, progress, and gate indicator, leaving an open working surface untouched so in-progress edits are never discarded.
- **Paths**: `src/codexspec/distill_review/assets/app.js`
- **Dependencies**: T010
- **Covers**: REQ-003; Plan: Phase 4
- **Verification**: no mutation path re-renders only part of the derived state; the working surface re-renders on selection change only.

### T012 — Implement the queue renderer

- **Status**: complete
- **Outcome**: the queue presents four labeled groups with counts, each entry showing its decision state, category, identifier, and title, with the open entry marked as the current selection and its state mark decorative only.
- **Paths**: `src/codexspec/distill_review/assets/app.js`, `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T011
- **Covers**: REQ-002, REQ-021; Plan: Phase 4
- **Verification**: per-entry decision state is read from the staged draft's decisions and deferred list, not from the accounting groups, because a discarded record and a record a merge replaces share one accounting group; the current entry carries the current-selection attribute; the state mark is hidden from assistive technology and the state also appears as text.

### T013 — Implement the staged-change ledger and the progress reading

- **Status**: complete
- **Outcome**: the ledger presents labeled groups with counts and record identifiers, omits empty groups except the undecided one, feeds the progress element from the same accounting, and resolves every listed identifier to a selection target.
- **Paths**: `src/codexspec/distill_review/assets/app.js`, `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T011
- **Covers**: REQ-004, REQ-010, REQ-011; Plan: Phase 4
- **Verification**: all counts come from the backend accounting and none from the rendered list; an identifier in the added group resolves to the cluster whose staged merge declares it, because that record does not exist yet, so no listed identifier is a control that does nothing.

### T014 — Render the project directory name in the header

- **Status**: complete
- **Outcome**: the header names the project directory the session will write, from the backend field, without the absolute path.
- **Paths**: `src/codexspec/distill_review/assets/app.js`
- **Dependencies**: T001, T009
- **Covers**: REQ-020; Plan: Phase 4
- **Verification**: the value rendered is the backend field, not a value derived in the page.

**Checkpoint CP-D**: `uv run pytest tests/test_distill_review_interfaces.py` is green, including the offline assertion, the pinned implementation symbols, and the accessibility contract.

## Group E — Working surface

Plan Phase 5.

### T015 — Implement the adaptive field control

- **Status**: complete
- **Outcome**: every editable structured field uses one control type whose height follows its content, and no field value can be made to contain a line break.
- **Paths**: `src/codexspec/distill_review/assets/app.js`, `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T011
- **Covers**: REQ-014, REQ-015; Plan: Phase 5
- **Verification**: control height no longer depends on the stored value's length; the stylesheet sizing property is the primary mechanism and a row-attribute fallback runs where it is unsupported, with the capability check guarded so a missing interface cannot throw; a typed line break is cancelled and a pasted one is normalized to a single space.

### T016 — Implement the record working surface

- **Status**: complete
- **Outcome**: the selected record renders its title at the largest type step, a compact metadata list replacing the browser-indented definition list, and its editable fields, preserving the label association and the field-error channel.
- **Paths**: `src/codexspec/distill_review/assets/app.js`, `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T015
- **Covers**: REQ-005, REQ-022; Plan: Phase 5
- **Verification**: the metadata list keeps its definition-list semantics with a two-column presentation; each label is associated with its control; a field-level failure still marks the control invalid, links it to its message, and moves focus to it.

### T017 — Implement the final-content panel, the gate indicator, and the verification state

- **Status**: complete
- **Outcome**: the exact Markdown that will be written is presented as the working surface's dominant titled panel, the gate state is shown next to the decision controls in its three distinguishable states, and the reviewer can see before choosing to vet whether verification evidence is required.
- **Paths**: `src/codexspec/distill_review/assets/app.js`, `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T016, T002
- **Covers**: REQ-005, REQ-006, REQ-007, REQ-008; Plan: Phase 5
- **Verification**: the gate reads as satisfied only when the recorded digest is still among those the backend reports **and** the form is unchanged since that preview, so a state the backend would refuse cannot display as ready; while the gate is unsatisfied previewing is the primary control; the verification state is read from the record field the session already exposes; the panel wraps rather than scrolling horizontally and scrolls without pushing the decision controls out of reach.

### T018 — Implement the decision action bar

- **Status**: complete
- **Outcome**: routine decisions are grouped and the file-removing decision is separated from them in position, weight, and colour.
- **Paths**: `src/codexspec/distill_review/assets/app.js`, `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T017
- **Covers**: REQ-012; Plan: Phase 5
- **Verification**: keeping as candidate, vetting, and deferring are visually one group; discarding is outside it and uses the discard colour; the action bar stays reachable at the narrowest supported width.

### T019 — Implement the destructive confirmations

- **Status**: complete
- **Outcome**: discarding a record, staging a merge, and discarding the draft each require a second confirmation that states its consequence with the affected count, and the gate is evaluated before the confirmation so no confirmation is raised for an action the backend would refuse.
- **Paths**: `src/codexspec/distill_review/assets/app.js`
- **Dependencies**: T018
- **Covers**: REQ-013; Plan: Phase 5
- **Verification**: the record confirmation states that applying will delete that record file; the merge confirmation states how many member records applying will delete; the draft confirmation states how many staged decisions will be dropped; declining leaves the draft untouched; a suppressed dialog is treated as a decline, so the destructive action does not proceed.

### T020 — Implement the consolidation-cluster working surface

- **Status**: complete
- **Outcome**: a cluster presents its member records and its generalized proposal under the same panel, gate, and separation rules as a record, with merging treated as file-removing and keeping the records separate as routine.
- **Paths**: `src/codexspec/distill_review/assets/app.js`, `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T019
- **Covers**: REQ-023; Plan: Phase 5
- **Verification**: the member list and the proposal are distinguishable; the final-content panel shows the generalized record's bytes; the two merge decisions sit in the separated group and route through the confirmation; a cluster with no generalized proposal keeps its blocking notice and offers no merge control.

### T021 — Move decision feedback next to its control

- **Status**: complete
- **Outcome**: the result of a decision control — staged, refused, or a field-level validation failure — appears next to that control, while the status region keeps session-level outcomes and fatal errors with its multi-line error rendering.
- **Paths**: `src/codexspec/distill_review/assets/app.js`, `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T020
- **Covers**: REQ-009, REQ-022; Plan: Phase 5
- **Verification**: no decision outcome is reachable only through the page-top status region; the status region keeps its live announcement behavior; the rule code, detail, record list, and failure list the error formatter renders all remain visible.

**Checkpoint CP-E**: `uv run pytest tests/test_distill_review_interfaces.py` green; the page is exercised by hand once for a record and once for a cluster, confirming the gate's three states and one confirmation of each kind.

## Group F — Keyboard, end states, verification, and documentation

Plan Phase 6.

### T022 — Implement the keyboard map

- **Status**: complete
- **Outcome**: the queue and the routine decisions are operable from the keyboard with the letters the text review carrier already uses where they exist, the available keys are discoverable from the page, keys are inert inside editable controls, and no single key performs a terminal operation.
- **Paths**: `src/codexspec/distill_review/assets/app.js`
- **Dependencies**: T021
- **Covers**: REQ-016, REQ-017; Plan: Phase 6
- **Verification**: the map is declared once as data and both dispatch and the rendered hint read it; no binding exists for batch application, session cancellation, or draft discarding; a letter typed inside a field is entered as text and takes no decision; the field stays reachable and escapable by keyboard.

### T023 — Implement the automatic advance and its switch

- **Status**: complete
- **Outcome**: staging a decision moves the working surface to the next item with no decision yet, the advance is active when the page opens, and a visible switch turns it off.
- **Paths**: `src/codexspec/distill_review/assets/app.js`
- **Dependencies**: T022
- **Covers**: REQ-018; Plan: Phase 6
- **Verification**: the advance is on at open and is not restored from any stored preference; with the switch off, staging still updates the queue and the ledger but the surface stays on the record just decided.

### T024 — Implement the empty-queue and all-decided states

- **Status**: complete
- **Outcome**: an empty queue says so, and when no undecided item remains the interface says so and offers batch application as the next step rather than leaving the last reviewed record on screen.
- **Paths**: `src/codexspec/distill_review/assets/app.js`, `src/codexspec/distill_review/assets/styles.css`
- **Dependencies**: T023
- **Covers**: REQ-002, REQ-019; Plan: Phase 6
- **Verification**: both states render from catalog strings; the all-decided state appears as soon as the last item is decided, driven by the same render pass.

### T025 — Extend the front-end contract assertions

- **Status**: complete
- **Outcome**: the repository asserts the new behavior alongside the contracts it already guards, so a later change cannot silently drop it.
- **Paths**: `tests/test_distill_review_interfaces.py`
- **Dependencies**: T024
- **Covers**: NFR-010; Plan: Phase 6
- **Test Scenarios**:
  - **S025.1** The page or its controller marks the queue's current entry with the current-selection attribute.
  - **S025.2** The controller distinguishes the three gate states and resolves each from a catalog key.
  - **S025.3** A confirmation path exists for each of the three actions that remove record files or drop staged decisions.
  - **S025.4** The review progress is a native progress element rather than a construct requiring a dynamic style.
  - **S025.5** The three assets together still contain no absolute URL scheme.
  - **S025.6** The pinned implementation symbols and the accessibility attributes the repository already asserts are still present.
  - **S025.7** All thirteen catalogs still carry identical top-level keys and the unchanged thirteen field-label keys.
  - **S025.8** The server's served-path allowlist is unchanged — the page at the root and at its own name, the script, the stylesheet, and the per-language catalog route, and nothing else — so no asset path was widened for presentation.
  - **S025.9** Neither the page nor the controller writes a style attribute or assigns an inline style, so every dynamic visual is carried by a class name, an attribute, or a native element's own state as the content-security policy requires.

### T026 — Run the manual verification matrix

- **Status**: complete
- **Outcome**: the visual, responsive, right-to-left, keyboard, confirmation, and gate-regression outcomes are verified by observation and the result is recorded, because no automated check in this repository renders a page.
- **Paths**: no file changes; verification only
- **Dependencies**: T025
- **Covers**: NFR-002, NFR-003, NFR-004, REQ-021, REQ-022; Plan: Phase 6
- **Setup**: build a fixture profile with a candidate record and a consolidation cluster using the fixture builders in `tests/test_distill_review_core.py`, then start a session with `uv run codexspec _distill-review-helper --project-root <fixture>` — the project's development invocation, which does not depend on the tool being installed on the path — and it prints the token-protected local URL when it cannot open a browser.
- **Pass conditions**:
  - **P026.1** In both colour schemes every text and mark is legible, focus is visible on every control, and the gate and state colours are distinguishable from each other.
  - **P026.2** At 1280, 900, and 420 logical pixels the region count degrades as designed, no horizontal page scrolling appears, and the decision controls stay reachable. The 420 figure is the specification's labeled assumption for the narrowest supported width, not a confirmed requirement.
  - **P026.3** With a right-to-left interaction language, spacing, alignment, and borders follow the text direction.
  - **P026.4** One record's full cycle — select, read the final content, preview, decide — completes from the keyboard with no pointer, and no key performs batch application, cancellation, or draft discarding.
  - **P026.5** Each of the three confirmations states its consequence with the correct count, and declining changes nothing.
  - **P026.6** Previewing a cluster merge, keeping the records separate, then returning to the merge shows that a preview is needed rather than offering a decision the backend would refuse.
  - **P026.7** Both field-sizing paths behave: with the stylesheet property active, and with the fallback forced.

### T027 — Update the user guide for the user-visible changes

- **Status**: complete
- **Outcome**: the review-page section of the user guide states that every action removing record files — discarding a record and merging a cluster — and discarding the draft each require a second confirmation stating its consequence; that the queue, the progress, and the staged-change ledger show decision state; that the page is operable from the keyboard and advances to the next undecided item; and that the header names the project directory the session will write.
- **Paths**: `docs/en/user-guide/commands.md`
- **Dependencies**: T024
- **Covers**: REQ-013, REQ-016, REQ-018, REQ-020; Plan: Phase 6
- **Verification**: the section describes behavior that now exists and claims none that does not; `mkdocs build --strict` succeeds.

### T028 — Produce the documentation translations

- **Status**: complete
- **Outcome**: the seven translated guides carry the same changes as the English source, in one atomic reviewed change with it.
- **Paths**: `docs/de/user-guide/commands.md`, `docs/es/…`, `docs/fr/…`, `docs/ja/…`, `docs/ko/…`, `docs/pt-BR/…`, `docs/zh/…` — the seven translated documentation languages. **The documentation language codes are not the review-interface catalog codes**: the documentation uses `pt-BR` and `zh` where the catalogs use `pt`, `zh-CN`, and `zh-TW`, and the documentation has no Arabic, Hindi, Italian, or Russian version. Mirroring the catalog codes here would create directories the documentation site does not serve.
- **Dependencies**: T027
- **Authority**: necessary implementation support. It is required by the constitution's documentation principle and by this repository's documentation workflow, which records that translations are produced manually with `/codexspec:translate-docs` and committed together with the English source in one reviewed commit. It realizes no specification requirement and traces to no design component; the review interface's own language obligation is satisfied entirely by T004.
- **Verification**: `mkdocs build --strict` succeeds across every language version, which is the gate the documentation workflow runs.

**Checkpoint CP-F**: the full suite and lint are green — `uv run pytest` and `uv run ruff check src/ tests/` — before any push, and the remote pipeline is watched to completion rather than assumed green, as the constitution's push gate requires.

## Dependency Summary

- No cycles. Each task's dependencies appear earlier in this list.
- Three entry points can start concurrently: T001 and T002 (backend, different modules), T004 (catalogs), and T005 (tokens). T001 and T002 both add to one test file, so they are sequenced rather than marked concurrent.
- `T002 → T003` because the regression scenario observes the invariant through the projection.
- `T004 → T010` because the controller resolves the new keys; `T005 → T009` because the shell is styled by the token layer.
- Group D depends on Group B and Group C; Group E depends on Group D; Group F depends on Group E.
- `T027 → T028` because the translations follow the English source.

## Coverage

### Plan deliverable to task

| Plan deliverable | Task or checkpoint |
|---|---|
| Phase 1 — project-name projection | T001 |
| Phase 1 — gate digest projection | T002 |
| Phase 1 — revision invariant and its regression test | T003 |
| Phase 1 — closing confirmation of delivered gate tests | CP-A |
| Phase 2 — English catalog keys | T004 |
| Phase 2 — twelve translated catalogs | T004 (one change, per the plan's catalog decision) |
| Phase 2 — closing parity confirmation | CP-B |
| Phase 3 — token layer and dark override | T005 |
| Phase 3 — base typography and font stacks | T006 |
| Phase 3 — grid and degradations | T007 |
| Phase 3 — focus indicator | T008 |
| Phase 3 — closing stylesheet confirmation | CP-C |
| Phase 4 — page shell | T009 |
| Phase 4 — state store and interpolation | T010 |
| Phase 4 — state-change entry point and render pass | T011 |
| Phase 4 — queue renderer | T012 |
| Phase 4 — ledger and progress | T013 |
| Phase 4 — project name in header | T014 |
| Phase 4 — closing contract-test confirmation | CP-D |
| Phase 5 — adaptive field control | T015 |
| Phase 5 — record working surface | T016 |
| Phase 5 — final-content panel, gate indicator, verification state | T017 |
| Phase 5 — action bar | T018 |
| Phase 5 — destructive confirmations | T019 |
| Phase 5 — cluster working surface | T020 |
| Phase 5 — adjacent feedback | T021 |
| Phase 6 — keyboard map | T022 |
| Phase 6 — automatic advance | T023 |
| Phase 6 — empty and all-decided states | T024 |
| Phase 6 — extended contract assertions | T025 |
| Phase 6 — served-path and offline confirmation | S025.5, S025.8, CP-C |
| Phase 6 — manual matrix | T026 |
| Phase 6 — English documentation | T027 |
| Phase 6 — documentation translations | T028 |
| Phase 6 — full suite and lint before push | CP-F |

### Requirement to task

| Requirement | Tasks |
|---|---|
| REQ-001 | T009 |
| REQ-002 | T012, T024 |
| REQ-003 | T011 |
| REQ-004 | T009, T013 |
| REQ-005 | T016, T017 |
| REQ-006 | T017 |
| REQ-007 | T002, T003, T017 |
| REQ-008 | T017 |
| REQ-009 | T021 |
| REQ-010 | T013 |
| REQ-011 | T013 |
| REQ-012 | T018 |
| REQ-013 | T019, T027, P026.5 |
| REQ-014 | T015 |
| REQ-015 | T015 |
| REQ-016 | T022, T027, P026.4 |
| REQ-017 | T022 |
| REQ-018 | T023, T027 |
| REQ-019 | T024 |
| REQ-020 | T001, T009, T014, T027 |
| REQ-021 | T012, T026 |
| REQ-022 | T008, T009, T016, T021, T026 |
| REQ-023 | T020 |
| NFR-001 | T005, T006 |
| NFR-002 | T005, P026.1 |
| NFR-003 | T007, P026.2 |
| NFR-004 | T007, P026.3 |
| NFR-005 | S025.5, S025.8, CP-C |
| NFR-006 | T005, T009, CP-C, S025.4, S025.9 |
| NFR-007 | T003 |
| NFR-008 | T004, T010 |
| NFR-009 | T004, T006 |
| NFR-010 | T025, CP-A, CP-B, CP-D, CP-F |

### Test scenario to task

| Task | Scenarios |
|---|---|
| T001 | S001.1, S001.2, S001.3 |
| T002 | S002.1, S002.2, S002.3, S002.4, S002.5 |
| T003 | S003.1, S003.2, S003.3, S003.4, S003.5 |
| T025 | S025.1, S025.2, S025.3, S025.4, S025.5, S025.6, S025.7, S025.8, S025.9 |

Tasks T004 through T024 and T026 through T028 are catalog, asset, verification, and documentation work. The plan's test-discipline decision records that these are implemented directly and verified by the deterministic checks stated on each task, by the group checkpoints, and by the manual matrix, rather than by test scenarios of their own. T026 carries explicit pass conditions instead, and the behavior those tasks produce is additionally guarded by T025's scenarios.

## Unmapped Tasks

T028 realizes no specification requirement and is declared as necessary implementation support on the task itself, with the constitution's documentation principle and the repository's documentation workflow named as its authority. Every other task maps to at least one requirement and one plan deliverable.

## Implementation Notes

Recorded because each departs from the task list as written, or was found only by executing it.

- **T004 reformatted one existing block in eleven catalogs.** The plan's catalog decision said to preserve each file's formatting. The twenty keys were added by a JSON load, modify and dump, which also re-laid-out the `fieldLabels` object in the eleven catalogs that had written it several pairs to a line. The values are byte-identical; only the line layout changed, and all thirteen catalogs now match the one-pair-per-line form that English and Simplified Chinese already used. Accepted rather than reverted, because reproducing the compact layout would need custom serialization for a purely cosmetic result in files this change already touches.
- **T026 found two defects that no automated check in this repository could have caught.** First, the completion state never appeared: it was conditioned on the absence of candidate records, but a staged decision leaves a record's stored status as `candidate`, so that branch was unreachable and the last reviewed record stayed on screen with nothing undecided. It now reads completion from the draft, and a decided record remains reachable from the queue. Second, in a right-to-left interface the final-content panel rendered every Markdown line with its leading marker at the far edge, the file path put its first character at the wrong edge, and the queue's identifier line overflowed its box so the ellipsis truncated the start of an identifier rather than its end. Logical properties mirror box geometry but do not govern bidirectional text reordering; literal technical content now pins an explicit left-to-right direction while record titles and field values resolve direction from their own content. Both fixes carry a regression assertion in T025.
- **T019 corrected a latent defect in the delivered controller.** It attached the verification field to every staged operation, including a removal, which the domain rejects as a removal carrying a payload. A discard taken with text in the verification box would have been refused. Only a revision or a vetting now carries that field.
- **T022 changed how a decision key is dispatched.** Selecting the control by its position in the action bar meant one letter addressed different actions on the record and cluster surfaces — the discard letter would have started a merge. Each control now carries its key as an attribute and dispatch reads the attribute.
- **The repository's documented development install is stale.** `uv sync --dev` installs nothing here, because the dev dependencies are declared under `[project.optional-dependencies]` rather than as a dependency group; `uv sync --extra dev` is what installs pytest and ruff. Syncing with `--extra docs` alone removes them, after which `uv run pytest` silently falls back to an interpreter outside the project and fails to import the package under test.
- **T028 closed a pre-existing gap rather than translating a delta.** The section the English change edits did not exist in any of the seven translated guides; the whole section was translated and inserted, bringing every language to the same twenty-one documented commands. Each file keeps its own label convention: the Japanese and Korean guides carry English bold labels, and the inserted section matches that.

## Repairs Applied After the Complete-Feature Review

Twelve defects were admitted by the review gate and independently verified before any edit. Six were in this feature's own changes; six were in the carrier code this branch already carried, which the default review target includes. The user directed that all twelve be repaired on this branch rather than deferred.

**Verification gate read the request instead of the written bytes** — `domain.py` gated a vetting decision on the request's `evidence.state`, while `records.py` rebuilds that field from the stored value whenever an attestation is supplied and the apply-time gate reads the rendered bytes. A staged, previewed vet could therefore make the whole batch refuse. The stage-time gate now renders first and reads the rendered `evidence.state`, matching the apply-time gate exactly.

**A missing category directory was reported as a symlink attack and bricked the tool** — any `OSError` from the directory walk became `symlink_target`, so a consolidation promoting across categories failed, its rollback failed identically, the journal stayed in `applying`, and every later session including `--discard-draft` was refused by recovery. `prepare` now creates a needed category directory before any journal exists, `ENOENT` is reported as its own condition, and restore and cleanup treat an absent directory as nothing to do.

**Staging mutated the draft before its last validation** — a rejected request dropped an already-staged merge while leaving the revision unchanged, so a later apply reported success for a batch the user never reviewed. `stage` now computes and validates the decision before touching the draft.

**A saved merge became unopenable when a record joined its cluster** — the whole session refused rather than the one stale decision. The stale merge and its reconstructed proposal are now dropped, the cluster returns as undecided, and every other staged decision stays resumable.

**Three unguarded failure paths in the HTTP carrier** — a non-ASCII `Authorization` header raised `TypeError` from `compare_digest`, a caller-sized catalog name raised `OSError` from the unauthenticated asset branch, and the session read touched state every mutation locks. Each dropped the connection with no response. The comparison is now on bytes, the asset branch answers an unreadable name, and the session read takes the same lock.

**The gate indicator described one operation variant** — it was computed for the keep-candidate and merge-as-candidate variants while the vetting controls submit different operations, so it claimed a match for controls the backend still refuses. Every gated control now carries its own operation builder and is marked ready on its own terms.

**The post-stage render pass omitted the gate** — with the advance switch off, the indicator kept claiming a match after the backend cleared its set. The render pass now re-derives it.

**Completion was reachable only through the advance** — the switch governs jumping to the next item, not whether the interface states that none remain, and a restored fully-decided draft opened on an arbitrary record. Completion is now derived from the draft in both cases.

**A ledger entry could resolve to nothing and claim the queue was finished** — an in-scope non-candidate record now resolves to its cluster, an unresolvable selection falls back to remaining work, and the completion panel refuses to claim completion while work remains.

**Seven translated guides lacked three command-table rows** the English guide carries. All eight tables now match.

## Repairs Applied After the Second Fresh Review

A second isolated review of the repaired tree admitted seven further defects, each independently reproduced before any edit. All seven are fixed and each fix is pinned by a new regression test that failed against the pre-repair code.

**A failed transaction recovery permanently disabled review, and the documented escape hatch could not clear it (most severe)** — the helper ran `recover()` before reading `--discard-draft`, so a journal this version cannot recover from (a schema version from a newer release, corrupt bytes, an unresolved conflict, or a rollback that cannot finish) exited as an input error on every invocation, `--discard-draft` included, retaining the draft and the journal forever. The escape hatch now also covers this path: an explicit discard abandons the draft and the stuck journal together, while a successful recovery still precedes the discard. Recovery itself also resolved one self-made dead end: a category directory deleted while a batch was in flight left a replace-shaped journal entry that rollback refused forever, because the old bytes and the backup both lived in the vanished directory; recovery now treats an absent directory as nothing to restore, the same rule a created record already had.

**Dropping a stale staged merge deleted a fresh manifest proposal for the same cluster** — the stale-merge cleanup removed every consolidation for the cluster, including one freshly supplied by the current manifest, leaving the cluster unmergeable for the session and pushing the user toward discarding all staged work. The cleanup now removes only the proposal reconstructed from the stale draft, identified by its exact bytes; a manifest proposal describing current membership survives and the merge stages normally.

**Three request shapes crashed the HTTP handler instead of being refused** — an `operation` that is not an object reached code expecting a mapping; a body that is not valid UTF-8 escaped the JSON error path; and a lone surrogate inside an otherwise valid JSON string could not be encoded by any later UTF-8 write. Each killed the handler with no response. All three are now refused at the JSON boundary with explicit errors (`object_required`, `invalid_json`, `invalid_encoding`), and the response encoder fails safe. A manifest that is not valid UTF-8 likewise reports `invalid_manifest` instead of an unhandled decode error.

**The git-exclude rule for the review runtime was anchored at the repository root** — a project nested inside a larger repository wrote `/.codexspec/.runtime/` into `info/exclude`, which matches only the root's own path, so a nested project's draft and lock files were git-trackable, against the feature's exclusion requirement. The rule is now anchored at the project's path inside the repository.

**A concurrent session's capability token was printed to stdout** — the machine JSON for "a review session is already active" echoed the stored metadata verbatim, including the capability token and its token-bearing URL, exposing a live credential to whichever agent read the output. The machine envelope now omits exactly those two fields and keeps the operational ones (mode, process id, port).

Result: full suite green (1714 passed, 53 skipped), ruff clean, `mkdocs build --strict` clean.

## Repairs Applied After the Third Fresh Review

The third isolated review verified every incoming obligation (all twelve first-round behaviors and all seven second-round repairs) and admitted two further P3 findings, both in the page script. Each was reproduced against the running page before the fix.

**A cluster resolved by its members' own decisions never reached a decided state** — the queue lists cluster members individually, so deciding each member is a normal path, but the cluster state had no terminal branch for that outcome: the cluster stayed in the remaining-work set forever, keep-separate was a backend no-op that still invalidated the preview gate, auto-advance kept re-selecting the cluster surface, and the completion state was unreachable while the ledger already reported zero undecided — contradicting the requirement that page progress and the ledger cannot disagree. The cluster state now resolves as "separate" once every member carries a decision (or deferral), the queue marks it with the pass voice, the inert keep-separate control is no longer offered on such a surface, and completion is reachable. Verified in the browser: deciding both members through the real controls empties the remaining-work set and opens the completion panel.

**The keep-separate control's failure feedback bypassed the control-adjacent region** — every other decision control reports a refusal (a stale page revision, a finished session) next to itself; keep-separate alone wrote only the page-level status region, against the feedback-placement requirement. It now reports through the same form feedback path, verified in the browser by staging a revision bump behind the page's back and clicking the control: the refusal appears in the form's feedback region while the status region stays untouched.

Both fixes are pinned by new source-structure tests. No new interface strings were introduced, so the thirteen catalogs are unchanged.

## Repair Applied After the Fourth Fresh Review

The fourth isolated review verified twenty of the twenty-one incoming obligations and admitted one P2 defect, reproduced end-to-end before the fix.

**A whitespace-only verification attestation stranded an otherwise accepted decision** — stage time normalizes such an attestation to absent when it renders the record, but stored the raw string in the decision, and apply time re-renders from that stored value verbatim. Typing a space into the verification field therefore produced a decision the interface previewed and staged as accepted, and that the batch then refused wholesale with `empty_verification`, stranding the staged work until the field was re-edited. The decision now stores the value exactly as it was rendered, so stage and apply read the same bytes — the same stage/apply symmetry the vetting gate was given in the first repair round. Pinned by a regression test that stages with whitespace and requires the batch to apply; the whole suite passes.

The remaining coverage gaps the review recorded (no test previously pinned this symmetry; the two-tab shared-session flow needs a manual reload after a stale-revision refusal; a corrupt managed `.gitignore` would crash `init`) are noted for the record; none is a defect in this change.

## Repair Applied After the Fifth Fresh Review

The fifth isolated review verified all twenty-two incoming obligations and admitted one bounded P3 finding, reproduced from the code paths before the fix.

**The merge surface claimed verification evidence was required when the proposal's own evidence already satisfied the gate** — the record surface reads a backend-reported flag for whether stored evidence establishes verification, but the consolidation payload never carried the equivalent, so the cluster surface hard-coded the "required" hint while the backend would have accepted "Merge as vetted" with no attestation. The consolidation now reports `outcome_verified` — computed from its rendered evidence fields, on manifest proposals and on proposals reconstructed from a saved draft alike, and mirrored in the exact-reconstruction identity the stale-merge cleanup compares — and the surface reads that flag, so the interface and the backend state the same requirement. The review also recorded that the merge path stored the raw verification string while the record path stores the rendered value; that convention drift is now aligned, closing the last consumer-visible gap of the same shape the previous round repaired. Pinned by a backend flag test (verified and unverified proposals, plus an attestation-free vetted merge staging) and a surface source test; verified in the browser with an outcome-verified proposal showing the satisfied hint. No new interface strings: the satisfied-hint catalog entry already shipped, so the thirteen catalogs are unchanged.

## Repair Applied After the Sixth Fresh Review

The sixth isolated review verified all twenty-three incoming obligations and admitted one bounded P3 finding, reproduced before the fix.

**The keep-separate control was still offered on a cluster whose members are all deferred** — the guard added for member-decided clusters enumerated that resolution only, but deferral resolves a cluster just as fully: the backend's keep-separate changes nothing on it except the revision, yet the page reported "Decision staged." and invalidated the preview gate. The guard now covers both resolved states, so the control is offered only where the action can actually record something. Verified in the browser: after deferring both members through the real controls, the cluster surface offers preview and the two merge actions, and no keep-separate. The source assertion covering the guard was tightened first and failed against the pre-fix page.

## Repair Applied After the Seventh Fresh Review

The seventh isolated review verified all twenty-four incoming obligations and admitted one bounded P3 finding, reproduced before the fix.

**Structured field values crossed the staging boundary without the string type the draft codec requires** — `render` stringifies values silently, so a text-carrier edit or a raw loopback client could stage `{"claim": 42}`; the saved draft then failed its own schema at load and the only escape was discarding every staged decision. Field values are now type-checked at all three producers — record fields, merge field changes, and manifest-supplied editable values — with the same refusal convention as their sibling scalars, before any draft mutation. Pinned by tests for each producer, including the manifest ingestion path; a refused request leaves the draft byte-identical.

## Convergence Verdict — Round 8 (fresh review, no repairs required)

The eighth review round ran three fully isolated reviewers against one target fingerprint (`sha256:628aa7a4…`, 111 records). **All three admitted zero findings**, and every incoming obligation verified:

- **Primary reviewer** — 25/25 obligations verified, zero findings. Added independent verification beyond the obligations: an i18n key-parity and key-usage sweep across all thirteen catalogs, `node --check` on the page script, a rename audit, and live server probes including hostile body/header shapes.
- **Security specialist** — 2/2 obligations pass, zero findings. Exercised a live server across the full auth/origin matrix (non-ASCII and NUL authorization bytes, seven origin variants, path games, no redirect surface anywhere), hostile payloads (invalid UTF-8, lone surrogates in values and keys, non-object operations, wrong schema, oversized and non-integer lengths), DoS mechanics (semaphore saturation with clean recovery, deadline expiry at exactly the timeout, ten-thread mixed reads and writes converging to one coherent draft), an injection sweep (no HTML sinks, no inline handlers, CSP without unsafe-inline, no storage or cookie writes, no-referrer everywhere), disclosure scans (no token in any response body; digests only), and gate-evasion attempts (forged digests, post-advance replay, inline proposals, protected fields, stale revisions — all refused).
- **Filesystem/persistence specialist** — 4/4 obligations hold, zero findings. Ran twelve SIGKILL-mid-apply trials through real CLI recovery (every trial ended byte-identical to the original records, no stray backup or temp files, no surviving journal), hash-conflict races injected both between prepare and apply and mid-apply at a write boundary (batch refused or fully rolled back, third-party bytes preserved in both), lease races across processes, six-thread staging races (exactly one winner, five correct 409s), and real-git probes for nested, root-level, and non-repository projects.

The finding trajectory across the loop: 12 (two P1-class) → 7 → 2 → 1 → 1 → 1 → 1 → 0. Every admitted finding was independently reproduced before repair, fixed test-first, and pinned by a regression test; behavioral repairs were additionally verified in a live browser. The loop is closed on this fingerprint; the worktree is ready for the merge gate. Remaining coverage gaps on record: packaging gate runs in CI only (local build would write into the repository), Windows-specific branches run on Windows CI only, and two design-trade-off surfaces (two-tab shared-session staleness, reload after token stripping) self-recover through documented re-invocation.
