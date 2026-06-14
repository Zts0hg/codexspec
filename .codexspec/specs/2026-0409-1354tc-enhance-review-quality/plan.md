# Implementation Plan: CodexSpec Review 评分机制与生成质量优化

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Template Format | Markdown | - | 所有 slash command 模板使用 Markdown + YAML frontmatter |
| Template Engine | Claude Code | - | 模板由 Claude Code 解析并执行 |
| Output Language | Multi-language | - | 支持通过 config.yml 配置输出语言 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 通过明确的评分细则提升模板生成质量 |
| Documentation | ✅ | 评分依据展示机制改进文档透明度 |
| Architecture | ✅ | 遵循模板修改规范，仅修改源模板 |
| Slash Command Template Modification Rules | ✅ | 所有修改仅在 `templates/commands/` 目录下进行 |

## 3. Architecture Overview

本项目是对现有 slash command 模板的质量改进，不涉及新代码开发。架构核心是**模板评分体系**的标准化和**生成-评分一致性**的保证。

```
┌─────────────────────────────────────────────────────────────────┐
│                    CodexSpec Template System                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │                  Generation Templates                  │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │     │
│  │  │spec-to-plan  │  │plan-to-tasks │  │  generate-*  │  │     │
│  │  │    .md       │  │     .md      │  │     .md      │  │     │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │     │
│  │         │                 │                 │           │     │
│  │         └─────────────────┴─────────────────┘           │     │
│  │                           │                             │     │
│  │                    ┌──────▼──────┐                      │     │
│  │                    │ Quality      │                      │     │
│  │                    │ Targets      │ ← ADD THIS           │     │
│  │                    │ (NEW)        │                      │     │
│  │                    └──────────────┘                      │     │
│  └────────────────────────────────────────────────────────┘     │
│                           │                                      │
│                           ▼                                      │
│  ┌────────────────────────────────────────────────────────┐     │
│  │                   Review Templates                      │     │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │     │
│  │  │review-spec   │  │review-plan   │  │review-tasks  │  │     │
│  │  │    .md       │  │     .md      │  │     .md      │  │     │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │     │
│  │         │                 │                 │           │     │
│  │         └─────────────────┴─────────────────┘           │     │
│  │                           │                             │     │
│  │                    ┌──────▼──────┐                      │     │
│  │                    │ Scoring     │                      │     │
│  │                    │ Rubrics     │ ← ADD THIS           │     │
│  │                    │ (NEW)        │                      │     │
│  │                    └──────┬──────┘                      │     │
│  │                           │                             │     │
│  │                    ┌──────▼──────┐                      │     │
│  │                    │ Score       │                      │     │
│  │                    │ Justification│ ← ADD THIS          │     │
│  │                    │ (NEW)        │                      │     │
│  │                    └──────────────┘                      │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │  Improved User         │
              │  Experience            │
              │  - Transparent Scores  │
              │  - Less Iteration      │
              │  - Objective Review    │
              └────────────────────────┘
```

## 4. Component Structure

```
templates/commands/
├── review-spec.md         # Spec review template - MODIFY
├── review-plan.md         # Plan review template - MODIFY
├── review-tasks.md        # Tasks review template - MODIFY
├── review-python-code.md  # Python code review template - MODIFY
├── review-react-code.md   # React code review template - MODIFY
├── spec-to-plan.md        # Spec to plan generation - MODIFY
└── plan-to-tasks.md       # Plan to tasks generation - MODIFY
```

## 5. Module Dependency Graph

```
┌────────────────────────────────────────────────────────────┐
│                    Shared Components                        │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │           Scoring Rubrics (Shared)               │     │
│  │  - 评分细则定义（可复用于所有 review 模板）       │     │
│  └──────────────────────────────────────────────────┘     │
│                          │                                 │
│         ┌────────────────┼────────────────┐               │
│         ▼                ▼                ▼               │
│  ┌───────────┐    ┌───────────┐    ┌───────────┐          │
│  │review-spec│    │review-plan│    │review-tasks│          │
│  └───────────┘    └───────────┘    └───────────┘          │
│         │                │                │               │
│         └────────────────┼────────────────┘               │
│                          ▼                                 │
│  ┌──────────────────────────────────────────────────┐     │
│  │        Quality Targets (Shared)                   │     │
│  │  - 生成质量目标定义（可复用于所有生成模板）         │     │
│  └──────────────────────────────────────────────────┘     │
│                          │                                 │
│         ┌────────────────┼────────────────┐               │
│         ▼                ▼                ▼               │
│  ┌───────────┐    ┌───────────┐                            │
│  │spec-to-   │    │plan-to-   │                            │
│  │  plan     │    │  tasks     │                            │
│  └───────────┘    └───────────┘                            │
└────────────────────────────────────────────────────────────┘
```

## 6. Module Specifications

### Module: Review Scoring Rubrics (Shared Component)

- **Responsibility**: 定义统一的评分标准和细则
- **Dependencies**: 无（独立组件）
- **Interface**: 可被所有 review 模板引用的评分细则片段
- **Files**:
  - `templates/commands/review-spec.md` - 包含评分细则
  - `templates/commands/review-plan.md` - 包含评分细则
  - `templates/commands/review-tasks.md` - 包含评分细则
  - `templates/commands/review-python-code.md` - 包含评分细则
  - `templates/commands/review-react-code.md` - 包含评分细则

### Module: Score Justification Component (Shared Component)

- **Responsibility**: 定义评分依据展示格式
- **Dependencies**: Scoring Rubrics
- **Interface**: 统一的评分依据报告模板
- **Files**: 所有 review 模板（同上）

### Module: Quality Targets Component (Shared Component)

- **Responsibility**: 定义生成质量目标清单
- **Dependencies**: 无（独立组件）
- **Interface**: 可被所有生成模板引用的质量目标片段
- **Files**:
  - `templates/commands/spec-to-plan.md`
  - `templates/commands/plan-to-tasks.md`

## 7. API Contracts (Template Interface)

### Template: Review Scoring Interface

**Input**:

```markdown
- 被审查的文档（spec/plan/tasks）
- 项目宪法（constitution.md，如果存在）
```

**Output**:

```markdown
- Overall Status: Pass/Needs Work/Fail
- Quality Score: X/100（带完整评分依据）
- Scoring Breakdown:
  - 每个类别的评分标准对照
  - 每个类别的扣分明细（如有）
  - 加权计算过程
- Issues categorized by severity
```

**Scoring Rules**:

```yaml
Critical Issues: 影响分数，每个扣 10-20 分
Warnings: 影响分数，每个扣 5-10 分
Suggestions: 最多影响 5 分（或分离显示）
```

### Template: Generation Quality Interface

**Input**:

```markdown
- 源文档（spec/plan）
- 项目宪法（constitution.md，如果存在）
```

**Output**:

```markdown
- 生成的目标文档（plan/tasks）
- 生成过程中的质量自检报告
```

**Quality Targets**:

```yaml
Completeness: 所有必需部分存在且内容充实
Clarity: 无模糊语言，术语明确
Consistency: 无内部矛盾
Testability: 所有需求可测试
```

## 8. Implementation Phases

### Phase 1: Foundation - 评分细则设计

创建统一的评分细则（Rubrics），定义各评分类别的评分标准：

- [ ] **Task 1.1**: 设计 review-spec.md 的评分细则
  - Completeness 评分标准（0-100 分）
  - Clarity 评分标准（0-100 分）
  - Consistency 评分标准（0-100 分）
  - Testability 评分标准（0-100 分）
  - Constitution Alignment 评分标准（0-100 分）

- [ ] **Task 1.2**: 设计 review-plan.md 的评分细则
  - Spec Alignment 评分标准
  - Tech Stack 评分标准
  - Architecture Quality 评分标准
  - Phase Planning 评分标准
  - Constitution Alignment 评分标准

- [ ] **Task 1.3**: 设计 review-tasks.md 的评分细则
  - Plan Coverage 评分标准
  - TDD Compliance 评分标准
  - Dependency & Ordering 评分标准
  - Task Granularity 评分标准
  - Parallelization & Files 评分标准

- [ ] **Task 1.4**: 设计 review-python-code.md 和 review-react-code.md 的评分细则

### Phase 2: Core Implementation - Review 模板改进

实现 REQ-001 到 REQ-005：

- [ ] **Task 2.1**: 添加评分细则到所有 review 模板（REQ-001）
  - 在每个 review 模板中添加 "Scoring Rubrics" 章节
  - 定义每个类别的满分标准
  - 定义扣分规则和具体扣分值
  - 提供评分示例

- [ ] **Task 2.2**: 实现建议项分数上限机制（REQ-002）
  - 修改所有 review 模板的 "Detailed Findings" 章节
  - 明确 Suggestions 类别最多影响 5 分
  - 添加说明：修复所有 Critical 和 Warning 后应 ≥ 95 分

- [ ] **Task 2.3**: 实现评分依据展示（REQ-003）
  - 修改 Scoring Breakdown 章节格式
  - 添加"评分标准对照"列
  - 添加"扣分明细"列
  - 确保用户可追溯每个分数来源

- [ ] **Task 2.4**: 实现评分验证机制（REQ-004）
  - 在 Quality Criteria 章节添加评分验证清单
  - 验证每个扣分点都有明确依据
  - 验证分数计算正确
  - 验证分数与问题列表一致

- [ ] **Task 2.5**: 实现质疑响应流程（REQ-005）
  - 在 review 模板末尾添加"Score Challenge Response"章节
  - 定义标准的三步响应流程
  - 提供依据展示模板
  - 提供重新评估指导

### Phase 3: Generation Quality Enhancement

实现 REQ-006 和 REQ-007：

- [ ] **Task 3.1**: 添加质量目标到 spec-to-plan.md（REQ-006）
  - 在生成指令前添加 "Quality Targets" 章节
  - 定义 plan 生成的质量标准
  - 与 review-plan.md 的评分标准对齐

- [ ] **Task 3.2**: 添加质量目标到 plan-to-tasks.md（REQ-006）
  - 在生成指令前添加 "Quality Targets" 章节
  - 定义 tasks 生成的质量标准
  - 与 review-tasks.md 的评分标准对齐

- [ ] **Task 3.3**: 验证生成与评分对齐（REQ-007）
  - 对比质量目标和评分细则
  - 确保使用相同术语
  - 确保分类结构一致

### Phase 4: Testing & Validation

- [ ] **Task 4.1**: 单模板测试
  - 测试每个修改后的 review 模板
  - 验证评分依据完整性（TC-002）
  - 验证建议项影响上限（TC-003）

- [ ] **Task 4.2**: 集成测试
  - 测试质疑响应流程（TC-004）
  - 测试生成质量改进（TC-005）
  - 测试模板一致性（TC-006）

- [ ] **Task 4.3**: 边界情况测试
  - 测试无宪法项目
  - 测试空文档或不完整文档
  - 测试跨语言项目

## 9. Technical Decisions

### Decision 1: 评分细则的详细程度

- **Choice**: 为每个评分类别提供详细的评分细则，包括满分标准、典型扣分场景和具体扣分值
- **Rationale**: 用户反馈的核心问题是"评分不透明"，详细的评分细则是解决问题的根本
- **Alternatives**:
  - 仅提供简单的评分描述（不够透明）
  - 使用 AI 自动评估而不定义细则（缺乏一致性）
- **Trade-offs**: 增加了模板长度，但显著提升了用户体验和评分一致性

### Decision 2: 建议项分数处理方式

- **Choice**: Suggestions (Nice to Have) 最多影响 5 分，在 Scoring Breakdown 中单独标注
- **Rationale**: 平衡"合理满分路径"和"持续改进动力"
- **Alternatives**:
  - 建议项完全不影响分数（可能导致用户忽略改进建议）
  - 建议项按数量扣分（导致修复全部问题仍难高分）
- **Trade-offs**: 保留了改进建议的价值，同时确保修复主要问题后能获得高分

### Decision 3: 质疑响应流程设计

- **Choice**: 三步流程：提供依据 → 询问具体项 → 针对性重新评估
- **Rationale**: 既保持评分客观性，又响应用户合理疑问
- **Alternatives**:
  - 直接按用户要求修改分数（丧失客观性）
  - 拒绝修改任何分数（不够灵活）
- **Trade-offs**: 需要额外模板内容，但建立了可信赖的评分机制

### Decision 4: 质量目标的实现方式

- **Choice**: 在生成模板中添加 "Quality Targets" 章节，作为 LLM 生成前的参考
- **Rationale**: 简单有效，不需要修改模板引擎
- **Alternatives**:
  - 创建独立的质量检查模板（增加复杂度）
  - 使用外部工具验证（不适用本项目）
- **Trade-offs**: 依赖 LLM 遵循指导，但与现有架构一致

## 10. Implementation Notes

### 文件修改清单

| 文件 | 修改类型 | 关联需求 |
|------|----------|----------|
| `templates/commands/review-spec.md` | 修改 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005 |
| `templates/commands/review-plan.md` | 修改 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005 |
| `templates/commands/review-tasks.md` | 修改 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005 |
| `templates/commands/review-python-code.md` | 修改 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005 |
| `templates/commands/review-react-code.md` | 修改 | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005 |
| `templates/commands/spec-to-plan.md` | 修改 | REQ-006, REQ-007 |
| `templates/commands/plan-to-tasks.md` | 修改 | REQ-006, REQ-007 |

### 关键设计原则

1. **模板修改规范**：仅修改 `templates/commands/` 下的源模板，不修改 `.claude/commands/codexspec/` 下的活跃命令
2. **向后兼容**：改进后的模板应与现有工作流兼容
3. **语言支持**：所有新增内容应支持项目配置的输出语言
