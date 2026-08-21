# Implementation Plan: reverse-spec

**Feature Branch**: `2026-0818-2053p5-reverse-spec`
**Created**: 2026-08-20
**Input**: `requirements.md` (32 confirmed) · `spec.md` (REQ-001..021, NFR-001..006) · `design.md` (C1–C11, Decisions 1–8)

## Context

`design.md` settles what the system is: a single agent-driven command template
realizing three modes (overview / generate / reconcile), plus one installer entry
and its lockstep count sites. This plan settles only *how to build it* — ordering,
verification, and the repository-specific hazards that ordering must avoid. It
introduces no component and no interface beyond `design.md`.

The decisive planning fact is that the deliverable is **prose plus one metadata
entry**, not a runtime module (design Decision 1). That collapses the usual
foundation/core/integration layering: there is no code layer for the template to
sit on, so the build order is driven instead by the repository's distribution
mechanics — derived artifacts must be regenerated after the template is final, and
the command-count sites must move in lockstep or the suite goes red.

## Goals / Non-Goals

**Goals**

- Author `templates/commands/reverse-spec.md` realizing C1–C10.
- Lock the discipline with contract tests in the established style.
- Register the command and move every count site together (C11).
- Regenerate derived install artifacts and leave the suite green.

**Non-Goals**

- No runtime Python module for scanning or drift detection (design Decision 1).
- No change to `onboard`, `analyze`, `review-code`, or any pipeline command —
  `reverse-spec` is standalone and referenced by nothing (REQ-018).
- No translation-catalog entry and no `commit_templates` membership (REQ-021).
- No edit to either constitution (NFR-003).
- No hand-editing of `.claude/commands/codexspec/` or `.agents/skills/` (NFR-002).

## Tech Stack

Existing only: Markdown command templates under `templates/commands/`; Python 3.11
CLI (`typer`) with the command registry in `src/codexspec/commands/installer.py`;
`pytest` contract tests under `tests/`; `ruff` (120 columns); `pre-commit`.
No new dependency.

## Plan-Level Decisions

### Decision 1: Author the template before its contract tests

- **Evidence**: the repository's template contract tests
  (`tests/test_onboard_template.py`, `tests/test_debug_template.py`) assert exact
  substrings of the template's prose via `read_command(...)`.
- **Decision**: Phase 1 authors the template; Phase 2 writes the contract tests
  against it.
- **Rationale**: an assertion written before the prose would have to invent the
  exact wording the template must then reproduce verbatim — that inverts the
  dependency without adding safety, because the "red" it produces proves only that
  a string is missing, not that a behavior is wrong. The discipline is still
  locked by tests before the feature is complete, satisfying the constitution's
  testing standard.
- **Alternatives**: test-first. Rejected for the reason above; it is the right
  order for the Phase 3 Python change, where it is applied.
- **Trade-off**: Phase 1 has no automated gate of its own and is verified by
  deterministic review against `design.md`. Accepted — this matches how every
  existing command template in the repository was built.
- **Covers**: REQ-001; **Design**: C1

### Decision 2: Sweep every count site up front with one grep, before editing any

- **Evidence**: profile convention `Con-2026-0811-1418yq-1` records that adding a
  distributed command requires the installer entry, the docstring total *and*
  per-category count, the inline `# <Category> Commands (N)` comment whose wording
  varies by category, independent assertions in **both**
  `tests/commands/test_installer.py` and `tests/test_cli.py`, and rows in 8
  READMEs. Profile strategy `S-2026-0814-1548g5-1` records that fixing only the
  site a reviewer names costs one review round per site.
- **Decision**: Phase 3 begins with a single repository-wide grep enumerating every
  occurrence of the current counts (`25`, `enhanced (8)`, `# Enhanced Commands (8)`)
  and every README command table, then edits them in one pass and re-greps to
  confirm zero stale sites remain.
- **Rationale**: these sites are a known lockstep set; discovering them one review
  round at a time is the failure mode both records describe.
- **Covers**: REQ-020; **Design**: C11

### Decision 3: Target contract assertions at emphasis-free spans

- **Evidence**: profile pitfall `P-2026-0813-1606fz-1` — inline `**`/`*`/backticks
  inside an asserted span break substring matching, and the resulting failure looks
  like a template defect when the assertion is what is wrong.
- **Decision**: every assertion in `tests/test_reverse_spec_template.py` targets a
  span containing no inline markdown emphasis; where a concept must be asserted and
  its natural phrasing is emphasized, assert an adjacent plain span or the
  unemphasized fragment.
- **Covers**: NFR-001; **Design**: C1

### Decision 4: Regenerate derived artifacts last, with `--ai both`

- **Evidence**: profile convention `Con-2026-0813-1143el-1` records that
  `uv run codexspec init . --force --ai both` safely regenerates derived command
  and skill files mid-feature and preserves unrelated `config.yml` keys; a separate
  memory records that omitting `--ai both` rewrites `project.ai` (this repository
  must stay `both`).
- **Decision**: Phase 4 runs regeneration only after the template is final, always
  with `--ai both`, then verifies via `git status` that the only new or changed
  paths are this feature's sources plus the expected derived artifacts, and that
  `.codexspec/config.yml` is untouched.
- **Covers**: NFR-002; **Design**: C1, C11

### Decision 5: New README row goes in the Enhanced Commands table, not Self-Evolution

- **Evidence**: verified repository fact — the installer's `enhanced` category is
  `clarify, analyze, checklist, tasks-to-issues, distill, evolve, onboard, debug`,
  while `README.md` splits those across an **Enhanced Commands** table and a
  separate **Self-Evolution Commands** table holding `distill`, `evolve`, `onboard`.
  The README grouping is therefore not the installer category.
- **Decision**: register under installer category `enhanced` (per C11) but place the
  README row in the **Enhanced Commands** table in all 8 files.
- **Rationale**: `reverse-spec` writes SDD artifacts, never `.codexspec/profile/`
  (REQ-017), so it is not a self-evolution command despite scanning code like
  `onboard` does.
- **Covers**: REQ-020; **Design**: C11

## Risks / Trade-offs

| Risk | Impact on delivery | Mitigation |
|---|---|---|
| A count site is missed and the suite goes red late | Extra review rounds; the exact failure `Con-2026-0811-1418yq-1` describes | Decision 2's up-front grep sweep plus a confirming re-grep |
| A contract assertion spans markdown emphasis and fails misleadingly | Time lost "fixing" a correct template | Decision 3 |
| `codexspec init --force` without `--ai both` rewrites `project.ai` | Unrelated config churn staged into the commit | Decision 4 pins the flag and diffs `git status` |
| `markdownlint` reformats the new template or artifacts at commit time | Commit fails once | Re-stage only the hook-modified files and retry — the one permitted `git add` during `commit-staged` |
| `pre-commit` stalls building the `shellcheck_py` environment (needs network) | Commit appears to hang | Diagnose with `pre-commit run --verbose` before retrying; this feature adds no shell code |
| The template grows long enough to be skimmed rather than followed | Weakens the discipline it encodes | Keep C9 a reference to `/codexspec:onboard` rather than a restatement (design Decision 4) |

## Implementation Phases

### Phase 1: Command template (core deliverable)

Author `templates/commands/reverse-spec.md` with frontmatter (`description`,
`argument-hint: "[path]"`, `allowed-tools` modeled on `onboard.md`) and body
sections realizing the design: Language Preference (interaction + document, never
commit); Role and Operating Model; Mode Resolution (C2, bare run short-circuits
before any baseline lookup); Slice & Workspace (C3); Generate Mode (C4); Overview
Mode (C5); Inference Marking & Confirmation Contract (C6); Reconcile Mode (C7)
including the three drift kinds, impact-based severity, and the both-side-evidence
rule; `reconcile.md` format (C8); Scan Discipline as a reference to
`/codexspec:onboard` (C9); Boundaries (C10). The template carries **no**
`## Auto-Next Chain Advance` and **no** `## Automatic Distillation` section.

- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007,
  REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-013, REQ-014, REQ-015, REQ-016,
  REQ-017, REQ-018, REQ-019, REQ-021, NFR-001, NFR-004, NFR-005, NFR-006
- **Design**: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10

### Phase 2: Contract tests for the template discipline

Create `tests/test_reverse_spec_template.py` following
`tests/test_onboard_template.py`: a `read_command()` helper over
`templates/commands/`, frontmatter assertions via
`codexspec.translator.extract_frontmatter_fields`, and one test per discipline
clause — mode resolution including the bare-run short-circuit, the unconfirmed
baseline refusal, the three drift kinds, impact-based non-gating severity, the
both-side-evidence rule, direction reasoning against `requirements.md` including
the `needs-your-judgment` fallback, report-only, the read-only/no-profile
boundary, the `onboard` scan reference, path-only slice input, absence of
auto-next and Automatic Distillation sections, and the interaction/document
language regime with no `language.commit` reference.

Design Decision 5 has two halves — require both-side evidence, and never guess a
direction. Both are asserted, so neither anti-fabrication safeguard can be dropped
from the template without a test failing.

- **Covers**: REQ-002, REQ-005, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011,
  REQ-012, REQ-013, REQ-015, REQ-016, REQ-017, REQ-018, REQ-019, REQ-021, NFR-001
- **Design**: C1–C10

### Phase 3: Registration and lockstep count sites

Begin with Decision 2's grep sweep. Then, test-first for the Python change: update
`tests/commands/test_installer.py` (`len(result) == 25 → 26`,
`len(enhanced_commands) == 8 → 9`) and `tests/test_cli.py` (`"25" → "26"`), observe
them fail, then add the `get_commands_metadata()` entry for `reverse-spec` in the
`enhanced` category adjacent to `onboard` with a short zh-CN description, and
update the docstring (`enhanced (8) → (9)`, `Total: 25 → 26`) and the inline
`# Enhanced Commands (8) → (9)` comment. Add a row to the **Enhanced Commands**
table in all 8 `README*.md` files, translated per language. Do not add the command
to `commit_templates` and do not create a translation-catalog entry. Re-grep to
confirm no stale count remains.

- **Covers**: REQ-020, REQ-021, NFR-003
- **Design**: C11

### Phase 4: Derived regeneration and integration verification

Run `uv run codexspec init . --force --ai both` to regenerate
`.claude/commands/codexspec/reverse-spec.md` and
`.agents/skills/codexspec-reverse-spec/SKILL.md`. Verify with `git status` that
only this feature's sources and the expected derived artifacts changed and that
`.codexspec/config.yml` is untouched (notably `project.ai: "both"`). Then run the
verification suite below.

- **Covers**: NFR-002
- **Design**: C1, C11

## Verification Strategy

| Level | Command / check | Expectation |
|---|---|---|
| Lint | `uv run ruff check src/ tests/` | 0 findings; the zh-CN installer description stays within 120 columns |
| Targeted | `uv run pytest tests/test_reverse_spec_template.py tests/commands/test_installer.py tests/test_cli.py -q` | all green |
| Cross-cutting | `uv run pytest tests/test_sdd_workflow_templates.py tests/test_translation_files.py -q` | green — confirms the language-regime split and that no catalog entry is required |
| Full suite | `uv run pytest -q` | green, no regression against the current baseline of **1199 passed / 50 skipped** |
| Distribution | `git status` after Phase 4 | only feature sources + expected derived artifacts; `config.yml` unchanged |
| Deterministic doc check | read `templates/commands/reverse-spec.md` against `design.md` C1–C10 | every component realized; no auto-next / Automatic Distillation section present |

## Requirements Coverage

| Requirement | Plan Reference | Design Component |
|---|---|---|
| REQ-001 standalone command surface | Phase 1, Decision 1 | C1 |
| REQ-002 mode auto-detection | Phase 1, Phase 2 | C2, C3 |
| REQ-003 generate output boundary | Phase 1 | C4 |
| REQ-004 workspace records its slice | Phase 1 | C3 |
| REQ-005 derived content marked inferred/open | Phase 1, Phase 2 | C6 |
| REQ-006 confirmation reuses existing convention | Phase 1 | C6 |
| REQ-007 baseline is confirmed spec/design only | Phase 1, Phase 2 | C7 |
| REQ-008 unconfirmed baseline blocks reconcile | Phase 1, Phase 2 | C2 |
| REQ-009 three drift kinds | Phase 1, Phase 2 | C7 |
| REQ-010 persistent report plus briefing | Phase 1, Phase 2 | C8 |
| REQ-011 severity by impact; gates nothing | Phase 1, Phase 2 | C7, C8 |
| REQ-012 report only, never repair | Phase 1, Phase 2 | C7, C8, C10 |
| REQ-013 direction appeals to requirements | Phase 1, Phase 2 | C7 |
| REQ-014 slice unit and workspace creation | Phase 1 | C3 |
| REQ-015 bare run yields a map | Phase 1, Phase 2 | C2, C5 |
| REQ-016 scan discipline reused | Phase 1, Phase 2 | C9 |
| REQ-017 read-only, workspace-confined writes | Phase 1, Phase 2 | C10 |
| REQ-018 no pipeline coupling | Phase 1, Phase 2 | C1 |
| REQ-019 path-based slice input only | Phase 1, Phase 2 | C1 |
| REQ-020 registration and lockstep | Phase 3, Decisions 2 and 5 | C11 |
| REQ-021 language regime | Phase 1, Phase 2, Phase 3 | C1, C11 |
| NFR-001 English template with Language Preference | Phase 1, Phase 2, Decision 3 | C1 |
| NFR-002 self-bootstrap discipline | Phase 4, Decision 4 | C1 |
| NFR-003 two constitutions separate | Non-Goals (explicit exclusion), Phase 3 (bounded change set) | C11 |
| NFR-004 scales without blocking | Phase 1 | C9 |
| NFR-005 independently readable output | Phase 1 | C3, C5 |
| NFR-006 no fabricated intent | Phase 1 | C4 |

Design component coverage: C1 (Phases 1, 4) · C2–C10 (Phases 1, 2) · C11 (Phase 3).

## Assumptions

- **A-1** — The current full-suite baseline is 1199 passed / 50 skipped, measured
  on this branch before implementation. If it differs at implementation time, the
  measured value is the baseline; the requirement is no regression, not a fixed
  number.
- **A-2** — `codexspec init . --force --ai both` remains safe to run mid-feature, as
  recorded in `Con-2026-0813-1143el-1`. Phase 4 verifies this with `git status`
  rather than assuming it.
