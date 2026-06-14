# Task Breakdown: `/codexspec:quick` — 一站式快速实现命令

## 概览

- **总任务数**: 10
- **可并行任务**: 3
- **阶段数**: 3
- **产物类型**: Markdown 模板（非代码，不适用 TDD）

> 本功能的全部交付物为一个 Markdown 文件 `templates/commands/quick.md`。
> 按照宪法中关于非代码任务（docs, config, assets）的规定，直接实现并验证正确性。

## Phase 1: 基础结构

### Task 1.1: 创建模板文件并编写 YAML Frontmatter ✅

- **Type**: Setup
- **Files**: `templates/commands/quick.md`
- **Description**: 创建 `templates/commands/quick.md` 文件，编写 YAML frontmatter（description、argument-hint）。参照 `generate-spec.md` 的 frontmatter 格式。
- **Dependencies**: 无
- **Est. Complexity**: Low
- **Acceptance**: 文件存在且 frontmatter 格式正确

### Task 1.2: 编写 Configuration Check 段落 ✅

- **Type**: Implementation
- **Files**: `templates/commands/quick.md`
- **Description**: 复用 `specify.md` 中的 Configuration Check 段落（检查 `.codexspec/config.yml` 存在性、不存在时显示提示、存在时读取配置）。直接从 `specify.md` 复制该段落内容。
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Acceptance**: 段落与 `specify.md` 中的 Configuration Check 保持一致

### Task 1.3: 编写 Language Preference 段落 ✅

- **Type**: Implementation
- **Files**: `templates/commands/quick.md`
- **Description**: 添加标准的 Language Preference 段落。从任意现有模板（如 `generate-spec.md`）复制该段落内容。
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Acceptance**: 段落与现有模板保持一致

### Task 1.4: 编写 User Input 和 Git Branch Safety Check 段落 ✅

- **Type**: Implementation
- **Files**: `templates/commands/quick.md`
- **Description**: 添加 User Input 段落（`$ARGUMENTS`）和 Git Branch Safety Check 段落。Git Branch Safety Check 直接从 `generate-spec.md` 复制。
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Acceptance**: User Input 接受 `$ARGUMENTS`；Git Branch Safety Check 与 `generate-spec.md` 一致

## Phase 2: 核心流程逻辑

### Task 2.1: 编写复杂度评估指引 ✅

- **Type**: Implementation
- **Files**: `templates/commands/quick.md`
- **Description**: 在 Instructions 段落中编写复杂度评估指引，包括：
  - 角色定义（流程编排器 Orchestrator）
  - 评估维度：预估文件变更数、模块跨度、外部依赖
  - 参考阈值：小型 ≤3 文件 / 中型 4-8 / 大型 >8
  - 中型/大型时使用 `AskUserQuestion` 询问用户是否继续或切换标准流程
  - 用户选择标准流程时输出建议命令序列并终止
  - 空输入/过短输入的处理
- **Dependencies**: Task 1.4
- **Est. Complexity**: Medium
- **Acceptance**: 包含评估维度、阈值表、AskUserQuestion 示例 JSON

### Task 2.2: 编写精简澄清指引 ✅

- **Type**: Implementation
- **Files**: `templates/commands/quick.md`
- **Description**: 编写精简澄清指引，包括：
  - 仅针对关键模糊点提问（2-5 个问题）
  - 使用 `AskUserQuestion` 结构化选项格式（附示例 JSON）
  - 需求已清晰时可跳过澄清的判断条件
  - 澄清中范围大幅扩展时重新评估复杂度
  - 澄清完成后汇总需求摘要
- **Dependencies**: Task 2.1
- **Est. Complexity**: Medium
- **Acceptance**: 包含 AskUserQuestion 示例、跳过条件、摘要汇总说明

### Task 2.3: 编写自动化 SDD 流程编排 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/quick.md`
- **Description**: 编写 4 步 Skill 原样调用序列，包括：
  - Skill 调用设计原则（原样调用、不传特殊前缀、子命令内含自动审查）
  - 步骤 [1/4]: `Skill("codexspec:generate-spec", args="基于以上澄清结果生成 spec")`
  - 步骤 [2/4]: `Skill("codexspec:spec-to-plan", args="{spec_dir}/spec.md")`
  - 步骤 [3/4]: `Skill("codexspec:plan-to-tasks", args="{spec_dir}/spec.md {spec_dir}/plan.md")`
  - 步骤 [4/4]: `Skill("codexspec:implement-tasks", args="{spec_dir}/tasks.md")`
  - 每步的进度提示格式
  - spec 目录路径获取说明（从 generate-spec 对话上下文中获取）
- **Dependencies**: Task 2.2
- **Est. Complexity**: Medium
- **Acceptance**: 4 步 Skill 调用完整，路径传递清晰，进度提示格式正确

### Task 2.4: 编写重大问题回退指引 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/quick.md`
- **Description**: 编写重大问题回退机制指引，包括：
  - 小问题定义：格式缺失、措辞不精确、可推断的遗漏
  - 重大问题定义：逻辑矛盾、范围膨胀 >50%、技术不可行、关键信息缺失
  - 判断原则：agent 能自信修正 = 小问题；需用户决策 = 重大问题
  - 回退时使用 AskUserQuestion 描述问题并获取反馈的流程
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low
- **Acceptance**: 小/大问题分类清晰，判断原则明确，AskUserQuestion 交互说明完整

## Phase 3: 辅助段落与验证

### Task 3.1: 编写完成总结段落 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/quick.md`
- **Description**: 编写流程完成后的总结段落，包括：
  - 产物目录和文件清单
  - 代码变更摘要（新增/修改的文件列表）
  - 后续建议（`/codexspec:commit-staged`、`/codexspec:pr`）
  - 边缘情况处理：上下文窗口接近极限时精简输出、子命令失败时的报告格式、项目无 `.codexspec/` 目录时的提示
- **Dependencies**: Task 2.3
- **Est. Complexity**: Low
- **Acceptance**: 总结格式包含产物清单、变更摘要、后续建议

### Task 3.2: 整体验证与格式校对 ✅

- **Type**: Verification
- **Files**: `templates/commands/quick.md`
- **Description**: 对完成的 quick.md 进行整体验证：
  - 检查段落顺序：frontmatter → Configuration Check → Language Preference → User Input → Git Branch Safety Check → Instructions
  - 验证 Markdown 格式正确性（标题层级、代码块、引用块）
  - 对照 `generate-spec.md` 确认标准段落格式一致性
  - 确认所有 spec 需求（REQ-001 ~ REQ-007、NFR-001 ~ NFR-003）均已覆盖
  - 确认边缘情况处理完整
- **Dependencies**: Task 3.1, Task 2.4
- **Est. Complexity**: Low
- **Acceptance**: 通过 NFR-001 模板一致性检查，所有 REQ 和 NFR 均有对应模板段落

## 执行顺序

```
Phase 1:
  Task 1.1 ──► Task 1.2
           ──► Task 1.3
           ──► Task 1.4
                  │
Phase 2:         │
           Task 2.1 ──► Task 2.2 ──► Task 2.3 [P]
                │
                └──────► Task 2.4 [P]
                                      │
Phase 3:                              │
           Task 3.1 [P] ◄────────────┘
                │
           Task 3.2 ◄──── Task 2.4
```

## 检查点

- [x] **Checkpoint 1**: Phase 1 完成后 — 验证 quick.md 包含所有标准段落（frontmatter、Configuration Check、Language Preference、User Input、Git Branch Safety Check）
- [x] **Checkpoint 2**: Phase 2 完成后 — 验证核心流程逻辑完整（复杂度评估、精简澄清、4 步 Skill 调用、回退机制）
- [x] **Checkpoint 3**: Phase 3 完成后 — 验证完成总结段落和整体格式，确认所有 spec 需求覆盖
