---
description: Analyze staged git changes and generate Conventional Commits compliant commit messages
allowed-tools: Bash(git diff:*), Bash(git commit:*)
---

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate
- All user-facing messages, questions, and generated documents should use the configured language

## Instructions

1. Execute `git diff --staged` to retrieve staged changes.

2. Analyze the changes and generate a commit message that strictly follows **Conventional Commits** specification:
   - Format: `type(scope): description`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
   - If the project has a `CLAUDE.md` with custom commit conventions, follow those instead
   - **DO NOT** include any AI attribution in the commit message
   - Do not add `Co-Authored-By` lines or any references to AI tools/agents
   - The commit message should focus solely on describing the changes

3. Present the generated commit message to the user and ask for confirmation.

4. If confirmed, execute `git commit -m "..."` with the generated message.

## Important Notes

- If no staged changes exist, inform the user and suggest using `git add` first
- For breaking changes, include `BREAKING CHANGE:` in the commit body
- Keep the description concise and in imperative mood (e.g., "add feature" not "added feature")
