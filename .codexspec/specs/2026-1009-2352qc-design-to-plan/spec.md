# Feature Specification: design-to-plan command rename

## Context and Goals

The planning stage consumes design.md and produces plan.md. Rename its public
command from spec-to-plan to design-to-plan so the command sequence expresses
spec → design → plan → tasks → implementation. Preserve the planning contract.
Authority: requirements.md NEED-001, NEED-002, and DEC-001, confirmed 2026-10-09.

## Requirements

### REQ-001: Official planning command

- **Sources**: NEED-001, DEC-001
- **Statement**: Claude slash commands and Codex skills expose design-to-plan as the
  official planning command. spec-to-plan is removed, with no alias or forwarding
  entry. The command remains in its existing category and pipeline position.
- **Acceptance**: A fresh installation exposes /codexspec:design-to-plan and
  $codexspec:design-to-plan; the old command/skill and registry entry are absent.
  Replacement does not increase the distributed command count.

### REQ-002: Preserve planning behavior

- **Sources**: NEED-001
- **Statement**: The renamed command retains its existing inputs, authority order,
  implementation-planning rules, legacy artifact handling, plan.md output, review-plan
  gate, and advancement to plan-to-tasks. Its title describes design-to-plan.
- **Acceptance**: Given the same confirmed artifacts, the command still consumes
  design.md, plans phases/order/verification without redesigning the architecture,
  and maps plan components to requirements and design components. Existing behavior
  for legacy features without design.md is unchanged. Removing a command alias does
  not remove support for legacy input artifacts.

### REQ-003: Update every active workflow and distribution surface

- **Sources**: NEED-002, DEC-001
- **Statement**: Automatic advancement, auto-dev, active command guidance, installer
  metadata, translations, current documentation, tests, and generated Claude/Codex
  copies reference design-to-plan. spec-to-design advances to design-to-plan, which
  advances to plan-to-tasks.
- **Acceptance**: All supported languages and both integrations expose the new name;
  their existing localized descriptions remain semantically accurate. Maintainer
  source, complete templates, installed copies, and workflow tests agree. Current
  instructions do not direct users to the removed command.

### REQ-004: Remove previously installed old entries on update

- **Sources**: NEED-002, DEC-001
- **Statement**: A successful command installation/update for a selected integration
  removes its previously installed spec-to-plan entry and installs design-to-plan.
  Removal targets the retired command entry; unrelated project files and commands
  are preserved. No compatibility entry is created.
- **Acceptance**: Updating an existing Claude, Codex, or both installation leaves no
  runnable old entry in the selected integration(s). Repeating the update is safe.
  If installation/removal fails, the operation reports failure instead of claiming
  that the old command was removed. Unselected integrations follow existing selection
  behavior. This is removal during installation, not old-name command dispatch.

## Scenarios

1. A user lists commands in a new installation: design-to-plan appears where the
   planning command belongs, and spec-to-plan is unavailable.
2. A user finishes spec-to-design with auto_next enabled: the next invocation is
   design-to-plan, followed by the existing plan review and plan-to-tasks stages.
3. A user updates a project with old command files: selected integrations receive
   the new entry and lose the retired entry; unrelated commands survive.
4. A user supplies a legacy feature without design.md: the existing planning
   fallback remains available under the new command name.

## Constraints and Decisions

- DEC-001 rejects old-name aliases, forwarders, and compatibility entries.
- NEED-001 preserves behavior and output; this is a public command rename.
- Existing repository governance applies: edit opted-in internal sources, render
  complete distribution templates, and regenerate installation copies. Do not
  hand-edit derived command/skill files or widen packaging boundaries.

## Scope Boundaries

No architectural redesign of the planner, output-format change, or compatibility
command is included. Historical feature records and release history remain evidence
of names used at the time; current operational guidance uses the new name. Mentioning
old names in removal tests or historical evidence does not expose a command entry.

## Open Questions and Assumptions

No unresolved questions or additional product assumptions.

## Requirements Traceability

| Confirmed Entry | Spec Coverage |
| --- | --- |
| NEED-001 | REQ-001, REQ-002 |
| NEED-002 | REQ-003, REQ-004 |
| DEC-001 | REQ-001, REQ-003, REQ-004; Scope Boundaries |
