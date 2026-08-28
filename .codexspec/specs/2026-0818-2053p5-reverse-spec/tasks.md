# Tasks: reverse-spec

**Feature Branch**: `2026-0818-2053p5-reverse-spec`
**Created**: 2026-08-20
**Input**: `requirements.md` · `spec.md` · `design.md` (C1–C11,
Decisions 1–9) · `plan.md` (Phases 1–5, Decisions 1–5)

Task groups follow the approved plan's five phases. Every task states its outcome,
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
| Frontmatter: `description`, `argument-hint: "[path]"`, and general `Bash` plus read/write tools required for host-native publication; `## User Input` treats the entire payload as one separately quoted literal path with no shell evaluation | C1, C2, C10 |
| `## Language Preference` referencing `language.interaction` and `language.document`, never `language.commit`, **plus the verbatim-evidence exception** — `reconcile.md`'s `location`/`evidence` quote code and baseline verbatim and MUST NOT be translated, except that detected secret values are redacted | C1, C8, NFR-001, REQ-010, REQ-017 |
| `## Role and Operating Model` — three mutually exclusive modes | C1 |
| `## Mode Resolution` — bare run short-circuits **before** any baseline lookup; an existing path wins over changeset-shaped spelling; a `[path]` resolving to the repository root is that same bare run; a `[path]` resolving **outside** the repository is reported and refused; the survey workspace is found by the `slices.md` marker and **never** by directory name; containment is decided on the **resolved** path so an in-repo symlink pointing out of the tree is refused; the slice path is normalized on both the write and read side **including symlink resolution**, persisted with `/` while preserving exact Unicode code points and never NFC/NFD-normalized or case-folded, rejects control- or secret-bearing identity without echo, and is stated as a rule (one directory by any spelling = one slice) rather than a closed list; every present spec/design artifact in one workspace carries one valid agreeing `Slice:`; only an **exact** match selects a mode, several exact matches ask, a **covering** (proper-ancestor) match asks rather than reconciling and, when chosen, re-enters the status gate so it can never reconcile an unconfirmed baseline; at most one file-level `Status:` line is allowed per present artifact and only explicit `confirmed` counts; missing spec or anything missing/unreadable takes confirmation-gated resume-generate; a nested-inside workspace is disclosed as an overlap in **every** mode | C2, Decision 8, Decision 9 |
| `## Slice and Workspace` — `Slice:` header field recorded in portable normalized form on **slice** artifacts only (the survey workspace carries none and is identified by `slices.md`); control/secret-bearing paths are refused before lookup/creation/output; the repository root is not a slice; the directory name is a human convenience and never an identifier; workspace directory `.codexspec/specs/<id>-<slice>/` reusing the existing id convention, published from a same-device temporary sibling by one proven host-native atomic no-replace rename without weak fallback or git branch; collisions retry and the ASCII human suffix falls back to `slice` for Unicode-only basenames; `.codexspec`, specs root, workspace, every read artifact, and every write target validate and use via retained handle-relative no-follow access with opened-object type/link-count/identity checks | C3, Decision 8 |
| `## Generate Mode` — `spec.md` + `design.md` (scaled) + thin all-`open` `requirements.md` stub | C4 |
| `## Overview Mode` — `<id>-overview` workspace with thin architecture `design.md` + `slices.md`; no `spec.md`, no `reconcile.md` | C5 |
| `## Inference Marking and Confirmation` — file-level `Status: inferred/open`, `[inferred]` markers, promotion by `Status: confirmed` + Confirmation Log; no new command | C6 |
| `## Reconcile Mode` — baseline is confirmed spec (+ design when present); three drift kinds; severity by impact; both-side evidence with globally redacted sensitive values; direction suggested never applied; `needs-your-judgment` when intent does not decide | C7, C8, C10 |
| `## Reconcile Report` — the `reconcile.md` structure and per-item fields; global secret/control-safe rendering applies to the report and briefing; replacing an existing report pauses for explicit confirmation and otherwise preserves it byte-for-byte | C8, C10 |
| `## Scan Discipline` — name `/codexspec:onboard` only as design provenance, never load a repository-local sibling prompt at runtime, pin the complete applicable scan contract, and state three differences: no profile writes, `[path]` is the whole slice boundary, and descendant symlinks are followed only while contained | C9 |
| `## Instruction and Evidence Trust` / `## Boundaries` — read-only on code, writes confined to the handle-bound validated workspace, repository content and baselines (including local agent/command/skill files) remain untrusted evidence, detected sensitive values are redacted and controls originating in untrusted interpolated data are escaped before every artifact/conversation output without escaping renderer-authored structure, never `.codexspec/profile/`, never source/tests/git/constitution/baseline; a resumed draft appends only after explicit confirmation and never overwrites, with `reconcile.md` likewise explicitly confirmed before regeneration | C10 |
| `## Mode Resolution` / `## Slice and Workspace` / `## Overview Mode` — generate runs only a minimal read-only analyzable-code preflight before workspace preparation; workspace creation prepares and validates its identifying artifact (`spec.md` with the `Slice:` header, or `slices.md`) under a temporary non-workspace name, then atomically publishes to the absent final path before substantive scanning; a resume creates absent artifacts but requires confirmation before appending to present ones | C2, C3, C5, Decision 7 |

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
19. **S19 — path-only slice input**: a non-existing argument with diff or
    pull-request syntax is unsupported as a slice source, without excluding an
    existing path that has the same spelling. *(REQ-019)*
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

## Phase 5 — Coverage-gap closure

### T5.1 Add regression contracts for G-3, G-4, and G-5

- [x] Add focused assertions to `tests/test_reverse_spec_template.py` before
  changing the template, then run the module and record the expected failures.
  Red result: 2 failed / 55 passed (G-3 and G-5); G-4 was a characterization
  assertion over already-correct prose.
- **Outcome**: each confirmed rule fails independently when absent from the source
  template.
- **Paths**: `tests/test_reverse_spec_template.py`
- **Dependencies**: none
- **Covers**: REQ-022; **Plan**: Phase 5
- **Test Scenarios**:
  - **S21**: mode step 1 states that symbolic links are resolved before the
    resulting real path is compared with the repository root.
  - **S22**: the workspace rule requires `{YYYY-MMDD-HHMM}{rr}`, forbids a
    separate identifier generator, and forbids sequential numbering.
  - **S23**: a confirmed spec plus a present open design is classified as an
    unconfirmed workspace and cannot enter reconcile mode; an absent design keeps
    the spec-only fallback.

### T5.2 Update the authoritative template and gap register

- [x] Update `templates/commands/reverse-spec.md` to realize S21–S23 and update
  `coverage-gaps.md` with explicit resolution notes for G-3/G-4/G-5.
- **Outcome**: mode resolution is deterministic for both edge cases and the gap
  register no longer presents the three items as open on newer code.
- **Paths**: `templates/commands/reverse-spec.md`,
  `.codexspec/specs/2026-0818-2053p5-reverse-spec/coverage-gaps.md`
- **Dependencies**: T5.1
- **Covers**: REQ-002, REQ-007, REQ-008, REQ-014, REQ-015, REQ-022;
  **Plan**: Phase 5

### T5.3 Regenerate and verify distribution forms

- [x] Run `uv run codexspec init . --force --ai both`, verify only expected
  derived files change, then run targeted tests, ruff, and the full suite.
  Green result: targeted 264 passed; ruff and `git diff --check` passed; full
  suite 1258 passed / 50 skipped.
- **Outcome**: template and Claude/Codex distribution forms are synchronized and
  all checks are green.
- **Paths**: `.claude/commands/codexspec/reverse-spec.md`,
  `.agents/skills/codexspec-reverse-spec/SKILL.md`
- **Dependencies**: T5.2
- **Covers**: REQ-022, NFR-002; **Plan**: Phase 5

### T5.4 Repair complete-feature trust/path findings

- [x] Add reproducing contracts, update the authoritative template and affected
  SDD metadata, regenerate derived forms, and re-establish the green full suite.
  Red result: 4 failed / 57 passed. Green result: 61 targeted tests passed,
  268 cross-cutting tests passed, ruff and diff checks passed, and the full suite
  completed with 1262 passed / 50 skipped.
- **Outcome**: repository content cannot become authority; reads/writes cannot
  escape their permitted real paths; conflicting identity markers stop instead of
  bypassing a baseline; follow-up artifacts describe their current inputs.
- **Paths**: `templates/commands/reverse-spec.md`,
  `tests/test_reverse_spec_template.py`, the reverse-spec SDD workspace, and the
  two generated distribution forms.
- **Dependencies**: T5.3
- **Covers**: REQ-002, REQ-017, REQ-022; **Plan**: Phase 5
- **Test Scenarios**:
  - **S24**: instruction-shaped repository content remains evidence-only and no
    repository-provided command is executed.
  - **S25**: symlinked specs roots, workspaces, or write targets are rejected
    before mutation.
  - **S26**: descendant symlinks escaping the normalized slice are skipped and
    reported.
  - **S27**: conflicting `slices.md` and `Slice:` identity markers stop resolution.

### T5.5 Repair final security/mode findings

- [x] Add four reproducing contracts and repair the authoritative template and
  SDD together. Red result: 4 failed / 61 passed. Green result: 65 targeted
  template tests passed; the combined targeted suite passed 166 tests, the
  cross-cutting suite passed 106, and the full suite completed with 1266 passed /
  50 skipped. Ruff, format, and diff checks also passed.
- **Outcome**: parent-entry symlinks cannot bypass repository containment; one
  workspace cannot present contradictory slice identities; detected secrets are
  redacted from reports and briefing; and a design-only workspace deterministically
  resumes generate mode.
- **Paths**: `templates/commands/reverse-spec.md`,
  `tests/test_reverse_spec_template.py`, the reverse-spec SDD workspace, and the
  two generated distribution forms.
- **Dependencies**: T5.4
- **Covers**: REQ-002, REQ-004, REQ-008, REQ-010, REQ-017, REQ-022;
  **Plan**: Phase 5
- **Test Scenarios**:
  - **S28**: `.codexspec`, specs-root, and workspace entries are each non-symlink
    directories with explicit realpath containment and direct-parent checks.
  - **S29**: every present spec/design artifact carries one valid normalized
    `Slice:` and all values in the workspace agree.
  - **S30**: sensitive evidence is redacted from `reconcile.md` and conversation
    while preserving its location and non-sensitive context.
  - **S31**: a workspace found through confirmed design but missing `spec.md`
    resumes generate mode rather than falling outside all three modes.

### T5.6 Repair final trust/parser/compatibility findings

- [x] Add four reproducing contracts, repair the authoritative template and SDD,
  regenerate both distribution forms, and re-establish the complete green
  baseline. Red result: 4 failed / 63 passed. Template-level green result: 67
  passed; the combined targeted suite passed 168 tests, the cross-cutting suite
  passed 106, and the full suite completed with 1268 passed / 50 skipped. Ruff,
  format, and diff checks passed.
- **Outcome**: every verified finding is covered by an independent contract or
  deterministic metadata check, source and generated forms are synchronized, and
  the full baseline is green.
- **Paths**: `templates/commands/reverse-spec.md`,
  `tests/test_reverse_spec_template.py`, the reverse-spec SDD workspace, and the
  two generated distribution forms.
- **Dependencies**: T5.5
- **Covers**: REQ-001, REQ-002, REQ-008, REQ-010, REQ-017, REQ-019, REQ-022;
  **Plan**: Phase 5
- **Test Scenarios**:
  - **S32**: sensitive values are redacted from every overview/generate/reconcile
    artifact and every conversation output.
  - **S33**: an existing write target must have a determinable hard-link count of
    exactly one before it is read or written.
  - **S34**: duplicate or conflicting file-level `Status:` lines stop mode
    resolution instead of letting an executor choose one.
  - **S35**: an existing path wins over diff/PR-shaped spelling; only a
    non-existing changeset-shaped argument is rejected by the path-only contract.

### T5.7 Repair final workspace-read/collision/portable-path findings

- [x] Add three reproducing contracts, repair source and SDD, regenerate both
  distribution forms, and re-establish the full frozen baseline. Red result: 3
  failed / 67 passed. Green result: 70 template tests, 171 combined targeted, 106
  cross-cutting, and full suite 1271 passed / 50 skipped. Ruff, format, and diff
  checks passed.
- **Outcome**: workspace reads cannot escape through artifact links, workspace
  creation cannot reuse a random collision, and persisted slice identity has a
  portable separator encoding plus a stable Unicode-only suffix fallback. T5.8
  supersedes this task's lossy Unicode-normalization interpretation.
- **Paths**: `templates/commands/reverse-spec.md`,
  `tests/test_reverse_spec_template.py`, the reverse-spec SDD workspace, and both
  generated distribution forms.
- **Dependencies**: T5.6
- **Covers**: REQ-002, REQ-004, REQ-014, REQ-017, REQ-022; **Plan**: Phase 5
- **Test Scenarios**:
  - **S36**: every workspace artifact is direct, regular, non-symlink, and
    single-link before identity/status/baseline/requirements content is read.
  - **S37**: workspace creation is exclusive; an occupied random ID redraws an
    untried `rr`, never reusing or modifying the collision.
  - **S38**: `Slice:` persists with `/`, while a Unicode-only basename uses stable
    ASCII suffix fallback `slice` without changing artifact identity. T5.8 pins
    the exact-code-point rule.

### T5.8 Repair Unicode-identity and atomic-publication findings

- [x] Add two reproducing contracts, repair source and SDD, regenerate both
  distribution forms, and re-establish the full frozen baseline. Red result: 2
  failed / 70 passed. Green result: 72 template tests, 173 combined targeted, 106
  cross-cutting, and full suite 1273 passed / 50 skipped. Ruff, format, and diff
  checks passed.
- **Outcome**: distinct physical directories are never collapsed by Unicode
  normalization, and an interrupted creation never leaves an official workspace
  visible without a validated identity marker.
- **Paths**: `templates/commands/reverse-spec.md`,
  `tests/test_reverse_spec_template.py`, the reverse-spec SDD workspace, and both
  generated distribution forms.
- **Dependencies**: T5.7
- **Covers**: REQ-002, REQ-004, REQ-014, REQ-016, REQ-017, REQ-022, NFR-004;
  **Plan**: Phase 5
- **Test Scenarios**:
  - **S39**: persisted `Slice:` preserves exact filesystem Unicode code points, so
    two canonically equivalent but distinct physical directory names remain two
    identities; NFC/NFD normalization and case-folding are forbidden.
  - **S40**: a new workspace is prepared with a validated marker under a temporary
    name outside the official naming pattern, then atomically published to the
    absent final path without replacement; interruption before publication exposes
    no unidentifiable official workspace.

### T5.9 Repair input/serialization/publication/replacement findings

- [x] Add four reproducing contracts plus one sibling trust contract, repair
  source and SDD, regenerate both distribution forms, and re-establish the full
  frozen baseline. Reviewer red result: 4 failed / 71 passed. Sibling-sweep red
  result: 1 failed / 75 passed. Green result: 76 template tests, 177 combined
  targeted, 106 cross-cutting, and full suite 1277 passed / 50 skipped. Ruff,
  format, and diff checks passed.
- **Outcome**: path input remains literal data; single-line identity cannot be
  injected by control characters; untrusted controls cannot manufacture output
  structure; workspace publication has a same-device native atomic no-replace
  protocol or stops; and an existing reconciliation report is preserved unless
  the user explicitly confirms replacement.
- **Paths**: `templates/commands/reverse-spec.md`,
  `tests/test_reverse_spec_template.py`, the reverse-spec SDD workspace, and both
  generated distribution forms.
- **Dependencies**: T5.8
- **Covers**: REQ-001, REQ-002, REQ-004, REQ-010, REQ-014, REQ-016, REQ-017,
  REQ-019, REQ-022, NFR-004; **Plan**: Phase 5
- **Test Scenarios**:
  - **S41**: the complete non-empty argument payload is one literal path, passed
    as separately quoted data with an end-of-options delimiter where supported;
    no character becomes flags, instructions, extra arguments, or shell syntax.
  - **S42**: a normalized slice path containing a Unicode control or
    line/paragraph separator is refused before lookup or creation because it
    cannot fit the single-line `Slice:` identity safely.
  - **S43**: a same-device temporary sibling is published only with one proven
    host-native atomic no-replace directory rename; weaker emulation and
    unavailable primitives stop before publication.
  - **S44**: regeneration of an existing `reconcile.md` pauses for explicit user
    confirmation; without it, the report remains byte-for-byte unchanged.
  - **S45**: controls in descendant paths or evidence spans are rendered as
    escaped code-point tokens before every artifact or conversation output.

### T5.10 Repair identity-secret/handle/resume/preflight findings

- [x] Add four reproducing contracts, repair source and SDD, regenerate both
  distribution forms, and re-establish the full frozen baseline. Red result: 4
  failed / 74 passed. Green result: 78 template tests, 179 combined targeted,
  106 cross-cutting, and full suite 1279 passed / 50 skipped. Ruff, format, diff,
  repository-version Markdown lint, mypy, and Bandit checks passed.
- **Outcome**: a secret-bearing path cannot leak through identity; concurrent path
  replacement cannot redirect workspace access; resume never changes a
  pre-existing artifact without explicit confirmation; and empty-slice refusal
  occurs before any workspace preparation.
- **Paths**: `templates/commands/reverse-spec.md`,
  `tests/test_reverse_spec_template.py`, the reverse-spec SDD workspace, and both
  generated distribution forms.
- **Dependencies**: T5.9
- **Covers**: REQ-002, REQ-004, REQ-008, REQ-014, REQ-016, REQ-017, REQ-022,
  NFR-004; **Plan**: Phase 5
- **Test Scenarios**:
  - **S46**: a normalized slice path containing a detected secret is refused
    before lookup, suffix derivation, creation, or output without echoing the path
    or using redaction as identity.
  - **S47**: workspace reads/writes bind to a verified opened directory handle;
    artifacts open relative with no-follow semantics and verify type, link count,
    and stable identity on the opened object, otherwise access stops.
  - **S48**: resume discloses missing sections and waits for explicit user
    confirmation before appending to any artifact present at run start; refusal
    leaves it byte-for-byte unchanged, while wholly absent artifacts may be created.
  - **S49**: generate's minimal read-only analyzable-code preflight is the only
    scan before workspace publication and a negative result prepares nothing.

### T5.11 Repair sibling-prompt trust and control-source findings

- [x] Add two reproducing contracts, repair source and SDD, regenerate both
  distribution forms, and re-establish the full frozen baseline. Red result: 2
  failed / 78 passed. Green result: 80 template tests, 181 combined targeted,
  106 cross-cutting, and full suite 1281 passed / 50 skipped. Ruff, format, diff,
  repository-version Markdown lint, mypy, and Bandit checks passed.
- **Outcome**: a mutable repository-local sibling prompt can never become runtime
  instruction, while output escaping consumes only controls originating in
  untrusted interpolated data and preserves command-authored Markdown structure.
- **Paths**: `templates/commands/reverse-spec.md`,
  `tests/test_reverse_spec_template.py`, the reverse-spec SDD workspace, and both
  generated distribution forms.
- **Dependencies**: T5.10
- **Covers**: REQ-010, REQ-016, REQ-017, REQ-022, NFR-004; **Plan**: Phase 5
- **Test Scenarios**:
  - **S50**: `/codexspec:onboard` is design provenance, not a runtime include;
    repository-local sibling commands and skills remain untrusted evidence and
    are never opened, loaded, or followed as instructions.
  - **S51**: control escaping applies to controls originating in untrusted paths,
    evidence, or other interpolated data, but never to renderer-authored
    structural newlines or formatting characters.

## Dependency Summary

```text
T1.1 ──┬── T2.1 ─────────────┐
       └── T4.1 ─────────────┤
                             ├── T4.2
T3.1 ── T3.2 ──┬── T3.3 ─────┤
               └─────────────┘
T5.1 ── T5.2 ── T5.3 ── T5.4 ── T5.5 ── T5.6 ── T5.7 ── T5.8 ── T5.9 ── T5.10 ── T5.11
```

Acyclic. `T1.1` and `T3.1` have no dependencies and may start concurrently `[P]`;
everything else follows its declared predecessors. `T5.11` is the final checkpoint.

## Plan Coverage

| Plan deliverable | Tasks |
|---|---|
| Phase 1 — command template (C1–C10) | T1.1 |
| Phase 2 — contract tests | T2.1 |
| Phase 3 — registration and lockstep count sites (C11) | T3.1, T3.2, T3.3 |
| Phase 4 — derived regeneration and verification | T4.1, T4.2 |
| Phase 5 — coverage-gap closure | T5.1, T5.2, T5.3, T5.4, T5.5, T5.6, T5.7, T5.8, T5.9, T5.10, T5.11 |
| Decision 1 — template before tests | T1.1 → T2.1 ordering |
| Decision 2 — up-front grep sweep | T3.1 step 1, T3.2 step 6 |
| Decision 3 — emphasis-free assertions | T2.1 constraint |
| Decision 4 — regenerate last with `--ai both` | T4.1 |
| Decision 5 — README Enhanced table | T3.3 |

## Requirements Coverage

| Requirement | Tasks |
|---|---|
| REQ-001 standalone command surface | T1.1, T2.1 (S1), T5.6 (S35), T5.9 (S41) |
| REQ-002 mode auto-detection | T1.1, T2.1 (S3, S4, S5), T5.5 (S29, S31), T5.6 (S34), T5.7 (S38), T5.8 (S39–S40), T5.9 (S42), T5.10 (S46) |
| REQ-003 generate output boundary | T1.1 |
| REQ-004 workspace records its slice | T1.1, T5.5 (S29), T5.7 (S38), T5.8 (S39–S40), T5.9 (S42), T5.10 (S46) |
| REQ-005 derived content marked inferred/open | T1.1, T2.1 (S16) |
| REQ-006 confirmation reuses existing convention | T1.1 |
| REQ-007 baseline is confirmed spec/design only | T1.1, T2.1 (S7, S8) |
| REQ-008 unconfirmed baseline blocks reconcile | T1.1, T2.1 (S6), T5.5 (S31), T5.6 (S34), T5.10 (S48) |
| REQ-009 three drift kinds | T1.1, T2.1 (S9, S12) |
| REQ-010 persistent report plus briefing | T1.1, T2.1 (S12, S15), T5.5 (S30), T5.6 (S32), T5.9 (S44–S45), T5.11 (S51) |
| REQ-011 severity by impact; gates nothing | T1.1, T2.1 (S10, S11) |
| REQ-012 report only, never repair | T1.1, T2.1 (S14) |
| REQ-013 direction appeals to requirements | T1.1, T2.1 (S13) |
| REQ-014 slice unit and workspace creation | T1.1, T5.7 (S37–S38), T5.8 (S40), T5.9 (S43), T5.10 (S49) |
| REQ-015 bare run yields a map | T1.1, T2.1 (S3) |
| REQ-016 scan discipline reused | T1.1, T2.1 (S18), T5.8 (S40), T5.9 (S43), T5.10 (S49), T5.11 (S50) |
| REQ-017 read-only, workspace-confined writes | T1.1, T2.1 (S17), T5.4 (S24–S27), T5.5 (S28–S30), T5.6 (S32–S33), T5.7 (S36–S37), T5.8 (S40), T5.9 (S41–S45), T5.10 (S46–S48), T5.11 (S50–S51) |
| REQ-018 no pipeline coupling | T1.1, T2.1 (S11, S20) |
| REQ-019 path-based slice input only | T1.1, T2.1 (S1, S19), T5.6 (S35), T5.9 (S41) |
| REQ-020 registration and lockstep | T3.1 (S1–S4), T3.2, T3.3 |
| REQ-021 language regime | T1.1, T2.1 (S2), T3.2 |
| REQ-022 regression contracts | T5.1 (S21–S23), T5.2, T5.3, T5.4, T5.5, T5.6, T5.7, T5.8, T5.9, T5.10, T5.11 |
| NFR-001 English template with Language Preference | T1.1, T2.1 (S2) |
| NFR-002 self-bootstrap discipline | T4.1 |
| NFR-003 two constitutions separate | T3.2 step 5 |
| NFR-004 scales without blocking | T1.1, T5.8 (S40), T5.9 (S43), T5.10 (S48–S49), T5.11 (S50–S51) |
| NFR-005 independently readable output | T1.1 |
| NFR-006 no fabricated intent | T1.1 |

## Scenario-to-Task Mapping

| Task | Scenarios | Count |
|---|---|---|
| T2.1 | S1–S20 | 20 |
| T3.1 | S1–S4 | 4 |
| T5.1 | S21–S23 | 3 |
| T5.4 | S24–S27 | 4 |
| T5.5 | S28–S31 | 4 |
| T5.6 | S32–S35 | 4 |
| T5.7 | S36–S38 | 3 |
| T5.8 | S39–S40 | 2 |
| T5.9 | S41–S45 | 5 |
| T5.10 | S46–S49 | 4 |
| T5.11 | S50–S51 | 2 |

Non-testable tasks (T1.1 documentation-class, T3.3 documentation, T4.1
regeneration, T4.2 verification) carry deterministic verification instead of test
scenarios, per the task rules.

## Unmapped Tasks

None. Every task traces to a plan phase or plan-level decision and to at least one
`REQ`/`NFR`.
