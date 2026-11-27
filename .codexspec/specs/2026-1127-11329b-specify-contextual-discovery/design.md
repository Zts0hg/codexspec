# Design Document: Context-Aware Requirement Discovery

**Related Spec**: spec.md
**Confirmed Requirements**: requirements.md
**Created**: 2026-11-27
**Status**: Reviewed — PASS (see review-design.md)

## Context

This is an instruction-template change. The existing authoring source is internal/command_templates/sources/specify.md. The complete template under templates/commands/ and Claude/Codex installed forms are derived outputs, not independent sources. No Python runtime behavior, configuration schema, data model, or downstream command behavior changes are needed.

## Architecture & Components

### D1: Discovery preparation in the specify source

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005

Place explicit discovery preparation after the existing history/profile consultation and before Discussion Rules. Read the applicable workspace's automation setting before substantive discovery. Require targeted current-functionality inspection and independent acquisition of accessible facts before asking substantive questions.

Question and option premises are verified before deciding their applicability. Surface descriptions alone do not establish functionality or implementation status; classifications such as placeholder, unused, or functional follow inspection. The instructions distinguish verified implementation facts, confirmed intent, and assumptions; explain insufficient or contradictory evidence; forbid treating an unsuccessful search as proof of absence; and ask only for necessary remaining gaps. Investigation stops when sufficient, reuses prepared evidence, and expands only on changed scope, new evidence, or insufficiency.

These instructions apply in both automation modes. They prescribe neither an exhaustive repository scan nor a fixed ritual of tool calls before every question.

### D2: Automation-aware question selection and completion

Covers: REQ-005, REQ-006, REQ-007, REQ-008

Add mode-dependent clarification guidance before Discussion Rules. Enabled mode checks foreseeable specification, design, planning, and implementation decisions before final confirmation. The decision boundary is user impact on behavior, scope, compatibility, or important cost/maintenance trade-offs; equivalent implementations remain autonomous.

Disabled mode retains staged discovery without mandatory frontloading of all technical choices. Extend Completion with the enabled-mode requirement that no foreseeable downstream user decision remains unresolved. Keep explicit final-summary confirmation and the existing single notice/single generate-spec invocation. Previously unforeseeable downstream decisions retain existing stop-and-ask behavior.

Do not duplicate full design or planning responsibilities in specify. Preserve the existing questions-at-a-time and candidate-entry rules.

### D3: Existing generation and installation pipeline

Covers: REQ-009

Maintain only the opted-in internal specify source. Render its complete template with internal/command_template_fragments.py --write. Generate installed forms through the existing ClaudeIntegration.install and CodexIntegration.install_skills APIs, using the checkout's interaction language.

Keep shared fragments, other command sources, frontmatter descriptions, runtime code, configuration, and command registrations unchanged. Existing distribution checks validate exact renderer/installer consistency. The normal installation path supplies the behavior to users without a new maintenance mechanism or runtime dependency.

### D4: Instruction contract verification

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009

Extend tests/test_sdd_workflow_templates.py with focused assertions of the required instruction relationships and placement before questioning, not isolated keyword presence. Use the same behavior assertions for the complete template and both installed forms where practical; existing fragment/distribution tests cover authored-source and generated-output byte fidelity.

Cover verification of question/option premises independently of their origin and inspection before implementation-status classification; accessible facts and necessary evidence gaps; missing/inaccessible/contradictory evidence; stopping and reuse; enabled/disabled configuration semantics; downstream-blocking choices; equivalent technical autonomy; and final confirmation/advance preservation.

Static contract tests verify the shipped instructions and generation consistency. They cannot establish that every model will comply in every conversation; scenario inspection supplements them without claiming a live-model evaluation.

## Key Design Decisions

### DD-001: Keep the change local to specify's existing source

Covers: REQ-001, REQ-002, REQ-005, REQ-006, REQ-009

- **Context**: Only specify's discovery behavior is in scope; all commands already share the authoring/distribution mechanism.
- **Decision**: Add local preparation and clarification sections and amend the existing Completion contract.
- **Alternatives**: Changing a shared fragment would affect unrelated entry points; adding a runtime inspector or configuration switch would exceed confirmed scope.
- **Trade-offs**: Instruction execution remains agent-driven. The implementation introduces no parser, tool orchestration service, or new configuration.

### DD-002: Preserve the separation between facts and decisions

Covers: REQ-001, REQ-002, REQ-003, REQ-004, REQ-006, REQ-007, REQ-008

- **Context**: Investigation can remove invalid question premises but cannot establish the user's desired outcome.
- **Decision**: Put factual preparation before decision selection; retain user control over material consequences and autonomous choices among equivalent implementations.
- **Alternatives**: Asking users to supply retrievable facts retains the reported burden; treating code as intent or asking approval for every implementation detail contradicts confirmed requirements.
- **Trade-offs**: Unavailable facts and genuinely new choices still require focused questions.

## Requirements Coverage

| Spec Requirement | Design Coverage |
|---|---|
| REQ-001 | D1, D4, DD-001, DD-002 |
| REQ-002 | D1, D4, DD-001, DD-002 |
| REQ-003 | D1, D4, DD-002 |
| REQ-004 | D1, D4, DD-002 |
| REQ-005 | D1, D2, D4, DD-001 |
| REQ-006 | D2, D4, DD-001, DD-002 |
| REQ-007 | D2, D4, DD-002 |
| REQ-008 | D2, D4, DD-002 |
| REQ-009 | D3, D4, DD-001 |

## Open Items

None. The design refines implementation within the confirmed scope and introduces no new product decision.
