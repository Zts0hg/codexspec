# Implementation Plan: CLI 国际化支持

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 项目现有要求 |
| CLI Framework | Typer | ^0.9 | 现有 CLI 框架 |
| Console Output | Rich | ^13 | 现有输出库，已支持 Unicode |
| Data Format | JSON | - | 翻译缓存文件格式 |
| Testing | pytest | - | 现有测试框架 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 复用现有模块结构，保持函数单一职责 |
| Testing Standards | ✅ | 计划包含单元测试覆盖，测试边缘情况 |
| Documentation | ✅ | 新增公共函数将有 docstring |
| Architecture | ✅ | 扩展现有 translator.py，遵循分离关注点 |
| Performance | ✅ | NFR 要求 < 50ms 加载时间 |
| Security | ✅ | 无安全敏感操作 |

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLI Layer (__init__.py)                   │
│  ┌──────────┐  ┌──────────────┐  ┌─────────────┐                │
│  │   init   │  │list-commands │  │set-language │                │
│  └────┬─────┘  └──────┬───────┘  └──────┬──────┘                │
│       │               │                  │                        │
│       └───────────────┼──────────────────┘                        │
│                       ▼                                          │
│              ┌────────────────┐                                  │
│              │  translate()   │  ← 新增 CLI 消息翻译函数          │
│              └───────┬────────┘                                  │
│                      │                                           │
└──────────────────────┼───────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Translation Layer (translator.py)              │
│  ┌─────────────────────┐  ┌────────────────────────────────┐    │
│  │load_translation_cache│  │ _CLI_MESSAGES (English base)   │    │
│  └─────────────────────┘  └────────────────────────────────┘    │
│                                                                   │
│  templates/translations/*.json                                    │
│  ├── zh-CN.json  (添加 "cli" 命名空间)                            │
│  ├── ja.json                                                      │
│  └── ...                                                          │
└─────────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

```
src/codexspec/
├── __init__.py           # CLI 命令定义 - 修改消息输出
├── translator.py         # 翻译核心模块 - 扩展 CLI 消息支持
├── i18n.py               # 语言配置工具 - 无需修改
└── commands/
    └── installer.py      # 命令安装器 - 可能需要微调

templates/translations/
├── zh-CN.json            # 中文翻译 - 添加 "cli" 命名空间
├── ja.json               # 日语翻译 - 添加 "cli" 命名空间
├── ko.json               # 韩语翻译 - 添加 "cli" 命名空间
└── ...                   # 其他语言

tests/
├── test_cli_i18n.py      # 新增：CLI i18n 单元测试
└── test_translator.py    # 扩展：添加 CLI 消息翻译测试
```

## 5. Module Dependency Graph

```
┌─────────────────┐
│   CLI Layer     │
│  (__init__.py)  │
└────────┬────────┘
         │ imports & calls
         ▼
┌─────────────────┐     ┌─────────────────┐
│   translator.py │────▶│     i18n.py     │
│ (扩展后)         │     │  (无需修改)      │
└─────────────────┘     └─────────────────┘
         │
         │ reads
         ▼
┌─────────────────┐
│ translations/   │
│   *.json        │
│ (扩展后)         │
└─────────────────┘
```

## 6. Module Specifications

### Module: translator.py (扩展)

- **Responsibility**:
  - 现有：命令模板 frontmatter 翻译
  - 新增：CLI 交互消息翻译
- **Dependencies**: pathlib, json, i18n.py
- **Interface**:

  ```python
  # 新增公共函数
  def translate(key: str, lang: str, **kwargs) -> str
  def load_cli_translations(lang: str) -> dict
  def get_cli_message(key: str, lang: str, **kwargs) -> str
  ```

- **Files**: `src/codexspec/translator.py`

### Module: **init**.py (修改)

- **Responsibility**: CLI 命令入口，用户交互
- **Dependencies**: translator.py (新增), typer, rich
- **Interface**: CLI 命令不变，仅修改输出消息
- **Files**: `src/codexspec/__init__.py`

### Module: 翻译文件 (扩展)

- **Responsibility**: 存储多语言翻译
- **Dependencies**: 无
- **Interface**: JSON 格式
- **Files**: `templates/translations/zh-CN.json`, `ja.json`, `ko.json`, etc.

## 7. Data Models

### 翻译文件 JSON 结构 (扩展后)

```json
{
  "constitution": {
    "description": "...",
    "argument-hint": "..."
  },
  "specify": { ... },

  "cli": {
    "init": {
      "migration_found": "Found {count} old structure command files",
      "migration_found_zh": "发现 {count} 个旧结构命令文件",
      "migration_confirm": "Migrate to new structure?",
      "migration_confirm_zh": "是否迁移到新结构?",
      "migration_success": "✓ Migration complete",
      "migration_success_zh": "✓ 迁移完成",
      "migration_failed": "✗ Migration failed",
      "migration_failed_zh": "✗ 迁移失败",
      "update_confirm": "Overwrite and update command templates?",
      "update_confirm_zh": "是否覆盖更新命令模板?",
      "commands_updated": "✓ Updated {count} commands",
      "commands_updated_zh": "✓ 已更新 {count} 个命令",
      "commands_installed": "✓ Installed {count} commands to {path}",
      "commands_installed_zh": "✓ 已安装 {count} 个命令到 {path}",
      "file_created": "Created: {file}",
      "file_created_zh": "已创建: {file}",
      "file_updated": "Updated: {file} ({detail})",
      "file_updated_zh": "已更新: {file} ({detail})",
      "git_initialized": "Initialized: Git repository",
      "git_initialized_zh": "已初始化: Git 仓库",
      "git_failed": "Warning: Failed to initialize git repository",
      "git_failed_zh": "警告: Git 仓库初始化失败",
      "success_title": "Success",
      "success_title_zh": "成功",
      "success_message": "CodexSpec project initialized successfully!",
      "success_message_zh": "CodexSpec 项目初始化成功!",
      "success_project_dir": "Project directory: {path}",
      "success_project_dir_zh": "项目目录: {path}",
      "next_steps": "Next steps:",
      "next_steps_zh": "下一步:",
      "tips_header": "💡 Tips:",
      "tips_header_zh": "💡 提示:",
      "tips_git": "Add .claude/ to Git: git add .claude/",
      "tips_git_zh": "建议将 .claude/ 目录纳入 Git 管理: git add .claude/",
      "tips_list": "Run codexspec list-commands to see all available commands",
      "tips_list_zh": "运行 codexspec list-commands 查看所有可用命令",
      "tips_edit": "Edit .md files directly to customize command behavior",
      "tips_edit_zh": "直接编辑 .md 文件自定义命令行为",
      "important_header": "Important:",
      "important_header_zh": "重要提示:",
      "important_message": "The constitution is the foundation of your SDD workflow.",
      "important_message_zh": "Constitution 是 SDD 工作流的基础。",
      "important_action": "Run /codexspec.constitution to customize it for your project.",
      "important_action_zh": "运行 /codexspec.constitution 为您的项目定制它。",
      "compliance_confirm": "CLAUDE.md already exists without Constitution Compliance section.\nThe Constitution Compliance section ensures Claude follows your project's constitution.\n? Would you like to add the Constitution Compliance section?",
      "compliance_confirm_zh": "CLAUDE.md 已存在但缺少 Constitution 合规部分。\nConstitution 合规部分确保 Claude 遵循您项目的宪法。\n? 是否添加 Constitution 合规部分?",
      "category_core": "Core Commands ({count})",
      "category_core_zh": "核心命令 ({count})",
      "category_enhanced": "Enhanced Commands ({count})",
      "category_enhanced_zh": "增强命令 ({count})",
      "category_git": "Git Workflow ({count})",
      "category_git_zh": "Git 工作流 ({count})"
    },
    "list_commands": {
      "header": "CodexSpec Available Commands ({count})",
      "header_zh": "CodexSpec 可用命令 ({count} 个)",
      "table_header": "Command",
      "table_header_zh": "命令",
      "description_header": "Description",
      "description_header_zh": "描述",
      "no_project": "No CodexSpec project found in current directory.",
      "no_project_zh": "当前目录未找到 CodexSpec 项目。",
      "run_init": "Run codexspec init to create a new project.",
      "run_init_zh": "运行 codexspec init 创建新项目。"
    },
    "set_language": {
      "language_set": "Language set to: {lang} ({name})",
      "language_set_zh": "语言设置为: {lang} ({name})",
      "language_failed": "Failed to update language setting",
      "language_failed_zh": "语言设置更新失败",
      "language_warning": "Warning: '{lang}' is not in the list of commonly supported languages.",
      "language_warning_zh": "警告: '{lang}' 不在常用支持语言列表中。",
      "commit_lang_set": "Commit message language set to: {lang}",
      "commit_lang_set_zh": "提交消息语言设置为: {lang}"
    }
  }
}
```

> **Note**: 实际实现时，非英语翻译将存储在对应的语言文件中（如 `zh-CN.json`），而非在英文文件中添加 `_zh` 后缀。上述结构仅为设计示意。

### 实际翻译文件结构

**templates/translations/zh-CN.json** (扩展部分):

```json
{
  "cli": {
    "init": {
      "migration_found": "发现 {count} 个旧结构命令文件",
      "migration_confirm": "是否迁移到新结构?",
      ...
    },
    "list_commands": { ... },
    "set_language": { ... }
  }
}
```

**templates/translations/en.json** (新建，作为基准):

```json
{
  "cli": {
    "init": {
      "migration_found": "Found {count} old structure command files",
      "migration_confirm": "Migrate to new structure?",
      ...
    },
    ...
  }
}
```

## 8. API Contracts

### Function: translate()

```python
def translate(key: str, lang: str = "en", **kwargs) -> str:
    """Translate a CLI message to the target language.

    Args:
        key: Message key in format "cli.{command}.{message}"
             e.g., "cli.init.migration_found"
        lang: Target language code (default: "en")
        **kwargs: Format parameters for the message

    Returns:
        Translated and formatted message string

    Examples:
        >>> translate("cli.init.migration_found", "zh-CN", count=3)
        '发现 3 个旧结构命令文件'
        >>> translate("cli.init.migration_found", "en", count=3)
        'Found 3 old structure command files'
    """
```

### Function: load_cli_translations()

```python
def load_cli_translations(lang: str) -> dict:
    """Load CLI message translations for a language.

    Args:
        lang: Target language code

    Returns:
        Dictionary of CLI messages, or empty dict if not found

    Note:
        Falls back to English messages if translation not found
    """
```

### CLI Command Behavior (不变)

命令签名和行为保持不变，仅输出消息国际化：

```
codexspec init [PROJECT_NAME] [OPTIONS]
  --language TEXT    Output language (default: en)
  --ai TEXT          AI assistant type (default: claude)
  --force            Overwrite existing files
  --no-git           Skip git initialization
  --here             Initialize in current directory
```

## 9. Implementation Phases

### Phase 1: Foundation

- [ ] 在 `translator.py` 中定义英文基准消息 `_CLI_MESSAGES_EN`
- [ ] 实现 `load_cli_translations()` 函数
- [ ] 实现 `translate()` 函数，支持参数化消息
- [ ] 创建 `templates/translations/en.json` 作为英文基准

### Phase 2: 中文翻译

- [ ] 在 `zh-CN.json` 中添加 `cli` 命名空间
- [ ] 翻译所有 `init` 命令消息
- [ ] 翻译所有 `list-commands` 命令消息
- [ ] 翻译所有 `set-language` 命令消息

### Phase 3: CLI 集成

- [ ] 修改 `init()` 函数，使用 `translate()` 替换硬编码消息
- [ ] 修改 `list_commands()` 函数，使用 `translate()` 替换硬编码消息
- [ ] 修改 `set_language()` 函数，使用 `translate()` 替换硬编码消息
- [ ] 修改 `confirm_add_compliance()` 函数，使用 `translate()` 替换硬编码消息
- [ ] 修改 `_print_command_summary()` 函数，使用 `translate()` 替换硬编码消息

### Phase 4: 其他语言

- [ ] 在 `ja.json` 中添加 `cli` 命名空间
- [ ] 在 `ko.json` 中添加 `cli` 命名空间
- [ ] 在 `es.json`、`fr.json`、`de.json`、`pt-BR.json` 中添加 `cli` 命名空间

### Phase 5: 测试

- [ ] 编写 `test_cli_i18n.py` 单元测试
- [ ] 测试英文输出
- [ ] 测试中文输出
- [ ] 测试未知语言回退
- [ ] 测试参数化消息
- [ ] 测试翻译键缺失时的回退行为
- [ ] 测试翻译文件损坏时的回退行为
- [ ] 测试翻译缓存加载性能 (< 50ms，验证 NFR-001)

## 10. Technical Decisions

### Decision 1: 翻译文件结构

- **Choice**: 在现有 JSON 文件中添加 `cli` 命名空间
- **Rationale**:
  - 复用现有基础设施，无需新增文件类型
  - 翻译缓存加载逻辑可共用
  - 保持翻译文件的一致性
- **Alternatives**:
  - 创建独立的 `cli-messages.json` 文件
- **Trade-offs**:
  - 文件略大，但影响可忽略（JSON 加载很快）

### Decision 2: 英文基准存储位置

- **Choice**: 创建 `en.json` 存储英文基准，同时在代码中保留 `_CLI_MESSAGES_EN` 作为后备
- **Rationale**:
  - 双重保障，代码中保留基准防止文件缺失
  - 便于翻译工具处理（所有语言文件格式一致）
- **Alternatives**:
  - 仅在代码中定义英文，不创建 `en.json`
- **Trade-offs**:
  - 轻微冗余，但提高了健壮性

### Decision 3: 翻译键格式

- **Choice**: `cli.{command}.{message_key}` 格式
- **Rationale**:
  - 清晰的层级结构
  - 便于理解和维护
  - 与现有模板翻译（`constitution.description`）风格一致
- **Alternatives**:
  - 扁平格式如 `init_migration_found`
- **Trade-offs**:
  - 键名稍长，但更清晰

### Decision 4: 回退策略

- **Choice**: 翻译缺失时回退到英文，不抛出异常
- **Rationale**:
  - 用户体验优先，程序不应因翻译缺失而崩溃
  - 英文作为通用语言，适合作为回退选项
- **Alternatives**:
  - 显示翻译键名（用户不友好）
  - 抛出异常（过于激进）
- **Trade-offs**:
  - 用户可能看到英文消息，但比崩溃好

### Decision 5: 参数化消息语法

- **Choice**: Python 格式化字符串 `{key}` 语法
- **Rationale**:
  - 与 Python f-string 一致，开发者熟悉
  - `str.format()` 原生支持
- **Alternatives**:
  - `$key` 语法（shell 风格）
  - `%s` 语法（printf 风格，已过时）
- **Trade-offs**:
  - 无显著 trade-off

## 11. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| 翻译文件格式错误导致加载失败 | Low | Medium | try-except 包裹，回退到英文 |
| 消息键拼写错误 | Medium | Low | 代码中保留英文基准作为后备 |
| 参数化消息参数缺失 | Medium | Low | 使用 `str.format()` 的安全调用方式 |
| 多字节字符表格对齐问题 | Low | Low | Rich 库已支持 Unicode 宽度 |

## 12. Files to Modify

| File | Action | Description |
|------|--------|-------------|
| `src/codexspec/translator.py` | Modify | 添加 CLI 消息翻译函数 |
| `src/codexspec/__init__.py` | Modify | 替换硬编码消息为翻译调用 |
| `templates/translations/en.json` | Create | 英文基准消息 |
| `templates/translations/zh-CN.json` | Modify | 添加 `cli` 命名空间 |
| `templates/translations/ja.json` | Modify | 添加 `cli` 命名空间 |
| `templates/translations/ko.json` | Modify | 添加 `cli` 命名空间 |
| `templates/translations/es.json` | Modify | 添加 `cli` 命名空间 |
| `templates/translations/fr.json` | Modify | 添加 `cli` 命名空间 |
| `templates/translations/de.json` | Modify | 添加 `cli` 命名空间 |
| `templates/translations/pt-BR.json` | Modify | 添加 `cli` 命名空间 |
| `tests/test_cli_i18n.py` | Create | 单元测试 |
| `tests/test_translator.py` | Modify | 扩展测试 |

---

*Plan generated: 2026-03-12*
