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

CodexSpec 将已确认的需求逐步转化为可追溯的规格说明、设计、计划、任务和具体实现。你来决定做什么、为什么做；智能体则在这些需求的约束下制定实现方案，通过阶段审查把关，并结合长期保存的项目知识推进开发。

你可以通过 Claude Code 的斜杠命令或 Codex 技能使用 CodexSpec，也可以将两种方式配合使用。常规功能开发默认在各自独立的 Git worktree 中进行。如果需要，还可以使用共享蓝图，让智能体按顺序自主推进已确认需求的开发。

[📖 文档](https://zts0hg.github.io/codexspec/) | [中文文档](https://zts0hg.github.io/codexspec/zh/) | [日本語ドキュメント](https://zts0hg.github.io/codexspec/ja/) | [한국어 문서](https://zts0hg.github.io/codexspec/ko/) | [Documentación](https://zts0hg.github.io/codexspec/es/) | [Documentation](https://zts0hg.github.io/codexspec/fr/) | [Dokumentation](https://zts0hg.github.io/codexspec/de/) | [Documentação](https://zts0hg.github.io/codexspec/pt-BR/)

## 目录

- [为什么选择 CodexSpec？](#为什么选择-codexspec)
- [30 秒快速入门](#30-秒快速入门)
- [安装](#安装)
- [核心工作流](#核心工作流)
- [共享蓝图与自主开发](#共享蓝图与自主开发)
- [Worktree 开发](#worktree-开发)
- [处理现有代码](#处理现有代码)
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
| 明确要做什么 | 先确认需求，再编写规格；已确认需求保存在 `requirements.md` 中 |
| 让开发过程有据可查 | 需求 → 规格 → 设计 → 计划 → 任务，每一步都引用其依据 |
| 检查开发中的决策 | 四个文档审查命令、跨文档一致性分析，以及独立的代码缺陷门禁 |
| 换个会话或接手人也能继续 | 保留功能记录、项目原则、可复用知识和相关历史决策 |
| 同时推进多个功能 | 每个常规功能使用独立的 Git worktree，后续开发继续复用同一工作区 |
| 减少手动推进 | 可选择自动衔接开发阶段，或让智能体自主开发蓝图中已确认的需求 |
| 团队语言偏好 | 独立设置交互、文档和提交语言 |

### 什么是需求优先 SDD？

需求优先的规格驱动开发（Requirements-First Spec-Driven Development）以**已确认的需求作为功能开发的最高依据**。智能体先记录目标、约束、决策、不做的事项、待解决的问题以及用户确认的依据，再据此编写后续文档并实现功能。

```text
Idea → Confirmed Requirements →     Spec    →     Design    →     Plan    →    Tasks     →     Code
                 ↓                   ↓              ↓              ↓             ↓              ↓
         User confirmation      review-spec   review-design   review-plan   review-tasks   review-code
```

需求由你确认；从规格到代码，后续各项产物都有对应的审查环节。

产品要做什么、为什么做，由人与智能体协作讨论和调整；自动审查负责检查后续产物是否符合这些决定。启用自动化后，通过审查的阶段会继续向下推进，但智能体仍不能擅自改写已确认的需求。

## 30 秒快速入门

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

完成初始化后，在项目目录中启动你已安装的助手。两种助手使用相同的工作流，调用方式分别为：

| 助手 | 开始需求讨论 |
|-----------|------------------------------|
| Claude Code (`claude`) | `/codexspec:specify I want to build a todo application` |
| Codex (`codex`) | `$codexspec:specify I want to build a todo application` |

如需定制项目原则，可以使用 `constitution`。确认最终需求摘要后，在命令返回的功能目录和工作区中继续开发。后续步骤见[核心工作流](#核心工作流)。

使用 Codex 桌面应用？可以[让 Codex 安装并初始化你的项目](#通过-codex-桌面应用安装)。

## 安装

### 通过 Codex 桌面应用安装

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

### 前置要求

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)（推荐），或 pip
- 要使用的助手：Claude Code 或 Codex
- Git：用于 worktree 开发和 Git 操作

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

新建项目可运行 `codexspec init my-project --ai claude`；初始化当前目录可运行 `codexspec init . --ai codex`。如果要同时使用两个助手，请指定 `--ai both`。默认助手是 `claude`，使用 Codex 或同时使用两者时，需要明确指定相应选项。

<details>
<summary>其他安装方式</summary>

#### 一次性初始化

```bash
uvx codexspec init my-project --ai claude
uvx codexspec init . --ai codex
```

一次性初始化会安装项目命令和可独立运行的提交辅助程序。不过，worktree 路由、蓝图/auto-dev 和手动审阅项目知识仍需要调用 CodexSpec CLI；使用这些工作流时，请确保 CLI 可用。

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

如果遇到 PATH 或安装问题，请查阅 [Windows 故障排除指南](docs/en/WINDOWS-TROUBLESHOOTING.md)。

</details>

### 升级与刷新项目

更新 CLI 和刷新项目中已安装的命令是两个独立步骤：

```bash
uv tool install codexspec --upgrade
# Or: pip install --upgrade codexspec

# In the project you want to refresh; select its desired integration(s)
codexspec init . --force --ai both
```

如果只使用一个助手，请选择 `--ai claude` 或 `--ai codex`。`--force` 会重新生成随安装提供的命令和脚本、刷新审查资源，并自动确认迁移、命令更新和项目宪法合规提示。已有需求和项目原则会保留；上下文文件中的自动维护指引会更新，原有正文不会被替换；未明确修改的配置项也会保留原设置。

编写实现计划使用 `design-to-plan`。更新安装时会移除旧的 `spec-to-plan` 入口，不提供兼容别名。

### 通过插件市场安装

Claude Code 可以通过插件市场安装：

```text
/plugin marketplace add Zts0hg/codexspec
/plugin install codexspec@codexspec-market
/codexspec:config
```

插件会提供命令，并在新建或恢复会话时加载指引，要求先分析暂存内容再提交、先回顾相关历史需求再作判断。安装插件本身不会初始化项目。可以用 `/codexspec:config` 创建或修改语言、工作流和审查设置；如果需要完整的项目目录与资源，请通过 CLI 初始化。

预览提交，以及在当前工作区执行已获授权的提交，都可以使用插件自带的运行时；只需 Python 3.11+ 和 Git，无需长期安装 CodexSpec CLI。Worktree 路由、蓝图/auto-dev 和手动审阅项目知识仍需要 CLI。插件的启动钩子要求 Git 已加入 PATH，且 Claude Code 版本支持命令钩子的 `args`（exec 形式）。这些指引供智能体遵守，不会拦截你手动执行的 Git 命令。

详细设置见[安装指南](docs/en/getting-started/installation.md)。

## 核心工作流

标准功能开发会依次生成以下产物，每一步都保留对前序依据的引用：

```text
/specify          → requirements.md
/generate-spec    → spec.md       → review-spec
/spec-to-design   → design.md     → review-design
/design-to-plan   → plan.md       → review-plan
/plan-to-tasks    → tasks.md      → review-tasks → analyze
/implement-tasks  → implementation and complete-feature code review
```

下面的示例使用 Claude 的 `/codexspec:` 前缀。在 Codex 中，将前缀换成 `$codexspec:` 即可，命令名称和参数不变。

| 步骤 | 命令 | 目的与产物 |
|------|---------|--------------------|
| 项目原则 | `/codexspec:constitution` | 创建/更新 `constitution.md`，并验证受影响的产物 |
| 需求 | `/codexspec:specify <idea>` | 讨论意图、确认最终摘要，并持久保存 `requirements.md` |
| 规格 | `/codexspec:generate-spec <feature-dir>` | 根据已确认需求编写 `spec.md`，并标明需求来源 |
| 系统设计 | `/codexspec:spec-to-design <feature-dir>` | 生成 `design.md`：组件、接口和关键设计决策 |
| 实现计划 | `/codexspec:design-to-plan <feature-dir>` | 编写 `plan.md`，安排实现阶段、先后顺序和验证方式 |
| 任务 | `/codexspec:plan-to-tasks <feature-dir>` | 编写可追溯、可验证的 `tasks.md`，并检查各文档是否一致 |
| 实现 | `/codexspec:implement-tasks <feature-dir>` | 执行任务、验证结果，并修复经独立核实的审查问题 |

将 `<feature-dir>` 替换为需求讨论阶段返回的功能目录。后续操作应在对应的 worktree 中执行，或明确传入该目录的路径，这样更换命令或会话后仍会处理同一个功能。

### specify、clarify 与 analyze

- **specify** 用于开始需求讨论，也可重新讨论已有需求。需求摘要只有经用户明确确认后，才成为后续工作的依据。
- **clarify** 用于澄清已有需求和规格中的歧义。每次最多提出五个问题，检查范围涵盖四类问题；先更新 `requirements.md`，再同步修改 `spec.md`。
- **analyze** 检查需求 → 规格 → 设计 → 计划 → 任务的完整链路。如果根据上游依据能够确定下游文档应如何修正，就会自动修正；它绝不修改 `requirements.md`，无法解决的问题会明确报告。任务审查通过后会自动运行，结果供后续参考，不作为阻止实现的门禁。

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

### 使用 Quick 处理小型变更

对于局部修复等范围小、边界明确的变更，可以使用 `quick`：

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick 会先确认并保存一份精简的需求摘要，再依次调用生成命令及相应审查，推进规格、计划、任务和实现。如果变更涉及较大范围，或仍有产品和设计选择尚未确定，应使用标准工作流。需要用户作出新决定时，Quick 会暂停。

### 工作流自动化

`workflow.auto_next` 默认为 **false**。如果当前工作区将其设置为 `true`，确认最终需求后就会自动进入规格阶段。各生成阶段得到 `PASS` 或 `PASS_WITH_WARNINGS` 时会继续推进，得到 `NEEDS_REVISION` 或 `BLOCKED` 时则停止。`implement-tasks` 是最后一个阶段。

自动修正文档时，只处理已经验证的缺陷，且修正方式必须有上游依据支持；最多进行两轮修复和重新审查。建议另行列出。实现阶段的审查与修复遵循另一套完成标准，详见下文。

详细约定见[工作流指南](docs/en/user-guide/workflow.md)。

## 共享蓝图与自主开发

如果希望先把多条需求讨论并确认，再逐项开发，可以用 `blueprint` 整理需求，用 `auto-dev` 推进这组需求的开发：

```text
/codexspec:blueprint Add a confirmed requirement for task reminders
/codexspec:auto-dev
```

需求进入开发队列前，蓝图讨论会先明确需要由用户决定的方向、方案选择和约束。共享蓝图 `.codexspec/blueprint.md` 使用 `pending`、`in_progress` 和 `completed` 标记状态。待处理需求可以追加、替换、删除或调整顺序；正在开发和已完成的条目只允许查看，不能通过蓝图维护操作修改。

Auto-dev 按蓝图中的顺序开发需求。如果已有功能正在进行，会先接着完成它，再开始下一个。每完成一项，都会重新读取队列，因此运行期间新追加的待处理需求也能接着开发。整个过程在已确认的需求范围内完成 SDD 各阶段、实现、验证、审查和修复。调用 `auto-dev` 本身就会启用这一自动化流程，不受 `workflow.auto_next` 控制，也不会修改该设置。

这两个命令共用 `codexspec/auto-dev` 分支和 `worktree-for-codexspec-auto-dev` 工作区。它们可以同时运行，由共享机制协调工作区的使用并保护写入操作；需求开发则仍在该工作区内按顺序进行。自主执行中若遇到无法依据已确认需求作出的产品决定，会停止运行并说明依据，而不会在正常执行过程中发起询问。

只读查看当前共享蓝图：

```bash
codexspec show-blueprint
```

## Worktree 开发

Git worktree 是同一仓库的另一个工作目录，可以检出自己的分支。CodexSpec 默认在首次写入需求前，为每个常规功能创建独立的 worktree，让该功能的文档、实现、测试和修复始终留在同一个工作区内。

```text
projects/
├── my-project/
└── my-project-codexspec-worktrees/
    ├── <feature-id>-task-reminders/
    ├── <feature-id>-search/
    ├── worktree-for-codexspec-maintenance/
    └── worktree-for-codexspec-auto-dev/
```

继续开发已有功能时，会复用原来的工作区。单独修改配置、项目宪法或项目知识时，使用维护 worktree；开发当前功能时所做的这些修改，则留在该功能的工作区。配置**按 checkout 分别保存和生效**：修改某个 worktree 的设置，只会先影响该工作区，之后通过 Git 集成才会传到其他 checkout。CLI 命令和检查也应在返回的工作区中运行。

创建新功能时，会根据 Git 的提交祖先关系，比较本地主分支上已提交的历史与获取到的远端主分支历史，以确定开发基线。两者分叉时，会在新的 worktree 中合并并要求验证。获取远端失败时会提示警告，此时仍可使用本地已有引用；创建工作区失败时，不会改为向主 checkout 写入。

`workflow.worktrees` 默认为 **true**。只有将 YAML 值明确设为 `false`，才会关闭常规功能和维护工作的工作区隔离。蓝图/auto-dev 不受这一设置影响，始终使用固定的共享 worktree。初始化和安装更新会直接作用于你明确选择的 checkout。功能完成后，worktree 会保留，不会自动合并或删除。

见 [Worktree 开发](docs/en/user-guide/workflow.md#worktree-development)和[配置说明](docs/en/reference/configuration.md#workflowworktrees)。

## 处理现有代码

针对已有代码，可以按目的选择以下入口：

| 命令 | 用途 | 产物/边界 |
|---------|-----------|-----------------|
| `onboard [path]` | 从已有代码库提取可复用的项目知识 | 在项目知识库中建立候选惯例和有明确证据的约束；不修改代码 |
| `reverse-spec [path]` | 理解现有架构，或检查代码是否符合已确认的意图 | 生成文档草案或偏差报告；不修改代码 |

```text
/codexspec:onboard src/
/codexspec:reverse-spec
/codexspec:reverse-spec src/auth
```

Onboard 根据实际代码推断项目惯例，只有发现明确禁令时才会提出约束。候选惯例会立即在本地生效；候选约束则需要在当前会话中由用户决定保留、修改还是丢弃。已有知识会保留；仅凭一次初始扫描，不会编造过去的决策理由，也不会把未经经历的问题写成经验教训。

Reverse-spec 有三种模式：

- **概览**：不指定路径，或指定仓库根目录时，生成简要的架构说明 `design.md` 和模块划分文件 `slices.md`，帮助选择接下来要检查的模块。
- **生成**：指定的模块没有已确认基线时，生成 `spec.md`、`design.md` 草案，以及尚待确认或根据代码推断的需求。
- **核对**：模块已有确认过的基线时，生成 `reconcile.md`，列出尚未记录的行为、规格中尚未实现的内容，以及代码与已确认规格和设计之间的语义差异；判断产品意图时，以需求为准。

根据代码推断的草案，必须经人工确认才能作为后续基线。核对报告会建议下一步是修复代码、更新文档，还是先明确产品意图，但不会自动执行这些修改。

## 审查与调试

`review-spec`、`review-design`、`review-plan` 和 `review-tasks` 这四个文档审查命令，会检查文档是否忠于上游依据、覆盖是否完整、方案是否可行，以及文档自身的质量。生成文档后会自动审查，也可以手动调用。报告会区分已经验证的缺陷、不会阻止流程继续的风险建议和可改进的设计，并给出兼容性评分。

`review-code` 提供独立的代码缺陷门禁，审查范围由所选变更决定；也可以明确选择对完整代码进行质量评估：

```text
/codexspec:review-code --feature <feature-dir>
/codexspec:review-code --uncommitted
/codexspec:review-code --audit src/
```

默认审查会检查功能分支上的全部变更，包括已提交、已暂存、未暂存，以及未被忽略的未跟踪内容。也可以明确限定为已提交变更、尚未提交的变更，或某一次提交。`--feature` 用于提供功能需求背景，不会缩小 Git 变更范围。`--audit` 则评估指定路径的代码质量，给出建议性评分，不作出功能是否完成的判定。

审查会从 `.codexspec/review-code/` 读取共享标准，并选择与当前行为、语言和框架有关的检查项。每个问题都必须说明具体证据、触发条件、为何由所选变更引入，以及会造成什么影响。审查者只报告缺陷和有依据的维护建议，不修改文件；负责修复的工作流还需独立核实这些问题。

实现代码任务时，先写测试再实现；文档和配置任务则直接修改，并进行相应检查。修复后的增量审查可以复用未受影响部分的已有检查结果。最终验收仍须重新审查整个功能并得到 `PASS`，完成全部覆盖与验证，且没有尚未解决的已纳入 P0–P3 缺陷。有依据的维护建议另行报告。

`workflow.auto_maintenance` 默认为 **true**，用于控制修复工作流是否一并实施已经验证、且与现有要求兼容的维护改进。关闭后仍会报告这些建议，也仍需修复缺陷、完成必要检查。该设置与阶段自动推进相互独立，不是 `implement-tasks` 的命令参数。

需要先查明根因再修复时，可以使用：

```text
/codexspec:debug Investigate intermittent failures when saving a task
```

Debug 先调查问题，再对照已有模式分析原因，验证一个明确假设，最后编写能复现问题的失败测试并修复。在实现阶段，如果修复迟迟没有进展、需要追查较复杂的正确性问题，或多轮审查反复发现同一类根因，就会转入这一调试流程。三次修复失败后，必须重新评估架构。

使用 `checklist` 评估需求清晰度、完整性和一致性：

```text
/codexspec:checklist Check the authentication requirements for completeness
```

如何选择审查范围、传入参数以及执行详细流程，见[命令参考](docs/en/user-guide/commands.md)。

## 项目知识

可复用的项目知识保存在 `.codexspec/profile/` 中，按以下类别组织：

| 类别 | 内容 |
|----------|----------|
| `constraints/` | 明确禁令和硬边界，优先读取 |
| `conventions/` | 模式、命名及跨功能指引 |
| `pitfalls/` | 实际遇到的问题、根因、应对方法和经验教训 |
| `decisions/` | 可复用的架构及跨功能决策 |
| `strategies/` | 提示何时需要调整工作方法的信号 |
| `runbooks/` | 按步骤执行的操作流程，以及失败后的恢复方法 |

`distill` 用于从工作中提炼可复用的知识；某个功能自身的意图，仍记录在该功能的需求、设计和计划中。Init 会在 CLAUDE.md 和/或 AGENTS.md 中加入指引，要求开展实质性工作前，先读取全部约束和相关知识。以后新增的知识无需重新初始化即可生效。候选记录应谨慎采用；标记为已认可的记录，必须既有实际结果验证，也得到人工认可。

```text
/codexspec:distill Capture the reusable lessons from this work
/codexspec:distill review
/codexspec:evolve
```

手动调用 `distill review`，或在没有新素材可提炼时直接调用 `distill`，会打开本地、离线的浏览器审阅界面。在这里可以修改、认可、丢弃、暂缓处理或合并记录，预览最终 Markdown 后，再选择 **Apply all**（应用全部）。应用前，所有决定都保存在可恢复的草稿中；应用时会检查冲突，避免只写入一部分修改或无提示地覆盖原内容。无法使用浏览器时，可以明确选择文本方式。

`workflow.auto_distill` 默认为 **true**，控制三处任务结束后的自动知识提炼：`implement-tasks` 成功完成后、`commit-staged` 实际创建提交后，以及 `pr` 生成说明后。只预览提交不会触发提炼。

项目指引还要求智能体在普通对话、SDD 之外的修复，以及长时间执行 `implement-tasks` 的过程中，及时提炼新产生的可复用知识。这项要求不受任务结束后的自动提炼设置影响；结束时再提炼一次，用于补上可能遗漏的内容。

同一会话中多次触发时，只处理上次提炼后新增的素材。跨会话时，`distill` 会先读取项目知识库，跳过已经记录的内容。没有新的可复用知识就直接退出，不写入文件。自动提炼不会打开人工审阅界面、等待用户决定，也不会阻止调用它的工作流继续执行。

`evolve` 只采用已经认可、且对其他项目也有价值的知识，将其整理为命令或技能草案。推送变更或创建供人工审查的上游贡献 PR 前，必须获得明确批准。

详细指引见[项目知识](docs/en/user-guide/commands.md#codexspecdistill)。

### 复用历史决策

在就某项变更向你提问前，智能体会先查阅 `.codexspec/specs/` 下相关功能的迭代历史：读取 `requirements.md` 中已确认的决策，追踪后续补充和明确替换的内容，必要时再查阅设计理由或实现依据。在作出设计、实现、调试或审查方面的实质性判断前，也需要做好这项准备；普通对话和 SDD 工作流都适用。

功能目录的时间戳用于梳理迭代顺序，文档较新并不意味着旧决策自动失效。较早确认且未被修改的需求继续有效，尚在讨论的提案也不能当作已确认的意图。检索只围绕当前任务展开，背景足以支持判断时就停止，后续阶段继续复用已准备好的背景。

例如，修改接口时，如果没有回顾历史，智能体可能会问：

> “这个功能应该怎样处理兼容性？”

查阅相关决策并核对当前实现后，就能把问题缩小为：

> “之前确认保留旧接口，当前实现也仍在兼容。本次建议沿用，是否保持？”

已经明确且仍然适用的信息，可以直接复用，无需反复询问。如果你已经明确说“本次移除旧接口”，智能体就应按这个决定推进，并说明迁移影响。**你最新的明确决定始终优先**；历史用于让问询更准确、减少重复提问。

刷新已有项目的安装即可加入这项指引。

## Git 工作流

```text
/codexspec:commit-staged -p
/codexspec:pr --spec <feature-dir>/spec.md
/codexspec:release-notes --from <ref> --to HEAD
/codexspec:tasks-to-issues <feature-dir>
```

- **commit-staged** 只分析当前暂存内容，并据此生成 Conventional Commits 提交信息；`-p` 只预览，不提交。文件由调用它的工作流选择并暂存。执行已获授权的提交时，提交辅助程序会再次检查实际提交内容是否与分析一致。智能体提交指引适用于普通对话、SDD、蓝图和 auto-dev 工作流；命令已安装不等于已经调用，也不代表用户授权了提交。
- **pr** 根据 diff 生成结构化的 GitHub PR 或 GitLab MR 说明。可通过 `--spec` 附加功能背景：既可以传入 `spec.md` 的路径，也可以传入能定位到该文件的功能目录名或前缀。默认输出可直接用于代码托管平台。
- **release-notes** 根据 Git 历史编写 Keep a Changelog 条目和发布说明正文。默认写入 `[Unreleased]` 章节；传入 `--version` 时使用指定的标签。该命令只编写说明，不会暂存、提交、修改版本号、打标签、发布或创建 release。
- **tasks-to-issues** 根据已有任务创建 GitHub issues，并附上任务依赖和验收标准。需要已经登录的 GitHub CLI；创建前会检查目标仓库是否与配置的远端一致。

预览提交，或在当前工作区执行已获授权的提交，需要 Python 3.11+ 和 Git。提交运行时随 CLI 项目安装，也内置于 Claude 插件。智能体创建包含内容变更的合并提交时，同样须先分析暂存内容。仅用于连接提交历史的合并会保留 Git 的默认提交信息，并检查提交树和父提交；快进合并不创建新提交。

## 可用命令

CLI 提供六个公共命令；助手集成提供 28 个命令，Claude 中使用 `/codexspec:<name>`，Codex 中使用 `$codexspec:<name>`。为便于阅读，下表统一使用 Claude 的调用方式。

### CLI 命令

| 命令 | 用途 |
|---------|---------|
| `codexspec init` | 为 Claude、Codex 或两者初始化或刷新项目 |
| `codexspec check` | 检查已安装的工具和依赖 |
| `codexspec version` | 显示版本和系统信息 |
| `codexspec config` | 查看或修改项目配置 |
| `codexspec list-commands` | 按类别列出可用智能体命令 |
| `codexspec show-blueprint` | 显示共享工作区中的蓝图，不作修改 |

### 核心工作流命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:constitution` | 创建/更新项目原则，并进行跨产物验证 |
| `/codexspec:specify` | 讨论、确认并持久保存功能需求 |
| `/codexspec:blueprint` | 准备或维护已确认的待处理蓝图需求 |
| `/codexspec:generate-spec` | 根据已确认需求编写可追溯的规格文档，并自动审查 |
| `/codexspec:spec-to-design` | 定义架构、组件、接口和决策；自动审查 |
| `/codexspec:design-to-plan` | 规划实现阶段、顺序和验证；自动审查 |
| `/codexspec:plan-to-tasks` | 生成覆盖上游要求的可验证任务，并自动审查和分析 |
| `/codexspec:implement-tasks` | 执行任务、验证结果、审查并修复 |
| `/codexspec:auto-dev` | 按文档顺序自主开发已确认的蓝图需求 |

### 产物审查命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:review-spec` | 检查规格忠实度和内部质量 |
| `/codexspec:review-design` | 检查设计是否符合规格、是否可行，以及能否据此制定计划 |
| `/codexspec:review-plan` | 检查计划是否符合设计、是否可行，以及能否据此开始实现 |
| `/codexspec:review-tasks` | 检查任务忠实度、依赖、可执行性和验证 |

### 需求、既有代码与调试

| 命令 | 用途 |
|---------|---------|
| `/codexspec:clarify` | 解决需求歧义，先更新需求，再更新规格 |
| `/codexspec:analyze` | 检查整个开发链路是否可追溯，并让下游文档符合上游依据 |
| `/codexspec:checklist` | 生成需求质量检查清单 |
| `/codexspec:tasks-to-issues` | 将已有任务转为可操作的 GitHub issues |
| `/codexspec:debug` | 调查根因后再修复 |
| `/codexspec:reverse-spec` | 概览现有架构、生成模块草案，或报告相对于基线的偏差 |

### 项目知识命令

| 命令 | 用途 |
|---------|---------|
| `/codexspec:distill` | 提炼可复用知识，或在本地界面中审阅候选记录 |
| `/codexspec:evolve` | 将已认可的知识整理为向上游贡献的草案 |
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

配置保存在 `.codexspec/config.yml` 中。模板始终使用英文，智能体交流和生成文档时，则使用配置中指定的语言。支持的 13 个标准语言代码为 `en`、`zh-CN`、`zh-TW`、`ja`、`ko`、`es`、`fr`、`de`、`pt`、`ru`、`it`、`ar` 和 `hi`。葡萄牙语在 CLI 中使用 `pt`，在本地化文档和翻译目录中使用 `pt-BR`。

### 语言维度

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

### 工作流与审查设置

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

各项设置和语言选项的详细说明，见[配置](docs/en/reference/configuration.md)和[国际化](docs/en/user-guide/i18n.md)。

## 项目结构

初始化会安装共用资源，以及所选助手需要的集成文件：

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

共享蓝图保存在专用的 auto-dev worktree 中，各常规 checkout 不会分别保存可编辑副本。手动审阅项目知识时生成的草稿不纳入 Git。

## 扩展开发资料

仓库提供扩展清单模板、示例命令和[扩展开发指南](extensions/EXTENSION-DEVELOPMENT-GUIDE.md)，供编写扩展时参考。当前 CLI 尚未提供安装、列出或移除扩展的命令，也不会自动加载 `extension.yml` 中定义的命令和钩子。需要项目专用的审查规则时，可以在 `.codexspec/review-code/` 中添加内容；初始化会保留已修改的资源和附加文件，除非明确要求替换。

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

修改模板、打包或初始化行为前，请先阅读 [CLAUDE.md](CLAUDE.md)、[AGENTS.md](AGENTS.md) 和[仓库布局](docs/internal/repository-layout.md)。分发的命令和技能副本由源文件生成，属于安装产物；修改时应编辑对应的源文件，再重新生成副本。

## 贡献

本地开发环境的准备方法和贡献流程，见[贡献指南](docs/en/development/contributing.md)。贡献时应遵守已确认的需求，保留可追溯的来源依据，并维持面向用户的资源与维护者内部资源之间的打包边界。

## 许可证

MIT — 见 [LICENSE](LICENSE)。

## 致谢

灵感来自 [GitHub spec-kit](https://github.com/github/spec-kit)。
支持与 Claude Code 和 OpenAI Codex 集成。
