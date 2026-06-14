# 实现计划: 扩展 CodexSpec 支持 OpenAI Codex CLI

## 1. 技术栈

| 类别 | 技术 | 版本 | 备注 |
|------|------|------|------|
| 语言 | Python | >=3.11 | 现有技术栈 |
| CLI 框架 | Typer | >=0.9.0 | 现有技术栈 |
| 格式化 | Rich | >=13.0.0 | 现有技术栈 |
| 测试 | pytest + typer.testing.CliRunner | >=7.0 | 现有测试模式 |
| Lint | ruff | >=0.1.0 | 现有技术栈 |

无需引入新依赖。

## 2. Constitution 合规审查

| 原则 | 合规 | 说明 |
|------|------|------|
| Code Quality | ✅ | 遵循现有代码模式，函数单一职责 |
| Testing Standards | ✅ | 为每个新增/修改逻辑编写测试 |
| Documentation | ✅ | 新增公共函数包含 docstring 和 type hints |
| Architecture | ✅ | 最小化改动，不引入新抽象层 |
| Performance | ✅ | 仅增加简单条件分支，无性能影响 |
| Security | ✅ | 输入验证（--ai 参数白名单） |
| Slash Command Rules | ✅ | 不修改 templates/commands/ 内容 |

## 3. 架构概览

本功能在 `init` 命令现有流程中插入条件分支，根据 `--ai` 参数值选择不同的初始化路径。核心设计原则：**条件分支，非抽象层**。

```
codexspec init --ai {claude|codex}
        │
        ▼
┌─────────────────────┐
│ 参数验证             │ ← REQ-009: 白名单校验
│ (SUPPORTED_AI_TOOLS) │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ .codexspec/ 目录创建  │ ← REQ-004: AI 无关，共享
│ (memory, specs, etc.)│
└────────┬────────────┘
         │
         ▼
    ┌────┴────┐
    │ ai == ? │
    └────┬────┘
    claude│         codex
         │              │
         ▼              ▼
┌──────────────┐ ┌──────────────┐
│ .claude/     │ │ (跳过)        │ ← REQ-003
│ commands/    │ │              │
│ 安装模板     │ │              │
└──────┬───────┘ └──────┬───────┘
       │                │
       ▼                ▼
┌──────────────┐ ┌──────────────┐
│ CLAUDE.md    │ │ AGENTS.md    │ ← REQ-002, REQ-005
│ (@ 引用语法) │ │ (纯文本指令) │
└──────┬───────┘ └──────┬───────┘
       │                │
       └───────┬────────┘
               ▼
┌──────────────────────┐
│ config.yml           │ ← REQ-007, REQ-008
│ (ai: {claude|codex}) │
└──────────────────────┘
```

## 4. 组件结构

```
src/codexspec/
├── __init__.py              # [修改] init 函数 + _get_agents_md_content()
└── i18n.py                  # [修改] CONFIG_TEMPLATE + generate_config_content()

tests/
├── test_cli.py              # [修改] 扩展 TestInit 类
└── test_init_codex.py       # [新增] Codex 专项测试
```

## 5. 模块依赖图

```
┌────────────────────┐
│  __init__.py       │
│  (init command)    │
└────────┬───────────┘
         │ 调用
         ▼
┌────────────────────┐     ┌─────────────────────┐
│  i18n.py           │     │  commands/installer  │
│  generate_config() │     │  install_commands()  │
└────────────────────┘     └─────────────────────┘
```

改动方向：`__init__.py` → `i18n.py`（传递 ai 参数），`__init__.py` → `installer.py`（条件调用）。

## 6. 模块规格

### 模块: `src/codexspec/__init__.py`

- **职责**: init 命令主逻辑，AI 工具路由，AGENTS.md 内容生成
- **依赖**: `i18n.py`（配置生成），`commands/installer.py`（模板安装）
- **接口变更**:
  - `init()`: `--ai` 参数增加验证逻辑和条件分支
  - `_get_agents_md_content(project_name: str) -> str`: 新增函数
- **修改文件**: `src/codexspec/__init__.py`
- **关键改动点**:
  1. L388-389: `ai` 参数保持不变（已存在）
  2. 在 L446 后（normalized_lang 之后）: 添加 `--ai` 参数验证
  3. L522-580: 包裹 `.claude/commands/` 创建逻辑为 `if ai == "claude":` 条件块
  4. L637-648: 包裹 `CLAUDE.md` 创建逻辑为条件块，新增 `AGENTS.md` 分支
  5. L592: `generate_config_content()` 调用传入 `ai` 参数
  6. L660: `_print_command_summary()` 仅在 `ai == "claude"` 时调用
  7. L662-688: 成功面板和提示信息根据 `ai` 参数调整

### 模块: `src/codexspec/i18n.py`

- **职责**: 配置模板和语言工具
- **依赖**: 无外部依赖
- **接口变更**:
  - `CONFIG_TEMPLATE`: `project.ai` 从硬编码 `"claude"` 改为 `{ai}` 占位符
  - `generate_config_content(language, created, ai)`: 新增 `ai` 参数
- **修改文件**: `src/codexspec/i18n.py`

### 模块: `tests/test_init_codex.py`（新增）

- **职责**: Codex 初始化专项测试
- **依赖**: `codexspec.app`, `typer.testing.CliRunner`
- **接口**: pytest test functions
- **文件**: `tests/test_init_codex.py`

## 7. 命令接口

### `codexspec init`（修改）

- **参数**: `--ai` (已有，值域扩展为 `claude | codex`)
- **新增行为**:
  - `--ai codex`: 创建 AGENTS.md、跳过 .claude/、config 记录 codex
  - `--ai invalid`: 错误退出，提示支持的选项
- **退出码**: 0 成功、1 错误（含参数验证失败）

## 8. 实现阶段

### Phase 1: 基础 — 配置系统适配

- [ ] 修改 `CONFIG_TEMPLATE`：`project.ai` 改为 `{ai}` 占位符
- [ ] 修改 `generate_config_content()`：增加 `ai` 参数（默认 `"claude"`）
- [ ] 确保现有调用点传递默认值或显式值

### Phase 2: 核心 — init 命令条件分支

- [ ] 定义 `SUPPORTED_AI_TOOLS = ["claude", "codex"]` 常量
- [ ] 在 init 函数中添加 `--ai` 参数验证
- [ ] 将 `.claude/commands/` 创建和模板安装逻辑包裹为 `if ai == "claude":` 条件块
- [ ] 将 `CLAUDE.md` 创建逻辑包裹为条件块
- [ ] 添加 `elif ai == "codex":` 分支创建 `AGENTS.md`
- [ ] `generate_config_content()` 调用传入 `ai` 参数
- [ ] 调整成功面板和提示信息根据 ai 类型显示

### Phase 3: 内容生成 — AGENTS.md

- [ ] 实现 `_get_agents_md_content(project_name: str) -> str` 函数
- [ ] 内容包含：constitution 读取指令、项目概述、SDD 工作流、目录结构、开发指引
- [ ] 验证生成内容 < 32 KiB

### Phase 4: 测试

- [ ] 新增 `tests/test_init_codex.py`
- [ ] TC-001: `--ai codex` 创建 AGENTS.md，无 CLAUDE.md，无 .claude/
- [ ] TC-002: `--ai codex --lang zh-CN` 语言配置正确
- [ ] TC-003: `--ai claude` 回归测试
- [ ] TC-004: 默认（无 --ai）回归测试
- [ ] TC-005: `--ai invalid` 错误处理
- [ ] TC-006: config.yml 中 ai 字段正确
- [ ] TC-007: .codexspec/ 目录结构完整
- [ ] TC-008: AGENTS.md 文件大小 < 32 KiB
- [ ] `generate_config_content()` 单元测试（ai 参数传递）
- [ ] 现有测试全部通过（回归）

## 9. 技术决策

### 决策 1: 条件分支而非抽象层

- **选择**: 在 `init()` 函数中使用 `if ai == "claude" / elif ai == "codex"` 条件分支
- **理由**: 当前仅支持 2 种 AI 工具，抽象层（如 AgentAdapter 接口）过度设计。条件分支清晰直接，符合 YAGNI 原则。
- **替代方案**: 创建 `AIAgent` 基类 + `ClaudeAgent`/`CodexAgent` 子类
- **权衡**: 当未来支持 3+ 种 AI 工具时需要重构，但当前复杂度足够低

### 决策 2: AGENTS.md 使用纯文本指令引用 constitution

- **选择**: 在 AGENTS.md 中使用 `> **IMPORTANT**: ... read ... constitution.md` 纯文本指令
- **理由**: Codex CLI 不支持 Claude Code 的 `@file` 引用语法。纯文本指令是跨工具兼容的最简方案。
- **替代方案**: 将 constitution 内容直接嵌入 AGENTS.md
- **权衡**: 嵌入方案保证内容可见但导致重复和同步问题；引用方案依赖 Codex 主动读取文件

### 决策 3: 参数验证使用白名单常量

- **选择**: 定义 `SUPPORTED_AI_TOOLS` 常量列表，手动校验
- **理由**: Typer 的 `click.Choice` 虽然更优雅，但会改变帮助文本格式和错误信息格式，可能影响现有 i18n 翻译逻辑。手动校验保持一致性。
- **替代方案**: 使用 `typer.Option(click_type=click.Choice(...))`
- **权衡**: 手动校验需要自行格式化错误信息，但获得完全控制权
