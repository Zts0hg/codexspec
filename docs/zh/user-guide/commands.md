# 命令

这是 CodexSpec 斜杠命令的参考文档。这些命令在 Claude Code 的聊天界面中调用。

关于工作流模式以及何时使用每个命令，请参阅[工作流](workflow.md)。关于 CLI 命令，请参阅 [CLI](../reference/cli.md)。

## 快速参考

按类别分组，与 README 中的目录一致。每一组内命令按工作流顺序排列。

### 核心工作流命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:constitution` | 创建或更新项目宪法，带跨工件校验 |
| `/codexspec:specify` | 澄清、确认需求并持久化到 `requirements.md` |
| `/codexspec:generate-spec` | 从已澄清的需求生成 `spec.md` 文档（★ 自动评审） |
| `/codexspec:spec-to-plan` | 将规格转换为技术实现计划（★ 自动评审） |
| `/codexspec:plan-to-tasks` | 将计划拆解为可追溯、可验证的任务（★ 自动评审） |
| `/codexspec:implement-tasks` | 使用条件 TDD 工作流执行任务 |

### 评审命令（质量关卡）

| 命令 | 用途 |
|---------|---------|
| `/codexspec:review-spec` | 校验规格的完整性与质量 |
| `/codexspec:review-plan` | 评审技术计划的可行性与对齐情况 |
| `/codexspec:review-tasks` | 校验任务的覆盖、顺序与可行性 |

### 增强命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:config` | 交互式管理项目配置（创建/查看/修改/重置） |
| `/codexspec:clarify` | 扫描已有规格中的歧义（4 个类别，最多 5 个问题） |
| `/codexspec:analyze` | 跨工件一致性分析（只读，按严重级别分类） |
| `/codexspec:checklist` | 生成需求质量检查清单 |
| `/codexspec:tasks-to-issues` | 把任务转换为 GitHub Issues |

### Git 工作流命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:commit-staged` | 从暂存改动生成提交信息（感知会话上下文） |
| `/codexspec:pr` | 从 git diff 生成 PR/MR 描述（自动识别平台） |

### 代码评审命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:review-code` | 变更范围缺陷门禁；路径质量评分请使用 `--audit` |
| `/codexspec:review-python-code` | 评审 Python 代码（PEP 8、类型安全、健壮性、宪法一致性） |
| `/codexspec:review-react-code` | 评审 React/TypeScript 代码（组件架构、Hooks 规范、状态、性能） |

### 快速通道

| 命令 | 用途 |
|---------|---------|
| `/codexspec:quick` | 为小型改动运行精简的 Requirements-First SDD 流程 |

---

## 命令分类

### 核心工作流命令

用于主要 Requirements-First SDD 工作流的命令：宪法 → 已确认需求 → 规格 → 计划 → 任务 → 实现。在这里，已确认的需求拥有最高优先级的特性权威——在确认门处显式确认之前，链路中的任何内容都不具约束力。

### 评审命令（质量关卡）

在每个工作流阶段对工件进行校验的命令，遵循**基于证据的评审**契约：每个缺陷都必须给出具体的 `Evidence`、`Location`、`Mismatch`、`Impact` 与 `Remediation`。建议性的设计意见单独报告，既不改变状态也不触发自动改动。已核实的缺陷最多可修复并再审两轮；建议项始终可选。

### 增强命令

用于迭代细化、跨工件校验、配置以及项目管理集成的命令。

### Git 工作流命令

把已完成的工作转化为可分享工件的命令：从暂存 diff 生成提交信息，从分支 diff 生成结构化的 PR/MR 描述。

### 代码评审命令

评审源代码（任意语言、Python 专属、React/TypeScript 专属）以检查地道表达、正确性、健壮性、架构以及宪法一致性。发现沿用与工件评审相同的严重级别纪律：CRITICAL/HIGH 问题必须给出具体证据；LOW 建议仅供参考。

### 快速通道

一条针对规模小、边界清晰的改动，端到端运行 Requirements-First SDD 流程的精简命令。

---

## 命令参考

### `/codexspec:constitution`

创建或更新项目宪法。宪法界定架构原则、技术栈、代码标准与治理规则，用以指导后续所有开发决策。

**语法：**

```
/codexspec:constitution [原则描述]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `原则描述` | 否 | 要纳入的原则描述（未提供时会提示输入） |

**功能：**

- 若 `.codexspec/memory/constitution.md` 不存在则创建
- 用新原则更新已有宪法
- 校验与模板的跨工件一致性
- 生成同步影响报告，列出改动及受影响的文件
- 对依赖模板进行合宪性评审

**生成的文件：**

```
.codexspec/
└── memory/
    └── constitution.md    # 项目治理文档
```

**示例：**

```text
你: /codexspec:constitution 聚焦代码质量、测试标准与整洁架构

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

- 在项目早期就定义原则，确保后续决策一致
- 既包含技术原则，也包含流程原则
- 在重大功能开发前评审宪法
- 宪法变更会触发跨工件校验

---

### `/codexspec:specify`

通过交互式 Q&A 澄清需求、确认最终摘要，并将其持久化供后续会话使用。

**语法：**

```
/codexspec:specify [你的想法或需求]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `你的想法或需求` | 否 | 想构建内容的初始描述（未提供时会提示输入） |

**功能：**

- 通过提问澄清你的想法
- 探索你或许没考虑到的边界情况
- 通过对话共同打磨出高质量需求
- 关注"做什么"与"为什么"，而非技术实现
- 为已确认的需求、约束、决策、排除项与开放问题分配稳定 ID
- 记录用户依据与一份确认日志
- 创建功能工作区与 `requirements.md`

**生成的文件：**

```text
.codexspec/specs/{feature-id}-{feature-name}/requirements.md
```

只有已确认的条目才会成为权威需求；开放问题始终保持显式的开放状态。这就是针对需求的确认门：在你显式确认最终摘要之前，任何内容都不具约束力。

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
     - 任务要支持子任务还是只用扁平列表？
     - 有任何集成需求吗（GitHub、Slack 等）？

你: 实时很重要。子任务要。GitHub 集成就好了。

AI:  [继续探索需求...]

     已澄清的需求摘要：
     - 目标：小型开发团队（5-20 人）
     - 核心：带子任务的任务、实时更新
     - 集成：GitHub（可选）
     - 优先级：实时协作 > 子任务 > GitHub

     准备好生成规格文档了吗？
     用 /codexspec:generate-spec 创建 spec.md
```

**提示：**

- 用于初始需求探索
- 不必担心一开始就面面俱到——细化是迭代的
- 如果 AI 做出假设，主动提问
- 在生成规格之前先评审摘要

---

### `/codexspec:generate-spec`

从已澄清的需求生成 `spec.md` 文档。这条命令相当于一台"需求编译器"，把已澄清的需求转换为结构化的规格。

**语法：**

```
/codexspec:generate-spec
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| 功能路径 | 否 | 显式的功能目录、`requirements.md` 或目标 `spec.md`；当解析存在歧义时必须提供 |

**功能：**

- 从所选功能工作区读取已确认需求
- 兼容仅含 `spec.md` 的旧工作区，并给出显式的可追溯性警告
- 生成内容详尽的 `spec.md`，包括：
  - 功能概述与目标
  - 带验收标准的用户故事
  - 功能需求（REQ-XXX 格式）
  - 非功能需求（NFR-XXX 格式）
  - 边界情况及其处理方式
  - 范围外项目
- 通过 `Sources` 引用回需求 ID
- 权威来源冲突时停下请求用户确认，而不是擅自假设
- 自动评审，并最多修复两轮有证据支持的缺陷

**生成的文件：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── spec.md
```

**示例：**

```text
你: /codexspec:generate-spec

AI:  正在生成规格...

     ✓ 已创建 .codexspec/specs/2026-0613-1200ab-task-management/spec.md

     包含的章节：
     - 概述：面向小型开发团队的任务管理
     - 4 个带验收标准的用户故事
     - 12 个功能需求（REQ-001 到 REQ-012）
     - 3 个非功能需求（NFR-001 到 NFR-003）
     - 5 个记录的边界情况
     - 范围外：移动应用、企业 SSO

     下一步：
     - 用 /codexspec:review-spec 评审规格
     - 或继续 /codexspec:spec-to-plan
```

**提示：**

- 在 `/codexspec:specify` 澄清需求后运行
- 继续之前先评审生成的规格
- 用 `/codexspec:review-spec` 做质量校验
- 如需微调可直接编辑 spec.md

---

### `/codexspec:clarify`

扫描已有规格中的歧义与缺口。用于初始规格创建后的迭代细化。

**语法：**

```
/codexspec:clarify [path_to_spec.md]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path_to_spec.md` | 否 | 规格文件路径（未提供时自动检测） |

**功能：**

- 用聚焦的歧义类别扫描需求与规格
- 提出有针对性的澄清问题（最多 5 个）
- 用户确认后先更新 `requirements.md`，再同步 `spec.md`
- 如可用，与 review-spec 的发现整合

**歧义类别：**

| 类别 | 检测内容 |
|----------|-----------------|
| **完整性缺口** | 缺失章节、空白内容、缺少验收标准 |
| **具体性问题** | 模糊措辞（"快速"、"可扩展"）、未定义的约束 |
| **行为清晰度** | 错误处理缺口、未定义的状态转换 |
| **可衡量性问题** | 缺少指标的非功能需求 |

**示例：**

```text
你: /codexspec:clarify

AI:  正在扫描 spec.md 中的歧义...

     在 3 个类别中发现问题。

     ## 问题 1/5：具体性

     **上下文**：NFR-001 写道"系统应快速响应"

     **问题**：目标响应时间是多少？

     | 选项 | 描述 | 影响 |
     |--------|-------------|--------|
     | A | 所有操作 < 100ms | 高性能要求 |
     | B | 读取 < 500ms，写入 < 1s | 平衡方案 |
     | 自定义 | 提供不同答案 | - |

     **推荐**：选项 B——适合典型 Web 应用

你: B

AI:  ✓ 已更新 NFR-001：响应时间 读取 < 500ms，写入 < 1s
     已添加到 spec.md 的 Clarifications 章节
```

**提示：**

- 当 spec.md 已存在但需要细化时使用
- 与 `/codexspec:review-spec` 的发现整合
- 每个会话最多 5 个问题
- 对复杂规格可多次运行

---

### `/codexspec:spec-to-plan`

把功能规格转换为技术实现计划。这一步决定功能**如何**构建。

**语法：**

```
/codexspec:spec-to-plan [path_to_spec.md]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path_to_spec.md` | 否 | 规格文件路径（未提供时从 `.codexspec/specs/` 自动检测） |

**功能：**

- 读取规格与宪法
- 仅纳入已确认需求与仓库约束真正需要的技术细节
- 检查适用的宪法规则，但不把可选惯例当成功能需求
- 通过 `Covers` 关联回规格需求
- 记录技术决策及其理由
- 当某个决策会改动已确认意图时停下

**生成的文件：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── plan.md    # 技术实现计划
```

**示例：**

```text
你: /codexspec:spec-to-plan 后端用 Python FastAPI，前端用 React，数据库用 PostgreSQL

AI:  正在生成技术计划...

     合宪性评审：
     ✓ 整洁架构：边界清晰的模块化设计
     ✓ TDD：在相应阶段强制测试先行
     ✓ 代码质量：要求 lint 与类型注解

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

- 在规格评审通过并稳定后运行
- 适用的宪法规则必须遵守；无关的模板惯例不构成要求
- 按项目类型纳入相关章节
- 进入任务之前先评审计划

---

### `/codexspec:plan-to-tasks`

把技术计划拆解为可执行任务，每个任务都有显式的覆盖关系与可验证的结果。

**语法：**

```
/codexspec:plan-to-tasks [path_to_spec.md path_to_plan.md]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `路径` | 否 | 规格与计划的路径（未提供时自动检测） |

**功能：**

- 创建具备单一可验证结果的任务；一个任务可以触及多个相关文件
- 仅在计划、宪法、已确认需求或风险要求时才采用测试先行
- 仅在任务真正独立时才标记 `[P]`
- 为每个任务指定精确的文件路径
- 通过 `Covers` 关联回计划与需求 ID

**生成的文件：**

```
.codexspec/
└── specs/
    └── 2026-0613-1200ab-task-management/
        └── tasks.md    # 任务拆解
```

**任务结构：**

```markdown
### Task 2.1: 编写实体 A 的测试 [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: 为实体 A 编写单元测试
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**示例：**

```text
你: /codexspec:plan-to-tasks

AI:  正在将计划拆解为任务...

     ✓ 已创建 tasks.md
     总计：24 个任务
     可并行：8 个任务（33%）

     阶段 1：基础（4 个任务）
     阶段 2：核心实现 - TDD（10 个任务）
     阶段 3：集成（4 个任务）
     阶段 4：接口层（3 个任务）
     阶段 5：测试与文档（3 个任务）

     执行顺序：
     阶段 1 → [阶段 2 任务按并行分组] → 阶段 3 → 阶段 4 → 阶段 5

     在每个阶段边界都定义了检查点。
```

**提示：**

- 每个任务应产出一个可验证的结果，并可能触及紧密相关的多个文件
- 仅在要求测试先行时，测试任务才排在实现之前
- `[P]` 标记真正独立、可并行的任务
- 实现前先评审依赖关系

---

### `/codexspec:implement-tasks`

用条件 TDD 工作流执行实现任务，系统地走完任务列表。

**语法：**

```
/codexspec:implement-tasks [tasks_path]
/codexspec:implement-tasks [spec_path plan_path tasks_path]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `tasks_path` | 否 | tasks.md 的路径（未提供时自动检测） |
| `spec_path plan_path tasks_path` | 否 | 三份文档的显式路径 |

**文件解析：**

- **无参数**：从 `.codexspec/specs/` 自动检测
- **一个参数**：当作 `tasks.md` 路径，其余从同目录推导
- **三个参数**：spec.md、plan.md、tasks.md 的显式路径

**功能：**

- 读取 tasks.md 并识别未完成任务
- 对代码任务应用 TDD 工作流：
  - **Red**：先写失败的测试
  - **Green**：实现以通过测试
  - **Verify**：运行所有测试
  - **Refactor**：在不破坏测试的前提下改进
- 对不可测任务（文档、配置）直接实现
- 随进展更新任务复选框
- 遇到阻塞时记录到 issues.md

**代码任务的 TDD 工作流：**

```
Red → Green → Verify → Refactor → 标记完成
```

**不可测任务的直接实现：**

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

     处理任务 1.1：搭建项目结构
     ✓ 已创建 src/taskman/__init__.py
     ✓ 已创建 pyproject.toml
     [x] 任务 1.1 完成

     处理任务 2.1：编写任务实体测试 [P]
     ✓ 已创建 tests/test_task.py
     运行测试... 5 通过（均为预期失败）
     [x] 任务 2.1 完成

     处理任务 2.2：实现任务实体
     ✓ 已创建 src/taskman/models/task.py
     运行测试... 5 通过
     [x] 任务 2.2 完成

     ...
```

**提示：**

- 中断后可以从上次停下的位置恢复
- 阻塞问题记录在 issues.md
- 在重要任务/阶段后会提交
- 先运行 `/codexspec:review-tasks` 做校验

---

### `/codexspec:review-spec`

依据已确认的需求以及规格自身的内在质量对规格进行校验。

**语法：**

```
/codexspec:review-spec [path_to_spec.md]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path_to_spec.md` | 否 | 规格文件路径（未提供时自动检测） |

**功能：**

- 检查规格对 `requirements.md` 已确认条目的忠实度
- 检查内部一致性、清晰度与可验证性
- 仅当权威内容确实需要时，缺少模板章节才计为缺陷
- 每个缺陷必须给出 `Evidence`、`Location`、`Mismatch`、`Impact` 与 `Remediation`
- 把 `Risk Advisories / Design Opportunities` 与缺陷分开
- 生成状态以及由已分类发现推导出的兼容性分数

**共享的评审契约：**

| 类别 | 含义 |
|----------|---------|
| 忠实性缺陷 | 与权威来源冲突或遗漏必须覆盖的权威内容 |
| 内在缺陷 | 内部自相矛盾、不可实施或不可验证 |
| 建议项 | 没有当前缺陷证据的可选改进 |

状态为 `PASS`、`PASS_WITH_WARNINGS`、`NEEDS_REVISION` 或 `BLOCKED`。建议项不改变状态与分数。

**示例：**

```text
你: /codexspec:review-spec

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning SPEC-001
     Evidence: CON-002 要求一个可衡量的响应时间上限。
     Location: spec.md, REQ-006
     Mismatch: "快速响应"没有可衡量的阈值。
     Impact: 验收结果无法验证。
     Remediation: 请用户确认阈值，更新 requirements.md，再同步 REQ-006。

     Risk Advisories / Design Opportunities:
     - None
```

**提示：**

- 在 `/codexspec:spec-to-plan` 之前运行
- 把 `BLOCKED` 与 `NEEDS_REVISION` 视为尚未就绪
- 不要把建议项提升为需求
- 修复后重新运行

---

### `/codexspec:review-plan`

评审技术实现计划的忠实度、可行性，以及技术决策是否有依据。

**语法：**

```
/codexspec:review-plan [path_to_plan.md]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path_to_plan.md` | 否 | 计划文件路径（未提供时自动检测） |

**功能：**

- 校验 `Covers` 链接与必须覆盖的规格需求
- 检查适用的宪法规则与仓库事实
- 仅当复杂度带来具体成本或冲突时才将其标为缺陷
- 每个缺陷都必须给出证据字段，根因相同的发现会被合并
- 把可选的架构改进作为建议项报告
- 使用共享的状态与兼容性分数契约

**示例：**

```text
你: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - 如果生产测量超过已确认的延迟目标，缓存层可能有用。
       当前计划并不要求实现它。
```

**提示：**

- 在 `/codexspec:plan-to-tasks` 之前运行
- 生成任务前先解决有证据支持的缺陷
- 推测性的架构想法留在建议区域
- 校验技术栈与团队技能相匹配

---

### `/codexspec:review-tasks`

校验任务拆解的覆盖关系、可验证结果、正确顺序与可行依赖。

**语法：**

```
/codexspec:review-tasks [path_to_tasks.md]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path_to_tasks.md` | 否 | 任务文件路径（未提供时自动检测） |

**功能：**

- 检查所有必须的计划项与需求都有任务覆盖
- 仅在权威来源要求时校验测试先行顺序
- 验证每个任务都有一个可检查的结果
- 验证依赖（无环、顺序正确）
- 评审并行化标记
- 校验文件路径
- 每个缺陷必须给出证据字段
- 把可选的流程改进作为建议项报告
- 使用共享的状态与兼容性分数契约

**示例：**

```text
你: /codexspec:review-tasks

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning TASK-001
     Evidence: 任务 2.5 声明依赖任务 2.4。
     Location: tasks.md, 任务 2.5
     Mismatch: 任务 2.5 同时标记了 [P]。
     Impact: 并行执行可能在前置完成前就开始。
     Remediation: 移除 [P]；若计划能证明独立则移除依赖。
```

**提示：**

- 在 `/codexspec:implement-tasks` 之前运行
- 只有在权威来源要求测试时，测试顺序问题才算缺陷
- 检查并行化标记是否准确
- 校验文件路径与项目结构相符

---

### `/codexspec:analyze`

对 requirements.md、spec.md、plan.md 与 tasks.md 执行非破坏性的一致性分析，识别权威冲突、可追溯缺口、重复以及覆盖遗漏。

**语法：**

```
/codexspec:analyze
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| 无 | - | 分析当前功能的工件 |

**功能：**

- 检测跨工件的重复
- 识别缺乏可衡量标准的歧义
- 发现规格不足的条目
- 检查宪法对齐
- 把需求覆盖映射到任务
- 报告术语与顺序上的不一致

**严重级别：**

| 级别 | 定义 |
|-------|------------|
| **CRITICAL** | 宪法违规、缺失核心工件、零覆盖 |
| **HIGH** | 重复/冲突的需求、模糊的安全属性 |
| **MEDIUM** | 术语漂移、缺失非功能覆盖 |
| **LOW** | 风格/措辞改进 |

**示例：**

```text
你: /codexspec:analyze

AI:  正在分析工件...

     # Specification Analysis Report

     ## Coverage Summary
     | Requirement Key | Has Task? | Task IDs |
     |-----------------|-----------|----------|
     | REQ-001 | ✅ | 2.1, 2.2 |
     | REQ-002 | ✅ | 2.3, 2.4 |
     | REQ-003 | ❌ | None |

     ## Issues Found

     | ID | Category | Severity | Summary |
     |----|----------|----------|---------|
     | A1 | Coverage | CRITICAL | REQ-003 无任务覆盖 |
     | A2 | Duplication | HIGH | REQ-005 与 REQ-008 重叠 |
     | A3 | Ambiguity | MEDIUM | NFR-002 "secure" 未定义 |

     ## Metrics
     - Total Requirements: 12
     - Total Tasks: 24
     - Coverage: 92% (11/12 requirements)
     - Critical Issues: 1

     ## Next Actions
     1. 为 REQ-003 补充任务 (CRITICAL)
     2. 考虑合并 REQ-005 与 REQ-008
     3. 在 NFR-002 中定义 "secure"

     在 /codexspec:implement-tasks 之前解决 CRITICAL 问题
```

**提示：**

- 在 `/codexspec:plan-to-tasks` 之后、实现之前运行
- CRITICAL 问题应阻断实现
- 只读分析——不修改任何文件
- 用发现来提升工件质量

---

### `/codexspec:checklist`

生成质量检查清单，用于校验需求的完整性、清晰度与一致性。这些是"针对需求写作的单元测试"。

**语法：**

```
/codexspec:checklist [focus_area]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `focus_area` | 否 | 领域聚焦（如 "ux"、"api"、"security"、"performance"） |

**功能：**

- 生成按质量维度组织的检查清单
- 在 `FEATURE_DIR/checklists/` 目录下创建清单
- 条目聚焦于需求质量，而非实现测试

**质量维度：**

- **需求完整性**：是否所有必要需求都已列出？
- **需求清晰度**：需求是否具体且无歧义？
- **需求一致性**：需求之间是否对齐、无冲突？
- **验收标准质量**：成功标准是否可衡量？
- **场景覆盖**：是否覆盖了所有流程/用例？
- **边界情况覆盖**：边界条件是否已定义？
- **非功能需求**：性能、安全、可访问性是否已写明？
- **依赖与假设**：是否已文档化？

**清单类型示例：**

- `ux.md` - 视觉层次、交互状态、可访问性
- `api.md` - 错误格式、速率限制、认证
- `security.md` - 数据保护、威胁模型、泄露响应
- `performance.md` - 指标、负载条件、降级表现

**示例：**

```text
你: /codexspec:checklist security

AI:  正在生成安全清单...

     ✓ 已创建 .codexspec/specs/2026-0613-1200ab-task-management/checklists/security.md

     ## Security Requirements Quality Checklist

     ### Authentication Requirements
     - [ ] CHK001 - 是否为所有受保护端点都定义了认证需求？ [Completeness]
     - [ ] CHK002 - 是否显式指定了密码复杂度？ [Clarity]
     - [ ] CHK003 - 是否量化了会话超时需求？ [Measurability]

     ### Data Protection
     - [ ] CHK004 - 是否写明了静态数据加密需求？ [Completeness]
     - [ ] CHK005 - 是否写明了传输中数据加密需求？ [Completeness]
     - [ ] CHK006 - PII 处理是否已显式文档化？ [Clarity]

     Total: 15 items across 4 categories
```

**提示：**

- 清单校验的是需求质量，而非实现正确性
- 用于需求评审与改进
- 创建领域专属清单做聚焦校验
- 在进入技术规划前运行

---

### `/codexspec:tasks-to-issues`

把 `tasks.md` 中的任务转换为 GitHub issues，用于项目跟踪与协作。

**语法：**

```
/codexspec:tasks-to-issues
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| 无 | - | 转换当前功能的全部任务 |

**功能：**

- 解析任务 ID、描述、依赖与文件路径
- 创建带结构化正文的 GitHub issues
- 按任务类型打标签（setup、implementation、testing、documentation）
- 在 issues 之间链接依赖
- 报告创建的 issues 及其 URL

**前提条件：**

- 配置了 GitHub 远程的 Git 仓库
- 已安装并完成认证的 GitHub CLI（`gh`）
- `tasks.md` 文件存在

**示例：**

```text
你: /codexspec:tasks-to-issues

AI:  正在将任务转换为 GitHub issues...

     Repository: github.com/example/taskman

     Creating issues:
     ✓ #42: Task 1.1 - 搭建项目结构 (setup)
     ✓ #43: Task 2.1 - 编写任务实体测试 (testing)
     ✓ #44: Task 2.2 - 实现任务实体 (implementation)
     ...

     Summary:
     - Issues created: 24
     - Labels applied: setup(4), implementation(12), testing(5), documentation(3)
     - Dependencies linked: 18

     View issues: https://github.com/example/taskman/issues
```

**提示：**

- 需要已认证的 GitHub CLI（`gh auth login`）
- 仅适用于 GitHub 仓库
- 在仓库的默认配置下创建 issues
- 运行前先检查重复

---

### `/codexspec:commit-staged`

基于暂存的 git 改动生成符合 Conventional Commits 的提交信息，并感知会话上下文。这条命令理解你的开发会话，从而生成有意义的提交信息。

**语法：**

```
/codexspec:commit-staged [-p]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `-p` | 否 | 预览模式——只显示信息不提交 |

**功能：**

- 执行 `git diff --staged` 获取暂存改动
- 分析改动与会话上下文以理解意图
- 遵循 Conventional Commits 规范
- 执行模式（默认）：生成信息后直接提交
- 预览模式（`-p`）：只显示信息不提交
- 若没有暂存改动则报错

**示例：**

```text
你: /codexspec:commit-staged

AI:  正在分析暂存的改动...

     Files staged:
     - src/auth/service.py
     - tests/test_auth.py

     Generated commit message:
     feat(auth): 实现令牌刷新逻辑

     - 新增刷新令牌的生成
     - 处理令牌过期
     - 为刷新流程补充测试

     正在执行提交...

     ✓ Committed: def5678
```

**预览模式示例：**

```text
你: /codexspec:commit-staged -p

AI:  预览模式 - 不会执行提交

     Suggested commit message:
     feat(auth): 实现令牌刷新逻辑

     - 新增刷新令牌的生成
     - 处理令牌过期
     - 为刷新流程补充测试
```

**提示：**

- 先用 `git add` 暂存改动
- 只分析已暂存的内容——尊重 Git 的两阶段提交工作流
- 综合会话上下文以生成有意义的提交信息
- 用 `-p` 标志在提交前预览
- 默认遵循 Conventional Commits 规范

---

### `/codexspec:review-code`

将选定的 Git 变更作为合并前的严格缺陷门禁进行审查。默认目标包含完整特性差异；显式选择器可审查已提交、未提交或单个提交的证据，但不接受路径过滤。

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**下一版本的破坏性变更：**

- 默认命令现在是变更范围缺陷门禁，不再是宽泛的质量评分审计。
- 不再接受位置路径参数。需要按路径执行建议性质的质量评分时，请显式使用 `--audit`。

**缺陷门禁语法：**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
```

门禁会清点目标中的全部工件，评估适用需求，并执行 Scope、Behavior、Risk 和 Verification 四个阶段。结果只能是 `PASS`、`FAIL` 或 `INCONCLUSIVE`。六个报告段落之后会附带一个机器可读的 `<review-code-result>` envelope。任何 P0-P3 缺陷都会得到 `FAIL`；缺少强制证据时得到 `INCONCLUSIVE`。

```text
你: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — 必需的审查与验证全部完成，且没有发现缺陷。
```

<!-- REVIEW-CODE-AUDIT -->

#### 路径质量审计

显式 audit 分支按路径检查当前文件的完整内容，评估地道表达、正确性、健壮性、架构和宪法对齐情况。该评分仅供参考，不能作为 `implement-tasks` 的完成门禁。

**语法：**

```
/codexspec:review-code --audit [paths...]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path...` | 否 | 一个或多个待评审的源文件或目录（空格分隔）。省略时默认为 `src/` |

**功能：**

- 按文件扩展名识别主语言，并对混合语言目标按语言分别跑一遍
- 当存在静态分析工具的配置时运行它们（`ruff`/`mypy`、`eslint`/`tsc`、`go vet`/`gofmt`、`cargo check`/`cargo clippy`、`shellcheck`）；否则优雅跳过并报告覆盖降级
- 为四个维度打分：地道表达与简洁、正确性与显式契约、运行时健壮性与资源纪律、架构与设计完整性
- 为检测到的框架注入必检子节（例如 React 的 Hooks Compliance、Rust 的 Ownership & Borrowing、Go 的 Goroutine & Context Discipline、C/C++ 的 Memory & Lifetime Safety、Shell 的 Execution Safety）
- 当存在 `.codexspec/memory/constitution.md` 时与之交叉对照；不存在时则丢弃宪法轴并重新分配其权重
- 按严重级别归类发现：CRITICAL、HIGH、MEDIUM、LOW（LOW 建议最多扣 5 分）

**示例：**

```text
你: /codexspec:review-code --audit src/

AI:  # Code Review Report

     ## Summary
     - Overall Status: Needs Work
     - Quality Score: 78/100
     - Detected Language: Python

     ## Static Analysis Results
     | Tool   | Status | Issues | Details                |
     |--------|--------|--------|------------------------|
     | ruff   | Warn   | 3      | 未用导入、行长超限 |
     | mypy   | Pass   | 0      | 无类型错误            |

     ## Detailed Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/auth/service.py:42 - 裸 `except Exception:` 吞掉了原始原因
       Impact: 调试时原始错误上下文丢失。
       Suggestion: 收窄异常并用 `raise ... from err` 重新抛出。

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/auth/service.py:120 - 用手写循环的地方其实可以用推导式

     ## Recommendations
     1. Priority 1: 合并前修复 CODE-001。
     2. Priority 2: 视情况采纳 LOW 建议。
```

**提示：**

- 传入多个路径以聚焦评审某个切片，例如 `src/ tests/`
- 分数仅供参考；CRITICAL/HIGH 才是可操作的信号
- 对纯 Python 或纯 React 项目，优先使用专门的 `/codexspec:review-python-code` 或 `/codexspec:review-react-code`，可获得更深度的语言专属检查
- 修复后重跑，确认分数回升（CRITICAL/HIGH 解决后期望 ≥ 95）

---

### `/codexspec:review-python-code`

评审 Python 代码的 PEP 8 合规性、类型安全、工程健壮性，以及宪法一致性。

**语法：**

```
/codexspec:review-python-code [path...]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path...` | 否 | 一个或多个待评审的 Python 文件或目录（空格分隔）。省略时默认为 `src/` |

**功能：**

- 运行 `ruff check` 取得 PEP 8 / lint 结果，运行 `mypy` 取得类型检查结果
- 评审四个 Python 专属维度：Pythonic 与 KISS 原则、类型安全与显式性、工程健壮性、宪法对齐
- 检查类型注解完整性、宽泛异常处理，以及 `raise ... from err` 上下文保留
- 校验资源管理（`with` 上下文管理器）、async/await 正确性，以及结构化 `logging` 纪律
- 当存在 `.codexspec/memory/constitution.md` 时，对照其 MUST/SHOULD 原则交叉检查
- 按严重级别归类发现：CRITICAL（宪法 MUST 违规、逻辑 bug、安全漏洞）、HIGH（类型安全缺口、ruff/mypy 错误、资源泄漏）、MEDIUM（设计/重构机会、缺失注解）、LOW（可读性、Pythonic 用法）

**示例：**

```text
你: /codexspec:review-python-code src/codexspec/

AI:  # Python Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | ruff  | Pass   | 0      |
     | mypy  | Pass   | 0      |

     ## Findings
     ### Warnings (HIGH)
     - [ ] [CODE-002] src/codexspec/__init__.py:218 - 公开函数缺少返回类型注解
       Suggestion: 加上返回类型并用 mypy 校验。

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/codexspec/cli.py:140 - 用 `pathlib.Path` 替代 `os.path` 字符串拼接
```

**提示：**

- 当目标是纯 Python 且需要 PEP 8 / 类型安全的深度时，用它替代 `/codexspec:review-code`
- 要获得完整覆盖，目标项目必须安装并配置好 `ruff` 与 `mypy`；缺失时命令会报告覆盖降级
- 宪法的 MUST 原则参与打分；没有宪法时则应用语言无关的元原则（可测试性、简洁性）

---

### `/codexspec:review-react-code`

评审 React/TypeScript 代码的组件架构、Hooks 规范、状态管理、性能，以及宪法一致性。

**语法：**

```
/codexspec:review-react-code [path...]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `path...` | 否 | 一个或多个待评审的 React/TypeScript 文件或目录（空格分隔；接受 `.tsx`、`.ts`、`.jsx`、`.js`）。省略时默认为 `src/` |

**功能：**

- 当存在 ESLint 配置时运行 `npx eslint`，当存在 `tsconfig.json` 时运行 `npx tsc --noEmit`
- 评审四个 React 专属维度：组件原子性与单一职责、Hooks 合规与副作用管理、状态管理与数据流、性能与健壮性
- 校验 `useEffect` 依赖数组是否完备，检测把派生数据当作 state 的误用，并标出不必要的影响
- 检查闭包陈旧风险、缺失的 effect 清理、prop 透传、未 memo 的高昂渲染，以及缺失的 loading/error 状态
- 当存在 `.codexspec/memory/constitution.md` 时与之交叉对照
- 按严重级别归类发现：CRITICAL（违反 Hooks 规则、竞态条件）、HIGH（缺失清理、未处理的 promise 拒绝）、MEDIUM（重构候选）、LOW（可读性）

**示例：**

```text
你: /codexspec:review-react-code src/components/

AI:  # React Code Review Report

     ## Static Analysis
     | Tool  | Status | Issues |
     |-------|--------|--------|
     | eslint| Warn   | 2      |
     | tsc   | Pass   | 0      |

     ## Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/components/UserProfile.tsx:38 - `useEffect` 依赖数组缺少 `userId`
       Impact: 闭包陈旧，导航后会取到错误的用户。
       Suggestion: 把 `userId` 加入依赖数组，或抽成自定义 hook。

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/components/Button.tsx:12 - 改用推导值而非 `useState`
```

**提示：**

- 当目标是纯 React/TypeScript 且需要 Hooks / 组件架构深度时，用它替代 `/codexspec:review-code`
- 要获得完整覆盖，应同时具备 ESLint 与 `tsconfig.json`；缺失时命令会报告覆盖降级
- React 的发现叠加在基础 TypeScript 检查之上，因此类型安全问题仍会被报告

---

### `/codexspec:quick`

为小型改动运行精简的 Requirements-First SDD 流程。

**语法：**

```
/codexspec:quick [描述一个小需求]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `描述一个小需求` | 否 | 对这条规模小、边界清晰的改动的简短描述（未提供时会提示输入） |

**功能：**

- 评估范围（触及的文件、模块跨度、新增依赖、未决的产品决策）；若改动很广或包含多个独立结果，则建议改用标准流程
- 用与 `/codexspec:specify` 相同的时间戳约定创建功能工作区与 `requirements.md`
- 只解决会实质改变实现的歧义；呈现精简的已确认摘要（`NEED-*`、相关的 `CON-*`/`DEC-*`、`OUT-*`、未解决的 `OPEN-*`）
- 停在确认门：在你确认摘要之前不会生成任何内容
- 在新建的功能目录上链式调用生成命令：`/codexspec:generate-spec`、`/codexspec:spec-to-plan`、`/codexspec:plan-to-tasks`、`/codexspec:implement-tasks`
- 把评审交给各生成命令自带的自动评审闭环；若某次评审需要新的产品或架构决策，则暂停并向用户提问
- 分别报告功能目录、工件路径、评审结果、实现验证情况，以及未决的建议项

**生成的文件：**

```text
.codexspec/specs/{timestamp}-{feature-name}/
├── requirements.md
├── spec.md
├── plan.md
└── tasks.md
```

**示例：**

```text
你: /codexspec:quick 给登录表单加一个"记住我"复选框

AI:  范围检查：1 个组件、1 个表单字段、无新依赖。Quick 适用。

     Confirmed requirements:
     - NEED-1: 登录表单上的"记住我"复选框（默认不勾选）
     - DEC-1: 仅在勾选时才持久化一个长效刷新令牌
     OUT-1: SSO / 社交登录（保持不变）

     确认此摘要以启动自动化流程。[y/N]

你: y

AI:  运行 generate-spec → spec-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ 所有评审为 PASS_WITH_WARNINGS 或更高
     ✓ 实现已验证
     Open advisories: none
```

**提示：**

- 把 Quick 留给真正小型、单一结果的改动；否则运行 `/codexspec:specify` 走标准流程
- 仍需确认——Quick 绝不为了让自动化继续推进而替你推断产品决策
- 若任一生成评审返回 `NEEDS_REVISION`/`BLOCKED`，Quick 会停下并把控制权交还给你

---

### `/codexspec:pr`

从 git diff 生成结构化的 GitHub Pull Request / GitLab Merge Request 描述。可选地集成 `spec.md` 以提供 SDD 可追溯的上下文。

**语法：**

```
/codexspec:pr [--target-branch <branch>] [--sections <list>] [--spec <id-or-path>] [--output <file>]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `--target-branch <branch>` | 否 | 用于对比的目标分支（默认：`origin/main`） |
| `--sections <list>` | 否 | 逗号分隔的 `summary, changes, testing, verify, checklist, notes` 子集（默认：`all`） |
| `--spec <id-or-path>` | 否 | 可选的 spec 集成：在 `.codexspec/specs/` 下解析的功能 id（如 `2025-0321-1430k7-auth`），或显式的 `path/to/spec.md`。省略则仅依据 git 生成 |
| `--output <file>` | 否 | 把描述保存到文件而不是终端 |

**功能：**

- 对照目标分支收集 git 上下文（当前分支、远程 URL、领先的 commits、文件改动、完整 diff、commit 信息）
- 从远程 URL 自动识别平台：GitHub → "Pull Request"，GitLab → "Merge Request"，其他/无 → 默认采用 GitHub 术语并给出警告
- 当存在 `.codexspec/memory/constitution.md` 时加载，并按文档/代码评审标准对齐描述
- 按 `language.commit`（其次 `language.output`、再次英文）决定描述语言；技术术语（API、JWT、PR、MR）在合适时保留英文
- 提供 `--spec` 时，会加入从 spec.md 提取的用户故事与需求构成的 Context 章节；否则纯粹依据 diff 生成
- 按 `--sections` 产出对应章节（Summary、Changes、Testing、Verification Steps、Pre-merge Checklist、Notes / Breaking Changes）

**示例：**

```text
你: /codexspec:pr --spec 2026-0613-1200ab-task-management

AI:  正在生成 Pull Request 描述...

     Platform: GitHub (github.com/example/taskman)
     Branch:   feature/task-management  →  origin/main
     Commits:  8 ahead

     ## Pull Request: 面向小型开发团队的任务管理

     ### Context
     - 取自 spec.md 的用户故事与 REQ-*

     ### Summary
     - 新增任务 CRUD、子任务与实时更新

     ### Changes
     - src/taskman/models/task.py (new)
     - src/taskman/api/tasks.py (new)
     - ...

     ### Verification Steps
     1. `uv run pytest`
     2. `uv run codexspec check`
```

**提示：**

- 对于没有正式规格的小修复或改动，跳过 `--spec`
- 与 `/codexspec:commit-staged` 配合，可基于同一份工作同时产出提交信息与 PR 描述
- 这条命令的端到端实战案例（包括 spec.md 上下文如何接入）见 [PR 描述生成器案例研究](../case-studies/case-study-pr-description-generator.md)

---

### `/codexspec:config`

交互式管理项目配置（创建/查看/修改/重置）。这是 `codexspec config` CLI 的斜杠命令等价物，适合插件市场安装的用户。

**语法：**

```
/codexspec:config [--view]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `--view` | 否 | 只读显示当前配置。不带任何参数则打开交互式管理菜单 |

**功能：**

- 仅针对 `.codexspec/config.yml`
- `--view`（或菜单中的 "View current config"）以可读格式打印该文件；不存在时报告 "Configuration Not Found"
- 当配置存在时，交互模式提供：查看、修改、重置为默认、取消
- 若配置不存在，则走创建流程，写入一份仅含 `output` 的最小配置（interaction/document/commit 回退到 `output`，再到 `en`，因此仅含 `output` 的文件完全可用）
- 让你独立设置每个语言维度（output、interaction、document、commit），并可切换 `auto_next` 等工作流选项

**创建/编辑的文件：**

```
.codexspec/config.yml
```

**示例：**

```text
你: /codexspec:config

AI:  ## Configuration Manager

     在 .codexspec/config.yml 找到配置文件。
     你想做什么？
     - View current config
     - Modify config
     - Reset to defaults
     - Cancel

你: Modify config

AI:  选择要更改的维度：
     - Output language (base)
     - Interaction language
     - Document language
     - Commit-message language
     - workflow.auto_next

你: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction 与 document 会回退到 output，再到 en。)
```

**提示：**

- 改动前先用 `/codexspec:config --view` 查看当前状态
- 全新或重置后的配置只写入 `output`；仅当 interaction/document 应当与 output 不同时才显式设置
- 终端里的脚本化修改请优先使用 `codexspec config` CLI（`--set-lang`、`--set-interaction-lang`、`--set-document-lang`、`--set-commit-lang`、`--auto-next`）

---

## 工作流概览

```text
想法 → /specify → requirements.md → /generate-spec → spec.md → /spec-to-plan → plan.md → /plan-to-tasks → tasks.md → /implement
                                                  │                          │                           │
                                             评审 spec                   评审 plan                    评审 tasks
```

每次评审都是一个人工检查点，用有证据支持的发现校验忠实度与内在质量。可选的设计建议始终单独处理，从不阻断推进。已核实的缺陷最多可修复并再审两轮。

---

## 故障排除

### "Feature directory not found"

命令找不到功能目录。

**解决方案：**

- 先运行 `codexspec init` 初始化项目
- 检查 `.codexspec/specs/` 目录是否存在
- 确认你处于正确的项目目录
- 当存在多个候选时，传入显式的功能目录或工件路径

### "No spec.md found"

规格文件尚不存在。

**解决方案：**

- 先运行 `/codexspec:specify` 澄清需求
- 然后运行 `/codexspec:generate-spec` 创建 spec.md

### "Constitution not found"

尚不存在项目宪法。

**解决方案：**

- 运行 `/codexspec:constitution` 创建一份
- 宪法是可选的，但为了一致的决策建议使用

### "Tasks file not found"

任务拆解尚不存在。

**解决方案：**

- 确保先运行过 `/codexspec:spec-to-plan`
- 然后运行 `/codexspec:plan-to-tasks` 创建 tasks.md

### "GitHub CLI not authenticated"

`/codexspec:tasks-to-issues` 命令需要 GitHub 认证。

**解决方案：**

- 安装 GitHub CLI：`brew install gh`（macOS）或等效命令
- 认证：`gh auth login`
- 验证：`gh auth status`

---

## 下一步

- [工作流](workflow.md) - 常见模式与何时使用各条命令
- [CLI](../reference/cli.md) - 用于项目初始化的终端命令
