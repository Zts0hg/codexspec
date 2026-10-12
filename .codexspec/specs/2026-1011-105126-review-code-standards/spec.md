# Feature Specification: Evidence-Based Review with On-Demand Standards

**Feature Branch**: `2026-1011-105126-review-code-standards`
**Created**: 2026-10-11
**Status**: Confirmed requirements compiled
**Authority**: [requirements.md](requirements.md), confirmed entries only.

## Context and Goals

Review selected changes systematically, follow their actual behavior, and prevent hypothetical failures from generating unnecessary fixes. Reduce irrelevant runtime instructions through shared, conditionally loaded standards. Keep useful incremental maintenance in default review and implement it automatically by default in repair workflows.

A defect is a reachable violation attributable to the selected change with concrete impact. A verification gap is missing necessary evidence for an applicable obligation or material risk. A pure maintenance suggestion improves current readability, maintainability, or extensibility without claiming a functional failure.

## User Scenarios and Acceptance

### Review actual behavior (P1)

A developer requests review of a change spanning a producer, consumer, and unchanged dependency.

- The reviewer accounts for every selected change, identifies affected entry points and contracts, and traces relevant call/data/state relationships.
- The reviewer checks normal and evidenced failure, denial, cancellation, recovery, and compatibility paths.
- An existing upstream guarantee that covers the path prevents an unsupported defect report.
- Rare reachable failures and credible malicious input remain reviewable.
- A verified recurring cause triggers a bounded search of equivalent and symmetric paths.

### Load applicable standards (P1)

A reviewer handles a Python change, discovering a Go dependency and a required authorization behavior that is missing.

- Common discipline and the selected mode's procedure are loaded.
- Every dimension receives a short applicability assessment; only applicable detail is read.
- Python details are selected from actual semantics; tracing activates relevant Go and authorization sections.
- The missing authorization implementation does not deactivate the required check.
- The result records selected standards, rationale, scope, evidence, and completion.
- Missing required resources or uninspectable necessary evidence are visible; unrelated details are not mandatory work.

### Maintain incrementally (P1)

An implementation command invokes review and repairs findings.

- With configuration absent or enabled, substantiated maintenance suggestions join automatic repair.
- With configuration disabled, the same suggestions remain visible but are not automatically implemented.
- Actual defects and necessary verification remain mandatory in either case.
- Maintenance explains a current problem, a concrete improvement, and current benefit; fixes preserve intended behavior and public compatibility.

### Configure and install (P2)

A user configures the project and initializes supported integrations.

- `codexspec config --auto-maintenance on|off` persists a boolean.
- Repair commands read the selected project's configuration without a new invocation argument.
- Manual and automatically reached implementation obey the same policy.
- CLI initialization and installation updates provide shared resources under `.codexspec/review-code/`.
- Claude and Codex entries resolve the same installed standards; CLI-tool installation alone creates no project files.
- Supported plugin-only delivery retains access to usable standards without maintainer-only runtime dependencies.

## Functional Requirements

### REQ-001: Establish review direction and account for scope

Determine affected behaviors, entry points, contracts, callers, and dependencies before detail. Allocate depth by concrete impact and risk. Account for all selected changes; file-reading completion is insufficient.

Sources: NEED-001, DEC-002.

### REQ-002: Trace relevant behavior and bounded related occurrences

Trace producers, consumers, state transitions, and external boundaries, including relevant unchanged code. Cover normal and evidenced alternate paths. For a verified repeatable cause inspect equivalent and symmetric occurrences within a justified affected scope.

Sources: NEED-002, CON-006.

### REQ-003: Admit only evidenced defects

Establish operating context, triggering-condition origin, reachability, violated contract/behavior, concrete impact, and change attribution through reproduction or deterministic argument. Rarity alone does not exclude credible failures or malicious input.

Sources: NEED-003, CON-001, OUT-002.

### REQ-004: Test existing guarantees and handle uncertainty proportionately

Check actual upstream validation, types, state/order, framework and recovery guarantees, including whether they cover the path. Require a reachable bypass before recommending additional defensive handling. Resolve uncertain applicability through bounded inspection. Only missing necessary evidence for an applicable obligation or material risk constitutes a blocking gap.

Sources: NEED-004, CON-001, CON-004, DEC-003.

### REQ-005: Load common and mode procedures at runtime

Keep the coordinating command separate from mandatory common discipline, selected-mode procedures, and applicable detailed standards. Runtime loading must reduce unrelated context; expanding all authoring fragments into one command is insufficient. Preserve selected scope, correctness, risks, verification, and finding admission.

Sources: NEED-005, CON-003, DEC-001, DEC-006.

### REQ-006: Select and expand standards using semantic evidence

Use a lightweight index, affected behavior map, and brief assessment of every dimension. Select detail from binding obligations, constraints, language/version semantics, call/data relationships and dependencies. Extensions/keywords provide candidates only. Tracing may activate unchanged or cross-language dependencies; missing required implementation can activate checks.

Sources: NEED-006, CON-003, CON-004, DEC-002, DEC-003.

### REQ-007: Make standards and coverage inspectable

Each standard describes purpose, applicability/non-applicability, checkpoints, necessary evidence, false positives, and completion. Index entries contain conditions and locations, not full checklists. Record selected standards, reasons, scope, completion, and key evidence. Additional standards preserve admission and completion rules. Required missing resources cannot be silently skipped.

Sources: NEED-007, CON-003, DEC-001.

### REQ-008: Integrate every supplied checklist item

Account for all 87 source bullets, including five false-positive items, with destinations and retain/generalize/split/rewrite/exclude rationale. Generalize language-independent intent; retain actual language semantics in specialized standards. HTTP, database, upload and browser topics are not language identities. Future distributed standards must not depend on the external source pathname.

Sources: NEED-008, CON-004, DEC-006.

### REQ-009: Review maintenance in the default change mode

Assess readability, maintainability and extensibility in selected changes and directly affected structure. Explain the present structural/comprehension problem, concrete improvement and substantiated benefit. A suggestion need not be a functional defect, but respects actual requirements, compatibility and conventions. Keep suggestions distinguishable from defects.

Sources: NEED-009, NEED-010, CON-001, CON-005, DEC-004, OUT-002.

### REQ-010: Apply the configured maintenance policy at repair time

Implementation callers, including `implement-tasks`, include substantiated incremental maintenance in automatic repair by default. Read persistent configuration; disabled policy leaves suggestions visible without applying them. Defect repair and required verification remain mandatory. Review itself remains read-only and always assesses/reports applicable maintenance.

Sources: NEED-009, NEED-010, CON-005, CON-006, DEC-004, DEC-009.

### REQ-011: Provide independent persistent configuration

Add `workflow.auto_maintenance` in `.codexspec/config.yml`, default `true` including absent existing keys. Manage through `codexspec config --auto-maintenance on|off`; canonical help/examples use on/off. Accept case-insensitive, surrounding-whitespace-normalized aliases on/true/1/yes and off/false/0/no. Store unquoted YAML booleans and use internal booleans.

No maintenance argument, per-run override, priority hierarchy, or preceding-stage forwarding is added to implementation commands. `workflow.auto_next` controls stage advance independently; manual and automatic implementation behave identically.

Sources: NEED-009, CON-005, DEC-009.

### REQ-012: Ship the confirmed compact resource layout

Maintain `templates/review-code/{index,common,change-review,quality-assessment}.md`; seven `dimensions/{logic,business-semantics,security,concurrency,robustness,performance,maintainability}.md` files; initially one file per supported language/framework, including Go, Python and React. Install the same tree at `.codexspec/review-code/` through project initialization/update, shared by integrations.

Keep the main authoritative source at `internal/command_templates/sources/review-code.md`, render `templates/commands/review-code.md`, and derive installed Claude/Codex entries. CodexSpec's own installed copies are not additional sources. Tool-only installation creates no project resources.

Sources: NEED-005, CON-007, DEC-006.

### REQ-013: Split further only for independently useful topics

Keep authentication, authorization, transactions, cache, uploads, and language error/collection details as sections in corresponding files initially. Split only a substantial independent review theme whose current organization repeatedly loads unrelated content. Do not pre-create per-checkpoint/topic files, per-language subdirectories or separate scoring files; no arbitrary line-count threshold.

Sources: NEED-005, CON-007, DEC-006.

### REQ-014: Bound completion and verify edits

Complete applicable behavior, contract, risk, deterministic verification and justified related-occurrence work, plus substantiated incremental maintenance when enabled. Preserve behavior/public compatibility and verify changed code. Stop once obligations are complete; expand only for newly evidenced dependencies, risks or relevant maintenance needs.

Sources: NEED-010, CON-001, CON-006, OUT-002.

## Non-Functional Requirements

### NFR-001: Prevent language leakage and unnecessary defense

Evaluate nullability, missing keys, ordering, numeric limits, ignored results and recovery against actual semantics/contracts. Do not admit invented unreachable states, unsupported environments, future product obligations, unnecessary defenses/abstractions or unrelated broad cleanup. Maintenance with current substantiated benefit remains permitted.

Sources: CON-001, CON-004, CON-006, OUT-002.

### NFR-002: Keep delivery complete and extensible

User runtime resources are complete shipping assets independent of maintainer-only sources/tools. Adding standards preserves applicability, defect admission, maintenance assessment and bounded completion. Runtime selection must avoid indiscriminate loading of unrelated bodies.

Sources: NEED-005, NEED-007, CON-003, CON-007, DEC-006.

## Success Criteria

- Every selected change is accounted for through behavior, contract and applicable risk coverage.
- Every admitted defect has reachable, consequential, change-attributed evidence; blocked verification identifies its applicable obligation.
- Evaluations distinguish a real failure from the same candidate prevented by an existing guarantee, and useful maintenance from speculative refactoring.
- Evaluations activate missing required behavior and newly traced cross-language dependencies without loading irrelevant detailed bodies.
- All 87 supplied items have an explicit destination and rationale.
- Initialization/update and packaged assets provide the compact resource tree to supported consumers.
- Configuration tests cover default, on/off aliases, persistent booleans and independence from auto-next; disabling maintenance never hides advice or waives defects.
- Repair workflows keep findings/report evidence coherent and complete verified, behavior-compatible edits.

## Constraints and Out of Scope

The confirmed runtime layout and configuration boundary are binding. The source checklist provides review prompts, not authority to invent product requirements. No per-run maintenance override, preceding-stage propagation, arbitrary fragmentation threshold, speculative defenses or unrelated broad cleanup is included.

## Open Design Choices

OPEN-002 remains non-blocking: choose the index format, installation/resource resolution across supported delivery channels (including plugin-only delivery), runtime configuration access, and safe report consumption/versioning during design. These choices cannot reopen confirmed interfaces or expand product scope.

## Requirements Traceability

| Confirmed Entry | Coverage |
|-----------------|----------|
| NEED-001 | REQ-001 |
| NEED-002 | REQ-002 |
| NEED-003 | REQ-003 |
| NEED-004 | REQ-004 |
| NEED-005 | REQ-005, REQ-012, REQ-013, NFR-002 |
| NEED-006 | REQ-006 |
| NEED-007 | REQ-007, NFR-002 |
| NEED-008 | REQ-008 |
| NEED-009 | REQ-009, REQ-010, REQ-011 |
| NEED-010 | REQ-009, REQ-010, REQ-014 |
| CON-001 | REQ-003, REQ-004, REQ-009, REQ-014, NFR-001 |
| CON-003 | REQ-005, REQ-006, REQ-007, NFR-002 |
| CON-004 | REQ-004, REQ-006, REQ-008, NFR-001 |
| CON-005 | REQ-009, REQ-010, REQ-011 |
| CON-006 | REQ-002, REQ-010, REQ-014, NFR-001 |
| CON-007 | REQ-012, REQ-013, NFR-002 |
| DEC-001 | REQ-005, REQ-007 |
| DEC-002 | REQ-001, REQ-006 |
| DEC-003 | REQ-004, REQ-006 |
| DEC-004 | REQ-009, REQ-010 |
| DEC-006 | REQ-005, REQ-008, REQ-012, REQ-013, NFR-002 |
| DEC-009 | REQ-010, REQ-011 |
| OUT-002 | REQ-003, REQ-009, REQ-014, NFR-001 |
