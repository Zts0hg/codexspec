# Confirmed Requirements: CodexSpec example projects

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-1017-23338j`
**Status**: Confirmed
**Last Confirmed**: 2026-10-17

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Build exactly two example projects

- **Status**: confirmed
- **Statement**: Create exactly two CodexSpec example software projects. There is no third example project in this feature's target.
- **Rationale**: The examples should show how CodexSpec supports development of complete software across multiple feature iterations.
- **User Evidence**: “调整NEED-001为明确2个，不用留一个‘第三个项目’的需求缺口。”
- **Confirmed At**: 2026-10-17

### NEED-002: Preserve the real development history of both projects

- **Status**: confirmed
- **Statement**: Each example project must retain the actual CodexSpec development records created while its software is built and iterated, so readers can follow the real sequence of work on individual changes.
- **User Evidence**: “每个项目保留真实的逐功能开发记录。”
- **Confirmed At**: 2026-10-17

### NEED-003: Publish both applications and link them from CodexSpec

- **Status**: confirmed
- **Statement**: Publish the source code and development records of both example applications as public open-source projects on GitHub. The CodexSpec main repository must provide entry links to them.
- **User Evidence**: The user requested “将软件代码作为开源项目代码上传到github” and agreed that CodexSpec's main repository should link to the two independent public repositories.
- **Confirmed At**: 2026-10-17

### NEED-004: Provide a chronological guide in each example repository

- **Status**: confirmed
- **Statement**: Each example repository must include a guide ordered by the actual development sequence. For every independently scoped change, the guide must link to its CodexSpec feature directory and corresponding code commit or milestone, and explain how to run or verify that stage. The guide must let a reader follow how the application evolved from earlier working versions to its completed state.
- **User Evidence**: The user replied “确认” to the proposal for a guide in each repository linking each change's requirements directory, code commit, and run or verification instructions.
- **Confirmed At**: 2026-10-17

### NEED-005: Deliver two complete, usable applications

- **Status**: confirmed
- **Statement**: Develop each application through successive, independently recorded changes until it is a mature, usable software product within a coherent product scope. The project lead must determine and verify the necessary functionality and quality criteria; the examples must not stop at a partial prototype merely because the educational workflow has been demonstrated.
- **User Evidence**: The initial request called for “一步一步开发和迭代各个功能得到一个成熟的系统/软件”; the user rejected the interpretation that work might stop at a half-finished product.
- **Confirmed At**: 2026-10-17

### NEED-006: Delegate end-to-end product leadership to the external project lead

- **Status**: confirmed
- **Statement**: The assistant leading this CodexSpec initiative has full authority and responsibility for requirements research, analysis, product decisions, feature sequencing, acceptance criteria, and engineering oversight for both applications from start to finish. It must make those product decisions itself and direct repository-local coding agents to implement them with CodexSpec skills. The user does not participate in feature-level product decisions.
- **User Evidence**: “我全权授权你作为这两款软件的负责人和工程师，关于这两款软件的功能需求从头到尾我都不进行决策。”
- **Confirmed At**: 2026-10-17

## Constraints

### CON-001: Use a separate requirements record and feature directory for each change

- **Status**: confirmed
- **Statement**: In each example project, every independently scoped feature, bug fix, and refactor must be treated as a separate requirement and have its own `.codexspec/specs/<feature-id>-<feature-name>/` directory. Do not combine multiple independent changes into one directory merely to shorten the example history.
- **User Evidence**: “一个功能（feature/bugfix/refactor）应该作为一个单独的需求，对应到开发记录就是一个单独的 .codexspec/specs/<feature 目录>。”
- **Existing CodexSpec Convention**: [Blueprint/auto-dev requirements](../2026-0829-2159yg-blueprint-auto-dev/requirements.md), CON-006, confirms the complete `<feature-id>-<feature-name>` directory form.
- **Confirmed At**: 2026-10-17

### CON-002: Keep the project lead and repository-local coding agent as separate roles

- **Status**: confirmed
- **Statement**: Each application must be developed in its own repository through a coding agent using CodexSpec skills. The project lead operates outside that repository-local agent, supplies product requirements and engineering decisions, reviews its work, and accepts or requests corrections. Communication with the coding agent must be based on those roles and task content; the agent must not need to know whether the external lead is a human. A tmux session is an allowed interaction channel, not a required product feature.
- **User Evidence**: “两款软件是分别在独立的代码仓库中通过 coding agent + codexspec skills 进行开发的”; “你是那个‘agent之外的负责人’”; “代码仓库下运行的coding agent 对你是否是真实人类不需要有感知”; “可以是启动一个 tmux 然后通过跟tmux中的 coding agent交互”.
- **Confirmed At**: 2026-10-17

### CON-003: The external project lead confirms each repository's requirements summaries

- **Status**: confirmed
- **Statement**: When a repository-local coding agent runs `codexspec:specify` for an individual change, the external project lead must review the final requirements summary and provide the explicit confirmation required by that workflow. The original user does not participate in those project-level confirmations or feature decisions.
- **User Evidence**: “codexspec:specify 要求在结束发现阶段前核对一次最终摘要。这也是完全由你来进行，而不需要我来参与。”
- **Confirmed At**: 2026-10-17

## Decisions

### DEC-001: Use Todo List and personal bookkeeping as the two software products

- **Status**: confirmed
- **Decision**: The two example projects will develop a Todo List application and a personal bookkeeping application.
- **Reason**: Both have established product patterns and enough functionality to demonstrate successive feature development; the user proposed them as the first candidates and confirmed the selection.
- **User Evidence**: The user proposed “todo list软件” and “记账软件”, then replied “确认” when asked whether these were the definitive two products.
- **Confirmed At**: 2026-10-17

### DEC-002: Use one independent GitHub repository per application

- **Status**: confirmed
- **Decision**: Keep the Todo List and personal bookkeeping applications in separate public GitHub repositories, each with its own source code, commits, and `.codexspec/specs/` history.
- **Reason**: Each project's development sequence remains independently navigable and reproducible.
- **User Evidence**: The user replied “同意” to the proposal for two independent public repositories and entry links from the CodexSpec main repository.
- **Confirmed At**: 2026-10-17

### DEC-003: Give the two projects different CodexSpec language settings

- **Status**: confirmed
- **Decision**: Initialize the Todo List project with `language.output: en` and the personal bookkeeping project with `language.output: zh-CN`. Leave `language.interaction`, `language.document`, and `language.commit` unset unless a later independently recorded requirement changes them, so each follows its project's `language.output` fallback. Keep `language.templates: en` for command-template compatibility. Consequently, CodexSpec conversations, generated development records, and commit messages use English in Todo List and Simplified Chinese in bookkeeping.
- **Reason**: The two examples should demonstrate actual CodexSpec development in different language settings, including the language of their authentic records.
- **User Evidence**: “todo list软件的项目使用英文作为 codexspec 的语言设置项，记账软件使用简体中文作为语言设置项。” The user explicitly confirmed the proposed base-language and fallback mapping, with templates remaining in English.
- **Confirmed At**: 2026-10-17

## Open Questions

No open product question blocks specification generation. The project lead owns the detailed feature roadmaps, quality criteria, technical choices, and repository publication decisions under NEED-005 and NEED-006. The authenticated GitHub account and CodexSpec origin currently identify the same account; confirm the available destination at publication time.

## Confirmation Log

### 2026-10-17 — Example project count

- **Summary Presented**: Proposed two to three public example projects, with Todo List and personal bookkeeping as the first two and a possible third project deferred.
- **User Confirmation**: Explicitly corrected the target to exactly two projects and rejected a third-project gap.
- **Entries Confirmed**: NEED-001.

### 2026-10-17 — Development record granularity

- **Summary Presented**: Asked whether each project should retain its complete, real, feature-by-feature CodexSpec development history or only selected steps and final code.
- **User Confirmation**: Chose real records for each project and explicitly required a separate requirement and `.codexspec/specs/<feature>/` directory for every feature, bug fix, or refactor.
- **Entries Confirmed**: NEED-002, CON-001.

### 2026-10-17 — Software product selection

- **Summary Presented**: Asked whether the two example projects should definitively be Todo List and personal bookkeeping.
- **User Confirmation**: “确认”.
- **Entries Confirmed**: DEC-001.

### 2026-10-17 — GitHub repository structure

- **Summary Presented**: Proposed one independent public GitHub repository for each application, with source and CodexSpec history together, plus links from the CodexSpec main repository.
- **User Confirmation**: “同意”.
- **Entries Confirmed**: NEED-003, DEC-002.

### 2026-10-17 — Reader guide

- **Summary Presented**: Proposed a required chronological guide in each example repository, linking each change's feature directory, code commit, and run or verification method.
- **User Confirmation**: “确认”.
- **Entries Confirmed**: NEED-004.

### 2026-10-17 — Product leadership and coding-agent boundary

- **Summary Presented**: Asked whether to confirm the complete product scope together and then let the lead develop individual changes, or to seek the user's approval for every change.
- **User Confirmation**: Corrected the proposal: the lead has full authority over both applications' requirements and decisions from start to finish; repository-local coding agents implement through CodexSpec skills under the external lead's direction, without depending on the lead's human identity.
- **Entries Confirmed**: NEED-005, NEED-006, CON-002.

### 2026-10-17 — Final discovery confirmation

- **Summary Presented**: Exactly two mature, usable applications (Todo List and personal bookkeeping), each in its own public GitHub repository; genuine feature-by-feature CodexSpec records and code history; a chronological guide per repository and links from CodexSpec; full product authority held by the external project lead, with repository-local coding agents using CodexSpec skills and identity-independent engineering communication.
- **User Confirmation**: “对……这也是完全由你来进行，而不需要我来参与。确认。” The user additionally assigned every repository-local `codexspec:specify` final-summary confirmation to the external project lead.
- **Entries Confirmed**: NEED-001 through NEED-006, CON-001 through CON-003, DEC-001 and DEC-002.
- **Open IDs**: None blocking specification generation.

### 2026-10-17 — Application-project language settings

- **Summary Presented**: Proposed `codexspec init --lang en` for Todo List and `codexspec init --lang zh-CN` for bookkeeping, using each base language for interaction, documents, and commit messages through existing fallback rules while keeping command templates in English.
- **User Confirmation**: “确认”.
- **Entries Confirmed**: DEC-003.
