<a id="installation"></a>

# 安装

<a id="install-with-the-codex-desktop-app"></a>

## 通过 Codex 桌面应用安装

你可以直接在 Codex 桌面应用中提出安装请求，让它安装 CodexSpec 并完成项目初始化。

1. 在 Codex 桌面应用中添加本地项目，并选择要开展工作的文件夹。
2. 打开该项目的对话，粘贴下面的提示词。
3. 如果应用请求下载或安装依赖的权限，批准后即可继续。

```text
Please install and initialize CodexSpec in the current project.
Project: https://github.com/Zts0hg/codexspec

Complete the setup directly instead of asking me to run terminal commands.

Check the environment. If uv or Python 3.11+ is missing, install the required
tools in my user directory using their official installation instructions.
Install the latest stable release of CodexSpec.

For a new setup, initialize the current project for Codex in English:
codexspec init . --ai codex --lang en

If CodexSpec is already configured, check its version and configuration before
updating. Preserve existing requirements, project principles, user files,
and configuration settings.

Verify that the CLI works and that AGENTS.md and the CodexSpec skill files
under .agents/skills/ are installed. Explain the result and how to start
describing my requirements in plain English. If the skills are not yet
available in this chat, tell me whether to start a new chat or restart the app.
```

如果希望使用中文交流并生成中文文档，请将 `--lang en` 改为 `--lang zh-CN`，同时要求 Codex 用中文说明安装结果。

这种方式安装的 CLI 和项目技能与手动安装相同。安装完成后，可以输入 `$codexspec:specify I want to build a todo application` 这样的提示词，开始描述需求。如何让 Codex 发现或刷新本地技能，见 [OpenAI 的技能指南](https://learn.chatgpt.com/docs/build-skills)。

<a id="prerequisites"></a>

## 前置要求

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推荐），或 pip
- 要使用的助手：Claude Code 或 Codex
- Git：用于 worktree 开发和 Git 操作

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

<a id="plugin-marketplace-installation"></a>

## 通过插件市场安装

Claude Code 可以通过插件市场安装：

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

插件会提供命令，并在新建或恢复会话时加载指引，要求先分析暂存内容再提交、先回顾相关历史需求再作判断。安装插件本身不会初始化项目。可以用 `/codexspec:config` 创建或修改语言、工作流和审查设置；如果需要完整的项目目录与资源，请通过 CLI 初始化。

预览提交，以及在当前工作区执行已获授权的提交，都可以使用插件自带的运行时；只需 Python 3.11+ 和 Git，无需长期安装 CodexSpec CLI。Worktree 路由、蓝图/auto-dev 和手动审阅项目知识仍需要 CLI。插件的启动钩子要求 Git 已加入 PATH，且 Claude Code 版本支持命令钩子的 `args`（exec 形式）。这些指引供智能体遵守，不会拦截你手动执行的 Git 命令。

详细设置见[安装指南](installation.md)。
