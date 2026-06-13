# 命令

这是 CodexSpec 斜杠命令的参考文档。这些命令在 Claude Code 的聊天界面中调用。

关于工作流程模式和何时使用每个命令，请参阅[工作流程](workflow.md)。关于 CLI 命令，请参阅 [CLI](../reference/cli.md)。

## 快速参考

| 命令 | 用途 |
|------|------|
| `/codexspec:constitution` | 创建或更新项目宪法，带有跨工件验证 |
| `/codexspec:specify` | 通过交互式问答澄清、确认并持久化需求 |
| `/codexspec:generate-spec` | 从澄清的需求生成 spec.md 文档 |
| `/codexspec:clarify` | 扫描现有规格说明中的歧义（迭代细化） |
| `/codexspec:spec-to-plan` | 将规格说明转换为技术实现方案 |
| `/codexspec:plan-to-tasks` | 将方案分解为可追踪、可验证的任务 |
| `/codexspec:implement-tasks` | 使用条件 TDD 工作流执行任务 |
| `/codexspec:review-spec` | 验证规格说明的完整性和质量 |
| `/codexspec:review-plan` | 审查技术方案的可行性和一致性 |
| `/codexspec:review-tasks` | 验证任务覆盖、顺序和可实施性 |
| `/codexspec:analyze` | 跨工件一致性分析（只读） |
| `/codexspec:checklist` | 生成需求质量检查清单 |
| `/codexspec:tasks-to-issues` | 将任务转换为 GitHub issues |
| `/codexspec:commit-staged` | 从暂存更改生成提交消息（含会话上下文感知） |

---

## 命令分类

### 核心工作流程命令

用于主要 SDD 工作流程的命令：项目原则 → 已确认需求 → 规格 → 方案 → 任务 → 实现。

### 审查命令（质量关卡）

在每个工作流程阶段验证工件的命令。缺陷必须有证据，可选设计建议单独报告。

### 高级命令

用于迭代细化、跨工件验证和项目管理集成的命令。

---

## 命令参考

### `/codexspec:constitution`

创建或更新项目宪法。宪法定义了指导所有后续开发决策的架构原则、技术栈、代码标准和治理规则。

**语法：**

```
/codexspec:constitution [原则描述]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `原则描述` | 否 | 要包含的原则描述（如未提供将提示输入） |

**功能：**

- 如果不存在则创建 `.codexspec/memory/constitution.md`
- 用新原则更新现有宪法
- 验证与模板的跨工件一致性
- 生成同步影响报告，显示更改和受影响的文件
- 包含依赖模板的合规性审查

**创建的文件：**

```
.codexspec/
└── memory/
    └── constitution.md    # 项目治理文档
```

**示例：**

```text
你: /codexspec:constitution 专注于代码质量、测试标准和整洁架构

AI:  正在创建宪法...

     ✓ 已创建 .codexspec/memory/constitution.md
     版本: 1.0.0

     同步影响报告:
     - plan-template-*.md: ✅ 已对齐
     - spec-template-*.md: ✅ 已对齐
     - tasks-template-*.md: ✅ 已对齐

     核心原则:
     1. 代码质量优先
     2. 测试驱动开发
     3. 整洁架构

     建议提交: docs: create constitution v1.0.0
```

**提示：**

- 在项目早期定义原则，确保决策一致
- 同时包含技术和流程原则
- 在重大功能开发前审查宪法
- 宪法更改会触发跨工件验证

---

### `/codexspec:specify`

通过交互式问答澄清需求、确认最终摘要，并将其持久化供后续会话使用。

**语法：**

```
/codexspec:specify [你的想法或需求]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `你的想法或需求` | 否 | 你想构建的内容的初始描述（如未提供将提示输入） |

**功能：**

- 提出澄清问题以理解你的想法
- 探索你可能没有考虑到的边界情况
- 通过对话共同创建高质量需求
- 关注"做什么"和"为什么"，而非技术实现
- 为已确认需求、约束、决策、排除项和开放问题分配稳定 ID
- 记录用户依据和确认日志
- 创建功能工作区和 `requirements.md`

**创建的文件：**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

只有已确认条目成为权威需求，开放问题保持明确的开放状态。

**示例：**

```text
你: /codexspec:specify 我想构建一个任务管理应用

AI:  好的！让我帮你澄清需求。

     首先，这个应用的目标用户是谁？
     - 个人专业人士
     - 小团队
     - 企业组织
     - 以上全部

你: 小团队，主要是软件开发团队

AI:  明白了。对于小型开发团队：
     - 需要实时协作功能吗？
     - 任务应该支持子任务还是仅支持扁平列表？
     - 有任何集成需求吗（GitHub、Slack 等）？

你: 实时很重要。子任务要。GitHub 集成就好了。

AI:  [继续探索需求...]

     澄清的需求摘要：
     - 目标：小型开发团队（5-20 人）
     - 核心：带子任务的任务、实时更新
     - 集成：GitHub（可选）
     - 优先级：实时协作 > 子任务 > GitHub

     准备好生成规格文档了吗？
     使用 /codexspec:generate-spec 创建 spec.md
```

**提示：**

- 用于初始需求探索
- 不必担心完整性——细化是迭代的
- 如果 AI 做出假设，请提问
- 在生成规格之前审查摘要

---

### `/codexspec:generate-spec`

从澄清的需求生成 `spec.md` 文档。此命令充当"需求编译器"，将你澄清的需求转换为结构化的规格说明。

**语法：**

```
/codexspec:generate-spec
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| 功能路径 | 否 | 明确的功能目录、`requirements.md` 或目标 `spec.md`；解析不唯一时必须提供 |

**功能：**

- 从选定功能工作区读取已确认需求
- 兼容仅包含 `spec.md` 的旧工作区，并明确提示无法追踪原始讨论
- 生成包含以下内容的综合 `spec.md`：
  - 功能概述和目标
  - 带验收标准的用户故事
  - 功能需求（REQ-XXX 格式）
  - 非功能需求（NFR-XXX 格式）
  - 边界情况及处理方法
  - 范围外项目
- 通过 `Sources` 引用需求 ID
- 权威来源冲突时停止并请求用户确认，不自行假设
- 自动审查，并最多进行两轮有证据支持的缺陷修复

**创建的文件：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**示例：**

```text
你: /codexspec:generate-spec

AI:  正在生成规格说明...

     ✓ 已创建 .codexspec/specs/2026-0613-1200ab-task-management/spec.md

     包含的部分：
     - 概述：小型开发团队的任务管理
     - 4 个带验收标准的用户故事
     - 12 个功能需求（REQ-001 到 REQ-012）
     - 3 个非功能需求（NFR-001 到 NFR-003）
     - 5 个记录的边界情况
     - 范围外：移动应用、企业 SSO

     下一步：
     - 使用 /codexspec:review-spec 审查规格
     - 或继续 /codexspec:spec-to-plan
```

**提示：**

- 在 `/codexspec:specify` 澄清需求后运行
- 在继续之前审查生成的规格
- 使用 `/codexspec:review-spec` 进行质量验证
- 如果需要微调，直接编辑 spec.md

---

### `/codexspec:clarify`

扫描现有规格说明中的歧义和缺口。在初始规格创建后用于迭代细化。

**语法：**

```
/codexspec:clarify [spec.md 路径]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `spec.md 路径` | 否 | 规格文件路径（如未提供则自动检测） |

**功能：**

- 使用聚焦的歧义类别扫描需求与规格
- 提出有针对性的澄清问题（最多 5 个）
- 用户确认后先更新 `requirements.md`，再同步 `spec.md`
- 如果可用，与 review-spec 发现集成

**歧义类别：**

| 类别 | 检测内容 |
|------|----------|
| **完整性缺口** | 缺失部分、空内容、缺少验收标准 |
| **具体性问题** | 模糊术语（"快速"、"可扩展"）、未定义的约束 |
| **行为清晰度** | 错误处理缺口、未定义的状态转换 |
| **可衡量性问题** | 没有指标的非功能需求 |

**示例：**

```text
你: /codexspec:clarify

AI:  正在扫描 spec.md 中的歧义...

     在 3 个类别中发现问题。

     ## 问题 1/5：具体性

     **上下文**：NFR-001 声明"系统应该快速响应"

     **问题**：目标响应时间是多少？

     | 选项 | 描述 | 影响 |
     |------|------|------|
     | A | 所有操作 < 100ms | 高性能要求 |
     | B | 读取 < 500ms，写入 < 1s | 平衡方法 |
     | 自定义 | 提供不同的答案 | - |

     **推荐**：选项 B - 适合典型 Web 应用

你: B

AI:  ✓ 已更新 NFR-001：响应时间 读取 < 500ms，写入 < 1s
     已添加到 spec.md 的澄清部分
```

**提示：**

- 当 spec.md 存在但需要细化时使用
- 与 `/codexspec:review-spec` 发现集成
- 每个会话最多 5 个问题
- 对于复杂规格说明可多次运行

---

### `/codexspec:spec-to-plan`

将功能规格说明转换为技术实现方案。这是你定义功能**如何**构建的地方。

**语法：**

```
/codexspec:spec-to-plan [spec.md 路径]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `spec.md 路径` | 否 | 规格文件路径（如未提供则从 `.codexspec/specs/` 自动检测） |

**功能：**

- 读取规格说明和宪法
- 仅包含确认需求和仓库约束所需要的技术细节
- 检查适用的项目原则，不把可选惯例提升为功能需求
- 通过 `Covers` 关联规格需求
- 记录技术决策及理由
- 决策会改变已确认意图时停止

**创建的文件：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── plan.md    # 技术实现方案
```

**示例：**

```text
你: /codexspec:spec-to-plan 使用 Python FastAPI 作为后端，React 作为前端，PostgreSQL 作为数据库

AI:  正在生成技术方案...

     合规性审查：
     ✓ 整洁架构：具有清晰边界的模块化设计
     ✓ TDD：在阶段中强制测试优先方法
     ✓ 代码质量：需要代码检查和类型提示

     架构：
     - 后端：FastAPI 分层架构
     - 前端：React 组件结构
     - 数据库：PostgreSQL 迁移策略

     模块依赖图：
     ┌─────────────┐
     │    API      │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │  Services   │
     └──────┬──────┘
            │
     ┌──────▼──────┐
     │    Data     │
     └─────────────┘

     ✓ 已创建 plan.md
     定义了 5 个实现阶段
```

**提示：**

- 在规格审查完成且稳定后运行
- 适用的项目原则必须遵守；与当前功能无关的模板惯例不构成要求
- 根据项目类型包含相关部分
- 在继续任务之前审查方案

---

### `/codexspec:plan-to-tasks`

将技术方案分解为具有明确覆盖关系和可验证结果的可执行任务。

**语法：**

```
/codexspec:plan-to-tasks [spec.md 路径 plan.md 路径]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `路径` | 否 | 规格和方案路径（如未提供则自动检测） |

**功能：**

- 创建具有单一可验证结果的任务；一个任务可以修改多个相关文件
- 仅在方案、项目原则、确认需求或风险要求时采用测试优先
- 仅为真正独立的任务标记 `[P]`
- 为每个任务指定精确的文件路径
- 通过 `Covers` 关联方案项与需求 ID

**创建的文件：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # 任务分解
```

**任务结构：**

```markdown
### Task 2.1: 编写实体 A 的测试 [P]
- **类型**: 测试
- **文件**: `tests/test_entity_a.py`
- **描述**: 为实体 A 编写单元测试
- **依赖**: Task 1.3
- **预估复杂度**: 低
```

**示例：**

```text
你: /codexspec:plan-to-tasks

AI:  正在将方案分解为任务...

     ✓ 已创建 tasks.md
     总计：24 个任务
     可并行化：8 个任务（33%）

     阶段 1：基础（4 个任务）
     阶段 2：核心实现 - TDD（10 个任务）
     阶段 3：集成（4 个任务）
     阶段 4：接口层（3 个任务）
     阶段 5：测试与文档（3 个任务）

     执行顺序：
     阶段 1 → [阶段 2 任务按并行组] → 阶段 3 → 阶段 4 → 阶段 5

     在每个阶段边界定义了检查点。
```

**提示：**

- 每个任务应产生一个可验证结果，并可修改紧密相关的多个文件
- 仅在要求测试优先时，测试任务才位于实现任务之前
- `[P]` 标记真正独立的可并行化任务
- 在实现之前审查依赖关系

---

### `/codexspec:implement-tasks`

使用条件 TDD 工作流执行实现任务。系统地完成任务列表。

**语法：**

```
/codexspec:implement-tasks [tasks 路径]
/codexspec:implement-tasks [spec 路径 plan 路径 tasks 路径]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `tasks 路径` | 否 | tasks.md 路径（如未提供则自动检测） |
| `spec 路径 plan 路径 tasks 路径` | 否 | 三个文档的显式路径 |

**文件解析：**

- **无参数**：从 `.codexspec/specs/` 自动检测
- **一个参数**：视为 `tasks.md` 路径，从同一目录推导其他文件
- **三个参数**：spec.md、plan.md 和 tasks.md 的显式路径

**功能：**

- 读取 tasks.md 并识别未完成任务
- 对代码任务应用 TDD 工作流：
  - **红**：先编写失败的测试
  - **绿**：实现以通过测试
  - **验证**：运行所有测试
  - **重构**：在保持测试通过的同时改进
- 对不可测试任务（文档、配置）直接实现
- 随着进展更新任务复选框
- 如果遇到阻塞，记录到 issues.md

**代码任务的 TDD 工作流：**

```
红 → 绿 → 验证 → 重构 → 标记完成
```

**不可测试任务的直接实现：**

- 文档文件
- 配置文件
- 静态资源
- 基础设施文件

**示例：**

```text
你: /codexspec:implement-tasks

AI:  开始实现...

     加载上下文：
     - spec.md ✓
     - plan.md ✓
     - tasks.md ✓
     - constitution.md ✓

     技术栈：Python 3.11+ / FastAPI / PostgreSQL / pytest

     正在处理任务 1.1：设置项目结构
     ✓ 已创建 src/taskman/__init__.py
     ✓ 已创建 pyproject.toml
     [x] 任务 1.1 完成

     正在处理任务 2.1：编写任务实体测试 [P]
     ✓ 已创建 tests/test_task.py
     运行测试... 5 通过（所有预期失败）
     [x] 任务 2.1 完成

     正在处理任务 2.2：实现任务实体
     ✓ 已创建 src/taskman/models/task.py
     运行测试... 5 通过
     [x] 任务 2.2 完成

     ...
```

**提示：**

- 如果中断可以从上次停止的地方恢复
- 阻塞问题记录在 issues.md 中
- 在重要任务/阶段后进行提交
- 先运行 `/codexspec:review-tasks` 进行验证

---

### `/codexspec:review-spec`

依据已确认需求及规格自身质量验证规格说明。

**语法：**

```
/codexspec:review-spec [spec.md 路径]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `spec.md 路径` | 否 | 规格文件路径（如未提供则自动检测） |

**功能：**

- 检查规格对 `requirements.md` 已确认条目的忠实性
- 检查内部一致性、清晰度和可验证性
- 只有权威内容确实需要时，缺少模板章节才构成缺陷
- 每个缺陷必须包含 `Evidence`、`Location`、`Mismatch`、`Impact` 和 `Remediation`
- 将“风险建议 / 设计机会”与缺陷分开
- 生成状态，以及由已分类缺陷推导的兼容分数

**统一审查契约：**

| 类别 | 含义 |
|------|------|
| 忠实性缺陷 | 与权威来源冲突或遗漏权威内容 |
| 内在缺陷 | 内部矛盾、不可实施或不可验证 |
| 建议项 | 没有当前缺陷证据的可选改进 |

状态为 `PASS`、`PASS_WITH_WARNINGS`、`NEEDS_REVISION` 或 `BLOCKED`。建议项不改变状态和分数。

**示例：**

```text
你: /codexspec:review-spec

AI:  总体状态：NEEDS_REVISION
     兼容分数：79/100

     警告 SPEC-001
     Evidence：CON-002 要求可衡量的响应时间限制。
     Location：spec.md，REQ-006
     Mismatch：“快速响应”没有可衡量阈值。
     Impact：无法验证验收结果。
     Remediation：请用户确认阈值，更新 requirements.md，再同步 REQ-006。

     风险建议 / 设计机会：
     - 无
```

**提示：**

- 在 `/codexspec:spec-to-plan` 之前运行
- `BLOCKED` 和 `NEEDS_REVISION` 状态下不要继续
- 不得将建议项提升为需求
- 修复后重新运行

---

### `/codexspec:review-plan`

审查技术方案的忠实性、可实施性和技术决策依据。

**语法：**

```
/codexspec:review-plan [plan.md 路径]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `plan.md 路径` | 否 | 方案文件路径（如未提供则自动检测） |

**功能：**

- 验证 `Covers` 关联和必须覆盖的规格需求
- 检查适用的项目原则和仓库事实
- 只有复杂度带来具体成本或冲突时才作为缺陷
- 每个缺陷必须给出证据字段，同一根因的发现应合并
- 将可选架构改进作为建议项报告
- 使用统一状态与兼容分数契约

**示例：**

```text
你: /codexspec:review-plan

AI:  总体状态：PASS
     兼容分数：100/100
     已验证缺陷：无

     风险建议 / 设计机会：
     - 如果生产测量超过确认的延迟目标，缓存层可能有用。
       当前方案不需要实现缓存。
```

**提示：**

- 在 `/codexspec:plan-to-tasks` 之前运行
- 生成任务前解决有证据支持的缺陷
- 将推测性的架构想法保留在建议区域
- 验证技术栈与团队技能一致

---

### `/codexspec:review-tasks`

验证任务分解的覆盖关系、可验证结果、正确顺序和可实施依赖。

**语法：**

```
/codexspec:review-tasks [tasks.md 路径]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `tasks.md 路径` | 否 | 任务文件路径（如未提供则自动检测） |

**功能：**

- 检查所有必须的方案项和需求都有任务覆盖
- 仅在权威来源要求时验证测试优先顺序
- 验证每个任务都有一个可检查结果
- 验证依赖（无循环、正确排序）
- 审查并行化标记
- 验证文件路径
- 每个缺陷都必须给出证据字段
- 将可选流程改进作为建议项报告
- 使用统一状态与兼容分数契约

**示例：**

```text
你: /codexspec:review-tasks

AI:  总体状态：NEEDS_REVISION
     兼容分数：79/100

     警告 TASK-001
     Evidence：任务 2.5 声明依赖任务 2.4。
     Location：tasks.md，任务 2.5
     Mismatch：任务 2.5 同时标记了 [P]。
     Impact：并行执行可能在前置任务完成前开始。
     Remediation：移除 [P]；如果方案能证明独立，则移除依赖。
```

**提示：**

- 在 `/codexspec:implement-tasks` 之前运行
- 只有权威来源要求测试时，测试顺序问题才构成缺陷
- 检查并行化标记准确
- 验证文件路径与项目结构匹配

---

### `/codexspec:analyze`

对 requirements.md、spec.md、plan.md 和 tasks.md 执行非破坏性一致性分析，识别权威冲突、追踪缺口、重复和覆盖遗漏。

**语法：**

```
/codexspec:analyze
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| 无 | - | 分析当前功能的工件 |

**功能：**

- 检测跨工件的重复
- 识别缺乏可衡量标准的歧义
- 发现规格不足的项
- 检查宪法一致性
- 映射需求覆盖到任务
- 报告术语和排序的不一致

**严重级别：**

| 级别 | 定义 |
|------|------|
| **CRITICAL** | 宪法违规、缺少核心工件、零覆盖 |
| **HIGH** | 重复/冲突需求、模糊的安全属性 |
| **MEDIUM** | 术语漂移、缺少非功能覆盖 |
| **LOW** | 风格/措辞改进 |

**示例：**

```text
你: /codexspec:analyze

AI:  正在分析工件...

     # 规格分析报告

     ## 覆盖摘要
     | 需求键 | 有任务? | 任务 ID |
     |--------|--------|---------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | 无 |

     ## 发现的问题

     | ID | 类别 | 严重性 | 摘要 |
     |----|------|--------|------|
     | A1 | 覆盖 | CRITICAL | REQ-003 无任务覆盖 |
     | A2 | 重复 | HIGH | REQ-005 和 REQ-008 重叠 |
     | A3 | 歧义 | MEDIUM | NFR-002 "安全"未定义 |

     ## 指标
     - 总需求数：12
     - 总任务数：24
     - 覆盖率：92%（11/12 需求）
     - 关键问题：1

     ## 下一步操作
     1. 为 REQ-003 添加任务（CRITICAL）
     2. 考虑合并 REQ-005 和 REQ-008
     3. 在 NFR-002 中定义"安全"

     在 /codexspec:implement-tasks 之前解决 CRITICAL 问题
```

**提示：**

- 在 `/codexspec:plan-to-tasks` 之后、实现之前运行
- CRITICAL 问题应该阻止实现
- 只读分析——不修改文件
- 使用发现来改进工件质量

---

### `/codexspec:checklist`

生成用于验证需求完整性、清晰度和一致性的质量检查清单。这些是"需求编写的单元测试"。

**语法：**

```
/codexspec:checklist [聚焦领域]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `聚焦领域` | 否 | 领域聚焦（如 "ux"、"api"、"security"、"performance"） |

**功能：**

- 生成按质量维度组织的检查清单
- 在 `FEATURE_DIR/checklists/` 目录创建检查清单
- 项目聚焦于需求质量，而非实现测试

**质量维度：**

- **需求完整性**：是否所有必要需求都存在？
- **需求清晰度**：需求是否具体且无歧义？
- **需求一致性**：需求是否一致无冲突？
- **验收标准质量**：成功标准是否可衡量？
- **场景覆盖**：是否所有流程/用例都已覆盖？
- **边界情况覆盖**：边界条件是否已定义？
- **非功能需求**：性能、安全、可访问性是否已指定？
- **依赖与假设**：是否已文档化？

**示例检查清单类型：**

- `ux.md` - 视觉层次、交互状态、可访问性
- `api.md` - 错误格式、速率限制、认证
- `security.md` - 数据保护、威胁模型、泄露响应
- `performance.md` - 指标、负载条件、降级

**示例：**

```text
你: /codexspec:checklist security

AI:  正在生成安全检查清单...

     ✓ 已创建 .codexspec/specs/2026-0613-1200ab-task-management/checklists/security.md

     ## 安全需求质量检查清单

     ### 认证需求
     - [ ] CHK001 - 是否为所有受保护端点定义了认证需求？ [完整性]
     - [ ] CHK002 - 密码复杂度是否明确指定？ [清晰度]
     - [ ] CHK003 - 会话超时需求是否量化？ [可衡量性]

     ### 数据保护
     - [ ] CHK004 - 静态数据加密需求是否指定？ [完整性]
     - [ ] CHK005 - 传输中数据加密需求是否指定？ [完整性]
     - [ ] CHK006 - PII 处理是否明确文档化？ [清晰度]

     总计：4 个类别中的 15 个项目
```

**提示：**

- 检查清单验证需求质量，而非实现正确性
- 用于需求审查和改进
- 为聚焦验证创建领域特定检查清单
- 在进入技术规划之前运行

---

### `/codexspec:tasks-to-issues`

将 `tasks.md` 中的任务转换为 GitHub issues，用于项目跟踪和协作。

**语法：**

```
/codexspec:tasks-to-issues
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| 无 | - | 转换当前功能的所有任务 |

**功能：**

- 解析任务 ID、描述、依赖和文件路径
- 创建带结构化正文的 GitHub issues
- 根据任务类型添加标签（setup、implementation、testing、documentation）
- 在 issues 之间链接依赖
- 报告创建的 issues 及 URL

**前提条件：**

- 带有 GitHub 远程的 Git 仓库
- GitHub CLI（`gh`）已安装并认证
- `tasks.md` 文件存在

**示例：**

```text
你: /codexspec:tasks-to-issues

AI:  正在将任务转换为 GitHub issues...

     仓库：github.com/example/taskman

     创建 issues：
     ✓ #42: Task 1.1 - 设置项目结构 (setup)
     ✓ #43: Task 2.1 - 编写任务实体测试 (testing)
     ✓ #44: Task 2.2 - 实现任务实体 (implementation)
     ...

     摘要：
     - 已创建 issues：24
     - 已应用标签：setup(4), implementation(12), testing(5), documentation(3)
     - 已链接依赖：18

     查看 issues：https://github.com/example/taskman/issues
```

**提示：**

- 需要 GitHub CLI 认证（`gh auth login`）
- 仅适用于 GitHub 仓库
- 在仓库的默认配置中创建 issues
- 运行前检查重复

---

### `/codexspec:commit-staged`

基于暂存的 git 更改生成符合 Conventional Commits 的提交消息，并具有会话上下文感知能力。此命令理解你的开发会话以生成有意义的提交消息。

**语法：**

```
/codexspec:commit-staged [-p]
```

**参数：**

| 参数 | 必需 | 描述 |
|------|------|------|
| `-p` | 否 | 预览模式 - 仅显示消息而不提交 |

**功能：**

- 执行 `git diff --staged` 获取暂存的更改
- 分析更改和会话上下文以理解意图
- 遵循 Conventional Commits 规范
- 执行模式（默认）：生成消息后直接提交
- 预览模式（`-p`）：仅显示消息而不提交
- 如果没有暂存更改则报告错误

**示例：**

```text
你: /codexspec:commit-staged

AI:  正在分析暂存的更改...

     已暂存的文件：
     - src/auth/service.py
     - tests/test_auth.py

     生成的提交消息：
     feat(auth): 实现令牌刷新逻辑

     - 添加刷新令牌生成
     - 包含令牌过期处理
     - 添加刷新流程的测试

     正在执行提交...

     ✓ 已提交：def5678
```

**预览模式示例：**

```text
你: /codexspec:commit-staged -p

AI:  预览模式 - 不会执行提交

     建议的提交消息：
     feat(auth): 实现令牌刷新逻辑

     - 添加刷新令牌生成
     - 包含令牌过期处理
     - 添加刷新流程的测试
```

**提示：**

- 先使用 `git add` 暂存更改
- 仅分析暂存的内容 - 尊重 Git 的两阶段提交流程
- 考虑会话上下文以生成有意义的提交消息
- 使用 `-p` 标志在提交前预览
- 默认遵循 Conventional Commits 规范

---

## 工作流程概览

```text
想法
  -> specify -> requirements.md
  -> generate-spec -> spec.md -> review-spec
  -> spec-to-plan -> plan.md -> review-plan
  -> plan-to-tasks -> tasks.md -> review-tasks
  -> analyze -> implement-tasks
```

每次审查都是人工检查点，使用有证据支持的发现验证忠实性与内在质量。可选改进保持为建议项，不阻止流程继续。

---

## 故障排除

### "找不到功能目录"

命令无法定位功能目录。

**解决方案：**

- 先运行 `codexspec init` 初始化项目
- 检查 `.codexspec/specs/` 目录是否存在
- 确认你在正确的项目目录中
- 存在多个候选功能时，传入明确的功能目录或产物路径

### "找不到 spec.md"

规格文件尚不存在。

**解决方案：**

- 先运行 `/codexspec:specify` 澄清需求
- 然后运行 `/codexspec:generate-spec` 创建 spec.md

### "找不到宪法"

不存在项目宪法。

**解决方案：**

- 运行 `/codexspec:constitution` 创建一个
- 宪法是可选的，但建议用于一致的决策

### "找不到任务文件"

任务分解不存在。

**解决方案：**

- 确保你已先运行 `/codexspec:spec-to-plan`
- 然后运行 `/codexspec:plan-to-tasks` 创建 tasks.md

### "GitHub CLI 未认证"

`/codexspec:tasks-to-issues` 命令需要 GitHub 认证。

**解决方案：**

- 安装 GitHub CLI：`brew install gh`（macOS）或等效命令
- 认证：`gh auth login`
- 验证：`gh auth status`

---

## 下一步

- [工作流程](workflow.md) - 常见模式和何时使用每个命令
- [CLI](../reference/cli.md) - 用于项目初始化的终端命令
