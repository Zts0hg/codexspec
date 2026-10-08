# Tasks: Review Convergence

**Input**: `.codexspec/specs/2026-1008-1952ti-review-convergence/` (`requirements.md`, `spec.md`, `design.md`, `plan.md`)
**Tests**: Required. Plan Decision 1: contract tests are written or adjusted first for templates, and red-green-refactor applies to the Python CLI change. Documentation tasks use deterministic checks.
**Organization**: Follows the plan's Phases 0–7. Tasks editing the same file are sequential; `[P]` marks tasks that can run concurrently once their declared dependencies are done.

## Format: `[ID] [P?] Description`

Each task lists its outcome, paths, dependencies, `Covers: REQ-xxx; Plan: <phase/unit>`, and for testable tasks an individually identifiable **Test Scenarios** list (`TS-<task>.<n>`).

---

## Phase 0: Baseline

- [x] **T001** Establish the green baseline in the feature worktree: run `uv sync --dev`, `uv run pytest`, `uv run ruff check src/ tests/` and record the results.
  - **Note**: the dev tools are an optional-dependency extra, so the working commands are `uv sync --extra dev` and `.venv/bin/python -m pytest`; `uv sync --dev` leaves pytest out of the venv and `uv run pytest` then falls back to a global interpreter. Baseline: 1836 passed, 54 skipped; ruff clean.
  - **Depends on**: —
  - **Verification**: All three commands succeed; any pre-existing failure is recorded before changes begin.
  - **Covers**: NFR-004; Plan: Phase 0

---

## Phase 1: Configuration Surface

- [x] **T002** Write failing tests for `review.decided_by` in a new `tests/test_config_review_decided_by.py`, modeled on `tests/test_config_auto_next.py`, and observe the expected failures (red).
  - **Depends on**: T001
  - **Covers**: REQ-010, REQ-005; Plan: Phase 1 (plan Decision 5)
  - **Test Scenarios**:
    - TS-2.1 Read: no `review` section → `reviewer`.
    - TS-2.2 Read: `review.decided_by: ask` → `ask`; `review.decided_by: reviewer` → `reviewer`.
    - TS-2.3 Read: an invalid stored value (e.g. `maybe`) is reported as invalid, not as `reviewer`.
    - TS-2.4 Write: when no `review:` mapping exists, one is created and the rest of the file (other sections and comments) is preserved.
    - TS-2.5 Write: an existing value is updated in place without a duplicate key.
    - TS-2.6 CLI: `codexspec config --decided-by ask` writes `ask` and confirms the new value.
    - TS-2.7 CLI: `codexspec config --decided-by foo` exits with an error, lists the accepted values, and leaves the file unchanged.
    - TS-2.8 CLI: bare `codexspec config` prints the effective `review.decided_by`: `reviewer` when absent, an invalid notice when invalid.

- [x] **T003** Implement the `review.decided_by` read/write helpers next to the `workflow.*` helpers in `src/codexspec/__init__.py`, add the `--decided-by` option to `codexspec config` (with a docstring example and the effective-value line in the bare display), until T002 passes (green); run `uv run ruff check src/`.
  - **Depends on**: T002
  - **Verification**: `uv run pytest tests/test_config_review_decided_by.py tests/test_config_auto_next.py tests/test_config_auto_distill.py` passes.
  - **Covers**: REQ-005, REQ-010; Plan: Phase 1 (helpers and CLI option)
  - **Test Scenarios**: TS-2.1 – TS-2.8 (implemented by this task)

- [x] **T004** [P] Add a `review.decided_by` entry and set flow to `templates/commands/config.md`, following the existing `auto_distill` flow and the `request_user_input` schema note, with a contract test in `tests/test_config_review_decided_by.py` written first.
  - **Depends on**: T003 (T004 appends tests to the module whose full run is T003's verification; starting after T003 keeps that run unaffected by T004's in-progress tests)
  - **Covers**: REQ-010; Plan: Phase 1 (`/codexspec:config` entry)
  - **Test Scenarios**:
    - TS-4.1 `config.md` offers `review.decided_by` with values `reviewer` and `ask`, and states that `reviewer` is the default.
    - TS-4.2 `config.md` writes the key under a `review:` mapping, updating in place when present.
    - TS-4.3 `config.md` does not accept values other than `reviewer` and `ask`.

**Checkpoint**: `review.decided_by` can be set and displayed through the CLI and `/codexspec:config`.

---

## Phase 2: `review-code` Template (Producer)

> **Implementation note:** `review-code`, `config`, `implement-tasks`, and `debug` are opted-in commands; see the plan's correction under Relevant Repository Constraints. Each template task:
>
> 1. edits `internal/command_templates/sources/<command>.md`;
> 2. runs `uv run python internal/command_template_fragments.py --write`;
> 3. regenerates the tracked `.claude/commands/codexspec/` and `.agents/skills/` copies with the existing integration generators;
> 4. passes `--check-distribution`.

All tasks edit `templates/commands/review-code.md` sequentially. Contract assertions go first into `tests/test_review_code_templates.py`.

- [x] **T005** Arguments and resolver boundary:
  - add `--decided-by reviewer|ask` and `--incremental-from <fingerprint>` to the frontmatter `argument-hint`, `## Usage Hints`, and the Defect-Gate Argument Contract;
  - state in the Resolver Compatibility Gate that the coordinator validates and strips both modifiers before invoking the resolver;
  - add both modifiers to the `review-code` `argument-hint` (and to the `description` if it enumerates modifiers) in all eight `templates/translations/{en,zh-CN,ja,ko,de,es,fr,pt-BR}.json`;
  - update `REVIEW_CODE_HINTS`, `REVIEW_CODE_DESCRIPTIONS` and the token list in `tests/test_translation_files.py`.
  - **Depends on**: T001
  - **Covers**: REQ-005, REQ-009; Plan: Phase 2 (Arguments)
  - **Test Scenarios**:
    - TS-5.1 The frontmatter `argument-hint` and `## Usage Hints` list `--decided-by reviewer|ask` and `--incremental-from <fingerprint>`.
    - TS-5.2 `--incremental-from` is valid only with the default target or `--committed`; with `--uncommitted`, `--commit`, or `--audit` it is an argument error.
    - TS-5.3 `--decided-by` is valid with every defect-gate selector; with `--audit` it is an argument error; any value other than `reviewer`/`ask` is an `INCONCLUSIVE` argument error.
    - TS-5.4 A duplicated `--decided-by` or `--incremental-from` is an argument error.
    - TS-5.5 The Resolver Compatibility Gate states that the coordinator validates and removes both modifiers before invoking the resolver, and that the resolver is unchanged.
    - TS-5.6 Each of the eight catalogs' `review-code` `argument-hint` contains both modifiers and equals its pinned constant.

- [x] **T006** Decision mode and scenario-decision items (design C4):
  - mode resolution;
  - the `ask`-only classification at Finding Admission;
  - pending-item verdict rules;
  - treating confirmed `OUT`/`CON` decisions as authoritative context.
  - **Depends on**: T005
  - **Covers**: REQ-006, REQ-007, REQ-008, NFR-001, NFR-002; Plan: Phase 2 (Decision mode and scenario items)
  - **Test Scenarios**:
    - TS-6.1 Mode resolution order is `--decided-by` → `review.decided_by` → `reviewer`.
    - TS-6.2 An invalid `review.decided_by` value is an `INCONCLUSIVE` argument error and is never treated as `ask`.
    - TS-6.3 In `reviewer` mode there is no scenario classification, and the existing Finding Admission rules remain verbatim.
    - TS-6.4 In `ask` mode, a finding whose trigger depends on inputs or environments outside the real operating context becomes a scenario-decision item with a `context_basis` grounded in requirements, constitution, and project instructions.
    - TS-6.5 A pending item adds a blocking gap `scenario decision <id>`; the verdict is never `PASS`; it is `FAIL` only when an admitted finding exists, otherwise `INCONCLUSIVE`.
    - TS-6.6 Confirmed requirements decisions are authoritative: an accepted scenario (`OUT`) is not reported again; a violated "fix" decision (`CON`) is an ordinary admitted finding.
    - TS-6.7 `review-code.md` still contains no `/codexspec:debug` reference.
    - TS-6.8 The human report's Scope section states the resolved decision mode (design C3).

- [x] **T007** Schema `3` envelope (design Decision 1): bump the example and rules to `"schema_version": "3"`; add `review_scope`, `decided_by`, `scenario_decisions` and their validation rules while keeping every schema `2` rule.
  - **Depends on**: T006
  - **Covers**: REQ-003, REQ-005, REQ-007; Plan: Phase 2 (Schema `3` envelope)
  - **Test Scenarios**:
    - TS-7.1 The example envelope has `"schema_version": "3"` and the members `review_scope`, `decided_by`, `scenario_decisions`.
    - TS-7.2 The rules require `review_scope.since` to be non-null exactly when `kind = "incremental"`.
    - TS-7.3 The rules require `scenario_decisions` to be empty when `decided_by = "reviewer"`.
    - TS-7.4 The rules require every pending item to have a matching blocking gap that is also an outgoing follow-up source, and forbid `PASS` with a pending item.
    - TS-7.5 Existing schema `2` rules remain present: the closed top-level object, finding/gap count agreement, the PASS conditions, and the null-fingerprint rules.

- [x] **T008** Incremental review (design C1, C2, Decisions 2, 3, 5):
  - state store root and results layout;
  - prior-record loading and mismatch rules;
  - delta, affected-partition and affected-contract computation;
  - delegation contents;
  - carried-coverage merge;
  - incremental envelope semantics;
  - non-terminal incremental `PASS`.
  - **Depends on**: T007
  - **Covers**: REQ-001, REQ-002, REQ-003, REQ-014; Plan: Phase 2 (Incremental review)
  - **Test Scenarios**:
    - TS-8.1 The state store root is under `$XDG_CACHE_HOME` (fallback `$HOME/.cache`) or `%LOCALAPPDATA%`, keyed by repository; result directories are named `sha256-<hex>`; `inventory.json` records per-entry digests and `partition_ids`.
    - TS-8.2 Missing or unreadable prior records, or a mismatch in repository, selector, feature, `base_ref`, or `merge_base_sha`, produce an `INCONCLUSIVE` argument error that tells the caller to run a complete review.
    - TS-8.3 The delta is the changed, added, removed, or renamed entries by digest; affected partitions come from the delta entries' `partition_ids`; affected contracts come from those partitions' `contract_ids`.
    - TS-8.4 The fresh reviewer receives the delta, affected-contract obligations, incoming follow-ups, and full current evidence, but no prior coverage evidence, statuses, or findings.
    - TS-8.5 Unchanged entries outside affected partitions keep prior coverage, marked `carried`.
    - TS-8.6 In an incremental result, the target block describes the full target, `review_coverage` lists only this round's records, and accounting runs over the merged records.
    - TS-8.7 An incremental `PASS` is stated to be target-limited and never terminal.
    - TS-8.8 Without `--incremental-from`, the complete review protocol is unchanged.
    - TS-8.9 The fresh reviewer may trace beyond the computed scope and must report any finding it discovers; carried coverage never suppresses an admitted finding (spec edge case "Incremental round finds a defect in an unchanged area").

- [x] **T009** Verification environment (design C8): the mirror contract, the output rule, and the topology rule.
  - **Depends on**: T008
  - **Covers**: REQ-013, REQ-014, REQ-015; Plan: Phase 2 (Verification environment)
  - **Test Scenarios**:
    - TS-9.1 The mirror reproduces the selected state: the manifest `HEAD` for default/`--committed`/`--uncommitted`, the selected commit for `--commit`, plus the selected uncommitted content.
    - TS-9.2 Ignored files the checks need, such as installed dependencies, are copied rather than linked, and nothing is installed.
    - TS-9.3 The mirror has its own Git metadata from a local clone, never shares the original's Git directory, and never uses `git worktree add`.
    - TS-9.4 Full inventory, coverage records, and logs go to the results directory; the conversation carries only the six-section report and the envelope.
    - TS-9.5 The coordinator in the caller's context is the only spawner; reviewers and specialists are its direct children; reviewers never spawn reviewers.

- [x] **T010** Host-explicit isolation (design C9) in Reviewer Isolation.
  - **Depends on**: T009
  - **Covers**: REQ-016; Plan: Phase 2 (Isolation per host)
  - **Test Scenarios**:
    - TS-10.1 Codex: reviewers and specialists are spawned with `spawn_agent` and `fork_turns: "none"`; `fork_turns: "all"` and any conversation fork are forbidden.
    - TS-10.2 Claude Code: reviewers are delegated to a fresh non-fork `Task`/`Agent` subagent; forks that inherit the conversation are forbidden.
    - TS-10.3 The task message contains only the listed isolation items: no prior finding prose, implementation reasoning, or repair-success claims.

**Checkpoint**: `uv run pytest tests/test_review_code_templates.py tests/test_translation_files.py tests/test_debug_template.py` passes.

---

## Phase 3: Eval Harness (Schema `3` Consumer)

- [x] **T011** [P] Update `parse_review_result` in `tests/evals/review_code/run_eval.py` to schema `3`, and update `tests/test_review_code_eval.py`: tests first, canned envelopes moved to schema `3`, and `tests/evals/review_code/README.md` adjusted if it names the result schema.
  - **Depends on**: T007 (can run in parallel with T008–T010)
  - **Covers**: REQ-003, REQ-007, NFR-001; Plan: Phase 3
  - **Test Scenarios**:
    - TS-11.1 A valid schema `3` complete-review envelope parses.
    - TS-11.2 Schema `1` and schema `2` envelopes are rejected explicitly.
    - TS-11.3 An envelope missing `review_scope`, `decided_by`, or `scenario_decisions` is rejected.
    - TS-11.4 `kind: "incremental"` with `since: null`, or `kind: "complete"` with a non-null `since`, is rejected.
    - TS-11.5 `decided_by: "reviewer"` with a non-empty `scenario_decisions` is rejected.
    - TS-11.6 A pending item without a matching blocking gap or follow-up source is rejected.
    - TS-11.7 `verdict: "PASS"` with a pending item is rejected.
    - TS-11.8 A valid `ask`-mode `INCONCLUSIVE` result with a pending item, its gap, and its follow-up parses.
    - TS-11.9 The canned adapter run records a parsed schema `3` result for a case.

---

## Phase 4: `implement-tasks` Template (Consumer and Loop Driver)

All tasks edit `templates/commands/implement-tasks.md` sequentially; contract assertions go first into `tests/test_sdd_workflow_templates.py` (and `tests/test_debug_template.py` for T016).

- [x] **T012** §7.2 validation and §7.6 success for schema `3`.
  - **Depends on**: T007
  - **Covers**: REQ-003, NFR-001; Plan: Phase 4 (§7.2 validation)
  - **Test Scenarios**:
    - TS-12.1 §7.2 requires schema version `3` and explicitly rejects `1` and `2`.
    - TS-12.2 §7.2 validates `review_scope`, `decided_by`, and `scenario_decisions` with the design's cross-field rules.
    - TS-12.3 Success requires `review_scope.kind = "complete"` and no pending scenario item, in addition to the existing conditions.
    - TS-12.4 Existing validation text remains: exactly one `<review-code-result>`, the neutral follow-up retention rules (updated to schema `3`), and "Prose cannot override".

- [x] **T013** §7.1/§7.5 round policy (design C6, rules 1–5).
  - **Depends on**: T012, T008
  - **Covers**: REQ-001, REQ-003, REQ-004, REQ-009, NFR-003; Plan: Phase 4 (round policy)
  - **Test Scenarios**:
    - TS-13.1 The first review is complete, using `/codexspec:review-code --feature <feature-dir>`.
    - TS-13.2 After a green repair set, the next review is incremental with `--incremental-from <last valid result fingerprint>`.
    - TS-13.3 After an incremental `PASS`, a complete review runs; only a complete `PASS` satisfies §7.6.
    - TS-13.4 After a complete `FAIL`, the loop returns to incremental review.
    - TS-13.5 A prior-record-unavailable or mismatch argument error triggers a complete review and is neither a transient retry nor a failed round.
    - TS-13.6 The loop never passes `--decided-by`, keeps the neutral follow-up handoff, and introduces no round cap (the existing progress guards are unchanged).

- [x] **T014** Loop ledger in the out-of-repository state store (design C1, C6).
  - **Depends on**: T013
  - **Covers**: REQ-011; Plan: Phase 4 (Loop ledger)
  - **Test Scenarios**:
    - TS-14.1 The ledger lives at `loops/<feature-id>.json` under the review state store root, outside the repository.
    - TS-14.2 The ledger holds the round list (fingerprint, kind, verdict), the last complete fingerprint, verified findings with `root_cause_class`, retained obligations, and pending scenario items.
    - TS-14.3 "Do not create repository-local review-state files" remains.

- [x] **T015** Scenario-decision flow (design C5).
  - **Depends on**: T014
  - **Covers**: REQ-007, REQ-008; Plan: Phase 4 (Scenario decisions)
  - **Test Scenarios**:
    - TS-15.1 Results whose blocking gaps include `scenario decision <id>` go to the decision flow before §7.5's transient-retry and persistent-`INCONCLUSIVE` handling.
    - TS-15.2 The user is asked with the host structured-question tool; when that tool is unavailable, in plain text, ending the turn and resuming from the ledger.
    - TS-15.3 Accept is recorded as a new `OUT-xxx` and fix as a new `CON-xxx` in `requirements.md`, each with a Confirmation Log line.
    - TS-15.4 A "fix" decision is handled as a verified finding.
    - TS-15.5 Under `CODEXSPEC_AUTO_DEV_DELEGATION`, no prompt is issued; a stop state naming the pending items is returned.

- [x] **T016** Escalation trip (c) in `## Systematic Debugging Escalation`.
  - **Depends on**: T014
  - **Covers**: REQ-011, REQ-012; Plan: Phase 4 (Escalation trip)
  - **Test Scenarios**:
    - TS-16.1 Trip (c): a verified finding whose `root_cause_class` matches a class recorded in an earlier round invokes `/codexspec:debug` with the whole class as one defect.
    - TS-16.2 The wording of trips (a) and (b) is unchanged (existing `tests/test_debug_template.py` assertions pass).
    - TS-16.3 The four-phase discipline text is still absent from `implement-tasks.md`.
    - TS-16.4 No `auto_debug` key appears.
    - TS-16.5 Classification never removes a finding from repair: a finding that matches no recorded class is repaired through the normal §7.4 path (spec edge case "Root-cause class ambiguous").

---

## Phase 5: `debug` Template

- [x] **T017** [P] Class-level intake in `templates/commands/debug.md` (design C7), with assertions added first to `tests/test_debug_template.py`.
  - **Depends on**: T016 (both add assertions to `tests/test_debug_template.py`; can still run in parallel with T015)
  - **Covers**: REQ-012; Plan: Phase 5
  - **Test Scenarios**:
    - TS-17.1 Symptom Intake accepts a recurring defect class together with its known instances.
    - TS-17.2 For a class, the Fix phase requires one uniform fix and a codebase-wide search for every location of the class, each covered by a regression check.
    - TS-17.3 The Architecture Gate (≥3 failed fixes) applies to the class.
    - TS-17.4 The existing four-phase, iron-law, and architecture-gate assertions still pass.

**Checkpoint**: `uv run pytest tests/test_sdd_workflow_templates.py tests/test_debug_template.py tests/test_review_code_eval.py` passes.

---

## Phase 6: Documentation

- [ ] **T018** Update the English docs:
  - the `docs/en/user-guide/commands.md` review-code section: schema `3`, `--decided-by`, `--incremental-from`, incremental and complete rounds, scenario decisions, keeping every test-enforced marker and syntax;
  - `docs/en/reference/configuration.md`: `review.decided_by`;
  - `docs/en/reference/cli.md`: `codexspec config --decided-by`;
  - `tests/test_review_code_docs.py`: expect `schema_version: "3"` and the new flags.
  - **Depends on**: T003, T010, T015, T016
  - **Verification**: the English parametrizations pass. Select them by node ID, because `-k en` also matches the substring in "documents" and would select every locale:

    ```
    uv run pytest "tests/test_review_code_docs.py::test_localized_guide_documents_defect_gate_and_audit_migration[en-readme_and_term0]" "tests/test_review_code_docs.py::test_readme_summary_describes_gate_not_default_scorecard[en-readme_and_term0]"
    ```

    Then confirm the pages read correctly.
  - **Covers**: NFR-004, REQ-005, REQ-010; Plan: Phase 6 (English docs)

- [ ] **T019** Run `/codexspec:translate-docs` for the three changed English pages across the seven locales (zh, ja, ko, de, es, fr, pt-BR); check each locale's test-enforced strings.
  - **Depends on**: T018
  - **Verification**: `uv run pytest tests/test_review_code_docs.py tests/test_translation_files.py` passes for all locales.
  - **Covers**: NFR-004; Plan: Phase 6 (localization, plan Decision 3)

- [ ] **T020** [P] Update `CLAUDE.md`:
  - add a "Review Convergence" architecture section covering incremental rounds, `review.decided_by`, schema `3`, the state store, and cross-round escalation;
  - change the debug section's "two trip conditions" to three;
  - list `review.decided_by` with the configuration keys.

  Adjust the README review-code row only if its summary has become inaccurate.
  - **Depends on**: T010, T015, T016, T017
  - **Verification**: The content matches the shipped behavior; `uv run pytest tests/test_review_code_docs.py -k readme_summary` passes. The run is scoped to the README rows so T019's in-progress locale guides cannot affect it.
  - **Covers**: NFR-004; Plan: Phase 6 (CLAUDE.md)

---

## Phase 7: Verification and Acceptance

- [ ] **T021** Run the full suite, lint, and the docs build: `uv run pytest`, `uv run ruff check src/ tests/`, and `mkdocs build --strict` when available locally (otherwise the `docs.yml` CI).
  - **Depends on**: T003, T004, T010, T011, T015, T016, T017, T019, T020
  - **Verification**: All green.
  - **Covers**: NFR-004; Plan: Phase 7

- [ ] **T022** [P] Consistency check:
  - Grep the source-of-truth paths (`templates/`, `src/`, `tests/`, `docs/`, `CLAUDE.md`, root `README*.md`) for ``schema version `2` ``, `schema-v2`, and `"schema_version": "2"`. Nothing may still require, emit, or document schema `2` as current.
  - Expected exceptions: rejection rules and rejection fixtures for `1`/`2`, and the eval case files' independent case schema `"1"`.
  - Excluded paths: `.codexspec/specs/` and the derived `.claude/commands/codexspec/` and `.agents/skills/` copies.
  - Confirm `git diff --stat origin/main -- scripts/` is empty.
  - **Depends on**: T021
  - **Verification**: The grep shows only expected exceptions; the resolver is unchanged.
  - **Covers**: NFR-002, NFR-004; Plan: Phase 7 (consistency grep)

- [ ] **T023** [P] Rendering check in a scratch project:
  - run `uv tool install --force .`, then `codexspec init --ai both` in a temporary directory;
  - inspect the rendered `review-code`, `implement-tasks`, `debug`, and `config` in both `.claude/commands/codexspec/` and `.agents/skills/` forms, including localized `argument-hint` for one non-English language.
  - **Depends on**: T021
  - **Verification**: Both forms contain the new rules (`/codexspec:` versus `$codexspec:` syntax) and the isolation instructions.
  - **Covers**: REQ-016, NFR-004; Plan: Phase 7 (rendering check, plan Decision 4)

- [ ] **T024** Manual acceptance in a scratch repository with a seeded defect. Run it from a linked worktree, on Codex and Claude Code where available, and record each scenario's outcome.
  - **Depends on**: T023
  - **Covers**: REQ-001–REQ-016, NFR-001–NFR-003; Plan: Phase 7 (manual acceptance)
  - **Test Scenarios**:
    - TS-24.1 A complete `FAIL`, then repair, then an incremental round whose scope is the delta plus affected partitions, then a complete `PASS` (spec US1 scenarios 1–2).
    - TS-24.2 A new defect in the final complete review leads to repair, then an incremental round, then another complete review (spec US1 scenario 3).
    - TS-24.3 With `review.decided_by: ask` and an out-of-context trigger: a scenario prompt appears; "accept" records an `OUT-xxx`, which is not raised again in the next round (spec US2 scenarios 2 and 4).
    - TS-24.4 With `--decided-by reviewer` overriding a configured `ask`, no scenario items appear (spec US2 scenario 5).
    - TS-24.5 A root-cause class recurring in a later round triggers the trip (c) escalation into `debug` (spec US3 scenario 2).
    - TS-24.6 A check that needs Git metadata and installed dependencies passes in the mirror, and the original repository's Git state is unchanged (spec US4 scenario 1).
    - TS-24.7 Default configuration: no scenario items; admission behavior unchanged (spec US2 scenario 1).

- [ ] **T025** [P] Optional live eval: run `python tests/evals/review_code/run_eval.py --cases tests/evals/review_code/cases --host codex` (or `--host claude`) on two or three cases and confirm the schema `3` envelopes parse.
  - **Depends on**: T021
  - **Verification**: The recorded results show parsed verdicts with no parse failures.
  - **Covers**: REQ-003, NFR-002; Plan: Phase 7 (optional live eval)

---

## Dependency Summary

```
T001 ─┬─ T002 → T003 → T004 [P]
      └─ T005 → T006 → T007 ─┬─ T008 → T009 → T010
                             ├─ T011 [P]
                             └─ T012 ─┐
                     (T008) ──────────┴→ T013 → T014 ─┬─ T015
                                                      └─ T016 → T017 [P]
T018 (T003, T010, T015, T016) → T019
T020 [P] (T010, T015, T016, T017)
T021 (all implementation and docs tasks) ─┬─ T022 [P]
                                          ├─ T023 [P] → T024
                                          └─ T025 [P]
```

The graph is acyclic: same-file tasks are chained, and every dependency precedes its dependent.

## Coverage

### Plan Units → Tasks

| Plan unit | Tasks |
|---|---|
| Phase 0 Baseline | T001 |
| Phase 1 config tests / helpers and CLI / `/codexspec:config` entry | T002, T003, T004 |
| Phase 2 Arguments (incl. translation catalogs) | T005 |
| Phase 2 Decision mode and scenario items | T006 |
| Phase 2 Schema `3` envelope | T007 |
| Phase 2 Incremental review | T008 |
| Phase 2 Verification environment | T009 |
| Phase 2 Isolation per host | T010 |
| Phase 2 "no `/codexspec:debug` reference" check | T006 (TS-6.7) |
| Phase 3 Eval harness | T011 |
| Phase 4 §7.2 validation / round policy / ledger / scenario decisions / escalation trip | T012, T013, T014, T015, T016 |
| Phase 5 debug | T017 |
| Phase 6 English docs / localization / CLAUDE.md | T018, T019, T020 |
| Phase 7 suite / consistency grep / rendering / acceptance / optional live eval | T021, T022, T023, T024, T025 |

### Requirements → Tasks

| Requirement | Tasks | Scenarios |
|---|---|---|
| REQ-001 | T008, T013, T024 | TS-8.3–8.5, TS-13.2, TS-24.1 |
| REQ-002 | T008, T024 | TS-8.1, TS-8.3, TS-8.5, TS-24.1 |
| REQ-003 | T007, T008, T011, T012, T013 | TS-7.2, TS-8.7, TS-11.4, TS-12.3, TS-13.3 |
| REQ-004 | T013, T024 | TS-13.4, TS-24.2 |
| REQ-005 | T003, T005, T006, T007, T018 | TS-2.1–2.8, TS-5.1, TS-5.3, TS-6.1, TS-6.8, TS-7.1 |
| REQ-006 | T006, T024 | TS-6.3, TS-24.7 |
| REQ-007 | T006, T007, T011, T015 | TS-6.4, TS-6.5, TS-7.3, TS-7.4, TS-11.5–11.8, TS-15.1 |
| REQ-008 | T006, T015, T024 | TS-6.6, TS-15.3, TS-15.4, TS-24.3 |
| REQ-009 | T005, T013 | TS-5.5, TS-13.6 |
| REQ-010 | T002, T003, T004, T018 | TS-2.4–2.8, TS-4.1–4.3 |
| REQ-011 | T014, T016 | TS-14.2, TS-16.1 |
| REQ-012 | T016, T017, T024 | TS-16.1, TS-16.5, TS-17.1–17.3, TS-24.5 |
| REQ-013 | T009, T024 | TS-9.1–9.3, TS-24.6 |
| REQ-014 | T008, T009 | TS-8.1, TS-8.6, TS-9.4 |
| REQ-015 | T009 | TS-9.5 |
| REQ-016 | T010, T023 | TS-10.1–10.3 |
| NFR-001 | T006, T008, T011, T012, T016 | TS-6.5, TS-8.9, TS-11.7, TS-12.3, TS-16.5 |
| NFR-002 | T006, T022, T024, T025 | TS-6.3, TS-24.7 |
| NFR-003 | T013 | TS-13.6 |
| NFR-004 | T001, T018–T023 | (deterministic verification) |

### Unmapped Tasks

None. T001, T021, T022, T023 and T025 are implementation-support verification tasks required by plan Phases 0 and 7.
