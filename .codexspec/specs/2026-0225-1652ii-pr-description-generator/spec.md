# Feature: PR Description Generator

## Overview

A new slash command `/codexspec.pr` that generates structured, comprehensive Pull Request (GitHub) or Merge Request (GitLab) descriptions. The command analyzes git differences, commit history, and optionally spec.md files to produce well-formatted PR/MR documentation.

## Goals

- Automate the creation of PR/MR descriptions following best practices
- Support both GitHub (PR) and GitLab (MR) platforms with automatic detection
- Integrate with existing CodexSpec workflow (spec.md, i18n configuration)
- Complement the existing `/codexspec.commit` command for branch-level documentation

## User Stories

### Story 1: Generate PR Description for Feature Branch

**As a** developer who has completed a feature
**I want** to generate a comprehensive PR description automatically
**So that** I can create a well-documented pull request without manual writing

**Acceptance Criteria:**

- [ ] Command analyzes git diff between current branch and target branch
- [ ] Generated description includes structured sections (Context, Implementation, Testing, How to Verify)
- [ ] Description language follows project configuration

### Story 2: Platform-Aware Description Generation

**As a** developer using different Git platforms
**I want** the command to automatically detect whether I'm using GitHub or GitLab
**So that** the generated description uses appropriate terminology and format

**Acceptance Criteria:**

- [ ] Command detects platform from remote URL (github.com vs gitlab.com)
- [ ] Uses "Pull Request" terminology for GitHub
- [ ] Uses "Merge Request" terminology for GitLab

### Story 3: Spec-Integrated Description (Opt-in)

**As a** developer following Spec-Driven Development
**I want** to optionally include my spec.md content in the PR description
**So that** reviewers understand the context and requirements behind the changes

**Acceptance Criteria:**

- [ ] By default, spec.md is NOT used (git-only mode)
- [ ] `--spec` parameter enables spec integration
- [ ] Extracts user stories and requirements for Context section when enabled
- [ ] Supports spec directory name (e.g., `001-auth`) or full path

### Story 4: Customizable Output

**As a** developer with specific documentation needs
**I want** to customize the PR description sections and output format
**So that** I can tailor the output to my team's standards

**Acceptance Criteria:**

- [ ] `--sections` parameter allows selecting specific sections
- [ ] `--output` parameter allows saving to file
- [ ] `--target-branch` parameter allows specifying comparison target

## Functional Requirements

### REQ-001: Command Invocation

The command shall be invoked as `/codexspec.pr` with optional arguments.

### REQ-002: Platform Detection

The command shall automatically detect the Git platform by analyzing the remote URL:

- URLs containing `github.com` → GitHub mode (PR terminology)
- URLs containing `gitlab.com` → GitLab mode (MR terminology)
- Other URLs → Default to GitHub terminology

### REQ-003: Language Configuration

The command shall determine output language in the following priority order:

1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)

### REQ-004: Default Target Branch

The command shall use `origin/main` as the default target branch for comparison.

### REQ-005: Content Generation Sources

The command shall gather information from multiple sources:

- Git diff between current branch and target branch
- Commit messages on the current branch (not in target)
- spec.md files in `.codexspec/specs/*/spec.md` (only when `--spec` is specified)

### REQ-005b: Spec Content Extraction Strategy

When extracting content from spec.md (via `--spec`), the command shall:

- **Best-effort extraction**: Extract available information, skip missing sections
- **Graceful degradation**: If User Stories missing, use Overview/Goals for Context
- **No errors for incomplete specs**: Continue generation even if spec structure is partial
- **Priority order for Context**: User Stories > Goals > Overview > Requirements

### REQ-006: Default Section Structure

The command shall generate the following sections by default:

1. **Context** - Background and problem statement (from spec.md if `--spec` is used)
2. **Implementation** - Technical approach summary (from git diff analysis)
3. **Testing** - Test coverage and methodology (from test files and commit messages)
4. **How to Verify** - Step-by-step verification instructions

### REQ-006b: Test File Discovery

When gathering Testing section content, the command shall discover test files using:

- **Directory patterns**: `tests/`, `test/`, `__tests__/`, `spec/`
- **File name patterns**: `*_test.py`, `test_*.py`, `*.test.js`, `*.spec.ts`, `*_test.go`, `*Test.java`
- **Combined approach**: Match files that are in test directories OR match file name patterns
- **Language-agnostic**: Apply all patterns regardless of detected project language

### REQ-007: Spec.md Integration (Opt-in)

The command shall NOT use spec.md by default. Spec integration is opt-in:

- **Default behavior**: Generate PR description from git information only (no spec.md)
- **With `--spec`**: Include Context section from specified or auto-detected spec.md
- **Rationale**: Avoids incorrect spec references for small changes that didn't follow SDD workflow

### REQ-008a: PR Title Generation Strategy

The command shall generate PR titles using a comprehensive approach:

- **Primary source**: Analyze git diff content to understand actual code changes
- **Supporting sources**: Branch name parsing and commit messages for context
- **Synthesis**: Combine insights from all sources into a single descriptive title
- **Rationale**: First commit may only represent partial work; branch names may not follow conventions; actual code changes provide the most accurate representation

**Example**:

- Branch: `feature/auth-cleanup`
- First commit: "Add password validation"
- Actual changes: Full authentication refactor with JWT, session management, tests
- Generated title: "Refactor Authentication System with JWT and Session Management"

### REQ-009: Output Modes

The command shall support two output modes:

- **Terminal output** (default): Print to stdout for copy-paste
- **File output**: Save to specified file when `--output` is provided

### REQ-010: Project Command Detection

For the "How to Verify" section, the command shall detect project-specific commands:

**Detection Rules**:

| Project File | Detected Command | Example |
|--------------|-------------------|---------|
| `pyproject.toml` + `pytest.ini` or `tests/` | `pytest` | `uv run pytest` or `pytest` |
| `package.json` + `jest.config.js` | `npm test` | `npm test` |
| `package.json` + `vitest.config.ts` | `vitest` | `npm run test` |
| `Cargo.toml` + `src/` | `cargo test` | `cargo test` |
| `go.mod` | `go test` | `go test ./...` |
| `Makefile` with test target | `make test` | `make test` |

**Fallback**: If no project file detected, use generic steps:

1. Install dependencies
2. Run tests (with project-appropriate command if identifiable)

## Command Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--target-branch` | string | `origin/main` | Branch to compare against |
| `--output` | string | none | Output file path (optional) |
| `--sections` | string | all | Comma-separated list of sections to include |
| `--spec` | string | none | Path to spec.md or spec directory name (e.g., `001-auth`) |

### Parameter Details

#### `--sections` Values

- `context` - Background and problem statement
- `implementation` - Technical approach
- `testing` - Test coverage information
- `verify` - Verification steps
- `all` - Include all sections (default)

Example: `--sections context,implementation,verify`

#### `--spec` Usage

The `--spec` parameter enables spec.md integration (opt-in):

| Value | Behavior |
|-------|----------|
| (not specified) | No spec integration, generate from git only |
| `001-auth` | Use `.codexspec/specs/001-auth/spec.md` |
| `path/to/spec.md` | Use specified spec.md file path |

**When to use**:

- Following SDD workflow with existing spec.md
- Want Context section with user stories and requirements
- Large feature changes with documented specifications

**When NOT to use**:

- Small bug fixes or minor changes
- Quick iterations without formal specification
- Changes unrelated to existing specs

## Non-Functional Requirements

### NFR-001: Performance

The command shall complete within 10 seconds for repositories with up to 100 commits in the branch diff.

### NFR-002: Compatibility

The command shall work with:

- GitHub.com and GitHub Enterprise
- GitLab.com and self-hosted GitLab
- Git version 2.0+

### NFR-003: Error Handling

The command shall provide clear error messages for:

- Invalid target branch
- No commits to compare (branch up to date with target)
- Missing git repository

## Acceptance Criteria (Test Cases)

### TC-001: Basic PR Generation

**Given** a feature branch with commits ahead of origin/main
**When** user runs `/codexspec.pr`
**Then** a structured PR description is generated with all four sections

### TC-002: GitHub Platform Detection

**Given** a repository with remote URL containing "github.com"
**When** user runs `/codexspec.pr`
**Then** the output uses "Pull Request" terminology

### TC-003: GitLab Platform Detection

**Given** a repository with remote URL containing "gitlab.com"
**When** user runs `/codexspec.pr`
**Then** the output uses "Merge Request" terminology

### TC-004: Custom Target Branch

**Given** a feature branch compared against `origin/develop`
**When** user runs `/codexspec.pr --target-branch origin/develop`
**Then** the PR description reflects changes relative to develop branch

### TC-005: Output to File

**Given** a feature branch with changes
**When** user runs `/codexspec.pr --output pr_description.md`
**Then** the PR description is saved to `pr_description.md`

### TC-006: Partial Sections

**Given** a feature branch with changes
**When** user runs `/codexspec.pr --sections context,implementation`
**Then** only Context and Implementation sections are generated

### TC-007: Default Behavior (No Spec)

**Given** a repository with or without spec.md files
**When** user runs `/codexspec.pr` (without --spec)
**Then** PR description is generated without Context section (git-only mode)

### TC-008: Spec Integration with --spec

**Given** a repository with spec.md at `.codexspec/specs/001-auth/spec.md`
**When** user runs `/codexspec.pr --spec 001-auth`
**Then** PR description includes Context section with user stories from spec.md

### TC-009: Language Configuration Priority

**Given** config.yml has `language.commit: "zh-CN"` and `language.output: "en"`
**When** user runs `/codexspec.pr`
**Then** the PR description is generated in Chinese

### TC-010: Fallback to Output Language

**Given** config.yml has only `language.output: "ja"` (no commit language)
**When** user runs `/codexspec.pr`
**Then** the PR description is generated in Japanese

## Edge Cases

### EC-001: Branch Up to Date with Target

**Scenario**: Current branch has no commits ahead of target branch
**Handling**: Display message "No changes detected between current branch and [target]. Nothing to generate."

### EC-002: Invalid Target Branch

**Scenario**: Specified target branch does not exist
**Handling**: Display error "Target branch '[branch]' not found. Please verify the branch name."

### EC-003: Not a Git Repository

**Scenario**: Command run outside of a git repository
**Handling**: Display error "Not a git repository. Please run this command from within a git repository."

### EC-004: Spec.md Not Specified (Default)

**Scenario**: User runs `/codexspec.pr` without `--spec` parameter
**Handling**: Generate PR description from git information only. No Context section from spec.md. This is the expected behavior for small changes or non-SDD workflow.

### EC-004b: Invalid Spec Path

**Scenario**: User specifies `--spec` but the path/directory doesn't exist
**Handling**: Display error "Spec '[path]' not found. Available specs: [list specs in .codexspec/specs/]"

### EC-004c: Incomplete Spec Structure

**Scenario**: User specifies `--spec` but the spec.md lacks expected sections (no User Stories, etc.)
**Handling**: Best-effort extraction - use available sections (Overview, Goals, Requirements) for Context. Do not error or warn.

### EC-005: Detached HEAD State

**Scenario**: Repository is in detached HEAD state
**Handling**: Display error "Cannot determine current branch. Please checkout a branch before generating PR description."

### EC-006: No Remote Configured

**Scenario**: Repository has no remote configured
**Handling**: Default to GitHub terminology with a warning

## Output Format Example

### GitHub PR Example

```markdown
## Pull Request: Add User Authentication Feature

### Context
This PR implements user authentication to address security requirements
defined in spec #001. Users currently cannot securely log in to the system,
which prevents personalized experiences and data protection.

**Related User Stories:**
- As a user, I want to log in securely so that my data is protected

### Implementation
- Created `auth` module with JWT-based authentication
- Added password hashing using bcrypt
- Implemented session management with Redis
- Created login/logout API endpoints

**Key Files Changed:**
- `src/auth/__init__.py` - Authentication module
- `src/api/routes/auth.py` - Auth endpoints
- `tests/test_auth.py` - Unit tests

### Testing
- Unit tests: 95% coverage on auth module
- Integration tests: All API endpoints tested
- Manual testing: Login/logout flow verified

**Test Commands:**
```bash
pytest tests/test_auth.py -v
```

### How to Verify

1. Checkout this branch: `git checkout feature/auth`
2. Install dependencies: `uv sync`
3. Run tests: `uv run pytest tests/test_auth.py`
4. Start server: `uv run python -m app`
5. Test login at `http://localhost:8000/login`

```

### GitLab MR Example

```markdown
## Merge Request: Add User Authentication Feature

### Context
...

### Implementation
...

### Testing
...

### How to Verify
...
```

## Out of Scope

- Creating the actual PR/MR via API (only generates description text)
- Integration with issue trackers (Jira, Linear, etc.)
- PR template customization beyond section selection
- Multi-language support within a single PR description
- Automatic changelog generation
- Code review suggestions

## Dependencies

- Git CLI (for diff and log operations)
- Existing CodexSpec configuration structure
- Existing `/codexspec.commit` command patterns (for consistency)

## Related Commands

- `/codexspec.commit` - Generates commit messages for individual commits
- `/codexspec.specify` - Creates the spec.md that this command may reference
- `/codexspec.generate-spec` - Generates detailed specification documents

## Clarifications

### Session 2025-02-25

**Q1**: When multiple spec.md files exist, how should the correct one be selected?
**A1**: Use Option A - Default to NOT using spec.md unless user explicitly specifies `--spec` parameter
**Impact**: REQ-007, EC-004, Command Parameters, Story 3, TC-007, TC-008

**Rationale**: Users often make small changes without following SDD workflow. Defaulting to no spec avoids incorrect references to unrelated specs. The `--spec` parameter provides opt-in integration for SDD workflows.

**Q2**: When spec.md structure is incomplete (missing User Stories, etc.), how should extraction work?
**A2**: Use Option A - Best-effort extraction from available content, skip missing sections without error
**Impact**: REQ-005b (new), EC-004c (new)

**Rationale**: Avoids blocking workflow due to spec format issues. Users can still get useful Context from partial specs.

**Q3**: How should test files be discovered for the Testing section?
**A3**: Use Option B - Language-agnostic heuristics combining directory patterns and file name patterns
**Impact**: REQ-006b (new)

**Rationale**: Covers diverse project structures across languages without requiring language detection.

**Q4**: How should the PR title be generated?
**A4**: Use Option C - Comprehensive approach combining git diff analysis, branch name, and commit messages
**Impact**: REQ-008a (new)

**Rationale**: First commit may only represent partial work; branch names may not follow conventions; actual code changes provide the most accurate representation.

**Q5**: How should verification commands be generated for the "How to Verify" section?
**A5**: Use Option B - Project detection based on project files (pyproject.toml, package.json, etc.)
**Impact**: REQ-010 (new)

**Rationale**: Generates more actionable verification steps by detecting project-specific test commands, improving PR usability.

---
