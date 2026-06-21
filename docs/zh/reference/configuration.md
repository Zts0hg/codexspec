# 配置

## 配置文件位置

`.codexspec/config.yml`

## 配置模式

```yaml
version: "1.0"

language:
  output: "zh-CN"        # 基础语言；以下三项回退到它，再到 "en"
  interaction: "zh-CN"   # LLM 对话 + codexspec CLI 输出（可选 → 默认为 output）
  document: "en"         # 生成的 requirements/spec/plan/tasks（可选 → 默认为 output）
  commit: "en"           # git 提交信息（可选 → 默认为 output）
  templates: "en"        # 模板语言（保持为 "en"）

project:
  ai: "claude"      # AI 助手
  created: "2025-02-15"
```

## 语言设置

CodexSpec 将语言拆分为四个可独立配置的维度。`output` 是基础；`interaction`、`document` 和 `commit` 覆盖它，并在未设置时回退到它（再到 `en`）。这样你就可以例如用一种语言与 Claude 对话，同时把生成的产物或提交信息保留在另一种语言。

| 维度 | 键 | 初始化时设置 | 之后设置 | 控制 | 回退到 |
|------|----|-------------|-----------|------|--------|
| Output（基础） | `output` | `--lang` | `config --set-lang` | 其他三项的基础 | `en` |
| Interaction | `interaction` | `--interaction-lang` | `config --set-interaction-lang` | LLM 对话 + CLI 输出 | output → `en` |
| Document | `document` | `--document-lang` | `config --set-document-lang` | 生成的 spec/plan/tasks | output → `en` |
| Commit | `commit` | `--commit-lang` | `config --set-commit-lang` | git 提交信息 | output → `en` |
| Templates | `templates` | — | — | 命令模板来源（始终为 `en`） | — |

**支持的值：** 参见[国际化](../user-guide/i18n.md#supported-languages)

### `language.output`

基础输出语言。其他维度在未显式设置时回退到它。

### `language.interaction`

你与 LLM 之间对话的语言，以及 `codexspec` CLI 终端输出的语言。可选 —— 默认为 `output`。

### `language.document`

生成的产物文件（requirements/spec/plan/tasks）的语言。可选 —— 默认为 `output`。

### `language.commit`

git 提交信息的语言。可选 —— 默认为 `output`。

### `language.templates`

模板语言。应保持为 `"en"` 以确保兼容性。

## 项目设置

### `project.ai`

正在使用的 AI 助手。当前支持：

- `claude`（默认）

### `project.created`

项目初始化的日期。
