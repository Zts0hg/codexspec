# Task Breakdown: PR Description Generator

## Overview

- **Total Tasks**: 18
- **Completed**: 18 ✅
- **Parallelizable Tasks**: 11
- **Phases**: 5

---

## Phase 1: Foundation

### Task 1.1: Create PR Template File with YAML Frontmatter ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Create the main template file with YAML frontmatter containing description and allowed-tools
- **Acceptance Criteria**:
  - ✅ File exists at `templates/commands/pr.md`
  - ✅ YAML frontmatter includes `description` field
  - ✅ YAML frontmatter includes `allowed-tools` with git commands
- **Dependencies**: None

### Task 1.2: Reference Existing commit.md Pattern [P] ✅

- **Type**: Research
- **Files**: `templates/commands/commit.md` (read-only)
- **Description**: Study the existing commit.md template to understand structure, language handling, and git context collection patterns
- **Acceptance Criteria**:
  - ✅ Understand YAML frontmatter structure
  - ✅ Understand language preference handling
  - ✅ Understand git command execution approach
- **Dependencies**: None

---

## Phase 2: Core Template Content

### Task 2.1: Add Language Preference Section [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add language preference section with priority: language.commit > language.output > English
- **Acceptance Criteria**:
  - ✅ Section reads `.codexspec/config.yml`
  - ✅ Priority order correctly specified
  - ✅ Matches commit.md pattern
- **Dependencies**: Task 1.1

### Task 2.2: Add Git Context Collection Section [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add instructions for collecting git context (current branch, diff, commits)
- **Acceptance Criteria**:
  - ✅ Commands for `git branch --show-current`
  - ✅ Commands for `git diff` (staged and unstaged)
  - ✅ Commands for `git log` (commit history)
  - ✅ Commands for `git remote get-url origin`
- **Dependencies**: Task 1.1

### Task 2.3: Add Platform Detection Logic [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add logic to detect GitHub vs GitLab from remote URL
- **Acceptance Criteria**:
  - ✅ Detect `github.com` → "Pull Request" terminology
  - ✅ Detect `gitlab.com` → "Merge Request" terminology
  - ✅ Other URLs → Default to GitHub terminology
  - ✅ Handle no remote configured case (warning + GitHub default)
- **Dependencies**: Task 1.1

### Task 2.4: Add Parameter Handling Section ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add instructions for parsing $ARGUMENTS and handling parameters
- **Acceptance Criteria**:
  - ✅ `--target-branch <branch>` with default `origin/main`
  - ✅ `--output <file>` optional file output
  - ✅ `--sections <list>` with values: context, implementation, testing, verify, all
  - ✅ `--spec <path>` opt-in spec.md integration
- **Dependencies**: Task 2.1, Task 2.2, Task 2.3

---

## Phase 3: Content Generation Logic

### Task 3.1: Add PR Title Generation Logic ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add comprehensive title generation logic (git diff + branch name + commit messages)
- **Acceptance Criteria**:
  - ✅ Primary source: git diff analysis
  - ✅ Supporting sources: branch name, commit messages
  - ✅ Synthesis into single descriptive title
- **Dependencies**: Task 2.4

### Task 3.2: Add Spec.md Integration Section (Opt-in) [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add instructions for optional spec.md integration via --spec parameter
- **Acceptance Criteria**:
  - ✅ Only active when `--spec` is provided
  - ✅ Support spec directory name (e.g., `001-auth`)
  - ✅ Support full path to spec.md
  - ✅ Best-effort extraction from incomplete specs
  - ✅ Priority order: User Stories > Goals > Overview > Requirements
  - ✅ Error handling for invalid spec path
- **Dependencies**: Task 2.4

### Task 3.3: Add Test File Discovery Section [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add language-agnostic test file discovery patterns
- **Acceptance Criteria**:
  - ✅ Directory patterns: `tests/`, `test/`, `__tests__/`, `spec/`
  - ✅ File name patterns: `*_test.py`, `test_*.py`, `*.test.js`, `*.spec.ts`, `*_test.go`, `*Test.java`
  - ✅ Combined approach (directory OR file name match)
- **Dependencies**: Task 2.4

### Task 3.4: Add Project Command Detection Section [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add logic to detect project-specific test commands
- **Acceptance Criteria**:
  - ✅ `pyproject.toml` + `pytest.ini`/`tests/` → `pytest`
  - ✅ `package.json` + `jest.config.js` → `npm test`
  - ✅ `package.json` + `vitest.config.ts` → `vitest`
  - ✅ `Cargo.toml` + `src/` → `cargo test`
  - ✅ `go.mod` → `go test`
  - ✅ `Makefile` with test target → `make test`
  - ✅ Fallback to generic steps if no match
- **Dependencies**: Task 2.4

---

## Phase 4: Output Generation

### Task 4.1: Add Section Generation Logic ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add logic for generating each PR section based on gathered information
- **Acceptance Criteria**:
  - ✅ **Context**: From spec.md (if --spec used), skip otherwise
  - ✅ **Implementation**: From git diff analysis
  - ✅ **Testing**: From test file discovery and commit messages
  - ✅ **How to Verify**: Step-by-step with project-detected commands
  - ✅ Support `--sections` parameter to include/exclude sections
- **Dependencies**: Task 3.1, Task 3.2, Task 3.3, Task 3.4

### Task 4.2: Add Output Format Template ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add markdown output format template with examples
- **Acceptance Criteria**:
  - ✅ GitHub PR example format
  - ✅ GitLab MR example format
  - ✅ Proper markdown structure with all sections
  - ✅ Terminal output (default) vs file output (--output)
- **Dependencies**: Task 4.1

### Task 4.3: Add Edge Case Handling ✅

- **Type**: Implementation
- **Files**: `templates/commands/pr.md`
- **Description**: Add error messages and fallback behaviors for edge cases
- **Acceptance Criteria**:
  - ✅ EC-001: No changes → "No changes detected..."
  - ✅ EC-002: Invalid branch → "Target branch not found..."
  - ✅ EC-003: Not a git repo → "Not a git repository..."
  - ✅ EC-004b: Invalid spec path → "Spec not found..." with available specs
  - ✅ EC-005: Detached HEAD → "Cannot determine current branch..."
  - ✅ EC-006: No remote → GitHub terminology with warning
- **Dependencies**: Task 4.2

---

## Phase 5: Testing & Documentation

### Task 5.1: Write Template Structure Tests [P] ✅

- **Type**: Testing
- **Files**: `tests/test_pr_template.py`
- **Description**: Write tests to validate template structure
- **Acceptance Criteria**:
  - ✅ Test YAML frontmatter presence
  - ✅ Test `description` field exists
  - ✅ Test `allowed-tools` field exists with git commands
  - ✅ Test required sections present (Language Preference, Git Context, etc.)
- **Dependencies**: Task 4.3

### Task 5.2: Write Parameter Documentation Tests [P] ✅

- **Type**: Testing
- **Files**: `tests/test_pr_template.py`
- **Description**: Write tests to validate parameter documentation
- **Acceptance Criteria**:
  - ✅ Test `--target-branch` documented with default
  - ✅ Test `--output` documented
  - ✅ Test `--sections` documented with values
  - ✅ Test `--spec` documented with opt-in behavior
- **Dependencies**: Task 4.3

### Task 5.3: Write Template Installation Tests ✅

- **Type**: Testing
- **Files**: `tests/test_pr_template.py`
- **Description**: Write tests to verify template installation via codexspec init
- **Acceptance Criteria**:
  - ✅ Test template copied to `.claude/commands/codexspec.pr.md`
  - ✅ Test template content matches source
  - ✅ Test init command includes pr.md in copy list
- **Dependencies**: Task 5.1, Task 5.2

### Task 5.4: Update CLAUDE.md Documentation [P] ✅

- **Type**: Documentation
- **Files**: `CLAUDE.md`
- **Description**: Add `/codexspec.pr` command to the command table
- **Acceptance Criteria**:
  - ✅ Command listed in available commands table
  - ✅ Description: "Generate structured PR/MR descriptions"
  - ✅ Include in "Git Workflow Commands" category
- **Dependencies**: Task 4.3

### Task 5.5: Update README.md Documentation [P] ✅

- **Type**: Documentation
- **Files**: `README.md`
- **Description**: Add command to available commands list with usage examples
- **Acceptance Criteria**:
  - ✅ Command listed in README
  - ✅ Brief description of functionality
  - ✅ Usage examples with parameters
- **Dependencies**: Task 4.3

---

## Execution Order

```
Phase 1: Foundation
    Task 1.1 ─────────────────────────────────┐
    Task 1.2 [P] ─────────────────────────────┤
                                              │
Phase 2: Core Template Content                │
    ┌─────────────────────────────────────────┴───────────────┐
    │                                                           │
    Task 2.1 [P] ───┐                                          │
    Task 2.2 [P] ───┼──► Task 2.4                              │
    Task 2.3 [P] ───┘         │                               │
                              │                               │
Phase 3: Content Generation Logic                              │
    ┌─────────────────────────┴───────────────────┐           │
    │                                               │           │
    Task 3.1 ────────────────────────────┐         │           │
    Task 3.2 [P] ────────────────────────┤         │           │
    Task 3.3 [P] ────────────────────────┼──► Task 4.1         │
    Task 3.4 [P] ────────────────────────┘         │           │
                                                   │           │
Phase 4: Output Generation                         ▼           │
                                        Task 4.2 ──┤           │
                                                   │           │
                                        Task 4.3 ──┤           │
                                                   │           │
Phase 5: Testing & Documentation                   │           │
    ┌──────────────────────────────────────────────┴───────────┘
    │
    Task 5.1 [P] ───┐
    Task 5.2 [P] ───┼──► Task 5.3
    Task 5.4 [P] ───┤
    Task 5.5 [P] ───┘
```

---

## Checkpoints

- [x] **Checkpoint 1**: After Phase 1 - Template file created with basic structure ✅
- [x] **Checkpoint 2**: After Phase 2 - Core sections added (language, git, platform, params) ✅
- [x] **Checkpoint 3**: After Phase 3 - All content generation logic complete ✅
- [x] **Checkpoint 4**: After Phase 4 - Full template with output format and edge cases ✅
- [x] **Checkpoint 5**: After Phase 5 - Tests pass, documentation updated ✅

---

## Summary

| Phase | Tasks | Parallelizable |
|-------|-------|----------------|
| Phase 1: Foundation | 2 | 1 |
| Phase 2: Core Template | 4 | 3 |
| Phase 3: Content Generation | 4 | 3 |
| Phase 4: Output Generation | 3 | 0 |
| Phase 5: Testing & Docs | 5 | 4 |
| **Total** | **18** | **11** |

---

## Notes

- This feature is implemented as a **Markdown template**, not Python code
- No new Python dependencies required
- Template follows the existing `/codexspec.commit` pattern
- All logic is executed by Claude Code, not by Python code
- Tests validate template structure, not runtime behavior
