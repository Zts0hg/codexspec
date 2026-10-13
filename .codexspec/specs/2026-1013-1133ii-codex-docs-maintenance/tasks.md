# Tasks: Codex Documentation Maintenance

## Phase 1: Maintainer Command Infrastructure

- [x] T001 Define failing behavior tests in tests/test_maintainer_doc_tools.py
  and paired-maintainer cases in tests/test_command_template_fragments.py.
  Observe the new feature failures before implementation. Covers: REQ-001,
  REQ-002, REQ-003, REQ-005, NFR-001; Plan: Phase 1, unit 1.
  Test Scenarios: TS-001 through TS-012 below.

- [x] T002 Implement internal/maintainer_doc_skills.py and integrate exact
  maintainer-source-derived expectations in internal/command_template_fragments.py.
  Generate/check only the two native entries; preserve public distribution and
  unknown-extra rejection. Covers: REQ-001, REQ-005, NFR-001;
  Plan: Phase 1, unit 2. Depends on T001.
  Test Scenarios:
  - TS-001: Native source conversion and current-byte regeneration.
  - TS-002: Read-only check rejects stale/missing native output.
  - TS-003: Unsafe output preflight rejects before either file is changed.
  - TS-004: Public installation stays unchanged; known pair and unknown-extra rules.

- [x] T003 Implement inventory/verify in internal/doc_translation.py for README
  and site selection, target aliases, preservation/structure and local navigation.
  Covers: REQ-002, REQ-003, REQ-005, NFR-001;
  Plan: Phase 1, unit 2. Depends on T001.
  Test Scenarios:
  - TS-005: Complete README mapping and resource aliases.
  - TS-006: Existing site source selection and timestamp incremental behavior.
  - TS-007: Invalid/duplicate languages fail without writes.
  - TS-008: Missing/redirected/escaping selected paths fail without writes.
  - TS-009: Valid translated headings, tokens, examples and tables pass.
  - TS-010: Changed/omitted technical content or structure fails.
  - TS-011: Invalid local links/Unicode or duplicate heading anchors fail.
  - TS-012: Inventory/verification/dry-run CLI operations remain read-only.

- [x] T004 Update .claude/commands/codexspec/translate-docs.md and
  .claude/commands/codexspec/check-i18n-semantics.md; add shared
  internal/references/doc-translation.md; derive both Codex SKILL.md files.
  Align maintainer-only authoring/scope guidance in constitution, CLAUDE.md,
  AGENTS.md and docs/internal/repository-layout.md. Covers: REQ-001, REQ-002,
  REQ-003, REQ-005, NFR-001; Plan: Phase 1, unit 3. Depends on T002, T003.
  Verification: renderer/check pass, shared references resolve, preserved public
  registrations/install output and consistent host semantics.

## Phase 2: Complete README Translation and Review

- [x] T005 Invoke the new worktree Codex translate-docs entry in README/all mode;
  pin English source hash and translate all seven root variants completely:
  README.zh-CN.md, README.ja.md, README.ko.md, README.es.md, README.fr.md,
  README.de.md, README.pt-BR.md. Covers: REQ-002, REQ-003, REQ-004, REQ-005,
  NFR-001; Plan: Phase 2, unit 4. Depends on T004.
  Verification: complete section mapping; immutable examples/tokens retained;
  active-language navigation and translated TOC anchors work.

- [x] T006 Invoke new worktree Codex check-i18n-semantics for all seven complete
  pairs. Assess source propositions, default values, conditions/order/exclusions,
  capability coverage, notes, terminology and native readability. Repair verified
  issues and record per-language evidence in translation-review.md.
  Covers: REQ-003, REQ-004, NFR-001;
  Plan: Phase 2, unit 5. Depends on T005.
  Verification: no unresolved substantive semantic or mechanical defect.

## Phase 3: Verification and Complete-Feature Acceptance

- [x] T007 Run native/distribution checks, Python lint, declared Markdown lint,
  package exclusion checks, targeted and full suite, seven-language mechanics,
  English hash, scope and whitespace checks. Map every TS to real asserting tests;
  save actual outcomes and execution provenance in verification.md.
  Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001;
  Plan: Phase 3, unit 6. Depends on T004, T006.

## Mandatory Acceptance Checkpoint

After T001–T007 and their green baseline, run the fresh isolated complete-feature
review required by implement-tasks. Validate the defect envelope, maintenance,
coverage and findings; repair only independently verified problems with green
checks; completion requires a valid complete PASS. Review state remains external.
This checkpoint covers all requirements and Plan Phase 3, unit 7. It is separate
from implementation task checkboxes so its own review can inspect frozen tasks.

## Test Scenario Definitions

- TS-001: Both authored entries render valid named Codex frontmatter and native
  argument/invocation syntax; changing source changes expected bytes.
- TS-002: Current entries pass; missing/stale entries fail; check never repairs.
- TS-003: Symlinked/non-regular/hard-linked outputs or redirected parent paths
  fail preflight and preserve every existing output byte.
- TS-004: A maintainer source requires its matching native entry; unknown extras
  remain errors; fresh public install contains the same registered public set.
- TS-005: Full README inventory has exactly seven root targets; zh/zh-CN and
  pt/pt-BR normalize to the correct resource names.
- TS-006: Site directory/single-file input preserves relative paths and docs/zh
  versus README.zh-CN distinction; timestamp selection includes missing/newer pairs.
- TS-007: Unsupported language and duplicate normalized targets give errors and
  do not create or alter translation files.
- TS-008: Missing source, redirected source/target or escaping selection is
  refused with existing source/target bytes unchanged.
- TS-009: Translated headings with correct anchors, retained fenced/code spans,
  equivalent table structure and valid relative links pass mechanics.
- TS-010: Changed fenced code, missing inline token, missing heading and malformed
  table each fail with a corresponding diagnostic.
- TS-011: Missing local file, missing Unicode heading anchor and wrong duplicate
  heading suffix are detected; valid Unicode and duplicate slugs resolve.
- TS-012: Invoking inventory, verify and preview paths never mutates selected
  sources, targets or creates hidden persistent state.

## Dependencies and Coverage

T001 → T002/T003 → T004 → T005 → T006 → T007 → acceptance checkpoint.

| Requirement / Plan | Tasks |
|--------------------|-------|
| REQ-001 | T001, T002, T004, T007 |
| REQ-002 | T001, T003, T004, T005, T007 |
| REQ-003 | T001, T003, T004, T005, T006, T007 |
| REQ-004 | T005, T006, T007 |
| REQ-005 | T001, T002, T003, T004, T005, T007 |
| NFR-001 | All tasks |
| Phase 1 units 1–3 | T001–T004 |
| Phase 2 units 4–5 | T005–T006 |
| Phase 3 unit 6 | T007 |
| Phase 3 unit 7 | Mandatory acceptance checkpoint |

Instructions, guidance and translations are documentation tasks with direct
implementation and verification. New functional mechanics follow red-green.
