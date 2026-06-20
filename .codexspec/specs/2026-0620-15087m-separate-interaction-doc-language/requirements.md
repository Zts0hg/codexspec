# Confirmed Requirements: separate-interaction-doc-language

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0620-15087m`
**Status**: Discovery
**Last Confirmed**: 2026-06-20

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: 拆分"交互语言"与"文档语言"为独立控制

- **Status**: confirmed
- **Statement**: 将当前 `language.output`(同时控制"与 LLM 交互的语言"和"生成文档的语言")拆分为两个独立可控的语言——**交互语言**(LLM 与用户对话、提问、状态说明,以及 `codexspec` CLI 终端输出所用的语言)与**文档语言**(生成的 requirements/spec/plan/tasks 等工件文件所用的语言)。典型场景:面向全球开发者的项目文档用英文,而母语非英语的开发者用自己的母语与 LLM 沟通效率更高。
- **Rationale**: 单一 `output` 字段无法表达"文档语言 ≠ 交互语言"的常见需求;拆分后可同时满足"全球可读的英文文档"与"高效的母语交互"。
- **User Evidence**: "希望能够将交互语言和文档语言也能够进行分别控制……文档语言最好是英文,但是在跟 LLM 交互的时候母语非英语的开发者使用自己的母语交互效率会更高"
- **Confirmed At**: 2026-06-20

## Constraints

### CON-001: 向后兼容——仅有 output 的现存配置行为不变

- **Status**: confirmed
- **Statement**: 现存只配置了 `language.output` 的项目必须继续正常工作,无需强制迁移。当 `interaction`/`document` 均未设置而 `output` 存在时,两者都解析为 `output` 的值,行为与当前完全一致。
- **User Evidence**: 用户确认 DEC-001/DEC-002 的兼容回退设计,采纳"新增 interaction+document、output 兼容"方案。

### CON-002: 翻译标准同时应用于"对话"与"工件"两侧

- **Status**: confirmed
- **Statement**: 各斜杠命令模板的 `## Language Preference` 段须指示 LLM:**对话内容**用 `interaction` 语言、按既定翻译标准(按意思译、无合适母语词时保留英文、地道表达)自然表述;**生成工件**用 `document` 语言、按同一标准撰写。工件应是"以文档语言原生撰写",而非"先以一种语言写好再事后翻译"。
- **User Evidence**: "需要利用好我们之前讨论过的良好的语言翻译标准来确保生成的文档内容准确完整的同时,用户与 LLM 交互时的对话内容也可以准确完整且符合对应语言的描述风格"

## Decisions

### DEC-001: 配置结构——新增 interaction + document,output 降为兼容字段

- **Status**: confirmed
- **Decision**: 在 `language:` 下新增 `interaction`(交互语言)与 `document`(文档语言)两个子字段;保留 `output` 作为向后兼容字段。
- **Alternatives Rejected**: (a) 将 `output` 语义改为仅"文档语言"并新增 `interaction`——拒绝,因 `output` 含义发生隐式微变;(b) 彻底移除 `output`、强制 `interaction`+`document`——拒绝,因破坏所有现存配置。
- **Reason**: 新增字段 + output 兼容回退,改动最小、对现有用户零破坏。
- **User Evidence**: 用户选择"新增 interaction+document,output 兼容"。
- **Confirmed At**: 2026-06-20

### DEC-002: 字段回退优先级——各自独立 → output → en

- **Status**: confirmed
- **Decision**: `interaction` 与 `document` 各自独立解析:显式值 → `output`(legacy)→ `en`。
- **Alternatives Rejected**: (a) `interaction` 缺省时回退到 `document`(耦合)——拒绝,因与 output-only 老配置行为有差异;(b) 各自直接回退 `en`(不读 output)——拒绝,因老配置行为会从 output 语言掉回 en。
- **Reason**: 各自 → output → en 最可预测,且 output-only 老配置行为完全不变。
- **User Evidence**: 用户选择"各自 → output → en"。
- **Confirmed At**: 2026-06-20

### DEC-003: 交互语言的覆盖范围——LLM 对话 + CLI 终端输出

- **Status**: confirmed
- **Decision**: `interaction` 管所有面向用户的会话/终端文本:`/codexspec:*` 斜杠命令中 LLM 的提问/说明/状态,以及 `codexspec` CLI(init 提示、list-commands、version、config)的终端输出。`document` 管生成的工件文件(requirements/spec/plan/tasks)。
- **Alternatives Rejected**: `interaction` 仅限 LLM 斜杠命令对话、CLI 终端输出单独处理——拒绝,因不符合"任何被对话的地方都用母语"的统一心智。
- **Reason**: 统一"面向用户的会话/提示 = 交互语言""生成的文件 = 文档语言"最清晰、最贴合用户场景。
- **User Evidence**: 用户选择"LLM 对话 + CLI 终端输出"。
- **Confirmed At**: 2026-06-20

### DEC-004: init 行为与 commit 字段

- **Status**: confirmed
- **Decision**: `codexspec init --lang X` 同时设置 `interaction` 与 `document`(并写入 legacy `output`);用户之后可用 `/codexspec:config` 拆分。`commit` 字段行为不变(解析:显式值 → output → en)。
- **Reason**: 新项目默认"单一语言、简单上手";需要拆分时再配置。`commit` 已是成熟独立字段,不改其回退以免意外。
- **User Evidence**: 用户确认采纳此提议("你提议的 3 条也很合理 都采纳")。
- **Confirmed At**: 2026-06-20

### DEC-005: output 字段的弃用策略——暂时静默回退

- **Status**: confirmed
- **Decision**: 本版本中,当配置仍使用 `output` 时静默回退(不发出 deprecation 提示);在未来版本中再考虑加入弃用警告。
- **Reason**: 避免一次性给所有现有用户引入噪音;先稳定新字段,再逐步引导迁移。
- **User Evidence**: 用户确认"OPEN-001 也按照你说的暂时静默回退,未来版本再警告"。
- **Confirmed At**: 2026-06-20

## Out of Scope

### OUT-001: 不改变 CodexSpec 自身 mkdocs 站点(docs/)的翻译

- **Status**: confirmed
- **Statement**: 本功能不涉及 CodexSpec 自己文档站(`docs/`,由 `/codexspec:translate-docs` 维护的多语言站点)的翻译流程。
- **Reason**: 那是独立的翻译范畴,与本配置拆分无关。
- **User Evidence**: 阶段小结中列为 OUT,用户确认。

### OUT-002: 不回溯重译已有的 spec 工件

- **Status**: confirmed
- **Statement**: 不对 `.codexspec/specs/` 下已存在的 requirements/spec/plan/tasks 工件进行回溯性语言重译。
- **Reason**: 历史工件保持原样;新语言控制只影响此后新生成的内容。
- **User Evidence**: 阶段小结中列为 OUT,用户确认。

## Open Questions

_无阻塞性开放问题。_ (原 OPEN-001「output 是否给 deprecation 提示」已由 DEC-005 解决:暂时静默回退。)

## Confirmation Log

### Session 2026-06-20

- **Summary Presented**: 阶段小结,含 NEED-001(目标)、DEC-001(配置结构)、DEC-002(回退)、DEC-003(交互覆盖范围),以及 3 条 AI 提议(DEC-004 init+commit、CON-001 兼容、CON-002 双侧翻译标准)、2 条 OUT(OUT-001 docs 站点、OUT-002 回溯重译)、1 条 OPEN(OPEN-001)。
- **User Confirmation**: "确认,你提议的 3 条也很合理 都采纳。OPEN-001 也按照你说的暂时静默回退,未来版本再警告。"
- **Entries Confirmed**: NEED-001, CON-001, CON-002, DEC-001, DEC-002, DEC-003, DEC-004, DEC-005, OUT-001, OUT-002
