<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/images/codexspec-logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/images/codexspec-logo-light.svg">
  <img alt="CodexSpec Logo" src="assets/images/codexspec-logo-light.svg" width="420">
</picture>

# 欢迎使用 CodexSpec

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**一款面向 Claude Code 的 Requirements-First SDD 工具包**

CodexSpec 通过**需求优先的规格驱动开发（Requirements-First SDD）**帮助你交付高质量软件——已确认的需求拥有最高优先级的权威地位，在你显式确认之前，没有任何内容会被视为约束。它不急于写代码，而是先与你确认要构建**什么**以及**为什么**，再决定**如何**实现。

## 为什么选择 CodexSpec？

为什么要基于 Claude Code 使用 CodexSpec？对比如下：

| 维度 | 仅使用 Claude Code | CodexSpec + Claude Code |
|------|--------------------|-------------------------|
| **多语言支持** | 默认以英文交互 | 可为团队设定工作语言，协作与评审更顺畅 |
| **可追溯性** | 会话结束后决策难以追溯 | 所有 spec、plan、tasks 均保存在 `.codexspec/specs/` |
| **会话恢复** | Plan 模式被打断后难以恢复 | 多命令拆分 + 持久化文档，恢复轻松 |
| **团队治理** | 缺乏统一原则、风格不一致 | `constitution.md` 强制执行团队标准与质量底线 |

### 什么是 Requirements-First SDD？

**Requirements-First SDD** 是规格驱动开发（SDD）方法论的一次升级：**已确认的需求拥有最高优先级的权威地位**。在决定*如何*实现之前，你先定义并确认要做什么以及为什么——在你显式确认之前，没有任何内容会成为约束。

```
传统方式:    想法 → 代码 → 调试 → 重写
SDD:        想法 → 已确认需求 → 规格文档 → 计划 → 任务 → 代码
```

### 核心特性

- **基于宪法（Constitution）的开发** - 建立项目原则，让其指导后续所有决策
- **持久化的需求捕获** - `/specify` 在生成正式文档之前，先把已确认的讨论固化为 `requirements.md`
- **自动评审** - 每个生成的 spec、plan、tasks 工件都内置质量检查
- **交互式澄清** - 通过 Q&A 不断打磨需求
- **跨工件分析** - 在进入实现之前发现不一致
- **可追溯的任务** - 任务拆解保留对需求与计划的覆盖，并应用**条件式 TDD**（仅当计划、宪法或风险有要求时才采用测试先行；文档/配置等不可测任务直接实现）
- **原生 Claude Code 集成** - 斜杠命令无缝衔接
- **多语言支持** - 通过 LLM 动态翻译覆盖 13+ 种语言
- **跨平台** - 同时提供 Bash 与 PowerShell 脚本
- **可扩展** - 通过插件架构支持自定义命令

## 快速开始

```bash
# 安装
uv tool install codexspec

# 创建新项目
codexspec init my-project

# 或在已有项目中初始化
codexspec init . --ai claude
```

[完整安装指南](getting-started/installation.md)

## 工作流概览

CodexSpec 把开发过程拆解为一系列**可评审的检查点**。已确认的需求沿着 spec、plan、tasks 一路流转到代码，每个阶段都附带评审。

```
想法 → 已确认需求 → 规格文档 → 计划 → 任务 → 代码
```

每个工件都由专属命令产出，并在进入下一阶段之前完成校验：

```
想法 → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                  │                          │                           │
                                             评审 spec                   评审 plan                    评审 tasks
```

### 确认门（Confirmation Gate）

最关键的差异化设计是**确认门（Confirmation Gate）**：需求、spec、plan、tasks 只有在你显式确认之后才会成为约束。已确认需求拥有最高优先级的特性权威，因此 AI 无法悄悄锁定决策——派生出的工件都带显式的来源链接，冲突会被回溯定位而不是被传播扩散。

### 迭代式质量环

每个生成命令都内置**自动化、基于证据的评审**：缺陷必须有具体证据，建议性意见绝不会触发自动改动；经过验证的缺陷可被修复并最多再审两轮。这个闭环让质量持续上升，而无需你逐项盯防每一个细节。

[了解完整工作流](user-guide/workflow.md)

## 许可证

MIT License - 详情见 [LICENSE](https://github.com/Zts0hg/codexspec/blob/main/LICENSE)。
