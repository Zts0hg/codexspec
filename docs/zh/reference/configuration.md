<a id="configuration-and-internationalization"></a>

# 配置与国际化

配置保存在 `.codexspec/config.yml` 中。模板始终使用英文，智能体交流和生成文档时，则使用配置中指定的语言。支持的 13 个标准语言代码为 `en`、`zh-CN`、`zh-TW`、`ja`、`ko`、`es`、`fr`、`de`、`pt`、`ru`、`it`、`ar` 和 `hi`。葡萄牙语在 CLI 中使用 `pt`，在本地化文档和翻译目录中使用 `pt-BR`。

<a id="language-dimensions"></a>

## 语言维度

| 维度 | 配置键 | 初始化时 | 后续设置 | 控制范围 |
|-----------|------------|-------------------|-----------|----------|
| 输出/基础 | `language.output` | `--lang` | `config --set-lang` | 其他语言选项未设置时使用的语言 |
| 交互 | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | 对话和 CLI 输出 |
| 文档 | `language.document` | `--document-lang` | `config --set-document-lang` | 需求、规格、设计、计划、任务 |
| 提交 | `language.commit` | `--commit-lang` | `config --set-commit-lang` | 提交信息及 Git 工作流生成的文本 |

每项语言设置都独立生效：未指定时先使用 `language.output`，它也未指定时再使用 `en`。`language.templates` 始终为 `en`。

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

首次在交互式终端（TTY）中初始化时，如果没有指定 `--lang`，也没有完整指定三个具体语言选项，程序会询问基础语言。`--force` 会自动确认其他初始化提示，但仍会要求选择语言。在非 TTY 环境中初始化时，默认使用英文。重新初始化时，没有明确修改的语言设置会保留。

<a id="workflow-and-review-settings"></a>

## 工作流与审查设置

| 设置 | 默认值 | 作用 | CLI 控制 |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | 常规 SDD 阶段通过审查后自动进入下一阶段 | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | 成功执行收尾步骤后自动提炼知识，无需交互 | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | 自动修复时一并实施已验证的增量维护改进 | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | 为常规功能和独立维护工作隔离工作区 | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | 问题只在项目实际运行范围之外触发时，由谁决定是否处理 | `config --decided-by reviewer\|ask` |

布尔类型的 CLI 开关可以使用 `on/true/1/yes` 或 `off/false/0/no`，不区分大小写，也允许值的前后带空白。不传值时，会切换目标 checkout 中的当前设置；写入 YAML 的值始终是布尔值。

如果设置为 `review.decided_by: reviewer`，由审查者决定是否将问题纳入缺陷。设置为 `ask` 时，只在实际运行范围之外触发的问题，会作为待用户确认的场景：用户决定修复该问题，还是排除该场景；确认后的决定会沿用到后续轮次。仍有待定决定时，不能宣告完成。单次调用 `review-code` 时，可以用 `--decided-by` 覆盖配置中的模式。

修改配置时，同样遵循 worktree 路由规则。从主 checkout 单独修改配置，会写入维护 worktree，不会立即改变 main 使用的设置；在功能 worktree 中修改，则先在该工作区生效。

<details>
<summary>CLI 初始化选项</summary>

| 选项 | 含义 |
|--------|---------|
| `PROJECT_NAME` | 新目录名；使用 `.` 表示当前目录 |
| `--here`, `-h` | 初始化当前目录 |
| `--ai`, `-a` | `claude`、`codex` 或 `both`；默认为 `claude` |
| `--lang`, `-l` | 设置基础输出语言 |
| `--interaction-lang` | 设置交互语言 |
| `--document-lang` | 设置文档语言 |
| `--commit-lang` | 设置提交信息语言 |
| `--force`, `-f` | 重新生成安装资源并自动确认迁移、更新和合规提示；保留项目自行编写的上下文及无关配置 |
| `--no-git` | 跳过 Git 仓库初始化 |
| `--debug`, `-d` | 显示详细调试输出 |

</details>

<details>
<summary>CLI 配置选项</summary>

| 选项 | 含义 |
|--------|---------|
| `--set-lang`, `-l` | 设置基础输出语言 |
| `--set-interaction-lang` | 设置交互语言 |
| `--set-document-lang` | 设置文档语言 |
| `--set-commit-lang`, `-c` | 设置提交信息语言 |
| `--list-langs` | 列出支持的语言代码 |
| `--auto-next` | 切换/设置阶段自动推进 |
| `--auto-distill` | 切换/设置自动知识捕获 |
| `--auto-maintenance` | 切换/设置自动增量维护 |
| `--worktrees` | 切换或设置当前 checkout 的 worktree 隔离方式 |
| `--decided-by` | 选择由 `reviewer` 判断，还是用 `ask` 询问用户 |

</details>

<details>
<summary>配置示例</summary>

```yaml
version: "1.0"

language:
  output: "en"
  interaction: "zh-CN"
  document: "en"
  commit: "en"
  templates: "en"

project:
  ai: "both"

workflow:
  auto_next: false
  auto_distill: true
  auto_maintenance: true
  worktrees: true

review:
  decided_by: reviewer
```

</details>

各项设置和语言选项的详细说明，见[配置](configuration.md)和[国际化](../user-guide/i18n.md)。
