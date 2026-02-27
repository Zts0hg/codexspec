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

Generate the PR title following **Conventional Commits** specification:

- Format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- If the project has a `CLAUDE.md` with custom commit conventions, follow those instead

### Generation Process

1. **Primary Source**: Analyze git diff content
   - Identify main components/modules changed
   - Understand the nature of changes (feature, fix, refactor, etc.)
   - Determine the appropriate **type** prefix

2. **Supporting Sources**:
   - Branch name (extract feature/fix hints)
   - Commit messages (understand intent, look for existing type prefixes)

3. **Synthesis**:
   - Combine insights into a single descriptive title
   - Keep it concise but informative
   - Use imperative mood (e.g., "Add" not "Added")

### Type Determination Rules

| Type | When to Use |
|------|-------------|
| `feat` | New feature or functionality |
| `fix` | Bug fix |
| `docs` | Documentation changes only |
| `style` | Code style changes (formatting, semicolons, etc.) |
| `refactor` | Code refactoring without changing behavior |
| `perf` | Performance improvements |
| `test` | Adding or modifying tests |
| `build` | Build system or dependency changes |
| `ci` | CI/CD configuration changes |
| `chore` | Other changes that don't modify src or test files |
| `revert` | Reverting a previous commit |

### Scope (Optional)

Add scope when changes are focused on a specific module/component:
- `feat(auth): add OAuth2 support`
- `fix(api): handle timeout errors`
- `refactor(core): improve caching mechanism`

**Example**:
- Branch: `feature/auth-cleanup`
- First commit: "Add password validation"
- Actual changes: Full authentication refactor
- **Generated title**: `refactor(auth): improve authentication system with JWT and session management`

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

**IMPORTANT**: Generate PR descriptions using proper Markdown formatting for optimal rendering across all platforms (GitHub, GitLab, Bitbucket, etc.).

### Markdown Structure Guidelines

1. **Title**: Use `##` for the PR title (first line of description)
2. **Sections**: Use `###` for main sections (Context, Implementation, Testing, etc.)
3. **Subsections**: Use `####` for subsections within main sections
4. **Lists**: Use proper bullet points `-` or numbered lists `1.`
5. **Code**: Use fenced code blocks with language hints (```bash, ```python, etc.)
6. **Tables**: Use Markdown tables for structured data (file changes, test results, etc.)
7. **Emphasis**: Use `**bold**` for key terms, `*italic*` for subtle emphasis
8. **Links**: Use `[text](url)` format for references
9. **Task Lists**: Use `- [ ]` and `- [x]` for verification checklists

### GitHub PR Format

```markdown
## type(scope): description

> Brief summary of what this PR accomplishes (1-2 sentences)

### Summary

[High-level overview of changes and motivation]

### Changes

#### Key Modifications
| File | Change Type | Description |
|------|-------------|-------------|
| `path/to/file.py` | Modified | Brief description of change |
| `path/to/another.py` | Added | Brief description of new file |

#### Technical Details
[Detailed explanation of implementation approach, architectural decisions, etc.]

### Testing

**Test Coverage:**
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

**Run Tests:**
```bash
[project-specific test commands]
```

### How to Verify

1. [Step 1 - e.g., Checkout the branch]
2. [Step 2 - e.g., Install dependencies]
3. [Step 3 - e.g., Run tests with specific command]
4. [Step 4 - e.g., Verify expected behavior]

### Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if applicable)
- [ ] No new warnings introduced
- [ ] Tests pass locally

### Notes

[Any additional notes, breaking changes, or migration instructions]

---
*Related: #[issue-number]* (if applicable)
```

### GitLab MR Format

```markdown
## type(scope): description

> Brief summary of what this MR accomplishes (1-2 sentences)

### Summary

[High-level overview of changes and motivation]

### Changes

| File | Change Type | Description |
|------|-------------|-------------|
| `path/to/file.py` | Modified | Brief description of change |

#### Technical Details
[Detailed explanation of implementation approach]

### Testing

**Test Coverage:**
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated

**Run Tests:**
```bash
[project-specific test commands]
```

### How to Verify

1. [Step 1 - e.g., Checkout the branch]
2. [Step 2 - e.g., Install dependencies]
3. [Step 3 - e.g., Run tests]

### Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if applicable)

### Notes

[Any additional notes or breaking changes]

/label ~"[label]" @reviewer (if applicable)
```

### Section Content Guidelines

#### Summary Section
- Keep to 2-3 sentences maximum
- Answer "What" and "Why" (not "How")
- Use plain language accessible to all reviewers

#### Changes Section
- Use tables for file changes (improves readability)
- Group related changes logically
- Include change type: Added, Modified, Deleted, Renamed

#### Testing Section
- Use task lists for test coverage status
- Include exact commands to run tests
- Note any special test requirements

#### How to Verify Section
- Use numbered list for step-by-step verification
- Include specific commands to run
- Be precise and actionable (e.g., "Run `pytest tests/auth/`")
- Include expected outcomes where helpful

#### Checklist Section
- Use GitHub/GitLab task list syntax `- [ ]`
- Include project-specific checklist items
- Focus on author self-confirmation before merge

#### Notes Section
- Highlight breaking changes with `**Breaking Change:**` prefix
- Include migration instructions if needed
- Link to related issues/PRs

### Title Examples

| Type | Example Title |
|------|---------------|
| Feature | `feat(auth): add OAuth2 login support` |
| Bug Fix | `fix(api): resolve timeout issue in user endpoint` |
| Refactor | `refactor(core): improve caching mechanism` |
| Documentation | `docs: update API documentation` |
| Performance | `perf(db): optimize query performance` |
| Test | `test(auth): add unit tests for password validation` |

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
