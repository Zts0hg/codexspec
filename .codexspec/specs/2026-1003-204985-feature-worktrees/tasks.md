# Implementation Tasks: Feature Worktrees

**Feature**: `2026-1003-204985-feature-worktrees`
**Authority**: [requirements.md](requirements.md) → [spec.md](spec.md) → [design.md](design.md) → [plan.md](plan.md)
**Status**: Complete; required local verification and isolated complete-feature review passed

Code changes follow red-green verification. Each scenario below must map to an asserting test before
completion. Documentation is checked deterministically. All implementation occurs in this feature's
worktree. Task order is sequential; no parallel marker implies authorization to overlap shared edits.

## Phase 1: Configuration and repository foundation

### T001 — Define checkout-local settings and stable repository location

- [x] **Outcome**: The shipping workspace service reads/writes default-on `workflow.worktrees`, and
  shared discovery locates the same external parent from normal/bare linked worktrees.
- **Paths**: `src/codexspec/worktrees.py` (new), `src/codexspec/automation.py`,
  `tests/test_worktrees.py` (new), `tests/test_automation_git.py`.
- **Dependencies**: None.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-004, REQ-012, REQ-016, NFR-002; **Plan**: Phase 1.
- **Verification**: Write failing parsing/discovery tests, implement, run focused tests including
  existing automation discovery cases.
- **Test Scenarios**:
  - S001: Absent config/section/key is enabled; literal false disables; true enables.
  - S002: Writing a setting preserves unrelated fields/comments and produces a literal boolean.
  - S003: Two checkouts retain independent switch values; no shared override is created.
  - S004: Main, nested, and linked callers resolve one normal-repository parent.
  - S005: Bare repository and linked worktree callers resolve one bare-repository parent.
  - S006: Auto-dev retains its fixed branch/basename but uses the new parent; ambiguous/invalid
    repository or main-branch identity errors rather than selecting an arbitrary feature branch.

## Phase 2: Workspace creation and readiness

### T002 — Create and reuse ordinary and maintenance worktrees

- [x] **Outcome**: Validated roles create distinct registered workspaces, publish requirements only
  when ready, and reuse existing state without overwriting caller or target content.
- **Paths**: `src/codexspec/worktrees.py`, `tests/test_worktrees.py`.
- **Dependencies**: T001.
- **Covers**: REQ-004, REQ-005, REQ-006, REQ-007, REQ-011, REQ-014, REQ-015, NFR-001, NFR-002;
  **Plan**: Phase 2.
- **Verification**: Red-green tests against real temporary Git repositories and registration state.
- **Test Scenarios**:
  - S007: Two full feature identities produce distinct external branches/worktrees and requirements.
  - S008: Creation preserves caller branch, HEAD, staged bytes, and unstaged/untracked files.
  - S009: Continuation from another checkout reuses the feature's committed and uncommitted state
    without overwriting its requirements or resetting to main.
  - S010: Occupied paths, incompatible branch registration, and invalid feature identities fail
    without overwriting directories or falling back to main.
  - S011: Standalone maintenance uses/reuses its dedicated workspace; maintenance within an active
    ordinary feature remains in that feature.
  - S012: Completion leaves feature worktree and branch registered; no main merge/delete occurs.
  - S013: Interrupted creation metadata distinguishes owned partial creation from unrelated paths;
    concurrent attempts cannot create conflicting registrations or clobber metadata.

### T003 — Implement ancestry-based baselines and verified merge continuation

- [x] **Outcome**: New workspaces use the specified committed history and cannot begin feature writes
  while divergent baseline preparation is unresolved or unverified.
- **Paths**: `src/codexspec/worktrees.py`, `tests/test_worktrees.py`.
- **Dependencies**: T002.
- **Covers**: REQ-007, REQ-008, REQ-009, REQ-010, REQ-014, NFR-001, NFR-003; **Plan**: Phase 2.
- **Verification**: Red-green tests with local remotes, controlled commits, and preparation state.
- **Test Scenarios**:
  - S014: Equal tips, local ahead, and remote ahead select the correct commit, including timestamps
    that disagree with ancestry.
  - S015: Configured remote is fetched; failed fetch reports stale information, uses available refs,
    and the next creation retries rather than retaining a disabled-fetch state.
  - S016: No remote uses local main; missing/unusable baseline stops before requirements writes.
  - S017: Diverged histories merge only in the new worktree; requirements are withheld until
    matching successful project-verification evidence is supplied.
  - S018: Conflicts remain non-ready; resolving the merge and verifying the resulting HEAD permits
    completion, while unresolved entries, failed checks, or stale evidence do not.
  - S019: Interrupted/failed preparation remains non-ready on reuse; caller main and unrelated work
    are preserved rather than force-cleaned.

## Phase 3: CLI and platform integration

### T004 — Wire helper, configuration, and mutable review entry points

- [x] **Outcome**: CLI operations use the shipping workspace service and report actual paths/scope;
  ordinary opt-out and installation exemptions remain functional.
- **Paths**: `src/codexspec/__init__.py`, `src/codexspec/worktrees.py`,
  `src/codexspec/i18n.py` if needed for default display, `tests/test_worktrees_cli.py` (new),
  relevant existing config and distill-review interface tests.
- **Dependencies**: T003.
- **Covers**: REQ-001, REQ-002, REQ-005, REQ-006, REQ-011, REQ-013, REQ-014, REQ-016, NFR-001, NFR-003;
  **Plan**: Phase 3.
- **Verification**: Red-green CLI tests; preserve existing legacy behavior with explicit opt-out in
  tests whose premise is in-place mutation.
- **Test Scenarios**:
  - S020: Helper create/resolve/maintenance/finish responses expose absolute paths and distinguish
    ready, pending verification/conflict, and explicit failures without shell evaluation.
  - S021: Config set from main writes maintenance and reports destination; main remains enabled
    while a disable takes effect in maintenance. A bare toggle uses destination's current value.
  - S022: Config display is read-only; explicit disabled mode writes the current checkout; enabled
    feature-local settings stay in the feature. Unrelated language/frontmatter writes share routing.
  - S023: Mutable distill-review setup uses the resolved destination before draft/profile/runtime
    writes, with the UI/response identifying that project.
  - S024: First-time and update init write only their explicitly selected checkout regardless of the
    switch and preserve unrelated settings.
  - S025: Non-ready workspace creation prevents a config/review write and reports the path/status;
    no missing-runtime or invalid-baseline error falls back to modifying main.

### T005 — Adapt both feature-creation scripts

- [x] **Outcome**: Bash and PowerShell creation use isolated helper output by default and preserve
  explicit opt-out behavior and supported argument forms.
- **Paths**: `scripts/bash/create-new-feature.sh`, `scripts/powershell/create-new-feature.ps1`,
  `tests/scripts/bash/test_create_new_feature.py`,
  `tests/scripts/powershell/test_create_new_feature.py`, relevant script fixtures.
- **Dependencies**: T004.
- **Covers**: REQ-002, REQ-004, REQ-005, REQ-006, REQ-014, NFR-001, NFR-003; **Plan**: Phase 3.
- **Verification**: Run both platform test groups when interpreters are available; deterministic
  contract checks remain necessary for an unavailable interpreter.
- **Test Scenarios**:
  - S026: Default-enabled invocation returns external absolute artifact/workspace paths and leaves
    caller branch/files/index unchanged.
  - S027: Explicit disabled mode retains in-place branch/artifact behavior and existing naming.
  - S028: Invalid names, unavailable helper, or non-ready preparation return failure/status without
    creating requirements in main; returned feature identity supports resuming preparation.
  - S029: PowerShell JSON output and Bash supported short-name arguments retain their caller contract
    while exposing the new workspace path.

## Phase 4: Agent workflow and documentation

### T006 — Route distributed command writes and regenerate artifacts

- [x] **Outcome**: Distributed Claude/Codex command bodies enforce the same write destination and
  explicitly preserve auto-dev delegation and caller input provenance.
- **Paths**: `internal/command_templates/fragments/workspace-routing.md` (new),
  `internal/command_templates/sources/*.md`, generated `templates/commands/*.md`,
  derived `.claude/commands/codexspec/*.md` and `.agents/skills/codexspec-*/SKILL.md`,
  `tests/test_worktrees_template.py` (new).
- **Dependencies**: T004, T005.
- **Covers**: REQ-001 through REQ-016, NFR-001, NFR-002, NFR-003; **Plan**: Phase 4.
- **Verification**: Verify meaningful command contracts, render sources, regenerate installed forms
  through existing tooling, and run the read-only distribution check.
- **Test Scenarios**:
  - S030: Every distributed command source includes the workspace routing contract before its writes;
    specify/quick creation occurs before requirements publication and carries absolute paths onward.
  - S031: Auto-dev and delegated stages keep their fixed workspace; enabled ordinary creation cannot
    take the old in-place failure fallback; explicit disabled behavior remains available.
  - S032: Read-only source inspection retains original inputs; commit-staged and other caller-state
    operations cannot silently stage/copy/reset main state to satisfy routing.
  - S033: Configuration scope, first/update init exception, maintenance routing, and finish-before-
    artifact creation are reflected consistently in complete distributed/installed bodies.

### T007 — Document the shipped user workflow and maintenance architecture

- [x] **Outcome**: User-facing configuration/development documentation and maintainer guidance
  describe the new default, unified paths, checkout-local effects, baseline/failure behavior,
  fixed auto-dev model, installation exceptions, and retained-worktree lifecycle.
- **Paths**: Existing relevant pages under `docs/en/`, `README.md`, `CLAUDE.md`, and corresponding
  translated documentation where a changed existing path example would otherwise be incorrect.
- **Dependencies**: T006.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-005, REQ-008, REQ-010, REQ-011, REQ-012, REQ-013,
  REQ-014, REQ-015, REQ-016; **Plan**: Phase 4.
- **Verification**: Resolve links/paths; search published docs for stale old-parent examples; check
  new interface names against implementation and run applicable documentation checks. No artificial
  runtime tests are required for prose.

## Phase 5: Integrated verification

### T008 — Establish complete verification and isolated review evidence

- [x] **Outcome**: Full-suite and required deterministic gates pass, every scenario has an asserting
  test, and the isolated complete-feature defect review returns a valid PASS envelope.
- **Paths**: All implementation paths above, this feature's `tasks.md`, optional `issues.md`, and
  `review-code.md` according to the review skill.
- **Dependencies**: T001–T007.
- **Covers**: REQ-001 through REQ-016, NFR-001, NFR-002, NFR-003; **Plan**: Phase 5.
- **Verification**: Focused suites, full pytest, Ruff, distribution checks, archive build/inspection,
  scenario self-check, then isolated `$codexspec:review-code --feature <feature-dir>`; verify and
  repair findings according to the implementation skill before declaring completion.
- **Test Scenarios**:
  - S034: Built/installable package includes the new runtime/helper and complete templates but no
    internal fragment sources; a temporary installed project creates an isolated feature correctly.
  - S035: End-to-end config/creation/continuation/maintenance/auto-dev interactions preserve caller
    checkout state and use one parent under both normal and bare layouts.

## Coverage

| Plan Deliverable | Tasks | Scenario Coverage |
|---|---|---|
| Phase 1 / C1, C2, C6 | T001 | S001–S006 |
| Phase 2 / C3, C4 | T002, T003 | S007–S019 |
| Phase 3 / C2, C3, C5, C6 | T004, T005 | S020–S029 |
| Phase 4 / C5, C6 | T006, T007 | S030–S033; deterministic documentation checks |
| Phase 5 / C1–C6 | T008 | S034–S035 and full scenario audit |

| Requirement | Task References |
|---|---|
| REQ-001 | T001, T004, T006, T007, T008 |
| REQ-002 | T001, T004, T005, T006, T007, T008 |
| REQ-003 | T001, T006, T007, T008 |
| REQ-004 | T001, T002, T005, T006, T008 |
| REQ-005 | T002, T004, T005, T006, T007, T008 |
| REQ-006 | T002, T004, T005, T006, T008 |
| REQ-007 | T002, T003, T006, T008 |
| REQ-008 | T003, T006, T007, T008 |
| REQ-009 | T003, T006, T008 |
| REQ-010 | T003, T006, T007, T008 |
| REQ-011 | T002, T004, T006, T007, T008 |
| REQ-012 | T001, T006, T007, T008 |
| REQ-013 | T004, T006, T007, T008 |
| REQ-014 | T002, T003, T004, T005, T006, T007, T008 |
| REQ-015 | T002, T006, T007, T008 |
| REQ-016 | T001, T004, T006, T007, T008 |
| NFR-001 | T002, T003, T004, T005, T006, T008 |
| NFR-002 | T001, T002, T006, T008 |
| NFR-003 | T003, T004, T005, T006, T008 |

## Unmapped Tasks and Open Issues

None. All tasks have upstream authority. Artifact review alone does not establish implementation completion.
