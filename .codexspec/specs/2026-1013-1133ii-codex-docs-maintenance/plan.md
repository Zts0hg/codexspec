# Implementation Plan: Codex Documentation Maintenance

## Context and Scope

Implement [design.md](design.md) against the confirmed requirements/spec. Keep
all writes and checks in `2026-1013-1133ii-codex-docs-maintenance`. Retain the
English README and historical records, the 28 public distributed commands and
existing site content. No new user runtime dependency is needed.

## Approach and Decisions

### Decision 1: Implement and verify maintainers' mechanics before translation

Build deterministic entry rendering, selection and preservation/link checks
with meaningful test-first cases. Then update shared instructions, derive the
native entries, and invoke those new entries for actual translation/review.
This ordering proves the command mechanics before producing large outputs.

Covers: REQ-001, REQ-002, REQ-003, REQ-005;
Design: Shared instructions; native rendering/checks; deterministic verification.

### Decision 2: Preserve full-source correspondence for every language

Use full README mode for this run, not timestamp-based incremental mode. Preserve
code/example blocks and technical spans while translating prose/structure;
reconstruct translated TOC anchors and active-language navigation. Complete
one language at a time and verify it, then assess all pairs semantically.

Covers: REQ-003, REQ-004, NFR-001;
Design: Translation execution and semantic assessment.

### Decision 3: Maintain checkout-specific and external verification evidence

Use the selected worktree's uv-managed CPython 3.11.13 and editable import path.
Fixture roots, caches, rendering/build outputs and review state remain outside
Git checkouts. Record real red/green and final outcomes; never use a prior report
as correctness evidence. Run targeted tests then required full-suite, Markdown,
Python style, distribution and package checks before the isolated final review.

Covers: REQ-001, REQ-003, REQ-004, REQ-005, NFR-001;
Design: Native checks; deterministic verification; semantic assessment.

## Phases and Units

### Phase 1: Maintainer command infrastructure

1. Add `tests/test_maintainer_doc_tools.py` with entry-rendering, current/stale
   checking, output preflight, README/site mapping, language/error cases and
   mechanical verification scenarios. Extend relevant self-bootstrap cases in
   `tests/test_command_template_fragments.py` to establish the paired maintainer
   expectations while retaining unknown-extra rejection. Observe failures before
   implementing the new mechanics.
2. Implement `internal/maintainer_doc_skills.py` and
   `internal/doc_translation.py`; integrate the two exact maintainer expectations
   in `internal/command_template_fragments.py`. Reuse native renderer and stable
   filesystem checks where appropriate; do not change src/ or installation lists.
3. Update the two authored `.claude/commands/codexspec/` entries, add
   `internal/references/doc-translation.md`, and derive the two Codex SKILL.md
   entries. Align the maintainer-only scope/authoring instructions in
   `.codexspec/memory/constitution.md`, `CLAUDE.md`, `AGENTS.md` and
   `docs/internal/repository-layout.md`; preserve all unrelated principles and
   the generic end-user constitution. Verify maintained entries and public scope.

Covers: REQ-001, REQ-002, REQ-003, REQ-005, NFR-001;
Design: Shared instructions; native rendering/checks; deterministic verification.

### Phase 2: Execute complete README translations

4. Explicitly invoke the worktree's new Codex translate-docs entry in README/all
   language mode. Pin English source hash, read glossary, and translate the seven
   complete source-target pairs to README.zh-CN.md, README.ja.md, README.ko.md,
   README.es.md, README.fr.md, README.de.md and README.pt-BR.md.
5. Invoke the worktree's new Codex check-i18n-semantics entry for the seven complete
   pairs. Perform source-to-target proposition checks, including conditions,
   default values, ordering, exclusions, command/capability completeness and
   natural target prose. Repair real issues; record per-language outcomes and
   applicable deterministic checks in `translation-review.md`.

Covers: REQ-002, REQ-003, REQ-004, REQ-005, NFR-001;
Design: Shared instructions; translation execution and semantic assessment.

### Phase 3: Verify and close the complete feature

6. Close all enumerated test scenarios against meaningful assertions; run targeted
   and full existing suite, native entry check, distribution check, Python lint,
   declared Markdown lint, seven-language mechanics checks, English-source hash,
   change-scope and whitespace checks. Build package archives to verify maintained
   resources remain excluded. Record exact commands/results in verification.md.
7. Complete the fresh isolated feature defect gate after a green baseline,
   validating schema/maintenance/coverage and independently verifying findings
   before any repairs. Retain required review state externally. Only a valid
   complete-feature PASS closes implementation.

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, NFR-001;
Design: All components and evidence boundaries.

## Dependencies

Infrastructure tests → mechanics → instructions/native entries → translations
→ semantic assessment/repairs → final checks → isolated complete-feature review.

## Risks and Validation

| Risk | Validation |
|------|------------|
| New internal entries accidentally become public | Fresh init/distribution and package boundary checks |
| Extra native entries loosely exempted from checks | Paired current-byte expectations; stale/missing/unknown tests |
| Symlink or hard-link output redirection | Preflight rejection tests and no-write snapshots |
| Wrong root/site language filename mapping | Real inventory argument tests for all seven languages and aliases |
| Mechanical counts hide wrong meaning | Explicit per-language proposition assessment |
| Broken translated anchors or copied old content | Target navigation/link checks and complete English-source comparison |

## Coverage

| Spec | Phase / Unit | Design |
|------|--------------|--------|
| REQ-001 | Phase 1; Phase 3 | Instructions; native rendering/checks |
| REQ-002 | Phases 1–3 | Inventory/checker; shared instructions |
| REQ-003 | Phases 1–3 | Checker; translation and semantic assessment |
| REQ-004 | Phase 2; Phase 3 | Translation and semantic assessment |
| REQ-005 | Phases 1–3 | Maintainer boundary and source preservation |
| NFR-001 | All phases | Shared guidance and evidence |
