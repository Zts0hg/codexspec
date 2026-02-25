---
description: Generate and execute Conventional Commits compliant commit messages based on git status and session context
argument-hint: "[-p] Use -p to only preview the message without committing"
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git add:*), Bash(git commit:*)
---

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

**Examples**:
- `output: "zh-CN"` + `commit: "en"` → Chinese interactions, English commits
- `output: "zh-CN"` + `commit: "zh-CN"` → Chinese for both
- `output: "zh-CN"` + no `commit` setting → Chinese for both (fallback)

## Git Context Collection

Execute the following commands to gather git context:

1. **Current Branch**: `git branch --show-current`
2. **File Status**: `git status --short`
3. **Staged Changes**: `git diff --staged`
4. **Unstaged Changes**: `git diff`

## Parameter Check

Check if `$ARGUMENTS` contains `-p`:
- **If `-p` is present**: Preview mode - only output the commit message, do not execute `git commit`
- **If `-p` is NOT present**: Execute mode - generate the message and execute `git commit` directly

## Decision Logic

Based on the git context, follow this priority order:

### Case A: Staged Changes Exist (Priority)

1. Ignore unstaged changes
2. Generate a commit message based on staged changes only
3. Consider the current session conversation history to understand the intent and context
4. **If preview mode (`-p`)**: Display the commit message and stop
5. **If execute mode (default)**: Execute `git commit -m "..."` directly

### Case B: No Staged Changes, But Unstaged Changes Exist

1. **IMPORTANT**: Display a prominent warning at the beginning: "Staging area is empty. The following is a suggested commit message based on working directory changes. Please run `git add` first."
2. Analyze the unstaged changes
3. Generate a **suggested** commit message
4. **REMINDER**: After displaying the commit message, repeat the reminder: "Remember: You must stage changes with `git add` before committing."
5. **STOP here** - Do NOT execute any git commands. The user must manually stage the appropriate changes first.

**Rationale**: When staging area is empty, we cannot safely assume which changes should be committed. The user may only want to commit a subset of the changes, or may need to split changes into multiple commits. Always require explicit user action to stage changes.

### Case C: No Changes At All

Respond with: "Working directory is clean. No changes detected."

## Commit Message Format

Generate commit messages following **Conventional Commits** specification:

- Format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- If the project has a `CLAUDE.md` with custom commit conventions, follow those instead
- For breaking changes, include `BREAKING CHANGE:` in the commit body
- Keep the description concise and in imperative mood (e.g., "add feature" not "added feature")
- **DO NOT** include any AI attribution in the commit message
- Do not add `Co-Authored-By` lines or any references to AI tools/agents
- The commit message should focus solely on describing the changes

## Session Context Awareness

When analyzing changes, consider:
- What the user has been working on in this session
- The purpose and goals discussed in the conversation
- Any related specifications, plans, or tasks mentioned

This context helps generate more meaningful commit messages that reflect the "why" behind the changes, not just the "what".

## Important Notes

- In execute mode (default), execute `git commit` directly after generating the message (only for Case A with staged changes)
- In preview mode (`-p`), only display the commit message without executing
- For Case B (no staged changes), always display the suggested message and stop - never auto-stage or auto-commit
- Do not make assumptions about change intent without context
