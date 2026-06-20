# Tasks: separate-interaction-doc-language

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.
-->

**Related Plan**: `.codexspec/specs/2026-0620-15087m-separate-interaction-doc-language/plan.md`
**Related Spec**: `.codexspec/specs/2026-0620-15087m-separate-interaction-doc-language/spec.md`
**Created**: 2026-06-20
**Status**: Implemented (T1–T9 complete; 804 tests pass, ruff clean, build/wheel OK)

> 每个任务标注 `Covers: REQ/NFR; Plan: <组件/阶段>`。代码任务按项目"conditional TDD"(逻辑代码先写测试);模板/配置为直接实现 + 守卫测试。`[P]` 表示满足依赖后可与同阶段其它 `[P]` 任务并行。

---

## Phase 1 — 解析层(config 读)

### T1 — i18n 解析函数:interaction / document / output 回退

- **Outcome**: `get_interaction_language()` 与 `get_document_language()` 按"显式 → output → en"正确解析并经 `normalize_locale` 规范化;`get_project_language()` 成为前者的兼容别名(output-only 配置结果不变)。
- **Covers**: REQ-001; REQ-002; REQ-003; REQ-007; NFR-001 — Plan: PLD-1 / Phase 1
- **Files**: `src/codexspec/i18n.py`(新增 `_read_lang_key`、`get_interaction_language`、`get_document_language`;重构 `get_project_language`);`tests/test_i18n.py`(新增解析/回退/无效码用例)
- **Deps**: —
- **Verification**: `uv run pytest tests/test_i18n.py`;用例覆盖——仅 interaction、仅 document、仅 output(legacy)、三者皆无→en、无效码、带/不带引号。

### T2 — init/config 写入三字段

- **Outcome**: `generate_config_content()` 与 `CONFIG_TEMPLATE` 生成含 `interaction`+`document`+`output`(legacy)的 config.yml,三者同值。
- **Covers**: REQ-001; REQ-004 — Plan: PLD-3 / Phase 1
- **Files**: `src/codexspec/i18n.py`(`CONFIG_TEMPLATE` ~L190-215、`generate_config_content` ~L218);`tests/test_i18n.py`(`TestGenerateConfigContent` 更新);`tests/test_init_language.py`(断言 `--lang` 写三字段)
- **Deps**: —(与 T1 同文件不同段,顺序执行以免冲突;逻辑独立)
- **Verification**: `uv run pytest tests/test_i18n.py::TestGenerateConfigContent tests/test_init_language.py`;生成的 config.yml 含三键。

### T3 — CLI 调用点改用 interaction

- **Outcome**: `list_commands()` 等 CLI 展示改用 `get_interaction_language()`(终端输出跟随交互语言)。
- **Covers**: REQ-003 — Plan: Phase 1
- **Files**: `src/codexspec/__init__.py`(`list_commands` ~L344 及其它读语言处)
- **Deps**: T1
- **Verification**: `uv run pytest tests/test_cli_i18n.py`;手动 `codexspec list-commands` 在 interaction=zh-CN 下输出中文。

---

## Phase 2 — 配置与模板(config 写 + 模板)

### T4 — `codexspec config` 新增两个语言 flag

- **Outcome**: `--set-interaction-lang` / `--set-document-lang` 可独立设置两字段,经 `is_supported_language` 校验(非法码报错);`--set-lang` 行为不变(仍只改 output)。
- **Covers**: REQ-005; REQ-007 — Plan: PLD-3 / Phase 2
- **Files**: `src/codexspec/__init__.py`(`config` ~L175-332,镜像 `--set-lang`/`--set-commit-lang` 模式);对应测试
- **Deps**: T1, T2
- **Verification**: `uv run pytest`(config 相关);手动设置两 flag 后 config.yml 两键更新、非法码报错。

### T5 — `/codexspec:config` 模板菜单 `[P]`

- **Outcome**: `config.md` 交互菜单新增"Interaction language""Document language"选项(保留 Output/Commit)。
- **Covers**: REQ-005 — Plan: Phase 2
- **Files**: `templates/commands/config.md`(菜单选项区 ~L95-106)
- **Deps**: —
- **Verification**: 通读模板,菜单含四个语言选项;`mkdocs build --strict`(若该模板入站)。

### T6 — 命令模板统一 Language Preference 新块 `[P]`

- **Outcome**: 非 commit 模板替换为 plan 所定义的统一新块(区分 interaction/document + 引用翻译标准);`commit-staged.md` 与 `pr.md` 的 commit 部分保持"commit > output > en"不变;新增守卫测试确保所有非 commit 模板含新块。
- **Covers**: REQ-003; REQ-006; REQ-008 — Plan: PLD-2 / Phase 2
- **Files**: `templates/commands/*.md`(16 个非 commit 模板替换;`pr.md` 文档部分归 document、commit 部分不动;`commit-staged.md` 不动);`tests/test_sdd_workflow_templates.py`(新增"非 commit 模板含统一 Language Preference 块"守卫,复用既有同步测试模式)
- **Deps**: —
- **Verification**: `uv run pytest tests/test_sdd_workflow_templates.py`;grep 确认 commit 类模板仍为旧 commit 块、其余含新块。

### T7 — 重跑 init 同步自举产物

- **Outcome**: `.claude/commands/codexspec/*.md` 与更新后的 `templates/commands/` 一致(自举刷新)。
- **Covers**: REQ-006 — Plan: Phase 2
- **Files**: `.claude/commands/codexspec/`(派生产物,由 init 生成)
- **Deps**: T6
- **Verification**: `codexspec init .` 后 `git status` 显示 `.claude/commands/codexspec/*.md` 改动;正文与模板一致。

---

## Phase 3 — 测试与验证

### T8 — 向后兼容回归

- **Outcome**: 仅含 `output` 的配置,interaction/document 解析结果与旧版逐字一致,且无 deprecation 警告。
- **Covers**: NFR-001; NFR-002 — Plan: PLD-4 / Phase 3
- **Files**: `tests/test_i18n.py`(output-only 对照用例);确认解析路径无 warning 输出
- **Deps**: T1, T2
- **Verification**: `uv run pytest`;output-only 配置下 `get_interaction_language==get_document_language==旧 get_project_language 结果`,无 stderr 警告。

### T9 — 端到端 + 构建/打包校验

- **Outcome**: interaction=zh-CN/document=en 时对话中文、工件英文;CLI 终端中文;`ruff`/`uv build`/wheel 边界通过。
- **Covers**: REQ-003; REQ-004; NFR-001 — Plan: Phase 3
- **Files**: —(验收性任务)
- **Deps**: T1–T7
- **Verification**:
  - 配置 `interaction: zh-CN`、`document: en`,跑 `/codexspec:generate-spec`(或 dry-run)→ LLM 对话中文、生成 spec.md 英文。
  - `codexspec list-commands` 终端输出中文。
  - `uv run pytest`、`uv run ruff check src/` 全绿;`uv build` 后 wheel 内 `scripts/` 仅 bash/powershell(边界不变)。

---

## Coverage

| Plan 组件 / REQ / NFR | 任务覆盖 |
|---|---|
| REQ-001(schema interaction+document) | T1, T2 |
| REQ-002(回退 各自→output→en) | T1 |
| REQ-003(interaction=对话+CLI,document=工件) | T1, T3, T6 |
| REQ-004(init 写三字段) | T2, T9 |
| REQ-005(config 暴露两者) | T4, T5 |
| REQ-006(模板双侧 + 翻译标准) | T6, T7 |
| REQ-007(语言码 i18n 校验) | T1, T4 |
| REQ-008(commit 不变) | T6(显式不改动 commit 模板) |
| NFR-001(向后兼容) | T1, T8, T9 |
| NFR-002(output 静默回退) | T8 |
| Plan: i18n 解析(PLD-1) | T1 |
| Plan: CONFIG_TEMPLATE/init(PLD-3) | T2 |
| Plan: config CLI(PLD-3) | T4 |
| Plan: 模板统一块(PLD-2) | T6, T7 |
| Plan: 向后兼容(PLD-4) | T8 |

## 依赖摘要

- 线性主干:T1 → T3;T1+T2 → T4;T6 → T7;T1+T2 → T8;T1–T7 → T9。
- 可并行(满足依赖后):T5、T6(独立模板编辑,与 Phase 1 代码可并行)。
- 无环;每个依赖均为执行/校验所需。

## Unmapped Tasks

无。所有任务均映射到 REQ/NFR 或必要实现支撑(如 T7 自举刷新、T9 构建校验)。

## Open Questions

无阻塞性问题。
