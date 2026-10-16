# CodexSpec

![CodexSpec](assets/images/codexspec-logo-light.svg#only-light){ width="420" }

![CodexSpec](assets/images/codexspec-logo-dark.svg#only-dark){ width="420" }

**面向 Claude Code 和 OpenAI Codex 的需求优先 SDD 工具包**

CodexSpec 将已确认的需求逐步转化为可追溯的规格说明、设计、计划、任务和具体实现。你来决定做什么、为什么做；智能体则在这些需求的约束下制定实现方案，通过阶段审查把关，并结合长期保存的项目知识推进开发。

你可以通过 Claude Code 的斜杠命令或 Codex 技能使用 CodexSpec，也可以将两种方式配合使用。常规功能开发默认在各自独立的 Git worktree 中进行。如果需要，还可以使用共享蓝图，让智能体按顺序自主推进已确认需求的开发。

<a id="why-choose-codexspec"></a>

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

<a id="what-is-requirements-first-sdd"></a>

### 什么是需求优先 SDD？

需求优先的规格驱动开发（Requirements-First Spec-Driven Development）以**已确认的需求作为功能开发的最高依据**。智能体先记录目标、约束、决策、不做的事项、待解决的问题以及用户确认的依据，再据此编写后续文档并实现功能。

```text
Idea → Confirmed Requirements →     Spec    →     Design    →     Plan    →    Tasks     →     Code
                 ↓                   ↓              ↓              ↓             ↓              ↓
         User confirmation      review-spec   review-design   review-plan   review-tasks   review-code
```

需求由你确认；从规格到代码，后续各项产物都有对应的审查环节。

产品要做什么、为什么做，由人与智能体协作讨论和调整；自动审查负责检查后续产物是否符合这些决定。启用自动化后，通过审查的阶段会继续向下推进，但智能体仍不能擅自改写已确认的需求。

[![CodexSpec：需求优先开发流程、阶段审查与经验迭代循环](../../assets/workflow/workflow-zh-CN-light.png#only-light)](../../assets/workflow/workflow-zh-CN-light.png#only-light)

[![CodexSpec：需求优先开发流程、阶段审查与经验迭代循环](../../assets/workflow/workflow-zh-CN-dark.png#only-dark)](../../assets/workflow/workflow-zh-CN-dark.png#only-dark)

打开完整尺寸的流程图： [☀️](../../assets/workflow/workflow-zh-CN-light.png) · [🌙](../../assets/workflow/workflow-zh-CN-dark.png)

<a id="30-second-quick-start"></a>

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

如需定制项目原则，可以使用 `constitution`。确认最终需求摘要后，在命令返回的功能目录和工作区中继续开发。后续步骤见[核心工作流](user-guide/workflow.md#core-workflow)。

使用 Codex 桌面应用？可以[让 Codex 安装并初始化你的项目](getting-started/installation.md#install-with-the-codex-desktop-app)。
