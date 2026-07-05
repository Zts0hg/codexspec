# 快速入门

本页用一个八步流程走完完整的 **Requirements-First SDD** 链路。
已确认的需求拥有最高优先级，在你显式确认之前，没有任何内容会被视为约束——每个阶段都终止于由你掌控的**确认门**。

对于规模小、边界清晰的改动，可以跳过完整流程，改用 [`/codexspec:quick`](#小改动codexspecquick)。

## 1. 初始化项目

安装完成后，创建或初始化项目：

```bash
# 创建新项目
codexspec init my-awesome-project

# 或在当前目录初始化
codexspec init . --ai claude

# 使用中文输出（设定输出基准语言）
codexspec init my-project --lang zh-CN

# 完全非交互（CI/脚本）：zh-CN 输出，英文提交信息
codexspec init my-project --lang zh-CN --commit-lang en

# 显式设定每个语言维度（可脚本化，无提示）
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

然后进入项目目录并启动 Claude Code：

```bash
cd my-awesome-project
claude
```

## 2. 建立项目原则

使用 constitution 命令确立后续所有工件都要对照检查的标准：

```
/codexspec:constitution 创建聚焦代码质量与测试的原则
```

## 3. 澄清需求

使用 `/codexspec:specify` 探索需求：

```
/codexspec:specify 我想构建一个任务管理应用
```

该命令会提出澄清问题、暴露边界情况，并请你确认最终的需求摘要，该摘要会被持久化到 `requirements.md`。

> **确认门**：`/codexspec:specify` 只写入你显式确认的条目。它呈现的需求摘要**在你接受之前并不具备约束力**——在按下 yes 之前，你可以拒绝、修改或重新打开任一项。下游没有任何东西能够覆盖你在这里确认的内容。

## 4. 生成规格

需求摘要确认后，生成规格文档：

```
/codexspec:generate-spec
```

`generate-spec` 把已确认的条目编译为结构化的 `spec.md`，并附带来源引用以便追溯，随后自动运行评审（缺陷需有具体证据；建议性意见从不触发自动修改；已核实的缺陷最多可修复并重审两轮）。

## 5. 评审与校验

**推荐**：在继续之前先校验规格：

```
/codexspec:review-spec
```

这是一次**基于证据的评审**：每条报告的缺陷都引用具体证据，设计建议与验收保持分离。

## 6. 创建技术计划

```
/codexspec:spec-to-plan 后端使用 Python FastAPI
```

计划会记录指向规格需求的 `Covers` 链接，并校验适用的宪法原则。

## 7. 生成任务

```
/codexspec:plan-to-tasks
```

任务围绕可验证的结果组织，并带有指向计划与需求的追溯链接。测试优先的顺序**有条件地**施加——仅在计划、宪法或任务风险要求时。文档、配置等不可测任务直接实现。

## 8. 实现

```
/codexspec:implement-tasks
```

实现遵循**条件式 TDD**：代码任务在需要时采用 Red → Green → Verify → Refactor 循环；文档与配置任务直接实现。

## 小改动：`/codexspec:quick`

对于规模小、边界清晰的改动，你不需要走完整的八步流程。`/codexspec:quick` 用单条命令运行一个精简的 Requirements-First SDD 流程：

```
/codexspec:quick 给登录表单加一个"记住我"复选框
```

Quick 仍然遵守与完整流程相同的护栏：

- 它创建功能工作区与 `requirements.md`，时间戳命名约定与 `/codexspec:specify` 一致。
- 它呈现精简的已确认需求摘要（`NEED-*`、相关的 `CON-*`/`DEC-*`、`OUT-*`、未解决的 `OPEN-*`），并等待你的显式确认——**确认门**依然生效。
- 随后在该功能目录上链式调用 `/codexspec:generate-spec` → `/codexspec:spec-to-plan` → `/codexspec:plan-to-tasks` → `/codexspec:implement-tasks`，每个生成命令各自负责其自动评审闭环。

如果改动最终范围较广、或包含多个独立结果，Quick 会暂停并建议改用标准流程。

## 项目结构

初始化后的目录结构：

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # 项目宪法
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # 功能规格
│   │       ├── plan.md        # 技术计划
│   │       ├── tasks.md       # 任务拆解
│   │       └── checklists/    # 质量检查清单
│   ├── templates/             # 自定义模板
│   ├── scripts/               # 辅助脚本
│   └── extensions/            # 自定义扩展
├── .claude/
│   └── commands/              # Claude Code 斜杠命令
├── .agents/
│   └── skills/                # Codex skills（使用 --ai codex 或 both 初始化时生成）
├── CLAUDE.md                  # Claude Code 上下文
└── AGENTS.md                  # Codex 上下文
```

## 下一步

[完整工作流指南](../user-guide/workflow.md)
