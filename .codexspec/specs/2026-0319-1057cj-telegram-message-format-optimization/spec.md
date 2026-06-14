# Feature: Telegram 消息格式优化

## Overview

优化 `scripts/python/notify_telegram.py` 中的消息格式，使用 Markdown 代码块（`<pre>` 标签）来组织详情内容，提升消息的可读性和视觉区分度。

## Goals

- 统一所有消息类型的格式风格
- 使用代码块组织结构化内容，提升可读性
- 保持与任务完成消息（TASK_COMPLETE）一致的设计语言
- 确保消息在 Telegram 客户端中显示清晰整洁

## User Stories

### Story 1: 工具调用消息可读性优化

**As a** Claude Code 用户
**I want** 收到格式清晰的工具调用通知
**So that** 我能快速了解 Claude 执行了哪些操作

**Acceptance Criteria:**

- [ ] 每个工具的详情使用独立的代码块展示
- [ ] 工具名称作为代码块标题，清晰可辨
- [ ] 最多显示 5 个工具，超出部分显示数量提示
- [ ] 长内容自动截断，不影响整体布局

### Story 2: 用户询问消息格式优化

**As a** Claude Code 用户
**I want** 收到格式清晰的询问通知
**So that** 我能快速理解问题并做出决策

**Acceptance Criteria:**

- [ ] 问题内容使用代码块展示
- [ ] 选项列表格式清晰，易于阅读
- [ ] 多选提示明确可见

### Story 3: 错误通知消息格式优化

**As a** Claude Code 用户
**I want** 收到格式清晰的错误通知
**So that** 我能快速定位问题原因

**Acceptance Criteria:**

- [ ] 错误消息使用代码块展示
- [ ] 错误类型、消息、工具名清晰区分
- [ ] 长错误消息自动截断

## Functional Requirements

### REQ-001: TOOL_USE 消息格式重构

将工具调用消息从列表格式改为代码块格式：

**当前格式：**

```
• Bash: cmd: git commit -m "..." | desc: Execute git commit
• Read: file: claude_monitor.py | lines: 1-50
```

**目标格式：**

```
<b>Bash</b>
<pre>cmd: git commit -m "..."
desc: Execute git commit with generated message</pre>

<b>Read</b>
<pre>file: claude_monitor.py
lines: 1-50</pre>
```

### REQ-002: USER_QUESTION 消息格式优化

优化用户询问消息，使用代码块组织问题详情：

- 每个问题使用独立代码块
- 选项列表在代码块内使用结构化格式
- 保留 header、multi_select 等元信息

### REQ-003: ERROR_STOP 消息格式优化

优化错误通知消息，使用代码块组织错误详情：

- 错误消息使用代码块包裹
- 错误类型、消息、工具名分行显示
- 保留 Session 和错误类型在代码块外

### REQ-004: TASK_COMPLETE 消息保持不变

任务完成消息已符合预期格式，保持现有实现：

```
✅ Claude Code 任务完成

📌 Session: b477a17c
🔄 Stop reason: end_turn

📝 输出:
<pre>...</pre>
```

### REQ-005: 内容截断策略

保持现有截断逻辑：

- 工具列表：最多显示 5 个工具
- 命令/输出：超长内容截断并添加提示
- 错误消息：截断至合理长度

## Non-Functional Requirements

### NFR-001: 消息长度限制

- 单条消息总长度不超过 Telegram 限制（4096 字符）
- 超长消息应优先保留关键信息

### NFR-002: 渲染兼容性

- 使用 Telegram 支持的 HTML 标签（`<b>`, `<pre>`, `<code>`）
- 避免使用不支持的 Markdown 语法
- 确保在 Telegram 各客户端（iOS、Android、Desktop）显示一致

### NFR-003: 可维护性

- 格式化函数保持单一职责
- 代码结构清晰，易于扩展新的消息类型

## Acceptance Criteria (Test Cases)

### TC-001: TOOL_USE 单工具消息格式

**输入：** 单个 Bash 工具调用事件

**预期输出：**

```
🔧 Claude Code 工具调用

📌 Session: b477a17c

📝 工具调用详情:

<b>Bash</b>
<pre>cmd: git status
desc: Show working tree status</pre>
```

### TC-002: TOOL_USE 多工具消息格式

**输入：** 3 个工具调用事件（Bash, Read, Write）

**预期输出：** 每个工具一个代码块，格式正确

### TC-003: TOOL_USE 超过限制

**输入：** 7 个工具调用事件

**预期输出：** 显示前 5 个工具 + "还有 2 个工具" 提示

### TC-004: USER_QUESTION 单问题格式

**输入：** 单个问题的用户询问事件

**预期输出：** 问题内容在代码块中，格式清晰

### TC-005: USER_QUESTION 多选项格式

**输入：** 包含 4 个选项的用户询问事件

**预期输出：** 选项列表格式清晰，每个选项占一行

### TC-006: ERROR_STOP 消息格式

**输入：** 错误停止事件

**预期输出：** 错误消息在代码块中，类型和工具名清晰

### TC-007: 长内容截断

**输入：** 超长命令（>500 字符）

**预期输出：** 内容截断，末尾显示 "... (已截断)"

## Edge Cases

### Edge Case 1: 空工具列表

- **场景：** 收到 TOOL_USE 事件但 tools 数组为空
- **处理：** 显示 "无工具调用信息" 或跳过通知

### Edge Case 2: 缺失字段

- **场景：** 工具详情中某些字段缺失
- **处理：** 跳过缺失字段，显示已有字段

### Edge Case 3: 特殊字符转义

- **场景：** 命令包含 `<`, `>`, `&` 等 HTML 特殊字符
- **处理：** 使用 `escape_html()` 函数转义

### Edge Case 4: 超长消息

- **场景：** 消息总长度接近 4096 字符限制
- **处理：** 优先保留前面的工具信息，截断后续内容

## Output Examples

### TOOL_USE 消息示例

```
🔧 Claude Code 工具调用

📌 Session: b477a17c

📝 工具调用详情:

<b>Bash</b>
<pre>cmd: git commit -m "feat(monitor): enhance tool use"
desc: Execute git commit with generated message</pre>

<b>Read</b>
<pre>file: claude_monitor.py
lines: 1-100</pre>

<b>Edit</b>
<pre>file: notify_telegram.py
old: format_tool_use(data: dict) -&gt; str:</pre>

• ... 还有 2 个工具
```

### USER_QUESTION 消息示例

```
❓ Claude Code 需要你的输入

📌 Session: b477a17c

📝 问题详情:

<b>问题 1: 选择认证方式</b>
<pre>📋 Auth method

选项:
  • OAuth - 使用 OAuth 2.0 授权
  • JWT - 使用 JWT Token 认证
  • API Key - 使用 API 密钥

☑️ 可多选</pre>
```

### ERROR_STOP 消息示例

```
❌ Claude Code 执行出错

📌 Session: b477a17c
🔴 Error type: tool_error

📝 错误详情:
<pre>Message: File not found: config.yml
Tool: Read</pre>
```

## Out of Scope

- 消息分页（单条消息超长时拆分为多条）
- 自定义消息模板
- 新增消息类型
- 修改 JSON 输入格式
- 日志系统变更
- 重试机制变更

## Implementation Notes

### 需要修改的函数

1. `format_tool_use(data: dict) -> str` - 主要重构
2. `format_user_question(data: dict) -> str` - 格式优化
3. `format_error(data: dict) -> str` - 格式优化

### 代码块实现

使用 Telegram HTML 格式的 `<pre>` 标签：

```python
def format_code_block(content: str) -> str:
    """格式化代码块"""
    escaped = escape_html(content)
    return f"<pre>{escaped}</pre>"
```

### 格式化模式

```python
def format_tool_entry(name: str, details: dict) -> str:
    """格式化单个工具条目"""
    lines = [f"<b>{name}</b>"]

    detail_lines = []
    for key, value in details.items():
        detail_lines.append(f"{key}: {value}")

    content = "\n".join(detail_lines)
    lines.append(f"<pre>{escape_html(content)}</pre>")

    return "\n".join(lines)
```
