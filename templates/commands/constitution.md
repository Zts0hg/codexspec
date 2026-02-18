---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
argument-hint: |
  [quick|deep | project principles] (optional)

  This command creates/updates the project constitution at .codexspec/memory/constitution.md.

  Three ways to use:
  1. No arguments → Interactive mode: choose exploration depth (quick/deep)
  2. quick → Lightweight exploration: config files + README + core entry points (~5-10 files)
  3. deep → Full exploration: all of above + source code analysis + architecture patterns
  4. <description> → Skip exploration, use your principles directly

  Examples:
    /codexspec.constitution
    /codexspec.constitution quick
    /codexspec.constitution deep
    /codexspec.constitution Python FastAPI backend with pytest, focus on type safety
handoffs:
  - agent: codexspec.specify
    step: Create a feature specification based on the updated constitution
---

## Language Preference

**IMPORTANT**: Before proceeding, read the project's language configuration from `.codexspec/config.yml`.
- If `language.output` is set to a language other than "en", respond and generate all content in that language
- If not configured or set to "en", use English as default
- Technical terms (e.g., API, JWT, OAuth) may remain in English when appropriate

## User Input

```text
$ARGUMENTS
```

## Input Mode Detection

Parse `$ARGUMENTS` to determine execution mode:

**Mode A: No Arguments**
→ Present exploration options and let user choose

**Mode B: Exploration Keyword (`quick` or `deep`)**
→ Execute the corresponding exploration mode

**Mode C: Project Principles Description**
→ Use provided principles directly, skip exploration

---

### Mode A: No Arguments - Present Options

Output the following and wait for user response:

> 📋 **Constitution 创建向导**
>
> 检测到无参数输入。我将探索项目来生成 constitution，请选择探索深度：
>
> | 模式 | 探索范围 | 适用场景 |
> |------|----------|----------|
> | `quick` | 项目结构、配置文件、README/CLAUDE.md、核心入口代码（约 5-10 个关键文件） | 新初始化项目、快速创建基础 constitution |
> | `deep` | 上述内容 + 完整源代码分析、代码风格、架构模式、测试策略（可能分析数十到上百个文件） | 成熟项目、需要全面捕捉项目现状 |
>
> 请回复 `quick` 或 `deep`，或直接描述你的项目原则（例如："Python Flask 后端项目，注重测试覆盖率"）。

After user responds, proceed to Mode B or Mode C accordingly.

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

1. **User input** (from $ARGUMENTS above) - use if provided
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
