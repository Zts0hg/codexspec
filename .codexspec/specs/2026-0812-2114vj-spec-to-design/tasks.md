# Tasks: spec-to-design

**Feature ID**: `2026-0812-2114vj`
**Authority**: `requirements.md` → `spec.md` → `plan.md`

**Test module placement**: template/init assertions live in a new
`tests/test_spec_to_design_templates.py` (mirroring `tests/test_debug_template.py` /
`tests/test_profile_templates.py`); command-count assertions live in the existing
`tests/commands/test_installer.py` and `tests/test_cli.py`. Each testable task's Test Scenarios
map one-to-one to assertions in these modules.

---

## Phase 1 — New design-stage artifacts

### T1.1 — Create `design-template.md`

- **Outcome**: `templates/docs/design-template.md` exists with the fixed core + on-demand
  optional sections (PLD-004).
- **Paths**: `templates/docs/design-template.md`
- **Covers**: REQ-002, REQ-003, REQ-006; Plan: C1
- **Dependencies**: none
- **Testable**: yes
- **Test Scenarios**:
  - S1.1.1 (happy): the file exists and contains the fixed-core headings — Architecture &
    Components, Key Design Decisions, Requirements Coverage.
  - S1.1.2 (structure): optional sections (Data Models, API / Interface Contracts, Sequence &
    Data Flow, Cross-Cutting Design, Risks & Trade-offs) are present but marked
    include-when-relevant (`*(include if …)*`).
  - S1.1.3 (traceability): the template demonstrates the `Covers: REQ-` field on components/
    decisions and contains a Requirements Coverage table.

### T1.2 — Create `spec-to-design.md` command

- **Outcome**: `templates/commands/spec-to-design.md` exists, mirroring `spec-to-plan.md`
  structure (PLD-002), producing `design.md` from `design-template.md`.
- **Paths**: `templates/commands/spec-to-design.md`
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-013, REQ-014; Plan: C2
- **Dependencies**: T1.1 (references the design template), T1.3 (review loop targets it)
- **Testable**: yes
- **Test Scenarios**:
  - S1.2.1 (happy): the file exists, is English, and contains a `## Language Preference` section.
  - S1.2.2 (review loop): it invokes `/codexspec:review-design <feature-dir>/design.md` in an
    automatic review loop.
  - S1.2.3 (auto_next): its Auto-Next Chain Advance invokes `/codexspec:spec-to-plan
    <feature-dir>`.
  - S1.2.4 (authority): its authority order ranks requirements and spec above design-level
    decisions (design cannot override product intent).
  - S1.2.5 (intent guard): it contains Stop Conditions preventing changes to confirmed product
    intent (REQ-014).
  - S1.2.6 (no branch check): it contains no Git Branch Safety Check section.

### T1.3 — Create `review-design.md` command

- **Outcome**: `templates/commands/review-design.md` exists, mirroring `review-plan.md`, saving
  `review-design.md`, with the verbatim Compatibility Score formula (PLD-003).
- **Paths**: `templates/commands/review-design.md`
- **Covers**: REQ-005, REQ-013; Plan: C3
- **Dependencies**: none
- **Testable**: yes
- **Test Scenarios**:
  - S1.3.1 (happy): the file exists, is English, and contains a `## Language Preference` section.
  - S1.3.2 (report path): it saves `<feature-dir>/review-design.md`.
  - S1.3.3 (score formula): it contains the Compatibility Score formula text identical to the
    other review commands (the `max(80, 100 - 3 × Minor)` / `max(50, 79 - …)` / `max(0, 49 - …)`
    lines).
  - S1.3.4 (authority): its authority order ranks requirements and spec above design-level
    decisions.

---

## Phase 2 — Downstream pipeline edits

### T2.1 — Retarget `generate-spec` auto_next to `spec-to-design`

- **Outcome**: `generate-spec.md` Auto-Next Chain Advance invokes `/codexspec:spec-to-design`.
- **Paths**: `templates/commands/generate-spec.md`
- **Covers**: REQ-007; Plan: C4
- **Dependencies**: T1.2
- **Testable**: yes
- **Test Scenarios**:
  - S2.1.1 (happy): `generate-spec.md`'s auto_next invocation names `spec-to-design`.
  - S2.1.2 (negative): `generate-spec.md`'s auto_next no longer names `spec-to-plan` as its
    direct next stage.

### T2.2 — Narrow `spec-to-plan` to implementation planner

- **Outcome**: `spec-to-plan.md` reads `design.md`; role = implementation planner; plan
  components use `Covers: REQ-xxx; Design: <design component>`; authority order gains `design`.
- **Paths**: `templates/commands/spec-to-plan.md`
- **Covers**: REQ-008, REQ-013; Plan: C5
- **Dependencies**: T1.2
- **Testable**: yes
- **Test Scenarios**:
  - S2.2.1 (input): `spec-to-plan.md` lists `design.md` among its inputs.
  - S2.2.2 (authority): authority order lists `design.md` below `spec` and above plan-level
    decisions.
  - S2.2.3 (notation): it specifies the plan `Covers: REQ-xxx; Design:` pointer notation.
  - S2.2.4 (role): the role/framing is implementation planning, not "constrained technical
    designer".

### T2.3 — Slim the plan templates

- **Outcome**: `plan-template-detailed.md` and `plan-template-simple.md` have design-only
  sections removed (PLD-005), retaining implementation-planning sections.
- **Paths**: `templates/docs/plan-template-detailed.md`, `templates/docs/plan-template-simple.md`
- **Covers**: REQ-008; Plan: C6
- **Dependencies**: T1.1 (design content now lives in the design template)
- **Testable**: yes
- **Test Scenarios**:
  - S2.3.1 (detailed slimmed): `plan-template-detailed.md` no longer contains the design-only
    section headings (Architecture Overview, Component Structure, Data Models, API Contracts).
  - S2.3.2 (retained): `plan-template-detailed.md` still contains Implementation Phases and
    Requirements Coverage.
  - S2.3.3 (simple slimmed): `plan-template-simple.md` no longer contains an Architecture section
    housing design content.

### T2.4 — `plan-to-tasks` consumes design

- **Outcome**: `plan-to-tasks.md` reads `design.md` as context; authority order gains `design`;
  task notation unchanged.
- **Paths**: `templates/commands/plan-to-tasks.md`
- **Covers**: REQ-009, REQ-013; Plan: C7
- **Dependencies**: none
- **Testable**: yes
- **Test Scenarios**:
  - S2.4.1 (input): `plan-to-tasks.md` lists `design.md` among its inputs.
  - S2.4.2 (authority): `design.md` is listed among the Read inputs after `spec.md` and before
    `plan.md`.

### T2.5 — Deepen `analyze` traceability chain

- **Outcome**: `analyze.md` chain is `confirmed → REQ → design → plan → task`; remediation covers
  `design.md` and never edits `requirements.md`.
- **Paths**: `templates/commands/analyze.md`
- **Covers**: REQ-010; Plan: C8
- **Dependencies**: none
- **Testable**: yes
- **Test Scenarios**:
  - S2.5.1 (chain): `analyze.md`'s traceability chain text includes `design` between `REQ` and
    `plan`.
  - S2.5.2 (inputs): `analyze.md` lists `design.md` among its loaded inputs.
  - S2.5.3 (invariant): `analyze.md` still states it never modifies `requirements.md`.

### T2.6 — `implement-tasks` treats design as authority

- **Outcome**: `implement-tasks.md` reads `design.md`; authority order gains `design`.
- **Paths**: `templates/commands/implement-tasks.md`
- **Covers**: REQ-011, REQ-013; Plan: C9
- **Dependencies**: none
- **Testable**: yes
- **Test Scenarios**:
  - S2.6.1 (input): `implement-tasks.md` lists `design.md` among its input documents.
  - S2.6.2 (authority): authority order lists `design.md` below `spec` and above `plan`.

### T2.7 — Insert design into the review commands' authority

- **Outcome**: `review-plan.md` authority order gains `design` and its Fidelity pass is
  design-aware; `review-tasks.md` authority order gains `design`. `review-spec.md` unchanged.
- **Paths**: `templates/commands/review-plan.md`, `templates/commands/review-tasks.md`
- **Covers**: REQ-013; Plan: C15
- **Dependencies**: none
- **Testable**: yes
- **Test Scenarios**:
  - S2.7.1 (review-plan authority): `review-plan.md` authority order places `design` below `spec`.
  - S2.7.2 (review-plan fidelity): `review-plan.md` fidelity pass references design coverage
    (plan covers design).
  - S2.7.3 (review-tasks authority): `review-tasks.md` authority order places `design` below
    `spec`.

---

## Phase 3 — Registration, docs, tests

### T3.1 — Register commands in the installer

- **Outcome**: `get_commands_metadata()` includes `spec-to-design` and `review-design`
  (category `core`, placed per PLD-001); docstring `core (9)→(11)` / `Total 21→23`; inline
  `# Core Commands (9)→(11)`.
- **Paths**: `src/codexspec/commands/installer.py`
- **Covers**: REQ-012; Plan: C10
- **Dependencies**: T1.2, T1.3
- **Testable**: yes
- **Test Scenarios**:
  - S3.1.1 (present): `get_commands_metadata()` contains entries named `spec-to-design` and
    `review-design` with `category == "core"` and correct `file_name`.
  - S3.1.2 (placement): `spec-to-design` is ordered between `generate-spec` and `spec-to-plan`;
    `review-design` between `review-spec` and `review-plan`.
  - S3.1.3 (count): total metadata length is 23; core count is 11.

### T3.2 — Update command-count assertions

- **Outcome**: the command-count assertions in `tests/commands/test_installer.py` and
  `tests/test_cli.py` reflect the new totals (core 11 / total 23).
- **Paths**: `tests/commands/test_installer.py`, `tests/test_cli.py`
- **Covers**: REQ-012; Plan: C11
- **Dependencies**: T3.1
- **Testable**: yes (self-verifying — the assertions are the test)
- **Test Scenarios**:
  - S3.2.1 (installer count): `test_installer.py` asserts the updated total/core counts and
    passes.
  - S3.2.2 (cli count): `test_cli.py`'s command-count assertion passes with the new total.

### T3.3 — Add template/init test module

- **Outcome**: `tests/test_spec_to_design_templates.py` implements the Phase 1/2 template Test
  Scenarios plus an init-copy assertion.
- **Paths**: `tests/test_spec_to_design_templates.py`
- **Covers**: REQ-001..006, REQ-013 (verification); Plan: C13
- **Dependencies**: T1.1, T1.2, T1.3, T2.1–T2.7
- **Testable**: yes (this task is the tests)
- **Test Scenarios**:
  - S3.3.1 (init copy): `codexspec init <tmp> --force` produces
    `.codexspec/templates/docs/design-template.md` (use `--force` — `tmp_path` pre-exists, per
    profile `P-2026-0812-14054p-1`).
  - S3.3.2 (aggregate): the module houses assertions S1.1.*, S1.2.*, S1.3.*, S2.1–S2.7.*.

### T3.4 — Update `README*.md`

- **Outcome**: every `README*.md` (8 files) lists `spec-to-design` and `review-design` rows,
  translated per language.
- **Paths**: `README.md`, `README.de.md`, `README.es.md`, `README.fr.md`, `README.ja.md`,
  `README.ko.md`, `README.pt-BR.md`, `README.zh-CN.md`
- **Covers**: REQ-012; Plan: C12
- **Dependencies**: none
- **Testable**: no (documentation)
- **Verification**: deterministic check — each `README*.md` contains both `spec-to-design` and
  `review-design`.

### T3.5 — Update `CLAUDE.md`

- **Outcome**: `CLAUDE.md` documents the design stage (architecture section, command tables,
  implementation status).
- **Paths**: `CLAUDE.md`
- **Covers**: NEED-007 documentation support; Plan: C14
- **Dependencies**: none
- **Testable**: no (project documentation)
- **Verification**: deterministic check — `CLAUDE.md` mentions `spec-to-design` and
  `review-design` and the deepened chain.

---

## Phase 4 — Verification

### T4.1 — Full-suite green + guard checks

- **Outcome**: the full test suite is green; no changes under `.claude/commands/` or
  `.agents/skills/`; no changes to either constitution.
- **Paths**: repository-wide
- **Covers**: NFR-001, NFR-002; Plan: Phase 4
- **Dependencies**: all prior tasks
- **Testable**: no (verification/guard task)
- **Verification**: `uv run pytest` green; `git diff --name-only` for the feature shows no
  `.claude/commands/`, `.agents/skills/`, `.codexspec/memory/constitution.md`, or
  `_get_default_constitution()` changes.

---

## Coverage Table

| Plan component | Task(s) |
|---|---|
| C1 design-template | T1.1 |
| C2 spec-to-design | T1.2 |
| C3 review-design | T1.3 |
| C4 generate-spec | T2.1 |
| C5 spec-to-plan | T2.2 |
| C6 plan templates slim | T2.3 |
| C7 plan-to-tasks | T2.4 |
| C8 analyze | T2.5 |
| C9 implement-tasks | T2.6 |
| C15 review-plan + review-tasks | T2.7 |
| C10 installer | T3.1 |
| C11 count assertions | T3.2 |
| C13 template/init tests | T3.3 |
| C12 READMEs | T3.4 |
| C14 CLAUDE.md | T3.5 |
| Phase 4 verification | T4.1 |

| REQ / NFR | Task(s) |
|---|---|
| REQ-001 | T1.2, T3.3 |
| REQ-002 | T1.1, T1.2, T3.3 |
| REQ-003 | T1.1, T1.2, T3.3 |
| REQ-004 | T1.2, T3.3 |
| REQ-005 | T1.3, T3.3 |
| REQ-006 | T1.1, T3.3 |
| REQ-007 | T2.1 |
| REQ-008 | T2.2, T2.3 |
| REQ-009 | T2.4 |
| REQ-010 | T2.5 |
| REQ-011 | T2.6 |
| REQ-012 | T3.1, T3.2, T3.3, T3.4 |
| REQ-013 | T1.2, T1.3, T2.2, T2.4, T2.6, T2.7 |
| REQ-014 | T1.2 |
| NFR-001 | T4.1 |
| NFR-002 | T4.1 |
| NFR-003 | T1.2, T1.3 |

## Scenario-to-Task Map (testable tasks)

| Task | Scenarios |
|---|---|
| T1.1 | S1.1.1, S1.1.2, S1.1.3 |
| T1.2 | S1.2.1–S1.2.6 |
| T1.3 | S1.3.1–S1.3.4 |
| T2.1 | S2.1.1, S2.1.2 |
| T2.2 | S2.2.1–S2.2.4 |
| T2.3 | S2.3.1–S2.3.3 |
| T2.4 | S2.4.1, S2.4.2 |
| T2.5 | S2.5.1–S2.5.3 |
| T2.6 | S2.6.1, S2.6.2 |
| T2.7 | S2.7.1–S2.7.3 |
| T3.1 | S3.1.1–S3.1.3 |
| T3.2 | S3.2.1, S3.2.2 |
| T3.3 | S3.3.1, S3.3.2 |

## Unmapped Tasks

None. Every task maps to a plan component and upstream REQ/NFR.
