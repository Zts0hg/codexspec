# CLI 参考

<a id="cli-commands"></a>

## CLI 命令

| 命令 | 用途 |
|---------|---------|
| `codexspec init` | 为 Claude、Codex 或两者初始化或刷新项目 |
| `codexspec check` | 检查已安装的工具和依赖 |
| `codexspec version` | 显示版本和系统信息 |
| `codexspec config` | 查看或修改项目配置 |
| `codexspec list-commands` | 按类别列出可用智能体命令 |
| `codexspec show-blueprint` | 显示共享工作区中的蓝图，不作修改 |

<a id="cli-installation"></a>

## CLI 安装

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

新建项目可运行 `codexspec init my-project --ai claude`；初始化当前目录可运行 `codexspec init . --ai codex`。如果要同时使用两个助手，请指定 `--ai both`。默认助手是 `claude`，使用 Codex 或同时使用两者时，需要明确指定相应选项。

<details>
<summary>其他安装方式</summary>

<a id="one-time-initialization"></a>

### 一次性初始化

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

一次性初始化会安装项目命令和可独立运行的提交辅助程序。不过，worktree 路由、蓝图/auto-dev 和手动审阅项目知识仍需要调用 CodexSpec CLI；使用这些工作流时，请确保 CLI 可用。

<a id="development-versions"></a>

### 开发版本

```bash
uv tool install git+https://github.com/Zts0hg/codexspec.git
uv tool install git+https://github.com/Zts0hg/codexspec.git@main

# Replace <tag> with the version you want
uv tool install git+https://github.com/Zts0hg/codexspec.git@<tag>
```

</details>

<details>
<summary>Windows 安装</summary>

使用 PowerShell：

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
# Restart PowerShell, then:
uv tool install codexspec
codexspec version
```

如果遇到 PATH 或安装问题，请查阅 [Windows 故障排除指南](../WINDOWS-TROUBLESHOOTING.md)。

</details>

<a id="upgrade-and-refresh-a-project"></a>

## 升级与刷新项目

更新 CLI 和刷新项目中已安装的命令是两个独立步骤：

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

如果只使用一个助手，请选择 `--ai claude` 或 `--ai codex`。`--force` 会重新生成随安装提供的命令和脚本、刷新审查资源，并自动确认迁移、命令更新和项目宪法合规提示。已有需求和项目原则会保留；上下文文件中的自动维护指引会更新，原有正文不会被替换；未明确修改的配置项也会保留原设置。

编写实现计划使用 `design-to-plan`。更新安装时会移除旧的 `spec-to-plan` 入口，不提供兼容别名。

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

## `codexspec show-blueprint`

从固定分支 `codexspec/auto-dev` 和 `worktree-for-codexspec-auto-dev` 输出完整的
`.codexspec/blueprint.md`。文件原文写入标准输出；仓库、分支、worktree 或文件不存在时，
错误写入标准错误并返回非零状态。该命令为只读操作，不执行 fetch、merge、写入或加锁。

```bash
codexspec show-blueprint
```
