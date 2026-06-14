# 特性：命令组织优化

## 概述

当前 CodexSpec 通过 `codexspec init` 命令将所有 slash command 模板直接复制到项目的 `.claude/commands/` 目录根目录。随着命令数量增加（目前已有 13+ 个），这些命令与用户自定义命令混在一起，导致：

1. 不易区分哪些是 CodexSpec 提供的工具命令
2. 想要自定义调整时难以搜索和定位
3. 管理混乱，用户体验不佳

本特性旨在通过子目录组织结构优化命令管理，同时提供更好的自定义和版本控制支持。

## 目标

- 将 CodexSpec 命令与用户自定义命令分离
- 简化用户自定义命令模板的流程
- 利用 Git 提供透明的版本控制和变更管理
- 提供命令列表查看功能，提升可发现性
- 平滑迁移现有用户到新结构

## 用户故事

### 故事 1：新用户初始化项目

**作为** CodexSpec 的新用户
**我想要** 运行 `codexspec init` 时命令被整洁地组织在子目录中
**以便于** 我能清晰地区分 CodexSpec 命令和我的自定义命令

**验收标准：**

- [ ] 命令安装到 `.claude/commands/codexspec/` 子目录
- [ ] 终端显示已安装的命令列表摘要
- [ ] 提示用户将 `.claude/` 目录纳入 Git 管理
- [ ] 不再自动将 `.claude/` 添加到 `.gitignore`

### 故事 2：用户自定义命令模板

**作为** 想要自定义工作流的用户
**我想要** 直接修改 `.claude/commands/codexspec/` 下的命令模板
**以便于** 我能根据项目需求调整命令行为

**验收标准：**

- [ ] 可以直接编辑子目录中的任何 `.md` 文件
- [ ] 通过 Git 可以查看修改历史和差异
- [ ] Claude Code 能正常识别和使用修改后的命令

### 故事 3：现有用户迁移

**作为** 已有项目的现有用户（使用旧结构）
**我想要** 升级 CodexSpec 后平滑迁移到新结构
**以便于** 我能继续使用新版本而不会丢失自定义修改

**验收标准：**

- [ ] `init` 检测到旧结构（根目录有 `codexspec.*.md` 文件）时提示迁移选项
- [ ] 迁移过程将旧文件移动到新目录，**保留用户已修改的文件内容**
- [ ] 迁移后根目录的旧命令文件被删除
- [ ] 迁移完成后自动进入"更新模板"流程（故事4）

### 故事 4：更新命令模板

**作为** 项目已有新目录结构的用户
**我想要** 有选择地更新项目中的命令模板
**以便于** 我能获取新功能同时保留我的自定义

**验收标准：**

- [ ] `init` 检测到 `.claude/commands/codexspec/` 目录已存在时询问是否更新
- [ ] 用户确认后直接覆盖模板文件
- [ ] 用户通过 Git 工具（如 `git diff`）查看变更
- [ ] 用户可通过 `git checkout` 恢复自定义内容

### 故事 5：查看可用命令

**作为** 用户
**我想要** 快速查看所有可用的 CodexSpec 命令
**以便于** 我能了解可以使用的功能

**验收标准：**

- [ ] 新增 `codexspec list-commands` CLI 命令
- [ ] 显示命令名称、描述和用途
- [ ] 输出格式清晰易读

## 功能需求

### REQ-001：子目录组织结构

所有 CodexSpec 命令模板安装到 `.claude/commands/codexspec/` 子目录，而非 `.claude/commands/` 根目录。

**命令列表：**

- 核心命令 (9)：`constitution.md`, `specify.md`, `generate-spec.md`, `spec-to-plan.md`, `plan-to-tasks.md`, `review-spec.md`, `review-plan.md`, `review-tasks.md`, `implement-tasks.md`
- 增强命令 (4)：`clarify.md`, `analyze.md`, `checklist.md`, `tasks-to-issues.md`
- Git 命令 (3)：`commit.md`, `commit-staged.md`, `pr.md`

### REQ-002：Git 集成推荐

`init` 命令应推荐用户将 `.claude/` 目录纳入 Git 版本控制，不再自动添加到 `.gitignore`。

**实现要点：**

- 移除自动添加 `.claude/` 到 `.gitignore` 的逻辑
- 在 `init` 输出中添加提示信息
- 在 README.md 中说明推荐的 Git 管理方式

### REQ-003：迁移策略（旧结构→新结构）

> **流程说明**：迁移和更新是同一流程的两个阶段。对于现有用户，先执行迁移（REQ-003），迁移完成后自动进入更新流程（REQ-004）。

当检测到旧结构（`.claude/commands/` 根目录下存在 CodexSpec 命令文件）时：

1. 识别旧命令文件（通过文件名前缀 `codexspec.` 匹配）
2. 提示用户是否迁移到新结构
3. 如果用户同意，将旧文件移动到 `.claude/commands/codexspec/` 子目录
4. **保留用户已修改的文件内容**（不做内容变更，仅移动位置）
5. 迁移完成后删除根目录的旧文件
6. **继续执行 REQ-004**（询问是否更新模板）

### REQ-004：更新策略（新结构已存在）

当 `.claude/commands/codexspec/` 目录已存在时（新用户初始化后，或现有用户迁移后）：

1. 询问用户是否更新/覆盖命令模板
2. 用户确认后直接覆盖所有模板文件
3. 用户通过 Git 查看差异（`git diff`）并决定保留哪些变更
4. 用户可通过 `git checkout` 恢复自定义内容

### REQ-005：`list-commands` 命令

新增 CLI 命令 `codexspec list-commands`，显示所有可用的 CodexSpec 命令。

**输出格式：**

```
CodexSpec 可用命令：

核心命令 (Core Commands):
  /codexspec.constitution    创建或更新项目宪法
  /codexspec.specify         通过交互式问答明确需求
  ...

增强命令 (Enhanced Commands):
  /codexspec.clarify         在规划前提出澄清问题
  ...

Git 工作流命令 (Git Workflow):
  /codexspec.commit          生成规范的提交信息
  ...

共 16 个命令可用。
```

### REQ-006：`init` 输出增强

`init` 命令执行完成后，在终端显示已安装的命令列表摘要。

**示例输出：**

```
✅ CodexSpec 初始化完成！

📁 已安装 16 个命令到 .claude/commands/codexspec/

💡 提示：
   - 建议将 .claude/ 目录纳入 Git 管理
   - 运行 codexspec list-commands 查看所有可用命令
   - 直接编辑 .md 文件自定义命令行为
```

## 非功能需求

### NFR-001：向后兼容

- 旧项目（使用根目录命令）应继续正常工作
- 用户可以选择不迁移，保持原有结构

### NFR-002：性能

- `init` 命令总执行时间 < 3 秒（在标准 SSD 硬盘上）
- `init` 命令因新增功能导致的执行时间增加不超过 500ms
- `list-commands` 命令响应时间 < 1 秒

### NFR-003：用户体验

- 提示信息清晰、简洁
- 迁移过程可逆或可取消
- 错误信息提供可操作的建议

### NFR-004：文档完整性

- README.md 更新说明新的组织结构
- CLI 帮助文本 (`--help`) 准确描述功能
- 内联代码注释解释关键逻辑

## 验收标准（测试用例）

### TC-001：新项目初始化

**前置条件：** 空项目目录
**步骤：**

1. 运行 `codexspec init`
2. 检查 `.claude/commands/codexspec/` 目录存在
3. 验证所有命令模板已安装
4. 验证终端显示命令列表摘要

**预期结果：**

- 目录结构正确
- 所有 16 个命令文件存在
- 输出包含提示信息

### TC-002：旧结构迁移

**前置条件：** 项目中存在 `.claude/commands/codexspec.specify.md`（旧结构）
**步骤：**

1. 运行 `codexspec init`
2. 选择迁移选项

**预期结果：**

- 旧文件移动到 `.claude/commands/codexspec/specify.md`
- 根目录的旧文件被删除
- **用户自定义的内容被保留**（仅移动位置）
- 迁移后自动询问是否更新模板

### TC-003：更新已修改的命令

**前置条件：** 项目已初始化（新结构），用户已修改 `specify.md` 并提交到 Git
**步骤：**

1. 升级 CodexSpec 到新版本
2. 运行 `codexspec init`
3. 选择更新命令模板

**预期结果：**

- 模板文件被覆盖
- 用户可通过 `git diff` 查看变更
- 用户可通过 `git checkout` 恢复自定义内容

### TC-004：list-commands 输出

**步骤：**

1. 运行 `codexspec list-commands`

**预期结果：**

- 输出包含所有 16 个命令
- 命令按类别分组
- 每个命令有简短描述

### TC-005：Claude Code 识别子目录命令

**前置条件：** 项目已初始化
**步骤：**

1. 在 Claude Code 中输入 `/`
2. 查看命令列表

**预期结果：**

- CodexSpec 命令出现在列表中
- 命令显示命名空间标识 `(project:codexspec)`
- 命令可正常执行

## 边界情况

### 边界 1：部分迁移场景

**场景：** 用户只有部分旧命令文件（不是全部 16 个）
**处理：** 迁移时只移动存在的文件，不报错

### 边界 2：目标目录已存在同名文件

**场景：** `.claude/commands/codexspec/` 目录已存在（可能是之前手动创建的）
**处理：** 旧结构文件优先移动到新位置（覆盖目标），然后统一询问用户是否用模板覆盖所有命令

> **说明**：不存在"冲突"问题，迁移流程是：移动旧文件 → 询问是否用模板覆盖 → 用户决定。用户自行根据是否使用 Git 来决定覆盖策略。

## 输出示例

### init 命令输出

```
$ codexspec init

🚀 初始化 CodexSpec 项目配置...

✓ 创建 .codexspec/ 目录
✓ 创建 .claude/commands/codexspec/ 目录
✓ 安装 16 个命令模板
✓ 创建项目 CLAUDE.md

📁 已安装命令：

  核心命令 (9):
    /codexspec.constitution
    /codexspec.specify
    /codexspec.generate-spec
    /codexspec.spec-to-plan
    /codexspec.plan-to-tasks
    /codexspec.review-spec
    /codexspec.review-plan
    /codexspec.review-tasks
    /codexspec.implement-tasks

  增强命令 (4):
    /codexspec.clarify
    /codexspec.analyze
    /codexspec.checklist
    /codexspec.tasks-to-issues

  Git 工作流 (3):
    /codexspec.commit
    /codexspec.commit-staged
    /codexspec.pr

💡 下一步：
   1. 将 .claude/ 目录纳入 Git 管理：git add .claude/
   2. 查看所有命令：codexspec list-commands
   3. 开始使用：/codexspec.constitution

✅ 初始化完成！
```

### list-commands 命令输出

```
$ codexspec list-commands

CodexSpec 可用命令 (共 16 个)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 核心命令 (Core Commands)

  /codexspec.constitution
      创建或更新项目宪法，定义开发原则和规范

  /codexspec.specify
      通过交互式问答明确需求，探索"做什么"和"为什么"

  /codexspec.generate-spec
      从已明确的需求生成详细的 spec.md 规格文档

  ... (更多命令)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 增强命令 (Enhanced Commands)

  /codexspec.clarify
      在技术规划前提出澄清问题

  ... (更多命令)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔀 Git 工作流 (Git Workflow)

  /codexspec.commit
      生成符合 Conventional Commits 规范的提交信息

  ... (更多命令)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 提示：直接编辑 .claude/commands/codexspec/ 下的 .md 文件自定义命令
```

## 不在范围内

- **覆盖优先级机制**：不实现根目录命令覆盖子目录命令的优先级逻辑
- **命令版本锁定**：不提供锁定特定版本命令的功能
- **命令热更新**：不实现运行时自动检测和更新命令的功能
- **多 AI Agent 支持**：暂不支持 Claude Code 以外的 AI 工具
- **命令同步服务**：不提供云端同步命令配置的功能

## 依赖关系

- 依赖 Claude Code 的子目录命令识别能力（已验证可行）
- 依赖 Git 作为版本控制工具（推荐但非强制）

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 用户不熟悉 Git | 无法有效管理变更 | 提供清晰的文档和引导 |
| 迁移过程中断 | 数据丢失 | 迁移前备份，支持回滚 |
| Claude Code 子目录支持变化 | 功能失效 | 监控 Claude Code 更新，及时适配 |

## 时间线建议

- **Phase 1**：实现子目录结构和 `init` 增强
- **Phase 2**：实现迁移逻辑和 `list-commands` 命令
- **Phase 3**：更新文档和发布

---

*规格版本：1.0*
*创建日期：2026-03-02*
*基于需求澄清会话生成*

## 澄清记录

### 会话 2026-03-02

**Q1**: 边界情况 2（冲突的自定义命令）、3（Git 未初始化）、4（权限问题）是否需要在计划中明确处理？

**A1**:

- **边界 2（冲突）**：不存在冲突问题。旧结构文件优先移动到新位置，然后统一询问用户是否用模板覆盖，由用户决定。
- **边界 3（Git 未初始化）**：不需要特殊处理。询问用户是否覆盖时，用户自行结合是否使用 Git 来决定是否覆盖。
- **边界 4（权限问题）**：不需要特殊处理。无法写入时由 Python 抛出具体异常说明问题。

**影响**：移除边界 3、4，简化边界 2 的描述。降低实现复杂度。

---
