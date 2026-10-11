# Feature Specification: Unified Staged Commit Analysis

**Feature ID**: `2026-1010-21225w`
**Authority**: [Confirmed requirements](requirements.md)

## Context

CodexSpec provides commit-staged, but command availability alone does not tell an
agent to use it when creating a commit. Implementation instructions allow direct
commits, auto-dev supplies message fields to a Python helper, and blueprint
mutations use fixed operation-name messages. These paths do not consistently use
the command's staged-diff analysis.

The agent performs semantic analysis. A helper is deterministic Python code that
validates and executes an operation. Helpers need not call a model themselves;
they must participate in a workflow that uses commit-staged analysis before the
commit is created.

## Goals

Use the same staged-change analysis for accurate and complete commit messages
across direct agent commits, auto-dev implementation commits, and blueprint
commits, while preserving staging ownership and helper protections.

## ADDED Requirements

### REQ-001: Proactively invoke the analysis command

**Sources**: NEED-001

When an agent is about to create a commit in a covered workflow, it must invoke
commit-staged's analysis instead of independently composing a message or falling
back to an operation-name message. Both Codex and Claude integration instructions
must state the trigger, including agent work outside explicitly invoked SDD stages.
The rule selects how an already-authorized commit is prepared; it does not grant
new authorization to stage, commit, or push.

#### Scenario: A user requests a commit without naming a command

- **WHEN** an agent is authorized to commit staged changes through ordinary
  conversation or an implementation stage,
- **THEN** it proactively invokes commit-staged before creating the commit.

### REQ-002: Describe all material staged changes faithfully

**Sources**: NEED-001, NEED-002

The message must describe the actual staged changes with sufficient detail to
represent their material behavior and scope. Use a concise subject and a body
when needed to describe those changes accurately and completely. Do not claim
unstaged changes, conversation-only intent, or unsupported verification outcomes.
Existing applicable commit format and language configuration still govern output.

#### Scenario: Staged and unstaged edits have different purposes

- **WHEN** the staging area contains a bug fix but the working tree or
  conversation contains a separate feature,
- **THEN** the message describes the staged fix and excludes that feature.
- **AND** a message is not truncated to a generic subject when a body is needed
  to cover material staged changes.

### REQ-003: Keep staging preparation with the caller

**Sources**: CON-001, NEED-002

The caller prepares the intended staging area before invoking analysis.
Commit-staged analyzes that staging area without independently selecting or
staging files. A helper's path selection must therefore be reflected in the
staging area supplied to analysis; a proposed diff or conversation summary is
not a substitute for the staged input.

#### Scenario: The helper commits a selected set of files

- **WHEN** a helper workflow intends to commit selected paths,
- **THEN** the caller prepares the intended staged content before analysis,
  and the analysis input and resulting commit include the same intended changes.
- **AND** unrelated staged or unstaged changes are not silently incorporated,
  discarded, or rewritten to make that correspondence appear valid.

### REQ-004: Integrate auto-dev and blueprint commits

**Sources**: NEED-001, CON-001, CON-002

Auto-dev feature commits and blueprint mutation commits must use messages
produced by commit-staged analysis of their prepared staging area. Blueprint
commits are included even when their current message is a fixed operation name.
The agent may pass analysis results to a helper that executes the commit.
The feature workflow must preserve its feature-identifying commit convention;
blueprint transactions remain limited to their blueprint changes.

#### Scenario: A blueprint status changes

- **WHEN** a blueprint mutation is committed,
- **THEN** commit-staged analyzes its staged change and the message describes
  the actual change instead of being generated solely from the operation label.
- **AND** the existing blueprint transaction and recovery protections remain.

### REQ-005: Commit exactly the content that was analyzed

**Sources**: CON-002, NEED-002

The commit must contain the content analyzed to produce its message. Detect a
change to that content before proceeding with the commit and repeat analysis
against the newly prepared staging area. This applies to caller edits, competing
operations, and hook-induced changes. Do not reuse a message based on stale
content merely because the selected paths or operation name are unchanged.

#### Scenario: A hook changes files and the commit is retried

- **WHEN** hook-modified content is prepared for another commit attempt,
- **THEN** analysis runs again on the new staged content before the retry.
- **AND** staging preparation remains the caller's responsibility.

### REQ-006: Preserve helper safety and report unusable input

**Sources**: CON-001, CON-002, NEED-002, DEC-001

Preserve existing helper ownership validation, path restrictions, concurrency
protection, and failure recovery throughout preparation, analysis, and execution.
Except for history-only merges under DEC-002, do not create a commit when the
staging area is empty, its intended content
cannot be determined, analysis is unavailable or insufficient, or the applicable
helper validation fails. Report the failed condition and retain enough existing
workflow state for the supported retry or recovery path. Do not silently bypass
analysis by generating a fixed message or performing a direct commit.

#### Scenario: Ownership or the prepared content becomes stale

- **WHEN** a helper can no longer establish ownership or that its prepared
  content matches the analysis,
- **THEN** it does not create a stale or unauthorized commit and reports the
  condition so the workflow can recover or prepare and analyze again.

## User Stories and Acceptance

As a CodexSpec user, I want agents to consistently use staged-change analysis so
that commit history explains the changes actually committed.

Acceptance requires all three commit workflows to satisfy REQ-001 through
REQ-006 where applicable, on both integrations. Verification must cover proactive
invocation instructions; staged versus unstaged content; messages requiring a
body; helper path isolation; blueprint updates; changed-content reanalysis;
and empty-input, analysis-failure, ownership, and recovery behavior.

## Constraints and Decisions

- The caller prepares staging; commit-staged supplies semantic analysis.
- Analysis and committed content must correspond, including on retries.
- Helper safety mechanisms remain effective across the analysis boundary.
- The choice of agent or helper for Git execution remains a design decision.

## Open Questions

None blocking specification or design. How callers prepare staging, hand off
analysis results, and establish content correspondence is for the design stage.

## Out of Scope

No additional user-confirmed exclusions. This specification does not authorize
unrelated staging, history rewriting, remote pushes, or removal of existing
helper protections. It introduces no new requirement for deterministic Python
helpers to host or call an LLM.

## Assumptions

No unconfirmed product assumptions are used as binding requirements. Existing
commit formatting and helper protection behavior are compatibility context for
implementing the confirmed requirements, not an exemption from analysis.

## Requirements Traceability

| Confirmed Entry | Spec Coverage |
|-----------------|---------------|
| NEED-001 | REQ-001, REQ-002, REQ-004 |
| NEED-002 | REQ-002, REQ-003, REQ-005, REQ-006 |
| CON-001 | REQ-003, REQ-004, REQ-006 |
| DEC-001 | REQ-006 |
| CON-002 | REQ-004, REQ-005, REQ-006 |

## CLI-Free Installation Compatibility

**Sources**: DEC-001; **Refines**: REQ-006.

Claude plugin installation and one-time uvx initialization retain the same
standalone commit guard used by the CLI. With Python 3.11+ and Git available,
original-index preview and authorized in-place direct execution work without a
persistent CodexSpec executable. The agent still generates messages from staged
diffs; the helper introduces no LLM dependency. Worktree routing, blueprint and
auto-dev retain their existing CLI prerequisites.

Acceptance: exercise installed Claude and Codex project helpers and a copied
marketplace plugin artifact with CodexSpec absent from PATH and Python site
packages disabled. Verify snapshot-only behavior, full messages, partial staging,
original hooks and stale-analysis rejection. Distribution checks establish byte
identity with the shared source before release.

## Merge Commit Compatibility

REQ-001, REQ-002, REQ-005 and REQ-006 include agent-created merge commits, as
confirmed in DEC-002. Contentful merges stop before commit creation, use the
original merge index for commit-staged preview, and require its exact snapshot
and complete message at finalization. The snapshot includes HEAD, index tree,
index identity, and merge parents. Hook changes invalidate that snapshot.
History-only merges retain the default Git merge message and the same validation;
empty non-merge staging remains rejected. Fast-forward creates no new commit.
Synchronization and baseline preparation retain conflict resolution, verification,
ownership, resumable state, and protection of the invoking checkout.
