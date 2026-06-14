# Feature: CLI 国际化支持 (CLI i18n Support)

## Overview

为 CodexSpec CLI 的用户交互消息实现多语言支持，消除当前 `init`、`list-commands`、`set-language` 命令中存在的中英文混用问题，提供一致的用户体验。

## Goals

- 实现所有 CLI 用户交互消息的国际化支持
- 复用现有翻译缓存基础设施，降低实现复杂度
- 确保用户在使用非英语语言运行命令时获得一致的语言体验
- 建立可扩展的 i18n 框架，便于未来命令的国际化

## User Stories

### Story 1: 中文用户初始化项目

**As a** 中文用户
**I want** 运行 `codexspec init --language zh-CN` 时看到全程中文输出
**So that** 我能更好地理解操作流程和结果

**Acceptance Criteria:**

- [ ] 所有确认提示使用中文（如 "是否迁移到新结构?"）
- [ ] 所有状态反馈使用中文（如 "✓ 已安装 16 个命令"）
- [ ] 成功面板使用中文
- [ ] 提示和建议使用中文
- [ ] 错误和警告消息使用中文

### Story 2: 日语用户查看命令列表

**As a** 日语用户
**I want** 运行 `codexspec list-commands --language ja` 时看到日语输出
**So that** 我能了解可用的命令功能

**Acceptance Criteria:**

- [ ] 命令分类标题使用日语
- [ ] 命令描述使用日语
- [ ] 表格标题使用日语

### Story 3: 韩语用户设置语言

**As a** 韩语用户
**I want** 运行 `codexspec set-language ko` 时看到韩语反馈
**So that** 我能确认语言设置成功

**Acceptance Criteria:**

- [ ] 语言确认消息使用韩语
- [ ] 错误提示使用韩语（如语言不支持时）

### Story 4: 未知语言回退

**As a** 使用小众语言的用户
**I want** 当我的语言没有翻译时看到英文消息
**So that** 我至少能理解基本操作

**Acceptance Criteria:**

- [ ] 缺少翻译时自动显示英文原文
- [ ] 不会出现空白或错误
- [ ] 程序继续正常执行

## Functional Requirements

### REQ-001: CLI 消息翻译存储

- 在现有 `templates/translations/*.json` 文件中添加 `cli` 命名空间
- 翻译键采用层级结构：`cli.{command}.{message_key}`
- 支持参数化消息（如 `{count}`、`{path}` 占位符）

### REQ-002: init 命令消息国际化

需要国际化的消息类别：

| 类别 | 消息示例 | 参数 |
|------|----------|------|
| 迁移检测 | "发现 {count} 个旧结构命令文件" | count |
| 迁移确认 | "是否迁移到新结构?" | - |
| 迁移结果 | "✓ 迁移完成" / "✗ 迁移失败" | - |
| 更新确认 | "是否覆盖更新命令模板?" | - |
| 安装结果 | "✓ 已安装 {count} 个命令到 {path}" | count, path |
| 文件创建 | "Created: {file}" | file |
| 文件更新 | "Updated: {file} ({detail})" | file, detail |
| Git 初始化 | "Initialized: Git repository" | - |
| 命令摘要 | "已安装 {count} 个命令到 {path}" | count, path |
| 分类标题 | "核心命令 (Core Commands)" | - |
| 成功面板 | 标题、内容、下一步提示 | project_name |
| 提示信息 | "💡 提示:" 及具体建议 | - |
| 重要提醒 | Constitution 相关提醒 | - |

### REQ-003: list-commands 命令消息国际化

需要国际化的消息：

| 类别 | 消息示例 |
|------|----------|
| 标题 | "CodexSpec 可用命令 ({count} 个)" |
| 分类名 | "核心命令"、"增强命令"、"Git 工作流" |
| 空状态 | "No CodexSpec project found in current directory." |
| 建议操作 | "Run codexspec init to create a new project." |

### REQ-004: set-language 命令消息国际化

需要国际化的消息：

| 类别 | 消息示例 | 参数 |
|------|----------|------|
| 成功设置 | "Language set to: {lang} ({name})" | lang, name |
| 设置失败 | "Failed to update language setting" | - |
| 不支持警告 | "Warning: '{lang}' is not in the list of commonly supported languages." | lang |
| 提交语言设置 | "Commit message language set to: {lang}" | lang |

### REQ-005: 翻译加载机制

- 扩展现有 `translator.py` 模块，添加 `load_cli_translations()` 函数
- 翻译缓存加载时同时加载 CLI 消息
- 语言检测优先级：命令行参数 > 环境变量 > 默认英语

### REQ-006: 消息格式化

- 支持 `{key}` 格式的参数替换
- 提供 `t()` 或 `translate()` 工具函数供 CLI 使用
- 函数签名：`translate(key: str, lang: str, **kwargs) -> str`

### REQ-007: Constitution Compliance 确认国际化

修复当前英文硬编码的确认消息：

```
# 当前（英文）
"CLAUDE.md already exists without Constitution Compliance section.
The Constitution Compliance section ensures Claude follows your project's constitution.
? Would you like to add the Constitution Compliance section?"

# 目标（支持多语言）
```

## Non-Functional Requirements

### NFR-001: 性能

- 翻译缓存加载时间 < 50ms
- 不影响 CLI 命令的整体响应时间

### NFR-002: 可维护性

- 翻译键命名清晰，易于理解和扩展
- 新增消息只需添加翻译条目，无需修改代码
- 翻译文件结构保持与现有 frontmatter 翻译一致

### NFR-003: 兼容性

- 不破坏现有翻译缓存文件结构
- 现有命令模板翻译功能不受影响
- 支持所有已在 SUPPORTED_LANGUAGES 中定义的语言

### NFR-004: 代码质量

- 遵循项目 constitution 中定义的代码质量标准
- 添加适当的单元测试覆盖

## Acceptance Criteria (Test Cases)

### TC-001: init 命令中文输出

**Given** 用户使用中文语言配置
**When** 运行 `codexspec init --language zh-CN`
**Then** 所有输出消息均为中文
**And** 无中英文混用情况

### TC-002: init 命令英文输出

**Given** 用户使用默认英语
**When** 运行 `codexspec init`
**Then** 所有输出消息均为英文

### TC-003: init 命令日语输出

**Given** 用户使用日语
**When** 运行 `codexspec init --language ja`
**Then** 所有输出消息均为日语（如翻译存在）

### TC-004: 未知语言回退

**Given** 用户使用未翻译的语言
**When** 运行 `codexspec init --language ar`
**Then** 输出回退到英文
**And** 程序正常执行无错误

### TC-005: 参数化消息

**Given** 中文语言配置
**When** 安装 16 个命令
**Then** 显示 "已安装 16 个命令到 .claude/commands/codexspec/"

### TC-006: Constitution 确认消息国际化

**Given** 中文语言配置且 CLAUDE.md 已存在但无 compliance section
**When** 运行 `codexspec init`
**Then** 确认提示使用中文

### TC-007: list-commands 输出国际化

**Given** 中文语言配置
**When** 运行 `codexspec list-commands --language zh-CN`
**Then** 命令描述和分类标题使用中文

### TC-008: set-language 输出国际化

**Given** 任意语言配置
**When** 运行 `codexspec set-language ko`
**Then** 设置成功消息使用韩语（如果 ko 翻译存在）

## Edge Cases

### Edge Case 1: 翻译键缺失

**场景**: 某个消息键在目标语言翻译文件中不存在
**处理**: 显示英文原文，记录 debug 日志

### Edge Case 2: 参数化消息参数缺失

**场景**: 消息模板需要 `{count}` 但调用时未提供
**处理**: 显示原始模板字符串（含 `{count}`），不抛出异常

### Edge Case 3: 翻译文件损坏

**场景**: 翻译 JSON 文件格式错误
**处理**: 回退到英文，记录警告日志

### Edge Case 4: 空语言参数

**场景**: `--language ""` 或 `--language "  "`
**处理**: 视为未指定，使用默认英语

### Edge Case 5: 多字节字符宽度

**场景**: 中文/日文等宽字符在表格中对齐
**处理**: 使用 rich 库的 Unicode 宽度感知功能（已支持）

## Output Examples

### 中文 init 输出示例

```
$ codexspec init --language zh-CN

发现 3 个旧结构命令文件
旧结构: .claude/commands/codexspec.*.md
新结构: .claude/commands/codexspec/*.md
? 是否迁移到新结构? [Y/n]: y
✓ 迁移完成
✓ 已更新 16 个命令

📁 已安装 16 个命令到 .claude/commands/codexspec/

  核心命令 (9)
    /codexspec.constitution
    /codexspec.specify
    ...

  增强命令 (4)
    /codexspec.clarify
    ...

  Git 工作流 (3)
    /codexspec.commit
    ...

╭─────────────── Success ───────────────╮
│ CodexSpec 项目初始化成功!             │
│                                       │
│ 项目目录: ./my-project                │
│                                       │
│ 下一步:                               │
│ 1. 进入项目: cd my-project            │
│ 2. 启动 Claude Code: claude           │
│ 3. 使用 /codexspec.constitution 建立项目原则
│ 4. 使用 /codexspec.specify 创建第一个规格
╰───────────────────────────────────────╯

💡 提示:
   - 建议将 .claude/ 目录纳入 Git 管理: git add .claude/
   - 运行 codexspec list-commands 查看所有可用命令
   - 直接编辑 .md 文件自定义命令行为

重要提示: Constitution 是 SDD 工作流的基础。
运行 /codexspec.constitution 为您的项目和团队定制它。
```

### 英文 init 输出示例

```
$ codexspec init --language en

Found 3 old structure command files
Old structure: .claude/commands/codexspec.*.md
New structure: .claude/commands/codexspec/*.md
? Migrate to new structure? [Y/n]: y
✓ Migration complete
✓ Updated 16 commands

📁 Installed 16 commands to .claude/commands/codexspec/

  Core Commands (9)
    /codexspec.constitution
    ...

╭─────────────── Success ───────────────╮
│ CodexSpec project initialized!        │
│                                       │
│ Project directory: ./my-project       │
│                                       │
│ Next steps:                           │
│ 1. Navigate to project: cd my-project │
│ 2. Start Claude Code: claude          │
│ 3. Use /codexspec.constitution to establish principles
│ 4. Use /codexspec.specify to create your first spec
╰───────────────────────────────────────╯

💡 Tips:
   - Add .claude/ to Git: git add .claude/
   - Run codexspec list-commands to see all available commands
   - Edit .md files directly to customize command behavior

Important: The constitution is the foundation of your SDD workflow.
Run /codexspec.constitution to customize it for your project.
```

## Out of Scope

- 动态翻译（Claude CLI 实时翻译）- 本次使用预翻译缓存
- 命令模板内容（frontmatter）的国际化 - 已有独立功能
- 其他 CLI 命令（如 `publish`）的国际化 - 可在后续迭代中添加
- 翻译管理工具或 Web UI
- 用户自定义翻译的运行时编辑功能
