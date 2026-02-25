---
description: Generate structured Pull Request (GitHub) or Merge Request (GitLab) descriptions based on git diff and optional spec.md integration
allowed-tools: Bash(git branch:*), Bash(git diff:*), Bash(git log:*), Bash(git remote:*), Bash(git rev-parse:*), Bash(ls:*), Bash(cat:*)
---

## Language Preference

**IMPORTANT**: Before generating PR descriptions, read the project's language configuration from `.codexspec/config.yml`.

**PR description language priority**:
1. If `language.commit` is set, use that language for the PR description
2. Otherwise, use `language.output` as fallback
3. If neither is configured, default to English

**Note**:
- Technical terms (e.g., API, JWT, OAuth, PR, MR) may remain in English when appropriate
- The PR title and section headers should follow the configured language

**Examples**:
- `output: "zh-CN"` + `commit: "en"` → Chinese interactions, English PR descriptions
- `output: "zh-CN"` + `commit: "zh-CN"` → Chinese for both
- `output: "zh-CN"` + no `commit` setting → Chinese for both (fallback)

## User Input

```
$ARGUMENTS
```

## Parameters

Parse `$ARGUMENTS` for the following optional parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--target-branch <branch>` | `origin/main` | Branch to compare against |
| `--output <file>` | (none) | Save output to file instead of terminal |
| `--sections <list>` | `all` | Comma-separated sections to include |
| `--spec <path>` | (none) | Enable spec.md integration (opt-in) |

### `--sections` Values
- `context` - Background and problem statement
- `implementation` - Technical approach
- `testing` - Test coverage information
- `verify` - Verification steps
- `all` - Include all sections (default)

Example: `--sections context,implementation,verify`

### `--spec` Usage (Opt-in)

By default, spec.md is **NOT** used. Use `--spec` to enable SDD workflow integration:

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

## Git Context Collection

Execute the following commands to gather git context:

1. **Current Branch**: `git branch --show-current`
2. **Current Branch (full ref)**: `git rev-parse --abbrev-ref HEAD`
3. **Remote URL**: `git remote get-url origin` (or error if no remote)
4. **Commits Ahead**: `git log --oneline --no-merges <target-branch>..HEAD`
5. **File Changes**: `git diff --name-status <target-branch>...HEAD`
6. **Full Diff**: `git diff <target-branch>...HEAD`
7. **Commit Messages**: `git log --pretty=format:"%s" --no-merges <target-branch>..HEAD`

## Platform Detection

Detect the Git platform from the remote URL:

### Detection Rules

1. **GitHub**: URL contains `github.com`
   - Use "Pull Request" terminology
   - Title format: `## Pull Request: [Title]`

2. **GitLab**: URL contains `gitlab.com`
   - Use "Merge Request" terminology
   - Title format: `## Merge Request: [Title]`

3. **Other/No Remote**: Default to GitHub terminology
   - Display warning if no remote configured

## Spec.md Integration (Opt-in)

Only when `--spec` is provided, read spec.md for Context section.

### Spec Resolution

1. If `--spec` is a number like `001`, resolve to `.codexspec/specs/001-*/spec.md`
2. If `--spec` is a directory name like `001-auth`, resolve to `.codexspec/specs/001-auth/spec.md`
3. If `--spec` is a path, use directly

### Content Extraction (Best-Effort)

Extract content from spec.md with priority order:
1. **User Stories** - Primary source for Context
2. **Goals** - Fallback if no User Stories
3. **Overview** - Fallback if no Goals
4. **Requirements** - Last resort

**Graceful Degradation**:
- If spec structure is incomplete, use available sections
- Do not error or warn on incomplete specs
- Skip Context section if no spec or extraction fails

### Invalid Spec Path Handling

If `--spec` path doesn't exist:
1. List available specs: `ls .codexspec/specs/`
2. Display error: "Spec '[path]' not found. Available specs: [list]"
3. Continue without Context section

## PR Title Generation

Generate the PR title using a **comprehensive approach**:

1. **Primary Source**: Analyze git diff content
   - Identify main components/modules changed
   - Understand the nature of changes (feature, fix, refactor, etc.)

2. **Supporting Sources**:
   - Branch name (extract feature/fix hints)
   - Commit messages (understand intent)

3. **Synthesis**:
   - Combine insights into a single descriptive title
   - Keep it concise but informative
   - Use imperative mood (e.g., "Add" not "Added")

**Example**:
- Branch: `feature/auth-cleanup`
- First commit: "Add password validation"
- Actual changes: Full authentication refactor
- **Generated title**: "Refactor Authentication System with JWT and Session Management"

## Test File Discovery

Identify test files using language-agnostic patterns:

### Directory Patterns
- `tests/`
- `test/`
- `__tests__/`
- `spec/`

### File Name Patterns
- `*_test.py`, `test_*.py`
- `*.test.js`, `*.spec.ts`
- `*_test.go`
- `*Test.java`, `*Tests.java`

### Combined Approach
Match files that are:
- In test directories, OR
- Match file name patterns

## Project Command Detection

Detect project-specific test commands for "How to Verify" section:

| Detection | Command | Example |
|-----------|---------|---------|
| `pyproject.toml` + (`pytest.ini` OR `tests/`) | `pytest` | `uv run pytest` or `pytest` |
| `package.json` + `jest.config.js` | `npm test` | `npm test` |
| `package.json` + `vitest.config.ts` | `npm run test` | `npm run test` |
| `Cargo.toml` | `cargo test` | `cargo test` |
| `go.mod` | `go test` | `go test ./...` |
| `Makefile` with `test` target | `make test` | `make test` |

**Fallback**: If no project files detected, use generic steps:
1. Install dependencies
2. Run tests

## Section Generation

Generate PR sections based on gathered information:

### Context Section
- **Include**: Only if `--spec` is provided and spec.md found
- **Content**: Extract from spec.md (User Stories, Goals, Overview)
- **Skip**: If no spec or extraction fails

### Implementation Section
- **Source**: Git diff analysis
- **Content**:
  - Summary of technical changes
  - Key files changed with brief descriptions
  - Architectural decisions if apparent

### Testing Section
- **Source**: Test file discovery + commit messages
- **Content**:
  - Test files discovered
  - Test coverage information (if available in commits)
  - Test commands to run

### How to Verify Section
- **Source**: Project command detection
- **Content**:
  - Step-by-step verification instructions
  - Project-specific test commands
  - Manual verification steps if applicable

## Section Selection

If `--sections` is specified, only include listed sections:
- `context` → Include Context section
- `implementation` → Include Implementation section
- `testing` → Include Testing section
- `verify` → Include How to Verify section
- `all` → Include all sections (default)

## Output Format

### GitHub PR Format

```markdown
## Pull Request: [Title]

### Context
[Background from spec.md if --spec used]

### Implementation
[Technical changes summary]

**Key Files Changed:**
- `path/to/file.py` - [Brief description]
- `path/to/another.py` - [Brief description]

### Testing
[Test coverage and methodology]

**Test Commands:**
```bash
[project-specific test commands]
```

### How to Verify
1. [Step 1]
2. [Step 2]
3. [Step 3]
...
```

### GitLab MR Format

```markdown
## Merge Request: [Title]

### Context
...

### Implementation
...

### Testing
...

### How to Verify
...
```

## Edge Cases

### EC-001: Branch Up to Date with Target
**Scenario**: No commits ahead of target branch
**Response**: "No changes detected between current branch and [target]. Nothing to generate."

### EC-002: Invalid Target Branch
**Scenario**: Target branch doesn't exist
**Response**: "Target branch '[branch]' not found. Please verify the branch name."

### EC-003: Not a Git Repository
**Scenario**: Command run outside git repo
**Response**: "Not a git repository. Please run this command from within a git repository."

### EC-004b: Invalid Spec Path
**Scenario**: `--spec` path doesn't exist
**Response**: "Spec '[path]' not found. Available specs: [list specs in .codexspec/specs/]"

### EC-005: Detached HEAD State
**Scenario**: Repository in detached HEAD
**Response**: "Cannot determine current branch. Please checkout a branch before generating PR description."

### EC-006: No Remote Configured
**Scenario**: No git remote configured
**Handling**: Use GitHub terminology with warning: "No remote configured. Defaulting to GitHub terminology."

## Output Modes

### Terminal Output (Default)
Print the generated PR description to stdout for copy-paste.

### File Output (`--output`)
Save the PR description to the specified file path.

## Important Notes

- Always verify the current branch has commits ahead of target before generating
- The PR description should be self-contained and understandable without external context
- Include enough detail for reviewers to understand the changes
- Do not include any AI attribution in the PR description
- Focus on clarity and usefulness for code reviewers
