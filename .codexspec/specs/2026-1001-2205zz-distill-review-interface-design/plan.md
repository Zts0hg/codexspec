# Implementation Plan: Distill Review Interface Design

**Related Spec**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/spec.md`<br>
**Related Design**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/design.md`<br>
**Confirmed Requirements**: `.codexspec/specs/2026-1001-2205zz-distill-review-interface-design/requirements.md`<br>
**Created**: 2026-10-01<br>
**Status**: Draft

## Context

This plan implements the confirmed design for the manual distill review workspace. The architecture, the component responsibilities, the token table, the response contracts, the catalog key list, the keyboard map, and the eight design decisions are defined in `design.md` and are not restated here.

The work touches four code surfaces and one documentation surface: `src/codexspec/distill_review/domain.py` and `server.py` for two additive read-only projections and the preview-gate invariant; the thirteen interaction-language catalogs under `src/codexspec/distill_review/assets/i18n/`; the three served assets `index.html`, `styles.css`, and `app.js` in that same directory; and the review-page section of the user guide at `docs/en/user-guide/commands.md` with its translations, because the behavior that section describes changes. It adds no file, no dependency, and no served path.

## Goals / Non-Goals

**Goals:**

- Deliver the confirmed design so a reviewer can see every record's decision state, the review progress, the exact bytes a decision will write, and the gates before they refuse.
- Separate and confirm every action that removes record files or drops staged decisions.
- Produce one coherent visual system in both colour schemes that holds up at narrow widths and in a right-to-left interaction language.
- Keep every delivered review safety property and every delivered accessibility behavior intact, and keep the repository gates that guard them green at every step.
- Keep the user guide truthful about the page, in every language it ships in, so a reader learns that merging now requires a confirmation and that the page is operable from the keyboard.

**Non-Goals:**

- Changing what the review workflow does. No decision action is added and no staging, application, conflict, or vetting rule changes.
- Changing the terminal review carrier, which keeps its current prompts and output.
- Introducing a bundler, framework, icon set, web font, or any dependency.
- Regenerating install artifacts. This feature changes package code under `src/codexspec/`, not a slash-command template, so neither `templates/commands/` nor the derived `.claude/commands/codexspec/` and `.agents/skills/` trees are involved and no `codexspec init --force` resync is part of this work.

## Tech Stack

- **Language**: Python 3.11 for the backend projections; browser-native HTML, CSS, and JavaScript for the page, with no build step and no dependency.
- **Served assets**: three files plus the per-language catalogs, delivered from the package directory over the existing loopback server.
- **Tests**: pytest, in the existing `tests/test_distill_review_interfaces.py` and `tests/test_distill_review_core.py`.
- **Lint**: ruff, line length 120.

## Existing Repository Constraints

Verified before planning; each one shapes the sequence below.

- **The served-path allowlist is closed.** `ReviewHandler.do_GET` in `src/codexspec/distill_review/server.py` maps only `/`, `/index.html`, `/app.js`, `/styles.css`, and `/i18n/<lang>.json`. No new asset file can be reached, so the whole interface must land in those files.
- **The three assets must contain no absolute URL scheme.** `tests/test_distill_review_interfaces.py::test_frontend_is_offline_and_uses_fragment_bearer` concatenates the page, the script, and the stylesheet and asserts that neither `http://` nor `https://` appears. This is what rules out vector graphics, and it is easy to break accidentally in a comment or a data URI.
- **That same test pins a list of implementation symbols**, including `renderConsolidation`, `renderRecordContext`, `previewOperation`, `previewMatches`, `previewBeforeStage`, `formatError`, `formatResult`, `record.editable_fields`, `state.proposals[record.id]`, `state.draft.decisions[record.id]`, `staged.field_changes`, `Object.keys(state.clusters)`, `details.records`, and `details.failures`. The rewrite keeps these names and expressions rather than renaming them.
- **A second test pins the accessibility contract**: `test_frontend_connects_field_errors_to_controls_and_moves_focus` requires `aria-live="polite"` and `tabindex="-1"` in the page, and `label.htmlFor = id`, `input.setAttribute("aria-invalid", "true")`, `input.setAttribute("aria-describedby", input.dataset.errorId)`, `input.focus()`, and the right-to-left direction ternary in the script.
- **Catalog parity is enforced across thirteen files.** `test_frontend_and_terminal_catalogs_cover_every_interaction_language` asserts that every catalog's top-level key set equals the English one, that `documentTitle` and `navigationLabel` are non-empty, and that `fieldLabels` holds exactly its thirteen keys with values that differ from the key. A key added to fewer than thirteen catalogs is a red suite. **This catalog set is not the command-frontmatter catalog set** under `templates/translations/`; the two are separate surfaces and this feature touches only the review assets.
- **The persisted draft rejects unknown fields.** `ReviewDraft.from_dict` in `models.py` validates each decision with exact key-set equality, so nothing may be added to a draft decision. All new state is ephemeral.
- **Assets already ship.** `pyproject.toml` sets `packages = ["src/codexspec"]` for the wheel and includes `/src` in the sdist, so the asset and catalog files are packaged with no configuration change. No packaging edit is planned; the existing archive check still runs before release.
- **The constitution's push gate applies.** The full local suite and lint must pass before a push, and the remote pipeline must be watched to completion rather than assumed green.

## Plan-Level Decisions

### Decision 1: Land the backend projections and the catalogs before the front-end rewrite

**Context**: The work splits into parts with very different verifiability. The two response projections and the gate invariant are testable in isolation with pytest. The catalog additions are verified by an existing assertion. The page itself has no automated visual verification and is one artifact that cannot be half-migrated.

**Options Considered**:

1. Backend and catalogs first, then the page.
2. Page first against stubbed data, then wire the backend.

**Decision**: Option 1.

**Rationale**: Each early phase ends with the suite green and the delivered page still working, so a regression is attributable to the phase that introduced it. Option 2 would require throwaway stubs for data the backend already returns, and would leave the page referencing fields that do not exist yet.

**Covers**: REQ-007, REQ-020, NFR-008; Design: Session snapshot extension, Preview gate authority, Localization layer

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design

### Decision 2: Add the twenty catalog keys to all thirteen files in one change

**Context**: The parity assertion compares every catalog's key set with the English one, so a partial rollout is a red suite rather than an incremental step.

**Options Considered**:

1. One change covering English plus the twelve other languages.
2. English first, then translations in follow-up changes.

**Decision**: Option 1, applying each file with a JSON load, modify, and dump at `indent=2` and `ensure_ascii=False` so existing formatting and non-ASCII text survive unchanged.

**Rationale**: Option 2 cannot produce a green intermediate state. The load-modify-dump approach is the method this repository already uses for its other catalog set, where editing by string replacement proved unsafe because values are shared between entries.

**Covers**: NFR-008, NFR-009; Design: Localization layer

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design

### Decision 3: Replace the page and the controller in one phase, with units in dependency order

**Context**: `index.html` gains elements the controller renders into, and the controller's render pipeline depends on those elements. A phase boundary between them would leave the page broken at that boundary.

**Options Considered**:

1. Shell and render pipeline in one phase, then the working surface, then the keyboard and end states.
2. One unit per requirement, each shipping independently.

**Decision**: Option 1.

**Rationale**: The shell, the state store, the single render pass, the queue, and the ledger are mutually dependent — the render pass is what keeps them consistent, which is the point of the confirmed design's single-entry-point decision. The working surface and the keyboard layer sit on top of that pipeline and can follow as separate phases. Option 2 would strand the page in a non-working state between units.

**Covers**: REQ-001, REQ-002, REQ-003, REQ-004; Design: Page shell, Queue renderer, Staged-change ledger and progress

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design

### Decision 4: Python changes are test-first; markup, stylesheet, and catalog data are implemented directly and verified by contract assertions plus a manual matrix

**Context**: This repository's implementation discipline applies test-first development to code and direct implementation to documentation and configuration. The work here spans both: the projections and the gate invariant are behavior with a natural failing-test form, while a token table, a grid, and a translated string have none beyond the structural assertions written alongside them.

**Options Considered**:

1. Test-first for the Python surface; direct implementation plus contract assertions and a manual matrix for the assets.
2. Test-first for everything, including the stylesheet and markup.

**Decision**: Option 1.

**Rationale**: Option 2 produces assertions that restate the implementation — a test that a token exists, or that a rule mentions a breakpoint — which pass without establishing that the interface is legible in either scheme. What actually verifies the asset work is the structural contract already enforced by the existing tests, extended for the new behavior, plus the manual matrix in the verification strategy, which is a required gate here and not an optional extra because no automated check in this repository renders a page.

**Covers**: NFR-010; Design: Verification (Cross-Cutting Design)

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design

### Decision 5: New assertions go into the existing distill-review test files

**Context**: The front-end contract, the catalog parity rule, and the server behavior are already asserted in `tests/test_distill_review_interfaces.py`, with the record and domain layer in `tests/test_distill_review_core.py`.

**Options Considered**:

1. Extend the two existing files.
2. Add a new test module for the interface redesign.

**Decision**: Option 1.

**Rationale**: The new assertions guard the same contracts as the ones already there, including the ones that must not regress; keeping them together means a reader sees the whole contract in one place and a future change cannot satisfy one file while breaking the other.

**Covers**: NFR-010; Design: Verification (Cross-Cutting Design)

**Decision Level**: Plan-level implementation decision; does not change confirmed product scope or the confirmed design

## Risks / Trade-offs

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| An absolute URL scheme slips into a comment, a data URI, or a namespace attribute in one of the three assets | Medium | High — the offline assertion fails and, if it were ever relaxed, the page would reach the network | Treat the offline assertion as a per-phase gate, not an end-of-work check; never introduce vector graphics, as the design already forbids |
| One of the pinned implementation symbols is renamed during the rewrite | Medium | Medium — a red suite that looks like a regression in behavior rather than a renamed symbol | The symbol list is recorded under Existing Repository Constraints; run the two front-end contract tests after every asset unit |
| Translating twenty keys into twelve languages introduces an encoding or key-order error | Medium | Medium — a red parity assertion, or shipped text that is wrong in one language | Apply per file with JSON load, modify, dump at `indent=2`, `ensure_ascii=False`; the parity assertion catches a missing key, so the residual risk is translation quality, reviewed per language |
| `field-sizing: content` is unavailable in the reviewer's browser and the fallback is untested there | Medium | Medium — field heights stop following content, reintroducing the inconsistency the feature removes | Implement the `rows` fallback in the same unit as the CSS property, guard the capability check so a missing `CSS` object cannot throw, and exercise both paths in the manual matrix |
| A geometric state character renders as a blank or with emoji presentation on some platform | Medium | Low — the mark is decorative and the state is also in text | Confirmed in the design: marks are `aria-hidden` and never the sole carrier; check the marks on each platform available during the manual matrix |
| The manual matrix is skipped under time pressure | Low | High — the one gate that verifies the visual, responsive, right-to-left, and keyboard outcomes is the only one not automated | The matrix is listed as a required verification unit with explicit pass conditions and a named launch command, not as polish |
| The documentation change carries a seven-language translation obligation | High | Medium — a partial change either leaves the translated guides describing behavior that no longer exists, or splits one reviewed commit into several | Produce the English source and all translations in one change with the maintainer translation command, as this repository's documentation workflow records; the documentation build gate runs `mkdocs build --strict` across every language, so a malformed translation fails before merge |
| The full suite is large, so running it on every unit is slow | High | Low | Run the two distill-review test files per unit and the full suite plus ruff before any push, as the constitution's push gate requires |

## Implementation Phases

### Phase 1: Backend projections and the preview-gate invariant

- [ ] Add a failing test that `GET /api/session` reports the project directory name — **Covers**: REQ-020; Design: Session snapshot extension
- [ ] Add `project_name` to `ReviewService.snapshot()` from the resolved project root's directory name — **Covers**: REQ-020; Design: Session snapshot extension
- [ ] Add failing tests that `POST /api/preview` returns a gate digest and that the session, draft, and refresh responses report the digests the server holds — **Covers**: REQ-007; Design: Preview gate authority
- [ ] Add the digest helper and the `gate_token` and `gate_tokens` projections in the request handler, leaving the carrier-independent domain untouched — **Covers**: REQ-007; Design: Preview gate authority, Key Design Decision 1
- [ ] Add a failing regression test for the false-ready path: preview a cluster merge, stage a keep-separate so the revision advances, then confirm the server reports no valid digest and still refuses the merge — **Covers**: REQ-007, NFR-010; Design: Preview gate authority
- [ ] Replace the single-key discard with clearing the previewed-operation set when the draft revision advances, keeping the existing clear on refresh and keeping the rollback path unchanged so a failed save leaves the restored revision's key valid — **Covers**: REQ-007, NFR-007; Design: Preview gate authority, Key Design Decision 1
- [ ] Confirm the delivered gate tests still pass, including the one that stages only after a matching preview — **Covers**: NFR-007, NFR-010; Design: Verification

### Phase 2: Interaction-language catalogs

- [ ] Add the twenty new keys to the English catalog with their final text — **Covers**: NFR-008; Design: Localization layer
- [ ] Add the same twenty keys, translated, to the other twelve catalogs, preserving each file's formatting and non-ASCII text — **Covers**: NFR-008, NFR-009; Design: Localization layer
- [ ] Confirm catalog parity and the unchanged `fieldLabels` key set — **Covers**: NFR-008, NFR-010; Design: Verification

### Phase 3: Visual system — tokens, base, layout

- [ ] Replace the stylesheet's ad-hoc rules with the token layer and its dark-scheme override, declaring every colour, type step, spacing step, and radius once — **Covers**: NFR-001, NFR-002; Design: Design token layer
- [ ] Set the base typography including the control weight reset that removes the inherited semibold on field values, and the two font stacks with their CJK and Arabic fallbacks — **Covers**: NFR-001, NFR-009; Design: Design token layer
- [ ] Implement the three-region grid and its two degradations using logical properties throughout — **Covers**: NFR-003, NFR-004; Design: Layout and responsive grid
- [ ] Implement the single focus-visible rule from an accent-derived token so focus is visible in both schemes — **Covers**: REQ-022; Design: Cross-Cutting Design — Accessibility
- [ ] Confirm the stylesheet carries no style element, no style attribute, no vector graphic, and no absolute URL scheme — **Covers**: NFR-006; Design: Key Design Decision 2

### Phase 4: Page shell and render pipeline

- [ ] Rewrite the page markup: the three regions, the header slots for the project name, the native progress element and the labeled automatic-advance checkbox, the hidden key-hint region, and the ledger container, preserving every pinned element identity and accessibility attribute — **Covers**: REQ-001, REQ-004, REQ-020, REQ-022; Design: Page shell
- [ ] Implement the page state store and the string interpolation helper — **Covers**: NFR-008; Design: Localization layer
- [ ] Implement the single state-change entry point and the one render pass it drives over queue, ledger, progress, and gate indicator, leaving the open working surface untouched — **Covers**: REQ-003; Design: Key Design Decision 6
- [ ] Implement the queue renderer: four labeled groups with counts, per-entry decision state from the draft decisions, the decorative state mark, and the current-selection semantics — **Covers**: REQ-002, REQ-021; Design: Queue renderer, Key Design Decision 4
- [ ] Implement the ledger and the progress reading from the backend accounting, omitting empty groups except the undecided one, and resolving every listed identifier to a selection target including the merge-created identifier — **Covers**: REQ-004, REQ-010, REQ-011; Design: Staged-change ledger and progress, Key Design Decision 5
- [ ] Render the project directory name in the header — **Covers**: REQ-020; Design: Page shell
- [ ] Confirm the two front-end contract tests still pass — **Covers**: NFR-010; Design: Verification

### Phase 5: Working surface

- [ ] Implement the adaptive field control: one control type for every editable field, the stylesheet sizing property with a guarded capability check and a `rows` fallback, line-break cancellation on input, and paste normalization — **Covers**: REQ-014, REQ-015; Design: Adaptive field control, Key Design Decision 2
- [ ] Implement the record working surface: title at the largest type step, the compact metadata list replacing the browser-indented definition list, and the field grid, preserving the label association and the field-error channel — **Covers**: REQ-005, REQ-022; Design: Working surface renderer
- [ ] Implement the final-content panel and the three-state gate indicator from the recorded digest and the pre-edit snapshot, plus the verification-requirement state read from the existing record field — **Covers**: REQ-005, REQ-006, REQ-007, REQ-008; Design: Final-content panel and preview gate indicator
- [ ] Implement the action bar: routine decisions grouped, file-removing decisions separated in position, weight, and colour, previewing as the primary control while the gate is unsatisfied — **Covers**: REQ-012; Design: Decision action bar and destructive confirmation
- [ ] Implement the confirmations for discarding a record, staging a merge, and discarding the draft, each stating its consequence with its count, with the gate evaluated before the confirmation so no confirmation is raised for an action the backend would refuse — **Covers**: REQ-013; Design: Decision action bar and destructive confirmation, Key Design Decision 3
- [ ] Implement the cluster working surface: member records, proposal fields, and the merge and keep-separate decisions under the same panel, gate, and separation rules — **Covers**: REQ-023; Design: Working surface renderer, Decision action bar
- [ ] Move decision feedback next to the control that produced it, keeping the status region for session-level outcomes and fatal errors with its multi-line error rendering — **Covers**: REQ-009, REQ-022; Design: Status and feedback channel

### Phase 6: Keyboard, advance, end states, and verification

- [ ] Implement the keyboard map as data, with dispatch, the rendered hint, inertness inside editable controls, and no binding for batch application, cancellation, or draft discarding — **Covers**: REQ-016, REQ-017; Design: Keyboard controller, Key Design Decision 7
- [ ] Implement the automatic advance to the next undecided item, active at open, with its visible switch — **Covers**: REQ-018; Design: Key Design Decision 6, Page shell
- [ ] Implement the empty-queue state and the all-decided state that offers batch application as the next step — **Covers**: REQ-002, REQ-019; Design: Queue renderer, Status and feedback channel
- [ ] Extend the front-end contract assertions: the queue's current-selection semantics, the three gate states, a confirmation path for each of the three file-removing or decision-dropping actions, the native progress element, and the two response projections — **Covers**: NFR-010; Design: Verification
- [ ] Confirm no served path was added and the three assets still contain no absolute URL scheme — **Covers**: NFR-005, NFR-006; Design: Cross-Cutting Design — Security and delivery
- [ ] Run the manual verification matrix and record its result — **Covers**: NFR-002, NFR-003, NFR-004, REQ-021, REQ-022; Design: Cross-Cutting Design — Accessibility, Internationalization and direction
- [ ] Update the review-page section of `docs/en/user-guide/commands.md` for the user-visible changes: that every action removing record files — discarding a record and merging a cluster — and discarding the draft each require a second confirmation stating its consequence; that the queue, the progress, and the staged-change ledger show decision state; that the page is operable from the keyboard and advances to the next undecided item; and that the header names the project directory the session will write — **Covers**: REQ-013, REQ-016, REQ-018, REQ-020; Design: Decision action bar and destructive confirmation, Keyboard controller, Page shell
- [ ] Produce the seven documentation translations in the same change as the English source with `/codexspec:translate-docs`, the maintainer-only command for this repository's own documentation, so the source and its translations land in one atomic reviewed commit as the documentation workflow records — **Necessary implementation support**: required by the constitution's documentation principle and by the documentation workflow's recorded convention; it realizes no specification requirement of its own and traces to no design component, because the review interface's own language obligation is NFR-008 and NFR-009 and is satisfied entirely by the interaction-language catalogs in Phase 2
- [ ] Run the full suite and ruff, and keep them green before any push — **Covers**: NFR-010; Design: Verification

## Verification Strategy

**Automated, per phase.** Phase 1 is test-first: each projection and the gate invariant gets a failing test before its implementation, including the false-ready regression that motivated the invariant. Phases 2 through 6 run `tests/test_distill_review_interfaces.py` and `tests/test_distill_review_core.py` after every unit, because those files hold the offline assertion, the pinned implementation symbols, the accessibility contract, and catalog parity — the four contracts most easily broken by a rewrite.

**Automated, at the end.** The full pytest suite and ruff, both green, before any push. The constitution's push gate also requires watching the remote pipeline to completion rather than assuming it.

**Manual matrix, required.** No automated check in this repository renders a page, so the following is a gate, not polish. Build a fixture project holding at least one candidate record per shape and one consolidation cluster — `make_profile` and `write_consolidation_manifest` in `tests/test_distill_review_core.py` already produce exactly that shape — then start a review session against it with the hidden helper command `codexspec _distill-review-helper --project-root <fixture>`, which prints the token-protected local URL when it cannot open a browser. Then confirm:

- Both colour schemes: every text and mark is legible, focus is visible on every control, and the gate and state colours are distinguishable.
- Three widths — 1280, 900, and 420 logical pixels: the region count degrades as designed, no horizontal page scrolling appears, and the decision controls stay reachable. The 420-pixel figure is the specification's labeled assumption for the narrowest supported width, not a confirmed requirement; if it is revised, this bullet follows it and no requirement changes.
- A right-to-left interaction language: spacing, alignment, and borders follow the text direction.
- Keyboard only: one record's full cycle — select, read the final content, preview, decide — with no pointer, and no key triggering batch application, cancellation, or draft discarding.
- Each of the three confirmations: discarding a record, staging a merge over several members, and discarding a draft holding several staged decisions; each states its consequence with the right count and nothing happens on cancel.
- The gate's own regression path: preview a cluster merge, keep the records separate, return to the merge, and confirm the indicator reports that a preview is needed rather than offering a decision the backend would refuse.
- Both field-sizing paths: with the stylesheet property active, and with the fallback forced.

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|---|---|---|
| REQ-001 | Page shell; Layout and responsive grid | Decision 3 / Phase 3 / Phase 4 |
| REQ-002 | Queue renderer | Decision 3 / Phase 4 / Phase 6 |
| REQ-003 | Key Design Decision 6 | Decision 3 / Phase 4 |
| REQ-004 | Staged-change ledger and progress | Decision 3 / Phase 4 |
| REQ-005 | Final-content panel; Working surface renderer | Phase 5 |
| REQ-006 | Final-content panel and preview gate indicator | Phase 5 |
| REQ-007 | Preview gate authority; Key Design Decision 1 | Decision 1 / Phase 1 / Phase 5 |
| REQ-008 | Final-content panel and preview gate indicator | Phase 5 |
| REQ-009 | Status and feedback channel | Phase 5 |
| REQ-010 | Staged-change ledger and progress | Phase 4 |
| REQ-011 | Staged-change ledger and progress | Phase 4 |
| REQ-012 | Decision action bar and destructive confirmation | Phase 5 |
| REQ-013 | Decision action bar; Key Design Decision 3 | Phase 5 / Phase 6 manual matrix |
| REQ-014 | Adaptive field control | Phase 5 |
| REQ-015 | Adaptive field control | Phase 5 |
| REQ-016 | Keyboard controller; Key Design Decision 7 | Phase 6 |
| REQ-017 | Keyboard controller | Phase 6 |
| REQ-018 | Key Design Decision 6; Page shell | Phase 6 |
| REQ-019 | Status and feedback channel | Phase 6 |
| REQ-020 | Session snapshot extension; Page shell | Decision 1 / Phase 1 / Phase 4 |
| REQ-021 | Queue renderer; Accessibility | Phase 4 / Phase 6 manual matrix |
| REQ-022 | Page shell; Adaptive field control; Status channel; Accessibility | Phase 3 / Phase 4 / Phase 5 / Phase 6 manual matrix |
| REQ-023 | Working surface renderer; Decision action bar | Phase 5 |
| NFR-001 | Design token layer; Key Design Decision 4 | Phase 3 |
| NFR-002 | Design token layer | Phase 3 / Phase 6 manual matrix |
| NFR-003 | Layout and responsive grid | Phase 3 / Phase 6 manual matrix |
| NFR-004 | Layout and responsive grid | Phase 3 / Phase 6 manual matrix |
| NFR-005 | Cross-Cutting Design — Security and delivery | Phase 6 |
| NFR-006 | Key Design Decision 2; Key Design Decision 4 | Phase 3 / Phase 6 |
| NFR-007 | Key Design Decision 1; Key Design Decision 8 | Phase 1 |
| NFR-008 | Localization layer | Decision 2 / Phase 2 / Phase 4 |
| NFR-009 | Localization layer; Status and feedback channel | Phase 2 / Phase 3 |
| NFR-010 | Cross-Cutting Design — Verification | Decision 4 / Decision 5 / every phase's closing unit |
