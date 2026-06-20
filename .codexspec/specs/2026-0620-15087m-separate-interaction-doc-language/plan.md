# Implementation Plan: separate-interaction-doc-language

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Related Spec**: `.codexspec/specs/2026-0620-15087m-separate-interaction-doc-language/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0620-15087m-separate-interaction-doc-language/requirements.md`
**Created**: 2026-06-20
**Status**: Draft

## Context

当前 `.codexspec/config.yml` 的 `language.output` 单一字段同时决定"与 LLM 交互/CLI 终端输出的语言"和"生成工件文件的语言"。`src/codexspec/i18n.py` 用正则直接解析 `output:`(与 `commit:`),没有引入 YAML 依赖;`get_project_language()` 读 `output`、`get_commit_language()` 读 `commit`。18 个命令模板各自带一段 `## Language Preference`,统一引用 `language.output`。`codexspec init --lang` 经 `generate_config_content()` + `CONFIG_TEMPLATE` 写入 `output`。`codexspec config` 提供 `--set-lang`/`--set-commit-lang`。

本计划在**不破坏向后兼容、不引入新依赖**的前提下,把单一 `output` 拆为 `interaction` + `document`,并让模板按既定翻译标准在两侧分别执行。

## Goals / Non-Goals

**Goals**:

- 新增 `language.interaction` / `language.document`,各自按"显式 → output → en"解析(REQ-001/002)。
- interaction 管 LLM 对话 + CLI 终端输出;document 管工件文件(REQ-003)。
- `init --lang` 同时写入三者;`/codexspec:config` 与 `codexspec config` 可独立编辑两者(REQ-004/005)。
- 18 个命令模板的 Language Preference 段改为区分两侧并引用翻译标准(REQ-006)。
- 新字段经 i18n 校验(REQ-007);`commit` 解析路径不变(REQ-008)。

**Non-Goals**(继承自 spec 的 OUT-001/002):

- 不改 CodexSpec 自身 `docs/` 站点的翻译流程。
- 不回溯重译既有 spec 工件。
- 不引入 YAML 解析依赖(继续沿用既有正则解析模式)。
- 本版本不对 `output` 发 deprecation 警告(NFR-002)。

## 既有仓库约束(已核实)

- **解析模式**:`i18n.py` 用正则 `^\s*{key}:\s*['\"]?(\S+?)['\"]?\s*$` 逐字段读取(非完整 YAML),语言码统一经 `normalize_locale()` 规范化、`is_supported_language()` 校验。本计划沿用此模式,不新增依赖。
- **写配置**:`generate_config_content(language, created)`(`__init__.py:218-235`)+ `CONFIG_TEMPLATE`(`i18n.py:190-215`,含 `output: "{language}"`)。
- **CLI 语言入口**:`get_project_language()`(`i18n.py:238-260`)被 `list_commands()`(`__init__.py:344`)等调用;`get_commit_language()` 被 init 调用。
- **翻译提供**:`translator.translate(key, language, **kwargs)` 按 key 取本地化串。
- **模板**:`templates/commands/*.md` 共 18 个含 `## Language Preference`;其中 commit 类(`commit-staged.md`、`pr.md` 的 commit 部分)用"commit > output > en"优先级块。
- **自举规则(constitution)**:命令模板**只改 `templates/commands/` 源**,改完重跑 `codexspec init` 同步 `.claude/commands/codexspec/`;不动 `_get_default_constitution()`(两个 constitution 受众不同)。

## 技术方案

核心是在 `i18n.py` 增加两个解析函数,把"语言"按用途分成 interaction / document 两条解析链,二者共享"显式 → output → en"的回退;`output` 作为 legacy 字段被两条链回退引用,从而 output-only 配置行为不变。

```
config.yml                i18n.py 解析
─────────────             ────────────────────────────────
interaction: zh-CN  ──►   get_interaction_language() ──► zh-CN
document: en        ──►   get_document_language()    ──► en
output: zh-CN  (legacy)        ▲
                               └─ 两者回退都经此(显式缺失时)
```

- **LLM 对话 / CLI 终端输出** 调用 `get_interaction_language()`(替代/等同于旧 `get_project_language()` 的用途)。
- **工件文件** 由命令模板按 `get_document_language()` 指示的语言生成(模板指令层面)。
- `commit` 路径完全不变(`get_commit_language()` 原样,REQ-008)。

## Plan-Level Decisions

### PLD-1:解析函数设计(复用正则模式)

**Context**: 需要分别解析 interaction / document / output 三个键。
**Decision**: 在 `i18n.py` 新增私有助手 `_read_lang_key(content, key) -> Optional[str]`(泛化现有正则);新增 `get_interaction_language(config_file=None)` 与 `get_document_language(config_file=None)`,各自:`显式键 → output → en`(经 `normalize_locale`)。`get_project_language()` 重构为 `get_interaction_language()` 的薄封装(向后兼容别名;output-only 配置结果与旧实现一致)。
**Rationale**: 沿用既有正则解析模式,零新依赖;单一回退逻辑集中,易测。
**Covers**: REQ-001, REQ-002, REQ-003, REQ-007
**Decision Level**: Plan-level(仅细化实现,不改产品意图)

### PLD-2:模板 Language Preference 统一新块

**Context**: 18 个模板现有 3 种 Language Preference 变体(A 简版 13 个、B 扩展 5 个、C commit 专用 2 个),都引用 `language.output`。
**Decision**: 为 18 个**非 commit** 模板(Var A/B)替换为统一新块——区分 interaction(对话)/ document(工件),各自标注"→ output → en"回退,并引用翻译标准(按意思译、无合适母语词时保留英文、地道表达)。**commit 类模板(`commit-staged.md`、`pr.md` 的 commit 部分)保持"commit > output > en"优先级块不变**(REQ-008)。`pr.md` 的 PR 描述生成部分归入 document。
**Rationale**: 统一块降低维护成本、确保两侧一致;commit 路径不变以控制风险。
**Covers**: REQ-003, REQ-006, REQ-008
**Decision Level**: Plan-level

### PLD-3:init 写三字段、config 暴露两新字段

**Context**: init 与 config 需支持新字段。
**Decision**:

- `CONFIG_TEMPLATE`(`i18n.py:190-215`)与 `generate_config_content()`:同时写 `interaction: "{language}"`、`document: "{language}"`、`output: "{language}"`(legacy)。
- `codexspec config`(`__init__.py:175-332`)新增 `--set-interaction-lang` / `--set-document-lang`(镜像现有 `--set-lang`/`--set-commit-lang` 模式,经 `is_supported_language` 校验);`--set-lang` 保持只更新 `output`(legacy 行为不变)。`templates/commands/config.md` 交互菜单新增"Interaction language""Document language"选项。
**Rationale**: 复用既有 flag 模式与校验;`--set-lang` 不变以避免破坏脚本/肌肉记忆。
**Covers**: REQ-004, REQ-005, REQ-007
**Decision Level**: Plan-level

### PLD-4:向后兼容与弃用策略

**Context**: 现存 output-only 配置须零改动继续工作。
**Decision**: 解析回退(PLD-1)保证 output-only → 两者皆 output,行为与旧版逐字一致;本版本**不**对 `output` 发 deprecation 警告(NFR-002);`get_project_language()` 保留为兼容别名。
**Rationale**: 见 DEC-002/DEC-005(CON-001)。
**Covers**: NFR-001, NFR-002
**Decision Level**: Plan-level

## 受影响组件(均带 Covers)

| 组件 | 文件 | 改动 | Covers |
|---|---|---|---|
| 语言解析 | `src/codexspec/i18n.py` | 新增 `_read_lang_key`/`get_interaction_language`/`get_document_language`;`get_project_language` 改为别名 | REQ-001/002/003/007 |
| 配置模板 | `src/codexspec/i18n.py`(`CONFIG_TEMPLATE` ~L190-215)+ `generate_config_content`(~L218) | 写 interaction+document+output | REQ-001/004 |
| CLI 调用点 | `src/codexspec/__init__.py`(`list_commands` ~L344 等) | 改用 `get_interaction_language()` | REQ-003 |
| config CLI | `src/codexspec/__init__.py`(`config` ~L175-332) | 新增 `--set-interaction-lang`/`--set-document-lang` | REQ-005/007 |
| config 模板 | `templates/commands/config.md` | 菜单加 Interaction/Document 选项 | REQ-005 |
| 命令模板 | `templates/commands/*.md`(16 个非 commit + `pr.md` 文档部分) | 替换为统一 Language Preference 新块 | REQ-003/006 |
| commit 模板 | `templates/commands/commit-staged.md`、`pr.md`(commit 部分) | **不改**(commit 优先级不变) | REQ-008 |
| 测试 | `tests/test_i18n.py`、`tests/test_init_language.py`、`tests/test_cli_i18n.py`、新增模板块守卫测试 | 见验证策略 | NFR-001/002 等 |

**统一 Language Preference 新块(拟)**:

```
## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (requirements/spec/plan/tasks).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.
```

## Risks / Trade-offs

| 风险 | 可能性 | 影响 | 缓解 |
|---|---|---|---|
| 16+ 模板新块不一致 | 中 | 中 | 用脚本批量替换 + 加"所有非 commit 模板含新块"守卫测试(复用 `test_sdd_workflow_templates.py` 模式) |
| 正则解析对新的 interaction/document 键的边界(引号/空格)处理 | 低 | 中 | 复用已验证的现有正则;单测覆盖带/不带引号、缺字段、仅 output 等场景 |
| `get_project_language()` 语义从 output 变为 interaction,影响未知外部调用方 | 低 | 低 | 保留为别名且 output-only 时结果不变;内部唯一调用方(list_commands)本就该用 interaction |
| 自举产物 `.claude/commands/codexspec/` 滞后 | 低 | 低 | 模板改完重跑 `codexspec init` 同步(既有流程) |

## Implementation Phases

### Phase 1 — 解析层(config 读)

- [ ] `i18n.py`:新增 `_read_lang_key`、`get_interaction_language`、`get_document_language`;`get_project_language` 改别名。
- [ ] `CONFIG_TEMPLATE` + `generate_config_content`:写 interaction+document+output。
- [ ] `__init__.py`:`list_commands` 等改用 `get_interaction_language()`。

### Phase 2 — 配置与模板(config 写 + 模板)

- [ ] `codexspec config`:新增 `--set-interaction-lang`/`--set-document-lang`(含校验)。
- [ ] `templates/commands/config.md`:菜单加两选项。
- [ ] `templates/commands/*.md`:16 个非 commit 模板替换为统一新块;`pr.md` 文档部分归 document;`commit-staged.md`/`pr.md` commit 部分不动。
- [ ] 重跑 `codexspec init` 同步 `.claude/commands/codexspec/`。

### Phase 3 — 测试与验证

- [ ] `test_i18n.py`:新增 interaction/document 解析与回退用例;更新 `TestGenerateConfigContent`(期望三字段)。
- [ ] `test_init_language.py`:断言 init 写 interaction+document+output。
- [ ] config CLI 新 flag 测试;新增"非 commit 模板含统一 Language Preference 新块"守卫测试。
- [ ] 向后兼容回归:output-only 配置行为对照。

## Verification Strategy

- **单元**:`get_interaction_language`/`get_document_language` 覆盖(显式 / output 回退 / en 默认 / 无效码);`generate_config_content` 含三字段;config 新 flag 校验非法码报错。
- **回归**:`pytest`(重点 `test_i18n.py`/`test_init_language.py`/`test_cli_i18n.py`)全绿;新增守卫测试确保 16 个模板含新块。
- **端到端**:配置 `interaction: zh-CN`、`document: en`,跑 `/codexspec:generate-spec`(或 dry-run)→ 对话中文、生成的 spec.md 英文;`codexspec list-commands` 终端输出中文。
- **兼容**:仅 `output: zh-CN` 的配置,行为与旧版逐字一致(对话+文档皆 zh-CN,无 deprecation 警告)。
- **构建/门禁**:`ruff check`、`uv build`(wheel 仅含 bash/powershell)。

## Requirements Coverage

| Spec Requirement | Plan Coverage | Reference |
|------------------|---------------|-----------|
| REQ-001 | Full | PLD-1 / PLD-3(CONFIG_TEMPLATE)/ Phase 1 |
| REQ-002 | Full | PLD-1(解析回退)/ Phase 1 |
| REQ-003 | Full | PLD-1 + PLD-2(调用点 + 模板)/ Phase 1-2 |
| REQ-004 | Full | PLD-3(init 写三字段)/ Phase 1 |
| REQ-005 | Full | PLD-3(config CLI + config.md)/ Phase 2 |
| REQ-006 | Full | PLD-2(统一新块 + 翻译标准)/ Phase 2 |
| REQ-007 | Full | PLD-1/PLD-3(normalize/is_supported + flag 校验)/ Phase 1-2 |
| REQ-008 | Full | PLD-2(commit 模板与解析路径不变)/ 显式不改动 |
| NFR-001 | Full | PLD-4 + Phase 3 回归 |
| NFR-002 | Full | PLD-4(不加 deprecation 警告)/ 显式不改动 |

## Open Questions

无阻塞性技术开放问题。(产品层 OPEN-001 已由 DEC-005/NFR-002 解决。)

## Assumptions

- **假设-P1**:`codexspec config --set-lang` 继续只更新 `output`(legacy);用户用新的 `--set-interaction-lang`/`--set-document-lang` 做拆分。(实现选择,不扩展范围。)
- **假设-P2**:既有外部对 `get_project_language()` 的调用(若有)接受其等价于 interaction。(output-only 时结果不变,风险低。)
