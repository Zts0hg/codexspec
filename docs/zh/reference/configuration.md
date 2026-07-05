# 配置

## 配置文件位置

`.codexspec/config.yml`

## 配置 Schema

```yaml
version: "1.0"

language:
  output: "zh-CN"        # 基础语言；以下三项回退到它，再到 "en"
  interaction: "zh-CN"   # LLM 对话 + codexspec CLI 输出（可选 → 默认为 output）
  document: "en"         # 生成的 requirements/spec/plan/tasks（可选 → 默认为 output）
  commit: "en"           # git 提交信息（可选 → 默认为 output）
  templates: "en"        # 保持为 "en"

project:
  ai: "claude"
  created: "2025-02-15"

workflow:
  auto_next: false       # 在工作流各阶段之间自动推进（opt-in）
```

## 语言设置

CodexSpec 把语言拆分为四个可独立配置的维度。`output` 是基础；`interaction`、`document` 与 `commit` 覆盖它，并在未设置时回退到它（再到 `en`）。这样你就可以，比如用一种语言与 Claude 对话，而把生成的工件或提交信息保留在另一种语言里。

| 维度 | 键 | 初始化时设置 | 之后设置 | 控制 | 回退到 |
|------|----|-------------|-----------|------|--------|
| Output（基础） | `output` | `--lang` | `config --set-lang` | 其他三项的基础 | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | LLM 对话 + CLI 输出 | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | 生成的 spec/plan/tasks | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | git 提交信息 | output → `en` |
| Templates | `templates` | — | — | 命令模板来源（始终为 `en`） | — |

**支持的取值：** 见[国际化](../user-guide/i18n.md#supported-languages)

### `language.output`

基础输出语言。其他维度在未显式设置时回退到它。

### `language.interaction`

你与 LLM 对话所用的语言，以及 `codexspec` CLI 终端输出所用的语言。可选——默认为 `output`。

### `language.document`

生成的工件文件（requirements/spec/plan/tasks）所用的语言。可选——默认为 `output`。

### `language.commit`

git 提交信息所用的语言。可选——默认为 `output`。

### `language.templates`

模板语言。为兼容性应保持为 `"en"`。

## 项目设置

### `project.ai`

正在使用的 AI 助手。决定 `codexspec init` 会落盘哪些 agent 上下文文件：

- `claude`（默认）——写入 `CLAUDE.md`（以及 `.claude/commands/`）。
- `codex`——改为写入 `AGENTS.md` 和 `.agents/skills/`。
- `both`——写入上述全部内容，让项目同时适配 Claude Code 与 Codex CLI。

`CLAUDE.md` 始终会被创建（这样项目仍可从 Claude Code 使用）；`AGENTS.md` 与 `.agents/skills/` 仅在 `project.ai` 为 `codex` 或 `both` 时创建。

### `project.created`

项目初始化的日期。

## 工作流设置

### `workflow.auto_next`

控制 Requirements-First SDD 流水线是否在当前阶段通过之后**自动推进**到下一个工作流阶段，而不需要你手动触发下一条命令。

- **默认：** `false`（opt-in）。只有字面值 `true` 才会启用自动推进。
- **切换 / 设置：** `codexspec config --auto-next`（裸标志切换当前值；传入 `on`/`off` 显式设置）。

**链路：**

```
specify → generate-spec → spec-to-plan → plan-to-tasks → implement-tasks
```

**通过门：**

- `generate-spec`、`spec-to-plan`、`plan-to-tasks`：命令内置的评审闭环需报告 Overall Status 为 `PASS` 或 `PASS_WITH_WARNINGS`。
- `specify`：没有评审闭环，因此通过门是你对需求探索已完成的显式确认（指**最终**的阶段摘要，而不是每一次中间摘要）。
- `implement-tasks`：终端阶段——其后不会自动触发任何内容。

当评审闭环报告 `NEEDS_REVISION` 或 `BLOCKED` 时，链路停下并把控制权交还给你。每次推进之前，agent 会输出一条提示行（例如：`auto_next: review passed → invoking /codexspec:spec-to-plan`）。
