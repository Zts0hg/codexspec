# CLI 参考

## 命令

### `codexspec show-blueprint`

从固定分支 `codexspec/auto-dev` 和 `worktree-for-codexspec-auto-dev` 输出完整的
`.codexspec/blueprint.md`。文件原文写入标准输出；仓库、分支、worktree 或文件不存在时，
错误写入标准错误并返回非零状态。该命令为只读操作，不执行 fetch、merge、写入或加锁。

```bash
codexspec show-blueprint
```

---

### `codexspec init`

初始化一个新的 CodexSpec 项目。

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**参数：**

| 参数 | 描述 |
|------|------|
| `PROJECT_NAME` | 新项目目录的名称（用 `.` 或 `--here` 指代当前目录） |

**选项：**

| 选项 | 简写 | 描述 |
|------|------|------|
| `--here` | `-h` | 在当前目录初始化 |
| `--ai` | `-a` | 要使用的 AI 助手：`claude`、`codex` 或 `both`（默认：claude） |
| `--lang` | `-l` | 输出（基础）语言；interaction/document/commit 在未设置时回退到它（如 en、zh-CN、ja） |
| `--interaction-lang` | | 交互语言（LLM 对话 + `codexspec` CLI 输出）；覆盖 `--lang` |
| `--document-lang` | | 文档语言（生成的 requirements/spec/plan/tasks）；覆盖 `--lang` |
| `--commit-lang` | | 提交信息语言；覆盖 `--lang` |
| `--force` | `-f` | 覆盖现有文件并自动确认提示；绝不重新生成 `config.yml` |
| `--no-git` | | 跳过 git 仓库初始化 |
| `--debug` | `-d` | 启用调试输出 |

`--lang` 设置 `output` 基础语言；`--interaction-lang`、`--document-lang` 与 `--commit-lang` 分别覆盖各自的维度（各自回退到 `output`，再到 `en`）。完整模型见[国际化](../user-guide/i18n.md)。

在 TTY 中首次运行 `init` 且未指定 `--lang`（也未同时指定全部三个维度标志）时会提示选择基础语言；在非 TTY 环境（CI/脚本）下默认为 `en`——**完全非交互**。重新运行 `init` 会保留你未显式指定的任何语言键；`--force` 绝不重新生成 `config.yml`。

**示例：**

```bash
# 创建新项目
codexspec init my-project

# 在当前目录初始化
codexspec init . --ai claude

# 一次性运行（无需安装）——为 Codex CLI 或 both 初始化
uvx codexspec init . --ai codex
uvx codexspec init . --ai both

# 完全非交互：zh-CN 基础语言，英文提交信息
codexspec init my-project --lang zh-CN --commit-lang en

# 显式设置每个维度（可脚本化，无提示）
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

`codexspec init` 将 Claude Code 与 Codex 共享的审查资源安装到 `.codexspec/review-code/`。`--force` 更新随工具提供的资源，并保留路径不同的扩展文件。仅安装 CLI 不会创建项目文件。仅使用插件时，若项目没有已安装的资源目录，审查会读取宿主解析的插件根目录中的同一套资源。

---

### `codexspec check`

检查已安装的工具。

```bash
codexspec check
```

---

### `codexspec version`

显示版本信息。

```bash
codexspec version
```

---

### `codexspec config`

查看或修改项目配置。

```bash
codexspec config [OPTIONS]
```

**选项：**

| 选项 | 简写 | 描述 |
|------|------|------|
| `--set-lang` | `-l` | 设置输出（基础）语言 |
| `--set-interaction-lang` | | 设置交互语言（LLM 对话 + CLI 输出） |
| `--set-document-lang` | | 设置文档语言（生成的 spec/plan/tasks） |
| `--set-commit-lang` | `-c` | 设置提交信息语言 |
| `--list-langs` | | 列出所有支持的语言 |
| `--auto-next` | | 切换/设置 `workflow.auto_next`（裸标志切换；或传 on/off） |
| `--auto-maintenance` |  | 切换或设置 `workflow.auto_maintenance`（默认开启；不带值即切换；或 on/off） |
| `--decided-by` | | 将 `review.decided_by` 设为 `reviewer`（默认）或 `ask` |

每个 `--set-*-lang` 更新一个[语言维度](../user-guide/i18n.md)；未设置的维度回退到 `output`，再到 `en`。

`codexspec config --auto-maintenance on|off` 将 `workflow.auto_maintenance` 作为 YAML 布尔值持久化到 `.codexspec/config.yml`；未配置时按 `true` 处理。两个工作流开关都接受不区分大小写的 `on/true/1/yes` 和 `off/false/0/no`。`implement-tasks` 自动修复审查问题时读取此配置：`on` 将有依据的增量维护改进纳入修复，`off` 仍会报告这些建议。实际缺陷与必要验证仍必须处理。它与 `auto-next` 独立，也不是 `implement-tasks` 的调用参数。

```bash
codexspec config --auto-maintenance on
codexspec config --auto-maintenance off
```
