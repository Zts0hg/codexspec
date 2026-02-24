---
description: Generate Conventional Commits compliant commit messages based on git status and session context
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git branch:*), Bash(git add:*), Bash(git commit:*)
---

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, commit messages, and interactions should use the configured language

## Git Context Collection

Execute the following commands to gather git context:

1. **Current Branch**: `git branch --show-current`
2. **File Status**: `git status --short`
3. **Staged Changes**: `git diff --staged`
4. **Unstaged Changes**: `git diff`

## Decision Logic

Based on the git context, follow this priority order:

### Case A: Staged Changes Exist (Priority)

1. Ignore unstaged changes
2. Generate a commit message based on staged changes only
3. Consider the current session conversation history to understand the intent and context
4. Present the commit message to user for confirmation
5. If confirmed, execute `git commit -m "..."`

### Case B: No Staged Changes, But Unstaged Changes Exist

1. **IMPORTANT**: Display a prominent warning at the beginning: "Staging area is empty. The following is a suggested commit message based on working directory changes. Please run `git add` first."
2. Analyze the unstaged changes
3. Generate a **suggested** commit message
4. **REMINDER**: After displaying the commit message, repeat the reminder: "Remember: You must stage changes with `git add` before committing."
5. Ask user if they want to stage all changes and commit

### Case C: No Changes At All

Respond with: "Working directory is clean. No changes detected."

## Commit Message Format

Generate commit messages following **Conventional Commits** specification:

- Format: `type(scope): description`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
- If the project has a `CLAUDE.md` with custom commit conventions, follow those instead
- For breaking changes, include `BREAKING CHANGE:` in the commit body
- Keep the description concise and in imperative mood (e.g., "add feature" not "added feature")

## Session Context Awareness

When analyzing changes, consider:
- What the user has been working on in this session
- The purpose and goals discussed in the conversation
- Any related specifications, plans, or tasks mentioned

This context helps generate more meaningful commit messages that reflect the "why" behind the changes, not just the "what".

## Important Notes

- Always confirm with user before executing `git commit`
- For Case B, display a prominent reminder at the **beginning** before showing the suggested commit message, AND repeat the reminder at the **end** after displaying the message. This ensures the user is aware that the commit message is generated based on unstaged changes (not staged changes), so they can take appropriate action: proceed if intentional, or re-stage specific files and run the command again if they forgot to stage.
- Do not make assumptions about change intent without context
