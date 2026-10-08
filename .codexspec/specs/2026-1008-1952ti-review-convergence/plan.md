# Implementation Plan: Review Convergence

**Related Spec**: `.codexspec/specs/2026-1008-1952ti-review-convergence/spec.md`
**Related Design**: `.codexspec/specs/2026-1008-1952ti-review-convergence/design.md`
**Confirmed Requirements**: `.codexspec/specs/2026-1008-1952ti-review-convergence/requirements.md`
**Created**: 2026-10-08
**Status**: Draft

## Context

This plan builds the confirmed design (components C1–C10, Decisions 1–5 in `design.md`): incremental intermediate review rounds with a complete final round, the `review.decided_by` decision mode with scenario-decision items, cross-round root-cause escalation into `debug`, review-environment robustness, and host-explicit reviewer isolation. Almost all behavior lives in Markdown command templates whose contracts are pinned by string-contract tests; the only Python change is the `codexspec config` option for `review.decided_by`. The envelope schema moves from `2` to `3` (design Decision 1), which ripples into the eval harness parser, the template tests, and the eight localized command guides.

## Goals / Non-Goals

**Goals:**

- Deliver every REQ/NFR in `spec.md` through the design components, with the full test suite green.
- Keep default-configuration review behavior unchanged apart from the additive schema `3` members (NFR-002).

**Non-Goals:**

- No review round cap (OUT-001).
- No change to the resolver scripts (`scripts/bash/review-context.sh`, `scripts/powershell/review-context.ps1`) or the manifest schema (design C3 resolver boundary, Decision 3).
- No hand edits to derived `.claude/commands/codexspec/` or `.agents/skills/codexspec-*/` copies (CON-003); they are regenerated at release.
- No `CHANGELOG.md` edit in this feature; release notes are produced at release time by `/codexspec:release-notes`.

## Tech Stack

- **Language**: Python 3.11+ (CLI only); Markdown command templates
- **Framework**: Typer + Rich (`codexspec config`)
- **Testing**: pytest (string-contract template tests, CLI tests, eval-harness parser tests); ruff
- **Docs**: MkDocs i18n (`docs/<locale>/`), localized via the maintainer command `/codexspec:translate-docs`

## Relevant Repository Constraints

- Source of truth for commands is `templates/commands/`; derived copies are never hand-edited (constitution, Self-bootstrap).
- `implement-tasks` already forbids repository-local review-state files (`templates/commands/implement-tasks.md:355`); C1 stores state outside the repository.
- `review-code` passes its arguments to the resolver, which rejects any unknown `--*` argument (`scripts/bash/review-context.sh:115-117`).
- Schema `2` is pinned by: `templates/commands/review-code.md`, `templates/commands/implement-tasks.md`, `tests/test_review_code_templates.py`, `tests/test_sdd_workflow_templates.py` (e.g. "schema version `2`", "retained originating schema-v2 result"), `tests/evals/review_code/run_eval.py` (`parse_review_result`), `tests/test_review_code_eval.py`, and `tests/test_review_code_docs.py`, which asserts `schema_version: "2"` in the review-code section of `docs/<locale>/user-guide/commands.md` for all eight locales (en, zh, ja, ko, de, es, fr, pt-BR).
- `tests/test_debug_template.py` requires that `review-code` never references `/codexspec:debug`, that the four-phase discipline text lives only in `debug.md`, that trips (a) and (b) keep their wording, and that no `auto_debug` key exists.
- Localized command metadata (`description`, `argument-hint`) is rendered from `templates/translations/<language>.json` (eight catalogs); `tests/test_translation_files.py` pins the `review-code` hint and description exactly per language.
- `/codexspec:config` already uses the host structured-question tool with a `request_user_input` schema note (`templates/commands/config.md:153-170`).
- Config writes follow the comment-preserving helpers next to `_read_auto_next` / `_write_auto_next` (`src/codexspec/__init__.py:1423-1460`); bare `codexspec config` prints effective values before the raw file (`src/codexspec/__init__.py:862-863`).
- Docs translations are produced manually with `/codexspec:translate-docs` (`.github/workflows/docs-i18n.yml` no longer auto-translates).

- **Correction found during implementation:** `review-code`, `config`, `implement-tasks`, and `debug` are opted-in commands. Their authoritative sources are `internal/command_templates/sources/<command>.md`; `templates/commands/<command>.md` is generated with `uv run python internal/command_template_fragments.py --write`. The tracked derived copies under `.claude/commands/codexspec/` and `.agents/skills/` must also match the generators: `--check-distribution` (CI, release, and `tests/test_command_template_fragments.py`) fails on stale output. Every template unit therefore edits the internal source, runs `--write`, and regenerates the derived copies with the existing integration generators. This supersedes plan Decision 4's "synced at release" and the derived-copy exclusion in the Phase 7 consistency grep.

## Plan-Level Decisions

### Decision 1: Contract tests first for templates, TDD for Python

**Context**: Template behavior is verified by string-contract tests; the CLI change is ordinary code.
**Options Considered**:

1. Edit templates, then adjust tests to match.
2. Write or adjust the failing contract assertions first, then edit the template until they pass; use red-green-refactor for the Python CLI change.
**Decision**: Option 2.
**Rationale**: It keeps each template change anchored to a requirement and prevents tests from merely mirroring whatever text was written.
**Trade-offs**: Contract tests check the presence of rules, not LLM behavior; behavioral confidence comes from the manual acceptance run (Phase 7).

### Decision 2: Order phases by dependency, keeping schema `3` producer and consumers adjacent

**Context**: The schema `3` envelope is produced by `review-code` and consumed by `implement-tasks` and the eval harness. Docs tests are independent of the templates.
**Options Considered**:

1. One big change across all files.
2. Config → review-code (producer) → eval harness → implement-tasks and debug (consumers) → docs → acceptance.
**Decision**: Option 2. Intermediate states inside the branch may be inconsistent across files (for example, `review-code` emitting `3` while docs still say `2`), but each phase ends with the suite green, and the branch merges only after Phase 7.
**Trade-offs**: Cross-file consistency is guaranteed only at the end; the Phase 7 consistency check covers it.

### Decision 3: Localize docs with `/codexspec:translate-docs`, not by hand

**Context**: Eight locales are test-enforced for the review-code section; configuration and CLI references are also localized.
**Decision**: Edit `docs/en/` first, then run `/codexspec:translate-docs` for the changed pages so each locale is regenerated consistently; review the test-enforced strings (`schema_version: "3"`, flag syntax, marker comments) in every locale afterwards.
**Alternatives**: Hand-editing seven locales — rejected: error-prone and inconsistent with the project's translation workflow.
**Trade-offs**: Translation output needs a quick review per locale.

### Decision 4: Validate rendering in a scratch project, not in this repository

**Context**: Derived copies must not be hand-edited; rendering for both hosts still needs a check.
**Decision**: After template changes, install the working tree (`uv tool install --force .`) and run `codexspec init --ai both` in a temporary directory; inspect the rendered `review-code`, `implement-tasks`, `debug`, and `config` commands and skills there. The repository's own derived copies are synced at release.
**Trade-offs**: The repository's dogfooded commands lag until release.

### Decision 5: A focused test module for the new config key

**Decision**: Add `tests/test_config_review_decided_by.py`, mirroring `tests/test_config_auto_next.py` (read helper: absent, valid, invalid, malformed; write helper: create `review:` mapping, update in place, preserve comments; CLI: set, invalid value, effective-value display).

## Risks / Trade-offs

| Risk | Impact | Mitigation |
|---|---|---|
| `review-code.md` (1,190 lines) grows further | More reviewer context load and instruction dilution | Add one compact Incremental Review subsection and one Decision Mode subsection; reuse existing rules by reference; no duplicated text |
| String tests cannot prove LLM behavior | A template can pass tests yet be misread by a host | Phase 7 manual acceptance on both hosts; optional live eval run |
| Translated docs drift on test-enforced strings | Docs tests fail per locale | Run `tests/test_review_code_docs.py` after translation; fix locale strings directly when only literal tokens differ |
| Mirror recipe differs on linked worktrees (design advisory) | Mirror creation fails, rounds become `INCONCLUSIVE` | Phase 7 includes a run from a linked worktree, which is this repository's own layout |
| Schema bump breaks an unnoticed consumer | Validation rejects results | Repository grep confirms only `review-code`, `implement-tasks`, and the eval harness consume the envelope; Phase 7 greps again for `schema_version` and `schema-v2` |

## Implementation Phases

### Phase 0: Baseline

- [ ] Run `uv sync --dev`, `uv run pytest`, and `uv run ruff check src/ tests/` in the feature worktree and record the green baseline. — **Covers**: NFR-004 (implementation support); Design: —

### Phase 1: Configuration surface

- [ ] Add failing tests in `tests/test_config_review_decided_by.py` (plan Decision 5). — **Covers**: REQ-010; Design: C10
- [ ] Implement read and write helpers for `review.decided_by` (`reviewer` | `ask`; absent on read → `reviewer`; an invalid stored value is reported as invalid with the accepted values, never shown as `reviewer`, matching `review-code`'s argument-error treatment in design C3; invalid input on write → error) next to the `workflow.*` helpers in `src/codexspec/__init__.py`; add `--decided-by` to `codexspec config`, with an "Effective review.decided_by" line in the bare display and an example in the docstring. — **Covers**: REQ-005, REQ-010; Design: C10, C3
- [ ] Add a `/codexspec:config` menu entry and a set flow for `review.decided_by` in `templates/commands/config.md`, following the existing `auto_distill` flow and the `request_user_input` schema note. — **Covers**: REQ-010; Design: C10

### Phase 2: `review-code` template (producer)

Edit `templates/commands/review-code.md`; each unit first adds or adjusts assertions in `tests/test_review_code_templates.py`.

- [ ] **Arguments**: add `--decided-by reviewer|ask` and `--incremental-from <fingerprint>` to the frontmatter `argument-hint`, `## Usage Hints`, and the Defect-Gate Argument Contract (validity matrix, duplicates, the `--audit` conflict); in the Resolver Compatibility Gate, state that the coordinator validates and strips its own modifiers before invoking the resolver. Because installed commands render localized metadata from `templates/translations/<language>.json`, also add both modifiers to the `review-code` `argument-hint` (and to the `description` if it enumerates modifiers) in all eight catalogs (`en`, `zh-CN`, `ja`, `ko`, `de`, `es`, `fr`, `pt-BR`), and update `REVIEW_CODE_HINTS` / `REVIEW_CODE_DESCRIPTIONS` and the token list in `tests/test_translation_files.py` (`TestReviewCodeTranslationContract`). — **Covers**: REQ-005, REQ-009; Design: C3
- [ ] **Decision mode and scenario items**: resolve the mode (flag → `review.decided_by` → `reviewer`; invalid → `INCONCLUSIVE` argument error); in Finding Admission, add the `ask`-only scenario classification with the operating-context basis (requirements, constitution, project instructions); add the pending-item rules (blocking gap `scenario decision <id>`, never `PASS`, `FAIL` only with an admitted finding); state that confirmed `OUT`/`CON` decisions are authoritative context. — **Covers**: REQ-006, REQ-007, REQ-008, NFR-001, NFR-002; Design: C4
- [ ] **Schema `3` envelope**: bump `schema_version` to `"3"`; add `review_scope`, `decided_by`, and `scenario_decisions` with their validation rules (`since` iff incremental, empty in `reviewer` mode, matching gap and follow-up per pending item); keep every schema `2` rule otherwise. — **Covers**: REQ-003, REQ-005, REQ-007; Design: Decision 1
- [ ] **Incremental review**:
  - state store root and results layout (`sha256-<hex>` directory names; `report.md`, `envelope.json`, `inventory.json` with per-entry digests and `partition_ids`, `coverage.json`);
  - prior-record loading and mismatch rules (repository, selector, feature, `base_ref`, `merge_base_sha`);
  - delta, affected-partition, and affected-contract computation;
  - delegation contents (no prior evidence or statuses);
  - carried-coverage merge, incremental envelope semantics, and "incremental `PASS` is never terminal".

  **Covers**: REQ-001, REQ-002, REQ-003, REQ-014; Design: C1, C2, Decisions 2, 3, 5
- [ ] **Verification environment**: replace the mirror wording with the mirror contract (selected state, ignored dependencies copied rather than linked, independent Git metadata, never sharing the original's Git directory); add the output rule (full records to the results directory; conversation gets the six-section report plus the envelope); add the topology rule (coordinator in the caller's context is the only spawner; depth 1; reviewers never spawn). — **Covers**: REQ-013, REQ-014, REQ-015; Design: C8
- [ ] **Isolation per host**: add the concrete Codex rule (`spawn_agent` with `fork_turns: "none"`; never `"all"`) and the Claude Code rule (fresh non-fork `Task`/`Agent` subagent), and the task-message content restriction, to Reviewer Isolation. — **Covers**: REQ-016; Design: C9
- [ ] Confirm `templates/commands/review-code.md` still does not reference `/codexspec:debug` (`tests/test_debug_template.py`). — **Covers**: NFR-004; Design: —

### Phase 3: Eval harness (schema `3` consumer)

- [ ] Update `parse_review_result` in `tests/evals/review_code/run_eval.py` to require schema `3`, rejecting `1` and `2` explicitly; validate `review_scope`, `decided_by`, and `scenario_decisions` and their cross-field rules (pending item ↔ blocking gap ↔ follow-up source; pending → non-`PASS`; `reviewer` → empty items). — **Covers**: REQ-003, REQ-007, NFR-001; Design: Decision 1
- [ ] Update `tests/test_review_code_eval.py` fixtures and canned envelopes to schema `3`; add parser tests for incremental and scenario-decision envelopes (valid and contradictory cases); update `tests/evals/review_code/README.md` if it names the schema. — **Covers**: REQ-003, REQ-007; Design: Decision 1

### Phase 4: `implement-tasks` template (schema `3` consumer, loop driver)

Edit `templates/commands/implement-tasks.md`; adjust `tests/test_sdd_workflow_templates.py` and `tests/test_debug_template.py` first.

- [ ] **§7.2 validation**: require schema `3`, rejecting `1` and `2`; validate the new members; success additionally requires `review_scope.kind = "complete"` and no pending scenario item (§7.6). — **Covers**: REQ-003, NFR-001; Design: Decision 1, C6
- [ ] **§7.1 / §7.5 round policy**:
  - complete first review;
  - after a green repair set, incremental with `--incremental-from <last valid result fingerprint>`;
  - after an incremental `PASS`, a complete review;
  - after a complete `FAIL`, back to incremental;
  - fall back to a complete review on the prior-record-unavailable or mismatch argument error;
  - keep the fixed `--feature` invocation and never pass `--decided-by`;
  - keep the neutral follow-up handoff.

  **Covers**: REQ-001, REQ-003, REQ-004, REQ-009; Design: C6
- [ ] **Loop ledger**: store the round list, the last complete fingerprint, verified findings with `root_cause_class`, retained obligations, and pending scenario items in the C1 ledger, `loops/<feature-id>.json` (outside the repository). — **Covers**: REQ-011; Design: C1, C6
- [ ] **Scenario decisions**:
  - route `scenario decision <id>` gaps to the decision flow before §7.5 `INCONCLUSIVE` handling;
  - ask with the host tool, or in plain text and end the turn, resuming from the ledger;
  - record accept as `OUT-xxx` and fix as `CON-xxx` with a Confirmation Log line in `requirements.md`;
  - treat a "fix" as a verified finding;
  - under `CODEXSPEC_AUTO_DEV_DELEGATION`, return a stop state instead of prompting.

  **Covers**: REQ-007, REQ-008; Design: C5
- [ ] **Escalation trip (c)**: in `## Systematic Debugging Escalation`, add a third trip (a verified finding whose `root_cause_class` matches a class recorded in an earlier round) that invokes `/codexspec:debug` with the class as one defect, leaving the wording of trips (a) and (b) unchanged. — **Covers**: REQ-011, REQ-012; Design: C6

### Phase 5: `debug` template

- [ ] Extend Symptom Intake to accept a recurring defect class with known instances; in Phase 4 (Fix), require one uniform fix plus a codebase-wide search for every location of the class, each with a regression check; state that the Architecture Gate applies to the class. Add assertions to `tests/test_debug_template.py`. — **Covers**: REQ-012; Design: C7

### Phase 6: Documentation

- [ ] Update `docs/en/user-guide/commands.md` (review-code section): schema `3`, `--decided-by`, `--incremental-from`, incremental and complete rounds, scenario decisions, while keeping all existing test-enforced markers and syntax. Update `docs/en/reference/configuration.md` (`review.decided_by`) and `docs/en/reference/cli.md` (`codexspec config --decided-by`). Update `tests/test_review_code_docs.py` to expect `schema_version: "3"` and the new flags. — **Covers**: NFR-004, REQ-005, REQ-010; Design: C3, C10, Decision 1
- [ ] Run `/codexspec:translate-docs` for the three changed English pages across the seven locales (plan Decision 3); verify the test-enforced strings per locale. — **Covers**: NFR-004; Design: —
- [ ] Update `CLAUDE.md`: add a "Review Convergence" architecture section (incremental rounds, `review.decided_by`, schema `3`, state store, cross-round escalation); change the debug section's "two trip conditions" to three; mention the new config key alongside `workflow.*`. Update the README review-code row only if its summary becomes inaccurate (it must keep "defect gate" and `--audit`). — **Covers**: NFR-004; Design: all

### Phase 7: Verification and acceptance

- [ ] Run `uv run pytest`, `uv run ruff check src/ tests/`, and `mkdocs build --strict` (when available locally; otherwise rely on the `docs.yml` CI). — **Covers**: NFR-004; Design: —
- [ ] Consistency grep over the source-of-truth paths (`templates/`, `src/`, `tests/`, `docs/`, `CLAUDE.md`, root `README*.md`): nothing still requires, emits, or documents schema `2` as current (``schema version `2` ``, `schema-v2`, `"schema_version": "2"`). Expected exceptions: explicit rejection rules and rejection-test fixtures for schemas `1`/`2`, and the eval case files' independent case schema `"1"`. Excluded paths: historical `.codexspec/specs/` artifacts. The derived `.claude/commands/codexspec/` and `.agents/skills/` copies are regenerated with the templates (see the correction under Relevant Repository Constraints) and are covered by `--check-distribution`. Also confirm the resolver scripts are unchanged (`git diff --stat origin/main -- scripts/`). — **Covers**: NFR-002, NFR-004; Design: Decision 1, C3
- [ ] Rendering check in a scratch project (plan Decision 4) for both hosts. — **Covers**: REQ-016, NFR-004; Design: C9
- [ ] Manual acceptance in a scratch repository with a seeded defect, run from a linked worktree, on both Codex and Claude Code where available:
  1. a complete `FAIL`, then repair → incremental round (scope limited to delta and affected partitions) → complete `PASS`;
  2. `review.decided_by: ask` with an out-of-context trigger → scenario prompt → accept → recorded `OUT-xxx` → not re-raised;
  3. a recurring root-cause class across rounds → trip (c) escalation into `debug`;
  4. a mirror run that needs Git metadata and installed dependencies;
  5. default configuration → no scenario items and today's admission behavior.

  **Covers**: REQ-001–REQ-016, NFR-001–NFR-003; Design: C1–C9
- [ ] Optional: a live eval run (`tests/evals/review_code/run_eval.py --host codex|claude`) on two or three cases to confirm schema `3` envelopes parse. — **Covers**: REQ-003, NFR-002; Design: Decision 1

## Requirements Coverage

| Spec Requirement | Design Component | Plan Coverage |
|---|---|---|
| REQ-001 | C2, C6, Decision 2 | Phase 2 (Incremental review), Phase 4 (round policy), Phase 7 acceptance 1 |
| REQ-002 | C1, C2, Decisions 2, 3, 5 | Phase 2 (Incremental review), Phase 7 acceptance 1 |
| REQ-003 | C2, C6, Decision 1 | Phase 2 (Schema `3`, Incremental review), Phase 3, Phase 4 (§7.2, round policy) |
| REQ-004 | C6 | Phase 4 (round policy) |
| REQ-005 | C3, Decision 1 | Phase 1, Phase 2 (Arguments, Schema `3`), Phase 6 |
| REQ-006 | C3, C4 | Phase 2 (Decision mode), Phase 7 acceptance 5 |
| REQ-007 | C4, Decision 1 | Phase 2 (Decision mode, Schema `3`), Phase 3, Phase 4 (Scenario decisions) |
| REQ-008 | C4, C5, Decision 4 | Phase 2 (Decision mode), Phase 4 (Scenario decisions), Phase 7 acceptance 2 |
| REQ-009 | C3 | Phase 2 (Arguments), Phase 4 (round policy: never pass `--decided-by`) |
| REQ-010 | C10 | Phase 1, Phase 6 |
| REQ-011 | C1, C6 | Phase 4 (Loop ledger, Escalation trip) |
| REQ-012 | C6, C7 | Phase 4 (Escalation trip), Phase 5, Phase 7 acceptance 3 |
| REQ-013 | C8 | Phase 2 (Verification environment), Phase 7 acceptance 4 |
| REQ-014 | C1, C2, C8, Decision 5 | Phase 2 (Incremental review, Verification environment) |
| REQ-015 | C8 | Phase 2 (Verification environment) |
| REQ-016 | C9, Decision 2 | Phase 2 (Isolation per host), Phase 7 rendering check |
| NFR-001 | C2, C4, C6 | Phase 2 (Decision mode), Phase 3, Phase 4 (§7.2) |
| NFR-002 | C3, Decision 1 | Phase 2 (Decision mode), Phase 7 consistency grep and acceptance 5 |
| NFR-003 | C6 | Phase 4 (round policy adds no cap) |
| NFR-004 | All | Phases 0–7 (source templates only; derived copies untouched; docs and tests updated) |
