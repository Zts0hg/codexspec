# Compact Command Description Proposals

**Status**: Approved by the user on 2026-10-17.

The user approved all 28 bilingual proposals: "确认，按照建议版本更新并同步到各个语言". Apply English and Chinese verbatim; translate their meaning naturally into the other existing languages.

Baseline: `7d863964eddd4b34abf66cef3971959c7ff8bc0a` (0.7.25). Original English comes from current authored frontmatter; original Chinese comes from the zh-CN catalog. Proposals summarize the command bodies examined during this feature.

Keep the core purpose and result first. Use one compact sentence where practical; retain only modes and boundaries that materially help users choose a command. Inputs, preconditions and procedures need not be enumerated in every description.

## 1. constitution

| Language | Original | Proposed |
| --- | --- | --- |
| English | Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync. | Define or update project principles in constitution.md and check related documents for consistency. |
| 简体中文 | 通过交互式或提供的原则输入创建或更新项目宪法，确保所有依赖模板保持同步。 | 制定或更新项目开发原则，写入 constitution.md 并检查相关文档的一致性。 |

## 2. specify

| Language | Original | Proposed |
| --- | --- | --- |
| English | Discuss, confirm, and persist the authoritative requirements record | Clarify a feature’s goals, scope and constraints, then save confirmed requirements to requirements.md. |
| 简体中文 | 讨论、确认并固化权威的需求记录 | 澄清功能目标、范围和约束，将确认的需求整理为 requirements.md。 |

## 3. blueprint

| Language | Original | Proposed |
| --- | --- | --- |
| English | Discuss and maintain confirmed requirements in the shared product blueprint | Plan multiple features in a shared blueprint, recording confirmed requirements and organizing pending work for auto-dev. |
| 简体中文 | 讨论并维护共享产品蓝图中的已确认需求 | 规划多个功能，将确认的需求写入共享蓝图，并管理供 auto-dev 执行的待开发内容和顺序。 |

## 4. generate-spec

| Language | Original | Proposed |
| --- | --- | --- |
| English | Compile confirmed requirements into a traceable spec.md | Turn confirmed requirements into spec.md with feature behavior, error handling and acceptance criteria. |
| 简体中文 | 将已确认的需求编写为可追溯的 spec.md | 将已确认需求编写为 spec.md，明确功能行为、异常处理和验收标准。 |

## 5. spec-to-design

| Language | Original | Proposed |
| --- | --- | --- |
| English | Convert a confirmed specification into a traceable design document | Create design.md from spec.md to define components, interfaces and key technical decisions. |
| 简体中文 | 将已确认的规格转换为可追溯的设计文档 | 根据 spec.md 编写 design.md，定义组件、接口及关键技术决策。 |

## 6. design-to-plan

| Language | Original | Proposed |
| --- | --- | --- |
| English | Convert a confirmed design into a traceable implementation plan | Turn design.md into plan.md with implementation phases, execution order and verification steps. |
| 简体中文 | 将已确认的设计转换为可追溯的实现计划 | 将 design.md 转化为 plan.md，安排实现阶段、执行顺序和验证步骤。 |

## 7. plan-to-tasks

| Language | Original | Proposed |
| --- | --- | --- |
| English | Expand an approved plan into traceable, executable tasks | Break plan.md into tasks.md with concrete work, dependencies and verification, including scenarios for testable tasks. |
| 简体中文 | 将已批准的计划展开为可追溯、可执行的任务 | 将 plan.md 拆分为 tasks.md，明确具体工作、依赖和验证方法，并列出可测试任务的测试场景。 |

## 8. review-spec

| Language | Original | Proposed |
| --- | --- | --- |
| English | Review spec fidelity, internal quality, and planning readiness | Review spec.md for requirement coverage and verifiable acceptance criteria, judging readiness for design. |
| 简体中文 | 审查规格的忠实度、内部质量与计划就绪度 | 审查 spec.md 的需求覆盖和验收标准，判断是否可进入设计阶段。 |

## 9. review-design

| Language | Original | Proposed |
| --- | --- | --- |
| English | Review design fidelity, feasibility, and planning readiness | Review design.md for requirement coverage and technical feasibility, judging readiness for implementation planning. |
| 简体中文 | 审查设计的忠实度、可行性与规划就绪度 | 审查 design.md 的需求覆盖与技术可行性，判断是否可制定实现计划。 |

## 10. review-plan

| Language | Original | Proposed |
| --- | --- | --- |
| English | Review plan fidelity, feasibility, and implementation readiness | Review plan.md for implementation steps, ordering and requirement coverage, judging readiness for task breakdown. |
| 简体中文 | 审查计划的忠实度、可行性与实现就绪度 | 审查 plan.md 的实现步骤、顺序和需求覆盖，判断是否可拆分任务。 |

## 11. review-tasks

| Language | Original | Proposed |
| --- | --- | --- |
| English | Review task fidelity, executability, dependencies, and verification | Review tasks.md for coverage, dependencies and verification, judging whether implementation can begin. |
| 简体中文 | 审查任务的忠实度、可执行性、依赖关系与验证 | 审查 tasks.md 的任务覆盖、依赖和验证方法，判断是否可开始实现。 |

## 12. implement-tasks

| Language | Original | Proposed |
| --- | --- | --- |
| English | Execute implementation tasks with conditional TDD workflow (TDD for code, direct implementation for docs/config) | Implement tasks.md, run tests and independent review, and repair verified issues. |
| 简体中文 | 执行实现任务，支持条件 TDD 工作流（代码使用 TDD，文档/配置直接实现） | 按 tasks.md 实现功能，执行测试与独立审查，并修复经核实的问题。 |

## 13. auto-dev

| Language | Original | Proposed |
| --- | --- | --- |
| English | Autonomously develop every pending requirement in the shared blueprint | Develop confirmed blueprint requirements in order, from specification to verified implementation and commits. |
| 简体中文 | 自主开发共享蓝图中的每个待定需求 | 按蓝图顺序自动开发已确认需求，完成从规格到实现、验证和提交的流程。 |

## 14. clarify

| Language | Original | Proposed |
| --- | --- | --- |
| English | Resolve requirement ambiguities and synchronize requirements.md with spec.md | Resolve gaps, ambiguity and contradictions through focused questions, then synchronize confirmed decisions into requirements.md and spec.md. |
| 简体中文 | 解决需求歧义，并将 requirements.md 与 spec.md 同步 | 通过问答澄清遗漏、歧义和矛盾，将确认结果同步到 requirements.md 和 spec.md。 |

## 15. analyze

| Language | Original | Proposed |
| --- | --- | --- |
| English | Analyze end-to-end traceability and consistency across SDD artifacts | Check consistency from requirements through tasks and automatically fix downstream issues supported by confirmed requirements. |
| 简体中文 | 分析 SDD 工件间的端到端可追溯性与一致性 | 核对需求到任务的文档一致性，自动修复可由已确认需求确定的下游问题。 |

## 16. checklist

| Language | Original | Proposed |
| --- | --- | --- |
| English | Generate a custom quality checklist for validating requirements completeness, clarity, and consistency | Create a checklist for requirement completeness, clarity and scenario coverage, rather than testing code. |
| 简体中文 | 生成自定义质量检查清单，用于验证需求完整性、清晰性和一致性 | 生成需求质量检查清单，检查完整性、清晰度与场景覆盖，而非测试代码。 |

## 17. tasks-to-issues

| Language | Original | Proposed |
| --- | --- | --- |
| English | Convert existing tasks into actionable GitHub issues for the feature | Create GitHub issues from tasks.md, including relevant files, dependencies and available acceptance criteria. |
| 简体中文 | 将现有任务转换为该功能的可操作 GitHub Issues | 将 tasks.md 中的任务创建为 GitHub Issue，附上相关文件、依赖及已有验收标准。 |

## 18. distill

| Language | Original | Proposed |
| --- | --- | --- |
| English | Distill reusable, cross-feature knowledge from an interaction into the project profile | Capture reusable lessons from interactions in the project profile, or review, revise and consolidate existing records. |
| 简体中文 | 从工作交互中提炼跨功能的可复用知识，沉淀到项目 profile | 从工作交互中提取可复用经验，存入项目知识库，或审阅、修订和合并已有记录。 |

## 19. evolve

| Language | Original | Proposed |
| --- | --- | --- |
| English | Compile vetted project-profile knowledge into a reusable command/skill and contribute it upstream via a reviewed PR | Turn vetted, broadly useful project knowledge into commands or skills; open an upstream PR after your approval. |
| 简体中文 | 把已定稿（vetted）的项目知识整理成可复用的命令/技能，经人工评审的 PR 贡献回上游 | 将已验证并认可的通用项目知识整理成命令或技能，经你确认后向上游提交 PR。 |

## 20. onboard

| Language | Original | Proposed |
| --- | --- | --- |
| English | Cold-start the project profile by scanning an existing codebase for conventions and constraints | Scan existing code to record conventions and explicit constraints in the project profile, saving constraints after your review. |
| 简体中文 | 扫描既有代码库，提取约定与约束，冷启动项目 profile | 扫描已有代码，将项目约定和明确限制记录到知识库，限制类记录经你审阅后保存。 |

## 21. reverse-spec

| Language | Original | Proposed |
| --- | --- | --- |
| English | Reverse-derive spec/design from existing code, then reconcile code against the confirmed baseline | Derive an architecture overview or module spec and design from existing code; report differences when a confirmed baseline exists. |
| 简体中文 | 从既有代码逆向还原 spec/design，再核对代码与已确认基线的偏差 | 从已有代码生成架构概览或模块规格与设计；已有确认基线时报告差异。 |

## 22. debug

| Language | Original | Proposed |
| --- | --- | --- |
| English | Debug a failure to its root cause before proposing any fix | Reproduce a reported failure, trace its root cause, then apply and verify a minimal fix. |
| 简体中文 | 先定位故障的根本原因，再着手修复 | 复现报错或异常现象，定位根本原因，再进行最小修复并验证结果。 |

## 23. commit-staged

| Language | Original | Proposed |
| --- | --- | --- |
| English | Analyze staged git changes and generate Conventional Commits compliant commit messages strictly from the staged diff | Generate a message strictly from staged changes and execute the authorized commit; use -p to preview without committing. |
| 简体中文 | 分析暂存的 git 更改并生成符合 Conventional Commits 规范的提交信息 | 仅根据暂存改动生成提交信息并执行已授权的提交；-p 只预览，不执行提交。 |

## 24. pr

| Language | Original | Proposed |
| --- | --- | --- |
| English | Generate structured Pull Request (GitHub) or Merge Request (GitLab) descriptions based on git diff and optional spec.md integration | Draft GitHub PR or GitLab MR titles, descriptions and verification guidance from branch differences. |
| 简体中文 | 基于 git diff 和可选的 spec.md 集成生成结构化的 Pull Request (GitHub) 或 Merge Request (GitLab) 描述 | 根据分支差异生成 GitHub PR 或 GitLab MR 的标题、说明与验证指引。 |

## 25. release-notes

| Language | Original | Proposed |
| --- | --- | --- |
| English | Generate release notes from git history — maintain a Keep a Changelog CHANGELOG.md entry and emit a user-facing release body, without deciding versions or mutating git state | Add a CHANGELOG.md entry and draft release notes from Git history, without publishing a release. |
| 简体中文 | 从 git 历史生成发布说明——维护 Keep a Changelog 风格的 CHANGELOG.md 条目并产出面向用户的发布正文，不决定版本号、不改动 git 状态 | 根据 Git 历史增补 CHANGELOG.md 并生成发布说明，不执行发布。 |

## 26. review-code

| Language | Original | Proposed |
| --- | --- | --- |
| English | Review a selected change as a strict defect gate, or audit paths with --audit | Review Git changes for merge readiness; use --audit to assess existing code quality. |
| 简体中文 | 将所选变更作为严格缺陷门禁进行审查，或使用 --audit 审计路径 | 审查 Git 改动并判断是否可合并；--audit 用于评估现有代码质量。 |

## 27. config

| Language | Original | Proposed |
| --- | --- | --- |
| English | Manage CodexSpec project configuration interactively | Interactively configure languages, automation, worktrees and other project options; use --view to inspect settings only. |
| 简体中文 | 以交互方式管理 CodexSpec 项目配置 | 交互式设置语言、自动化和 worktree 等项目选项；--view 只查看配置。 |

## 28. quick

| Language | Original | Proposed |
| --- | --- | --- |
| English | Run a compact requirements-first SDD flow for a small change | Confirm a small, bounded requirement, then automate specification, planning, tasks, implementation and review. |
| 简体中文 | 为小型变更运行精简的 Requirements-First SDD 流程 | 确认小范围需求后，自动完成规格、计划、任务、实现与审查。 |
