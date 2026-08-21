# Tasks: reverse-spec

**Feature Branch**: `2026-0818-2053p5-reverse-spec`
**Created**: 2026-08-20
**Input**: `requirements.md` · `spec.md` · `design.md` (C1–C11) · `plan.md` (Phases 1–4, Decisions 1–5)

Task groups follow the approved plan's four phases. Every task states its outcome,
exact paths, dependencies, and traceability. Testable tasks enumerate individually
identifiable test scenarios; documentation and regeneration tasks carry
deterministic verification instead.

---

## Phase 1 — Command template

### T1.1 Author `templates/commands/reverse-spec.md`

- **Outcome**: the command template exists and realizes design components C1–C10.
- **Path**: `templates/commands/reverse-spec.md` (new)
- **Dependencies**: none
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007,
  REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016,
  REQ-017, REQ-018, REQ-019, REQ-021, NFR-001, NFR-004, NFR-005, NFR-006;
  **Plan**: Phase 1
- **Task type**: documentation-class artifact. Per plan Decision 1 it is authored
  before its contract tests and verified deterministically here; T2.1 then locks
  the discipline.

Required content, by design component:

| Section | Realizes |
|---|---|
| Frontmatter: `description`, `argument-hint: "[path]"`, `allowed-tools` modeled on `onboard.md` | C1 |
| `## Language Preference` referencing `language.interaction` and `language.document`, never `language.commit`, **plus the verbatim-evidence exception** — `reconcile.md`'s `location`/`evidence` quote code and baseline verbatim and MUST NOT be translated (the convention `onboard.md` and `distill.md` already carry) | C1, NFR-001, REQ-010 |
| `## Role and Operating Model` — three mutually exclusive modes | C1 |
| `## Mode Resolution` — bare run short-circuits **before** any baseline lookup; a `[path]` resolving to the repository root is that same bare run; a `[path]` resolving **outside** the repository is reported and refused; the survey workspace is found by the `slices.md` marker and **never** by directory name; containment is decided on the **resolved** path so an in-repo symlink pointing out of the tree is refused; the slice path is normalized on both the write and read side **including symlink resolution**, stated as a rule (one directory by any spelling = one slice) rather than a closed list; only an **exact** match selects a mode, several exact matches ask, a **covering** (proper-ancestor) match asks rather than reconciling and, when chosen, re-enters the status gate so it can never reconcile an unconfirmed baseline; only an explicit file-level `Status: confirmed` counts, anything missing or unreadable reads as open; a nested-inside workspace is disclosed as an overlap in **every** mode, not only generate; unconfirmed baseline refuses | C2, Decision 8 |
| `## Slice and Workspace` — `Slice:` header field recorded in normalized form on **slice** artifacts only (the survey workspace carries none and is identified by `slices.md`); the repository root is not a slice; the directory name is a human convenience and never an identifier; workspace directory `.codexspec/specs/<id>-<slice>/` reusing the existing id convention, created without any git branch | C3, Decision 8 |
| `## Generate Mode` — `spec.md` + `design.md` (scaled) + thin all-`open` `requirements.md` stub | C4 |
| `## Overview Mode` — `<id>-overview` workspace with thin architecture `design.md` + `slices.md`; no `spec.md`, no `reconcile.md` | C5 |
| `## Inference Marking and Confirmation` — file-level `Status: inferred/open`, `[inferred]` markers, promotion by `Status: confirmed` + Confirmation Log; no new command | C6 |
| `## Reconcile Mode` — baseline is confirmed spec (+ design when present); three drift kinds; severity by impact; both-side evidence; direction suggested never applied; `needs-your-judgment` when intent does not decide | C7 |
| `## Reconcile Report` — the `reconcile.md` structure and per-item fields | C8 |
| `## Scan Discipline` — reference to `/codexspec:onboard`, stating **both** overrides on the referenced text: (a) `onboard`'s "stream findings to the store / write each convention as confirmed" directive does **not** carry over — this command writes nothing to `.codexspec/profile/` and streams into its own workspace artifacts instead (OUT-002, REQ-017); (b) `[path]` is the slice boundary here, not a scan narrower | C9 |
| `## Boundaries` — read-only on code, writes confined to the workspace, never `.codexspec/profile/`, never source/tests/git/constitution/baseline; rewrites only what the current run wrote, so a resumed draft is appended to and never overwritten, with `reconcile.md` the single announced regeneration | C10 |
| `## Mode Resolution` / `## Slice and Workspace` / `## Overview Mode` — workspace creation writes its identifying artifact (`spec.md` with the `Slice:` header, or `slices.md`) as the creating act, and a resume completes only what is missing | C2, C3, C5, Decision 7 |

- **Must NOT contain**: an `## Auto-Next Chain Advance` section, an
  `## Automatic Distillation` section, or any reference to `language.commit`.
- **Deterministic verification**: read the file against `design.md` C1–C10 and
  confirm every row above is present; confirm the three prohibited items are
  absent; confirm the file is authored in English.

---

## Phase 2 — Contract tests

### T2.1 Create `tests/test_reverse_spec_template.py`

- **Outcome**: the template's discipline is locked by contract tests, all passing.
- **Path**: `tests/test_reverse_spec_template.py` (new)
- **Dependencies**: T1.1
- **Covers**: REQ-002, REQ-005, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011,
  REQ-012, REQ-013, REQ-015, REQ-016, REQ-017, REQ-018, REQ-019, REQ-021, NFR-001;
  **Plan**: Phase 2
- **Style**: follow `tests/test_onboard_template.py` — a `read_command()` helper
  over `templates/commands/`, and frontmatter assertions via
  `codexspec.translator.extract_frontmatter_fields`.
- **Constraint (plan Decision 3)**: every asserted span must be free of inline
  markdown emphasis (`**`, `*`, backticks inside the span), per pitfall
  `P-2026-0813-1606fz-1`.

**Test Scenarios**:

1. **S1 — frontmatter contract**: `description` is non-empty and
   `argument-hint` contains `[path]`. *(REQ-001, REQ-019)*
2. **S2 — language regime**: the template references `language.interaction` and
   `language.document`, and does **not** reference `language.commit`. *(REQ-021,
   NFR-001)*
3. **S3 — bare run short-circuits**: mode resolution states that a run with no
   path performs the survey and never reconciles, ordered before any baseline
   lookup. *(REQ-015, REQ-002)*
4. **S4 — generate when no baseline**: mode resolution states that a slice with no
   matching workspace enters generate mode. *(REQ-002)*
5. **S5 — ambiguous match asks the user**: multiple matching workspaces prompt a
   selection rather than silently choosing the newest. *(REQ-002)*
6. **S6 — unconfirmed baseline refuses**: an existing workspace whose artifacts
   are still open blocks reconciliation and writes no report. *(REQ-008)*
7. **S7 — baseline is confirmed spec/design only**: the template names confirmed
   `spec.md`/`design.md` as the comparison baseline and excludes
   `requirements.md`, `plan.md`, and `tasks.md`. *(REQ-007)*
8. **S8 — design-absent fallback**: when the confirmed baseline has a spec but no
   design, reconciliation proceeds against the spec alone. *(REQ-007)*
9. **S9 — three drift kinds**: `undocumented-behavior`, `unimplemented-spec`, and
   `semantic-mismatch` are all named. *(REQ-009)*
10. **S10 — severity by impact**: severity is assigned from the item's impact and
    explicitly not fixed by its kind. *(REQ-011)*
11. **S11 — report gates nothing**: the report status and severities are stated to
    be non-gating with no pass/fail verdict. *(REQ-011, REQ-018)*
12. **S12 — both-side evidence**: a `semantic-mismatch` item requires evidence
    quoted from both the code and the baseline. *(REQ-009, REQ-010)*
13. **S13 — direction never guessed**: direction reasoning appeals to confirmed
    requirements, and `needs-your-judgment` is used when intent does not decide.
    *(REQ-013)*
14. **S14 — report only**: the suggested direction is explicitly never applied and
    reconciliation modifies nothing. *(REQ-012)*
15. **S15 — report structure**: the `reconcile.md` per-item fields `kind`,
    `severity`, `location`, `evidence`, `direction`, and `status` are all
    documented. *(REQ-010)*
16. **S16 — inferred marking**: generated artifacts carry a file-level
    `inferred/open` status and state they are not a baseline until confirmed.
    *(REQ-005)*
17. **S17 — safety boundary**: the template states it is read-only on the
    codebase, confines writes to the feature workspace, and never writes
    `.codexspec/profile/`. *(REQ-017)*
18. **S18 — scan discipline referenced**: the template points at
    `/codexspec:onboard` for the scan discipline rather than restating it.
    *(REQ-016)*
19. **S19 — path-only slice input**: a diff or pull-request range is stated to be
    unsupported as a slice source. *(REQ-019)*
20. **S20 — no pipeline coupling**: the template contains no
    `Auto-Next Chain Advance` section and no `Automatic Distillation` section.
    *(REQ-018)*

---

## Phase 3 — Registration and lockstep count sites

### T3.1 Sweep count sites, then update the three count assertions (red)

- **Outcome**: every stale count site is enumerated up front, and the three
  independent count assertions are updated so the suite fails for the single
  reason that `reverse-spec` is not yet registered.
- **Paths**: `tests/commands/test_installer.py`, `tests/test_cli.py`
- **Dependencies**: none
- **Covers**: REQ-020; **Plan**: Phase 3, Decision 2

Steps:

1. Run one repository-wide sweep for the current counts before editing anything —
   for example `grep -rnE "Total: 25|enhanced \(8\)|Enhanced Commands \(8\)|== 25|== 8|\"25\"" src/ tests/` —
   and record the full site list. This is plan Decision 2; do not discover sites
   one review round at a time.
2. Update `tests/commands/test_installer.py`: total `25 → 26`, enhanced `8 → 9`
   (and the docstring text naming those counts).
3. Update `tests/test_cli.py`: the list-commands output assertion `"25" → "26"`.
4. Add the registry-entry assertions of S3/S4 below.
5. Observe the failures and confirm each is caused by the missing registration.

**Test Scenarios**:

1. **S1 — total command count**: `get_commands_metadata()` returns 26 entries.
   *(REQ-020)*
2. **S2 — enhanced category count**: the `enhanced` category holds 9 commands.
   *(REQ-020)*
3. **S3 — registry entry shape**: an entry named `reverse-spec` exists with
   `category == "enhanced"` and `file_name == "reverse-spec.md"`. *(REQ-020)*
4. **S4 — CLI list output**: `list-commands` output contains `26`. *(REQ-020)*

### T3.2 Register the command and update the count/doc sites (green)

- **Outcome**: T3.1's assertions pass; every count site found in T3.1 step 1 is
  updated in one pass.
- **Path**: `src/codexspec/commands/installer.py`
- **Dependencies**: T3.1
- **Covers**: REQ-020, REQ-021, NFR-003; **Plan**: Phase 3

Steps:

1. Add a `get_commands_metadata()` entry for `reverse-spec` in the `enhanced`
   category, placed adjacent to `onboard`, with `file_name: "reverse-spec.md"` and
   a short zh-CN description.
2. Update the docstring: `enhanced (8) → (9)` and `Total: 25 commands → 26 commands`.
3. Update the inline comment `# Enhanced Commands (8) → (9)`.
4. Do **not** add the command to the `commit_templates` set and do **not** create a
   `templates/translations/*.json` entry.
5. Do **not** modify `.codexspec/memory/constitution.md` or
   `_get_default_constitution()` — the change set stays bounded (NFR-003).
6. Re-run the T3.1 sweep and confirm zero stale counts remain.

- **Deterministic verification**: `uv run ruff check src/` reports no findings —
  in particular the zh-CN description must not push its line past 120 columns.

### T3.3 Add the command row to all 8 README files

- **Outcome**: every README documents `reverse-spec`, translated per language.
- **Paths**: `README.md`, `README.de.md`, `README.es.md`, `README.fr.md`,
  `README.ja.md`, `README.ko.md`, `README.pt-BR.md`, `README.zh-CN.md`
- **Dependencies**: T3.2 (so the row's wording matches the registered description)
- **Covers**: REQ-020; **Plan**: Phase 3, Decision 5
- **Placement**: the **Enhanced Commands** table — verified present in all 8 files
  by their `/codexspec:debug` row — **not** the Self-Evolution table, because
  `reverse-spec` writes SDD artifacts and never `.codexspec/profile/`.
- **Task type**: documentation.
- **Deterministic verification**: all 8 files contain a `/codexspec:reverse-spec`
  row inside the Enhanced Commands table, each in that file's language.

---

## Phase 4 — Derived regeneration and integration verification

### T4.1 Regenerate derived install artifacts

- **Outcome**: the derived Claude command and Codex skill forms exist and match the
  template, with no unrelated repository churn.
- **Command**: `uv run codexspec init . --force --ai both`
- **Expected new paths**: `.claude/commands/codexspec/reverse-spec.md`,
  `.agents/skills/codexspec-reverse-spec/SKILL.md`
- **Dependencies**: T1.1
- **Covers**: NFR-002; **Plan**: Phase 4, Decision 4
- **Task type**: infrastructure/regeneration; the derived files are never
  hand-edited.
- **Deterministic verification**: `git status` shows only this feature's sources
  and the expected derived artifacts; `.codexspec/config.yml` is unchanged, and in
  particular `project.ai` is still `"both"`.

### T4.2 Run the full verification suite

- **Outcome**: a green baseline with no regression, establishing the pre-review
  state.
- **Dependencies**: T1.1, T2.1, T3.2, T3.3, T4.1
- **Covers**: REQ-001..021 and NFR-001..006 as the whole-feature verification
  checkpoint (it gates no requirement individually; it confirms none regressed);
  **Plan**: Verification Strategy
- **Task type**: verification.
- **Deterministic verification**:

| Check | Command | Expectation |
|---|---|---|
| Lint | `uv run ruff check src/ tests/` | 0 findings |
| Targeted | `uv run pytest tests/test_reverse_spec_template.py tests/commands/test_installer.py tests/test_cli.py -q` | green |
| Cross-cutting | `uv run pytest tests/test_sdd_workflow_templates.py tests/test_translation_files.py -q` | green — confirms the language-regime split and that no catalog entry is needed |
| Full suite | `uv run pytest -q` | green, no regression against the measured baseline (1199 passed / 50 skipped on this branch) |

---

## Dependency Summary

```text
T1.1 ──┬── T2.1 ─────────────┐
       └── T4.1 ─────────────┤
                             ├── T4.2
T3.1 ── T3.2 ──┬── T3.3 ─────┤
               └─────────────┘
```

Acyclic. `T1.1` and `T3.1` have no dependencies and may start concurrently `[P]`;
everything else follows its declared predecessors. `T4.2` is the final checkpoint.

## Plan Coverage

| Plan deliverable | Tasks |
|---|---|
| Phase 1 — command template (C1–C10) | T1.1 |
| Phase 2 — contract tests | T2.1 |
| Phase 3 — registration and lockstep count sites (C11) | T3.1, T3.2, T3.3 |
| Phase 4 — derived regeneration and verification | T4.1, T4.2 |
| Decision 1 — template before tests | T1.1 → T2.1 ordering |
| Decision 2 — up-front grep sweep | T3.1 step 1, T3.2 step 6 |
| Decision 3 — emphasis-free assertions | T2.1 constraint |
| Decision 4 — regenerate last with `--ai both` | T4.1 |
| Decision 5 — README Enhanced table | T3.3 |

## Requirements Coverage

| Requirement | Tasks |
|---|---|
| REQ-001 standalone command surface | T1.1, T2.1 (S1) |
| REQ-002 mode auto-detection | T1.1, T2.1 (S3, S4, S5) |
| REQ-003 generate output boundary | T1.1 |
| REQ-004 workspace records its slice | T1.1 |
| REQ-005 derived content marked inferred/open | T1.1, T2.1 (S16) |
| REQ-006 confirmation reuses existing convention | T1.1 |
| REQ-007 baseline is confirmed spec/design only | T1.1, T2.1 (S7, S8) |
| REQ-008 unconfirmed baseline blocks reconcile | T1.1, T2.1 (S6) |
| REQ-009 three drift kinds | T1.1, T2.1 (S9, S12) |
| REQ-010 persistent report plus briefing | T1.1, T2.1 (S12, S15) |
| REQ-011 severity by impact; gates nothing | T1.1, T2.1 (S10, S11) |
| REQ-012 report only, never repair | T1.1, T2.1 (S14) |
| REQ-013 direction appeals to requirements | T1.1, T2.1 (S13) |
| REQ-014 slice unit and workspace creation | T1.1 |
| REQ-015 bare run yields a map | T1.1, T2.1 (S3) |
| REQ-016 scan discipline reused | T1.1, T2.1 (S18) |
| REQ-017 read-only, workspace-confined writes | T1.1, T2.1 (S17) |
| REQ-018 no pipeline coupling | T1.1, T2.1 (S11, S20) |
| REQ-019 path-based slice input only | T1.1, T2.1 (S1, S19) |
| REQ-020 registration and lockstep | T3.1 (S1–S4), T3.2, T3.3 |
| REQ-021 language regime | T1.1, T2.1 (S2), T3.2 |
| NFR-001 English template with Language Preference | T1.1, T2.1 (S2) |
| NFR-002 self-bootstrap discipline | T4.1 |
| NFR-003 two constitutions separate | T3.2 step 5 |
| NFR-004 scales without blocking | T1.1 |
| NFR-005 independently readable output | T1.1 |
| NFR-006 no fabricated intent | T1.1 |

## Scenario-to-Task Mapping

| Task | Scenarios | Count |
|---|---|---|
| T2.1 | S1–S20 | 20 |
| T3.1 | S1–S4 | 4 |

Non-testable tasks (T1.1 documentation-class, T3.3 documentation, T4.1
regeneration, T4.2 verification) carry deterministic verification instead of test
scenarios, per the task rules.

## Unmapped Tasks

None. Every task traces to a plan phase or plan-level decision and to at least one
`REQ`/`NFR`.
