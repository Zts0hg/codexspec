# 工作流程

CodexSpec 将开发组织为可审查的检查点，并在不同会话之间保留用户已确认的真实意图。

## 工作流程概览

```text
项目原则
    |
想法 -> /specify -> requirements.md -> /generate-spec -> spec.md
                                                    -> /spec-to-plan -> plan.md
                                                                    -> /plan-to-tasks -> tasks.md
                                                                                       -> /implement-tasks
```

`requirements.md` 持久化需求讨论的结果，记录已确认需求、约束、决策、排除项、开放问题、用户依据和确认日志。

## 权威顺序与可追踪性

来源冲突时，命令使用以下优先级：

1. `requirements.md` 中已确认的条目
2. `spec.md`
3. 适用的项目原则与仓库事实
4. `plan.md`
5. `tasks.md`
6. 通用最佳实践

后序产物不得静默改写前序产物。需求使用稳定 ID，规格项通过 `Sources` 引用来源，计划与任务通过 `Covers` 声明覆盖关系。无法消解的冲突必须停止生成并请求用户确认。

仅包含 `spec.md` 的旧功能目录仍然兼容，但命令会明确提示无法追踪到原始用户讨论。

## 核心命令

| 阶段 | 命令 | 输出 |
|------|------|------|
| 1 | `/codexspec:constitution` | 项目原则 |
| 2 | `/codexspec:specify` | 已确认的 `requirements.md` |
| - | `/codexspec:clarify` | 更新需求，再同步规格 |
| 3 | `/codexspec:generate-spec` | `spec.md` 与 `review-spec.md` |
| 4 | `/codexspec:spec-to-plan` | `plan.md` 与 `review-plan.md` |
| 5 | `/codexspec:plan-to-tasks` | `tasks.md` 与 `review-tasks.md` |
| 6 | `/codexspec:analyze` | 只读的端到端可追踪分析 |
| 7 | `/codexspec:implement-tasks` | 实现结果 |

存在多个功能时应传入明确的功能目录或产物路径。命令不会隐式选择最新目录。

## 审查模型

审查输出分为三类：

- **忠实性缺陷**：与权威来源冲突，或遗漏必须覆盖的内容。
- **内在缺陷**：产物内部矛盾、不可验证或不可实施。
- **风险建议 / 设计机会**：没有当前缺陷证据的可选改进。

每个缺陷都必须给出证据、位置、偏差、影响和最小修复方式。同一根因的发现应合并。建议项不影响状态、分数，也不触发自动修复。

审查状态：

- `PASS`：没有严重、警告或轻微缺陷。
- `PASS_WITH_WARNINGS`：仅剩轻微缺陷。
- `NEEDS_REVISION`：仍存在警告。
- `BLOCKED`：严重冲突阻止可靠继续。

兼容分数由同一组已分类缺陷推导，不再按固定模板章节扣分。状态是权威结论，分数仅用于仍依赖数字的集成。

## 有界自动审查

生成命令会自动运行对应审查。它们只能修复有证据支持的缺陷，且最多自动修复并复审两轮。出现以下情况时会提前停止：

- 权威来源之间存在冲突；
- 修复会改变用户已确认的意图；
- 剩余内容属于建议而非缺陷；
- 已使用两轮自动修复。

任何时候都可以手动运行 `/codexspec:review-*` 生成新的审查报告。

## specify 与 clarify

| 方面 | `/codexspec:specify` | `/codexspec:clarify` |
|------|----------------------|----------------------|
| 目的 | 建立并确认初始意图 | 解决缺口或歧义 |
| 主要产物 | `requirements.md` | `requirements.md` |
| 规格处理 | 后续生成 | 确认修改后同步 |
| 开放问题 | 记录但不提升为需求 | 仅在用户确认后更新 |

## 条件 TDD

当确认需求、项目原则、计划或实现风险要求时，任务采用测试优先顺序。文档与配置工作可以直接实现。每个任务应产生一个可验证结果，但不要求只能修改一个文件。
