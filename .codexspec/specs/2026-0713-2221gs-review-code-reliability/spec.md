# Feature Specification: Reliable Change-Scoped Code Review

<!--
Language: English, as configured by .codexspec/config.yml.
This specification is compiled from confirmed requirements.md entries.
-->

**Feature Branch**: `2026-0713-2221gs-review-code-reliability`
**Created**: 2026-07-14
**Status**: Draft
**Input**: Confirmed requirements at `.codexspec/specs/2026-0713-2221gs-review-code-reliability/requirements.md`

## Context

The current `review-code` workflow presents broad quality analysis as a complete review but can miss actionable defects introduced by the selected change. CodexSpec needs a stricter change-scoped defect gate that establishes exactly what was reviewed, applies requirements and risk evidence at the appropriate depth, distinguishes defects from incomplete evidence, and exposes a machine-stable result to `implement-tasks`.

The existing whole-path quality scorecard remains useful, but it has different semantics and must be invoked explicitly as an advisory audit. The defect gate must favor evidence completeness and defect recall over review speed, while avoiding speculative findings and preserving direct review usability when feature artifacts are unavailable.

## Goals

- Make the default `review-code` operation a reliable, change-scoped pre-merge defect gate.
- Resolve and inventory the selected Git target deterministically without mutating repository state.
- Use confirmed feature artifacts to assess implementation conformance and, only for complete feature targets, requirements completeness.
- Apply mandatory behavior, risk, and verification passes with independent specialist review for high-impact changes.
- Give direct callers and `implement-tasks` a strict, fail-closed verdict and result contract.
- Prove deterministic orchestration in normal CI and evaluate real reviewer quality with reusable synthetic fixtures.

## User Scenarios and Testing

### User Story 1 - Review a complete feature change (Priority: P1)

As a developer preparing a feature for merge, I want `review-code` to inspect the complete feature delta and relevant requirements so that a clean result means the delivered feature has no known qualifying defect and its required evidence was actually examined.

**Why this priority**: This is the primary failure mode and the core value of the feature.

**Independent Test**: In a temporary repository, create committed, staged, unstaged, and untracked feature changes plus matching feature artifacts, invoke `review-code`, and verify that the resolved target includes every non-ignored entry, all four review stages complete, and the report returns a valid terminal envelope.

**Acceptance Scenarios**:

1. **Given** a feature branch with committed, staged, unstaged, and untracked changes, **When** the developer invokes `review-code` without a target selector, **Then** the review covers the complete feature delta from the resolved merge base through the current working tree.
2. **Given** a uniquely resolved feature directory and a complete feature target, **When** the review runs, **Then** it checks both implementation conformance and full requirements completeness.
3. **Given** every mandatory stage and verification step completes with no qualifying findings, **When** the report is finalized, **Then** it emits `PASS` with a valid result envelope whose counts and statuses agree with the human-readable report.

### User Story 2 - Select an unambiguous review operation (Priority: P1)

As a developer investigating a specific change, I want explicit target selectors and a distinct audit mode so that I know whether the result covers a branch delta, uncommitted work, one commit, or whole-file quality.

**Why this priority**: Ambiguous scope can produce a clean result for the wrong evidence.

**Independent Test**: Exercise the default, `--committed`, `--uncommitted`, `--commit`, and `--audit` forms against a repository with different changes in each Git state and verify that every invocation selects only its defined target and reports its limited semantics.

**Acceptance Scenarios**:

1. **Given** committed and uncommitted feature work, **When** `review-code --committed` runs, **Then** only the merge-base-to-HEAD net diff is reviewed and excluded uncommitted work is disclosed.
2. **Given** one normal, root, or merge commit, **When** `review-code --commit <sha>` runs, **Then** the resolver uses the defined parent semantics and discloses the selected parent.
3. **Given** a path supplied through `--audit`, **When** the command runs, **Then** it performs the advisory whole-path quality scorecard rather than a patch-correctness gate.
4. **Given** a bare path or conflicting selectors, **When** the command is invoked, **Then** it returns an actionable error and an `INCONCLUSIVE` defect-gate envelope instead of inferring another mode.

### User Story 3 - Receive risk-appropriate independent review (Priority: P1)

As a developer changing a high-impact boundary, I want the review to activate relevant risk scenarios and an independent specialist so that authorization, command execution, injection, destructive operations, and comparable defects are not hidden by a single general pass.

**Why this priority**: High-impact defects require independent, adversarial evidence before a merge-ready result is credible.

**Independent Test**: Review synthetic high-risk changes and verify semantic profile activation, trigger evidence, isolated primary and specialist execution, independent inputs, merged qualifying findings, and fail-closed behavior when either required reviewer cannot complete.

**Acceptance Scenarios**:

1. **Given** a semantically high-risk change, **When** Risk Pass runs, **Then** it records each activated profile and the evidence that triggered it.
2. **Given** specialist review is required, **When** either the primary or specialist review is missing, malformed, or incomplete, **Then** the final verdict is `INCONCLUSIVE`.
3. **Given** primary and specialist reviewers disagree, **When** their outputs are coordinated, **Then** qualifying findings are unioned and deduplicated without discarding a finding merely because the other reviewer missed it.

### User Story 4 - Complete implementation only after a clean re-review (Priority: P1)

As a developer using `implement-tasks`, I want reported defects verified before edits and the complete feature re-reviewed after each fix so that false positives are not implemented and successful completion cannot hide remaining defects or regressions.

**Why this priority**: `implement-tasks` consumes the review result as its completion gate.

**Independent Test**: Feed the workflow verified defects, refuted findings, transient inconclusive results, and repeated no-progress outcomes; verify TDD repair behavior, fresh complete-feature re-reviews, retry limits, stop guards, and successful completion only on a valid final `PASS` envelope.

**Acceptance Scenarios**:

1. **Given** a reported functional defect, **When** `implement-tasks` independently confirms it, **Then** it first creates a reproducing regression test, applies the fix, and runs targeted plus mandatory verification.
2. **Given** a reported finding cannot be reproduced or supported by evidence, **When** it is independently checked, **Then** no edit is made solely to satisfy that finding.
3. **Given** fixes have been applied, **When** review repeats, **Then** a fresh reviewer evaluates the complete feature delta rather than only the files just changed.
4. **Given** a valid P0 through P3 finding remains, **When** the workflow reaches a terminal state, **Then** it does not claim successful completion.

### User Story 5 - Install and validate deterministic review context (Priority: P2)

As a CodexSpec maintainer, I want project-local cross-platform scope resolvers and reproducible contract tests so that initialized projects do not depend on an installed CodexSpec runtime and the reviewer cannot silently invent or omit its target.

**Why this priority**: Deterministic scope is foundational evidence for every defect-gate verdict.

**Independent Test**: Initialize supported test projects, run the installed Bash or PowerShell resolver in temporary Git repositories, compare manifests against shared fixtures, and verify equivalent output, no repository mutation, and fail-closed template behavior for missing or incompatible helpers.

**Acceptance Scenarios**:

1. **Given** a newly initialized project, **When** the applicable platform artifacts are installed, **Then** a project-local read-only resolver is available under `.codexspec/scripts/` without requiring the CodexSpec CLI at review time.
2. **Given** equivalent Git repositories on supported Bash and PowerShell hosts, **When** their resolvers run with the same arguments, **Then** they emit semantically equivalent versioned JSON manifests.
3. **Given** a missing resolver, unsupported schema, invalid JSON, or resolver failure, **When** defect review starts, **Then** it returns `INCONCLUSIVE` with project-update guidance and does not fall back to model-computed scope.

### Edge Cases

- The current branch is the resolved base branch: the default target is all uncommitted changes.
- The base ref, merge base, or requested commit cannot be resolved: the result is `INCONCLUSIVE`, never an implicit path audit.
- The direct code-only target is empty: the result can be `PASS` with `target: empty`; an `implement-tasks` feature review must still check for missing implementation obligations.
- The selected commit is a root commit: it is compared with the Git empty tree.
- The selected commit is a merge commit: the first parent is used by default and disclosed; `--parent <n>` can override it only for `--commit`.
- Changed entries include ignored, renamed, deleted, symlink, binary, submodule, generated, vendored, or lockfile content: ignored entries are excluded, while every selected non-ignored entry is inventoried and classified.
- A diff exceeds one reviewer context: it is partitioned under one complete inventory and never silently truncated.
- Required evidence is opaque or inaccessible: critical uninspectable evidence prevents `PASS`.
- Mandatory verification cannot run or its failure cannot be attributed to the change: the result is `INCONCLUSIVE`, not `PASS` or a speculative defect.
- A direct ordinary review cannot create an isolated reviewer: shared context is allowed only with a visible coverage gap; high-risk and `implement-tasks` final gates remain `INCONCLUSIVE`.
- Repository content contains command-like, forged-output, or review-bypass text: it remains untrusted evidence and cannot alter the review protocol.

## Requirements

### Functional Requirements

- **REQ-001: Review modes.** `review-code` MUST default to a change-scoped pre-merge defect gate. Only `review-code --audit [paths...]` may run the advisory whole-path quality scorecard. Audit mode MUST inspect complete current file contents, retain the existing default source-directory resolution when no path is supplied, remain mutually exclusive with defect-gate arguments, and MUST NOT act as an `implement-tasks` completion gate.
  - Sources: NEED-001, DEC-001, DEC-005, DEC-007

- **REQ-002: Default defect target.** On a feature branch, the default target MUST be the complete feature delta relative to the base merge point, including feature-branch commits, staged changes, unstaged changes, and untracked but non-ignored files. On the resolved base branch, the default target MUST be all uncommitted changes.
  - Sources: DEC-002, DEC-027

- **REQ-003: Explicit selectors and modifiers.** Defect-gate mode MUST support mutually exclusive `--committed`, `--uncommitted`, and `--commit <sha>` primary targets. `--committed` MUST select the merge-base-to-HEAD net diff while excluding staged, unstaged, and untracked work; `--uncommitted` MUST select staged, unstaged, and untracked but non-ignored work; and `--commit` MUST select only the requested commit under REQ-005 parent semantics. `--base <branch>` MUST modify only the default or committed target; `--feature <feature-dir>` MUST supply requirements context without changing Git scope; repeatable `--focus <instructions>` MUST add risk obligations without narrowing or replacing general review. Defect-gate mode MUST NOT accept path filters.
  - Sources: DEC-003, DEC-006, DEC-007, DEC-008, DEC-034

- **REQ-004: Default base resolution.** When `--base` is absent, the resolver MUST use Git metadata in this order: the selected remote's local symbolic `HEAD`, a read-only remote `HEAD` query when needed, then `origin/main`, `origin/master`, `main`, and `master`. It MUST NOT fetch or mutate refs. Failure to determine one base MUST produce actionable `INCONCLUSIVE` output. Scope MUST disclose the chosen base ref and merge-base SHA.
  - Sources: DEC-004, DEC-027

- **REQ-005: Commit parent semantics.** `--commit <sha>` MUST compare a normal commit with its parent, a root commit with the Git empty tree, and a merge commit with its disclosed first parent by default. `--parent <n>` MUST be valid only with `--commit`, MUST select that merge parent, and MUST produce `INCONCLUSIVE` for an invalid index. `--committed` MUST remain a merge-base-to-HEAD net diff and MUST NOT use `--parent`.
  - Sources: DEC-028

- **REQ-006: Argument validation and migration.** Bare path calls such as `review-code src/`, conflicting modes or selectors, and invalid defect-gate arguments MUST fail with an actionable error and an `INCONCLUSIVE` result envelope. Bare paths MUST direct the user to `review-code --audit <path>` and MUST NOT be inferred as audit activation or a narrowed defect target. Documentation, examples, translations, workflow callers, tests, and release notes MUST migrate atomically without a compatibility period.
  - Sources: DEC-029

- **REQ-007: Project-local resolver distribution.** CodexSpec MUST ship equivalent Bash and PowerShell implementations that validate review arguments, resolve base, merge-base, commit parent and feature context, and inventory the complete selected target. The existing initialization flow MUST copy the applicable helper into the initialized project's `.codexspec/scripts/`. The review template MUST invoke that local helper without requiring an installed CodexSpec CLI. The helper MUST emit a versioned JSON manifest to stdout.
  - Sources: DEC-035

- **REQ-008: Resolver compatibility gate.** The review workflow MUST accept only supported manifest schema versions. A missing helper, command failure, invalid JSON, unsupported schema, or incomplete manifest MUST produce `INCONCLUSIVE` with actionable project-update guidance. The reviewer MUST NOT compute a replacement Git scope itself.
  - Sources: DEC-036

- **REQ-009: Requirements context and coverage.** A complete feature target with resolved feature artifacts MUST assess both full requirements completeness and implementation conformance. `--uncommitted` and `--commit` MUST assess only affected-requirement conformance. `--committed` MUST assess full completeness when no uncommitted target content is excluded and MUST otherwise assess only affected-requirement conformance. Direct review MUST auto-match only a unique branch feature unless `--feature` is explicit; unresolved context MAY yield code-level `PASS` only with `Requirements coverage: not evaluated` and no whole-feature-readiness claim. `implement-tasks` MUST provide its feature directory, and missing or unreadable required artifacts MUST make its review `INCONCLUSIVE`.
  - Sources: NEED-002, DEC-007, DEC-008, DEC-011, DEC-027

- **REQ-010: Mandatory review stages.** Every defect-gate invocation MUST complete Scope, Behavior, Risk, and Verification passes. Scope MUST resolve and inventory evidence; Behavior MUST trace changed entry points, call chains, data flows, failure paths, compatibility, concurrency, and resources; Risk MUST independently re-inspect applicable specialist evidence; Verification MUST run applicable deterministic checks, validate finding triggers and impacts, remove speculation and duplicates, and derive the verdict and coverage gaps. `--focus` MAY only add Risk Pass obligations.
  - Sources: NEED-001, DEC-006, DEC-009

- **REQ-011: Complete artifact inventory.** Scope Pass MUST inventory every selected entry without source-extension filtering, including code, tests, configuration, schema, migration, scripts, CI and release files, manifests, lockfiles, documentation, templates, assets, CodexSpec artifacts, renames, deletions, symlinks, binaries, submodules, generated output, and vendored content. Documentation-only and configuration-only targets MUST still be reviewed. CodexSpec artifacts MUST be checked both as requirements evidence and for unauthorized intent drift. Every entry MUST end as `reviewed`, `verified by tool/generator`, `excluded with explicit justification`, or `uninspectable`.
  - Sources: DEC-021, DEC-022

- **REQ-012: Opaque, derived, and large target handling.** Generated content MUST be checked against its source and generator, lockfiles against manifests and dependency intent, vendored content against available provenance, and binary or submodule changes against available metadata and referenced content. Large targets MUST be partitioned under one complete inventory without truncation. Unclassified entries or critical uninspectable evidence MUST prevent `PASS`.
  - Sources: DEC-022, DEC-034

- **REQ-013: Risk profiles and activation.** Risk Pass MUST provide cross-language profiles for authorization/trust, command/process execution, filesystem/path handling, parsing/configuration, persistence/state, network/provider behavior, concurrency/lifecycle, public API/CLI compatibility, secrets/injection, and build/dependency behavior. It MUST activate one or more profiles from semantic diff, call-chain, dependency, and feature evidence rather than keywords alone; record each activation and trigger in Scope; exercise relevant normal, denial/failure, boundary, bypass, and compatibility scenarios; and return `INCONCLUSIVE` when critical high-risk evidence cannot be inspected. Behavior Pass MUST still perform general correctness review when no profile matches.
  - Sources: DEC-016, DEC-017

- **REQ-014: Independent specialist review.** Semantically high-impact trust, authorization, command execution, injection, secrets, destructive filesystem, data migration, or comparable changes MUST receive at least one fresh specialist review in addition to the primary review. A specialist MUST receive raw target evidence, relevant call chains, feature artifacts, and activated obligations, but not primary findings. The coordinator MUST union and deduplicate qualifying outputs without suppressing an independently reported finding solely because another reviewer missed it. Missing, failed, malformed, or incomplete required specialist execution MUST yield `INCONCLUSIVE`.
  - Sources: DEC-025, DEC-026

- **REQ-015: Reviewer isolation.** Defect-gate review MUST use a fresh review-only context by default and MUST use another fresh context after each fix. It MUST receive only the review contract, selected target, environment facts, authoritative project and feature context, and needed tool access; it MUST NOT inherit implementation reasoning, prior conclusions, or previous findings, and MUST NOT apply fixes. Ordinary direct review MAY visibly fall back to shared context, but high-risk review and the `implement-tasks` final gate MUST be `INCONCLUSIVE` when isolation is unavailable. Audit mode need not be isolated.
  - Sources: DEC-023, DEC-024

- **REQ-016: Verification selection.** Verification MUST select commands in this order: explicit project and feature instructions, existing CI or project-script entry points, standard build-manifest commands, then optional language-default analyzers. Applicable project-mandated and targeted component checks MUST run. A full suite MUST run when mandated or when shared-boundary impact cannot be validated locally. Pure documentation changes MUST run only applicable declared documentation checks. Every executed command and outcome MUST be reported.
  - Sources: DEC-012

- **REQ-017: Verification safety and classification.** Review verification MUST NOT modify project files or implementation state: it MUST NOT install or update dependencies, rewrite lockfiles, format in write mode, publish, deploy, or run migrations. An unavailable mandatory check MUST yield `INCONCLUSIVE`; missing optional tooling MUST be a visible coverage gap and MUST NOT independently prevent `PASS`. A deterministic failure MUST yield `FAIL` only when attributable to the selected change, otherwise `INCONCLUSIVE`.
  - Sources: DEC-013

- **REQ-018: Finding admission and test gaps.** Every finding MUST be a discrete, actionable P0-P3 defect introduced, worsened, or made reachable by the selected change; have concrete trigger and impact evidence; affect correctness, security, performance, reliability, compatibility, or confirmed intent; and warrant repair before merge. Every admitted priority MUST make the verdict `FAIL`. Test absence MUST be a finding only for a binding obligation, a concrete changed behavior or failure path without equivalent deterministic evidence, regression protection for a verified fix, or an unevidenced high-risk denial, bypass, or failure path. Existing indirect tests MUST count when they demonstrably cover the contract, and behavior-preserving refactors MUST NOT require redundant tests. When no binding test requirement exists, absent tests MUST be recorded as a coverage gap and MUST prevent `PASS` only when the change risk has no adequate substitute evidence. The report MUST exclude style preferences, generic coverage advice, praise, and general refactoring opportunities.
  - Sources: DEC-014, DEC-032

- **REQ-019: Human-readable report.** Defect-gate reports MUST contain only Verdict, Scope, Findings, Requirements Coverage, Verification Summary, and Coverage Gaps. Findings MUST cite the shortest useful changed location; omitted-requirement findings MAY cite the authoritative requirement and nearest implementation boundary; verification findings MUST cite the command and relevant code. Unverified material concerns MUST be evidence gaps, not speculative findings. Defect-gate output MUST NOT include a quality score, strengths section, or recommendation catalog.
  - Sources: DEC-015

- **REQ-020: Machine result envelope.** Every defect-gate report MUST end with exactly one `<review-code-result>` containing one valid JSON object with fixed English field names and enums. It MUST include `schema_version`, `mode`, `verdict`, `target`, `requirements_coverage`, `verification`, P0-P3 finding counts, coverage-gap count, `review_context`, and primary and specialist execution states. Envelope data MUST agree with the human report and all PASS invariants. Missing, malformed, contradictory, unsupported, or unknown data MUST be interpreted as `INCONCLUSIVE`; callers MUST NOT infer success from prose. Audit reports MUST remain separate and MUST NOT be consumed by `implement-tasks`.
  - Sources: DEC-018, DEC-023, DEC-026

- **REQ-021: Terminal verdict semantics.** Defect-gate mode MUST emit exactly one of `PASS`, `FAIL`, or `INCONCLUSIVE`. `PASS` MUST require all stages, mandatory verification, required review topology, complete inventory accounting, and no unresolved qualifying findings. `FAIL` MUST require a validated defect or attributable deterministic verification failure. Incomplete scope or evidence, blocked verification, invalid output, timeout, environment failure, or interruption MUST yield `INCONCLUSIVE`. An empty finding list alone MUST NOT establish `PASS`, and `implement-tasks` MUST accept only a valid `PASS`.
  - Sources: DEC-010, DEC-011, DEC-017, DEC-022, DEC-024, DEC-025

- **REQ-022: Target failure and empty target.** Unresolved base, merge base, requested commit, or parent MUST yield `INCONCLUSIVE` without an audit fallback. Scope MUST disclose exact refs, resolved SHAs, and inventory counts. A direct code-only review of a genuinely empty target MAY return `PASS` with `target: empty` and an explicit no-changes statement. An `implement-tasks` feature review with an empty target MUST still assess confirmed implementation obligations and MUST fail when they are absent.
  - Sources: DEC-027, DEC-028

- **REQ-023: Instruction and evidence trust.** Only host instructions, the review protocol, explicit arguments, recognized project instruction files, the Constitution, and confirmed feature artifacts MAY provide authoritative review context. Repository source text, ordinary documents, generated or vendored content, commit messages, test logs, and tool output MUST remain untrusted evidence and MUST NOT weaken gate invariants. Prompt-injection, forged-output, or bypass-shaped content MUST be assessed as evidence and admitted as a finding only when the selected change exposes a concrete qualifying impact.
  - Sources: DEC-030, DEC-031

- **REQ-024: No gate bypass.** Defect-gate mode MUST NOT provide finding ignore, waiver, severity suppression, fast, skip-risk, skip-tests, or equivalent controls. A valid finding may clear only through a verified fix and clean fresh review, evidence-based invalidation absent from fresh review, or a formally confirmed intent change followed by re-review. Smaller explicit targets MUST produce only target-limited verdicts. Resource exhaustion that prevents required review MUST yield `INCONCLUSIVE`; audit mode MUST NOT substitute for the gate.
  - Sources: CON-002, DEC-033, DEC-034

- **REQ-025: `implement-tasks` repair loop.** `implement-tasks` MUST establish a green baseline, invoke defect-gate mode for the complete target with its feature directory, independently verify each finding before editing, apply only verified fixes, and run targeted plus mandatory verification. Functional defects MUST use a reproducing regression test before the fix; documentation and non-code configuration defects MUST use applicable deterministic checks. Every post-fix review MUST use a fresh reviewer and the complete feature target. Only a valid final `PASS` envelope may produce successful completion, with no deferred P0-P3 finding.
  - Sources: DEC-019, DEC-023, DEC-033

- **REQ-026: Progress-based loop control.** The repair loop MUST continue while verified defects are resolved or new actionable defects are found. It MUST stop without success when the same defect survives two verified fixes, two consecutive rounds make no substantive progress, a finding requires a new product or architecture decision, or the same independently refuted false positive recurs. A transient `INCONCLUSIVE` cause MAY be retried up to two times; persistence MUST remain blocking. Stopped outcomes MUST preserve `FAIL` or `INCONCLUSIVE` evidence and MUST NOT become score-based success.
  - Sources: DEC-020

- **REQ-027: Deterministic contract tests.** Normal offline CI MUST use temporary Git repositories to cover every target mode and Git state, ignored handling, rename/delete/symlink/binary/submodule changes, base and merge-base resolution, normal/root/merge commit parent behavior, empty and error cases, resolver schema, Bash/PowerShell semantic parity, and no mutation. Template and integration tests MUST cover argument contracts, mode exclusivity, four stages, result envelope handling, supported-host installation, the `implement-tasks` clean-PASS loop, and removal of legacy bare-path semantics without requiring an LLM or network.
  - Sources: DEC-037

- **REQ-028: Model-assisted quality evaluation.** The development repository MUST provide source-independent synthetic defect and clean-patch fixtures with expected risk profiles, minimum qualifying findings, forbidden speculative findings, and expected verdicts. These fixtures MUST NOT be copied into initialized user projects or run in normal CI. Feature acceptance MUST include one complete recorded evaluation run on at least one supported host, and the corpus MUST remain reusable for later review-protocol regressions.
  - Sources: NEED-001, CON-001, CON-002, DEC-038

### Non-Functional Requirements

- **NFR-001: Evidence completeness over speed.** Review latency, token use, or target size MUST NOT justify skipping, truncating, or weakening mandatory review stages, inventory, verification, isolation, or specialist coverage.
  - Sources: CON-002, DEC-022, DEC-034

- **NFR-002: Source-independent product artifacts.** Requirements, specification, plan, tasks, and persistent evaluation cases MUST describe CodexSpec behavior without retaining external implementation-research paths, symbols, or replication constraints.
  - Sources: CON-001, DEC-038

- **NFR-003: Deterministic and non-mutating scope resolution.** Resolver behavior MUST be reproducible, read-only, project-local, and semantically equivalent across supported Bash and PowerShell hosts.
  - Sources: DEC-004, DEC-035, DEC-037

- **NFR-004: Fail-closed interoperability.** Machine consumers MUST have one versioned, language-neutral result contract and MUST interpret any missing or incompatible required structure as `INCONCLUSIVE` rather than success.
  - Sources: DEC-018, DEC-026, DEC-036

### Key Entities

- **Review Mode**: Either the change-scoped defect gate or the advisory whole-path audit.
- **Review Target**: The resolved Git evidence selected by default behavior or one explicit target selector, including refs, SHAs, parent semantics, inventory, and excluded states.
- **Review Context Manifest**: The versioned JSON emitted by the project-local resolver, containing validated arguments, resolved target metadata, feature context, and complete inventory.
- **Risk Profile**: A reusable cross-language set of behavior, failure, boundary, bypass, and compatibility obligations activated by semantic evidence.
- **Finding**: An evidence-backed P0-P3 defect with a concrete trigger, impact, location, and relationship to the selected change.
- **Coverage Gap**: Missing or degraded review evidence that is not itself a validated defect and can make the verdict `INCONCLUSIVE` when required.
- **Result Envelope**: The fixed-English, versioned JSON contract consumed by workflow callers.

## Expected Error Behavior

| Condition | Required Result |
|---|---|
| Ambiguous or invalid arguments | Actionable error plus `INCONCLUSIVE` envelope |
| Legacy bare path | Guidance to use `--audit`; no inferred execution |
| Base, merge base, commit, or parent unresolved | `INCONCLUSIVE`; no audit fallback |
| Resolver missing, invalid, failed, or schema-incompatible | `INCONCLUSIVE` plus project-update guidance |
| Required artifact missing in `implement-tasks` | `INCONCLUSIVE` |
| Mandatory verification unavailable | `INCONCLUSIVE` |
| Verification failure attributable to selected change | `FAIL` |
| Verification failure with unresolved attribution | `INCONCLUSIVE` |
| Required isolation or specialist unavailable | `INCONCLUSIVE` |
| Valid P0-P3 defect | `FAIL` |
| Critical evidence inaccessible or inventory incomplete | `INCONCLUSIVE` |
| Direct code-only empty target | `PASS` with `target: empty`, subject to all applicable gate invariants |
| Malformed or contradictory final envelope | `INCONCLUSIVE` |

## Confirmed Constraints and Decision Boundaries

- Defect gating and whole-path quality scoring are separate operations with separate result semantics.
- Git target, review mode, and requirements context are orthogonal; requirements conclusions cannot exceed target completeness.
- All four review stages and applicable independent coverage remain mandatory, with no fast or waiver path.
- Verification and scope resolution are read-only and fail closed when required evidence cannot be established.
- Defect reports remain compact and evidence-oriented; quality advice remains in audit mode.
- Distributed command changes must be made in `templates/commands/`, the CodexSpec source of truth required by the project Constitution, rather than generated `.claude/commands/codexspec/` install artifacts.
- The project-local resolver is distributed by initialization and does not create a runtime dependency on an installed CodexSpec CLI.
- No external implementation-research details may appear in this specification or downstream SDD artifacts.

## Success Criteria

- **SC-001**: Every deterministic target fixture resolves to the expected refs, SHAs, parent, feature context, and complete inventory on each supported resolver implementation, with no repository-state mutation.
- **SC-002**: Every selected non-ignored change entry in deterministic fixtures receives exactly one final inventory classification; no fixture can reach `PASS` with an unclassified entry or critical uninspectable evidence.
- **SC-003**: All invalid, missing, incompatible, and incomplete resolver or result-envelope fixtures produce `INCONCLUSIVE`; none is interpreted as a clean review.
- **SC-004**: All high-risk fixtures activate the expected profiles and required specialist topology; a high-risk `PASS` is impossible unless both primary and required specialist execution complete successfully.
- **SC-005**: `implement-tasks` integration fixtures complete successfully only after a fresh complete-feature review returns a valid `PASS`; verified defects, persistent inconclusive evidence, and loop stop conditions remain non-success outcomes.
- **SC-006**: The complete model-assisted evaluation corpus is run and recorded on at least one supported host, meets every fixture's minimum qualifying-finding and verdict expectations, and emits none of the fixture's forbidden speculative findings.
- **SC-007**: Existing whole-path quality audit behavior remains reachable only through `--audit`, remains advisory, and is never accepted as a defect-gate or `implement-tasks` completion result.

## Out of Scope

No separate product exclusions were confirmed. Rejected interfaces and prohibited bypasses are expressed as binding requirements above rather than as optional exclusions.

## Assumptions

No product assumptions are required. Planning must not add review modes, target semantics, bypasses, or acceptance thresholds that are absent from confirmed requirements.

## Dependencies

- A Git repository and readable Git metadata for change-scoped review.
- The existing CodexSpec initialization mechanism for distributing project-local scripts and command templates.
- A host capable of running the applicable Bash or PowerShell helper.
- Reviewer delegation support for isolated and specialist execution where those capabilities are mandatory; lack of support follows the confirmed `INCONCLUSIVE` behavior.
- Existing project, CI, and feature instructions used to select mandatory verification commands.

## Requirements Traceability

| Confirmed Entry | Spec Coverage | Notes |
|---|---|---|
| NEED-001 | REQ-001, REQ-010, REQ-028 | Reliable defect detection and measured reviewer quality |
| NEED-002 | REQ-009 | Requirements-aware conformance and completeness |
| CON-001 | NFR-002, REQ-028 | Persistent artifacts and fixtures remain source-independent |
| CON-002 | NFR-001, REQ-024, REQ-028 | Quality and evidence take priority over speed |
| DEC-001 | REQ-001 | Default defect-gate positioning |
| DEC-002 | REQ-002 | Complete default feature delta |
| DEC-003 | REQ-003 | Committed target and base modifier |
| DEC-004 | REQ-004, NFR-003 | Git-first base resolution without mutation |
| DEC-005 | REQ-001 | Explicit advisory audit mode |
| DEC-006 | REQ-003, REQ-010 | Supplemental focus only |
| DEC-007 | REQ-001, REQ-003, REQ-009 | Separate mode, target, and context |
| DEC-008 | REQ-009 | Target-dependent requirements depth |
| DEC-009 | REQ-010 | Four mandatory stages |
| DEC-010 | REQ-021 | Three terminal verdicts |
| DEC-011 | REQ-009, REQ-021 | Requirements evidence and verdict interaction |
| DEC-012 | REQ-016 | Project-first verification selection |
| DEC-013 | REQ-017 | Safe verification and failure attribution |
| DEC-014 | REQ-018 | Strict finding admission and blocking priorities |
| DEC-015 | REQ-019 | Compact report and evidence locations |
| DEC-016 | REQ-013 | Built-in risk profiles |
| DEC-017 | REQ-013, REQ-021 | Semantic activation and fail-closed evidence |
| DEC-018 | REQ-020, NFR-004 | Stable result envelope |
| DEC-019 | REQ-025 | Evidence-verified fix and full re-review |
| DEC-020 | REQ-026 | Progress-based loop termination |
| DEC-021 | REQ-011 | Complete artifact inventory |
| DEC-022 | REQ-011, REQ-012, NFR-001 | Derived, opaque, and large target handling |
| DEC-023 | REQ-015, REQ-020, REQ-025 | Fresh review-only contexts |
| DEC-024 | REQ-015, REQ-021 | Isolation degradation boundary |
| DEC-025 | REQ-014, REQ-021 | Independent specialist review |
| DEC-026 | REQ-014, REQ-020, NFR-004 | Reviewer execution disclosure |
| DEC-027 | REQ-002, REQ-004, REQ-009, REQ-022 | Target failure and empty-target semantics |
| DEC-028 | REQ-005, REQ-022 | Commit parent semantics |
| DEC-029 | REQ-006 | Hard-error migration |
| DEC-030 | REQ-023 | Authoritative instruction isolation |
| DEC-031 | REQ-023 | Injection evidence handling |
| DEC-032 | REQ-018 | Concrete test-gap boundary |
| DEC-033 | REQ-024, REQ-025 | No finding waiver |
| DEC-034 | REQ-003, REQ-012, REQ-024, NFR-001 | No degraded fast path |
| DEC-035 | REQ-007, NFR-003 | Project-local Bash and PowerShell resolver |
| DEC-036 | REQ-008, NFR-004 | Compatibility failures are inconclusive |
| DEC-037 | REQ-027, NFR-003 | Deterministic offline contract tests |
| DEC-038 | REQ-028, NFR-002 | Reusable model-assisted evaluation |

## Open Questions

None. All recorded discovery questions are resolved by confirmed decisions.
