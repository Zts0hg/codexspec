# Implementation Plan: Telegram 消息格式优化

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 现有项目要求 |
| Dependencies | python-dotenv | - | 已有依赖 |
| Runtime | stdin/stdout | - | 管道模式运行 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 保持函数单一职责，添加辅助函数 |
| Testing Standards | ✅ | 为新格式化逻辑编写单元测试 |
| Documentation | ✅ | 函数添加 docstring，包含示例 |
| Architecture | ✅ | 保持现有模块结构，仅修改格式化函数 |
| Performance | ✅ | 格式化操作简单，无性能风险 |
| Security | ✅ | 保持 HTML 转义逻辑 |

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     notify_telegram.py                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌────────┐  ┌──────────────┐                  │
│  │ Config  │  │ Logger │  │ RetryHandler │                  │
│  └─────────┘  └────────┘  └──────────────┘                  │
├─────────────────────────────────────────────────────────────┤
│                     Message Formatters                       │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  format_code_block()     [NEW - 辅助函数]            │    │
│  │  format_tool_entry()     [NEW - 辅助函数]            │    │
│  │  format_tool_use()       [REFACTOR]                  │    │
│  │  format_user_question()  [MODIFY]                    │    │
│  │  format_error()          [MODIFY]                    │    │
│  │  format_task_complete()  [KEEP AS IS]                │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐                                       │
│  │ send_telegram_msg│                                       │
│  └──────────────────┘                                       │
│  ┌──────────────────┐                                       │
│  │ main() / stdin   │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

```
scripts/python/
└── notify_telegram.py    # 单文件脚本，所有修改在此文件
```

**修改区域：** 消息格式化函数区（L575-L746）

## 5. Module Dependency Graph

```
┌────────────────────┐
│  format_tool_use   │
└─────────┬──────────┘
          │ depends on
          ▼
┌────────────────────┐     ┌────────────────────┐
│ format_tool_entry  │────▶│ format_code_block  │
│     [NEW]          │     │      [NEW]         │
└────────────────────┘     └─────────┬──────────┘
                                     │ depends on
                                     ▼
                           ┌────────────────────┐
                           │   escape_html      │
                           │   (existing)       │
                           └────────────────────┘

┌────────────────────┐     ┌────────────────────┐
│format_user_question│────▶│ format_code_block  │
│     [MODIFY]       │     └────────────────────┘
└────────────────────┘

┌────────────────────┐     ┌────────────────────┐
│   format_error     │────▶│ format_code_block  │
│     [MODIFY]       │     └────────────────────┘
└────────────────────┘
```

## 6. Module Specifications

### Module: format_code_block (NEW)

- **Responsibility**: 将文本内容包装为 Telegram `<pre>` 代码块
- **Dependencies**: `escape_html()`
- **Interface**: `format_code_block(content: str) -> str`
- **Files**: `notify_telegram.py` (L575 附近插入)

### Module: format_tool_entry (NEW)

- **Responsibility**: 格式化单个工具条目（标题 + 代码块）
- **Dependencies**: `format_code_block()`, `escape_html()`
- **Interface**: `format_tool_entry(name: str, details: dict) -> str`
- **Files**: `notify_telegram.py` (L575 附近插入)

### Module: format_tool_use (REFACTOR)

- **Responsibility**: 格式化工具调用通知消息
- **Dependencies**: `format_tool_entry()`
- **Interface**: `format_tool_use(data: dict) -> str` (签名不变)
- **Files**: `notify_telegram.py` (L663-L746 重构)

### Module: format_user_question (MODIFY)

- **Responsibility**: 格式化用户询问通知消息
- **Dependencies**: `format_code_block()`, `escape_html()`
- **Interface**: `format_user_question(data: dict) -> str` (签名不变)
- **Files**: `notify_telegram.py` (L605-L637 修改)

### Module: format_error (MODIFY)

- **Responsibility**: 格式化错误通知消息
- **Dependencies**: `format_code_block()`, `escape_html()`
- **Interface**: `format_error(data: dict) -> str` (签名不变)
- **Files**: `notify_telegram.py` (L640-L660 修改)

## 7. Data Models

N/A - 无数据模型变更，仅修改格式化输出

## 8. API Contracts

N/A - 内部脚本，无外部 API

## 9. Implementation Phases

### Phase 1: 基础设施

- [ ] 添加 `format_code_block(content: str, max_length: int = 500) -> str` 辅助函数
  - 自动调用 `escape_html()` 转义内容
  - 支持可选的内容截断
- [ ] 添加 `format_tool_entry(name: str, details: dict) -> str` 辅助函数
  - 调用 `format_code_block()` 格式化详情
  - 返回 `<b>{name}</b>\n<pre>{details}</pre>` 格式

### Phase 2: TOOL_USE 消息重构

- [ ] 重构 `format_tool_use()` 函数
  - 使用新的消息头部格式（添加 "📝 工具调用详情:" 标题）
  - 为每个工具调用 `format_tool_entry()`
  - 保持 5 个工具限制和 "还有 N 个工具" 提示
  - 处理空工具列表边缘情况

### Phase 3: USER_QUESTION 消息优化

- [ ] 修改 `format_user_question()` 函数
  - 添加 "📝 问题详情:" 标题
  - 将问题内容、选项、多选提示放入代码块
  - 保持问题编号格式

### Phase 4: ERROR_STOP 消息优化

- [ ] 修改 `format_error()` 函数
  - 添加 "📝 错误详情:" 标题
  - 将错误消息和工具名放入代码块
  - Session 和 Error type 保持在代码块外

### Phase 5: 测试验证

- [ ] 创建/更新单元测试
  - 测试 `format_code_block()` 各种输入
  - 测试 `format_tool_entry()` 格式化输出
  - 测试 `format_tool_use()` 多工具场景
  - 测试 `format_user_question()` 多选项场景
  - 测试 `format_error()` 各种错误类型
- [ ] 手动测试 Telegram 渲染效果

## 10. Technical Decisions

### Decision 1: 辅助函数设计

- **Choice**: 添加两个新的辅助函数 `format_code_block()` 和 `format_tool_entry()`
- **Rationale**:
  - 遵循单一职责原则
  - 代码复用，减少重复
  - 易于测试和维护
- **Alternatives**: 直接在各格式化函数中内联代码
- **Trade-offs**: 增加少量函数，但提升可维护性

### Decision 2: 代码块内容截断策略

- **Choice**: 在 `format_code_block()` 中支持可选截断，默认 500 字符
- **Rationale**:
  - 避免单个代码块过长
  - 保持与现有 `format_task_complete()` 截断策略一致
- **Alternatives**: 不截断，让调用者处理
- **Trade-offs**: 增加函数复杂度，但统一截断逻辑

### Decision 3: 空工具列表处理

- **Choice**: 返回包含 "无工具调用信息" 的消息
- **Rationale**: 保持消息格式一致性，而非返回空消息
- **Alternatives**: 跳过通知（返回 None）
- **Trade-offs**: 发送一条信息性消息 vs 完全静默

### Decision 4: 格式化函数签名

- **Choice**: 保持现有函数签名不变
- **Rationale**: 向后兼容，不影响 `process_event()` 和 `main()` 的调用
- **Alternatives**: 修改签名以支持更多配置
- **Trade-offs**: 限制灵活性，但保持稳定性

## 11. Code Reference

### format_code_block 实现

```python
def format_code_block(content: str, max_length: int = 500) -> str:
    """将内容格式化为 Telegram 代码块

    Args:
        content: 要格式化的内容
        max_length: 最大长度，超过则截断。设为 0 禁用截断

    Returns:
        格式化后的 <pre> 标签内容
    """
    if max_length > 0 and len(content) > max_length:
        content = content[:max_length] + "\n... (已截断)"

    return f"<pre>{escape_html(content)}</pre>"
```

### format_tool_entry 实现

```python
def format_tool_entry(name: str, details: dict) -> str:
    """格式化单个工具条目

    Args:
        name: 工具名称
        details: 工具详情字典

    Returns:
        格式化后的工具条目（标题 + 代码块）
    """
    detail_lines = [f"{k}: {v}" for k, v in details.items() if v]
    content = "\n".join(detail_lines) if detail_lines else "无详情"

    return f"<b>{escape_html(name)}</b>\n{format_code_block(content)}"
```

### format_tool_use 重构后结构

```python
def format_tool_use(data: dict) -> str:
    """格式化工具调用通知"""
    session_id = data.get("session_id", "unknown")[:8]
    tools = data.get("tools", [])

    lines = [
        "🔧 <b>Claude Code 工具调用</b>",
        "",
        f"📌 Session: <code>{session_id}</code>",
        "",
        "📝 工具调用详情:",
    ]

    # 处理空工具列表
    if not tools:
        lines.append("\n无工具调用信息")
        return "\n".join(lines)

    # 格式化每个工具
    for tool in tools[:5]:
        name = tool.get("name", "unknown")
        details = tool.get("details", {})
        # 提取工具特定详情...
        lines.append("")
        lines.append(format_tool_entry(name, extracted_details))

    # 超出限制提示
    if len(tools) > 5:
        lines.append(f"\n• ... 还有 {len(tools) - 5} 个工具")

    return "\n".join(lines)
```

## 12. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| 消息超长超过 4096 字符 | Medium | High | 添加消息长度检查，必要时截断 |
| HTML 转义遗漏 | Low | Medium | 统一使用 `format_code_block()` |
| Telegram 客户端渲染差异 | Low | Low | 使用标准 HTML 标签 |

## 13. Files to Modify

| File | Action | Lines | Description |
|------|--------|-------|-------------|
| `scripts/python/notify_telegram.py` | ADD | ~L575 | `format_code_block()` |
| `scripts/python/notify_telegram.py` | ADD | ~L590 | `format_tool_entry()` |
| `scripts/python/notify_telegram.py` | REFACTOR | L663-L746 | `format_tool_use()` |
| `scripts/python/notify_telegram.py` | MODIFY | L605-L637 | `format_user_question()` |
| `scripts/python/notify_telegram.py` | MODIFY | L640-L660 | `format_error()` |
| `tests/test_notify_telegram.py` | ADD/UPDATE | - | 单元测试 |
