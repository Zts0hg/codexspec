# Task Breakdown: CodexSpec Review 评分机制与生成质量优化

## Overview

- **Total tasks**: 20
- **Parallelizable tasks**: 11
- **Estimated phases**: 4

> **Note**: 本项目为模板改进项目，不涉及代码编写，因此不适用传统 TDD 模式。任务按"设计 → 实现 → 验证"的流程组织。

## Phase 1: Foundation - 评分细则设计

本阶段创建共享的评分细则组件，为后续模板修改提供基础。

### Task 1.1: 设计 review-spec 评分细则 [P] ✅

- **Type**: Design
- **Files**: `templates/commands/review-spec.md`
- **Description**: 为 review-spec.md 设计完整的评分细则，定义 5 个评分类别（Completeness, Clarity, Consistency, Testability, Constitution Alignment）的满分标准、典型扣分场景和具体扣分值
- **Dependencies**: None
- **Est. Complexity**: High
- **Deliverable**: 在 review-spec.md 中添加 "Scoring Rubrics" 章节

### Task 1.2: 设计 review-plan 评分细则 [P] ✅

- **Type**: Design
- **Files**: `templates/commands/review-plan.md`
- **Description**: 为 review-plan.md 设计完整的评分细则，定义 5 个评分类别（Spec Alignment, Tech Stack, Architecture Quality, Phase Planning, Constitution Alignment）的评分标准
- **Dependencies**: None
- **Est. Complexity**: High
- **Deliverable**: 在 review-plan.md 中添加 "Scoring Rubrics" 章节

### Task 1.3: 设计 review-tasks 评分细则 [P] ✅

- **Type**: Design
- **Files**: `templates/commands/review-tasks.md`
- **Description**: 为 review-tasks.md 设计完整的评分细则，定义 5 个评分类别（Plan Coverage, TDD Compliance, Dependency & Ordering, Task Granularity, Parallelization & Files）的评分标准
- **Dependencies**: None
- **Est. Complexity**: High
- **Deliverable**: 在 review-tasks.md 中添加 "Scoring Rubrics" 章节

### Task 1.4: 设计 review-python-code 评分细则 [P] ✅

- **Type**: Design
- **Files**: `templates/commands/review-python-code.md`
- **Description**: 为 review-python-code.md 设计完整的评分细则，定义 PEP 8 合规性、类型安全、工程健壮性等评分类别的标准
- **Dependencies**: None
- **Est. Complexity**: High
- **Deliverable**: 在 review-python-code.md 中添加 "Scoring Rubrics" 章节

### Task 1.5: 设计 review-react-code 评分细则 [P] ✅

- **Type**: Design
- **Files**: `templates/commands/review-react-code.md`
- **Description**: 为 review-react-code.md 设计完整的评分细则，定义组件架构、Hooks 规范、状态管理等评分类别的标准
- **Dependencies**: None
- **Est. Complexity**: High
- **Deliverable**: 在 review-react-code.md 中添加 "Scoring Rubrics" 章节

### Task 1.6: 创建评分细则格式规范 ✅

- **Type**: Design
- **Files**: `templates/commands/review-spec.md` (作为示例)
- **Description**: 定义统一的评分细则格式，包括：满分标准描述、典型扣分场景、具体扣分值、评分示例
- **Dependencies**: Task 1.1, Task 1.2, Task 1.3
- **Est. Complexity**: Medium
- **Deliverable**: 确保所有 review 模板的评分细则格式一致

## Phase 2: Core Implementation - Review 模板改进

本阶段实现 REQ-001 到 REQ-005，改进所有 review 模板。

### Task 2.1: 为 review-spec 添加评分依据展示 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/review-spec.md`
- **Description**: 修改 Scoring Breakdown 章节格式，添加"评分标准对照"和"扣分明细"列，确保用户可追溯每个分数来源
- **Dependencies**: Task 1.1
- **Est. Complexity**: Medium
- **关联需求**: REQ-003

### Task 2.2: 为 review-plan 添加评分依据展示 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/review-plan.md`
- **Description**: 修改 Scoring Breakdown 章节格式，添加"评分标准对照"和"扣分明细"列
- **Dependencies**: Task 1.2
- **Est. Complexity**: Medium
- **关联需求**: REQ-003

### Task 2.3: 为 review-tasks 添加评分依据展示 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/review-tasks.md`
- **Description**: 修改 Scoring Breakdown 章节格式，添加"评分标准对照"和"扣分明细"列
- **Dependencies**: Task 1.3
- **Est. Complexity**: Medium
- **关联需求**: REQ-003

### Task 2.4: 为 review-python-code 添加评分依据展示 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/review-python-code.md`
- **Description**: 修改 Scoring Breakdown 章节格式，添加"评分标准对照"和"扣分明细"列
- **Dependencies**: Task 1.4
- **Est. Complexity**: Medium
- **关联需求**: REQ-003

### Task 2.5: 为 review-react-code 添加评分依据展示 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/review-react-code.md`
- **Description**: 修改 Scoring Breakdown 章节格式，添加"评分标准对照"和"扣分明细"列
- **Dependencies**: Task 1.5
- **Est. Complexity**: Medium
- **关联需求**: REQ-003

### Task 2.6: 实现建议项分数上限机制 (review-spec) ✅

- **Type**: Implementation
- **Files**: `templates/commands/review-spec.md`
- **Description**: 修改 Detailed Findings 章节，明确 Suggestions 类别最多影响 5 分，添加说明：修复所有 Critical 和 Warning 后应 ≥ 95 分
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low
- **关联需求**: REQ-002

### Task 2.7: 实现建议项分数上限机制 (其他 review 模板) [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/review-plan.md`, `templates/commands/review-tasks.md`, `templates/commands/review-python-code.md`, `templates/commands/review-react-code.md`
- **Description**: 为其他所有 review 模板添加建议项分数上限机制
- **Dependencies**: Task 2.2, Task 2.3, Task 2.4, Task 2.5
- **Est. Complexity**: Low
- **关联需求**: REQ-002

### Task 2.8: 实现评分验证机制 [P] ✅

- **Type**: Implementation
- **Files**: 所有 review 模板
- **Description**: 在 Quality Criteria 章节添加评分验证清单：验证每个扣分点都有明确依据、验证分数计算正确、验证分数与问题列表一致
- **Dependencies**: Task 2.1, Task 2.2, Task 2.3, Task 2.4, Task 2.5
- **Est. Complexity**: Medium
- **关联需求**: REQ-004

### Task 2.9: 实现质疑响应流程 [P] ✅

- **Type**: Implementation
- **Files**: 所有 review 模板
- **Description**: 在 review 模板末尾添加"Score Challenge Response"章节，定义标准的三步响应流程：提供依据 → 询问具体项 → 针对性重新评估
- **Dependencies**: Task 2.8
- **Est. Complexity**: Medium
- **关联需求**: REQ-005

## Phase 3: Generation Quality Enhancement

本阶段实现 REQ-006 和 REQ-007，改进生成模板。

### Task 3.1: 为 spec-to-plan 添加质量目标 ✅

- **Type**: Implementation
- **Files**: `templates/commands/spec-to-plan.md`
- **Description**: 在生成指令前添加 "Quality Targets" 章节，定义 plan 生成的质量标准，与 review-plan.md 的评分标准对齐
- **Dependencies**: Task 1.2, Task 2.2
- **Est. Complexity**: Medium
- **关联需求**: REQ-006, REQ-007

### Task 3.2: 为 plan-to-tasks 添加质量目标 [P] ✅

- **Type**: Implementation
- **Files**: `templates/commands/plan-to-tasks.md`
- **Description**: 在生成指令前添加 "Quality Targets" 章节，定义 tasks 生成的质量标准，与 review-tasks.md 的评分标准对齐
- **Dependencies**: Task 1.3, Task 2.3
- **Est. Complexity**: Medium
- **关联需求**: REQ-006, REQ-007

### Task 3.3: 验证生成与评分对齐 ✅

- **Type**: Validation
- **Files**: `templates/commands/spec-to-plan.md`, `templates/commands/plan-to-tasks.md`, `templates/commands/review-plan.md`, `templates/commands/review-tasks.md`
- **Description**: 对比质量目标和评分细则，确保使用相同术语、确保分类结构一致
- **Dependencies**: Task 3.1, Task 3.2
- **Est. Complexity**: Medium
- **关联需求**: REQ-007

## Phase 4: Testing & Validation

本阶段验证所有改进是否正确实现。

### Task 4.1: 单模板评分细则验证 [P] ✅

- **Type**: Testing
- **Files**: 无（验证任务）
- **Description**: 验证每个 review 模板是否包含完整的评分细则，格式是否统一
- **Dependencies**: Task 1.6
- **Est. Complexity**: Medium
- **验收标准**: 所有 5 个 review 模板都有完整且格式一致的评分细则
- **验证结果**: 5 个模板均包含 "Scoring Rubrics" 章节，使用统一的 Score Range/Criteria 表格格式和 Typical Deductions 列表

### Task 4.2: 评分依据完整性验证 [P] ✅

- **Type**: Testing
- **Files**: 无（验证任务）
- **Description**: 验证所有 review 模板的 Scoring Breakdown 是否包含评分标准对照和扣分明细
- **Dependencies**: Task 2.1, Task 2.2, Task 2.3, Task 2.4, Task 2.5
- **Est. Complexity**: Low
- **验收标准**: TC-002 通过
- **验证结果**: 5 个模板的 Scoring Breakdown 均包含 "Rubric Basis" 和 "Deduction Details" 列

### Task 4.3: 建议项影响上限验证 [P] ✅

- **Type**: Testing
- **Files**: 无（验证任务）
- **Description**: 验证所有 review 模板是否正确实现建议项分数上限（最多 5 分）
- **Dependencies**: Task 2.6, Task 2.7
- **Est. Complexity**: Low
- **验收标准**: TC-003 通过
- **验证结果**: 5 个模板均包含 "Suggestion Score Cap Rule" 和 "Suggestion Cap" 行

### Task 4.4: 质疑响应流程验证 ✅

- **Type**: Testing
- **Files**: 无（验证任务）
- **Description**: 验证所有 review 模板是否包含完整的质疑响应流程指导
- **Dependencies**: Task 2.9
- **Est. Complexity**: Low
- **验收标准**: TC-004 通过
- **验证结果**: 5 个模板均包含 "Score Challenge Response Protocol" 三步流程

### Task 4.5: 生成质量目标验证 [P] ✅

- **Type**: Testing
- **Files**: 无（验证任务）
- **Description**: 验证生成模板是否包含质量目标章节，且与 review 评分标准对齐
- **Dependencies**: Task 3.3
- **Est. Complexity**: Low
- **验收标准**: TC-005 通过
- **验证结果**: spec-to-plan.md 和 plan-to-tasks.md 均包含 "Quality Targets" 章节，分类名称与对应 review 模板一致

### Task 4.6: 模板一致性验证 ✅

- **Type**: Testing
- **Files**: 无（验证任务）
- **Description**: 验证所有 review 模板使用统一的评分格式
- **Dependencies**: Task 4.1, Task 4.2, Task 4.3
- **Est. Complexity**: Low
- **验收标准**: TC-006 通过
- **验证结果**: 所有模板使用统一的 Scoring Rubrics → Scoring Breakdown (with Rubric Basis + Deduction Details) → Score Validation Checklist → Score Challenge Response Protocol 结构

### Task 4.7: 边界情况验证 ✅

- **Type**: Testing
- **Files**: 无（验证任务）
- **Description**: 验证边界情况处理：无宪法项目、空文档、跨语言项目
- **Dependencies**: Task 4.6
- **Est. Complexity**: Medium
- **验收标准**: 边界情况处理正确
- **验证结果**: review-spec/plan/python-code/react-code 的 Constitution Alignment 均注明"无宪法时默认 100 分并重新分配权重"；所有模板通过 Language Preference 支持跨语言

## Execution Order

```

Phase 1: ┌─► Task 1.1 [P] ───┐
         │                    │
         ├─► Task 1.2 [P] ───┤
         │                    ├──► Task 1.6
         ├─► Task 1.3 [P] ───┤
         │                    │
         ├─► Task 1.4 [P] ───┤
         │                    │
         └─► Task 1.5 [P] ───┘
                                  │
Phase 2: ┌───────────────────────┴───────────────────────────┐
         │                                                   │
    ┌────┴────┐   ┌────┴────┐   ┌────┴────┐   ┌────┴────┐  │
    │         │   │         │   │         │   │         │  │
Task 2.1 [P] Task 2.2 [P] Task 2.3 [P] Task 2.4 [P] Task 2.5 [P]
    │         │   │         │   │         │   │         │  │
    └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘  │
         │             │             │             │       │
         └─────────────┴─────────────┴─────────────┴───────┤
                       │                                   │
                       ▼                                   ▼
                  Task 2.6                           Task 2.7 [P]
                       │                                   │
                       └─────────────┬─────────────────────┘
                                     │
                        ┌────────────┴────────────┐
                        │                         │
                     Task 2.8 [P]              Task 2.9 [P]
                        │                         │
Phase 3: ┌──────────────┴─────────────┬─────────────┴──────────────┐
         │                            │                            │
      Task 3.1                    Task 3.2 [P]                     │
         │                            │                            │
         └────────────┬───────────────┘                            │
                      │                                           │
                   Task 3.3                                       │
                      │                                           │
Phase 4: ┌─────────────┴──────────────────────────────────────────┘
         │
    ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐
    │         │ │         │ │         │ │         │ │         │
Task 4.1 [P] Task 4.2 [P] Task 4.3 [P] Task 4.4   Task 4.5 [P] Task 4.6 [P]
    │         │ │         │         │         │         │
    └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
         │            │            │            │            │
         └────────────┴────────────┴────────────┴────────────┘
                                      │
                                  Task 4.7

```

## Checkpoints

- [x] **Checkpoint 1**: After Phase 1 - 所有 5 个 review 模板的评分细则设计完成且格式统一
- [x] **Checkpoint 2**: After Phase 2 - 所有 review 模板实现 REQ-001 到 REQ-005（评分细则、依据展示、建议项上限、验证机制、质疑响应）
- [x] **Checkpoint 3**: After Phase 3 - 生成模板添加质量目标且与评分标准对齐
- [x] **Checkpoint 4**: After Phase 4 - 所有验收标准通过，边界情况处理正确

## File Modification Summary

| Phase | Files Modified | Purpose |
|-------|----------------|---------|
| 1 | `templates/commands/review-spec.md`<br>`templates/commands/review-plan.md`<br>`templates/commands/review-tasks.md`<br>`templates/commands/review-python-code.md`<br>`templates/commands/review-react-code.md` | 添加评分细则 |
| 2 | 同 Phase 1 | 添加评分依据展示、建议项上限、验证机制、质疑响应 |
| 3 | `templates/commands/spec-to-plan.md`<br>`templates/commands/plan-to-tasks.md` | 添加质量目标 |
| 4 | 无（验证任务） | 验证所有改进 |
