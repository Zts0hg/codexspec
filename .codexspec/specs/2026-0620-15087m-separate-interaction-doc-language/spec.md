# Feature Specification: separate-interaction-doc-language

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Feature Branch**: `2026-0620-15087m-separate-interaction-doc-language`
**Created**: 2026-06-20
**Status**: Draft
**Input**: 将 `language.output`(同时控制"与 LLM 交互的语言"和"生成文档的语言")拆分为可独立控制的"交互语言"与"文档语言",并把既定翻译标准同时应用于对话与工件两侧。

## 概述与目标

当前 `.codexspec/config.yml` 的 `language.output` 单一字段同时决定两件事:(1) LLM 与用户对话、以及 `codexspec` CLI 终端输出所用的语言;(2) 生成的 requirements/spec/plan/tasks 等工件文件所用的语言。这无法表达"面向全球开发者的项目文档用英文、而母语非英语的开发者用母语与 LLM 沟通"这类常见需求。

本功能在不破坏向后兼容的前提下,将二者拆分为独立的 `language.interaction`(交互语言)与 `language.document`(文档语言)控制,并要求所有命令模板按既定翻译标准(按意思译、无合适母语词时保留英文、地道表达)在两侧分别执行。

## User Scenarios & Testing

### User Story 1 - 母语交互 + 英文文档(Priority: P1)

一位母语非英语的开发者维护一个面向全球开源用户的项目。他希望项目产出的 spec/plan/tasks 等工件为英文(全球可读、便于协作),但与 LLM 对话时用自己的母语效率更高。

**为何此优先级**:这是本功能的核心价值命题;没有它,该需求无法满足。

**独立测试**:仅配置 `interaction: zh-CN`、`document: en`,运行任一 `/codexspec:*` 命令,即可验证"对话为中文、工件为英文"。

**验收场景**:

1. **Given** 配置 `interaction: zh-CN`、`document: en`,**When** 运行 `/codexspec:generate-spec`,**Then** LLM 的提问/说明为中文,生成的 `spec.md` 为英文。
2. **Given** 同上配置,**When** 运行 `codexspec init`/`list-commands` 等 CLI,**Then** 终端提示/输出为中文(interaction)。
3. **Given** 同上配置,**When** 生成工件中出现技术术语,**Then** 文档(英文)中按英文惯例表达,对话(中文)中按中文习惯表达(如 "AI coding agent" → 工件 "AI coding agent"、对话 "AI 编程助手")。

---

### User Story 2 - 现有用户零改动升级(Priority: P1)

一个现存项目只有 `language.output: zh-CN`。升级到新版本后,无需修改配置,所有行为与升级前完全一致。

**为何此优先级**:向后兼容是采用前提;破坏它会导致现有用户在升级时遭遇回归。

**独立测试**:在一个仅含 `output` 的项目上升级后跑完整工作流,行为应与旧版逐字一致。

**验收场景**:

1. **Given** 配置仅有 `output: zh-CN`(无 interaction/document),**When** 升级到新版本,**Then** 交互与文档语言均解析为 `zh-CN`,行为不变,且无 deprecation 警告。
2. **Given** 配置 `output: zh-CN`、`commit: en`,**When** 升级,**Then** commit 语言仍为 `en`(显式优先),行为不变。

---

### User Story 3 - 新项目单语言起步,按需拆分(Priority: P2)

新项目用 `codexspec init --lang X` 初始化,默认交互与文档同为 X(简单上手);之后若需要拆分,用 `/codexspec:config` 分别调整。

**独立测试**:`codexspec init --lang en` 后检查生成的 config.yml 含 `interaction: en`、`document: en`(及 legacy `output: en`)。

**验收场景**:

1. **Given** 运行 `codexspec init --lang en`,**When** 初始化完成,**Then** 生成的 `.codexspec/config.yml` 同时写入 `interaction: en`、`document: en`、`output: en`。
2. **Given** 已初始化项目,**When** 用 `/codexspec:config` 把 `document` 改为 `en` 而保留 `interaction: zh-CN`,**Then** 后续工件为英文、对话为中文。

---

### Edge Cases

- 只设 `interaction` 不设 `document`(或反之):未设字段按 `output → en` 回退(REQ-002)。
- `output` 与 `interaction`/`document` 同时存在:新字段优先,`output` 被静默忽略(NFR-002)。
- `interaction`/`document` 设了无效语言码:经 i18n 校验失败并报错(REQ-007)。
- 三个语言字段(`interaction`/`document`/`commit`)均未显式设置但 `output` 存在:全部回退到 `output`(与旧行为一致)。

## Requirements

### Functional Requirements

- **REQ-001**: 系统 MUST 在 `language:` 下支持 `interaction` 与 `document` 两个新的子字段,分别表示交互语言与文档语言。
  - Sources: NEED-001, DEC-001
- **REQ-002**: 系统 MUST 按以下优先级解析 `interaction` 与 `document`:显式值 → `output`(legacy)→ `en`。两字段各自独立解析。
  - Sources: DEC-002, CON-001
- **REQ-003**: `interaction` MUST 决定所有面向用户的会话/终端文本语言——含 `/codexspec:*` 斜杠命令中 LLM 的对话,以及 `codexspec` CLI(init/list-commands/version/config)的终端输出;`document` MUST 决定生成的工件文件(requirements/spec/plan/tasks)语言。
  - Sources: DEC-003, NEED-001
- **REQ-004**: `codexspec init --lang X` MUST 同时写入 `interaction: X`、`document: X`,并写入 legacy `output: X`。
  - Sources: DEC-004
- **REQ-005**: `/codexspec:config` MUST 允许独立查看与修改 `interaction` 与 `document` 两个字段。
  - Sources: NEED-001, DEC-001
- **REQ-006**: 各斜杠命令模板的 `## Language Preference` 段 MUST 指示 LLM:对话内容用 `interaction` 语言、按既定翻译标准自然表述;生成工件用 `document` 语言、按同一标准原生撰写(而非事后翻译)。
  - Sources: CON-002, NEED-001
- **REQ-007**: 系统 MUST 对 `interaction` 与 `document` 的语言码进行 i18n 校验;无效值 MUST 报错并阻止使用。
  - Sources: NEED-001, DEC-001
- **REQ-008**: `commit` 字段的解析行为 MUST 保持不变(显式值 → `output` → `en`)。
  - Sources: DEC-004

### Non-Functional Requirements

- **NFR-001**(向后兼容): 仅有 `output` 的现存配置,其交互与文档语言的解析结果 MUST 与当前实现逐字一致,无需迁移。
  - Sources: CON-001, DEC-002
- **NFR-002**(弃用策略): 本版本中,当配置使用 `output` 时 MUST 静默回退,不得发出 deprecation 警告。
  - Sources: DEC-005

### Key Entities

- **language 配置**(`.codexspec/config.yml` 顶层 `language:` 映射):子字段 `interaction`(交互语言)、`document`(文档语言)、`commit`(提交信息语言,行为不变)、`templates`(模板语言,保持 `en`)、`output`(legacy 兼容字段)。

## Success Criteria

### Measurable Outcomes

- **SC-001**: 配置 `interaction: zh-CN`、`document: en` 的项目,运行 `/codexspec:*` 时 LLM 对话为中文、生成的 spec/plan/tasks 为英文。
- **SC-002**: 仅含 `output` 的现存项目升级后,交互与文档语言均等于 `output` 值,与旧版行为一致。
- **SC-003**: `codexspec init --lang X` 生成的配置默认 `interaction = document = X`。
- **SC-004**: `/codexspec:config` 可独立修改 `interaction` 与 `document`,且各自按 REQ-003 生效。

## Confirmed Constraints & Decisions

- **CON-001**(兼容): 仅有 `output` 的现存配置必须继续工作,无需强制迁移。
- **CON-002**(双侧翻译标准): 对话与工件两侧均应用既定翻译标准;工件为原生撰写而非事后翻译。
- **DEC-001**: 新增 `interaction` + `document`;保留 `output` 作兼容字段。
- **DEC-002**: 回退顺序各自 → `output` → `en`。
- **DEC-003**: `interaction` 覆盖 LLM 对话 + CLI 终端输出;`document` 覆盖工件文件。
- **DEC-004**: `init --lang` 同时设置两者;`commit` 行为不变。
- **DEC-005**: `output` 本版本静默回退,不发 deprecation 警告。

## Open Questions

无阻塞性开放问题。(原 OPEN-001 已由 DEC-005/NFR-002 解决。)

## Out of Scope

- **OUT-001**: 不改变 CodexSpec 自身 mkdocs 站点(`docs/`)的翻译流程(由 `/codexspec:translate-docs` 独立维护)。
- **OUT-002**: 不回溯重译 `.codexspec/specs/` 下已有的 requirements/spec/plan/tasks 工件。

## Assumptions

- **假设-1**: `.codexspec/config.yml` 的其它顶层结构(`project:`、`git:` 等)及其它 `language:` 子字段(`templates`)保持不变,本功能只新增/重新解释 `interaction`、`document`,并保留 `output`。(此为实现层面合理边界,不扩展产品范围。)

## Dependencies

- 现有语言校验机制(`src/codexspec/i18n.py`)。
- 现有语言读取/翻译机制(`src/codexspec/translator.py`)与各命令模板的 `## Language Preference` 段。
- `codexspec init`、`codexspec config` 及 `/codexspec:config` 的配置读写路径。

## Requirements Traceability

| Confirmed Requirement | Spec Coverage | Notes |
|-----------------------|---------------|-------|
| NEED-001 | REQ-001, REQ-003, REQ-005, REQ-006, REQ-007 | 完整:拆分控制 + 双侧翻译标准 |
| CON-001 | REQ-002, NFR-001 | 向后兼容 |
| CON-002 | REQ-006 | 双侧翻译标准 |
| DEC-001 | REQ-001, REQ-005, REQ-007 | 配置结构 |
| DEC-002 | REQ-002, NFR-001 | 回退顺序 |
| DEC-003 | REQ-003 | 交互覆盖范围 |
| DEC-004 | REQ-004, REQ-008 | init 行为 + commit 不变 |
| DEC-005 | NFR-002 | output 静默回退 |
| OUT-001 | Out of Scope | 不动 docs/ 站点 |
| OUT-002 | Out of Scope | 不回溯重译 |
