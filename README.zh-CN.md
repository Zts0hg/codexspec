# CodexSpec

[English](README.md) | **中文** | [日本語](README.ja.md) | [Español](README.es.md) | [Português](README.pt-BR.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md)

[![PyPI version](https://img.shields.io/pypi/v/codexspec.svg)](https://pypi.org/project/codexspec/)
[![Python](https://img.shields.io/pypi/pyversions/codexspec.svg)](https://pypi.org/project/codexspec/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**面向 Claude Code 的规格驱动开发 (SDD) 工具包**

CodexSpec 是一个帮助您使用结构化、规格驱动方法构建高质量软件的工具包。它颠覆了传统开发模式，将规格说明转化为直接指导实现的可执行产物。

## 设计理念：人机协同

CodexSpec 基于**有效的 AI 辅助开发需要在每个阶段都有人类积极参与**这一信念构建。该工具包围绕一个核心原则设计：

> **在推进之前，审查并验证每个产物。**

### 为什么人工监督很重要

在 AI 辅助开发中，跳过审查阶段会导致：

| 问题 | 后果 |
|------|------|
| 需求不清晰 | AI 做出的假设偏离您的意图 |
| 规格不完整 | 构建的功能缺少关键的边界情况处理 |
| 技术计划与需求脱节 | 架构与业务需求不匹配 |
| 任务分解模糊 | 实现偏离轨道，需要昂贵的返工 |

### CodexSpec 的方法

CodexSpec 将开发过程结构化为**可审查的检查点**：

```
想法 → 澄清 → 审查 → 计划 → 审查 → 任务 → 审查 → 分析 → 实现
              ↑              ↑              ↑
           人工检查        人工检查        人工检查
```

**每个产物都有对应的审查命令：**
- `spec.md` → `/codexspec.review-spec`
- `plan.md` → `/codexspec.review-plan`
- `tasks.md` → `/codexspec.review-tasks`
- 所有产物 → `/codexspec.analyze`

这种系统的审查流程确保：
- **早期错误检测**：在编写代码之前发现误解
- **一致性验证**：确认 AI 的理解与您的意图一致
- **质量关卡**：在每个阶段验证完整性、清晰性和可行性
- **减少返工**：花几分钟审查，节省数小时的重新实现

## 特性

### 核心 SDD 工作流
- **宪法驱动**：建立项目原则，指导所有后续决策
- **两阶段规格说明**：交互式澄清（`/specify`）后生成文档（`/generate-spec`）
- **计划驱动开发**：在需求验证后进行技术选型
- **TDD 就绪任务**：任务分解强制执行测试优先方法

### 人机协同
- **审查命令**：针对规格、计划和任务的专用审查命令，验证 AI 输出
- **交互式澄清**：基于问答的需求细化，提供即时反馈
- **跨产物分析**：在实现之前检测规格、计划和任务之间的不一致性
- **质量检查清单**：自动化的需求质量评估

### 开发者体验
- **Claude Code 集成**：Claude Code 原生斜杠命令支持
- **国际化 (i18n)**：通过 LLM 动态翻译支持多语言
- **跨平台**：同时支持 Bash 和 PowerShell 脚本
- **可扩展**：支持自定义命令的插件架构

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
# 创建新项目
codexspec init my-project

# 在现有项目中初始化
codexspec init . --ai claude
# 或
codexspec init --here --ai claude

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

[安装](#安装)后，创建或初始化您的项目：

```bash
codexspec init my-awesome-project
# 或在当前目录
codexspec init . --ai claude
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

### 3. 澄清需求

使用 `/codexspec.specify` 通过交互式问答**探索和澄清**您的需求：

```
/codexspec.specify 我想构建一个任务管理应用
```

此命令将：
- 提出澄清性问题以理解您的想法
- 探索您可能未考虑到的边界情况
- 通过对话共创高质量需求
- **不会**自动生成文件 - 您保持控制

### 4. 生成规格文档

需求澄清后，使用 `/codexspec.generate-spec` 创建 `spec.md` 文档：

```
/codexspec.generate-spec
```

此命令充当"需求编译器"，将您澄清的需求转换为结构化的规格文档。

### 5. 审查规格（推荐）

**在进入计划阶段之前，验证您的规格：**

```
/codexspec.review-spec
```

此命令生成详细的审查报告，包括：
- 章节完整性分析
- 清晰度和可测试性评估
- 宪法一致性检查
- 优先级建议

### 6. 创建技术计划

使用 `/codexspec.spec-to-plan` 定义如何实现：

```
/codexspec.spec-to-plan 使用 Python 和 FastAPI 作为后端，PostgreSQL 作为数据库，React 作为前端
```

该命令包含**合宪性审查** - 验证您的计划符合项目原则。

### 7. 审查计划（推荐）

**在分解任务之前，验证您的技术计划：**

```
/codexspec.review-plan
```

此命令验证：
- 规格一致性
- 架构合理性
- 技术栈适配性
- 宪法合规性

### 8. 生成任务

使用 `/codexspec.plan-to-tasks` 分解计划：

```
/codexspec.plan-to-tasks
```

任务按标准阶段组织，具有：
- **TDD 强制执行**：测试任务先于实现任务
- **并行标记 `[P]`**：识别独立任务
- **文件路径规范**：每个任务有明确的交付物

### 9. 审查任务（推荐）

**在实现之前，验证任务分解：**

```
/codexspec.review-tasks
```

此命令检查：
- 计划覆盖度
- TDD 合规性
- 依赖关系正确性
- 任务粒度

### 10. 分析（可选但推荐）

使用 `/codexspec.analyze` 进行跨产物一致性检查：

```
/codexspec.analyze
```

此命令检测规格、计划和任务中的问题：
- 覆盖缺口（没有任务的需求）
- 重复和不一致性
- 宪法违规
- 规格不充分的项目

### 11. 实现

使用 `/codexspec.implement-tasks` 执行实现：

```
/codexspec.implement-tasks
```

实现遵循**条件 TDD 工作流**：
- 代码任务：测试优先（红 → 绿 → 验证 → 重构）
- 不可测试任务（文档、配置）：直接实现

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

#### 核心工作流命令

| 命令 | 描述 |
|------|------|
| `/codexspec.constitution` | 创建或更新项目宪法，支持跨产物验证和同步影响报告 |
| `/codexspec.specify` | 通过交互式问答**澄清**需求（不生成文件） |
| `/codexspec.generate-spec` | 需求澄清后**生成** `spec.md` 文档 |
| `/codexspec.spec-to-plan` | 将规格转换为技术计划，包含合宪性审查和模块依赖图 |
| `/codexspec.plan-to-tasks` | 将计划分解为原子级、TDD 强制的任务，带并行标记 `[P]` |
| `/codexspec.implement-tasks` | 执行任务，采用条件 TDD 工作流（代码用 TDD，文档/配置直接实现） |

#### 审查命令（质量关卡）

| 命令 | 描述 |
|------|------|
| `/codexspec.review-spec` | 验证规格的完整性、清晰度、一致性和可测试性，提供评分 |
| `/codexspec.review-plan` | 审查技术计划的可行性、架构质量和宪法一致性 |
| `/codexspec.review-tasks` | 验证任务分解的计划覆盖度、TDD 合规性、依赖关系和粒度 |

#### 增强命令

| 命令 | 描述 |
|------|------|
| `/codexspec.clarify` | 使用 4 个聚焦类别扫描现有 spec.md 中的模糊区域，与审查发现集成 |
| `/codexspec.analyze` | 非破坏性的跨产物分析（规格、计划、任务），基于严重性检测问题 |
| `/codexspec.checklist` | 为需求验证生成质量检查清单 |
| `/codexspec.tasks-to-issues` | 将任务转换为 GitHub issues，用于项目管理集成 |

## 工作流概览

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    CodexSpec 人机协同工作流                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Constitution  ──►  定义项目原则                                       │
│         │                         包含跨产物验证                           │
│         ▼                                                                │
│  2. Specify  ───────►  交互式问答澄清需求                                  │
│         │               （不创建文件 - 人工控制）                           │
│         ▼                                                                │
│  3. Generate Spec  ─►  创建 spec.md 文档                                  │
│         │                                                                │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ 审查关卡 1: /codexspec.review-spec ★                            ║   │
│  ║  验证：完整性、清晰度、可测试性、宪法一致性                              ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  4. Clarify  ───────►  解决歧义（迭代）                                    │
│         │               4 个聚焦类别，最多 5 个问题                        │
│         ▼                                                                │
│  5. Spec to Plan  ──►  创建技术计划，包含：                                │
│         │               • 合宪性审查（强制）                               │
│         │               • 模块依赖图                                       │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ 审查关卡 2: /codexspec.review-plan ★                            ║   │
│  ║  验证：规格一致性、架构、技术栈、阶段                                 ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  6. Plan to Tasks  ─►  生成原子级任务，包含：                              │
│         │               • TDD 强制执行（测试先于实现）                      │
│         │               • 并行标记 [P]                                    │
│         │               • 文件路径规范                                    │
│         ▼                                                                │
│  ╔═══════════════════════════════════════════════════════════════════╗   │
│  ║  ★ 审查关卡 3: /codexspec.review-tasks ★                           ║   │
│  ║  验证：覆盖度、TDD 合规性、依赖关系、粒度                             ║   │
│  ╚═══════════════════════════════════════════════════════════════════╝   │
│         │                                                                │
│         ▼                                                                │
│  7. Analyze  ───────►  跨产物一致性检查                                    │
│         │               检测缺口、重复、宪法问题                           │
│         ▼                                                                │
│  8. Implement  ─────►  使用条件 TDD 工作流执行                             │
│                          代码：测试优先 | 文档/配置：直接实现              │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**关键洞察**：每个审查关卡（★）都是一个人工检查点，您在投入更多时间之前验证 AI 输出。跳过这些关卡通常会导致昂贵的返工。

### 核心概念：需求澄清工作流

CodexSpec 为工作流的不同阶段提供了**两个不同的澄清命令**：

#### specify 与 clarify：何时使用哪个？

| 方面 | `/codexspec.specify` | `/codexspec.clarify` |
|------|----------------------|----------------------|
| **目的** | 初始需求探索 | 现有规格的迭代细化 |
| **何时使用** | 从新想法开始，没有 spec.md | spec.md 已存在，需要填补空白 |
| **输入** | 您的初步想法或需求 | 现有的 spec.md 文件 |
| **输出** | 无（仅对话） | 更新 spec.md 并添加澄清内容 |
| **方法** | 开放式问答 | 结构化模糊扫描（4 个类别） |
| **问题限制** | 无限制 | 最多 5 个问题 |
| **典型用途** | "我想构建一个待办应用" | "规格缺少错误处理细节" |

#### 两阶段规格说明

在生成任何文档之前：

| 阶段 | 命令 | 目的 | 输出 |
|------|------|------|------|
| **探索** | `/codexspec.specify` | 交互式问答探索和细化需求 | 无（仅对话） |
| **生成** | `/codexspec.generate-spec` | 将澄清的需求编译成结构化文档 | `spec.md` |

#### 迭代澄清

spec.md 创建之后：

```
spec.md ──► /codexspec.clarify ──► 更新的 spec.md（包含 Clarifications 章节）
                │
                └── 扫描 4 个聚焦类别的模糊区域：
                    • 完整性缺口 - 缺失章节、空白内容
                    • 具体性问题 - 模糊术语、未定义约束
                    • 行为清晰度 - 错误处理、状态转换
                    • 可衡量性问题 - 没有指标的非功能需求
```

#### 此设计的优势

- **人机协同**：您积极参与需求发现
- **明确控制**：只有您决定时才创建文件
- **质量聚焦**：在文档化之前充分探索需求
- **迭代细化**：随着理解加深，规格可以逐步改进

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
| 核心理念 | 规格驱动开发 | 规格驱动开发 + 人机协同 |
| CLI 名称 | `specify` | `codexspec` |
| 主要 AI | 多代理支持 | 专注于 Claude Code |
| 命令前缀 | `/speckit.*` | `/codexspec.*` |
| 宪法系统 | 基础 | 完整宪法，支持跨产物验证 |
| 两阶段规格 | 否 | 是（澄清 + 生成） |
| 审查命令 | 可选 | 3 个专用审查命令，带评分 |
| Clarify 命令 | 是 | 4 个聚焦类别，与审查集成 |
| Analyze 命令 | 是 | 只读、基于严重性、感知宪法 |
| 任务中的 TDD | 可选 | 强制执行（测试先于实现） |
| 实现 | 标准 | 条件 TDD（代码 vs 文档/配置） |
| 扩展系统 | 是 | 是 |
| PowerShell 脚本 | 是 | 是 |
| i18n 支持 | 否 | 是（通过 LLM 翻译支持 13+ 语言） |

### 关键差异

1. **审查优先文化**：每个主要产物都有专用审查命令
2. **宪法治理**：原则经过验证，而不仅仅是记录
3. **默认 TDD**：任务生成中强制执行测试优先方法
4. **人工检查点**：工作流围绕验证关卡设计

## 理念

CodexSpec 遵循以下核心原则：

### SDD 基础原则

1. **意图驱动开发**：规格在"怎么做"之前定义"做什么"
2. **丰富的规格创建**：使用护栏和组织原则
3. **多步骤细化**：而非一次性代码生成
4. **宪法治理**：项目原则指导所有决策

### 人机协同原则

5. **人在环中**：AI 生成产物，人类验证
6. **审查导向**：在推进前验证每个产物
7. **渐进式披露**：复杂信息逐步揭示
8. **显式优于隐式**：需求应该清晰，而非假设

### 质量保证原则

9. **默认测试驱动**：TDD 工作流内置于任务生成
10. **跨产物一致性**：同时分析规格、计划和任务
11. **宪法一致性**：所有产物尊重项目原则

### 审阅的重要性对比

| 没有审查 | 有审查 |
|---------|--------|
| AI 做出错误的假设 | 人工早期发现误解 |
| 不完整的需求传播到后续阶段 | 在实现前识别缺口 |
| 架构偏离意图 | 在每个阶段验证一致性 |
| 任务遗漏关键功能 | 系统性验证覆盖度 |
| **结果：返工、浪费精力** | **结果：一次做对** |

## 贡献

欢迎贡献！请在提交 pull request 前阅读我们的贡献指南。

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

## 致谢

- 灵感来源于 [GitHub spec-kit](https://github.com/github/spec-kit)
- 为 [Claude Code](https://claude.ai/code) 构建
