# Feature: 扩展 CodexSpec 支持 OpenAI Codex CLI

## 概述

扩展 CodexSpec 的 `init` 命令和配置系统，使其在现有 Claude Code 支持的基础上，额外支持 OpenAI Codex CLI（github.com/openai/codex）。用户通过 `codexspec init --ai codex` 即可初始化一个适配 Codex CLI 的项目。

## 目标

- 支持 `codexspec init --ai codex` 创建 Codex CLI 适配的项目结构
- 生成 `AGENTS.md`（Codex 的项目指令文件）替代 `CLAUDE.md`
- 配置文件正确记录所选 AI 工具
- 保持与现有 Claude Code 支持的完全向后兼容

## 用户故事

### Story 1: 使用 Codex CLI 初始化项目

**As a** 使用 OpenAI Codex CLI 的开发者
**I want** 通过 `codexspec init --ai codex` 初始化一个 SDD 项目
**So that** 我能在 Codex CLI 中使用 CodexSpec 的规格驱动开发工作流

**验收标准：**

- [ ] 运行 `codexspec init my-project --ai codex` 成功创建项目
- [ ] 项目根目录生成 `AGENTS.md`（而非 `CLAUDE.md`）
- [ ] `.codexspec/` 目录结构正常创建（memory, specs, templates, scripts）
- [ ] `.codexspec/config.yml` 中 `project.ai` 值为 `"codex"`
- [ ] 不创建 `.claude/commands/` 目录

### Story 2: AGENTS.md 内容完整且适配

**As a** Codex CLI 用户
**I want** 生成的 `AGENTS.md` 包含完整的 SDD 工作流指引
**So that** Codex CLI 能正确理解项目结构和开发流程

**验收标准：**

- [ ] `AGENTS.md` 包含 constitution 读取指令（纯文本形式，非 `@` 引用语法）
- [ ] 包含项目概述和 SDD 方法论说明
- [ ] 包含目录结构说明
- [ ] 以纯文本方式描述 SDD 工作流步骤（非 slash command 格式）
- [ ] 包含 `.codexspec/` 目录结构说明
- [ ] 文件大小不超过 Codex CLI 的 32 KiB 限制

### Story 3: 参数验证和错误处理

**As a** CodexSpec 用户
**I want** 输入无效的 `--ai` 参数时得到清晰的错误提示
**So that** 我能快速了解支持的 AI 工具选项

**验收标准：**

- [ ] `--ai invalid` 时显示错误信息，列出支持的选项（claude, codex）
- [ ] 错误信息遵循项目的 i18n 配置
- [ ] `--ai claude` 行为完全不变（向后兼容）

### Story 4: 配置系统适配

**As a** CodexSpec 开发者
**I want** 配置系统正确反映所选 AI 工具
**So that** 其他命令和模板能识别当前项目使用的 AI 工具

**验收标准：**

- [ ] `generate_config_content()` 函数接受 `ai` 参数
- [ ] 生成的 `config.yml` 中 `project.ai` 字段为传入的 AI 值
- [ ] CONFIG_TEMPLATE 使用 `{ai}` 占位符替代硬编码的 `"claude"`
- [ ] 默认值保持 `"claude"`（向后兼容）

## 功能需求

- [REQ-001] `init` 命令的 `--ai` 参数支持 `"codex"` 值，除现有的 `"claude"` 外
- [REQ-002] 当 `--ai codex` 时，在项目根目录创建 `AGENTS.md` 文件，内容为 Codex 适配的项目指引
- [REQ-003] 当 `--ai codex` 时，跳过 `.claude/commands/` 目录及 slash command 模板安装
- [REQ-004] 当 `--ai codex` 时，仍创建完整的 `.codexspec/` 目录结构（memory, specs, templates, scripts）
- [REQ-005] `_get_agents_md_content(project_name)` 函数生成 Codex 适配的 `AGENTS.md` 内容
- [REQ-006] `AGENTS.md` 内容包含：constitution 内联引导（非 `@` 语法）、项目概述、SDD 工作流（纯文本描述）、目录结构。由于 Codex CLI 不支持 Claude Code 的 `@file` 引用语法，改为在 AGENTS.md 中以纯文本指令引导 Codex 读取 constitution 文件
- [REQ-007] `generate_config_content()` 接受 `ai` 参数，写入 `project.ai` 字段
- [REQ-008] `CONFIG_TEMPLATE` 中的 `project.ai` 使用占位符 `{ai}` 替代硬编码值
- [REQ-009] `--ai` 参数验证：仅允许 `"claude"` 和 `"codex"`，无效值给出清晰错误
- [REQ-010] 所有变更保持与 `--ai claude`（默认值）的完全向后兼容

## 非功能需求

- [NFR-001] `AGENTS.md` 文件大小不超过 32 KiB（Codex CLI 的文档大小限制）
- [NFR-002] 代码遵循项目现有风格：120 字符行长、PEP 8、ruff 检查通过
- [NFR-003] 新增公共函数必须包含 type hints 和 docstrings
- [NFR-004] 测试覆盖所有新增和修改的逻辑分支

## 验收测试用例

- [TC-001] `codexspec init test-project --ai codex --lang en` → 创建 `AGENTS.md`，无 `CLAUDE.md`，无 `.claude/` 目录
- [TC-002] `codexspec init test-project --ai codex --lang zh-CN` → `AGENTS.md` 创建成功，config 语言为 zh-CN
- [TC-003] `codexspec init test-project --ai claude` → 行为与之前完全一致（回归测试）
- [TC-004] `codexspec init test-project` → 默认使用 claude，行为不变
- [TC-005] `codexspec init test-project --ai invalid` → 显示错误信息
- [TC-006] `codexspec init test-project --ai codex` → `.codexspec/config.yml` 包含 `ai: "codex"`
- [TC-007] `codexspec init test-project --ai codex` → `.codexspec/` 目录结构完整（memory, specs, templates, scripts）
- [TC-008] AGENTS.md 文件大小 < 32 KiB

## 边界情况

- **已存在 AGENTS.md**：与 CLAUDE.md 逻辑一致 — 如果已存在且非 `--force`，保留现有文件
- **已存在 CLAUDE.md 但使用 `--ai codex`**：不删除旧的 CLAUDE.md，仅创建新的 AGENTS.md
- **目录已初始化过**：`--force` 标志行为不变，适用于所有 AI 类型
- **非 TTY 环境**：`--ai` 默认值为 "claude"，行为不变
- **混合使用**：用户先 `--ai claude` 再 `--ai codex --force`，新文件覆盖配置但不清理旧文件

## 输出示例

### AGENTS.md 结构示例

```markdown
# AGENTS.md - {project_name} Guidelines

> **IMPORTANT**: Before making any decisions, read the project constitution at
> `.codexspec/memory/constitution.md`. All code changes must comply with the
> principles defined there.

## Project Overview

This project uses the **CodexSpec** methodology - a Spec-Driven Development (SDD)
approach that emphasizes specifications as executable artifacts that directly guide
implementation.

## Recommended SDD Workflow

1. **Establish Principles**: Edit `.codexspec/memory/constitution.md` to define project guidelines
2. **Create Specification**: Write feature requirements in `.codexspec/specs/{feature}/spec.md`
3. **Create Plan**: Write technical implementation plan in `.codexspec/specs/{feature}/plan.md`
4. **Break Down Tasks**: Create task breakdown in `.codexspec/specs/{feature}/tasks.md`
5. **Implement**: Execute tasks according to the breakdown
6. **Review**: Validate code against spec and constitution

## Directory Structure

```

.codexspec/
├── memory/
│   └── constitution.md    # Project governing principles
├── specs/
│   └── {feature-id}/
│       ├── spec.md        # Feature specification
│       ├── plan.md        # Technical implementation plan
│       └── tasks.md       # Task breakdown
├── templates/             # Custom templates
├── scripts/               # Helper scripts
└── config.yml             # Project configuration

```

## Important Notes

- Always read the constitution before making decisions
- Specifications focus on **what** and **why**, not **how**
- Plans focus on **how** and technical choices
- Tasks should be specific, ordered, and actionable

## Guidelines

1. **Constitution First**: Read `.codexspec/memory/constitution.md` before ANY action
2. **Respect the Constitution**: All decisions MUST align with the project constitution
3. **Follow the Workflow**: Use the SDD workflow in the recommended order
4. **Be Explicit**: When specifications are unclear, ask for clarification
5. **Validate**: Always review artifacts before implementation
```

### config.yml 示例

```yaml
project:
  ai: "codex"
  created: "2026-04-24"
```

## 不在范围内

- 不重构 AI agent 抽象层（如 AgentAdapter 接口）
- 不支持同时安装两个 AI 的配置（`--ai` 互斥选择）
- 不修改现有模板内容（templates/commands/*.md）
- 不支持其他 AI 工具（Gemini CLI、Cursor、Windsurf 等留待未来）
- 不在 Codex 的 `.codex/` 目录中安装自定义配置
- 不修改 `_get_default_constitution()` 内容（与 AI 工具无关）
