# CodexSpec 使用案例：为项目添加 PR 揑息生成功能

> 本文档记录了使用 CodexSpec 工具链为 CodexSpec 项目本身添加新功能的完整过程，展示了 Spec-Driven Development (SDD) 的实际应用。

## 概述

**目标功能**: 添加 `/codexspec.pr` 命令，用于生成结构化的 GitHub PR / GitLab MR 描述信息。

**开发流程**: `specify → generate-spec → review-spec → clarify → spec-to-plan`

**关键特点**: 在开发过程中发现需求问题并通过 `clarify` 命令进行调整，展示了 SDD 的灵活性。

---

## 阶段 1: 鎟始需求澄清 (`/codexspec.specify`)

### 用户初始输入

```
我希望为项目增加一个功能：提供一个新的git相关的指令用来生成准确详细且符合规范的github pr信息（或者mr信息，针对gitlab）。以下是我在其他项目中使用过的两个pr指令内容，提供给你参考。

[参考示例 1 - 结构化描述]
现在，请扮演项目维护者的角色，基于我们到目前为止的所有工作，为这次提交撰写一份清晰的Pull Request描述。
PR描述需要面向团队的其他审查者，包含以下几个部分：
1. 背景（Context）
2. 实现方案（Implementation）
3. 测试（Testing）
4. 如何手动验证（How to Verify）

[参考示例 2 - 简单描述]
请你根据当前分支与origin/main分支的代码差异，使用markdown格式整理一份符合git规范的merge request的title和description。（使用中文描述）
```

### 澄清过程

**Q1: 输出语言**
- 选项: 跟随项目配置 / 中文 / 自动检测
- **用户选择**: 跟随项目配置 (当前: en)

**Q2: 平台支持**
- 选项: 同时支持 GitHub 和 GitLab / 仅 GitHub / 自动检测平台
- **用户选择**: 自动检测平台

**Q3: PR 描述内容**
- 选项: 详细结构化描述 / 简洁描述 / 可自定义模板
- **用户选择**: 详细结构化描述 (推荐)

**Q4: 触发条件**
- 选项: 当前分支 vs origin/main / 未推送的 commits / 可指定目标分支
- **用户选择**: 可指定目标分支

**Q5: Spec 来源**
- 选项: 优先使用 spec.md / 仅用 git 信息 / 综合所有来源
- **用户选择**: 综合所有来源 (推荐)

**Q6: 命名**
- 选项: codexspec.pr / codexspec.create-pr / codexspec.create-mr
- **用户选择**: codexspec.pr (推荐)

**Q7: 无 Spec 处理**
- 选项: 继续生成，跳过背景 / 提示用户先创建 spec / 警告并继续
- **用户选择**: 继续生成，跳过背景

**Q8: 输出方式**
- 选项: 终端输出 / 保存到文件 / 终端 + 可选文件
- **用户选择**: 终端 + 可选文件 (推荐)

**Q9: 默认章节**
- 选项: 背景, 实现方案, 测试, 如何验证 (全选)
- **用户选择**: 全部四个章节

**Q10: 指令参数**
- **用户选择**: 所有参数都是可选参数
  - `--target-branch`: 默认 origin/main
  - `--output`: 不指定时默认只在终端输出
  - `--sections`: 不指定时按照默认
  - `--no-spec`: 跳过 spec.md 文件查找

### 语言配置修正

**用户反馈**: 语言应该跟 `/commit` 指令一样优先根据 `config.yml` 中的 `language.commit` 参数，如果没有 `language.commit` 参数设置，才根据 `language.output`。

**更新后的需求摘要**:
```
语言优先级: language.commit > language.output > English (默认)
```

---

## 阶段 2: 生成规格文档 (`/codexspec.generate-spec`)

### 生成的文档结构

生成的 `spec.md` 包含以下部分:

- **Overview**: 功能概述
- **Goals**: 4 个目标
- **User Stories**: 4 个用户故事及验收标准
- **Functional Requirements**: 8 个需求 (REQ-001 到 REQ-008)
- **Command Parameters**: 4 个参数定义
- **Non-Functional Requirements**: 3 个需求 (性能、兼容性、错误处理)
- **Acceptance Criteria (Test Cases)**: 10 个测试用例
- **Edge Cases**: 6 个边界情况
- **Output Format Example**: GitHub PR 和 GitLab MR 示例
- **Out of Scope**: 明确排除的功能
- **Dependencies**: 依赖项
- **Related Commands**: 相关命令

### 关键需求摘录

```markdown
### REQ-003: Language Configuration
The command shall determine output language in the following priority order:
1. `language.commit` in `.codexspec/config.yml` (highest priority)
2. `language.output` in `.codexspec/config.yml` (fallback)
3. English (default if no configuration)
```

---

## 阶段 3: 规格审查 (`/codexspec.review-spec`)

### 审查结果

- **总体状态**: ✅ 通过
- **质量评分**: 92/100
- **准备状态**: Ready for Planning

### 发现的问题

**警告 (Should Fix)**:
1. **SPEC-001**: 测试文件发现逻辑未明确指定
2. **SPEC-002**: 多个 spec.md 时选择"最近修改"可能不准确

**建议 (Nice to Have)**:
1. 考虑添加 `--title` 参数
2. 添加输出格式验证需求
3. 考虑 GitHub Enterprise URL 模式支持

### 审查报告保存位置

`.codexspec/specs/001-pr-description-generator/review-spec.md`

---

## 阶段 4: 需求澄清与调整 (`/codexspec.clarify`) ⚠️ 关键转折

### 发现的问题

**用户反馈**:
> 我意识到关于 spec.md 的使用有一个问题。比如用户事实上在进行一个很小的改动，所以没有使用 codexspec 的标准化流程 specify->plan->tasks->implement，而是直接进行对话修改或者是 claude code 内置的 plan mode，然后在修改完毕之后希望单独调用 codexspec 的命令来生成规范的 pr 信息。这种情况直接默认使用最近修改过的 spec.md 就可能使用了之前的与本次修改无关的 spec.md 内容。

### 澄清问答过程

**Q1: Spec 选择策略**

**Context**: 当前 EC-004 规定"多个 spec.md → 使用最近修改的"。但用户进行小改动时可能没有使用 SDD 流程，最近的 spec.md 可能与当前修改无关。

| Option | Description |
|--------|-------------|
| A | 默认不使用 spec.md，除非用户明确指定 `--spec` 参数 |
| B | 基于分支名匹配 |
| C | 提示用户选择 |
| D | 基于文件变更匹配 |

**用户选择**: Option A
**理由**: 避免错误引用，`--spec` 参数让需要 SDD 集成的用户显式指定。

---

**Q2: Spec 内容提取策略**

**Context**: 当用户使用 `--spec` 时，如果 spec.md 结构不完整怎么办？

| Option | Description |
|--------|-------------|
| A | 尽力提取，跳过缺失部分 |
| B | 警告并跳过 Context |
| C | 要求完整结构，否则报错 |

**用户选择**: Option A
**理由**: 避免因 spec 格式问题阻止工作流。

---

**Q3: 测试文件发现**

**Context**: Testing 部分如何发现测试文件？

| Option | Description |
|--------|-------------|
| A | 常见目录模式 (tests/, test/) |
| B | 语言无关启发式 (目录 + 文件名模式) |
| C | 不主动发现，仅从 commit 消息推断 |

**用户选择**: Option B
**理由**: 覆盖不同语言的多种项目结构。

---

**Q4: PR 标题生成**

**Context**: PR 标题应该如何生成？

| Option | Description |
|--------|-------------|
| A | 分支名解析优先 |
| B | 首个 commit 消息优先 |
| C | 综合生成 (git diff + 分支名 + commit 消息) |

**用户选择**: Option C
**用户理由**: 第一个 commit 可能只是一小部分改动；分支名对命名规范要求高。既然有大量 git 信息和 code changes 可以参考，综合分析更准确。

---

**Q5: 验证命令生成**

**Context**: "How to Verify" 部分如何生成验证命令?

| Option | Description |
|--------|-------------|
| A | 通用模板 |
| B | 项目检测 (pyproject.toml → pytest, package.json → npm test) |
| C | 从 commit 消息推断 |

**用户选择**: Option B
**理由**: 项目检测能生成更实用的验证命令。

---

### 澄清会话总结

| 问题 | 决策 | 影响 |
|------|------|------|
| Spec 选择策略 | Opt-in via `--spec` | REQ-007, EC-004, 参数表 |
| Spec 内容提取 | 最佳努力提取 | REQ-005b, EC-004c |
| 测试文件发现 | 语言无关启发式 | REQ-006b |
| PR 标题生成 | 综合分析 | REQ-008a |
| 验证命令生成 | 项目文件检测 | REQ-010 |

### 关键变更: 参数逻辑反转

```
原设计: --no-spec (跳过 spec)
新设计: --spec (启用 spec，opt-in)
```

---

## 阶段 5: 技术实现计划 (`/codexspec.spec-to-plan`)

### 计划概述

**实现方式**: Markdown 模板文件 (与 `/codexspec.commit` 一致)

**无新依赖** - 特性通过 slash command 模板实现，不需要 Python 代码。

### 技术决策摘要

| 决策 | 选择 | 理由 |
|------|------|------|
| 实现方式 | Markdown 模板 | 与现有命令一致，易维护 |
| 语言优先级 | commit > output > en | 与 `/commit` 命令一致 |
| 平台检测 | Remote URL 解析 | 简单可靠 |
| Spec 集成 | Opt-in (`--spec`) | 避免错误引用 |
| 内容提取 | 最佳努力 | 不阻塞工作流 |
| 测试发现 | 目录+文件名模式 | 语言无关 |
| 标题生成 | 综合分析 | 最准确 |
| 命令检测 | 项目文件检测 | 更实用 |
| 输出模式 | 终端优先，可选文件 | 灵活 |

### 实现阶段

1. **Phase 1**: 模板创建 (YAML frontmatter, 语言配置, Git 上下文)
2. **Phase 2**: 核心功能 (Spec 集成, 测试发现, 命令检测, 标题生成)
3. **Phase 3**: 边界情况处理
4. **Phase 4**: 测试
5. **Phase 5**: 文档更新

### 文件清单

**创建**:
- `templates/commands/pr.md`

**修改**:
- `CLAUDE.md` - 添加命令描述
- `README.md` - 添加命令到列表

**测试**:
- `tests/test_pr_template.py`

---

## 完整流程图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CodexSpec SDD 开发流程                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.specify                                                      │
│  ├─ 通过问答澄清需求                                                     │
│  ├─ 用户提供了参考示例                                                   │
│  └─ 10 个问题，覆盖语言、平台、内容、参数等                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.generate-spec                                                │
│  ├─ 生成完整的 spec.md                                                   │
│  ├─ 4 个用户故事，8 个功能需求，10 个测试用例                             │
│  └─ 保存到 .codexspec/specs/001-pr-description-generator/spec.md         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.review-spec                                                  │
│  ├─ 质量评分: 92/100                                                     │
│  ├─ 发现 2 个警告 (测试文件发现、多 spec 处理)                            │
│  └─ 状态: 通过，可进入规划阶段                                           │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.clarify  ⚠️ 关键调整                                        │
│  ├─ 用户发现实际使用场景问题                                             │
│  ├─ 5 个澄清问题，全部得到回答                                           │
│  ├─ 关键变更: --no-spec → --spec (opt-in)                                │
│  └─ 新增 5 个需求 (REQ-005b, 006b, 008a, 010, 更新 007)                  │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  /codexspec.spec-to-plan                                                 │
│  ├─ 更新技术实现计划                                                     │
│  ├─ 9 个技术决策，包含 5 个新增决策                                      │
│  ├─ 5 个实现阶段                                                         │
│  └─ 保存到 .codexspec/specs/001-pr-description-generator/plan.md         │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  后续步骤 (未在本 session 完成)                                          │
│  ├─ /codexspec.review-plan - 验证计划质量                                │
│  ├─ /codexspec.plan-to-tasks - 分解为可执行任务                          │
│  └─ /codexspec.implement-tasks - 执行实现                                │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 关键学习点

### 1. 澄清阶段的价值

本案例展示了 `clarify` 命令的关键作用：
- **用户在使用过程中发现实际问题** - 小改动场景下 spec.md 的误用风险
- **通过澄清问答解决设计缺陷** - 从自动检测改为 opt-in 模式
- **需求变更被系统记录** - 所有变更保存在 spec.md 的 Clarifications 部分

### 2. SDD 流程的灵活性

- 不是线性流程，可以在任何阶段返回调整
- `clarify` 可以在 `review-spec` 之后、`spec-to-plan` 之前插入
- 规格文档和技术计划都会被更新以反映变更

### 3. 参数设计的演变

```
初始设计:
  --no-spec: 跳过 spec.md (默认使用)

最终设计:
  --spec: 启用 spec.md (默认不使用)
```

这个变化反映了从"默认 SDD 工作流"到"支持非 SDD 工作流"的设计转变，使工具更加通用。

### 4. 文档产出

| 阶段 | 产出文件 | 内容 |
|------|----------|------|
| generate-spec | spec.md | 完整规格文档 |
| review-spec | review-spec.md | 质量审查报告 |
| clarify | (更新 spec.md) | 澄清记录 + 需求更新 |
| spec-to-plan | plan.md | 技术实现计划 |

---

## 附录: 命令使用速查

```bash
# 1. 初始需求澄清
/codexspec.specify

# 2. 生成规格文档
/codexspec.generate-spec

# 3. 审查规格质量
/codexspec.review-spec

# 4. 澄清/调整需求 (可选，发现问题后使用)
/codexspec.clarify [问题描述]

# 5. 生成技术计划
/codexspec.spec-to-plan

# 6. 审查计划质量 (可选)
/codexspec.review-plan

# 7. 分解为任务
/codexspec.plan-to-tasks

# 8. 执行实现
/codexspec.implement-tasks
```

---

*本文档由 CodexSpec SDD 工作流自动生成，记录了真实的开发对话过程。*
