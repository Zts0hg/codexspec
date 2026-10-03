---
name: codexspec:checklist
description: "生成自定义质量检查清单，用于验证需求完整性、清晰性和一致性"
---

# Requirements Quality Checklist Generator

## Constitution Compliance (MANDATORY)

**Before generating checklists:**

1. **Check for Constitution File**: Look for `.codexspec/memory/constitution.md`
2. **If Constitution Exists**:
   - Load and read quality standards and project principles
   - Use constitution quality standards as baseline for checklist items
   - Include constitution-specific checklist items where relevant
3. **If No Constitution Exists**: Use general best practices for requirements quality

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## Expression Standard

**IMPORTANT**: Everything this command produces — documents, reviews, reports, commit messages, diagnostics, and replies — is written for a reader who cannot see your working context. Apply the rules below to every artifact and message you output:

- **Write for the reader at hand-off.** Every reference must resolve without access to this session: no session-only identifiers or section numbers, no narration of what changed during the conversation, no arguments with absent reviewers. State current reality and cite committed, reachable sources.
- **Preserve every proposition.** Before summarizing or trimming, list the facts a passage carries: actors, conditions, ordering, modalities (must, never), negative guarantees, and consequences. Remove only reasoning transcripts, repetition, and decoration. Shorter is not clearer if any fact is lost.
- **State what the surface requires.** Diagnostics name what failed, which rule was violated, and the correction. Problem reports carry the defect, its location, its impact, and the evidence. Decisions record the alternatives they beat. Rejections give the reason in one line. Shipped work is described in the present tense; plans and open questions are labeled as such.
- **Define terms before relying on them.** Prefer the concrete rule, field, or behavior over a coined label; give a project-specific term a plain-language definition at first use, then use it consistently.
- **Be honest, not agreeable.** Verify claims before accepting them; fix or rebut on technical grounds. One substantiated blocker is worth more than a list of nitpicks. When a decision is needed, present only viable options, recommend one, and state the real difference between them.
- **Declare what is binding.** Say explicitly which instructions are hard requirements and where judgment is required. Keep one explanation in one place and link to it, but keep at the point of use the contract a reader needs there.

## Workspace Routing Before Writes

This section governs the location of every later file, index, branch, and commit mutation.
Record `SOURCE_ROOT` as the explicitly selected checkout (otherwise the invoking checkout) before
changing working directories. Read its `.codexspec/config.yml`: `workflow.worktrees` defaults to
on; only the literal boolean `false` disables it. Configuration remains checkout-local. Read-only
inspection keeps its original source target and does not create a worktree merely to read files.

- With `CODEXSPEC_AUTO_DEV_DELEGATION`, use the dedicated worktree supplied by auto-dev as
  `OUTPUT_ROOT` throughout. `blueprint` and `auto-dev` themselves retain their existing fixed branch
  `codexspec/auto-dev` and worktree `worktree-for-codexspec-auto-dev`; they always use the new shared
  `<repository-name>-codexspec-worktrees` parent, irrespective of the ordinary isolation switch.
- With ordinary isolation disabled, `OUTPUT_ROOT` is `SOURCE_ROOT` and existing in-place behavior
  applies. `codexspec init`, both first-time setup and installation updates, is explicitly exempt:
  it operates on its selected checkout regardless of this switch.
- For a new ordinary feature (`specify`, `quick`, or another feature-creation entry), invoke the
  installed platform create-new-feature script or `codexspec _worktree-helper create --name
  <short-name>` before the first artifact write. Parse returned JSON rather than evaluating shell
  output. `workspace`, `feature_dir`, and `requirements_file` are absolute paths; `branch` is the
  full `<feature-id>-<feature-name>`. Set `OUTPUT_ROOT` to that workspace.
- For an existing ordinary feature, resolve its explicit feature path/name first, otherwise its
  current feature branch, using `codexspec _worktree-helper resolve --feature <full-feature-name>`.
  Reuse that returned worktree. Do not silently pick another feature or create a replacement
  from main. If an explicit feature path names another checkout, use that checkout's configuration
  and preserve the identity of its documents and code.
- For standalone project-level writes without a selected ordinary feature, use
  `codexspec _worktree-helper route` from `SOURCE_ROOT`. An active feature workspace is reused;
  otherwise the helper uses `worktree-for-codexspec-maintenance`. Use the returned absolute
  workspace as `OUTPUT_ROOT`. Revalidate both source and destination rather than interpreting an
  arbitrary existing directory as a managed workspace.

When creation is interrupted, retain the returned `branch` and `workspace` even in an error
response. Resume the same identity with `codexspec _worktree-helper create --feature
<full-feature-name>`; a `creating` response from resolve requires this recovery step before
merge verification. A new `--name` request never adopts an existing identity after a random
name collision; report that collision and retry a new identity only for a genuinely new feature.

A `ready` response is required before writing feature artifacts or continuing development. Exit
status 3 with `merge_requires_resolution` or `merge_requires_verification` is a preparation handoff,
not success. Resolve conflicts and complete the merge only in the returned worktree, run the
project's required checks, and call `codexspec _worktree-helper finish --feature <full-feature-name>
--verification <json-file>` (use `worktree-for-codexspec-maintenance` for maintenance preparation).
The temporary JSON contains the verified `head`, `tree`, and `checks` entries with `command` and
integer `exit_code`; never claim a check ran when it did not. If conflicts cannot be resolved or
verification fails, stop. Retain the returned feature identity for continuation; do not create a
second feature to bypass failed preparation. Fetch warnings mean remote information may be stale;
they do not authorize bypassing an invalid baseline or failed verification.

Every mutating tool call and later SDD invocation must explicitly use `OUTPUT_ROOT` or paths inside
it. Before each file write, verify real filesystem containment: refuse symbolic links in the
output path and existing destination files with multiple hard links. A lexical path beneath
`OUTPUT_ROOT` alone does not establish isolation; never write through a link into another checkout.
A `cd` in one shell subprocess does not change the agent's later tool working directories.
Carry the same absolute workspace across stage handoffs. If required installation assets are
absent in a new worktree, run normal installation explicitly against that destination, preserving
existing project-authored files; stop if the required runtime or setup is unavailable.

Preserve input provenance: artifact-only reviews/reverse specification can read `SOURCE_ROOT`
while writing reports to `OUTPUT_ROOT`; their artifact containment checks apply to `OUTPUT_ROOT`.
Source edits and executable checks use the selected feature workspace. `commit-staged` preview
reads the original index; execution must stop if routing would substitute a different index or
mutate the protected main checkout. Do not copy, stash, stage, reset, or discard caller-owned changes
to make routing appear successful. Report an incompatible input/workspace and the required target
instead. Existing command-specific prohibitions still apply.

For configuration edits, decide routing from `SOURCE_ROOT`'s setting, then read and modify the
configuration in `OUTPUT_ROOT`. A bare toggle uses the destination's value. Report the exact path
and explain that other checkouts receive the setting through Git integration; do not add a shared
override or imply immediate changes to main's effective value. Completion retains worktrees; it
does not automatically merge to main or delete them. Any occupied path, invalid identity, failed
creation, or unusable baseline is an explicit stop, never permission to fall back to main writes.

## Checklist Purpose: "Unit Tests for Requirements"

**CRITICAL CONCEPT**: Checklists are **UNIT TESTS FOR REQUIREMENTS WRITING** - they validate the quality, clarity, and completeness of requirements.

**NOT for verification/testing:**

- ❌ NOT "Verify the button clicks correctly"
- ❌ NOT "Test error handling works"
- ❌ NOT "Confirm the API returns 200"

**FOR requirements quality validation:**

- ✅ "Are visual hierarchy requirements defined for all card types?" (completeness)
- ✅ "Is 'prominent display' quantified with specific sizing/positioning?" (clarity)
- ✅ "Are hover state requirements consistent across all interactive elements?" (consistency)
- ✅ "Are accessibility requirements defined for keyboard navigation?" (coverage)

## User Input

```text
the text after the $codexspec:checklist skill mention
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Steps

### 1. Setup

Run `.codexspec/scripts/check-prerequisites.sh --json` from repo root and parse JSON for:

- `FEATURE_DIR` - Feature directory path
- `AVAILABLE_DOCS` - Available documents list

### 2. Clarify Intent

Generate up to THREE contextual clarifying questions based on:

- Feature domain keywords (auth, latency, UX, API)
- Risk indicators ("critical", "must", "compliance")
- Stakeholder hints ("QA", "review", "security team")

Question types:

- Scope refinement
- Risk prioritization
- Depth calibration
- Audience framing

### 3. Load Feature Context

Read from FEATURE_DIR:

- spec.md: Feature requirements and scope
- plan.md (if exists): Technical details
- tasks.md (if exists): Implementation tasks

### 4. Generate Checklist

Create `FEATURE_DIR/checklists/` directory if needed.
Generate unique checklist filename: `[domain].md` (e.g., `ux.md`, `api.md`, `security.md`)

**Category Structure - Group items by requirement quality dimensions:**

- **Requirement Completeness**: Are all necessary requirements present?
- **Requirement Clarity**: Are requirements specific and unambiguous?
- **Requirement Consistency**: Do requirements align without conflicts?
- **Acceptance Criteria Quality**: Are success criteria measurable?
- **Scenario Coverage**: Are all flows/cases addressed?
- **Edge Case Coverage**: Are boundary conditions defined?
- **Non-Functional Requirements**: Performance, Security, Accessibility specified?
- **Dependencies & Assumptions**: Are they documented?

### 5. Item Structure

Each item should follow this pattern:

```
- [ ] CHK### - Are [requirement type] defined for [scenario]? [Quality Dimension, Spec §X.Y]
```

**Examples by Quality Dimension:**

**Completeness:**

- "Are error handling requirements defined for all API failure modes? [Gap]"
- "Are accessibility requirements specified for all interactive elements?"

**Clarity:**

- "Is 'fast loading' quantified with specific timing thresholds? [Clarity, Spec §NFR-2]"
- "Are 'related items' selection criteria explicitly defined?"

**Consistency:**

- "Do navigation requirements align across all pages? [Consistency, Spec §FR-10]"
- "Are card component requirements consistent between pages?"

**Coverage:**

- "Are requirements defined for zero-state scenarios? [Coverage, Edge Case]"
- "Are concurrent user interaction scenarios addressed?"

### 6. Prohibited Patterns

**❌ WRONG (Testing implementation):**

- "Verify landing page displays 3 cards"
- "Test hover states work on desktop"
- "Confirm logo click navigates home"

**✅ CORRECT (Testing requirements quality):**

- "Are the number and layout of featured items explicitly specified? [Completeness]"
- "Are hover state requirements consistently defined for all interactive elements? [Consistency]"
- "Are navigation requirements clear for all clickable brand elements? [Clarity]"

### 7. Report

Output:

- Full path to created checklist
- Item count
- Focus areas selected
- Depth level

## Example Checklist Types

### Reference Templates

Use the following template as reference for checklist structure:

- **Standard**: `.codexspec/templates/docs/checklist-template.md` - Multi-dimensional checklist covering spec, plan, tasks, security, performance, and documentation

**UX Requirements Quality:** `ux.md`

- Visual hierarchy requirements
- Interaction state requirements
- Accessibility requirements
- Fallback behavior requirements

**API Requirements Quality:** `api.md`

- Error response formats
- Rate limiting requirements
- Authentication requirements
- Versioning strategy

**Performance Requirements Quality:** `performance.md`

- Performance metrics quantification
- Load condition specifications
- Degradation requirements

**Security Requirements Quality:** `security.md`

- Authentication requirements
- Data protection requirements
- Threat model alignment
- Breach response requirements

> [!NOTE]
> Each `$codexspec:checklist` run creates a NEW file in `checklists/` directory.
