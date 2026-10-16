# 工作流

<a id="core-workflow"></a>

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

<a id="specify-clarify-and-analyze"></a>

### specify、clarify 与 analyze

- **specify** 用于开始需求讨论，也可重新讨论已有需求。需求摘要只有经用户明确确认后，才成为后续工作的依据。
- **clarify** 用于澄清已有需求和规格中的歧义。每次最多提出五个问题，检查范围涵盖四类问题；先更新 `requirements.md`，再同步修改 `spec.md`。
- **analyze** 检查需求 → 规格 → 设计 → 计划 → 任务的完整链路。如果根据上游依据能够确定下游文档应如何修正，就会自动修正；它绝不修改 `requirements.md`，无法解决的问题会明确报告。任务审查通过后会自动运行，结果供后续参考，不作为阻止实现的门禁。

```text
/codexspec:clarify <feature-dir>
/codexspec:analyze <feature-dir>
```

<a id="small-changes-with-quick"></a>

### 使用 Quick 处理小型变更

对于局部修复等范围小、边界明确的变更，可以使用 `quick`：

```text
/codexspec:quick Fix the empty-state message on the task list
```

Quick 会先确认并保存一份精简的需求摘要，再依次调用生成命令及相应审查，推进规格、计划、任务和实现。如果变更涉及较大范围，或仍有产品和设计选择尚未确定，应使用标准工作流。需要用户作出新决定时，Quick 会暂停。

<a id="workflow-automation"></a>

### 工作流自动化

`workflow.auto_next` 默认为 **false**。如果当前工作区将其设置为 `true`，确认最终需求后就会自动进入规格阶段。各生成阶段得到 `PASS` 或 `PASS_WITH_WARNINGS` 时会继续推进，得到 `NEEDS_REVISION` 或 `BLOCKED` 时则停止。`implement-tasks` 是最后一个阶段。

自动修正文档时，只处理已经验证的缺陷，且修正方式必须有上游依据支持；最多进行两轮修复和重新审查。建议另行列出。实现阶段的审查与修复遵循另一套完成标准，详见下文。

<a id="shared-blueprint-and-autonomous-development"></a>

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

<a id="worktree-development"></a>

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

见 [Worktree 开发](workflow.md#worktree-development)和[配置说明](../reference/configuration.md#workflow-and-review-settings)。

<a id="work-with-existing-code"></a>

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

<a id="review-and-debugging"></a>

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

如何选择审查范围、传入参数以及执行详细流程，见[命令参考](commands.md)。

<a id="project-knowledge"></a>

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

详细指引见[项目知识](commands.md#codexspecdistill)。

<a id="reusing-historical-decisions"></a>

### 复用历史决策

在就某项变更向你提问前，智能体会先查阅 `.codexspec/specs/` 下相关功能的迭代历史：读取 `requirements.md` 中已确认的决策，追踪后续补充和明确替换的内容，必要时再查阅设计理由或实现依据。在作出设计、实现、调试或审查方面的实质性判断前，也需要做好这项准备；普通对话和 SDD 工作流都适用。

功能目录的时间戳用于梳理迭代顺序，文档较新并不意味着旧决策自动失效。较早确认且未被修改的需求继续有效，尚在讨论的提案也不能当作已确认的意图。检索只围绕当前任务展开，背景足以支持判断时就停止，后续阶段继续复用已准备好的背景。

例如，修改接口时，如果没有回顾历史，智能体可能会问：

> “这个功能应该怎样处理兼容性？”

查阅相关决策并核对当前实现后，就能把问题缩小为：

> “之前确认保留旧接口，当前实现也仍在兼容。本次建议沿用，是否保持？”

已经明确且仍然适用的信息，可以直接复用，无需反复询问。如果你已经明确说“本次移除旧接口”，智能体就应按这个决定推进，并说明迁移影响。**你最新的明确决定始终优先**；历史用于让问询更准确、减少重复提问。

刷新已有项目的安装即可加入这项指引。

<a id="git-workflow"></a>

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

## 追溯与继续开发

已确认的 `requirements.md` 决定功能意图；下游依次是 `spec.md` → `design.md` → `plan.md` → `tasks.md`，同时需要结合适用的项目原则和经过核实的仓库事实。需求采用稳定 ID，规格条目通过 `Sources` 引用来源，下游工作通过 `Covers` 记录覆盖关系。下游工件不能擅自改写上游决策。权威来源冲突或需要新的产品决策时，必须由用户裁定。历史功能缺少需求记录时，应说明无法验证最初的确认；缺少历史设计工件时，采用已说明的兼容路径。

功能选择不明确时，应传入明确的功能路径；命令不会擅自选择最新目录。worktree 父目录根据主仓库确定，即使从子目录或其他关联 worktree 调用也一样。裸仓库使用同级的 `<bare-repository-name>-codexspec-worktrees` 目录。独立维护工作使用 `codexspec/maintenance` 分支。

worktree 准备失败后会保留其标识，方便继续处理。基线分叉产生的合并必须通过项目检查，之后才能写入功能需求或开始开发。只读检查保留原始输入位置，报告写入解析后的输出检出目录。暂存提交操作始终使用所选索引，不会将 main 的暂存修改转移到其他 worktree。新 worktree 缺少必需的安装资源时，应先在目标目录初始化，再继续工作。

## 评审模型

评审把输出区分为三类：

- **忠实性缺陷**：与权威来源冲突，或遗漏必须覆盖的内容。
- **内在缺陷**：工件内部自相矛盾、不可验证或不可实施。
- **风险建议 / 设计机会**：没有当前缺陷证据的可选改进。

每个缺陷都必须给出证据、位置、偏差、影响和最小修复方式。根因相同的发现会被合并。建议项不影响状态、分数，也不触发自动修复。

评审状态：

- `PASS`：没有严重、警告或轻微缺陷。
- `PASS_WITH_WARNINGS`：仅剩轻微缺陷。
- `NEEDS_REVISION`：仍存在警告。
- `BLOCKED`：严重冲突阻止可靠地继续。

兼容性分数由同一组已分类的发现推导而来，不再按固定模板章节扣分。状态是权威结论；分数只是为仍需要数字的集成而保留。

## 有界自动评审

生成命令会自动运行对应的评审。这正是**基于证据的评审**纪律的体现：它们只能修复有证据支持的缺陷，且最多自动修复并重审两轮。出现 `PASS` 时会提前停止；遇到以下情况时会停下来等待用户介入：

- 某个权威来源与其他来源冲突；
- 修复会改动已确认的意图；
- 剩余项目属于建议而非缺陷；
- 两轮修复已用完。

随时可以手动运行 `/codexspec:review-*` 命令获取一份新的报告。
