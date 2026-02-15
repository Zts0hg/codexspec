# CodexSpec

[English](README.md) | **中文** | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**面向 Claude Code 的规格驱动开发 (SDD) 工具包**

CodexSpec 是一个帮助您使用结构化、规格驱动方法构建高质量软件的工具包。它颠覆了传统开发模式，将规格说明转化为直接指导实现的可执行产物。

## 特性

- **结构化工作流**: 开发各阶段都有清晰的命令
- **Claude Code 集成**: 原生支持 Claude Code 斜杠命令
- **宪法驱动**: 项目原则指导所有决策
- **规格优先**: 先定义做什么和为什么，再考虑怎么做
- **计划驱动**: 技术选型在需求之后进行
- **任务导向**: 将实现分解为可执行的任务
- **质量保证**: 内置审查、分析和检查清单命令
- **国际化 (i18n)**: 通过 LLM 动态翻译支持多语言
- **跨平台**: 同时支持 Bash 和 PowerShell 脚本
- **可扩展**: 支持自定义命令的插件架构

## 安装

### 前置要求

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推荐）或 pip

### 方式 1: 使用 uv 安装（推荐）

使用 uv 安装 CodexSpec 最简单：

```bash
uv tool install codexspec
```

### 方式 2: 使用 pip 安装

也可以使用 pip：

```bash
pip install codexspec
```

### 方式 3: 一次性使用

无需安装直接运行：

```bash
# 创建新项目
uvx codexspec init my-project

# 在现有项目中初始化
cd your-existing-project
uvx codexspec init . --ai claude
```

### 方式 4: 从 GitHub 安装（开发版本）

获取最新开发版本或特定分支：

```bash
# 使用 uv
uv tool install git+https://github.com/Zts0hg/codexspec.git

# 使用 pip
pip install git+https://github.com/Zts0hg/codexspec.git

# 特定分支或标签
uv tool install git+https://github.com/Zts0hg/codexspec.git@main
uv tool install git+https://github.com/Zts0hg/codexspec.git@v0.2.0
```

## 快速开始

安装后，您可以使用 CLI：

```bash
# 创建新项目（中文输出）
codexspec init my-project --lang zh-CN

# 在现有项目中初始化
codexspec init . --ai claude

# 检查已安装的工具
codexspec check

# 查看版本
codexspec version
```

升级到最新版本：

```bash
# 使用 uv
uv tool install codexspec --upgrade

# 使用 pip
pip install --upgrade codexspec
```

## 使用方法

### 1. 初始化项目

安装后，创建或初始化您的项目：

```bash
codexspec init my-awesome-project --lang zh-CN
```

### 2. 建立项目原则

在项目目录中启动 Claude Code：

```bash
cd my-awesome-project
claude
```

使用 `/codexspec.constitution` 命令创建项目的治理原则：

```
/codexspec.constitution 创建专注于代码质量、测试标准和整洁架构的原则
```

### 3. 创建规格说明

使用 `/codexspec.specify` 定义您想要构建的内容：

```
/codexspec.specify 构建一个任务管理应用，包含以下功能：创建任务、分配给用户、设置截止日期、跟踪进度
```

### 4. 澄清需求（可选但推荐）

使用 `/codexspec.clarify` 在规划前解决歧义：

```
/codexspec.clarify
```

### 5. 创建技术计划

使用 `/codexspec.spec-to-plan` 定义如何实现：

```
/codexspec.spec-to-plan 使用 Python 和 FastAPI 作为后端，PostgreSQL 作为数据库，React 作为前端
```

### 6. 生成任务

使用 `/codexspec.plan-to-tasks` 分解计划：

```
/codexspec.plan-to-tasks
```

### 7. 分析（可选但推荐）

使用 `/codexspec.analyze` 进行跨产物一致性检查：

```
/codexspec.analyze
```

### 8. 实现

使用 `/codexspec.implement-tasks` 执行实现：

```
/codexspec.implement-tasks
```

## 可用命令

### CLI 命令

| 命令 | 描述 |
|------|------|
| `codexspec init` | 初始化新的 CodexSpec 项目 |
| `codexspec check` | 检查已安装的工具 |
| `codexspec version` | 显示版本信息 |
| `codexspec config` | 查看或修改项目配置 |

### `codexspec init` 选项

| 选项 | 描述 |
|------|------|
| `PROJECT_NAME` | 新项目目录的名称 |
| `--here`, `-h` | 在当前目录初始化 |
| `--ai`, `-a` | 使用的 AI 助手（默认：claude） |
| `--lang`, `-l` | 输出语言（如：en, zh-CN, ja） |
| `--force`, `-f` | 强制覆盖现有文件 |
| `--no-git` | 跳过 git 初始化 |
| `--debug`, `-d` | 启用调试输出 |

### `codexspec config` 选项

| 选项 | 描述 |
|------|------|
| `--set-lang`, `-l` | 设置输出语言 |
| `--list-langs` | 列出所有支持的语言 |

### 斜杠命令

初始化后，Claude Code 中可使用以下斜杠命令：

#### 核心命令

| 命令 | 描述 |
|------|------|
| `/codexspec.constitution` | 创建或更新项目治理原则 |
| `/codexspec.specify` | 定义您想要构建的内容（需求） |
| `/codexspec.generate-spec` | 从需求生成详细规格 |
| `/codexspec.spec-to-plan` | 将规格转换为技术计划 |
| `/codexspec.plan-to-tasks` | 将计划分解为可执行任务 |
| `/codexspec.implement-tasks` | 按分解执行任务 |

#### 审查命令

| 命令 | 描述 |
|------|------|
| `/codexspec.review-spec` | 审查规格的完整性 |
| `/codexspec.review-plan` | 审查技术计划的可行性 |
| `/codexspec.review-tasks` | 审查任务分解的完整性 |

#### 增强命令

| 命令 | 描述 |
|------|------|
| `/codexspec.clarify` | 在规划前澄清不明确的区域 |
| `/codexspec.analyze` | 跨产物一致性分析 |
| `/codexspec.checklist` | 为需求生成质量检查清单 |
| `/codexspec.tasks-to-issues` | 将任务转换为 GitHub issues |

## 工作流概览

```
┌──────────────────────────────────────────────────────────────┐
│                    CodexSpec 工作流                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Constitution  ──►  定义项目原则                           │
│         │                                                    │
│         ▼                                                    │
│  2. Specify  ───────►  创建功能规格                           │
│         │                                                    │
│         ▼                                                    │
│  3. Clarify  ───────►  解决歧义（可选）                        │
│         │                                                    │
│         ▼                                                    │
│  4. Review Spec  ───►  验证规格                               │
│         │                                                    │
│         ▼                                                    │
│  5. Spec to Plan  ──►  创建技术计划                           │
│         │                                                    │
│         ▼                                                    │
│  6. Review Plan  ───►  验证技术计划                           │
│         │                                                    │
│         ▼                                                    │
│  7. Plan to Tasks  ─►  生成任务分解                           │
│         │                                                    │
│         ▼                                                    │
│  8. Analyze  ───────►  跨产物一致性（可选）                    │
│         │                                                    │
│         ▼                                                    │
│  9. Review Tasks  ──►  验证任务分解                           │
│         │                                                    │
│         ▼                                                    │
│  10. Implement  ─────►  执行实现                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## 项目结构

初始化后，您的项目将具有以下结构：

```
my-project/
├── .codexspec/
│   ├── memory/
│   │   └── constitution.md    # 项目治理原则
│   ├── specs/
│   │   └── {feature-id}/
│   │       ├── spec.md        # 功能规格
│   │       ├── plan.md        # 技术计划
│   │       ├── tasks.md       # 任务分解
│   │       └── checklists/    # 质量检查清单
│   ├── templates/             # 自定义模板
│   ├── scripts/               # 辅助脚本
│   │   ├── bash/              # Bash 脚本
│   │   └── powershell/        # PowerShell 脚本
│   └── extensions/            # 自定义扩展
├── .claude/
│   └── commands/              # Claude Code 斜杠命令
└── CLAUDE.md                  # Claude Code 上下文
```

## 国际化 (i18n)

CodexSpec 通过 **LLM 动态翻译**支持多种语言。我们不需要维护翻译后的模板，而是让 Claude 在运行时根据您的语言配置进行翻译。

### 设置语言

**初始化时：**
```bash
# 创建中文输出的项目
codexspec init my-project --lang zh-CN

# 创建日语输出的项目
codexspec init my-project --lang ja
```

**初始化后：**
```bash
# 查看当前配置
codexspec config

# 更改语言设置
codexspec config --set-lang zh-CN

# 列出支持的语言
codexspec config --list-langs
```

### 配置文件

`.codexspec/config.yml` 文件存储语言设置：

```yaml
version: "1.0"

language:
  # Claude 交互和生成文档的输出语言
  output: "zh-CN"

  # 模板语言 - 保持 "en" 以获得最佳兼容性
  templates: "en"

project:
  ai: "claude"
  created: "2026-02-15"
```

### 支持的语言

| 代码 | 语言 |
|------|------|
| `en` | English（默认） |
| `zh-CN` | 中文（简体） |
| `zh-TW` | 中文（繁體） |
| `ja` | 日本語 |
| `ko` | 한국어 |
| `es` | Español |
| `fr` | Français |
| `de` | Deutsch |
| `pt` | Português |
| `ru` | Русский |
| `it` | Italiano |
| `ar` | العربية |
| `hi` | हिन्दी |

### 工作原理

1. **单一英文模板**: 所有命令模板保持英文
2. **语言配置**: 项目指定首选输出语言
3. **动态翻译**: Claude 读取英文指令，用目标语言输出
4. **上下文感知**: 技术术语（JWT、OAuth 等）在适当时保持英文

### 优势

- **零翻译维护**: 无需维护多个模板版本
- **始终保持最新**: 模板更新自动惠及所有语言
- **上下文感知翻译**: Claude 提供自然、符合上下文的翻译
- **无限语言**: Claude 支持的任何语言都可以立即使用

## 扩展系统

CodexSpec 支持用于添加自定义命令的插件架构：

### 扩展结构

```
my-extension/
├── extension.yml          # 扩展清单
├── commands/              # 自定义斜杠命令
│   └── command.md
└── README.md
```

### 创建扩展

1. 从 `extensions/template/` 复制模板
2. 修改 `extension.yml` 填写扩展详情
3. 在 `commands/` 中添加自定义命令
4. 本地测试并发布

详见 `extensions/EXTENSION-DEVELOPMENT-GUIDE.md`。

## 开发

### 前置要求

- Python 3.11+
- uv 包管理器
- Git

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# 安装开发依赖
uv sync --dev

# 本地运行
uv run codexspec --help

# 运行测试
uv run pytest

# 代码检查
uv run ruff check src/
```

### 构建

```bash
# 构建包
uv build
```

## 与 spec-kit 对比

CodexSpec 灵感来源于 GitHub 的 spec-kit，但有一些关键差异：

| 特性 | spec-kit | CodexSpec |
|------|----------|-----------|
| 核心理念 | 规格驱动开发 | 规格驱动开发 |
| CLI 名称 | `specify` | `codexspec` |
| 主要 AI | 多代理支持 | 专注于 Claude Code |
| 命令前缀 | `/speckit.*` | `/codexspec.*` |
| 工作流 | specify → plan → tasks → implement | constitution → specify → clarify → plan → tasks → analyze → implement |
| 审查步骤 | 可选 | 内置审查命令 |
| Clarify 命令 | 是 | 是 |
| Analyze 命令 | 是 | 是 |
| Checklist 命令 | 是 | 是 |
| 扩展系统 | 是 | 是 |
| PowerShell 脚本 | 是 | 是 |
| i18n 支持 | 否 | 是（通过 LLM 翻译支持 13+ 语言） |

## 理念

CodexSpec 遵循以下核心原则：

1. **意图驱动开发**: 规格在"怎么做"之前定义"做什么"
2. **丰富的规格创建**: 使用护栏和组织原则
3. **多步骤细化**: 而非一次性代码生成
4. **高度依赖 AI**: 利用 AI 解释规格
5. **审查导向**: 在推进前验证每个产物
6. **质量优先**: 内置检查清单和分析以确保需求质量

## 贡献

欢迎贡献！请在提交 pull request 前阅读我们的贡献指南。

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

## 致谢

- 灵感来源于 [GitHub spec-kit](https://github.com/github/spec-kit)
- 为 [Claude Code](https://claude.ai/code) 构建
