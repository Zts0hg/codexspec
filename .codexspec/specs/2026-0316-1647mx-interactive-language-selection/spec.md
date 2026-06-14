# Feature: Interactive Language Selection for init Command

## Overview

优化 `codexspec init` 命令的语言选择体验。当用户未通过 `--lang` 参数指定语言时，在 TTY 终端中显示交互式语言选择界面，引导用户选择合适的输出语言。此功能旨在解决用户不了解需要传入 `--lang` 参数来设置语言的问题。

## Goals

- **提升用户体验**：新用户无需阅读文档即可发现并选择语言
- **保持向后兼容**：非交互环境（CI/脚本）保持现有默认行为
- **简化依赖**：使用现有的 Rich 库实现交互，不引入新依赖
- **支持灵活性**：预定义常用语言 + 支持自定义语言代码输入

## User Stories

### Story 1: 新用户首次初始化项目

**As a** CodexSpec 新用户
**I want** 在运行 `codexspec init` 时看到语言选择提示
**So that** 我能选择熟悉的语言进行后续交互

**Acceptance Criteria:**

- [ ] 运行 `codexspec init my-project`（不带 `--lang`）时显示语言选择
- [ ] 显示 8 种预翻译语言 + "Other..." 选项
- [ ] 默认选中 English (en)
- [ ] 选择后正常初始化项目

### Story 2: 非中文用户选择其他语言

**As a** 日语/韩语/欧洲语言用户
**I want** 从预定义列表中选择我的语言
**So that** 后续的 CLI 消息和生成的文档使用我选择的语言

**Acceptance Criteria:**

- [ ] 支持选择 en, zh-CN, ja, ko, es, fr, de, pt-BR
- [ ] 选择后 config.yml 中的 `language.output` 设置正确

### Story 3: 使用非预翻译语言的用户

**As a** 使用非预翻译语言的用户（如俄语、阿拉伯语）
**I want** 能够手动输入我的语言代码
**So that** 即使没有预翻译，我也能使用偏好语言

**Acceptance Criteria:**

- [ ] 提供 "Other..." 选项
- [ ] 选择 "Other..." 后提示输入语言代码
- [ ] 输入的语言代码保存到 config.yml
- [ ] 显示提示：该语言可能没有预翻译内容

### Story 4: CI/CD 环境运行

**As a** CI/CD 系统管理员
**I want** `codexspec init` 在非 TTY 环境中正常运行
**So that** 自动化脚本不会因交互提示而卡住

**Acceptance Criteria:**

- [ ] 检测到非 TTY 环境时，自动使用默认语言 en
- [ ] 不显示任何交互提示
- [ ] 正常完成初始化流程

### Story 5: 用户明确指定语言

**As a** 熟悉 CLI 的用户
**I want** 通过 `--lang` 参数直接指定语言
**So that** 我可以跳过交互选择，快速初始化

**Acceptance Criteria:**

- [ ] 传入 `--lang zh-CN` 时跳过交互选择
- [ ] 直接使用指定的语言初始化

## Functional Requirements

### REQ-001: 参数默认值变更

- `--lang` 参数默认值从 `"en"` 改为 `None`
- 当值为 `None` 时，根据 TTY 检测决定行为

### REQ-002: TTY 环境检测

- 使用 `sys.stdin.isatty()` 检测是否为交互式终端
- 仅在 TTY 环境下显示交互选择

### REQ-003: 语言选择界面

- 使用 Rich 的 `Prompt.ask()` 显示编号选择列表
- 显示格式：

  ```
  Select output language:
    [1] English (en)
    [2] 简体中文 (zh-CN)
    [3] 日本語 (ja)
    [4] 한국어 (ko)
    [5] Español (es)
    [6] Français (fr)
    [7] Deutsch (de)
    [8] Português (Brasil) (pt-BR)
    [9] Other... (enter custom code)

  Enter choice [1]:
  ```

### REQ-004: 默认选项

- 默认选中选项 1 (English)
- 用户直接按 Enter 确认默认选项

### REQ-005: 自定义语言输入

- 选择选项 9 时，提示：`Enter language code (e.g., ru, ar, hi):`
- 使用 `normalize_locale()` 规范化输入
- 显示警告：`Note: Pre-translated content may not be available for 'xx'.`

### REQ-006: 无效输入处理

- 输入非 1-9 的数字时，提示重新输入
- 输入为空时使用默认选项

### REQ-007: 用户中断处理

- 用户按 Ctrl+C 时，显示取消消息并使用默认语言 en 继续初始化
- 不中断初始化流程

### REQ-008: 语言列表数据源

- 预定义语言列表从 `translator.py` 的 `SUPPORTED_LANGUAGES` + `en` 构建
- 语言名称使用 `i18n.get_language_name()` 获取

## Non-Functional Requirements

### NFR-001: 性能

- 语言选择界面应在 100ms 内显示
- 不增加初始化总时间的显著开销

### NFR-002: 兼容性

- 支持 macOS, Linux, Windows 终端
- Rich Prompt 在各平台表现一致

### NFR-003: 可访问性

- 提示文本清晰，使用英语（因为用户尚未选择语言）
- 选择过程完全可通过键盘完成

### NFR-004: 可维护性

- 语言列表应从现有配置动态生成，避免硬编码重复
- 新增预翻译语言时无需修改选择逻辑

## Acceptance Criteria (Test Cases)

### TC-001: TTY 环境下未指定 --lang

**Given** 终端是 TTY 环境
**And** 用户运行 `codexspec init my-project`（不带 --lang）
**When** 命令执行
**Then** 显示语言选择提示
**And** 用户可选择 1-9 任意选项

### TC-002: TTY 环境下指定 --lang

**Given** 终端是 TTY 环境
**And** 用户运行 `codexspec init my-project --lang zh-CN`
**When** 命令执行
**Then** 不显示语言选择提示
**And** 直接使用 zh-CN 初始化

### TC-003: 非 TTY 环境下运行

**Given** 终端不是 TTY（如通过管道或 CI）
**And** 用户运行 `codexspec init my-project`
**When** 命令执行
**Then** 不显示语言选择提示
**And** 使用默认语言 en 初始化

### TC-004: 选择预定义语言

**Given** 用户在语言选择界面
**When** 用户输入 `2` 并按 Enter
**Then** 语言设置为 zh-CN
**And** config.yml 中 `language.output` 为 `"zh-CN"`

### TC-005: 选择自定义语言

**Given** 用户在语言选择界面
**When** 用户输入 `9` 并按 Enter
**And** 然后输入 `ru` 并按 Enter
**Then** 语言设置为 ru
**And** 显示警告：预翻译内容可能不可用

### TC-006: 直接按 Enter 使用默认

**Given** 用户在语言选择界面
**When** 用户直接按 Enter（不输入任何内容）
**Then** 语言设置为 en（默认选项）

### TC-007: 输入无效选项

**Given** 用户在语言选择界面
**When** 用户输入 `0` 或 `abc`
**Then** 显示错误提示
**And** 重新提示选择

### TC-008: Ctrl+C 中断

**Given** 用户在语言选择界面
**When** 用户按 Ctrl+C
**Then** 显示 "Selection cancelled, using default language (en)"
**And** 继续使用 en 完成初始化

### TC-009: --here 模式下的语言选择

**Given** 终端是 TTY 环境
**And** 用户运行 `codexspec init --here`
**When** 命令执行
**Then** 显示语言选择提示
**And** 正确更新当前目录的 config.yml

## Edge Cases

### Edge Case 1: 已存在 config.yml 时更新语言

- **场景**：在已初始化的项目中再次运行 `init --here`，不传 `--lang`
- **处理**：仍显示语言选择，用户选择后调用 `update_config_language()` 更新配置

### Edge Case 2: 语言代码规范化

- **场景**：用户在 "Other..." 中输入 `ZH` 或 `chinese`
- **处理**：通过 `normalize_locale()` 规范化为 `zh-CN`

### Edge Case 3: 空字符串输入

- **场景**：用户在 "Other..." 提示中直接按 Enter
- **处理**：视为取消，回退到默认语言 en

### Edge Case 4: 非常长的语言代码

- **场景**：用户输入超长字符串
- **处理**：Rich Prompt 有内置限制，无需额外处理

## Output Examples

### 正常交互流程

```
$ codexspec init my-project

Select output language:
  [1] English (en)
  [2] 简体中文 (zh-CN)
  [3] 日本語 (ja)
  [4] 한국어 (ko)
  [5] Español (es)
  [6] Français (fr)
  [7] Deutsch (de)
  [8] Português (Brasil) (pt-BR)
  [9] Other... (enter custom code)

Enter choice [1]: 2

✓ Created: .codexspec/config.yml (language: Chinese (Simplified))
...
```

### 选择自定义语言

```
Enter choice [1]: 9
Enter language code (e.g., ru, ar, hi): ru

Note: Pre-translated content may not be available for 'ru'.
✓ Created: .codexspec/config.yml (language: Russian)
...
```

### Ctrl+C 中断

```
Enter choice [1]: ^C
Selection cancelled, using default language (en).

✓ Created: .codexspec/config.yml (language: English)
...
```

### 非 TTY 环境

```
$ echo "" | codexspec init my-project
✓ Created: .codexspec/config.yml (language: English)
...
```

## Out of Scope

- **记住上次选择**：不实现全局配置记忆用户偏好
- **系统语言检测**：不尝试从系统环境推断默认语言
- **箭头键选择**：不使用 ↑/↓ 箭头键导航（避免引入 readchar 依赖）
- **语言预览**：不展示每种语言的示例文本
- **动态下载翻译**：不支持运行时下载新的翻译包

## Implementation Notes

- 修改文件：`src/codexspec/__init__.py`
- 主要修改：`init()` 函数的 `--lang` 参数处理逻辑
- 可选：提取语言选择逻辑到独立函数 `prompt_language_selection()`
- 使用 `i18n.py` 中的 `normalize_locale()` 和 `get_language_name()`
- 使用 `translator.py` 中的 `SUPPORTED_LANGUAGES` 列表
