<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="codexspec-logo-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="codexspec-logo-light.svg">
    <img alt="CodexSpec Logo" src="codexspec-logo-light.svg" width="420">
  </picture>
</div>

<h1 align="center">CodexSpec</h1>

<p align="center">
  <a href="README.md">English</a> | <b>中文</b> | <a href="README.ja.md">日本語</a> | <a href="README.es.md">Español</a> | <a href="README.pt-BR.md">Português</a> | <a href="README.ko.md">한국어</a> | <a href="README.de.md">Deutsch</a> | <a href="README.fr.md">Français</a>
</p>

<p align="center">
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/v/codexspec.svg?style=for-the-badge" alt="PyPI version"></a>
  <a href="https://pypi.org/project/codexspec/"><img src="https://img.shields.io/pypi/pyversions/codexspec.svg?style=for-the-badge" alt="Python versions"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License: MIT"></a>
</p>

<p align="center">
  <strong>面向 Claude Code 和 OpenAI Codex 的需求优先 SDD 工具包</strong>
</p>

CodexSpec 将已确认的需求转化为可追溯的规格、设计、计划、任务和实现。你决定**做什么**以及**为什么做**；代理在这些已确认需求的范围内，借助审查关卡和持久化项目知识，制定**如何实现**。

可以通过 Claude Code 斜杠命令、Codex skills，或同时使用两者。普通功能默认使用独立 Git worktree；可选的共享蓝图支持代理自主开发一组已确认的需求。

[📖 文档](https://zts0hg.github.io/codexspec/) | [中文文档](https://zts0hg.github.io/codexspec/zh/) | [日本語ドキュメント](https://zts0hg.github.io/codexspec/ja/) | [한국어 문서](https://zts0hg.github.io/codexspec/ko/) | [Documentación](https://zts0hg.github.io/codexspec/es/) | [Documentation](https://zts0hg.github.io/codexspec/fr/) | [Dokumentation](https://zts0hg.github.io/codexspec/de/) | [Documentação](https://zts0hg.github.io/codexspec/pt-BR/)

## 目录

- [为什么选择 CodexSpec？](#为什么选择-codexspec)
- [30 秒快速开始](#30-秒快速开始)
- [安装](#安装)
- [核心工作流](#核心工作流)
- [共享蓝图与自主开发](#共享蓝图与自主开发)
- [Worktree 开发](#worktree-开发)
- [处理既有代码](#处理既有代码)
- [审查与调试](#审查与调试)
- [项目知识](#项目知识)
- [Git 工作流](#git-工作流)
- [可用命令](#可用命令)
- [配置与国际化](#配置与国际化)
- [项目结构](#项目结构)
- [扩展开发资料](#扩展开发资料)
- [开发](#开发)
- [贡献](#贡献)
- [许可证](#许可证)

## 为什么选择 CodexSpec？

| 需求 | CodexSpec 提供的支持 |
|------|-------------------------|
| 清晰的产品意图 | 在编写规格前明确确认需求，并持久保存到 `requirements.md` |
| 可追溯的开发过程 | 需求 → 规格 → 设计 → 计划 → 任务之间的来源引用 |
| 可审查的决策 | 四个产物审查命令、跨产物分析，以及独立的代码缺陷门禁 |
| 跨会话与团队协作的连续性 | 功能记录、项目原则、可复用知识及相关历史决策 |
| 多个功能并行推进 | 每个普通功能使用一个 Git worktree，并稳定复用其工作空间 |
| 更多自动化 | 可选的阶段自动推进，以及对已确认蓝图需求的自主开发 |
| 团队语言偏好 | 独立设置交互、文档和提交语言 |

### 什么是需求优先 SDD？

需求优先的规格驱动开发（Requirements-First Spec-Driven Development）将**已确认的需求作为功能的最高优先级依据**。代理在推导实现产物前，记录目标、约束、决策、排除项、待解决问题和确认凭据。

```text
Idea → Confirmed Requirements → Spec → Design → Plan → Tasks → Code
```

人与代理协作建立和变更产品意图。自动审查据此检查派生产物。启用自动化会推进通过审查的阶段；代理不能因此擅自替换已确认的需求。

## 30 秒快速开始

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

在初始化后的项目中启动已安装的助手。同一个工作流支持以下两种调用形式：

| 助手 | 开始需求讨论 |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

需要时，通过 `constitution` 定制项目原则。确认最终需求摘要后，在返回的功能目录和工作空间中继续工作。其余命令见[核心工作流](#核心工作流)。

使用 Codex 桌面应用？可以[让 Codex 安装并初始化你的项目](#通过-codex-桌面应用安装)。

## 安装

### 通过 Codex 桌面应用安装

你可以直接在桌面应用中让 Codex 安装 CodexSpec 并设置项目。

1. 在 Codex 桌面应用中添加一个本地项目，选择准备工作的文件夹。
2. 在该项目中开始对话，粘贴下方提示词。
3. 如果应用请求下载或安装依赖的权限，批准相应操作后继续。

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

如需中文回复和文档，将 `--lang en` 替换为 `--lang zh-CN`，并要求 Codex 用中文说明结果。

Codex 安装的 CLI 和项目 skills 与下方手动设置所用的相同。之后可使用类似 `$codexspec:specify I want to build a todo application` 的提示词开始工作。关于本地 skill 的发现与刷新行为，见 [OpenAI 的 skills 指南](https://learn.chatgpt.com/docs/build-skills)。

### 前置要求

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推荐），或 pip
- 你准备使用的助手：Claude Code 或 Codex
- 用于 worktree 开发和 Git 工作流的 Git

### CLI 安装

```bash
uv tool install codexspec

# Or use pip
pip install codexspec

# Verify the CLI and inspect available commands
codexspec version
codexspec --help
codexspec list-commands
```

使用 `codexspec init my-project --ai claude` 初始化新项目，或使用 `codexspec init . --ai codex` 初始化当前目录。两种集成都需要时，使用 `--ai both`。助手选择默认为 `claude`；使用 Codex 或两者时，请明确指定。

<details>
<summary>其他安装方式</summary>

#### 一次性初始化

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

一次性初始化会安装项目命令和独立的提交运行时。Worktree 路由、蓝图/auto-dev 和手动 profile 审阅仍会调用 CodexSpec CLI；使用这些工作流时，需要确保 CLI 可用。

#### 开发版本

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

关于 PATH 和安装问题，见 [Windows 故障排除指南](docs/en/WINDOWS-TROUBLESHOOTING.md)。

</details>

### 升级与刷新项目

更新 CLI 和刷新项目中已安装的命令是两个独立步骤：

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

只需要一种集成时，使用 `--ai claude` 或 `--ai codex`。`--force` 会重新生成分发的命令/脚本，并刷新审查资源；还会自动确认迁移、命令更新和宪法合规提示。既有需求和项目原则会保留；更新托管指引时，会保留已有上下文文件的正文；未明确设置的配置键也会保留。

计划命令为 `design-to-plan`；安装更新会移除旧的 `spec-to-plan` 入口，且不保留别名。

### 通过插件市场安装

Claude Code 可以通过插件市场安装：

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

插件提供命令和会话启动指引，用于暂存提交分析和历史需求回顾，也覆盖恢复的会话。安装插件不会初始化项目。使用 `/codexspec:config` 创建或修改语言、工作流和审查设置；需要完整项目骨架时，使用 CLI 初始化。

直接预览提交和已获授权的原地提交可以使用随插件提供的运行时，只需 Python 3.11+ 和 Git，无需持久安装 CodexSpec CLI。Worktree 路由、蓝图/auto-dev 和手动 profile 审阅仍需要 CLI。插件启动钩子要求 PATH 中有 Git，并要求 Claude Code 版本支持命令钩子的 `args`（exec 形式）。该指引面向代理；不会拦截手动 Git 命令。

详细设置见[安装指南](docs/en/getting-started/installation.md)。

## 核心工作流

标准功能工作流保留相互引用来源的产物链：

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

以下示例使用 Claude 的 `/codexspec:` 前缀。在 Codex 中，使用 `$codexspec:`，命令名称和参数保持相同。

| 步骤 | 命令 | 目的与产物 |
|------|---------|--------------------|
| 项目原则 | `/codexspec:constitution` | 创建/更新 `constitution.md`，并验证受影响的产物 |
| 需求 | `/codexspec:specify <idea>` | 讨论意图、确认最终摘要，并持久保存 `requirements.md` |
| 规格 | `/codexspec:generate-spec <feature-dir>` | 将已确认需求编译为带来源引用的 `spec.md` |
| 系统设计 | `/codexspec:spec-to-design <feature-dir>` | 生成 `design.md`：组件、接口和关键设计决策 |
| 实现计划 | `/codexspec:design-to-plan <feature-dir>` | 生成 `plan.md`：阶段、顺序和验证 |
| 任务 | `/codexspec:plan-to-tasks <feature-dir>` | 生成可追溯、可验证的 `tasks.md`；执行跨产物分析 |
| 实现 | `/codexspec:implement-tasks <feature-dir>` | 执行任务、验证结果，并修复独立核实的审查发现 |

将 `<feature-dir>` 替换为需求讨论阶段返回的功能目录。在对应 worktree 中继续，或传入其明确路径；这样可以在不同命令和会话间保持同一个功能身份。

### specify、clarify 与 analyze

- **specify** 开始或重新讨论需求。只有明确确认后，需求摘要才成为约束依据。
- **clarify** 解决既有需求/规格中的歧义：每次最多提出五个问题，覆盖四类问题。先更新 `requirements.md`，再同步 `spec.md`。
- **analyze** 检查完整的需求 → 规格 → 设计 → 计划 → 任务链。当下游产物的修正可以由上游权威依据确定时，自动应用确定性的修正；绝不修改 `requirements.md`。未解决的发现会被报告。任务审查通过后会自动运行；它提供信息，不作为实现门禁。

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### 使用 Quick 处理小型变更

局部修复等范围小、边界清晰的变更可以使用 `quick`：

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick 确认并持久保存简明需求摘要，然后调用生成命令及其审查，编排规格、计划、任务和实现。范围广或存在未定产品/设计选择的变更应使用标准工作流；Quick 需要新决策时会暂停。

### 工作流自动化

`workflow.auto_next` 默认为 **false**。当当前工作空间配置中的值为 `true` 时，最终需求确认后会推进到规格阶段。各生成阶段在 `PASS` 或 `PASS_WITH_WARNINGS` 后继续推进；`NEEDS_REVISION` 或 `BLOCKED` 会停止流程。`implement-tasks` 是最后阶段。

产物自动修复仅限于经验证的缺陷，且修正必须有上游证据支持；最多执行两轮修复与重审。建议单独列出。实现阶段的审查/修复循环有独立的完成规则，详见下文。

详细约定见[工作流指南](docs/en/user-guide/workflow.md)。

## 共享蓝图与自主开发

希望在开发前准备多条已确认需求时，使用 `blueprint`；使用 `auto-dev` 开发该队列：

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

蓝图讨论会先解决由用户决定的方向、选择和约束，再将需求纳入队列。共享的 `.codexspec/blueprint.md` 使用 `pending`、`in_progress` 和 `completed` 状态。可以追加、替换、删除或重排待处理需求；蓝图维护对正在开发和已完成的条目只读。

Auto-dev 按文档顺序工作，先恢复进行中的功能，再开始下一个；每次完成后重新读取队列，因此新追加的待处理需求也可加入本次运行。它在已确认需求范围内执行 SDD 阶段、实现、验证、审查和修复。调用 `auto-dev` 会独立于 `workflow.auto_next` 启用自身自动化，且不修改该设置。

两个命令共享分支 `codexspec/auto-dev` 上的 `worktree-for-codexspec-auto-dev`。它们可在共享所有权和写入保护机制下并发运行；需求在该工作空间中按顺序开发。正常自主执行期间，无法根据已确认需求解决的产品决策会带证据停止运行，而非发起询问。

只读查看当前共享蓝图：

```bash
codexspec show-blueprint
```

## Worktree 开发

Git worktree 是同一仓库的另一个工作目录，拥有独立检出的分支。CodexSpec 默认给每个普通功能使用一个 worktree，在首次写入需求前创建，并将该功能的文档、实现、测试和修复保存在一起。

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

继续开发功能时，会复用其工作空间。独立的配置、宪法和 profile 变更使用维护 worktree；在当前功能中做出的变更留在该功能工作空间。配置**仅作用于所在 checkout**：在路由后的 worktree 中改变设置，会先在那里生效，并通过 Git 集成到其他 checkout。应在返回的工作空间内运行 CLI 命令和检查。

新功能的基线根据 Git 祖先关系比较已提交的本地主分支与获取的远端主分支历史。历史发生分叉时，在新 worktree 中合并，并要求验证。获取失败会发出警告，允许使用本地已有引用；创建失败不会退回主 checkout 写入。

`workflow.worktrees` 默认为 **true**；只有字面 YAML `false` 才会关闭普通功能和维护工作的隔离。无论该设置如何，蓝图/auto-dev 都保留固定的共享 worktree。初始化和安装更新作用于你明确选定的 checkout。已完成的 worktree 会保留；完成不会自动合并或删除它们。

见 [Worktree 开发](docs/en/user-guide/workflow.md#worktree-development)和[配置说明](docs/en/reference/configuration.md#workflowworktrees)。

## 处理既有代码

两个入口分别服务于不同目标：

| 命令 | 用途 | 产物/边界 |
|---------|-----------|-----------------|
| `onboard [path]` | 从既有代码库初始化可复用项目知识 | profile 中的候选惯例和有明确证据支持的约束；代码只读 |
| `reverse-spec [path]` | 理解现有架构，或比较代码与已确认意图 | 草案产物或偏差报告；代码只读 |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard 从可观察代码中推断惯例，仅根据明确禁令提出约束。候选惯例立即在本地生效；候选约束需要在本会话中决定保留、编辑或丢弃。它保留既有知识，不会凭冷启动扫描虚构过往决策理由或经验性陷阱。

Reverse-spec 有三种模式：

- **概览**：不指定路径或指定仓库根目录，生成简要架构 `design.md` 和用于选择待检查模块的 `slices.md`。
- **生成**：模块路径没有已确认基线时，生成草案 `spec.md`、`design.md` 及开放/推断的需求。
- **核对**：模块具有已确认基线时，生成 `reconcile.md`，报告未记录的行为、未实现的规格，以及相对于已确认规格/设计的语义不一致；意图以需求为准。

推断草案必须经人工确认后才能成为基线。核对报告会提出方向——修复代码、更新文档或决定意图——但不会自动执行。

## 审查与调试

四个产物审查命令检查忠实度、覆盖率、可行性和内部质量：`review-spec`、`review-design`、`review-plan` 和 `review-tasks`。生成后会自动运行，也支持手动调用。报告区分经验证的缺陷、不阻断流程的风险建议和设计机会，并给出兼容性评分。

`review-code` 提供独立的、以所选变更为范围的缺陷门禁，以及明确的整体代码质量评估：

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

默认审查覆盖功能分支的完整变更，包括已提交、已暂存、未暂存和未被忽略的未跟踪变更。可以明确选择已提交、未提交或单次提交的证据。`--feature` 附加需求上下文，不缩小 Git 范围。`--audit` 评估指定路径，输出建议性评分表，而非完成判定。

审查从 `.codexspec/review-code/` 加载共享标准，选择相关行为维度和语言/框架检查。发现必须有具体证据、可触发的条件、对所选变更的归因及影响。审查者报告缺陷和有依据的维护建议，不编辑文件；修复调用方独立核实这些发现。

实现时，代码任务先写测试；文档/配置直接实现并进行适当检查。修复后，增量重审可以复用未受影响的覆盖；最终验收要求一次全新完整功能审查得出 `PASS`、完成覆盖与验证，且已纳入的 P0–P3 缺陷为零。有依据的维护建议单独报告。

`workflow.auto_maintenance` 默认为 **true**，控制修复调用方是否同时应用经过验证且兼容的维护改进。关闭后仍报告建议，且不免除缺陷修复或必需检查。它独立于阶段推进，也不是 `implement-tasks` 的参数。

根因优先的调试方式：

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug 按调查 → 模式分析 → 单一假设验证 → 先写失败测试再修复的顺序执行。实现阶段在修复停滞、非简单正确性缺陷需要追踪，或同类根因跨审查轮次再次出现时升级到这一流程。连续三次修复失败会触发架构重评。

使用 `checklist` 评估需求清晰度、完整性和一致性：

```text
/codexspec:checklist Check the authentication requirements for completeness
```

审查选择器、参数和详细流程见[命令参考](docs/en/user-guide/commands.md)。

## 项目知识

项目 profile 将可复用知识保存在 `.codexspec/profile/`：

| 类别 | 内容 |
|----------|----------|
| `constraints/` | 明确禁令和硬边界，优先读取 |
| `conventions/` | 模式、命名及跨功能指引 |
| `pitfalls/` | 经历过的陷阱、成因、变通办法和经验 |
| `decisions/` | 可复用的架构及跨功能决策 |
| `strategies/` | 提示需要换一种工作方式的信号 |
| `runbooks/` | 有顺序的操作流程和失败恢复 |

`distill` 从工作中提炼可复用知识；功能特定的意图仍保存在该功能的需求/设计/计划中。Init 在 CLAUDE.md 和/或 AGENTS.md 中安装指引，要求在实质性工作前读取全部约束和相关知识。后续新增知识无需重新初始化即可生效。候选记录应谨慎使用；已验证记录需要结果验证和人工认可。

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

手动执行 `distill review`，或直接执行没有新素材可捕获的 `distill`，会打开本地离线浏览器工作空间。可以修改、验证、丢弃、延后和合并记录，预览最终 Markdown，然后选择 **Apply all**（应用全部）。决定保存在可恢复草稿中，直到应用；冲突检查会防止部分应用或静默覆盖。不具备浏览器的环境可明确使用文本回退方式。

`workflow.auto_distill` 默认为 **true**，控制三个收尾钩子：成功的 `implement-tasks`、通过 `commit-staged` 实际执行的提交，以及 `pr` 生成。提交预览不会触发捕获。

已安装的项目指引还要求代理在普通对话、SDD 之外的修复和长时间 `implement-tasks` 执行过程中及时捕获可复用知识。该指引独立于收尾设置；任务结束时的捕获提供最后一道保障。

同一会话中的重复触发只处理新增素材。跨会话时，`distill` 会读取 profile 并跳过已覆盖的知识。没有剩余可复用知识时，不写入文件便退出。自动捕获绝不会打开手动审阅、等待人工或阻断调用方工作流。

`evolve` 只选择在项目外也有价值的已验证知识，编译为命令/skill 草案，并在推送或创建供人工审查的贡献 PR 前取得明确批准。

详细指引见[项目知识](docs/en/user-guide/commands.md#codexspecdistill)。

### 复用历史决策

在做出实质性需求、设计、实现、调试或审查判断前，也会查阅 `.codexspec/specs/` 下的相关历史；普通对话和 SDD 工作流都适用。代理会先还原未改变的决策、后续补充和明确替换，再询问用户。

较早且未改变的需求继续适用。用户最新的明确决定始终优先；开放提案不视为已确认意图。检索范围限定在当前任务内，并复用足够的背景资料。刷新现有项目安装即可获得这项指引。

## Git 工作流

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** 分析准确的暂存区，生成 Conventional Commits 提交信息；`-p` 只预览，不提交。调用工作流选择并暂存文件。获授权的执行使用受保护运行时，重新检查提交内容与分析是否一致。代理提交指引适用于普通对话、SDD、蓝图和 auto-dev 工作流；命令可用并不表示已经调用，也不构成提交授权。
- **pr** 根据 diff 生成结构化的 GitHub PR 或 GitLab MR 描述。`--spec` 可通过 `spec.md` 文件路径，或解析到该文件的功能目录名/前缀，添加功能上下文。默认输出为供托管平台使用的文本。
- **release-notes** 从 Git 历史生成 Keep a Changelog 条目和发布正文。默认章节为 `[Unreleased]`；`--version` 使用提供的标签。它不会暂存、提交、升级版本、打标签、发布或创建 release。
- **tasks-to-issues** 从已有任务创建 GitHub issues，包含依赖和验收标准。需要已认证的 GitHub CLI，并检查 issue 仓库与配置的远端是否一致。

直接预览提交和获授权的原地提交需要 Python 3.11+ 和 Git；运行时随 CLI 项目安装，并内置于 Claude 插件。有内容变更的代理合并也使用暂存分析。只连接历史的合并保留 Git 默认信息，同时验证树和父提交；快进不创建提交。

## 可用命令

CLI 有六个公共命令。代理集成分发 28 个命令：Claude 使用 `/codexspec:<name>`，Codex 使用 `$codexspec:<name>`。下方表格为方便阅读使用 Claude 的写法。

### CLI 命令

| 命令 | 用途 |
|---------|---------|
| `codexspec init` | 为 Claude、Codex 或两者初始化或刷新项目 |
| `codexspec check` | 检查已安装的工具和依赖 |
| `codexspec version` | 显示版本和系统信息 |
| `codexspec config` | 查看或修改项目配置 |
| `codexspec list-commands` | 按类别列出可用代理命令 |
| `codexspec show-blueprint` | 只读打印共享 worktree 的蓝图 |

### 核心工作流命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:constitution` | 创建/更新项目原则，并进行跨产物验证 |
| `/codexspec:specify` | 讨论、确认并持久保存功能需求 |
| `/codexspec:blueprint` | 准备或维护已确认的待处理蓝图需求 |
| `/codexspec:generate-spec` | 将已确认需求编译为可追溯规格；自动审查 |
| `/codexspec:spec-to-design` | 定义架构、组件、接口和决策；自动审查 |
| `/codexspec:design-to-plan` | 规划实现阶段、顺序和验证；自动审查 |
| `/codexspec:plan-to-tasks` | 生成覆盖上游产物的可验证任务；自动审查和分析 |
| `/codexspec:implement-tasks` | 执行任务、验证结果、审查并修复 |
| `/codexspec:auto-dev` | 按文档顺序自主开发已确认的蓝图需求 |

### 产物审查命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:review-spec` | 检查规格忠实度和内部质量 |
| `/codexspec:review-design` | 检查设计忠实度、可行性和规划就绪度 |
| `/codexspec:review-plan` | 检查计划忠实度、可行性和实现就绪度 |
| `/codexspec:review-tasks` | 检查任务忠实度、依赖、可执行性和验证 |

### 需求、既有代码与调试

| 命令 | 用途 |
|---------|---------|
| `/codexspec:clarify` | 解决需求歧义，先更新需求，再更新规格 |
| `/codexspec:analyze` | 检查端到端可追溯性，使下游产物符合权威依据 |
| `/codexspec:checklist` | 生成需求质量检查清单 |
| `/codexspec:tasks-to-issues` | 将已有任务转为可操作的 GitHub issues |
| `/codexspec:debug` | 调查根因后再修复 |
| `/codexspec:reverse-spec` | 概览现有架构、生成模块草案，或报告相对于基线的偏差 |

### 项目知识命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:distill` | 捕获可复用知识，或在本地工作空间审阅候选记录 |
| `/codexspec:evolve` | 将已验证知识编译为上游贡献草案 |
| `/codexspec:onboard` | 初始化候选惯例和有证据支持的约束 |

### Git 与代码审查命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:commit-staged` | 根据暂存变更生成信息；预览或执行获授权的提交 |
| `/codexspec:pr` | 生成结构化 PR/MR 描述 |
| `/codexspec:release-notes` | 维护 changelog 条目，并生成发布正文 |
| `/codexspec:review-code` | 以缺陷门禁审查所选变更；使用 `--audit` 评估路径质量 |

### 实用命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:config` | 交互式创建/查看/修改/重置项目配置 |
| `/codexspec:quick` | 为小型变更运行简明的需求优先 SDD 工作流 |

## 配置与国际化

配置位于 `.codexspec/config.yml`。模板保持英文；代理按配置的语言编写交互文字和生成的产物。13 个标准语言代码为 `en`、`zh-CN`、`zh-TW`、`ja`、`ko`、`es`、`fr`、`de`、`pt`、`ru`、`it`、`ar` 和 `hi`。葡萄牙语 CLI 代码为 `pt`；本地化文档和翻译目录使用 `pt-BR`。

### 语言维度

| 维度 | 配置键 | 初始化时 | 后续设置 | 控制范围 |
|-----------|------------|-------------------|-----------|----------|
| 输出/基础 | `language.output` | `--lang` | `config --set-lang` | 其他语言维度的回退值 |
| 交互 | `language.interaction` | `--interaction-lang` | `config --set-interaction-lang` | 对话和 CLI 输出 |
| 文档 | `language.document` | `--document-lang` | `config --set-document-lang` | 需求、规格、设计、计划、任务 |
| 提交 | `language.commit` | `--commit-lang` | `config --set-commit-lang` | 提交信息和 Git 交付内容 |

每个具体语言维度独立回退到 `language.output`，再回退到 `en`。`language.templates` 保持为 `en`。

```bash
codexspec init my-project --ai both \
  --interaction-lang zh-CN --document-lang en --commit-lang en

codexspec config
codexspec config --set-document-lang en
codexspec config --list-langs
```

首次在 TTY 中初始化时，除非提供 `--lang` 或全部三个具体语言选项，否则会询问基础语言。`--force` 自动确认其他初始化提示，但不取消语言选择。非 TTY 初始化默认为英文。重新初始化会保留未明确设置的语言键。

### 工作流与审查设置

| 设置 | 默认值 | 作用 | CLI 控制 |
|---------|---------|--------|-------------|
| `workflow.auto_next` | `false` | 推进通过审查的普通 SDD 阶段 | `config --auto-next on\|off` |
| `workflow.auto_distill` | `true` | 成功收尾后以非交互方式捕获知识 | `config --auto-distill on\|off` |
| `workflow.auto_maintenance` | `true` | 自动修复时应用已验证的增量维护改进 | `config --auto-maintenance on\|off` |
| `workflow.worktrees` | `true` | 隔离普通功能和独立维护工作 | `config --worktrees on\|off` |
| `review.decided_by` | `reviewer` | 由谁决定项目运行上下文之外触发的发现 | `config --decided-by reviewer\|ask` |

布尔 CLI 开关接受不区分大小写的 `on/true/1/yes` 和 `off/false/0/no`，也允许前后空白。不带值的布尔开关会切换目标 checkout 的当前值；YAML 存储值为布尔类型。

设置 `review.decided_by: reviewer` 时，审查者决定缺陷是否纳入。设置为 `ask` 时，上下文之外的触发条件会成为待定场景决策：用户一次性决定修复还是排除该场景，已确认决策供后续轮次使用。待定决策会阻止完成。单次 `review-code` 可用 `--decided-by` 覆盖配置模式。

配置写入遵循 worktree 路由。从主 checkout 发起的独立变更写在维护 worktree，不会立即改变 main 的有效设置；功能 worktree 中的变更在那里生效。

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
| `--force`, `-f` | 重新生成已安装产物，自动确认迁移/更新/合规提示；保留项目编写的上下文和无关配置 |
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
| `--worktrees` | 切换/设置仅作用于当前 checkout 的 worktree 隔离 |
| `--decided-by` | 设置 `reviewer` 或 `ask` 审查决策模式 |

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

语言和设置的详细行为见[配置](docs/en/reference/configuration.md)和[国际化](docs/en/user-guide/i18n.md)。

## 项目结构

初始化会安装公共资源及选定的助手集成：

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

共享蓝图位于专用 auto-dev worktree，不是在每个普通 checkout 中各保存一份可编辑副本。手动知识审阅草稿不纳入 Git。

## 扩展开发资料

仓库包含扩展清单模板、示例命令和[扩展开发指南](extensions/EXTENSION-DEVELOPMENT-GUIDE.md)。这些是编写扩展的资料。当前 CLI 没有扩展安装/列出/移除命令，也不会自动加载 `extension.yml` 中的命令或钩子。共享审查资源支持在 `.codexspec/review-code/` 下添加项目特定内容；初始化会保留既有资源修改和附加文件，除非明确要求替换。

## 开发

```bash
git clone https://github.com/Zts0hg/codexspec.git
cd codexspec

# Development tools are an optional dependency extra
uv sync --extra dev
# For documentation builds too: uv sync --extra dev --extra docs

uv run codexspec --help
uv run pytest
uv run ruff check src/
uv build
```

修改模板、打包或初始化行为前，请阅读 [CLAUDE.md](CLAUDE.md)、[AGENTS.md](AGENTS.md) 和[仓库布局](docs/internal/repository-layout.md)。分发的命令和 skill 副本是生成的安装产物；应编辑其权威来源并重新生成。

## 贡献

本地设置和贡献指引见[贡献指南](docs/en/development/contributing.md)。贡献应保留已确认需求、来源可追溯性，以及用户与维护者的打包边界。

## 许可证

MIT — 见 [LICENSE](LICENSE)。

## 致谢

灵感来自 [GitHub spec-kit](https://github.com/github/spec-kit)。
集成 Claude Code 和 OpenAI Codex。
