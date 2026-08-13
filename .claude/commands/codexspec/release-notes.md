---
description: Generate release notes from git history — maintain a Keep a Changelog CHANGELOG.md entry and emit a user-facing release body, without deciding versions or mutating git state
allowed-tools: Bash(git branch:*), Bash(git tag:*), Bash(git describe:*), Bash(git log:*), Bash(git diff:*), Bash(git rev-parse:*), Bash(git remote:*), Bash(ls:*), Bash(cat:*), Read, Edit, Write
---

## Constitution Compliance (MANDATORY)

**Before generating release notes:**

1. **Check for Constitution File**: Look for `.codexspec/memory/constitution.md`
2. **If Constitution Exists**:
   - Load and read relevant principles (especially documentation and versioning standards)
   - Ensure the generated notes align with constitutional guidelines
3. **If No Constitution Exists**: Proceed with the defaults below

## Language Preference

**IMPORTANT**: Before generating output, read the project's language configuration from `.codexspec/config.yml`.

**Generated-content language priority**:

1. If `language.commit` is set, use that language for the CHANGELOG entry and release body
2. Otherwise, use `language.output` as fallback
3. If neither is configured, default to English

**Note**:

- Section headings that are format keywords (`Added`, `Changed`, `Fixed`, etc.) and technical terms
  (API, JWT, OAuth) may remain in English when appropriate.
- The `## [Unreleased]` / `## [X.Y.Z]` version markers and ISO dates are format, not prose — keep them
  as-is.

## User Input

```
$ARGUMENTS
```

## Role

You generate **release notes** from git history for **this project**, whatever its release process.
You make **no assumption** about how the project releases: there may be no `publish.sh`, no CI, no
particular hosting platform, and no particular versioning scheme (semver, CalVer, and date tags are
all possible). Every behavior below degrades gracefully when such an assumption does not hold.

You produce two layered outputs from the same analysis:

1. A developer **CHANGELOG.md** entry in Keep a Changelog format.
2. A user-facing **release body** derived from it.

You **own no versioning** and **mutate no git state** (see Forbidden Operations).

## Forbidden Operations (CRITICAL)

This command is a **generator**, sharing the safety discipline of `commit-staged` and `pr`.

**UNDER NO CIRCUMSTANCES**:

- `git add` / `git commit` / `git reset` / `git checkout` / `git restore` / `git stash` / `git rm` —
  the command MUST NEVER modify the git staging area and MUST NEVER create a commit.
- Overwrite `CHANGELOG.md` wholesale with `Write`, or rewrite / reorder / delete any existing
  CHANGELOG entry.
- Decide or "own" a version bump; tag; publish; or create a GitHub/GitLab release.
- Include any AI attribution in generated content — no `Co-Authored-By`, "Generated with", robot
  emoji, or references to AI tools/agents.

The **only** permitted file writes are: the safe additive `CHANGELOG.md` insertion described in
**CHANGELOG.md Maintenance**, and — only when `--output <file>` is given — writing the release body to
that user-directed path.

## Parameters

Parse `$ARGUMENTS` for the following optional parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--version <X.Y.Z>` | (none) | Stamp this version on the new section; short-circuits all version inference/suggestion |
| `--from <ref>` | (resolved) | Explicit range start (overrides Range Resolution) |
| `--to <ref>` | `HEAD` | Explicit range end |
| `--output <file>` | (terminal) | Write the release body to a file instead of stdout |
| `--spec <feature>` | (none) | Enrich the "why" from that feature's `spec.md` / `tasks.md` |

- If `--version` is present, **validate** it is a well-formed version string. If it is malformed,
  **reject** with a clear validation message and do **not** write a malformed section.
- If `--spec` is present but does not resolve to an existing feature/path, **degrade gracefully**:
  proceed from git alone and report the unresolved path. Do not fail.

## Range Resolution

Determine the commit range `<from>..<to>` (default `<to>` is `HEAD`):

1. **Explicit override**: if `--from` (and optionally `--to`) is given, use it directly.
2. **Latest tag**: otherwise, the default range is `latest tag..HEAD` — resolve the latest tag via
   `git describe --tags --abbrev=0`.
3. **No reachable tag → CHANGELOG fallback**: if the repository has no reachable tag, fall back to
   "after the last version recorded in `CHANGELOG.md`" (anchor on the most recent versioned section).
4. **No tag and no CHANGELOG (or no anchorable version) → full history**: if neither a tag nor an
   anchorable CHANGELOG version exists (for example the only prior section is `Unreleased`, which has
   no commit anchor), summarize the **full history**.

Always apply `--no-merges` so merge commits are excluded. Route the Edge Cases below before analysis.

## Git Context Collection

Over the resolved range, collect:

1. **Commits**: `git log --no-merges --pretty=format:"%H %s" <from>..<to>`
2. **Full diff**: `git diff <from>..<to>` (to understand what each commit actually changed)
3. When `--spec` resolves: read that feature's `spec.md` / `tasks.md` for intent ("why").

## Change Categorization

Group the changes into **Keep a Changelog** categories, including only those that apply:

- `### Added` — new features
- `### Changed` — changes to existing functionality
- `### Deprecated` — soon-to-be-removed features
- `### Removed` — removed features
- `### Fixed` — bug fixes
- `### Security` — security fixes

**Conventional commits are used when present but are NOT required.** When commits do not follow the
convention, **infer** the category and wording from the **diff and commit subjects** (the "diff is the
source of truth" approach of `commit-staged` / `pr`).

**User-facing vs contributor split**: the user-facing lists lead with user-visible changes
(`feat` / `fix` / `perf`, and anything a user would notice). Internal / contributor-only changes
(`chore` / `refactor` / `test` / `ci` / `build`, internal docs) go **only** under a separate
`### For contributors` subsection. When commit types are absent, infer visibility from the diff.

## Completeness Cross-Check

After drafting, **cross-check** the entry against the commit list: **every non-merge commit in the
selected range must map to at least one bullet.** If any commit is unrepresented, add it. Do not pad
with bullets that correspond to no commit.

## Version Handling

Choose the new section's label:

- **Default**: `## [Unreleased]` — with **no date** (the Keep a Changelog convention for accumulating
  changes before a version is assigned).
- **`--version X.Y.Z` given**: stamp `## [X.Y.Z] - <YYYY-MM-DD>` (today's ISO date) and **skip all
  version inference and suggestion**.

**Guarded advisory** (only when `--version` is absent): print a console-only suggested next version
**only when** the project is detected to use **semver AND conventional commits** — i.e. existing
tags/versions are semver-shaped *and* the range's commits carry conventional-commit prefixes. In that
case print the suggested next version, the reasoning (e.g. counts of `feat` / `fix` / breaking), and
an explicit "override with `--version`" note. **Otherwise stay silent** on version suggestions.

The command MUST **never write a version number into the file on its own** — the file section is only
ever `## [Unreleased]` or a user-provided `--version`.

## CHANGELOG.md Maintenance

Maintain `CHANGELOG.md` at the repository root with a **safe, additive** edit:

1. **Create if absent**: if `CHANGELOG.md` does not exist, create it with the **standard Keep a
   Changelog header**:

   ```markdown
   # Changelog

   All notable changes to this project will be documented in this file.

   The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
   and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
   ```

2. **Insert additively**: read the entire existing `CHANGELOG.md` first. Insert the new section at a
   single insertion point — into an existing `## [Unreleased]` section when one is present (merge the
   new bullets in rather than duplicating the section), else immediately above the most recent
   versioned section, else directly after the header. **Never rewrite, reorder, or delete any
   existing entry.**
3. **Edit, never overwrite**: perform the insertion with a precise `Edit` (exact `old_string` match)
   — **never** use `Write` to overwrite the whole `CHANGELOG.md`.

This is the command's only mutation of `CHANGELOG.md`, and it never touches git state.

## Release Body Generation

Derive the user-facing **release body** from the same categorized model:

- Lead with what the user **can now do** — "You can now…", plain language, not implementation detail.
- Keep internal/contributor changes under a `### For contributors` subsection, out of the main list.
- Flag breaking changes visibly (`**Breaking change:**`).
- The body is **generic markdown**, platform-agnostic — the user pastes it into GitHub / GitLab / any
  release page. The command does **not** publish it.

## Output Modes

- **Terminal (default)**: print the release body to the terminal wrapped in a markdown code block so
  the raw markdown can be copied.
- **`--output <file>`**: write the raw release body to that file (the one user-directed file write
  permitted besides the CHANGELOG insertion).

The `CHANGELOG.md` entry is written in both modes.

## Edge Cases

- **Not a git repository**: report "Not a git repository." and take no action.
- **Empty range** (no commits since the resolved start): report "No changes to release." — do not
  fabricate entries and do not error.
- **Detached HEAD**: report that the branch cannot be determined and stop, rather than guessing.
- **Unresolved `--spec`**: proceed from git alone and report the unresolved path (see Parameters).
- **Malformed `--version`**: reject with a clear validation message; write no malformed section.

## Automatic Distillation

This command has **no** Automatic Distillation step. It is a generator, not an interaction that
produces reusable cross-feature knowledge.
