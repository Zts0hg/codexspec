# Feature: 添加 CodexSpec 优势说明章节

## Overview

在项目 README 和 GitHub Pages 文档中新增"为什么选择 CodexSpec"章节，突出展示 CodexSpec 相较于只使用 Claude Code 原生功能的四大核心优势。

## Goals

- 帮助用户快速理解 CodexSpec + Claude Code 的组合价值
- 通过对比表格清晰展示优势差异
- 在各语言版本文档中保持一致性

## User Stories

### Story 1: 开发者了解工具价值

**As a** 正在评估 CodexSpec 的开发者
**I want** 快速了解 CodexSpec 相比 Claude Code 原生功能的优势
**So that** 我能做出明智的选择，决定是否采用 CodexSpec

**Acceptance Criteria:**

- [ ] 文档中有清晰的对比表格
- [ ] 对比维度覆盖 4 个核心优势
- [ ] 优势描述具体可感知，非泛泛而谈

### Story 2: 多语言团队选择工具

**As a** 使用非英语母语的团队成员
**I want** 看到我熟悉的语言版本的优势说明
**So that** 我能更好地理解和传播工具价值

**Acceptance Criteria:**

- [ ] 所有语言版本 README 都包含该章节
- [ ] GitHub Pages 各语言版首页同步更新

## Functional Requirements

### REQ-001: README 新增章节

在 `README.md` 和 `README.zh-CN.md` 以及其他语言版本中，在"什么是规格驱动开发"章节之前新增"为什么选择 CodexSpec"章节。

**位置要求**：

- 紧跟项目简介（徽章、一句话描述、文档链接）之后
- 在"Table of Contents"之后
- 在"What is Spec-Driven Development?"之前

### REQ-002: 章节内容结构

章节标题：`## Why Choose CodexSpec?`（英文）/ `## 为什么选择 CodexSpec`（中文）

章节包含：

1. 简短引言（1-2 句话）
2. 对比表格（4 行对应 4 个优势）
3. 简短结语（可选）

### REQ-003: 四大核心优势对比

| 优势维度 | 只使用 Claude Code | CodexSpec + Claude Code |
|----------|-------------------|------------------------|
| **多语言适配** | 默认英文交互，非英语用户体验不佳 | 配置团队语言，交互和审阅过程更顺畅高效 |
| **可追溯性** | 会话结束后难以追溯历史决策 | `.codexspec/specs/` 保存所有规格、方案、任务 |
| **会话恢复** | plan mode 误操作会话中断，恢复困难 | 多命令拆分 + 持久化文档，随时恢复进度 |
| **团队治理** | 无统一原则约束，风格不统一 | constitution.md 定制团队原则，保持质量风格统一 |

### REQ-004: GitHub Pages 更新

在 `docs/*/index.md` 各语言版首页同步新增该章节。

**涉及文件**：

- `docs/en/index.md`
- `docs/zh/index.md`
- `docs/ja/index.md`
- `docs/ko/index.md`
- `docs/es/index.md`
- `docs/fr/index.md`
- `docs/de/index.md`
- `docs/pt-BR/index.md`

## Non-Functional Requirements

### NFR-001: 内容质量

- 对比描述准确反映实际功能差异
- 避免过度承诺或夸大
- 语言简洁有力

### NFR-002: 国际化一致性

- 各语言版本语义一致
- 术语翻译准确
- 保持各语言 README 风格统一

## Acceptance Criteria (Test Cases)

### TC-001: README 结构验证

- 打开 `README.md`，确认"为什么选择 CodexSpec"章节存在
- 确认章节位于"What is Spec-Driven Development?"之前
- 确认包含 4 行对比表格

### TC-002: 中文 README 验证

- 打开 `README.zh-CN.md`
- 确认章节标题为"为什么选择 CodexSpec"
- 确认内容与英文版语义一致

### TC-003: GitHub Pages 验证

- 检查 `docs/en/index.md` 包含该章节
- 检查 `docs/zh/index.md` 包含该章节
- 抽查其他语言版本

## Edge Cases

- **章节已存在**：如果文档中已有类似章节，应合并而非重复添加
- **结构变化**：如果 README 结构已变化，需要调整插入位置以保持逻辑流畅

## Output Examples

### 英文版示例

```markdown
## Why Choose CodexSpec?

Why use CodexSpec on top of Claude Code? Here's the comparison:

| Aspect | Claude Code Only | CodexSpec + Claude Code |
|--------|------------------|-------------------------|
| **Multi-language Support** | Default English interaction | Configure team language for smoother collaboration and reviews |
| **Traceability** | Hard to trace decisions after session ends | All specs, plans, and tasks saved in `.codexspec/specs/` |
| **Session Recovery** | Plan mode interruptions are hard to recover from | Multi-command split + persisted docs = easy recovery |
| **Team Governance** | No unified principles, inconsistent styles | `constitution.md` enforces team standards and quality |

---

## What is Spec-Driven Development?
...
```

### 中文版示例

```markdown
## 为什么选择 CodexSpec？

为什么在 Claude Code 之上使用 CodexSpec？以下是对比：

| 维度 | 只使用 Claude Code | CodexSpec + Claude Code |
|------|-------------------|------------------------|
| **多语言适配** | 默认英文交互，非英语用户体验不佳 | 配置团队语言，交互和审阅更顺畅高效 |
| **可追溯性** | 会话结束后难以追溯历史决策 | `.codexspec/specs/` 保存所有规格、方案、任务 |
| **会话恢复** | plan mode 误操作会话中断，恢复困难 | 多命令拆分 + 持久化文档，随时恢复进度 |
| **团队治理** | 无统一原则约束，风格不统一 | `constitution.md` 定制团队原则，保持质量风格统一 |

---

## 什么是规格驱动开发？
...
```

## Out of Scope

- 不修改 `docs/*/user-guide/` 或其他子页面
- 不创建独立的"为什么选择 CodexSpec"页面
- 不修改 CLAUDE.md 或其他配置文件
- 不更新 spec-kit 对比章节（保持现有内容）
