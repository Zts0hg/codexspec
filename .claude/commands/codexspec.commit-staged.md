---
description: Analyze staged git changes and generate Conventional Commits compliant commit messages
argument-hint: "[-p] Use -p to only preview the message without committing"
allowed-tools: Bash(git diff:*), Bash(git commit:*)
---

## Constitution Compliance (MANDATORY)

**Before generating commit messages:**

1. **Check for Constitution File**: Look for `.codexspec/memory/constitution.md`
2. **If Constitution Exists**:
   - Load and read relevant principles (especially coding standards, commit conventions)
   - Ensure commit message style aligns with constitutional guidelines
   - Verify that the changes being committed don't violate any principles
3. **If No Constitution Exists**: Proceed with default Conventional Commits format

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

## Instructions

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

## Important Notes

- In execute mode (default), execute `git commit` directly after generating the message
- In preview mode (`-p`), only display the commit message without executing
- If no staged changes exist, inform the user and suggest using `git add` first
- For breaking changes, include `BREAKING CHANGE:` in the commit body
- Keep the description concise and in imperative mood (e.g., "add feature" not "added feature")
