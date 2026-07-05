# CodexSpec Case Study: Adding a PR Description Generator to the Project

> This document records the complete process of using the CodexSpec toolchain to add a new feature to the CodexSpec project itself, demonstrating Spec-Driven Development (SDD) in practice.

## Overview

**Target feature**: Add the `/codexspec:pr` command, which generates structured GitHub PR / GitLab MR descriptions. (See the [README `/codexspec:pr` entry](https://github.com/Zts0hg/codexspec/blob/main/README.md) for the user-facing summary of the shipped command.)

**Development flow**: `specify → generate-spec → review-spec → clarify → spec-to-plan`

**Key characteristic**: A requirement issue surfaced mid-stream and was corrected through the `clarify` command, illustrating the flexibility of SDD. This is a concrete example of the CodexSpec **Confirmation Gate** — nothing is binding until you explicitly confirm it, and a previously accepted decision can be reopened and reversed at the clarify checkpoint.

---

## Stage 1: Initial Requirement Clarification (`/codexspec:specify`)

### Initial User Input

```
I want to add a feature to the project: a new Git-related command that generates accurate, detailed, and standards-compliant GitHub PR descriptions (or MR descriptions, for GitLab). Below are two PR commands I have used in other projects, provided for reference.

[Reference Example 1 - Structured Description]
Now, acting as a project maintainer, based on all the work we have done so far, write a clear Pull Request description for this submission.
The PR description should be aimed at the other reviewers on the team and include the following sections:
1. Context
2. Implementation
3. Testing
4. How to Verify

[Reference Example 2 - Simple Description]
Based on the code diff between the current branch and origin/main, use Markdown to produce a Merge Request title and description that comply with Git conventions. (Describe in Chinese.)
```

### Clarification Process

**Q1: Output language**

- Options: Follow project config / Chinese / Auto-detect
- **User choice**: Follow project config (current: en)

**Q2: Platform support**

- Options: Support both GitHub and GitLab / GitHub only / Auto-detect platform
- **User choice**: Auto-detect platform

**Q3: PR description content**

- Options: Detailed structured description / Concise description / Customizable template
- **User choice**: Detailed structured description (recommended)

**Q4: Trigger condition**

- Options: Current branch vs origin/main / Unpushed commits / Configurable target branch
- **User choice**: Configurable target branch

**Q5: Spec source**

- Options: Prefer spec.md / Git info only / Combine all sources
- **User choice**: Combine all sources (recommended)

**Q6: Naming**

- Options: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **User choice**: codexspec.pr (recommended)

**Q7: Handling missing spec**

- Options: Continue generating, skip Context / Prompt user to create spec first / Warn and continue
- **User choice**: Continue generating, skip Context

**Q8: Output method**

- Options: Terminal output / Save to file / Terminal + optional file
- **User choice**: Terminal + optional file (recommended)

**Q9: Default sections**

- Options: Context, Implementation, Testing, How to Verify (all selected)
- **User choice**: All four sections

**Q10: Command parameters**

- **User choice**: All parameters are optional
  - `--target-branch`: default origin/main
  - `--output`: when unspecified, default to terminal output only
  - `--sections`: when unspecified, follow defaults
  - `--no-spec`: skip spec.md lookup

### Language Configuration Correction

**User feedback**: The language behavior should match the `/commit-staged` command — first honor `language.commit` from `config.yml`, and only fall back to `language.output` when `language.commit` is not set.

**Updated requirement summary**:

```
Language priority: language.commit > language.output > English (default)
```

---

## Stage 2: Generate the Specification Document (`/codexspec:generate-spec`)

### Generated Document Structure

The generated `spec.md` contains the following sections:

- **Overview**: Feature overview
- **Goals**: 4 goals
- **User Stories**: 4 user stories with acceptance criteria
- **Functional Requirements**: 8 requirements (REQ-001 through REQ-008)
- **Command Parameters**: 4 parameter definitions
- **Non-Functional Requirements**: 3 requirements (performance, compatibility, error handling)
- **Acceptance Criteria (Test Cases)**: 10 test cases
- **Edge Cases**: 6 edge cases
- **Output Format Example**: GitHub PR and GitLab MR examples
- **Out of Scope**: Explicitly excluded features
- **Dependencies**: Dependencies
- **Related Commands**: Related commands

### Key Requirement Excerpt

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## Stage 3: Specification Review (`/codexspec:review-spec`)

### Review Outcome

- **Overall status**: ✅ Pass
- **Quality score**: 92/100
- **Readiness**: Ready for Planning

### Issues Found

**Warnings (Should Fix)**:

1. **SPEC-001**: Test-file discovery logic is not explicitly specified
2. **SPEC-002**: When multiple spec.md files exist, picking "most recently modified" may be inaccurate

**Suggestions (Nice to Have)**:

1. Consider adding a `--title` parameter
2. Add an output-format validation requirement
3. Consider supporting GitHub Enterprise URL patterns

### Review Report Location

`.codexspec/specs/2026-0613-1200ab-pr-description-generator/review-spec.md`

This is an **evidence-based review**: every warning and suggestion above is tied to a concrete, identifiable gap in the spec, and advisory items (Nice to Have) do not affect acceptance or trigger automatic changes.

---

## Stage 4: Requirement Clarification and Adjustment (`/codexspec:clarify`) — Critical Turning Point

### Issue Discovered

**User feedback**:
> I realized there is a problem with the use of spec.md. For example, the user may in fact be making a very small change, so they did not follow CodexSpec's standardized flow of specify → plan → tasks → implement. Instead they made changes directly through conversation or Claude Code's built-in plan mode, and after finishing the changes they want to invoke a CodexSpec command separately to generate a standards-compliant PR description. In this case, defaulting to the most recently modified spec.md may pull in content from a previous spec.md that has nothing to do with this change.

This is the **Confirmation Gate** in action: the earlier decision ("default to most recently modified spec.md") had been recorded, but it was not yet binding in the sense of being irreversible — the user reopened it at the clarify checkpoint with new information about a real usage pattern, and the previously accepted default was overturned.

### Clarification Q&A Process

**Q1: Spec selection strategy**

**Context**: The current EC-004 says "multiple spec.md files → use the most recently modified." But when a user makes a small change without following the SDD flow, the most recent spec.md may be unrelated to the current change.

| Option | Description |
|--------|-------------|
| A | Do not use spec.md by default unless the user explicitly passes `--spec` |
| B | Match by branch name |
| C | Prompt the user to choose |
| D | Match by file changes |

**User choice**: Option A
**Reason**: Avoids incorrect references; the `--spec` parameter lets users who want SDD integration opt in explicitly.

---

**Q2: Spec content extraction strategy**

**Context**: When the user passes `--spec`, what happens if the spec.md structure is incomplete?

| Option | Description |
|--------|-------------|
| A | Best-effort extraction, skip missing sections |
| B | Warn and skip Context |
| C | Require a complete structure, otherwise error out |

**User choice**: Option A
**Reason**: Avoid letting a spec format issue block the workflow.

---

**Q3: Test-file discovery**

**Context**: How should the Testing section discover test files?

| Option | Description |
|--------|-------------|
| A | Common directory patterns (tests/, test/) |
| B | Language-agnostic heuristics (directory + filename patterns) |
| C | No active discovery; infer only from commit messages |

**User choice**: Option B
**Reason**: Covers a variety of project structures across different languages.

---

**Q4: PR title generation**

**Context**: How should the PR title be generated?

| Option | Description |
|--------|-------------|
| A | Branch-name parsing first |
| B | First commit message first |
| C | Synthesize (git diff + branch name + commit messages) |

**User choice**: Option C
**User reason**: The first commit may represent only a small slice of the change, and branch names assume strong naming discipline. With substantial git information and code changes available to reference, synthesized analysis is more accurate.

---

**Q5: Verification command generation**

**Context**: How should the "How to Verify" section generate verification commands?

| Option | Description |
|--------|-------------|
| A | Generic templates |
| B | Project detection (pyproject.toml → pytest, package.json → npm test) |
| C | Infer from commit messages |

**User choice**: Option B
**Reason**: Project detection produces more practical verification commands.

---

### Clarification Session Summary

| Question | Decision | Impact |
|----------|----------|--------|
| Spec selection strategy | Opt-in via `--spec` | REQ-007, EC-004, parameter table |
| Spec content extraction | Best-effort extraction | REQ-005b, EC-004c |
| Test-file discovery | Language-agnostic heuristics | REQ-006b |
| PR title generation | Synthesized analysis | REQ-008a |
| Verification command generation | Project-file detection | REQ-010 |

### Key Change: Parameter Logic Reversal

```
Original design: --no-spec (skip spec)
New design:      --spec (enable spec, opt-in)
```

This reversal is the clearest illustration of the Confirmation Gate in this case study: a default that was originally "binding" (`--no-spec`, i.e. spec on by default) was reopened, reversed, and re-confirmed as opt-in once the user surfaced a real workflow it would have broken.

---

## Stage 5: Technical Implementation Plan (`/codexspec:spec-to-plan`)

### Plan Overview

**Implementation approach**: Markdown template file (consistent with `/codexspec:commit-staged`)

**No new dependencies** — the feature is delivered through a slash command template and requires no Python code.

### Technical Decision Summary

| Decision | Choice | Reason |
|----------|--------|--------|
| Implementation approach | Markdown template | Consistent with existing commands, easy to maintain |
| Language priority | commit > output > en | Consistent with `/commit-staged` |
| Platform detection | Remote URL parsing | Simple and reliable |
| Spec integration | Opt-in (`--spec`) | Avoid incorrect references |
| Content extraction | Best-effort | Does not block the workflow |
| Test discovery | Directory + filename patterns | Language-agnostic |
| Title generation | Synthesized analysis | Most accurate |
| Command detection | Project-file detection | More practical |
| Output mode | Terminal first, optional file | Flexible |

### Implementation Phases

1. **Phase 1**: Template creation (YAML frontmatter, language config, Git context)
2. **Phase 2**: Core functionality (Spec integration, test discovery, command detection, title generation)
3. **Phase 3**: Edge-case handling
4. **Phase 4**: Testing
5. **Phase 5**: Documentation updates

### File Manifest

**Created**:

- `templates/commands/pr.md`

**Modified**:

- `CLAUDE.md` - Add command description
- `README.md` - Add command to the list

**Tests**:

- `tests/test_pr_template.py`

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   CodexSpec SDD Development Flow                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:specify                                                     │
│  ├─ Clarify requirements through Q&A                                    │
│  ├─ User provides reference examples                                    │
│  └─ 10 questions covering language, platform, content, parameters, etc. │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:generate-spec                                               │
│  ├─ Generate a complete spec.md                                         │
│  ├─ 4 user stories, 8 functional requirements, 10 test cases            │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/spec.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:review-spec                                                 │
│  ├─ Quality score: 92/100                                               │
│  ├─ Found 2 warnings (test-file discovery, multi-spec handling)         │
│  └─ Status: Pass, can proceed to planning                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:clarify  (Critical adjustment)                              │
│  ├─ User surfaces a real-world usage issue                              │
│  ├─ 5 clarification questions, all answered                             │
│  ├─ Key change: --no-spec → --spec (opt-in)                             │
│  └─ Added 5 requirements (REQ-005b, 006b, 008a, 010, updated 007)       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec:spec-to-plan                                                │
│  ├─ Update the technical implementation plan                            │
│  ├─ 9 technical decisions, including 5 new ones                         │
│  ├─ 5 implementation phases                                             │
│  └─ Saved to .codexspec/specs/2026-0613-1200ab-pr-description-generator/plan.md │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Subsequent steps (not completed in this session)                       │
│  ├─ /codexspec:review-plan - Validate plan quality                      │
│  ├─ /codexspec:plan-to-tasks - Break down into executable tasks         │
│  └─ /codexspec:implement-tasks - Execute the implementation             │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Key Learnings

### 1. The Value of the Clarify Stage

This case shows the pivotal role of the `clarify` command:

- **The user discovers a real problem during use** — the risk of misusing spec.md in small-change scenarios
- **A design flaw is resolved through clarifying Q&A** — shifting from auto-detection to opt-in
- **Requirement changes are recorded systematically** — all changes are saved in the Clarifications section of spec.md

### 2. Flexibility of the SDD Flow

- It is not a linear flow; you can return and adjust at any stage
- `clarify` can be inserted after `review-spec` and before `spec-to-plan`
- Both the specification document and the technical plan are updated to reflect the change

### 3. Evolution of the Parameter Design

```
Initial design:
  --no-spec: skip spec.md (used by default)

Final design:
  --spec: enable spec.md (not used by default)
```

This change reflects a design shift from "default SDD workflow" to "also support non-SDD workflows," making the tool more general-purpose.

### 4. Documentation Outputs

| Stage | Output file | Content |
|-------|-------------|---------|
| generate-spec | spec.md | Complete specification document |
| review-spec | review-spec.md | Quality review report |
| clarify | (updates spec.md) | Clarification records + requirement updates |
| spec-to-plan | plan.md | Technical implementation plan |

---

## Appendix: Command Quick Reference

```bash
# 1. Initial requirement clarification
/codexspec:specify

# 2. Generate the specification document
/codexspec:generate-spec

# 3. Review the specification quality
/codexspec:review-spec

# 4. Clarify/adjust requirements (optional; use when an issue is found)
/codexspec:clarify [issue description]

# 5. Generate the technical plan
/codexspec:spec-to-plan

# 6. Review the plan quality (optional)
/codexspec:review-plan

# 7. Break down into tasks
/codexspec:plan-to-tasks

# 8. Execute the implementation
/codexspec:implement-tasks
```

---

*This document was generated by the CodexSpec SDD workflow and records a real development conversation.*
