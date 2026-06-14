# Feature: Claude Code Plugin Marketplace Support

## Overview

让 CodexSpec 支持 Claude Code 插件市场功能，使用户可以通过 `/plugin install codexspec@codexspec-market` 方式安装和使用所有 CodexSpec 命令，同时保持现有的 `codexspec init` 安装方式的兼容性。

## Goals

- **G-001**: 实现 Claude Code 插件市场支持，用户可通过 `/plugin` 命令安装 CodexSpec
- **G-002**: 保持与现有 `codexspec init` 安装方式的完全兼容
- **G-003**: 复用现有命令模板，避免维护两套代码
- **G-004**: 与现有 `publish.sh` 发布流程集成，使用版本标签管理
- **G-005**: 保持多语言支持能力

## User Stories

### Story 1: 通过插件市场安装 CodexSpec

**As a** Claude Code 用户
**I want** 通过 `/plugin` 命令安装 CodexSpec
**So that** 我可以快速获取所有 CodexSpec 命令，无需额外安装 Python 包

**Acceptance Criteria:**

- [ ] 用户可以执行 `/plugin marketplace add Zts0hg/codexspec` 添加市场
- [ ] 用户可以执行 `/plugin install codexspec@codexspec-market` 安装插件
- [ ] 安装后所有 CodexSpec 命令立即可用（如 `/codexspec:specify`）
- [ ] 插件安装不需要预先安装 Python 或 codexspec CLI

### Story 2: 使用现有方式安装 CodexSpec

**As a** 现有 CodexSpec 用户
**I want** 继续使用 `codexspec init` 方式初始化项目
**So that** 我现有的工作流程不受影响

**Acceptance Criteria:**

- [ ] `uv tool install codexspec` 继续正常工作
- [ ] `codexspec init` 命令行为不变
- [ ] 两种安装方式可以在同一项目中共存

### Story 3: 获取插件更新

**As a** CodexSpec 插件用户
**I want** 通过 `/plugin update` 获取最新版本
**So that** 我可以使用最新的功能和修复

**Acceptance Criteria:**

- [ ] 用户可以执行 `/plugin update codexspec@codexspec-market` 更新插件
- [ ] 更新后获取的是 `marketplace.json` 中 `ref` 指定的版本
- [ ] Claude Code 支持自动更新（可配置）

### Story 4: 多语言支持

**As a** 非英语用户
**I want** CodexSpec 命令支持我的语言
**So that** 我可以用熟悉的语言与 Claude 交互

**Acceptance Criteria:**

- [ ] 插件命令复用现有的 `## Language Preference` 机制
- [ ] Claude 读取项目的 `.codexspec/config.yml` 获取语言设置
- [ ] 响应和生成的文档使用配置的语言

### Story 5: 发布新版本

**As a** CodexSpec 维护者
**I want** 通过现有的 `publish.sh` 脚本发布新版本
**So that** 发布流程保持一致，插件用户自动获取更新

**Acceptance Criteria:**

- [ ] `publish.sh` 自动更新 `marketplace.json` 中的 `ref` 字段
- [ ] 发布后用户可通过 `/plugin update` 获取新版本
- [ ] 版本标签与 PyPI 版本保持同步

## Functional Requirements

### FR-001: 创建 marketplace.json

在仓库根目录创建 `.claude-plugin/marketplace.json` 文件，定义插件市场。

**文件结构**:

```
.claude-plugin/
└── marketplace.json
```

**marketplace.json 内容**:

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "codexspec-market",
  "description": "Spec-Driven Development (SDD) toolkit for Claude Code - structured slash commands for AI-assisted software development",
  "owner": {
    "name": "Zts0hg",
    "email": "support@example.com"
  },
  "metadata": {
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "codexspec",
      "description": "Complete Spec-Driven Development toolkit with constitution, specification, planning, and implementation commands",
      "source": {
        "source": "github",
        "repo": "Zts0hg/codexspec",
        "ref": "v0.3.0",
        "path": ".claude/commands/codexspec"
      },
      "version": "0.3.0",
      "author": {
        "name": "Zts0hg"
      },
      "homepage": "https://github.com/Zts0hg/codexspec",
      "repository": "https://github.com/Zts0hg/codexspec",
      "license": "MIT",
      "category": "development",
      "keywords": ["spec-driven", "development", "ai", "claude", "sdd"],
      "strict": false
    }
  ]
}
```

### FR-002: 创建插件命令目录

在仓库根目录创建 `.claude/commands/codexspec/` 目录，包含所有命令文件。

**目录结构**:

```
.claude/
└── commands/
    └── codexspec/
        ├── constitution.md
        ├── specify.md
        ├── clarify.md
        ├── generate-spec.md
        ├── spec-to-plan.md
        ├── plan-to-tasks.md
        ├── review-spec.md
        ├── review-plan.md
        ├── review-tasks.md
        ├── implement-tasks.md
        ├── analyze.md
        ├── checklist.md
        ├── tasks-to-issues.md
        ├── commit-staged.md
        ├── pr.md
        ├── review-python-code.md
        ├── review-react-code.md
        ├── translate-docs.md
        └── check-i18n-semantics.md
```

### FR-003: 命令文件来源

命令文件直接复制自 `templates/commands/` 目录，保持内容一致。

**实现方式**:

- 在构建/发布时自动同步 `templates/commands/` 到 `.claude/commands/codexspec/`
- 或使用符号链接（需验证 Claude Code 插件系统支持）

### FR-004: 集成 publish.sh

修改 `publish.sh` 脚本，在发布时自动更新 `marketplace.json` 中的版本引用。

**修改内容**:

```bash
# 在 publish.sh 中添加：
# 1. 更新 marketplace.json 中的 ref 字段为新创建的 tag
# 2. 提交 marketplace.json 的更改
# 3. 推送到远程仓库
```

### FR-005: 版本同步机制

确保 `marketplace.json` 中的版本与以下位置保持同步：

- `pyproject.toml` 中的 `version` 字段
- Git tag（如 `v0.3.0`）
- `marketplace.json` 中的 `ref` 和 `version` 字段

## Non-Functional Requirements

### NFR-001: 兼容性

- 插件安装方式与 `codexspec init` 方式完全兼容
- 两种安装方式可以在同一项目中共存
- 不影响现有用户的工作流程

### NFR-002: 性能

- 插件安装时间 < 30 秒（正常网络条件下）
- 命令执行无额外延迟
- 插件更新检查不影响 Claude Code 启动速度

### NFR-003: 可维护性

- 命令文件单一来源（`templates/commands/`）
- 发布流程自动化，无需手动同步
- 代码结构清晰，易于理解

### NFR-004: 用户体验

- 安装命令简单直观
- 错误信息清晰，提供解决建议
- 多语言支持无缝集成

## Acceptance Criteria (Test Cases)

### TC-001: 插件市场添加

**前置条件**: Claude Code 已安装
**步骤**:

1. 执行 `/plugin marketplace add Zts0hg/codexspec`
**预期结果**: 市场添加成功，显示可用插件列表

### TC-002: 插件安装

**前置条件**: 已添加 codexspec-market 市场
**步骤**:

1. 执行 `/plugin install codexspec@codexspec-market`
2. 执行 `/codexspec:specify --help`
**预期结果**: 安装成功，命令可执行

### TC-003: 多语言支持

**前置条件**: 项目有 `.codexspec/config.yml` 配置 `language.output: "zh-CN"`
**步骤**:

1. 执行 `/codexspec:specify` 并输入需求
**预期结果**: Claude 使用中文响应和生成内容

### TC-004: 插件更新

**前置条件**: 已安装 codexspec 插件
**步骤**:

1. 发布新版本（修改 `marketplace.json` 中的 `ref`）
2. 执行 `/plugin update codexspec@codexspec-market`
**预期结果**: 插件更新到指定版本

### TC-005: 与 codexspec init 共存

**前置条件**: 已通过插件安装 CodexSpec
**步骤**:

1. 执行 `codexspec init`
**预期结果**: 正常初始化，无冲突

### TC-006: publish.sh 集成

**前置条件**: 有未发布的新版本
**步骤**:

1. 执行 `./publish.sh`
2. 检查 `marketplace.json` 中的 `ref`
**预期结果**: `ref` 更新为新创建的 tag

## Edge Cases

### EC-001: 用户无 .codexspec/config.yml

**场景**: 用户通过插件安装 CodexSpec，但项目没有 `.codexspec/` 目录
**处理**: 命令中的 `## Language Preference` 部分会指示 Claude 检查配置文件，如果不存在则使用英语默认值

### EC-002: 网络问题导致安装失败

**场景**: 用户网络无法访问 GitHub
**处理**: Claude Code 显示网络错误，建议使用 `codexspec init` 替代方式

### EC-003: 版本回滚

**场景**: 新版本有 bug，用户想回滚到旧版本
**处理**: 用户可以手动安装特定版本：

```bash
/plugin uninstall codexspec@codexspec-market
/plugin install codexspec@codexspec-market --ref=v0.2.0
```

### EC-004: 命令冲突

**场景**: 用户项目中已有 `.claude/commands/codexspec/` 目录
**处理**: Claude Code 插件系统会处理冲突，插件命令可能覆盖或与本地命令共存（取决于 Claude Code 实现）

## Output Examples

### 成功安装输出

```
✓ Marketplace added: codexspec-market
✓ Plugin installed: codexspec@codexspec-market v0.3.0

Available commands:
  /codexspec:constitution    - Create/update project constitution
  /codexspec:specify         - Create feature specification
  /codexspec:generate-spec   - Generate detailed spec from requirements
  /codexspec:spec-to-plan    - Convert spec to technical plan
  /codexspec:plan-to-tasks   - Break down plan into tasks
  ...and 14 more commands

Run /codexspec:specify to get started!
```

### marketplace.json 示例

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "codexspec-market",
  "description": "Spec-Driven Development (SDD) toolkit for Claude Code",
  "owner": {
    "name": "Zts0hg"
  },
  "plugins": [
    {
      "name": "codexspec",
      "description": "Complete SDD toolkit with constitution, specification, planning, and implementation commands",
      "source": {
        "source": "github",
        "repo": "Zts0hg/codexspec",
        "ref": "v0.3.0",
        "path": ".claude/commands/codexspec"
      },
      "version": "0.3.0",
      "category": "development",
      "strict": false
    }
  ]
}
```

## Out of Scope

- **多插件拆分**: 不将 CodexSpec 拆分为多个独立插件（如 codexspec-specify, codexspec-plan 等）
- **自动翻译**: 不创建预翻译的命令文件，继续使用 LLM 动态翻译
- **独立版本管理**: 不为插件单独管理版本号，与 PyPI 版本保持同步
- **私有市场**: 不支持私有/内部市场部署
- **插件配置 UI**: 不提供图形化的插件配置界面
- **命令行工具变更**: `codexspec` CLI 工具的功能和行为保持不变

## Dependencies

- Claude Code 插件系统（已支持）
- GitHub 仓库托管（现有）
- 现有 `publish.sh` 脚本
- 现有 `templates/commands/` 命令模板

## Risks and Mitigations

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| Claude Code 插件 API 变更 | 高 | 关注官方文档更新，及时适配 |
| 命令模板格式不兼容 | 中 | 测试验证插件命令是否正常加载 |
| 发布流程自动化失败 | 中 | 保留手动更新 marketplace.json 的能力 |
| 用户混淆两种安装方式 | 低 | 在文档中明确说明两种方式的适用场景 |

## Timeline

| 阶段 | 任务 | 预估时间 |
|------|------|---------|
| Phase 1 | 创建 marketplace.json 和命令目录结构 | 1-2 小时 |
| Phase 2 | 修改 publish.sh 集成版本更新 | 1 小时 |
| Phase 3 | 测试插件安装和命令执行 | 1-2 小时 |
| Phase 4 | 更新文档和 README | 1 小时 |

**总计**: 4-6 小时

## References

- [Claude Code Plugin Marketplaces 文档](https://code.claude.com/docs/en/plugin-marketplaces)
- [官方插件仓库示例](https://github.com/anthropics/claude-plugins-official)
- [CodexSpec CLAUDE.md](/.codexspec/memory/constitution.md)
