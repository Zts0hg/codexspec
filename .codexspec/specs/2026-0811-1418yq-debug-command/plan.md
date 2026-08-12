# Implementation Plan: debug-command

<!--
Language: document language is English (.codexspec/config.yml → language.document: en).
Authority: requirements.md (confirmed) > spec.md > constitution/repo facts > plan decisions.
-->

**Feature Branch**: `2026-0811-1418yq-debug-command`
**Created**: 2026-08-11
**Status**: Draft

## Context, Goals, Non-Goals

- **Goal**: Add a root-cause-first debugging discipline, delivered from one definition as (1) a standalone `/codexspec:debug` command and (2) a low-ceremony escalation that `implement-tasks` enters when a fix is not converging.
- **Non-Goals** (from spec Out of Scope): not a mandatory pipeline stage; no hook on any command other than `implement-tasks`; no persistent debug artifact; no `workflow.auto_debug` or any config key; no metric/eval-driven optimization.

## Existing Repository Constraints (verified)

- **Self-bootstrap** (constitution): edit `templates/commands/` only; `.claude/commands/codexspec/` and `.agents/skills/` are regenerated via publish → `codexspec init`. Do not hand-edit derived artifacts.
- **Command-to-command primitive**: the only mechanism is a template line `Invoke /codexspec:<name>` (as used by `review-spec`/`review-plan`/`review-tasks` and the `## Automatic Distillation` section).
- **Command template convention**: frontmatter (`description`, `argument-hint`, optional `allowed-tools`) → `## Language Preference` → `## User Input` ($ARGUMENTS) → body → closing section.
- **`implement-tasks.md` structure** (attach points): §3 TDD Workflow has a **Verify — Run Tests** step ("ensure new tests pass and no existing tests break"); §7.4 **Apply Test-Safe Repairs** handles "a functional defect, first add a reproducing regression test... then red-green-refactor". These are the two semantic trigger locations.
- **Embedded-section precedent**: `## Automatic Distillation` is a self-contained section that references an earlier step (§7.6 success) and issues an `Invoke`.
- **Installer registration**: `src/codexspec/commands/installer.py::get_commands_metadata()` lists every distributed command with a `category`; `tests/commands/test_installer.py` asserts totals and per-category counts.
- **READMEs**: 8 language versions list the commands.

## Technical Approach

Two authored artifacts plus a release tail:

1. **New `templates/commands/debug.md`** — the four-phase root-cause discipline, authored once; this file *is* the standalone command and the single definition the hook references.
2. **Edit `templates/commands/implement-tasks.md`** — add one `## Systematic Debugging Escalation` section, plus brief in-context pointers at the two trigger locations so the escalation is discoverable at the moment it is needed.
3. **Release tail** (per NFR-005): register `debug` in installer metadata; update READMEs; derived artifacts regenerate at publish → `init` (not hand-edited).

## Plan-Level Decisions

- **PLAN-DEC-001 (resolves OPEN-001): `debug.md` skeleton.** Frontmatter `description` + `argument-hint: "[error text | failing test | file:line | plain-language symptom]"` + `allowed-tools: Read, Grep, Glob, Bash, Edit, Write` (reproduce needs read/run; Phase 4 needs edit/verify). Sections: `## Language Preference` → `## User Input` → `## Role and Iron Law` (no fix before root cause) → `## Symptom Intake` (free-form intake + reproduce-or-ask) → `## Investigation Protocol` with `### Phase 1 Root-Cause Investigation` (hard gate), `### Phase 2 Pattern Analysis`, `### Phase 3 Hypothesis & Verification`, `### Phase 4 Fix`, `### Architecture Gate` (≥3 fixes) → `## Completion`. *Covers: REQ-001, REQ-002, REQ-003, REQ-004, NFR-001.*
- **PLAN-DEC-002 (integration shape).** Add one `## Systematic Debugging Escalation` section to `implement-tasks.md` that: names the two trigger points **by semantic location** (the TDD Verify/green loop; the test-safe-repair of a functional defect) rather than brittle section numbers (per review-spec RA-1); states trip (a) and the narrowed trip (b); issues `Invoke /codexspec:debug`; declares it non-gating and low-ceremony; and ends with an explicit resume. Add a one-line pointer at the §3 Verify step and the §7.4 functional-defect bullet ("if this does not converge / the fix is non-trivial, see `## Systematic Debugging Escalation`"). *Covers: REQ-005, REQ-006, NFR-002.*
- **PLAN-DEC-003 (installer).** Add a `debug` entry to `get_commands_metadata()`, `category: "enhanced"` (alongside `analyze`/`checklist`/`distill`/`evolve`), with a Chinese description, e.g. "系统化根因排查（四阶段：复现→定位根因→单一修复），可独立调用或由 implement-tasks 升级进入". *Covers: NFR-005.*
- **PLAN-DEC-004 (resolves DO-1): Phase 4 wording.** Phrase Phase 4 so "write a failing test first" applies to code defects, and for a symptom with no natural unit test (docs/config/incident) it becomes "construct the closest reproducing check first". Refinement of confirmed intent, no scope change. *Covers: REQ-002.*
- **PLAN-DEC-005 (no config, no artifact).** Nothing is added to the config schema or handlers; `debug.md` instructs writing no files. *Covers: NFR-003, NFR-004.*

## Components / Interfaces

- **C1 — `templates/commands/debug.md`** (new): the standalone command and single discipline definition. *Covers: REQ-001, REQ-002, REQ-003, REQ-004, NFR-001, NFR-004.*
- **C2 — `templates/commands/implement-tasks.md`** (edit): `## Systematic Debugging Escalation` section + two in-context pointers. *Covers: REQ-005, REQ-006, NFR-002.*
- **C3 — `src/codexspec/commands/installer.py`** (edit): `debug` metadata entry. *Covers: NFR-005.*
- **C4 — READMEs** (edit, 8 languages): add the `debug` row to the command listing. *Covers: NFR-005.*
- **C5 — derived artifacts** (`.claude/commands/codexspec/debug.md`, `.agents/skills/codexspec-debug/`): regenerated at release via publish → `init`; NOT hand-edited. *Supports: CON-004/NFR-005.*
- **Unchanged**: `templates/commands/review-code.md` (stays review-only) and `.codexspec/config.yml` schema. *Enforces: REQ-006/SC-004, NFR-003.*

## Implementation Phases

1. **Phase 1 — Author `debug.md`** (C1) per PLAN-DEC-001/-004.
2. **Phase 2 — Edit `implement-tasks.md`** (C2) per PLAN-DEC-002.
3. **Phase 3 — Register in installer** (C3) per PLAN-DEC-003; update `tests/commands/test_installer.py` counts (total +1; `enhanced` +1).
4. **Phase 4 — Update READMEs** (C4, 8 languages).
5. **Phase 5 — Tests & gates**: add template-structure tests; run the full suite + ruff.

(Derived-artifact regeneration and version bump are the standard release tail, not part of this feature's task list.)

## Verification Strategy

- **Template-structure tests** (extend `tests/test_sdd_workflow_templates.py` or a new `tests/test_debug_template.py`):
  - `debug.md` exists, has frontmatter (`description`, `argument-hint`) and `## Language Preference`; body contains the four phases, the iron-law gate, and the ≥3-fix architecture gate.
  - **REQ-004 / SC-005**: `debug.md`'s `## Symptom Intake` instructs reproduce-or-ask — no fix is proposed before a stable reproduction is established or requested.
  - `implement-tasks.md` contains `## Systematic Debugging Escalation` that references `Invoke /codexspec:debug`, states an explicit resume, and includes trip (a), trip (b), and the (b) narrowing.
  - **SC-001**: the four-phase protocol text is NOT duplicated in `implement-tasks.md` (assert the discipline lives only in `debug.md`).
  - **SC-004**: `review-code.md` is unchanged by this feature.
  - **NFR-003**: no new key in the config schema/handlers.
- **Installer**: `test_installer.py` shows `debug` present; totals/`enhanced` counts updated.
- **Suite/lint**: `uv run python -m pytest` green; `uv run ruff check src/`.

## Risks & Trade-offs

- **Mid-flow escalation discoverability** — a section that triggers during §3/§7.4 risks being overlooked. Mitigated by the two in-context pointers (PLAN-DEC-002).
- **Section-reference brittleness (RA-1)** — mitigated by semantic-location wording.
- **"Non-trivial" is a judgment call** — intentional natural-language condition (consistent with CodexSpec's no-DSL style); bounded by the CON-003 definition (tracing vs mechanical edit).
- **Phase 4 for non-code symptoms (DO-1)** — mitigated by PLAN-DEC-004.

## Requirements Coverage

| Requirement | Plan Reference |
|-------------|----------------|
| REQ-001 | C1; PLAN-DEC-001 |
| REQ-002 | C1; PLAN-DEC-001, PLAN-DEC-004 |
| REQ-003 | C1 (Architecture Gate); PLAN-DEC-001 |
| REQ-004 | C1 (Symptom Intake); PLAN-DEC-001 |
| REQ-005 | C2; PLAN-DEC-002 |
| REQ-006 | C2; PLAN-DEC-002; review-code unchanged (C5/Unchanged) |
| NFR-001 | C1; PLAN-DEC-001 (single definition; hook references, no duplication) |
| NFR-002 | C2; PLAN-DEC-002 (conditional / non-gating / low-ceremony / explicit resume) |
| NFR-003 | PLAN-DEC-005 (no config key) |
| NFR-004 | C1; PLAN-DEC-005 (no persistent artifact) |
| NFR-005 | C3, C4, C5 (installer + READMEs + regenerated derived artifacts) |
