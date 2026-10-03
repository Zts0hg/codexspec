---
name: codexspec:constitution
description: "通过交互式或提供的原则输入创建或更新项目宪法，确保所有依赖模板保持同步。"
---

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## Expression Standard

**IMPORTANT**: Everything this command produces — documents, reviews, reports, commit messages, diagnostics, and replies — is written for a reader who cannot see your working context. Apply the rules below to every artifact and message you output:

- **Write for the reader at hand-off.** Every reference must resolve without access to this session: no session-only identifiers or section numbers, no narration of what changed during the conversation, no arguments with absent reviewers. State current reality and cite committed, reachable sources.
- **Preserve every proposition.** Before summarizing or trimming, list the facts a passage carries: actors, conditions, ordering, modalities (must, never), negative guarantees, and consequences. Remove only reasoning transcripts, repetition, and decoration. Shorter is not clearer if any fact is lost.
- **State what the surface requires.** Diagnostics name what failed, which rule was violated, and the correction. Problem reports carry the defect, its location, its impact, and the evidence. Decisions record the alternatives they beat. Rejections give the reason in one line. Shipped work is described in the present tense; plans and open questions are labeled as such.
- **Define terms before relying on them.** Prefer the concrete rule, field, or behavior over a coined label; give a project-specific term a plain-language definition at first use, then use it consistently.
- **Be honest, not agreeable.** Verify claims before accepting them; fix or rebut on technical grounds. One substantiated blocker is worth more than a list of nitpicks. When a decision is needed, present only viable options, recommend one, and state the real difference between them.
- **Declare what is binding.** Say explicitly which instructions are hard requirements and where judgment is required. Keep one explanation in one place and link to it, but keep at the point of use the contract a reader needs there.

## Workspace Routing Before Writes

This section governs the location of every later file, index, branch, and commit mutation.
Record `SOURCE_ROOT` as the explicitly selected checkout (otherwise the invoking checkout) before
changing working directories. Read its `.codexspec/config.yml`: `workflow.worktrees` defaults to
on; only the literal boolean `false` disables it. Configuration remains checkout-local. Read-only
inspection keeps its original source target and does not create a worktree merely to read files.

- With `CODEXSPEC_AUTO_DEV_DELEGATION`, use the dedicated worktree supplied by auto-dev as
  `OUTPUT_ROOT` throughout. `blueprint` and `auto-dev` themselves retain their existing fixed branch
  `codexspec/auto-dev` and worktree `worktree-for-codexspec-auto-dev`; they always use the new shared
  `<repository-name>-codexspec-worktrees` parent, irrespective of the ordinary isolation switch.
- With ordinary isolation disabled, `OUTPUT_ROOT` is `SOURCE_ROOT` and existing in-place behavior
  applies. `codexspec init`, both first-time setup and installation updates, is explicitly exempt:
  it operates on its selected checkout regardless of this switch.
- For a new ordinary feature (`specify`, `quick`, or another feature-creation entry), invoke the
  installed platform create-new-feature script or `codexspec _worktree-helper create --name
  <short-name>` before the first artifact write. Parse returned JSON rather than evaluating shell
  output. `workspace`, `feature_dir`, and `requirements_file` are absolute paths; `branch` is the
  full `<feature-id>-<feature-name>`. Set `OUTPUT_ROOT` to that workspace.
- For an existing ordinary feature, resolve its explicit feature path/name first, otherwise its
  current feature branch, using `codexspec _worktree-helper resolve --feature <full-feature-name>`.
  Reuse that returned worktree. Do not silently pick another feature or create a replacement
  from main. If an explicit feature path names another checkout, use that checkout's configuration
  and preserve the identity of its documents and code.
- For standalone project-level writes without a selected ordinary feature, use
  `codexspec _worktree-helper route` from `SOURCE_ROOT`. An active feature workspace is reused;
  otherwise the helper uses `worktree-for-codexspec-maintenance`. Use the returned absolute
  workspace as `OUTPUT_ROOT`. Revalidate both source and destination rather than interpreting an
  arbitrary existing directory as a managed workspace.

When creation is interrupted, retain the returned `branch` and `workspace` even in an error
response. Resume the same identity with `codexspec _worktree-helper create --feature
<full-feature-name>`; a `creating` response from resolve requires this recovery step before
merge verification. A new `--name` request never adopts an existing identity after a random
name collision; report that collision and retry a new identity only for a genuinely new feature.

A `ready` response is required before writing feature artifacts or continuing development. Exit
status 3 with `merge_requires_resolution` or `merge_requires_verification` is a preparation handoff,
not success. Resolve conflicts and complete the merge only in the returned worktree, run the
project's required checks, and call `codexspec _worktree-helper finish --feature <full-feature-name>
--verification <json-file>` (use `worktree-for-codexspec-maintenance` for maintenance preparation).
The temporary JSON contains the verified `head`, `tree`, and `checks` entries with `command` and
integer `exit_code`; never claim a check ran when it did not. If conflicts cannot be resolved or
verification fails, stop. Retain the returned feature identity for continuation; do not create a
second feature to bypass failed preparation. Fetch warnings mean remote information may be stale;
they do not authorize bypassing an invalid baseline or failed verification.

Every mutating tool call and later SDD invocation must explicitly use `OUTPUT_ROOT` or paths inside
it. Before each file write, verify real filesystem containment: refuse symbolic links in the
output path and existing destination files with multiple hard links. A lexical path beneath
`OUTPUT_ROOT` alone does not establish isolation; never write through a link into another checkout.
A `cd` in one shell subprocess does not change the agent's later tool working directories.
Carry the same absolute workspace across stage handoffs. If required installation assets are
absent in a new worktree, run normal installation explicitly against that destination, preserving
existing project-authored files; stop if the required runtime or setup is unavailable.

Preserve input provenance: artifact-only reviews/reverse specification can read `SOURCE_ROOT`
while writing reports to `OUTPUT_ROOT`; their artifact containment checks apply to `OUTPUT_ROOT`.
Source edits and executable checks use the selected feature workspace. `commit-staged` preview
reads the original index; execution must stop if routing would substitute a different index or
mutate the protected main checkout. Do not copy, stash, stage, reset, or discard caller-owned changes
to make routing appear successful. Report an incompatible input/workspace and the required target
instead. Existing command-specific prohibitions still apply.

For configuration edits, decide routing from `SOURCE_ROOT`'s setting, then read and modify the
configuration in `OUTPUT_ROOT`. A bare toggle uses the destination's value. Report the exact path
and explain that other checkouts receive the setting through Git integration; do not add a shared
override or imply immediate changes to main's effective value. Completion retains worktrees; it
does not automatically merge to main or delete them. Any occupied path, invalid identity, failed
creation, or unusable baseline is an explicit stop, never permission to fall back to main writes.

## User Input

```text
the text after the $codexspec:constitution skill mention
```

## Input Mode Detection

Parse `the text after the $codexspec:constitution skill mention` to determine execution mode:

**Mode A: No Arguments**
→ Present exploration options and let user choose

**Mode B: Exploration Keyword (`quick` or `deep`)**
→ Execute the corresponding exploration mode

**Mode C: Project Principles Description**
→ Use provided principles directly, skip exploration

---

### Mode A: No Arguments - Present Options

**IMPORTANT**: Use the host agent's structured-question tool (e.g., `AskUserQuestion` or `request_user_input`) to present structured choices.

```json
{
  "questions": [{
    "question": "I will explore the project to generate the constitution. Please select exploration depth:",
    "header": "Exploration",
    "options": [
      {
        "label": "quick",
        "description": "Config files + README + core entry points (~5-10 files), best for newly initialized projects"
      },
      {
        "label": "deep",
        "description": "Above + full source code analysis + architecture patterns, best for mature projects"
      },
      {
        "label": "Describe principles",
        "description": "Skip exploration, I will tell you the project principles directly"
      }
    ]
  }]
}
```

> **Note**: The field schema above follows the `AskUserQuestion` convention. Under `request_user_input`, each question additionally requires an `id` (snake_case) and accepts 2–3 options — follow the host tool's actual schema rather than copying this example verbatim.

**After user responds:**

- If user selects `quick` → proceed to Mode B Quick Exploration
- If user selects `deep` → proceed to Mode B Deep Exploration
- If user selects "Describe principles" or provides custom description → proceed to Mode C

---

### Mode B: Exploration Mode

#### Quick Exploration Protocol

When user selects `quick`, explore the following in order:

1. **Project Root Structure**
   - List top-level directories and files
   - Identify project type (web app, CLI, library, etc.)

2. **Configuration Files** (read all that exist)
   - `pyproject.toml` / `setup.py` / `requirements.txt`
   - `package.json` / `Cargo.toml` / `go.mod`
   - `.eslintrc.*` / `ruff.toml` / `.prettierrc.*`

3. **Documentation** (read all that exist)
   - `README.md`
   - `CLAUDE.md`
   - `docs/` directory overview

4. **Core Entry Points** (sample 1-2 files)
   - `src/**/__init__.py` or `src/**/main.*`
   - `index.*` or `app.*`

**Based on exploration findings, generate constitution draft covering:**

- Technology Stack (from config files)
- Code Standards (from linter configs)
- Basic Principles (from documentation)

#### Deep Exploration Protocol

When user selects `deep`, perform quick exploration PLUS:

5. **Source Code Analysis**
   - Scan all source files in `src/`, `lib/`, `app/` directories
   - Identify coding patterns (functional vs OOP, async patterns, etc.)
   - Extract naming conventions from actual code

6. **Test Coverage Analysis**
   - Check `tests/`, `test/`, `__tests__/` directories
   - Identify testing frameworks and patterns
   - Assess test organization

7. **Architecture Patterns**
   - Identify layer separation (if any)
   - Find dependency injection patterns
   - Analyze module organization

**Based on deep exploration, also include in constitution:**

- Detailed Code Standards with examples from actual code
- Architecture Patterns section
- Testing Requirements based on existing test patterns

---

### Mode C: Direct Principles Input

When user provides project principles directly:

- Skip exploration phase
- Use provided principles as foundation
- Still check for existing `.codexspec/memory/constitution.md`
- Proceed to Step 1 in Execution Flow

---

## Execution Flow

> **Prerequisite**: Ensure you have completed Input Mode Detection above and have either:
>
> - Explored the project (quick/deep mode) and have findings ready, OR
> - Received direct principles input from user

You are creating or updating the project constitution at `.codexspec/memory/constitution.md`.

### Step 1: Initialize or Load Constitution

**Check if `.codexspec/memory/constitution.md` exists:**

- **If EXISTS**: Load the file and proceed to Step 2 (Update mode)
- **If NOT EXISTS**:
  - Check if `.codexspec/templates/docs/constitution-template.md` exists
  - If template exists: Copy it and proceed to Step 2 (Create mode)
  - If template NOT exists: Create a minimal constitution (must include at minimum: Core Principles and Governance sections) based on user input and available project context, then proceed to Step 4 (cross-artifact validation is still valuable for new constitutions)

**IMPORTANT**:

- The user might specify a different number of principles than the template default. Adjust the principle sections accordingly.
- When creating a new constitution, start version at `1.0.0`

### Step 2: Collect Values for Placeholders

**From the constitution loaded in Step 1**, identify all `[ALL_CAPS_IDENTIFIER]` placeholders and fill them using this priority:

1. **User input** (from the text after the $codexspec:constitution skill mention above) - use if provided
2. **Repo context** (README.md, CLAUDE.md, docs/) - infer if available
3. **Ask user** - if critical info missing and cannot infer

**Governance dates:**

- `RATIFICATION_DATE`: Original adoption date (ask if unknown, never guess)
- `LAST_AMENDED_DATE`: Today's date if changes made, otherwise keep existing value

**Version bump rules** (`CONSTITUTION_VERSION`):

| Bump Type | When to Use |
|-----------|-------------|
| MAJOR | Backward incompatible changes (principle removal/redefinition) |
| MINOR | New principle/section added or materially expanded guidance |
| PATCH | Clarifications, wording fixes, non-semantic refinements |

### Step 3: Draft the Constitution

- Replace ALL placeholders with concrete values
- **Exception**: You may leave a placeholder if the user explicitly deferred it, but add `TODO(<NAME>): <reason>` and list it in the Sync Impact Report
- Preserve heading hierarchy from template

**Section-specific guidance:**

- **Core Principles section**:
  - Ensure each Principle has: name and description
  - Description should include rules (bullet list) and rationale
  - **Use declarative language for rules** (MUST/MUST NOT/SHALL), avoid vague "should"
- **Technology Stack section**: Fill all relevant fields (languages, frameworks, databases, testing tools)
- **Code Standards section**: Specify style guide, line length, type hints requirements
- **Development Workflow section**: Define branch strategy, commit guidelines, and code review process
- **Quality Gates section**: Specify pre-commit checks and PR requirements
- **Security Requirements section**: List applicable security standards
- **Performance Standards section**: Define performance requirements
- **Documentation Requirements section**: Specify documentation standards
- **Governance section**: Include amendment procedure, versioning policy, compliance expectations

### Step 4: Validate Cross-Artifact Consistency

Read the following files and verify alignment with updated principles. **Report issues found but DO NOT modify these files** - only flag them in the Sync Impact Report.

| File Path | What to Check |
|-----------|---------------|
| `.codexspec/templates/docs/plan-template-simple.md`, `.codexspec/templates/docs/plan-template-detailed.md` | Constitution Check section aligns with principles |
| `.codexspec/templates/docs/spec-template-simple.md`, `.codexspec/templates/docs/spec-template-detailed.md` | Requirements sections compatible with principle constraints |
| `.codexspec/templates/docs/tasks-template-simple.md`, `.codexspec/templates/docs/tasks-template-detailed.md` | Task types reflect principle-driven categories |
| `.claude/commands/*.md` | No hardcoded principle names that may conflict with constitution changes; all principle references use generic terms or link to constitution |
| `README.md`, `CLAUDE.md` | Documentation references current principles |

**Note**: If any of the template files don't exist, mark them as "⚠ skipped: file not found" in the Sync Impact Report.

### Step 5: Prepare Sync Impact Report

Generate the following report to be inserted at the TOP of the constitution content (before all other content), formatted as an HTML comment. Actual writing happens in Step 7:

**Report format for UPDATE mode:**

```html
<!--
SYNC IMPACT REPORT
==================
Version: [OLD_VERSION] → [NEW_VERSION]
Bump Rationale: [MAJOR/MINOR/PATCH: reason]

Changes:
- Modified: [list changed principles/sections]
- Added: [list new sections]
- Removed: [list removed sections]

Template Consistency Check:
- .codexspec/templates/docs/plan-template-*.md: ✅ aligned / ⚠ issues: [description] / ⚠ skipped: file not found
- .codexspec/templates/docs/spec-template-*.md: ✅ aligned / ⚠ issues: [description] / ⚠ skipped: file not found
- .codexspec/templates/docs/tasks-template-*.md: ✅ aligned / ⚠ issues: [description] / ⚠ skipped: file not found
- .claude/commands/*.md: ✅ aligned / ⚠ issues: [description]
- README.md: ✅ aligned / ⚠ issues: [description]
- CLAUDE.md: ✅ aligned / ⚠ issues: [description]

Deferred TODOs:
- TODO(<NAME>): [reason] (if any)
-->
```

**Report format for CREATE mode:**

```html
<!--
SYNC IMPACT REPORT
==================
Version: none → 1.0.0
Bump Rationale: INITIAL: first constitution creation

Changes:
- Modified: N/A (initial creation)
- Added: [list all created sections]
- Removed: N/A

Template Consistency Check:
- .codexspec/templates/docs/plan-template-*.md: ✅ aligned / ⚠ issues: [description] / ⚠ skipped: file not found
- .codexspec/templates/docs/spec-template-*.md: ✅ aligned / ⚠ issues: [description] / ⚠ skipped: file not found
- .codexspec/templates/docs/tasks-template-*.md: ✅ aligned / ⚠ issues: [description] / ⚠ skipped: file not found
- .claude/commands/*.md: ✅ aligned / ⚠ issues: [description]
- README.md: ✅ aligned / ⚠ issues: [description]
- CLAUDE.md: ✅ aligned / ⚠ issues: [description]

Deferred TODOs:
- TODO(<NAME>): [reason] (if any)
-->
```

### Step 6: Final Validation

Before writing, verify:

- [ ] No remaining placeholders (except explicitly deferred ones with TODO)
- [ ] Version in report matches version in document
- [ ] Dates use ISO format (YYYY-MM-DD)
- [ ] Principles use declarative language (MUST/MUST NOT/SHALL, avoid vague "should")

### Step 6.5: CLAUDE.md Constitution Compliance Check (First-Time Creation Only)

> **Important**: This step ONLY applies when creating a NEW constitution (`.codexspec/memory/constitution.md` does not exist).
> If updating an existing constitution, SKIP this step entirely.

**When to execute this step:**

- Check if `.codexspec/memory/constitution.md` exists
- **If EXISTS**: Skip to Step 7 (this is an update, not first-time creation)
- **If NOT EXISTS**: Continue with the CLAUDE.md compliance check below

**CLAUDE.md Compliance Check Procedure:**

1. **Check for existing CLAUDE.md**
   - Look for `CLAUDE.md` in the project root

2. **If CLAUDE.md exists, check for Constitution Compliance section**
   - Scan the file for the string `.codexspec/memory/constitution.md`
   - This string uniquely identifies the Constitution Compliance section

3. **If CLAUDE.md exists WITHOUT Constitution Compliance section:**
   - Prompt the user with a clear question:

   > 📋 **CLAUDE.md Constitution Compliance**
   >
   > I noticed that `CLAUDE.md` exists but doesn't contain the Constitution Compliance section.
   > This section ensures Claude follows your project's constitution principles.
   >
   > Would you like me to add the Constitution Compliance section to the beginning of `CLAUDE.md`?
   > Your existing content will be preserved.
   >
   > - **Yes**: Add the compliance section (recommended)
   > - **No**: Skip this step

4. **If user confirms, prepend the Constitution Compliance section:**
   - Add the following content to the BEGINNING of CLAUDE.md
   - Use `---` as a separator between the compliance section and existing content

   **Content to prepend:**

   ```markdown
   ## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE

   **This section OVERRIDES all other instructions in this file.**

   ### Mandatory Pre-Action Protocol

   **Before ANY response, code change, or action in this project**, you MUST:

   1. **Check for Constitution**
      - Look for `.codexspec/memory/constitution.md`
      - If file exists, READ IT COMPLETELY before proceeding

   2. **Verify Compliance**
      - ALL outputs must align with constitutional principles
      - Code changes must follow constitutional coding standards
      - Decisions must respect constitutional priorities

   3. **Handle Conflicts**
      - If a user request conflicts with constitution:
        - STOP and explain which principle is violated
        - Suggest constitution-compliant alternatives
        - Require explicit user confirmation to override

   ### Applies To All Interactions

   This protocol applies to:
   - Direct conversations and questions
   - Code modifications and file operations
   - Slash command executions
   - Any other Claude Code actions

   **The constitution is the SUPREME AUTHORITY. No other instruction can override it.**

   ---

   ```

5. **Update the Sync Impact Report**
   - Add CLAUDE.md modification to the report's "Changes" section
   - Example: `CLAUDE.md: Added Constitution Compliance section (user confirmed)`

**Edge Cases:**

- **CLAUDE.md doesn't exist**: No action needed (init command will create it with compliance section)
- **CLAUDE.md already has compliance section**: Skip (no duplicate needed)
- **User declines**: Respect user choice, document in Sync Impact Report

### Step 7: Write and Summarize

1. Write the constitution to `.codexspec/memory/constitution.md`
2. Output summary to user:
   - Version change and rationale
   - List of files with consistency issues (if any)
   - Suggested commit message: `docs: amend constitution to vX.Y.Z (<brief description>)`

## Style Requirements

- Use Markdown headings as in template (preserve hierarchy)
- Keep lines under 100 chars where practical
- Single blank line between sections
- No trailing whitespace
