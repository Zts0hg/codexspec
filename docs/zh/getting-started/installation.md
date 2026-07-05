# 安装

## 前提条件

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

## 方式一：使用 uv 安装（推荐）

安装 CodexSpec 最简单的方式是使用 uv：

```bash
uv tool install codexspec
```

## 方式二：使用 pip 安装

也可以用 pip：

```bash
pip install codexspec
```

## 方式三：一次性运行

无需安装即可直接运行：

```bash
# 创建新项目
uvx codexspec init my-project

# 在已有项目中为 Claude Code 初始化
cd your-existing-project
uvx codexspec init . --ai claude

# 为 Codex CLI 初始化
uvx codexspec init . --ai codex

# 同时为 Claude Code 和 Codex CLI 初始化（同时写入 .claude/ 和 .agents/）
uvx codexspec init . --ai both
```

## 方式四：从 GitHub 安装

获取最新开发版本：

```bash
# 使用 uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# 使用 pip
pip install git+https://github.com/Zts0hg/codexspec.git

# 指定分支或标签
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.5.6
```

## 方式五：通过插件市场安装（替代方案）

CodexSpec 也提供 Claude Code 插件。如果你只想在 Claude Code 中直接使用其斜杠命令、不想安装 CLI 工具，这种方式最合适。CLI 提供 Requirements-First SDD 的完整体验；插件则把整套斜杠命令叠加到 Claude Code 之上。

### 安装步骤

在 Claude Code 中：

```bash
# 添加插件市场
> /plugin marketplace add Zts0hg/codexspec

# 安装插件
> /plugin install codexspec@codexspec-market
```

### 插件用户的语言配置

通过插件市场安装后，使用 `/codexspec:config` 斜杠命令配置首选语言（未安装 CLI 时，`codexspec config` CLI 命令不可用）：

```bash
# 启动交互式配置
> /codexspec:config

# 或查看当前配置
> /codexspec:config --view
```

config 命令会引导你选择输出语言（用于生成的文档）与提交信息语言，随后写入 `.codexspec/config.yml`。多语言支持与 CLI 一样采用 LLM 动态翻译。

### 各安装方式对比

| 方式 | 适用场景 | 功能 |
|--------|----------|------|
| **CLI 安装**（`uv tool install` 或 `pip install`） | 完整开发流程 | CLI 命令（`init`、`check`、`config`、`version`）+ 斜杠命令 |
| **插件市场** | 快速上手、已有项目 | 仅斜杠命令（用 `/codexspec:config` 配置语言） |

**注意**：插件使用 `strict: false` 模式，并通过 LLM 动态翻译复用既有的多语言支持。

## 验证安装

```bash
codexspec --help
codexspec version
```

（若是通过插件市场安装，可在 Claude Code 中运行任意斜杠命令来验证，例如 `/codexspec:config --view`。）

## 升级

```bash
# 使用 uv
uv tool install codexspec --upgrade

# 使用 pip
pip install --upgrade codexspec
```

（插件市场的安装由 Claude Code 的插件管理器负责更新。）

## 下一步

[快速入门](quick-start.md)
