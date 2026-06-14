# Implementation Plan: PR Description Generator

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | Project requirement |
| CLI Framework | Typer | 0.9+ | Existing framework |
| Formatting | Rich | 13+ | Existing for console output |
| Package Manager | uv | Latest | Existing |
| Testing | pytest | 7+ | Existing |
| Linting | ruff | Latest | Existing |

**No new dependencies required** - The feature is a slash command template (Markdown file), not Python code.

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | Template follows clear structure with defined sections |
| Testing Standards | ✅ | 10 test cases defined in spec; will add template validation |
| Documentation | ✅ | Template includes inline instructions and examples |
| Architecture | ✅ | Follows existing command pattern (single .md file in templates/) |
| Performance | ✅ | No performance concerns for a Markdown template |
| Security | ✅ | No security implications (read-only operations via Claude) |

## 3. Architecture Overview

This feature is implemented as a **slash command template** - a Markdown file with YAML frontmatter. The template instructs Claude Code on how to generate PR/MR descriptions.

```
┌─────────────────────────────────────────────────────────────┐
│                     User invokes command                     │
│                    /codexspec.pr [options]                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Claude Code loads template                 │
│              templates/commands/pr.md                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Claude executes template steps              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ Read config │→ │ Detect git  │→ │ Gather information  │  │
│  │ (language)  │  │ platform    │  │ (diff, commits)     │  │
│  └─────────────┘  └─────────────┘  └──────────┬──────────┘  │
│                                           │                 │
│                                           ▼                 │
│                              ┌─────────────────────────┐    │
│                              │ If --spec: read spec.md  │    │
│                              └─────────────────────────┘    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Generate PR description                   │
│     - Title (comprehensive: diff + branch + commits)        │
│     - Context (from spec.md if --spec used)                 │
│     - Implementation (from git diff analysis)               │
│     - Testing (from test file detection)                    │
│     - How to Verify (project-detected commands)             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       Output result                          │
│            Terminal (default) or File (--output)            │
└─────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

```
codexspec/
├── templates/
│   └── commands/
│       ├── commit.md           # Existing - generates commit messages
│       ├── commit-staged.md    # Existing - generates commit for staged
│       └── pr.md               # NEW - generates PR/MR descriptions
│
├── .claude/
│   └── commands/
│       ├── codexspec.commit.md
│       ├── codexspec.commit-staged.md
│       └── codexspec.pr.md     # NEW - installed by codexspec init
│
└── tests/
    └── test_pr_template.py     # NEW - template validation tests
```

## 5. Module Dependency Graph

```
┌─────────────────────┐
│   codexspec init    │  (CLI command)
└──────────┬──────────┘
           │ copies
           ▼
┌─────────────────────┐
│ templates/commands/ │
│      pr.md          │  (NEW - template file)
└──────────┬──────────┘
           │ used by
           ▼
┌─────────────────────┐
│    Claude Code      │  (reads and executes template)
└──────────┬──────────┘
           │ reads (optional)
           ▼
┌─────────────────────┐
│ .codexspec/config.yml│  (for language settings)
└─────────────────────┘

┌─────────────────────┐
│ .codexspec/specs/*/ │  (optional, via --spec)
│    spec.md          │
└─────────────────────┘
```

## 6. Module Specifications

### Module: pr.md (Template File)

- **Responsibility**: Instruct Claude Code on how to generate structured PR/MR descriptions
- **Dependencies**: None (self-contained Markdown with embedded instructions)
- **Interface**: YAML frontmatter with `description` and `allowed-tools`
- **Files**:
  - Create: `templates/commands/pr.md`
  - Created on `codexspec init`: `.claude/commands/codexspec.pr.md`

### Template Sections

| Section | Purpose |
|---------|---------|
| YAML Frontmatter | Define description, allowed tools |
| Language Preference | Configure output language (priority: commit > output > en) |
| Git Context Collection | Commands to gather branch, diff, commit info |
| Platform Detection | Logic to detect GitHub vs GitLab from remote URL |
| Spec Integration (Opt-in) | Instructions for reading spec.md via `--spec` parameter |
| Test File Discovery | Language-agnostic patterns for finding test files |
| Project Command Detection | Detect test commands from project files (pyproject.toml, etc.) |
| Section Generation | Logic for each PR section (Context, Implementation, Testing, Verify) |
| Parameter Handling | How to process --target-branch, --output, --sections, --spec |
| Output Format | Markdown structure for generated PR description |
| Edge Case Handling | Error messages and fallback behaviors |

## 7. Data Models

N/A - This feature is a template file, not a data-driven application.

## 8. API Contracts

### Command: `/codexspec.pr`

**Arguments**: `$ARGUMENTS` (parsed by Claude)

**Options** (via $ARGUMENTS):

- `--target-branch <branch>` - Target branch for comparison (default: `origin/main`)
- `--output <file>` - Output file path (default: terminal only)
- `--sections <list>` - Comma-separated sections (default: `all`)
- `--spec <path>` - Path to spec.md or spec directory name (e.g., `001-auth`)

**Output Format**:

```markdown
## [Pull Request|Merge Request]: [Title from comprehensive analysis]

### Context
[Background and problem statement from spec.md if --spec used]

### Implementation
[Technical approach summary from git diff analysis]

**Key Files Changed:**
- `path/to/file.py` - [Brief description]

### Testing
[Test coverage and methodology from test files and commits]

**Test Commands:**
```bash
[Project-detected test commands]
```

### How to Verify

1. [Step 1 with project-specific commands]
2. [Step 2]
...

```

**Exit Conditions**:
- Success: PR description generated and output to terminal/file
- No changes: Message "No changes detected between [branch] and [target]"
- Error: Clear error message for invalid branch, not a git repo, invalid spec path, etc.

## 9. Implementation Phases

### Phase 1: Template Creation
- [ ] Create `templates/commands/pr.md` with YAML frontmatter
- [ ] Add language preference section (matching commit.md pattern)
- [ ] Add git context collection instructions
- [ ] Add platform detection logic

### Phase 2: Core Functionality
- [ ] Add spec.md integration instructions (opt-in via `--spec`)
- [ ] Add test file discovery patterns (language-agnostic)
- [ ] Add project command detection logic
- [ ] Add PR title generation logic (comprehensive approach)
- [ ] Add section generation logic (Context, Implementation, Testing, Verify)
- [ ] Add parameter handling instructions

### Phase 3: Edge Cases & Error Handling
- [ ] Add edge case handling (no changes, invalid branch, detached HEAD, invalid spec path, etc.)
- [ ] Add error message templates
- [ ] Add best-effort spec extraction (for incomplete specs)

### Phase 4: Testing
- [ ] Create `tests/test_pr_template.py` for template validation
- [ ] Test template structure:
  - [ ] Verify YAML frontmatter exists with `description` field
  - [ ] Verify `allowed-tools` includes necessary git commands
  - [ ] Verify all required sections present (Language Preference, Git Context, Platform Detection, etc.)
- [ ] Test parameter documentation:
  - [ ] Verify `--target-branch` default and usage documented
  - [ ] Verify `--output` parameter documented
  - [ ] Verify `--sections` values documented
  - [ ] Verify `--spec` opt-in behavior documented
- [ ] Test template installation via `codexspec init`:
  - [ ] Verify template copied to `.claude/commands/codexspec.pr.md`
  - [ ] Verify template content matches source
- [ ] Manual testing with various git scenarios:
  - [ ] GitHub repository (github.com URL)
  - [ ] GitLab repository (gitlab.com URL)
  - [ ] No remote configured
  - [ ] With `--spec` parameter
  - [ ] Without `--spec` parameter (default)

### Phase 5: Documentation
- [ ] Update CLAUDE.md with new command description
- [ ] Update README.md with command usage
- [ ] Add example outputs to template

## 10. Technical Decisions

### Decision 1: Template vs Python Implementation
- **Choice**: Implement as Markdown template, not Python code
- **Rationale**:
  - Consistent with existing `/codexspec.commit` command
  - No new Python dependencies
  - Easier to maintain and customize
  - Claude Code handles all execution logic
- **Alternatives Considered**:
  - Python module with git parsing - rejected for complexity
  - Hybrid approach - rejected for inconsistency
- **Trade-offs**: Limited to what Claude can do with shell commands; no direct API integration

### Decision 2: Language Configuration Priority
- **Choice**: Use `language.commit` > `language.output` > English
- **Rationale**: Consistent with `/codexspec.commit` command; PR descriptions are related to commit messages
- **Alternatives Considered**:
  - New `language.pr` setting - rejected to avoid config bloat
  - Only `language.output` - rejected as PR text is more like commit messages
- **Trade-offs**: None - follows established pattern

### Decision 3: Platform Detection via Remote URL
- **Choice**: Parse `git remote get-url origin` for platform detection
- **Rationale**: Simple, reliable, no additional dependencies
- **Alternatives Considered**:
  - Ask user to specify - rejected for poor UX
  - Check for `.github` or `.gitlab` directories - rejected as unreliable
- **Trade-offs**: May not detect self-hosted GitLab with custom domains

### Decision 4: Spec Integration (Opt-in) ⚠️ UPDATED
- **Choice**: Default to NO spec integration; use `--spec` parameter for opt-in
- **Rationale**:
  - Users often make small changes without following SDD workflow
  - Avoids incorrect references to unrelated specs
  - `--spec` parameter provides explicit control when SDD integration is desired
- **Alternatives Considered**:
  - Auto-detect spec by branch name - rejected for complexity
  - Use most recently modified spec - rejected for potential mismatch
  - Prompt user to select - rejected for interrupting workflow
- **Trade-offs**: Requires explicit `--spec` for SDD integration; no automatic spec detection

### Decision 5: Spec Content Extraction ⚠️ NEW
- **Choice**: Best-effort extraction from available content
- **Rationale**: Avoids blocking workflow due to spec format issues
- **Alternatives Considered**:
  - Require complete spec structure - rejected for being too strict
  - Warn on incomplete specs - rejected for adding noise
- **Trade-offs**: May generate partial Context section if spec is incomplete

### Decision 6: Test File Discovery ⚠️ NEW
- **Choice**: Language-agnostic heuristics (directory + file name patterns)
- **Rationale**: Covers diverse project structures across languages without requiring language detection
- **Patterns**: `tests/`, `test/`, `__tests__/`, `*_test.py`, `test_*.py`, `*.test.js`, `*.spec.ts`, etc.
- **Trade-offs**: May include non-test files that match patterns

### Decision 7: PR Title Generation ⚠️ NEW
- **Choice**: Comprehensive approach (git diff analysis + branch name + commit messages)
- **Rationale**:
  - First commit may only represent partial work
  - Branch names may not follow conventions
  - Actual code changes provide the most accurate representation
- **Alternatives Considered**:
  - Branch name only - rejected for convention dependency
  - First commit only - rejected for partial representation
- **Trade-offs**: Slightly more complex analysis required

### Decision 8: Project Command Detection ⚠️ NEW
- **Choice**: Detect project files to infer test commands
- **Detection Rules**:
  - `pyproject.toml` + `pytest.ini`/`tests/` → `pytest`
  - `package.json` + `jest.config.js` → `npm test`
  - `Cargo.toml` → `cargo test`
  - `go.mod` → `go test`
- **Rationale**: Generates more actionable verification steps
- **Trade-offs**: May not detect all project types; fallback to generic steps

### Decision 9: Output Mode
- **Choice**: Terminal output by default, optional file output
- **Rationale**: Matches user's expected workflow (copy-paste to GitHub/GitLab)
- **Alternatives Considered**:
  - File output only - rejected for extra step
  - Always both - rejected for clutter
- **Trade-offs**: None - provides flexibility

## 11. File Checklist

### Files to Create
| File | Purpose |
|------|---------|
| `templates/commands/pr.md` | PR description generator template |

### Files to Modify
| File | Change |
|------|--------|
| `src/codexspec/__init__.py` | No changes needed (template auto-copied by `init`) |
| `CLAUDE.md` | Add `/codexspec.pr` to command table |
| `README.md` | Add command to available commands list |

### Files to Create for Testing
| File | Purpose |
|------|---------|
| `tests/test_pr_template.py` | Validate template structure and installation |

## 12. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Claude misinterprets git diff | Low | Medium | Provide clear instructions and examples in template |
| Platform detection fails for custom domains | Medium | Low | Default to GitHub terminology with warning |
| Incomplete spec extraction produces weak Context | Low | Low | Best-effort approach; user can edit output |
| Large diffs timeout | Low | Low | NFR specifies 100 commit limit; Claude handles gracefully |
| Project command detection misses edge case | Medium | Low | Fallback to generic steps |

## 13. Success Criteria

- [ ] Template created at `templates/commands/pr.md`
- [ ] Template copied to `.claude/commands/codexspec.pr.md` on `codexspec init`
- [ ] Generates PR description with 4 sections when `--spec` is used
- [ ] Generates PR description with 3 sections (no Context) by default
- [ ] Correctly detects GitHub vs GitLab from remote URL
- [ ] Respects language configuration (commit > output > en)
- [ ] Handles all edge cases defined in spec (EC-001 to EC-006, EC-004b, EC-004c)
- [ ] Detects project-specific test commands for "How to Verify" section
- [ ] Tests pass for template validation

## 14. Changes from Clarification Session

The following changes were made during the clarification session on 2025-02-25:

| Topic | Original Design | Updated Design |
|-------|----------------|----------------|
| Spec Integration | Auto-detect (use most recent spec.md) | Opt-in via `--spec` parameter |
| Spec Content Extraction | Not specified | Best-effort extraction, skip missing sections |
| Test File Discovery | Not specified | Language-agnostic patterns (directory + file name) |
| PR Title Generation | Branch name or commits | Comprehensive (diff + branch + commits) |
| Project Commands | Not specified | Detect from project files (pyproject.toml, etc.) |
| Parameter | `--no-spec` (skip spec) | `--spec` (enable spec, opt-in) |
