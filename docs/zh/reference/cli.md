# CLI 参考

## 命令

### `codexspec init`

初始化一个新的 CodexSpec 项目。

```bash
codexspec init [PROJECT_NAME] [OPTIONS]
```

**参数：**

| 参数 | 描述 |
|------|------|
| `PROJECT_NAME` | 新项目目录的名称（使用 `.` 或 `--here` 指代当前目录） |

**选项：**

| 选项 | 简写 | 描述 |
|------|------|------|
| `--here` | `-h` | 在当前目录初始化 |
| `--ai` | `-a` | 要使用的 AI 助手（默认：claude） |
| `--lang` | `-l` | 输出（基础）语言；interaction/document/commit 在未设置时回退到该语言（如 en、zh-CN、ja） |
| `--interaction-lang` | | 交互语言（LLM 对话 + `codexspec` CLI 输出）；覆盖 `--lang` |
| `--document-lang` | | 文档语言（生成的 requirements/spec/plan/tasks）；覆盖 `--lang` |
| `--commit-lang` | | 提交信息语言；覆盖 `--lang` |
| `--force` | `-f` | 覆盖现有文件并自动确认提示；永不重新生成 `config.yml` |
| `--no-git` | | 跳过 git 初始化 |
| `--debug` | `-d` | 启用调试输出 |

`--lang` 设置 `output` 基础语言；`--interaction-lang`、`--document-lang` 和 `--commit-lang` 分别覆盖各自维度（各自回退到 `output`，再到 `en`）。完整模型请参见[国际化](../user-guide/i18n.md)。

在 TTY 中首次运行 `init` 且未指定 `--lang`（也未同时指定全部三个维度标志）时会提示选择基础语言；在非 TTY 环境（CI/脚本）下默认为 `en` —— **完全非交互**。重新运行 `init` 会保留你未指定的任何语言键；`--force` 永不重新生成 `config.yml`。

**示例：**

```bash
# 创建新项目
codexspec init my-project

# 在当前目录初始化
codexspec init . --ai claude

# 完全非交互：zh-CN 基础语言，英文提交信息
codexspec init my-project --lang zh-CN --commit-lang en

# 显式设置每个维度（可脚本化，无提示）
codexspec init my-project \
  --interaction-lang zh-CN --document-lang en --commit-lang en
```

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

每个 `--set-*-lang` 更新一个[语言维度](../user-guide/i18n.md)；未设置的维度回退到 `output`，再到 `en`。
