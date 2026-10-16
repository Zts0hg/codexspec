# 快速入门

<a id="30-second-quick-start"></a>

## 30 秒快速入门

安装 CodexSpec，并为你使用的助手初始化项目：

```bash
uv tool install codexspec

# Create a new project for Claude Code
codexspec init my-project --ai claude

# Or initialize an existing project for Codex
cd your-existing-project
codexspec init . --ai codex

# Use --ai both when you want both integrations
```

完成初始化后，在项目目录中启动你已安装的助手。两种助手使用相同的工作流，调用方式分别为：

| 助手 | 开始需求讨论 |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

如需定制项目原则，可以使用 `constitution`。确认最终需求摘要后，在命令返回的功能目录和工作区中继续开发。后续步骤见[核心工作流](../user-guide/workflow.md#core-workflow)。

使用 Codex 桌面应用？可以[让 Codex 安装并初始化你的项目](installation.md#install-with-the-codex-desktop-app)。

<a id="core-workflow"></a>

## 核心工作流

标准功能开发会依次生成以下产物，每一步都保留对前序依据的引用：

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

下面的示例使用 Claude 的 `/codexspec:` 前缀。在 Codex 中，将前缀换成 `$codexspec:` 即可，命令名称和参数不变。

| 步骤 | 命令 | 目的与产物 |
|------|---------|--------------------|
| 项目原则 | `/codexspec:constitution` | 创建/更新 `constitution.md`，并验证受影响的产物 |
| 需求 | `/codexspec:specify <idea>` | 讨论意图、确认最终摘要，并持久保存 `requirements.md` |
| 规格 | `/codexspec:generate-spec <feature-dir>` | 根据已确认需求编写 `spec.md`，并标明需求来源 |
| 系统设计 | `/codexspec:spec-to-design <feature-dir>` | 生成 `design.md`：组件、接口和关键设计决策 |
| 实现计划 | `/codexspec:design-to-plan <feature-dir>` | 编写 `plan.md`，安排实现阶段、先后顺序和验证方式 |
| 任务 | `/codexspec:plan-to-tasks <feature-dir>` | 编写可追溯、可验证的 `tasks.md`，并检查各文档是否一致 |
| 实现 | `/codexspec:implement-tasks <feature-dir>` | 执行任务、验证结果，并修复经独立核实的审查问题 |

将 `<feature-dir>` 替换为需求讨论阶段返回的功能目录。后续操作应在对应的 worktree 中执行，或明确传入该目录的路径，这样更换命令或会话后仍会处理同一个功能。

<a id="specify-clarify-and-analyze"></a>

### specify、clarify 与 analyze

- **specify** 用于开始需求讨论，也可重新讨论已有需求。需求摘要只有经用户明确确认后，才成为后续工作的依据。
- **clarify** 用于澄清已有需求和规格中的歧义。每次最多提出五个问题，检查范围涵盖四类问题；先更新 `requirements.md`，再同步修改 `spec.md`。
- **analyze** 检查需求 → 规格 → 设计 → 计划 → 任务的完整链路。如果根据上游依据能够确定下游文档应如何修正，就会自动修正；它绝不修改 `requirements.md`，无法解决的问题会明确报告。任务审查通过后会自动运行，结果供后续参考，不作为阻止实现的门禁。

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### 使用 Quick 处理小型变更

对于局部修复等范围小、边界明确的变更，可以使用 `quick`：

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick 会先确认并保存一份精简的需求摘要，再依次调用生成命令及相应审查，推进规格、计划、任务和实现。如果变更涉及较大范围，或仍有产品和设计选择尚未确定，应使用标准工作流。需要用户作出新决定时，Quick 会暂停。

<a id="workflow-automation"></a>

### 工作流自动化

`workflow.auto_next` 默认为 **false**。如果当前工作区将其设置为 `true`，确认最终需求后就会自动进入规格阶段。各生成阶段得到 `PASS` 或 `PASS_WITH_WARNINGS` 时会继续推进，得到 `NEEDS_REVISION` 或 `BLOCKED` 时则停止。`implement-tasks` 是最后一个阶段。

自动修正文档时，只处理已经验证的缺陷，且修正方式必须有上游依据支持；最多进行两轮修复和重新审查。建议另行列出。实现阶段的审查与修复遵循另一套完成标准，详见下文。

详细约定见[工作流指南](../user-guide/workflow.md)。

<a id="project-structure"></a>

## 项目结构

初始化会安装共用资源，以及所选助手需要的集成文件：

```text
my-project/
├── .codexspec/
│   ├── config.yml
│   ├── memory/
│   │   └── constitution.md
│   ├── profile/
│   │   ├── constraints/
│   │   ├── conventions/
│   │   ├── pitfalls/
│   │   ├── decisions/
│   │   ├── strategies/
│   │   └── runbooks/
│   ├── review-code/              # Shared review standards
│   ├── specs/
│   │   └── <feature-id>-<name>/   # Added by feature workflows
│   │       ├── requirements.md
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── plan.md
│   │       ├── tasks.md
│   │       ├── review-*.md
│   │       └── checklists/       # When requested
│   ├── templates/docs/
│   └── scripts/                 # Platform helpers and commit runtime
├── .claude/commands/codexspec/   # --ai claude or both
├── .agents/skills/              # --ai codex or both
├── CLAUDE.md                    # Claude project context
└── AGENTS.md                    # Codex project context
```

共享蓝图保存在专用的 auto-dev worktree 中，各常规 checkout 不会分别保存可编辑副本。手动审阅项目知识时生成的草稿不纳入 Git。
