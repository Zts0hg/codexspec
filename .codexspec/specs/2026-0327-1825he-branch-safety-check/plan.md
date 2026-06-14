# 实现计划：Git 分支安全检测

## 1. 技术栈

| 类别 | 技术 | 版本 | 说明 |
|------|------|------|------|
| 语言 | Markdown | N/A | slash 命令模板格式 |
| 运行环境 | Claude Code | N/A | AI 助手执行环境 |
| 依赖工具 | Bash | 3.2+ | Git 命令执行 |
| 依赖工具 | Git | 2.0+ | 分支检测和创建 |

## 2. 宪法合规性审查

| 原则 | 合规状态 | 说明 |
|------|----------|------|
| 代码质量 | ✅ | 改动范围极小（2 个 Markdown 文件），易于维护 |
| 测试标准 | ✅ | 通过手动测试验证，规格中已定义 6 个测试用例 |
| 文档 | ✅ | 修改本身即为文档更新，包含清晰的使用说明 |
| 架构 | ✅ | 遵循现有 slash 命令模板模式，无架构变更 |
| 性能 | ✅ | 单次 `git branch` 调用，性能影响可忽略 |
| 安全 | ✅ | 不涉及安全敏感操作，仅读取分支信息 |

## 3. 架构概述

```
┌─────────────────────────────────────────────────────────────┐
│                    用户执行命令                              │
│              /codexspec:specify "功能描述"                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Git 分支安全检测                           │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ 检测当前分支 │───▶│ 判断主分支？ │───▶│ 交互式询问  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌───────────┐   ┌───────────┐   ┌───────────┐
    │ 创建新分支 │   │ 继续当前  │   │ 取消操作  │
    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
          │               │               │
          ▼               ▼               ▼
    ┌─────────────────────────────────────────┐
    │           继续原有命令流程               │
    └─────────────────────────────────────────┘
```

## 4. 文件结构

### 目录结构说明

CodexSpec 项目有两个相关的命令目录：

| 目录 | 用途 | 修改策略 |
|------|------|----------|
| `templates/commands/` | **源模板目录** - `codexspec init` 从这里复制模板到用户项目 | ✅ **需要修改** |
| `.claude/commands/codexspec/` | **当前项目使用的命令** - 由 `codexspec init` 安装 | ❌ 不应直接修改 |

> **重要**：修改应该只在 `templates/commands/` 中进行。当用户运行 `codexspec init` 时，模板会被复制到项目的 `.claude/commands/codexspec/` 目录。

### 修改范围

```
codexspec/
├── templates/
│   └── commands/
│       ├── specify.md        # 【修改】添加分支检测指令
│       └── generate-spec.md  # 【修改】添加分支检测指令
└── scripts/
    └── bash/
        └── create-new-feature.sh  # 【不修改】现有脚本，可被调用
```

## 5. 模块依赖关系

```
┌─────────────────────┐
│  specify.md 模板    │
│  generate-spec.md   │
└──────────┬──────────┘
           │ 依赖
           ▼
┌─────────────────────┐     ┌─────────────────────┐
│   Claude Code Bash  │────▶│   Git 命令          │
│   工具              │     │   git branch        │
└─────────────────────┘     └─────────────────────┘
           │
           ▼
┌─────────────────────┐
│ AskUserQuestion     │
│ 工具                │
└─────────────────────┘
           │
           ▼
┌─────────────────────┐
│ create-new-feature  │
│ .sh（可选调用）     │
└─────────────────────┘
```

## 6. 模块规格

### 模块：Git 分支安全检测指令

- **职责**：在 slash 命令执行前检测当前 Git 分支状态，并在主分支时提示用户
- **依赖**：Claude Code Bash 工具、AskUserQuestion 工具
- **接口**：Markdown 指令块，指导 AI 执行特定操作
- **文件**：
  - `templates/commands/specify.md`（修改）
  - `templates/commands/generate-spec.md`（修改）

### 指令块设计

```markdown
## Git Branch Safety Check

Before proceeding with requirement clarification:

1. **Check Git Environment**
   - Run: `git rev-parse --is-inside-work-tree 2>/dev/null`
   - If not a git repository, skip this check and continue

2. **Get Current Branch**
   - Run: `git branch --show-current`
   - Store the result as `current_branch`

3. **Check Main Branch**
   - Read main branch names from `.codexspec/config.yml` (key: `git.main_branches`)
   - Default main branches: `["main", "master"]`
   - If `current_branch` is in main branches list, proceed to step 4
   - Otherwise, skip to continue with the command

4. **Interactive Prompt**
   Use AskUserQuestion tool with the following structure:
   - Question: "您当前在主分支「{current_branch}」上。建议为新功能创建独立分支。"
   - Options:
     1. "创建新功能分支（推荐）" - Prompt for feature name, create branch
     2. "在当前分支继续工作" - Continue without creating branch
     3. "取消操作" - Stop execution

5. **Branch Creation** (if user chose option 1)
   - Ask for feature name using AskUserQuestion
   - Generate branch name: `{timestamp}-{random}-{feature-name}`
   - Run: `git checkout -b {branch_name}`
   - Confirm success and continue

6. **Continue Command**
   After branch handling (or if skipped), proceed with the original command flow.
```

## 7. 实现阶段

### 阶段 1：基础实现

- [ ] 修改 `templates/commands/specify.md`，在 `## Instructions` 之前添加 `## Git Branch Safety Check` 章节
- [ ] 修改 `templates/commands/generate-spec.md`，添加相同的分支检测指令

### 阶段 2：测试验证

- [ ] 在 main 分支测试 `/codexspec:specify`，验证提示出现
- [ ] 测试选择"创建新功能分支"，验证分支创建成功
- [ ] 测试选择"在当前分支继续"，验证命令继续执行
- [ ] 在功能分支测试，验证无提示
- [ ] 在非 Git 目录测试，验证跳过检测

### 阶段 3：文档更新

- [ ] 更新 `CLAUDE.md` 中的命令说明（如有必要）
- [ ] 更新 `README.md` 中的功能列表（如有必要）

## 8. 技术决策

### 决策 1：检测位置选择

- **选择**：在 `## Instructions` 之前添加 `## Git Branch Safety Check` 章节
- **理由**：
  - 分支检测应在命令主体逻辑之前执行
  - 作为独立章节，易于维护和复用
  - 不干扰现有指令结构
- **备选方案**：
  - 在 `## Instructions` 内部添加（会导致指令混杂）
  - 作为 YAML frontmatter 中的配置（不支持复杂逻辑）
- **权衡**：增加了模板长度，但换来了更好的用户体验

### 决策 2：交互工具选择

- **选择**：使用 `AskUserQuestion` 工具
- **理由**：
  - 支持结构化选项，减少用户输入
  - 与 CodexSpec 现有命令风格一致
  - 自动支持"其他"选项
- **备选方案**：
  - 使用纯文本提示（用户需要手动输入）
- **权衡**：依赖特定工具，但该工具是 Claude Code 标准工具

### 决策 3：分支创建方式

- **选择**：直接使用 `git checkout -b` 命令
- **理由**：
  - 简单直接，不依赖外部脚本
  - 避免脚本路径解析问题
  - 分支命名格式与 `create-new-feature.sh` 一致
- **备选方案**：
  - 调用 `scripts/bash/create-new-feature.sh`（路径依赖复杂）
- **权衡**：不利用现有脚本，但实现更简洁可靠

### 决策 4：配置读取

- **选择**：读取 `.codexspec/config.yml` 中的 `git.main_branches` 配置
- **理由**：
  - 支持自定义主分支名称（如 `develop`）
  - 与现有配置系统集成
  - 提供合理的默认值
- **备选方案**：
  - 硬编码 `main` 和 `master`（不灵活）
- **权衡**：需要额外读取配置文件，但提供更好的灵活性

## 9. 配置扩展

需要在 `.codexspec/config.yml` 中添加新的配置项：

```yaml
version: "1.0"
language:
  output: "zh-CN"
git:
  main_branches:
    - "main"
    - "master"
  branch_check_enabled: true  # 可选：允许禁用分支检测
```

## 10. 质量检查清单

- [ ] 模板修改遵循现有格式风格
- [ ] 使用 AskUserQuestion 工具进行交互
- [ ] 非 Git 环境优雅降级
- [ ] 功能分支不触发检测
- [ ] 主分支名称可配置
- [ ] 分支命名格式与现有脚本一致
- [ ] 语言偏好设置得到尊重

## 11. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| Git 命令执行失败 | 低 | 使用 `2>/dev/null` 静默错误，跳过检测 |
| 配置文件不存在 | 低 | 提供默认值 `["main", "master"]` |
| 用户在 detached HEAD | 中 | 视为非主分支，不触发提示 |
| 分支名已存在 | 低 | Git 会报错，AI 可提示用户选择其他名称 |

## 12. 输出

保存位置：`.codexspec/specs/2026-0327-1825he-branch-safety-check/plan.md`
