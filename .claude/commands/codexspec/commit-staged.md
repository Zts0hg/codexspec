---
description: 分析暂存的 git 更改并生成符合 Conventional Commits 规范的提交信息
argument-hint: "[-p] 使用 -p 仅预览提交信息而不执行提交"
allowed-tools: Bash(git diff --staged:*), Bash(git diff --cached:*), Bash(git status:*), Bash(git commit:*)
forbidden-tools: Bash(git add:*), Bash(git reset:*), Bash(git checkout:*), Bash(git restore:*), Bash(git stash:*), Bash(git rm:*)
---

## Constitution Compliance (MANDATORY)

**Before generating commit messages:**

1. **Check for Constitution File**: Look for `.codexspec/memory/constitution.md`
2. **If Constitution Exists**:
   - Load and read relevant principles (especially coding standards, commit conventions)
   - Ensure commit message style aligns with constitutional guidelines
   - Verify that the changes being committed don't violate any principles
3. **If No Constitution Exists**: Proceed with default Conventional Commits format

## Configuration Check

**IMPORTANT**: Before proceeding, check if the project configuration exists.

### Execution Steps

1. **Check Configuration File**
   - Check if `.codexspec/config.yml` exists
   - This is a simple file existence check, no parsing needed at this stage

2. **If Configuration Does NOT Exist**
   - Display a one-time prompt:

     ```
     💡 检测到项目未配置语言设置。你可以使用 `/codexspec:config` 命令来创建配置文件。
     ```

   - Use default values for current session:
     - `language.output`: "en"
     - `language.commit`: "en"
     - `language.templates`: "en"
   - Continue with command execution normally

3. **If Configuration Exists**
   - Proceed to `## Language Preference` section
   - Read configuration and apply language settings as before

4. **Session State** (Implicit)
   - The prompt is shown only once per conversation session
   - Claude's conversation context naturally maintains this state
   - No additional mechanism needed

## Language Preference

**IMPORTANT**: Before generating commit messages, read the project's language configuration from `.codexspec/config.yml`.

**Commit message language priority**:

1. If `language.commit` is set, use that language for the commit message description
2. Otherwise, use `language.output` as fallback
3. If neither is configured, default to English

**Note**:

- The commit type (feat, fix, docs, etc.) and scope should always remain in English
- Only the description part should use the configured language
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate

## Parameter Check

Check if `$ARGUMENTS` contains `-p`:

- **If `-p` is present**: Preview mode - only output the commit message, do not execute `git commit`
- **If `-p` is NOT present**: Execute mode - generate the message and execute `git commit` directly

## Forbidden Operations (CRITICAL)

**SAFETY PRINCIPLE**: This command must NEVER modify the staging area. Only read staged changes and commit them as-is.

**UNDER NO CIRCUMSTANCES**:

- `git add` - Do not stage new files
- `git reset` - Do not unstage or rollback
- `git checkout` / `git restore` - Do not restore files
- `git stash` - Do not stash changes
- `git rm` - Do not remove files
- Any operation that modifies what is staged

**THE ONLY EXCEPTION** - Pre-commit Hook File Modifications:

- If a pre-commit hook modifies file content during commit, you MAY re-stage ONLY the files the hook modified
- This is the ONLY case where `git add` is permitted
- The hook output will indicate which files were modified

**If something seems wrong**: ABORT and inform the user. DO NOT attempt to "fix" or "repair" the staging area.

## Instructions

### Pre-commit Verification

Before analyzing changes, verify the staged state:

1. Run `git diff --staged --name-only` to confirm what is staged
2. If the list is empty, ABORT and inform the user (see Error Handling)
3. If the list seems incorrect or unexpected, ABORT and inform the user
4. DO NOT attempt to modify the staging area - only report what you see

### Change Analysis

1. Execute `git diff --staged` to retrieve staged changes.

2. Analyze the changes and generate a commit message that strictly follows **Conventional Commits** specification:
   - Format: `type(scope): description`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
   - If the project has a `CLAUDE.md` with custom commit conventions, follow those instead
   - **DO NOT** include any AI attribution in the commit message
   - Do not add `Co-Authored-By` lines or any references to AI tools/agents
   - The commit message should focus solely on describing the changes

3. **If preview mode (`-p`)**: Display the generated commit message and stop.

4. **If execute mode (default)**: Execute `git commit -m "..."` directly with the generated message.

### Pre-commit Hook Handling

If `git commit` fails due to a pre-commit hook modifying files:

1. Check the hook output to identify which files were modified
2. Re-stage ONLY those specific files: `git add <modified-files>`
3. Retry the commit with the same message
4. If it still fails or the situation is unclear, ABORT and inform the user

## Session Context Awareness

When analyzing changes, consider the current session context:

- What the user has been working on in this session
- The purpose and goals discussed in the conversation
- Any related specifications, plans, or tasks mentioned

This context helps generate more meaningful commit messages that reflect the "why" behind the changes, not just the "what".

## Important Notes

- In execute mode (default), execute `git commit` directly after generating the message
- In preview mode (`-p`), only display the commit message without executing
- For breaking changes, include `BREAKING CHANGE:` in the commit body
- Keep the description concise and in imperative mood (e.g., "add feature" not "added feature")

## Error Handling

**If no staged changes exist**:

- Inform the user: "No staged changes found"
- Suggest: "Use `git add <files>` to stage files first"
- DO NOT attempt to stage files automatically

**If unexpected state is detected**:

- ABORT immediately
- Report the issue clearly to the user
- DO NOT use `git reset`, `git checkout`, `git restore`, or any repair operations
- Let the user decide how to proceed

**If commit fails for unknown reasons**:

- Report the error message to the user
- DO NOT attempt to "fix" the situation
- The user should investigate and resolve manually
