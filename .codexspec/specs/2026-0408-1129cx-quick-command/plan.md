# Implementation Plan: `/codexspec:quick` — 一站式快速实现命令

## 1. 技术栈

| 类别 | 技术 | 版本 | 备注 |
|------|------|------|------|
| 语言 | Markdown | N/A | Slash command 模板 |
| 运行环境 | Claude Code | 最新版 | Skill 工具、AskUserQuestion 工具 |
| 包管理 | uv | ≥0.1.0 | 安装和分发 |
| 构建 | Hatchling | 现有版本 | 模板打包 |

> 本功能为纯模板实现，不涉及 Python 代码变更。quick.md 是一个 Markdown slash command 模板，通过 Skill 工具编排调用现有命令。

## 2. 宪法合规审查

| 原则 | 合规 | 说明 |
|------|------|------|
| 代码质量 | ✅ | 模板遵循现有格式规范，复用而非重写 |
| 测试标准 | ✅ | 模板本身为 Markdown，不需要单元测试；功能验证通过手动执行 |
| 文档 | ✅ | 模板包含完整的流程说明和输出示例 |
| 架构 | ✅ | 通过 Skill 工具调用实现关注点分离，quick.md 仅负责流程编排 |
| 性能 | ✅ | 无额外性能开销，复用现有命令执行路径 |
| 安全 | ✅ | 不引入新的输入处理，所有用户交互通过 AskUserQuestion |
| 模板修改规则 | ✅ | 在 `templates/commands/` 目录下创建源模板 |
| 决策指南 | ✅ | 优先可维护性（Skill 调用）和清晰性（阶段进度提示） |

## 3. 架构概览

```
用户输入需求描述
        │
        ▼
┌──────────────────────────────────────────┐
│           /codexspec:quick               │
│  ┌────────────────────────────────────┐  │
│  │ Phase 0: 前置检查                   │  │
│  │  - Configuration Check             │  │
│  │  - Language Preference             │  │
│  │  - Git Branch Safety Check         │  │
│  └──────────────┬─────────────────────┘  │
│                 │                         │
│  ┌──────────────▼─────────────────────┐  │
│  │ Phase 1: 复杂度评估                  │  │
│  │  - 分析需求 → 小/中/大              │  │
│  │  - 大型 → 建议标准流程              │  │
│  └──────────────┬─────────────────────┘  │
│                 │                         │
│  ┌──────────────▼─────────────────────┐  │
│  │ Phase 2: 精简澄清                   │  │
│  │  - 2-5 个结构化问题                 │  │
│  │  - 可跳过（需求已清晰）             │  │
│  └──────────────┬─────────────────────┘  │
│                 │                         │
│  ┌──────────────▼─────────────────────┐  │
│  │ Phase 3: 自动化 SDD 流程            │  │
│  │  ┌──────────────────────────────────┐│  │
│  │  │ [1/4] Skill: generate-spec      ││  │
│  │  │       (含自动 review-spec)       ││  │
│  │  │ [2/4] Skill: spec-to-plan       ││  │
│  │  │       (含自动 review-plan)       ││  │
│  │  │ [3/4] Skill: plan-to-tasks      ││  │
│  │  │       (含自动 review-tasks)      ││  │
│  │  │ [4/4] Skill: implement-tasks    ││  │
│  │  └──────────────────────────────────┘│  │
│  │  重大问题 → 暂停询问用户            │  │
│  └──────────────┬─────────────────────┘  │
│                 │                         │
│  ┌──────────────▼─────────────────────┐  │
│  │ Phase 4: 完成总结                   │  │
│  │  - 产物清单                        │  │
│  │  - 代码变更摘要                     │  │
│  │  - 后续建议                        │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

## 4. 组件结构

```
templates/commands/
├── quick.md              # 【新增】一站式快速实现命令模板
├── specify.md            # 现有 - 需求澄清（参考其澄清模式）
├── generate-spec.md      # 现有 - 被 quick 通过 Skill 调用（内含自动 review-spec）
├── review-spec.md        # 现有 - 由 generate-spec 自动调用
├── spec-to-plan.md       # 现有 - 被 quick 通过 Skill 调用（内含自动 review-plan）
├── review-plan.md        # 现有 - 由 spec-to-plan 自动调用
├── plan-to-tasks.md      # 现有 - 被 quick 通过 Skill 调用（内含自动 review-tasks）
├── review-tasks.md       # 现有 - 由 plan-to-tasks 自动调用
└── implement-tasks.md    # 现有 - 被 quick 通过 Skill 调用
```

## 5. 模块依赖图

```
┌──────────────────┐
│   quick.md       │ (新增 - 流程编排器)
│   (Orchestrator)  │
└────────┬─────────┘
         │ Skill 调用
         ▼
┌────────────────────────────────────────────┐
│              现有命令模板                     │
│                                            │
│  generate-spec (含 review-spec)            │
│       │                                    │
│       ▼                                    │
│  spec-to-plan (含 review-plan)             │
│       │                                    │
│       ▼                                    │
│  plan-to-tasks (含 review-tasks)           │
│       │                                    │
│       ▼                                    │
│  implement-tasks                           │
└────────────────────────────────────────────┘
```

**依赖关系说明**：

- `quick.md` 直接调用 4 个生成/实现命令（generate-spec、spec-to-plan、plan-to-tasks、implement-tasks）
- 3 个 review 命令由生成命令内部自动调用，quick 不单独调用
- 各子命令之间的依赖是数据依赖（通过 spec 目录路径传递），而非代码依赖
- `quick.md` 仅新增，不修改任何现有文件

## 6. 模块规格

### 模块: quick.md（核心 — 流程编排器）

- **职责**: 接收用户需求输入，依次编排复杂度评估、精简澄清、SDD 自动化流程、完成总结
- **依赖**: 通过 Skill 工具调用 4 个现有命令模板（generate-spec、spec-to-plan、plan-to-tasks、implement-tasks），review 命令由它们内部自动调用
- **接口**: 接受需求描述字符串作为 `$ARGUMENTS`
- **文件**: `templates/commands/quick.md`（新建）

### 模板内部结构设计

quick.md 模板应包含以下段落（按执行顺序）：

#### 段落 1: YAML Frontmatter

```yaml
---
description: One-stop quick implementation for small requirements — auto spec, plan, tasks, and code
argument-hint: "Describe your requirement"
---
```

#### 段落 2: Configuration Check

- 复用 `specify.md` 中的 Configuration Check 段落（检查 `.codexspec/config.yml` 存在性）

#### 段落 3: Language Preference

- 标准段落，与现有模板一致

#### 段落 4: User Input

- `$ARGUMENTS` — 用户的需求描述

#### 段落 5: Git Branch Safety Check

- 标准段落，与 `generate-spec.md` 一致

#### 段落 6: Instructions — 复杂度评估

- 角色定义：流程编排器（Orchestrator）
- 分析用户输入的需求，评估复杂度
- 评估维度：预估文件变更数、模块跨度、外部依赖
- 参考阈值：小型 ≤3 文件/中型 4-8/大型 >8
- 如果中型/大型，使用 AskUserQuestion 询问是否继续或切换标准流程
- 如果用户选择标准流程，输出建议的命令序列并终止

#### 段落 7: Instructions — 精简澄清

- 仅针对关键模糊点提问（2-5 个问题）
- 使用 AskUserQuestion 结构化选项格式
- 如需求已清晰可跳过
- 澄清完成后汇总需求摘要

#### 段落 8: Instructions — 自动化 SDD 流程

**Skill 调用设计原则**：
> 子命令通过 Skill 工具**原样调用**，不传递任何特殊前缀或跳过指令。
>
> - Language Preference：静默读取配置文件，幂等且轻量，重复执行无害
> - Git Branch Safety Check：仅 generate-spec 包含，会在对话中提示一次（quick 本身也有该检查，agent 应基于对话上下文识别已处理的分支选择，避免重复提示）
> - 自动审查：generate-spec、spec-to-plan、plan-to-tasks 各自内含 auto-review 步骤，quick 无需单独调用 review 命令
> - 这一设计确保零现有文件修改，子命令行为完全一致

按顺序执行以下 **4 步**（每个生成命令内含自动审查）：

**步骤 8.1**: 生成 spec + 自动审查（Skill 调用）

```
输出进度: 📋 [1/4] 生成并审查 spec ...
Skill("codexspec:generate-spec", args="基于以上澄清结果生成 spec")
→ generate-spec 自动创建 spec 目录和 spec.md
→ generate-spec 内部自动调用 review-spec 审查
→ 小问题由 review-spec 自动修正
→ 重大问题: 暂停，向用户描述问题，获取反馈后修正再继续
输出: ✅ spec.md 生成并审查完成
```

**步骤 8.2**: 生成 plan + 自动审查（Skill 调用）

```
输出进度: 📐 [2/4] 生成并审查 plan ...
Skill("codexspec:spec-to-plan", args="{spec_dir}/spec.md")
→ spec-to-plan 内部自动调用 review-plan 审查
→ 小问题自修正 / 重大问题回退（同 8.1）
输出: ✅ plan.md 生成并审查完成
```

**步骤 8.3**: 生成 tasks + 自动审查（Skill 调用）

```
输出进度: 📝 [3/4] 生成并审查 tasks ...
Skill("codexspec:plan-to-tasks", args="{spec_dir}/spec.md {spec_dir}/plan.md")
→ plan-to-tasks 内部自动调用 review-tasks 审查
→ 小问题自修正 / 重大问题回退（同 8.1）
输出: ✅ tasks.md 生成并审查完成
```

**步骤 8.4**: 实现代码（Skill 调用）

```
输出进度: 🚀 [4/4] 实现代码 ...
Skill("codexspec:implement-tasks", args="{spec_dir}/tasks.md")
输出: ✅ 代码实现完成
```

**关于 spec 目录路径**：
> generate-spec 会自行创建 spec 目录（使用时间戳+随机后缀命名方案）。
> quick.md 在步骤 8.1 完成后，从对话上下文中获取 generate-spec 创建的目录路径，
> 用于后续步骤的参数传递。

#### 段落 9: Instructions — 完成总结

- 列出产物目录和文件清单
- 汇总代码变更（新增/修改的文件）
- 提供后续建议（commit-staged、pr）

#### 段落 10: 重大问题回退指引

- 定义小问题/重大问题区分标准（直接嵌入模板中供 agent 参考）
- 小问题：格式缺失、措辞不精确、可推断的遗漏
- 重大问题：逻辑矛盾、范围膨胀 >50%、技术不可行、关键信息缺失
- 回退时使用 AskUserQuestion 向用户描述问题并获取反馈

## 7. 数据模型

N/A — 本功能不涉及持久化数据。所有数据通过 spec 目录下的 Markdown 文件传递。

**数据流**：

```
用户输入 → quick.md (澄清结果)
  → Skill: generate-spec → spec.md + review-spec.md（内含自动审查）
  → Skill: spec-to-plan → plan.md + review-plan.md（内含自动审查）
  → Skill: plan-to-tasks → tasks.md + review-tasks.md（内含自动审查）
  → Skill: implement-tasks → 代码文件
```

## 8. 实现阶段

### Phase 1: 创建模板文件（基础结构）

- [ ] 创建 `templates/commands/quick.md`
- [ ] 编写 YAML frontmatter（description, argument-hint）
- [ ] 编写 Configuration Check 段落（复用 specify.md 模式）
- [ ] 编写 Language Preference 标准段落
- [ ] 编写 User Input 段落
- [ ] 编写 Git Branch Safety Check 标准段落

### Phase 2: 核心流程逻辑

- [ ] 编写复杂度评估指引（维度、阈值、AskUserQuestion 交互）
- [ ] 编写精简澄清指引（2-5 问题、结构化选项、可跳过条件）
- [ ] 编写自动化 SDD 流程编排（4 步 Skill 原样调用序列、路径传递、进度提示）
- [ ] 编写重大问题回退机制（区分标准、回退流程、AskUserQuestion 交互）

### Phase 3: 辅助段落

- [ ] 编写完成总结段落（产物清单、代码变更、后续建议）
- [ ] 编写边缘情况处理指引（空输入、子命令失败、上下文窗口）

### Phase 4: 验证

- [ ] 在测试项目中运行 `/codexspec:quick` 验证完整流程
- [ ] 验证子命令路径传递正确性
- [ ] 验证复杂度评估的用户交互
- [ ] 验证重大问题回退机制

## 9. 技术决策

### Decision 1: 纯模板实现，不修改 Python CLI 代码

- **选择**: quick.md 作为独立的 slash command 模板，不在 `src/codexspec/__init__.py` 中添加新的 CLI 命令
- **理由**:
  - slash command 模板不需要 CLI 注册即可工作
  - 保持最小变更范围，降低引入 bug 的风险
  - 与现有 slash command（如 specify、generate-spec）保持一致的分发方式
- **替代方案**: 在 CLI 中添加 `codexspec quick` 命令来启动流程 — 但这需要在 Python 代码中实现流程编排，与 Skill 工具调用模式不一致
- **权衡**: 放弃了 CLI 级别的入口点，用户必须通过 `/codexspec:quick` 使用

### Decision 2: 全部 Skill 原样调用，利用子命令内置自动审查

- **选择**: 所有子命令通过 Skill 工具原样调用，不传递特殊前缀，不修改任何现有命令。利用 generate-spec、spec-to-plan、plan-to-tasks 各自内置的 auto-review 步骤，quick 仅需调用 4 个命令（而非 7 个）
- **理由**:
  - 零现有文件修改，最小影响范围
  - 子命令行为完全一致，无需维护特殊模式
  - 澄清上下文通过 Skill 调用自然传递（同一对话）
  - generate-spec 的目录创建和自动审查在 quick 流程中正常工作
- **替代方案**: 内联 spec 生成 — 需要在 quick.md 中重复 generate-spec 的生成逻辑，增加维护负担和不一致风险
- **权衡**: generate-spec 会重复执行 Git Branch Safety Check，但 agent 在同一对话中应能识别已处理的分支选择

### Decision 3: 复杂度评估使用参考阈值而非严格规则

- **选择**: 提供 ≤3/4-8/>8 文件的参考阈值，允许 agent 灵活判断
- **理由**: 不同类型的文件变更复杂度差异很大（修改一个配置文件 vs 新建一个模块），严格数字阈值可能导致误判
- **替代方案**: 设定严格的量化标准 — 但需求的复杂度是多维的，很难用单一数字准确衡量
- **权衡**: 灵活性可能导致不同执行之间的评估不一致，但这对用户体验的影响较小（用户始终有选择权）
