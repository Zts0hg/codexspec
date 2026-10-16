<a id="available-commands"></a>

# 可用命令

CLI 提供六个公共命令；助手集成提供 28 个命令，Claude 中使用 `/codexspec:<name>`，Codex 中使用 `$codexspec:<name>`。为便于阅读，下表统一使用 Claude 的调用方式。

<a id="cli-commands"></a>

## CLI 命令

| 命令 | 用途 |
|---------|---------|
| `codexspec init` | 为 Claude、Codex 或两者初始化或刷新项目 |
| `codexspec check` | 检查已安装的工具和依赖 |
| `codexspec version` | 显示版本和系统信息 |
| `codexspec config` | 查看或修改项目配置 |
| `codexspec list-commands` | 按类别列出可用智能体命令 |
| `codexspec show-blueprint` | 显示共享工作区中的蓝图，不作修改 |

<a id="core-workflow-commands"></a>

## 核心工作流命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:constitution` | 创建/更新项目原则，并进行跨产物验证 |
| `/codexspec:specify` | 讨论、确认并持久保存功能需求 |
| `/codexspec:blueprint` | 准备或维护已确认的待处理蓝图需求 |
| `/codexspec:generate-spec` | 根据已确认需求编写可追溯的规格文档，并自动审查 |
| `/codexspec:spec-to-design` | 定义架构、组件、接口和决策；自动审查 |
| `/codexspec:design-to-plan` | 规划实现阶段、顺序和验证；自动审查 |
| `/codexspec:plan-to-tasks` | 生成覆盖上游要求的可验证任务，并自动审查和分析 |
| `/codexspec:implement-tasks` | 执行任务、验证结果、审查并修复 |
| `/codexspec:auto-dev` | 按文档顺序自主开发已确认的蓝图需求 |

<a id="artifact-review-commands"></a>

## 产物审查命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:review-spec` | 检查规格忠实度和内部质量 |
| `/codexspec:review-design` | 检查设计是否符合规格、是否可行，以及能否据此制定计划 |
| `/codexspec:review-plan` | 检查计划是否符合设计、是否可行，以及能否据此开始实现 |
| `/codexspec:review-tasks` | 检查任务忠实度、依赖、可执行性和验证 |

<a id="requirements-existing-code-and-debugging"></a>

## 需求、既有代码与调试

| 命令 | 用途 |
|---------|---------|
| `/codexspec:clarify` | 解决需求歧义，先更新需求，再更新规格 |
| `/codexspec:analyze` | 检查整个开发链路是否可追溯，并让下游文档符合上游依据 |
| `/codexspec:checklist` | 生成需求质量检查清单 |
| `/codexspec:tasks-to-issues` | 将已有任务转为可操作的 GitHub issues |
| `/codexspec:debug` | 调查根因后再修复 |
| `/codexspec:reverse-spec` | 概览现有架构、生成模块草案，或报告相对于基线的偏差 |

<a id="project-knowledge-commands"></a>

## 项目知识命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:distill` | 提炼可复用知识，或在本地界面中审阅候选记录 |
| `/codexspec:evolve` | 将已认可的知识整理为向上游贡献的草案 |
| `/codexspec:onboard` | 初始化候选惯例和有证据支持的约束 |

<a id="git-and-code-review-commands"></a>

## Git 与代码审查命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:commit-staged` | 根据暂存变更生成信息；预览或执行获授权的提交 |
| `/codexspec:pr` | 生成结构化 PR/MR 描述 |
| `/codexspec:release-notes` | 维护 changelog 条目，并生成发布正文 |
| `/codexspec:review-code` | 以缺陷门禁审查所选变更；使用 `--audit` 评估路径质量 |

<a id="utility-commands"></a>

## 实用命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:config` | 交互式创建/查看/修改/重置项目配置 |
| `/codexspec:quick` | 为小型变更运行简明的需求优先 SDD 工作流 |

旧的 Python／React 审查入口是插件兼容工件，不属于初始化安装的 28 个命令。请使用 `review-code`，它会按需加载语言与框架标准；评估指定路径时使用 `--audit`。

## 命令参考

### `/codexspec:constitution`

创建或更新项目宪法。宪法界定架构原则、技术栈、代码标准与治理规则，用以指导后续所有开发决策。

**语法：**

```
/codexspec:constitution [principles description]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `principles description` | 否 | 要纳入的原则描述（未提供时会提示输入） |

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
    └── constitution.md    # Project governance document
```

**示例：**

```text
You: /codexspec:constitution Focus on code quality, testing standards, and clean architecture

AI:  Creating constitution...

     ✓ Created .codexspec/memory/constitution.md
     Version: 1.0.0

     Sync Impact Report:
     - plan-template-*.md: ✅ aligned
     - spec-template-*.md: ✅ aligned
     - tasks-template-*.md: ✅ aligned

     Core Principles:
     1. Code Quality First
     2. Test-Driven Development
     3. Clean Architecture

     Suggested commit: docs: create constitution v1.0.0
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
/codexspec:specify [your idea or requirement]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `your idea or requirement` | 否 | 想构建内容的初始描述（未提供时会提示输入） |

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
You: /codexspec:specify I want to build a task management app

AI:  Great! Let me help you clarify the requirements.

     First, who are the target users for this app?
     - Individual professionals
     - Small teams
     - Enterprise organizations
     - All of the above

You: Small teams, mainly software development teams

AI:  Got it. For small dev teams:
     - Do you need real-time collaboration features?
     - Should tasks support sub-tasks or just flat lists?
     - Any integration requirements (GitHub, Slack, etc.)?

You: Real-time is important. Sub-tasks yes. GitHub integration would be nice.

AI:  [Continues exploring requirements...]

     Summary of clarified requirements:
     - Target: Small dev teams (5-20 people)
     - Core: Tasks with sub-tasks, real-time updates
     - Integration: GitHub (optional)
     - Priority: Real-time collaboration > Sub-tasks > GitHub

     Ready to generate the spec document?
     Use /codexspec:generate-spec to create spec.md
```

**提示：**

- 用于初始需求探索
- 不必担心一开始就面面俱到——细化是迭代的
- 如果 AI 做出假设，主动提问
- 在生成规格之前先评审摘要

---

### `/codexspec:blueprint`

如果希望先把多条需求讨论并确认，再逐项开发，可以用 `blueprint` 整理需求，用 `auto-dev` 推进这组需求的开发：

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

需求进入开发队列前，蓝图讨论会先明确需要由用户决定的方向、方案选择和约束。共享蓝图 `.codexspec/blueprint.md` 使用 `pending`、`in_progress` 和 `completed` 标记状态。待处理需求可以追加、替换、删除或调整顺序；正在开发和已完成的条目只允许查看，不能通过蓝图维护操作修改。

Auto-dev 按蓝图中的顺序开发需求。如果已有功能正在进行，会先接着完成它，再开始下一个。每完成一项，都会重新读取队列，因此运行期间新追加的待处理需求也能接着开发。整个过程在已确认的需求范围内完成 SDD 各阶段、实现、验证、审查和修复。调用 `auto-dev` 本身就会启用这一自动化流程，不受 `workflow.auto_next` 控制，也不会修改该设置。

这两个命令共用 `codexspec/auto-dev` 分支和 `worktree-for-codexspec-auto-dev` 工作区。它们可以同时运行，由共享机制协调工作区的使用并保护写入操作；需求开发则仍在该工作区内按顺序进行。自主执行中若遇到无法依据已确认需求作出的产品决定，会停止运行并说明依据，而不会在正常执行过程中发起询问。

只读查看当前共享蓝图：

```bash
codexspec show-blueprint
```

---

### `/codexspec:generate-spec`

根据已确认需求编写可追溯的规格文档，并自动审查。

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
You: /codexspec:generate-spec

AI:  Generating specification...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/spec.md

     Sections included:
     - Overview: Task management for small dev teams
     - 4 User Stories with acceptance criteria
     - 12 Functional Requirements (REQ-001 to REQ-012)
     - 3 Non-Functional Requirements (NFR-001 to NFR-003)
     - 5 Edge Cases documented
     - Out of Scope: Mobile apps, Enterprise SSO

     Next steps:
     - Review the spec with /codexspec:review-spec
     - Or proceed to /codexspec:spec-to-design
```

---

### `/codexspec:spec-to-design`

读取已确认的 `requirements.md`、`spec.md`、项目原则和相关仓库事实，生成 `design.md`，说明组件、接口、数据流、备选方案和设计决策，并关联上游需求。生成后自动运行 `review-design`。如果设计选择会改变已确认的意图，或需要用户作出新决定，就暂停推进。

```text
/codexspec:spec-to-design <feature-dir>
```

---

### `/codexspec:design-to-plan`

将已确认的设计转换为实现计划。先运行 `spec-to-design`，确定架构、组件、接口和技术选型。

```text
/codexspec:design-to-plan [design.md | spec.md | feature-directory]
```

读取 `requirements.md`、`spec.md`、`design.md` 和项目宪法，规划实现阶段、顺序与验证方式；引用设计，不重新设计系统。每个计划组件标注 `Covers: REQ-xxx; Design: <design component>`。

生成 `plan.md` 并运行 `review-plan`。启用 `auto_next` 时，评审通过后进入 `plan-to-tasks`。改变已确认意图的决策需要用户确认。优先使用显式路径，其次匹配当前功能分支；无法唯一确定功能时要求选择。缺少 `design.md` 的旧功能仍保留从 `spec.md` 规划的原有行为。

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
| `paths` | 否 | 规格与计划的路径（未提供时自动检测） |

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
        └── tasks.md    # Task breakdown
```

**任务结构：**

```markdown
### Task 2.1: Write Tests for Entity A [P]
- **Type**: Testing
- **Files**: `tests/test_entity_a.py`
- **Description**: Write unit tests for Entity A
- **Dependencies**: Task 1.3
- **Est. Complexity**: Low
```

**示例：**

```text
You: /codexspec:plan-to-tasks

AI:  Breaking down plan into tasks...

     ✓ Created tasks.md
     Total: 24 tasks
     Parallelizable: 8 tasks (33%)

     Phase 1: Foundation (4 tasks)
     Phase 2: Core Implementation - TDD (10 tasks)
     Phase 3: Integration (4 tasks)
     Phase 4: Interface Layer (3 tasks)
     Phase 5: Testing & Documentation (3 tasks)

     Execution Order:
     Phase 1 → [Phase 2 tasks in parallel groups] → Phase 3 → Phase 4 → Phase 5

     Checkpoints defined at each phase boundary.
```

**提示：**

- 每个任务应产出一个可验证的结果，并可能触及紧密相关的多个文件
- 仅在要求测试先行时，测试任务才排在实现之前
- `[P]` 标记真正独立、可并行的任务
- 实现前先评审依赖关系

任务生成后运行 `review-tasks`。结果为 `PASS` 或 `PASS_WITH_WARNINGS` 时，运行一次 `analyze`；分析不会增加完成门禁。任务覆盖范围包括已确认需求、规格、设计和计划。

---

### `/codexspec:implement-tasks`

执行任务、验证结果、审查并修复.

```text
/codexspec:implement-tasks <feature-dir>
```

`review-spec`、`review-design`、`review-plan` 和 `review-tasks` 这四个文档审查命令，会检查文档是否忠于上游依据、覆盖是否完整、方案是否可行，以及文档自身的质量。生成文档后会自动审查，也可以手动调用。报告会区分已经验证的缺陷、不会阻止流程继续的风险建议和可改进的设计，并给出兼容性评分。

`review-code` 提供独立的代码缺陷门禁，审查范围由所选变更决定；也可以明确选择对完整代码进行质量评估：

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

默认审查会检查功能分支上的全部变更，包括已提交、已暂存、未暂存，以及未被忽略的未跟踪内容。也可以明确限定为已提交变更、尚未提交的变更，或某一次提交。`--feature` 用于提供功能需求背景，不会缩小 Git 变更范围。`--audit` 则评估指定路径的代码质量，给出建议性评分，不作出功能是否完成的判定。

审查会从 `.codexspec/review-code/` 读取共享标准，并选择与当前行为、语言和框架有关的检查项。每个问题都必须说明具体证据、触发条件、为何由所选变更引入，以及会造成什么影响。审查者只报告缺陷和有依据的维护建议，不修改文件；负责修复的工作流还需独立核实这些问题。

实现代码任务时，先写测试再实现；文档和配置任务则直接修改，并进行相应检查。修复后的增量审查可以复用未受影响部分的已有检查结果。最终验收仍须重新审查整个功能并得到 `PASS`，完成全部覆盖与验证，且没有尚未解决的已纳入 P0–P3 缺陷。有依据的维护建议另行报告。

`workflow.auto_maintenance` 默认为 **true**，用于控制修复工作流是否一并实施已经验证、且与现有要求兼容的维护改进。关闭后仍会报告这些建议，也仍需修复缺陷、完成必要检查。该设置与阶段自动推进相互独立，不是 `implement-tasks` 的命令参数。

需要先查明根因再修复时，可以使用：

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug 先调查问题，再对照已有模式分析原因，验证一个明确假设，最后编写能复现问题的失败测试并修复。在实现阶段，如果修复迟迟没有进展、需要追查较复杂的正确性问题，或多轮审查反复发现同一类根因，就会转入这一调试流程。三次修复失败后，必须重新评估架构。

使用 `checklist` 评估需求清晰度、完整性和一致性：

```text
/codexspec:checklist Check the authentication requirements for completeness
```

如何选择审查范围、传入参数以及执行详细流程，见[命令参考](commands.md)。

---

### `/codexspec:auto-dev`

按文档顺序自主开发已确认的蓝图需求.

参见 [`blueprint`](#codexspecblueprint).

```text
/codexspec:auto-dev
```

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
You: /codexspec:review-spec

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning SPEC-001
     Evidence: CON-002 requires a measurable response-time limit.
     Location: spec.md, REQ-006
     Mismatch: "Respond quickly" has no measurable threshold.
     Impact: Acceptance cannot be verified.
     Remediation: Ask the user to confirm a threshold, update requirements.md,
                  then synchronize REQ-006.

     Risk Advisories / Design Opportunities:
     - None
```

**提示：**

- 在 `/codexspec:spec-to-design` 之前运行
- 把 `BLOCKED` 与 `NEEDS_REVISION` 视为尚未就绪
- 不要把建议项提升为需求
- 修复后重新运行

---

### `/codexspec:review-design`

对照已确认需求与规格，检查 `design.md` 是否忠实、可行，以及是否已具备进入计划阶段的条件。报告应区分有证据支持的缺陷与可选的设计改进，并沿用其他工件审查的状态与有限修复规则。

```text
/codexspec:review-design <feature-dir>
```

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
You: /codexspec:review-plan

AI:  Overall Status: PASS
     Compatibility Score: 100/100
     Verified defects: none

     Risk Advisories / Design Opportunities:
     - A caching layer may become useful if production measurements exceed
       the confirmed latency target. It is not required by the current plan.
```

**提示：**

- 在 `/codexspec:plan-to-tasks` 之前运行
- 生成任务前先解决有证据支持的缺陷
- 推测性的架构想法留在建议区域
- 校验技术栈与团队技能相匹配

计划用于落实已确认的 `design.md`，不会重新决定架构方案。审查既检查需求覆盖，也检查计划对设计的引用是否正确。

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
You: /codexspec:review-tasks

AI:  Overall Status: NEEDS_REVISION
     Compatibility Score: 79/100

     Warning TASK-001
     Evidence: Task 2.5 declares a dependency on Task 2.4.
     Location: tasks.md, Task 2.5
     Mismatch: Task 2.5 is also marked [P].
     Impact: Parallel execution can start before its prerequisite completes.
     Remediation: Remove [P] or remove the dependency if the plan proves independence.
```

**提示：**

- 在 `/codexspec:implement-tasks` 之前运行
- 只有在权威来源要求测试时，测试顺序问题才算缺陷
- 检查并行化标记是否准确
- 校验文件路径与项目结构相符

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
You: /codexspec:clarify

AI:  Scanning spec.md for ambiguities...

     Found issues in 3 categories.

     ## Question 1/5: Specificity

     **Context**: NFR-001 states "System should respond quickly"

     **Question**: What is the target response time?

     | Option | Description | Impact |
     |--------|-------------|--------|
     | A | < 100ms for all operations | High performance requirement |
     | B | < 500ms for reads, < 1s for writes | Balanced approach |
     | Custom | Provide a different answer | - |

     **Recommendation**: Option B - balanced for typical web app

You: B

AI:  ✓ Updated NFR-001: Response time < 500ms reads, < 1s writes
     Added to Clarifications section in spec.md
```

**提示：**

- 当 spec.md 已存在但需要细化时使用
- 与 `/codexspec:review-spec` 的发现整合
- 每次运行最多 5 个问题
- 对复杂规格可多次运行

---

### `/codexspec:analyze`

- **specify** 用于开始需求讨论，也可重新讨论已有需求。需求摘要只有经用户明确确认后，才成为后续工作的依据。
- **clarify** 用于澄清已有需求和规格中的歧义。每次最多提出五个问题，检查范围涵盖四类问题；先更新 `requirements.md`，再同步修改 `spec.md`。
- **analyze** 检查需求 → 规格 → 设计 → 计划 → 任务的完整链路。如果根据上游依据能够确定下游文档应如何修正，就会自动修正；它绝不修改 `requirements.md`，无法解决的问题会明确报告。任务审查通过后会自动运行，结果供后续参考，不作为阻止实现的门禁。

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

历史功能缺少 `requirements.md` 时，分析从 `spec.md` 开始，明确说明缺少原始讨论证据，只报告问题，不修改工件。历史功能缺少 `design.md` 也不妨碍分析。

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
You: /codexspec:checklist security

AI:  Generating security checklist...

     ✓ Created .codexspec/specs/2026-0613-1200ab-task-management/checklists/security.md

     ## Security Requirements Quality Checklist

     ### Authentication Requirements
     - [ ] CHK001 - Are authentication requirements defined for all protected endpoints? [Completeness]
     - [ ] CHK002 - Is password complexity explicitly specified? [Clarity]
     - [ ] CHK003 - Are session timeout requirements quantified? [Measurability]

     ### Data Protection
     - [ ] CHK004 - Are data encryption requirements specified at rest? [Completeness]
     - [ ] CHK005 - Are data encryption requirements specified in transit? [Completeness]
     - [ ] CHK006 - Is PII handling explicitly documented? [Clarity]

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
You: /codexspec:tasks-to-issues

AI:  Converting tasks to GitHub issues...

     Repository: github.com/example/taskman

     Creating issues:
     ✓ #42: Task 1.1 - Setup Project Structure (setup)
     ✓ #43: Task 2.1 - Write Tests for Task Entity (testing)
     ✓ #44: Task 2.2 - Implement Task Entity (implementation)
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

创建 issue 前，必须根据远端核实目标仓库，并获得明确授权。生成任务清单本身并不代表可以发布。

---

### `/codexspec:debug`

调查根因后再修复.

参见 [工作流](workflow.md#review-and-debugging).

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

---

### `/codexspec:reverse-spec`

针对已有代码，可以按目的选择以下入口：

| 命令 | 用途 | 产物/边界 |
|---------|-----------|-----------------|
| `onboard [path]` | 从已有代码库提取可复用的项目知识 | 在项目知识库中建立候选惯例和有明确证据的约束；不修改代码 |
| `reverse-spec [path]` | 理解现有架构，或检查代码是否符合已确认的意图 | 生成文档草案或偏差报告；不修改代码 |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard 根据实际代码推断项目惯例，只有发现明确禁令时才会提出约束。候选惯例会立即在本地生效；候选约束则需要在当前会话中由用户决定保留、修改还是丢弃。已有知识会保留；仅凭一次初始扫描，不会编造过去的决策理由，也不会把未经经历的问题写成经验教训。

Reverse-spec 有三种模式：

- **概览**：不指定路径，或指定仓库根目录时，生成简要的架构说明 `design.md` 和模块划分文件 `slices.md`，帮助选择接下来要检查的模块。
- **生成**：指定的模块没有已确认基线时，生成 `spec.md`、`design.md` 草案，以及尚待确认或根据代码推断的需求。
- **核对**：模块已有确认过的基线时，生成 `reconcile.md`，列出尚未记录的行为、规格中尚未实现的内容，以及代码与已确认规格和设计之间的语义差异；判断产品意图时，以需求为准。

根据代码推断的草案，必须经人工确认才能作为后续基线。核对报告会建议下一步是修复代码、更新文档，还是先明确产品意图，但不会自动执行这些修改。

---

### `/codexspec:distill`

把可复用的跨功能知识沉淀到 `.codexspec/profile/`，并在不手工编辑 Markdown 文件的前提下审核待定候选记录。

**语法：**

```text
/codexspec:distill [interaction segment]
/codexspec:distill review
```

**手动审核：**

- `/codexspec:distill review`，或没有新片段可提取时的直接调用，会打开一个仅从 `127.0.0.1` 提供的离线 HTML 页面。页头标明本次会话将写入的项目目录名，因此并排打开两个审核也不会混淆。
- 页面支持结构化修订、通过、抛弃、暂缓、合并、完整的暂存变更清单，以及显式的**应用全部**。修订与合并必须先展示最终 Markdown 的准确预览，同一操作才能暂存；在你使用任何决定控件之前，页面会标明每条记录处于三种预览状态中的哪一种——尚未预览、与当前内容一致、预览后内容已改动。
- 任何会删除记录文件的操作都要求二次确认并说明后果：抛弃会指明应用时将删除的文件，合并会指明将删除多少条成员记录，放弃草稿会指明将丢弃多少条暂存决定。
- 一条记录必须同时具备人工背书与基于结果的验证依据才能变为 `vetted`。在你选择通过之前，页面会显示该记录已有的依据是否已满足这一要求。
- 队列按已决定的内容分组，并显示待定记录中已有多少条处理完毕。暂存一条决定后会跳到下一条未决定的记录；页头有开关可关闭该行为。
- 页面可用键盘操作——按 `?` 查看快捷键。应用全部、取消会话、放弃草稿都不绑定任何单键。
- 暂存决定保存在一份可恢复、且被 Git 排除的项目草稿中。每个项目同时只有一个可写审核会话。
- 结构受损的草稿会连同可操作的诊断一并保留，只有通过显式的放弃操作才会被移除。
- 应用时会重新校验源哈希，任一记录发生变化即拒绝整批；它绝不覆盖并发编辑，也绝不报告部分成功。
- 页面的全部资源随 CodexSpec 一同分发。页面不使用 CDN、不调用远端模型、不做遥测。
- 若无法打开浏览器，命令会打印带令牌保护的本地 URL。浏览器不合适时请明确要求文本模式；它使用同一套校验与写入路径。

自动 distill 仍然是非交互、非阻塞的：它绝不打开页面、绝不启动文本审核、也绝不等待已保存的草稿。

---

### `/codexspec:evolve`

`evolve` 只采用已经认可、且对其他项目也有价值的知识，将其整理为命令或技能草案。推送变更或创建供人工审查的上游贡献 PR 前，必须获得明确批准。

```text
/codexspec:evolve
```

---

### `/codexspec:onboard`

初始化候选惯例和有证据支持的约束.

参见 [`reverse-spec`](#codexspecreverse-spec).

```text
/codexspec:onboard src/
```

---

### `/codexspec:commit-staged`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** 只分析当前暂存内容，并据此生成 Conventional Commits 提交信息；`-p` 只预览，不提交。文件由调用它的工作流选择并暂存。执行已获授权的提交时，提交辅助程序会再次检查实际提交内容是否与分析一致。智能体提交指引适用于普通对话、SDD、蓝图和 auto-dev 工作流；命令已安装不等于已经调用，也不代表用户授权了提交。
- **pr** 根据 diff 生成结构化的 GitHub PR 或 GitLab MR 说明。可通过 `--spec` 附加功能背景：既可以传入 `spec.md` 的路径，也可以传入能定位到该文件的功能目录名或前缀。默认输出可直接用于代码托管平台。
- **release-notes** 根据 Git 历史编写 Keep a Changelog 条目和发布说明正文。默认写入 `[Unreleased]` 章节；传入 `--version` 时使用指定的标签。该命令只编写说明，不会暂存、提交、修改版本号、打标签、发布或创建 release。
- **tasks-to-issues** 根据已有任务创建 GitHub issues，并附上任务依赖和验收标准。需要已经登录的 GitHub CLI；创建前会检查目标仓库是否与配置的远端一致。

预览提交，或在当前工作区执行已获授权的提交，需要 Python 3.11+ 和 Git。提交运行时随 CLI 项目安装，也内置于 Claude 插件。智能体创建包含内容变更的合并提交时，同样须先分析暂存内容。仅用于连接提交历史的合并会保留 Git 的默认提交信息，并检查提交树和父提交；快进合并不创建新提交。

共享辅助程序位于 `.codexspec/scripts/commit-staged-helper.py`，也可使用插件自带的副本。它需要 Python 3.11+ 和 Git，不调用 LLM，保留 Git hooks，并拒绝提交分析后发生变化的暂存内容。一次性初始化会安装此运行时；工作区路由、blueprint 和 auto-dev 仍需要 CLI。

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
You: /codexspec:pr --spec 2026-0613-1200ab-task-management

AI:  Generating Pull Request description...

     Platform: GitHub (github.com/example/taskman)
     Branch:   feature/task-management  →  origin/main
     Commits:  8 ahead

     ## Pull Request: Task management for small dev teams

     ### Context
     - User stories and REQ-* pulled from spec.md

     ### Summary
     - Adds task CRUD, sub-tasks, and real-time updates

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

### `/codexspec:release-notes`

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** 只分析当前暂存内容，并据此生成 Conventional Commits 提交信息；`-p` 只预览，不提交。文件由调用它的工作流选择并暂存。执行已获授权的提交时，提交辅助程序会再次检查实际提交内容是否与分析一致。智能体提交指引适用于普通对话、SDD、蓝图和 auto-dev 工作流；命令已安装不等于已经调用，也不代表用户授权了提交。
- **pr** 根据 diff 生成结构化的 GitHub PR 或 GitLab MR 说明。可通过 `--spec` 附加功能背景：既可以传入 `spec.md` 的路径，也可以传入能定位到该文件的功能目录名或前缀。默认输出可直接用于代码托管平台。
- **release-notes** 根据 Git 历史编写 Keep a Changelog 条目和发布说明正文。默认写入 `[Unreleased]` 章节；传入 `--version` 时使用指定的标签。该命令只编写说明，不会暂存、提交、修改版本号、打标签、发布或创建 release。
- **tasks-to-issues** 根据已有任务创建 GitHub issues，并附上任务依赖和验收标准。需要已经登录的 GitHub CLI；创建前会检查目标仓库是否与配置的远端一致。

预览提交，或在当前工作区执行已获授权的提交，需要 Python 3.11+ 和 Git。提交运行时随 CLI 项目安装，也内置于 Claude 插件。智能体创建包含内容变更的合并提交时，同样须先分析暂存内容。仅用于连接提交历史的合并会保留 Git 的默认提交信息，并检查提交树和父提交；快进合并不创建新提交。

#### 发布说明参数

| 命令 | 参考 |
|---|---|
| `--version <X.Y.Z>` | 采用提供的版本标签；未提供时使用 `[Unreleased]` |
| `--from <ref>` | 起始引用；默认依次尝试最近可达标签、可定位的变更日志版本、完整历史 |
| `--to <ref>` | 结束引用，默认为 `HEAD` |
| `--output <file>` | 将发布正文写入此文件；默认输出到终端 |
| `--spec <feature>` | 可选的功能上下文；无法解析功能时会报告，并继续依据 Git 生成 |

---

### `/codexspec:review-code`

将选定的 Git 变更作为合并前的严格缺陷门禁进行审查。默认目标包含完整特性差异；显式选择器可审查已提交、未提交或单个提交的证据，但不接受路径过滤。

<!-- REVIEW-CODE-BREAKING: DEFAULT-GATE -->
<!-- REVIEW-CODE-BREAKING: PATH-AUDIT -->

**默认审查模式：**

- 默认命令现在是变更范围缺陷门禁，不再是宽泛的质量评分审计。
- 不再接受位置路径参数。需要按路径执行建议性质的质量评分时，请显式使用 `--audit`。

**缺陷门禁语法：**

```text
/codexspec:review-code
/codexspec:review-code --committed [--base <branch>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --uncommitted [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code --commit <sha> [--parent <n>] [--feature <feature-dir>] [--focus <instructions>]
/codexspec:review-code [--committed] --incremental-from <fingerprint> [--feature <feature-dir>]
```

每种缺陷门禁形式都可以附加 `--decided-by reviewer|ask`，用于在本次运行中覆盖 `review.decided_by`。

<!-- REVIEW-CODE-SYSTEM-CONTRACT -->
<!-- REVIEW-CODE-VARIANT-SEARCH -->
<!-- REVIEW-CODE-NEUTRAL-HANDOFF -->

门禁会清点目标中的全部工件、评估适用需求，并依次执行五个阶段：Scope、System Contract、Behavior、Risk 和 Verification。它会记录有来源依据的跨模块契约和按行为划分的审查分区；每个已确认且可重复出现的根因都会在本轮结束前触发一次有明确边界的同类问题搜索。六个报告段落之后会附带一个使用 `schema_version: "3"` 的机器可读 `<review-code-result>` 结果块。该结果块 包含目标标识、覆盖记录和修复后需要重新核实的客观事项；调用方保留这些中立事项并交给新的完整审查，但不会传递修复思路或之前的正确性结论。结果只能是 `PASS`、`FAIL` 或 `INCONCLUSIVE`：任何 P0-P3 缺陷都会得到 `FAIL`，缺少强制证据或覆盖不完整时得到 `INCONCLUSIVE`。

**增量复审。** 修复之后，`--incremental-from <fingerprint>` 只复审自那次结果以来的变化：改动过的文件、它们触及的审查分区和契约，以及遗留的待核实事项。未改动且未受影响的文件沿用之前的覆盖结果，审查员在其他位置发现的缺陷仍会照常报告。增量 `PASS` 永远不代表功能完成：`implement-tasks` 先做一次完整审查，每次修复后做增量审查，最后再做一次全新的完整审查作为最终验收。审查记录写在仓库之外的用户缓存目录（`~/.cache/codexspec/review/` 或 `%LOCALAPPDATA%\codexspec\review\`），对话中只出现报告和 结果块。

**判定模式。** `.codexspec/config.yml` 中的 `review.decided_by` 决定：当某个缺陷的触发条件超出项目实际使用场景（例如项目根本不会接收的输入）时，由谁来判定。默认值 `reviewer` 下，审查行为与之前完全一致。设为 `ask` 时，审查会把这类问题报告为待决的场景判定，而不是据此判定失败；`implement-tasks` 会就此询问你一次：修复，还是确认该场景不在范围内。你的回答会以已确认的 `CON` 或 `OUT` 条目写入 `requirements.md`，后续轮次不会再次提出。

```text
You: /codexspec:review-code --feature .codexspec/specs/2026-0714-example

AI:  ## Verdict
     **PASS** — all required review and verification completed with no findings.
```

**适用规则与维护建议。** 每次审查读取共享规则和所选模式，评估全部七个审查维度，再依据实际行为、契约和依赖按需加载详细清单。追踪中发现的未修改依赖也可以触发语言或框架子清单。维护建议须指出当前存在的问题，并给出有依据、兼容现有行为的局部改进；假想的未来复杂度和单独的风格阈值不足以支持修复。现有缺陷结果继续使用版本 3，另以版本 1 的 `<review-code-maintenance>` 附加结果报告建议，并绑定相同的目标指纹。独立审查只报告建议；`implement-tasks` 根据 `workflow.auto_maintenance`（默认 `true`）核验并实施。修复在持续取得实质进展时继续，同时遵守现有停止条件；不设固定轮次上限，最终验收要求全新的完整复审。

布尔类型的 CLI 开关可以使用 `on/true/1/yes` 或 `off/false/0/no`，不区分大小写，也允许值的前后带空白。不传值时，会切换目标 checkout 中的当前设置；写入 YAML 的值始终是布尔值。

`codexspec init` 将 Claude Code 与 Codex 共享的审查资源安装到 `.codexspec/review-code/`。`--force` 更新随工具提供的资源，并保留路径不同的扩展文件。仅安装 CLI 不会创建项目文件。仅使用插件时，若项目没有已安装的资源目录，审查会读取宿主解析的插件根目录中的同一套资源。

<!-- REVIEW-CODE-AUDIT -->

#### 路径质量审计

显式 audit 分支按路径检查当前文件的完整内容，评估符合语言惯例的清晰表达、正确性、健壮性、架构和宪法对齐情况。该评分仅供参考，不能作为 `implement-tasks` 的完成门禁。

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
- 当存在静态分析工具的配置时运行它们（`ruff`/`mypy`、`eslint`/`tsc`、`go vet`/`gofmt`、`cargo check`/`cargo clippy`、`shellcheck`）；否则跳过相应检查，并说明检查覆盖范围有所减少
- 为四个维度打分：符合语言惯例的清晰表达与简洁、正确性与显式契约、运行时健壮性与资源管理规范、架构与设计完整性
- 为检测到的框架注入必检子节（例如 React 的 Hooks Compliance、Rust 的 Ownership & Borrowing、Go 的 Goroutine & Context Discipline、C/C++ 的 Memory & Lifetime Safety、Shell 的 Execution Safety）
- 当存在 `.codexspec/memory/constitution.md` 时与之交叉对照；不存在时则丢弃宪法轴并重新分配其权重
- 按严重级别归类发现：CRITICAL、HIGH、MEDIUM、LOW（LOW 建议最多扣 5 分）

**示例：**

```text
You: /codexspec:review-code --audit src/

AI:  # Code Review Report

     ## Summary
     - Overall Status: Needs Work
     - Quality Score: 78/100
     - Detected Language: Python

     ## Static Analysis Results
     | Tool   | Status | Issues | Details                |
     |--------|--------|--------|------------------------|
     | ruff   | Warn   | 3      | Unused imports, line length |
     | mypy   | Pass   | 0      | No type errors         |

     ## Detailed Findings
     ### Critical Issues (CRITICAL)
     - [ ] [CODE-001] src/auth/service.py:42 - bare `except Exception:` swallows the original cause
       Impact: Original error context is lost during debugging.
       Suggestion: narrow the exception and re-raise with `raise ... from err`.

     ### Suggestions (LOW)
     - [ ] [CODE-004] src/auth/service.py:120 - manual loop where a comprehension suffices

     ## Recommendations
     1. Priority 1: Fix CODE-001 before merge.
     2. Priority 2: Apply LOW suggestions opportunistically.
```

**提示：**

- 传入多个路径以聚焦评审某个范围，例如 `src/ tests/`
- 分数仅供参考；CRITICAL/HIGH 才是可操作的信号

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
You: /codexspec:config

AI:  ## Configuration Manager

     Configuration file found at .codexspec/config.yml.
     What would you like to do?
     - View current config
     - Modify config
     - Reset to defaults
     - Cancel

You: Modify config

AI:  Select a dimension to change:
     - Output language (base)
     - Interaction language
     - Document language
     - Commit-message language
     - workflow.auto_next
     - workflow.auto_distill
     - workflow.auto_maintenance
     - workflow.worktrees (default on; checkout-local)
     - review.decided_by

You: Output language (base) → zh-CN

AI:  ✓ Updated language.output: "zh-CN"
     (interaction and document fall back to output, then en.)
```

**提示：**

- 改动前先用 `/codexspec:config --view` 查看当前状态
- 全新或重置后的配置只写入 `output`；仅当 `interaction`/`document` 应当与 `output` 不同时才显式设置
- 终端里的脚本化修改请优先使用 `codexspec config` CLI（`--set-lang`、`--set-interaction-lang`、`--set-document-lang`、`--set-commit-lang`、`--auto-next`）

交互菜单还可管理 `workflow.auto_distill`、`workflow.auto_maintenance`、`workflow.worktrees` 和 `review.decided_by`。配置修改遵循各检出目录独立生效的 worktree 路由规则。

---

### `/codexspec:quick`

为小型改动运行精简的 Requirements-First SDD 流程。

**语法：**

```
/codexspec:quick [describe a small requirement]
```

**参数：**

| 参数 | 必需 | 描述 |
|----------|----------|-------------|
| `describe a small requirement` | 否 | 对这条规模小、边界清晰的改动的简短描述（未提供时会提示输入） |

**功能：**

- 评估范围（触及的文件、模块跨度、新增依赖、未决的产品决策）；若改动很广或包含多个独立结果，则建议改用标准流程
- 用与 `/codexspec:specify` 相同的时间戳约定创建功能工作区与 `requirements.md`
- 只解决会实质改变实现的歧义；呈现精简的已确认摘要（`NEED-*`、相关的 `CON-*`/`DEC-*`、`OUT-*`、未解决的 `OPEN-*`）
- 停在确认门：在你确认摘要之前不会生成任何内容
- 在新建的功能目录上链式调用生成命令：`/codexspec:generate-spec`、`/codexspec:design-to-plan`、`/codexspec:plan-to-tasks`、`/codexspec:implement-tasks`
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
You: /codexspec:quick Add a "remember me" checkbox to the login form

AI:  Scope check: 1 component, 1 form field, no new dependencies. Quick is appropriate.

     Confirmed requirements:
     - NEED-1: "Remember me" checkbox on the login form (default unchecked)
     - DEC-1: Persist a long-lived refresh token only when checked
     OUT-1: SSO / social login (unchanged)

     Confirm this summary to start the automated flow. [y/N]

You: y

AI:  Running generate-spec → design-to-plan → plan-to-tasks → implement-tasks ...

     ✓ Feature dir: .codexspec/specs/2026-0713-0915ab-remember-me/
     ✓ All reviews PASS_WITH_WARNINGS or higher
     ✓ Implementation verified
     Open advisories: none
```

**提示：**

- 把 Quick 留给真正小型、单一结果的改动；否则运行 `/codexspec:specify` 走标准流程
- 仍需确认——Quick 绝不为了让自动化继续推进而替你推断产品决策
- 若任一生成评审返回 `NEEDS_REVISION`/`BLOCKED`，Quick 会停下并把控制权交还给你

---
