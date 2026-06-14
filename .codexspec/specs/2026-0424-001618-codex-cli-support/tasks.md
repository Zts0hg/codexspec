# 任务分解: 扩展 CodexSpec 支持 OpenAI Codex CLI

## 概览

总任务数: 10
可并行任务: 2
实现阶段: 4

## Phase 1: 基础 — 配置系统适配

### Task 1.1: 修改 CONFIG_TEMPLATE 支持 ai 占位符

- **类型**: 实现
- **文件**: `src/codexspec/i18n.py`
- **描述**: 将 `CONFIG_TEMPLATE` 中 `project.ai` 的硬编码值 `"claude"` 替换为 `{ai}` 占位符。修改 `generate_config_content()` 函数签名，增加 `ai: str = "claude"` 参数，并在 `CONFIG_TEMPLATE.format()` 调用中传入 `ai` 值。
- **依赖**: 无
- **预计复杂度**: 低
- **验收**: `generate_config_content(language="en", ai="codex")` 生成的内容包含 `ai: "codex"`；默认参数生成 `ai: "claude"`（向后兼容）

### Task 1.2: 为 generate_config_content 编写单元测试

- **类型**: 测试
- **文件**: `tests/test_i18n.py`
- **描述**: 在现有 `tests/test_i18n.py` 中新增测试用例：(1) `generate_config_content(ai="codex")` 输出包含 `ai: "codex"`；(2) `generate_config_content()` 默认输出包含 `ai: "claude"`（回归）；(3) `generate_config_content(ai="claude")` 显式传入与默认一致
- **依赖**: Task 1.1
- **预计复杂度**: 低

## Phase 2: 核心 — init 命令逻辑

### Task 2.1: 添加 SUPPORTED_AI_TOOLS 常量和参数验证

- **类型**: 实现
- **文件**: `src/codexspec/__init__.py`
- **描述**: 在模块顶部定义 `SUPPORTED_AI_TOOLS = ["claude", "codex"]` 常量。在 `init()` 函数中，normalized_lang 赋值之后、目标目录判断之前，添加 `--ai` 参数白名单校验：如果 `ai` 不在列表中，输出错误信息（列出支持选项）并 `raise typer.Exit(1)`。
- **依赖**: 无
- **预计复杂度**: 低
- **验收**: `codexspec init test --ai invalid` 输出包含 "claude" 和 "codex" 的提示并退出码 1

### Task 2.2: 将 .claude/ 和 CLAUDE.md 逻辑包裹为条件分支

- **类型**: 实现
- **文件**: `src/codexspec/__init__.py`
- **描述**: 将 init() 中以下三段逻辑包裹为 `if ai == "claude":` 条件块：(1) `.claude/commands/` 目录创建及模板安装（L522-580 区域）；(2) CLAUDE.md 创建及 compliance 检查（L637-648 区域）；(3) `_print_command_summary()` 调用（L660 区域）。同时将 `generate_config_content()` 调用中传入 `ai=ai` 参数。
- **依赖**: Task 1.1, Task 2.1
- **预计复杂度**: 中
- **验收**: `--ai codex` 时不创建 `.claude/` 目录和 `CLAUDE.md`；`--ai claude` 行为不变

### Task 2.3: 添加 Codex 分支 — 创建 AGENTS.md

- **类型**: 实现
- **文件**: `src/codexspec/__init__.py`
- **描述**: 在 CLAUDE.md 条件块之后添加 `elif ai == "codex":` 分支。逻辑：检查 `AGENTS.md` 是否已存在（与 CLAUDE.md 逻辑一致），不存在或 `--force` 时调用 `_get_agents_md_content(project_name)` 生成内容并写入 `AGENTS.md`。调整成功面板中的提示信息根据 `ai` 参数显示对应工具名（如 "Start Codex CLI" 替代 "Start Claude Code"）。
- **依赖**: Task 2.2, Task 3.1
- **预计复杂度**: 中
- **验收**: `--ai codex` 时创建 `AGENTS.md`；已存在时跳过；`--force` 时覆盖

## Phase 3: 内容生成

### Task 3.1: 实现 _get_agents_md_content 函数 [P]

- **类型**: 实现
- **文件**: `src/codexspec/__init__.py`
- **描述**: 新增 `_get_agents_md_content(project_name: str) -> str` 函数，生成 Codex CLI 适配的 `AGENTS.md` 内容。内容包含：(1) constitution 读取指令（纯文本 `> **IMPORTANT**: ...` 形式，非 `@` 语法）；(2) 项目概述和 SDD 方法论说明；(3) 推荐 SDD 工作流（纯文本步骤描述）；(4) `.codexspec/` 目录结构说明；(5) 开发指引和重要注意事项。参照 `_get_claude_md_content()` 的模式实现，确保输出小于 32 KiB。
- **依赖**: 无（可与 Phase 2 任务并行开发）
- **预计复杂度**: 中
- **验收**: 函数返回的字符串包含 constitution 指令、workflow 步骤、目录结构；`len(content.encode('utf-8')) < 32768`

## Phase 4: 测试

### Task 4.1: 编写 Codex init 集成测试 — 核心场景

- **类型**: 测试
- **文件**: `tests/test_init_codex.py`
- **描述**: 新增测试文件 `tests/test_init_codex.py`，包含以下测试用例：(1) TC-001: `--ai codex` 创建 AGENTS.md，无 CLAUDE.md，无 `.claude/` 目录；(2) TC-006: config.yml 中 `ai: "codex"`；(3) TC-007: `.codexspec/` 目录结构完整（memory, specs, templates, scripts）；(4) TC-008: AGENTS.md 文件大小 < 32 KiB。使用 `CliRunner` + `isolated_runner` fixture 模式（参照 `test_cli.py` 中的 TestInit 类）。
- **依赖**: Task 2.3, Task 3.1
- **预计复杂度**: 中

### Task 4.2: 编写 Codex init 集成测试 — 语言和错误处理 [P]

- **类型**: 测试
- **文件**: `tests/test_init_codex.py`
- **描述**: 在同一测试文件中补充：(1) TC-002: `--ai codex --lang zh-CN` 语言配置正确；(2) TC-005: `--ai invalid` 显示错误信息并退出码 1。
- **依赖**: Task 2.3, Task 3.1
- **预计复杂度**: 低

### Task 4.3: 编写回归测试

- **类型**: 测试
- **文件**: `tests/test_init_codex.py`
- **描述**: 在同一测试文件中补充回归测试：(1) TC-003: `--ai claude` 显式传入，行为与之前一致（创建 CLAUDE.md、.claude/）；(2) TC-004: 默认（无 --ai 参数），行为不变。
- **依赖**: Task 2.3
- **预计复杂度**: 低

### Task 4.4: 运行全量测试并验证

- **类型**: 验证
- **文件**: 无（运行 `uv run pytest`）
- **描述**: 运行全量测试套件 `uv run pytest`，确保：(1) 所有新增测试通过；(2) 所有现有测试通过（无回归）；(3) ruff 检查通过 `uv run ruff check src/`。
- **依赖**: Task 4.1, Task 4.2, Task 4.3
- **预计复杂度**: 低

## 执行顺序

```
Phase 1:  Task 1.1 ──► Task 1.2

Phase 2:  Task 2.1 ──┐
                      ├──► Task 2.2 ──► Task 2.3
Phase 3:  Task 3.1 [P]──────────────────┘

Phase 4:  Task 2.3 ──► ┌─► Task 4.1
                        ├─► Task 4.2 [P]
                        └─► Task 4.3
                              │
                              ▼
                          Task 4.4
```

## 检查点

- [x] **检查点 1**: Phase 1 完成后 — 验证 `generate_config_content(ai="codex")` 输出正确，现有测试通过
- [x] **检查点 2**: Phase 2 + 3 完成后 — 验证 `codexspec init test --ai codex --no-git` 手动执行成功
- [x] **检查点 3**: Phase 4 完成后 — 全量测试通过，ruff 检查通过
