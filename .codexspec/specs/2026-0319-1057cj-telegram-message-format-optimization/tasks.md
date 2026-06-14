# Task Breakdown: Telegram 消息格式优化

## Overview

- **Total tasks**: 12
- **Parallelizable tasks**: 4
- **Estimated phases**: 5
- **Primary file**: `scripts/python/notify_telegram.py`
- **Test file**: `tests/scripts/python/test_notify_telegram.py`

## User Story Mapping

| Story | Tasks |
|-------|-------|
| Story 1: 工具调用可读性 | 2.1, 2.2, 3.1, 3.2 |
| Story 2: 用户询问可读性 | 4.1, 4.2 |
| Story 3: 错误通知可读性 | 5.1, 5.2 |

---

## Phase 1: 基础设施

### Task 1.1: 添加 format_code_block() 辅助函数 ✅

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py` (~L575)
- **Description**: 添加 `format_code_block(content: str, max_length: int = 500) -> str` 函数
  - 调用 `escape_html()` 转义内容
  - 支持可选的内容截断（默认 500 字符）
  - 返回 `<pre>` 标签包裹的内容
- **Dependencies**: None
- **Acceptance**: 函数存在，docstring 完整，能正确格式化内容
- **Est. Complexity**: Low

### Task 1.2: 添加 format_tool_entry() 辅助函数 ✅

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py` (~L590)
- **Description**: 添加 `format_tool_entry(name: str, details: dict) -> str` 函数
  - 调用 `format_code_block()` 格式化详情
  - 返回 `<b>{name}</b>\n<pre>{details}</pre>` 格式
  - 处理空详情情况
- **Dependencies**: Task 1.1
- **Acceptance**: 函数存在，能正确格式化工具条目
- **Est. Complexity**: Low

---

## Phase 2: TOOL_USE 消息重构

### Task 2.1: 编写 format_tool_use() 单元测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_notify_telegram.py`
- **Description**: 为 `format_tool_use()` 编写单元测试
  - TC-001: 单工具消息格式
  - TC-002: 多工具消息格式
  - TC-003: 超过 5 个工具限制
  - Edge Case 1: 空工具列表
  - Edge Case 2: 缺失字段
- **Dependencies**: Task 1.2
- **Acceptance**: 测试用例覆盖所有场景
- **Est. Complexity**: Medium

### Task 2.2: 重构 format_tool_use() 函数 ✅

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py` (L663-L746)
- **Description**: 重构 `format_tool_use()` 函数
  - 使用新的消息头部格式（添加 "📝 工具调用详情:" 标题）
  - 为每个工具调用 `format_tool_entry()`
  - 保持 5 个工具限制和 "还有 N 个工具" 提示
  - 处理空工具列表边缘情况（显示 "无工具调用信息"）
- **Dependencies**: Task 2.1, Task 1.2
- **Acceptance**: 所有 Task 2.1 测试通过
- **Est. Complexity**: Medium

---

## Phase 3: USER_QUESTION 消息优化

### Task 3.1: 编写 format_user_question() 单元测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_notify_telegram.py`
- **Description**: 为 `format_user_question()` 编写单元测试
  - TC-004: 单问题格式
  - TC-005: 多选项格式
  - 多问题场景
  - 无选项场景
- **Dependencies**: Task 1.1
- **Acceptance**: 测试用例覆盖所有场景
- **Est. Complexity**: Low

### Task 3.2: 修改 format_user_question() 函数 ✅

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py` (L605-L637)
- **Description**: 修改 `format_user_question()` 函数
  - 添加 "📝 问题详情:" 标题
  - 将问题内容、选项、多选提示放入代码块
  - 保持问题编号格式
  - 保持 header 显示
- **Dependencies**: Task 3.1, Task 1.1
- **Acceptance**: 所有 Task 3.1 测试通过
- **Est. Complexity**: Low

---

## Phase 4: ERROR_STOP 消息优化

### Task 4.1: 编写 format_error() 单元测试 [P] ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_notify_telegram.py`
- **Description**: 为 `format_error()` 编写单元测试
  - TC-006: 错误消息格式
  - 包含工具名场景
  - 不包含工具名场景
  - 长错误消息截断
- **Dependencies**: Task 1.1
- **Acceptance**: 测试用例覆盖所有场景
- **Est. Complexity**: Low

### Task 4.2: 修改 format_error() 函数 ✅

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py` (L640-L660)
- **Description**: 修改 `format_error()` 函数
  - 添加 "📝 错误详情:" 标题
  - 将错误消息和工具名放入代码块
  - Session 和 Error type 保持在代码块外
- **Dependencies**: Task 4.1, Task 1.1
- **Acceptance**: 所有 Task 4.1 测试通过
- **Est. Complexity**: Low

---

## Phase 5: 测试验证

### Task 5.1: 编写辅助函数单元测试 ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_notify_telegram.py`
- **Description**: 为辅助函数编写单元测试
  - `format_code_block()`: 正常内容、空内容、超长截断、HTML 转义
  - `format_tool_entry()`: 正常详情、空详情、特殊字符
- **Dependencies**: Task 1.1, Task 1.2
- **Acceptance**: 辅助函数测试覆盖完整
- **Est. Complexity**: Low

### Task 5.2: 编写集成测试和验证消息长度 [P] ✅

- **Type**: Testing
- **Files**: `tests/scripts/python/test_notify_telegram.py`
- **Description**:
  - TC-007: 长内容截断验证
  - NFR-001: 消息长度不超过 4096 字符
  - 端到端消息格式验证
- **Dependencies**: Task 2.2, Task 3.2, Task 4.2
- **Acceptance**: 所有集成测试通过
- **Est. Complexity**: Medium

---

## Execution Order

```
Phase 1: Task 1.1 ──► Task 1.2
            │              │
            │              ├──────────────────┐
            │              │                  │
Phase 2:    │         Task 2.1 [P] ◄─────────┤
            │              │                  │
            │         Task 2.2                │
            │                                │
Phase 3:    ├────────► Task 3.1 [P] ◄────────┤
            │              │                  │
            │         Task 3.2                │
            │                                │
Phase 4:    ├────────► Task 4.1 [P] ◄────────┘
            │              │
            │         Task 4.2
            │
Phase 5:    ├────────► Task 5.1
            │
            └────────► Task 5.2 [P]
```

---

## Checkpoints

- [ ] **Checkpoint 1**: Phase 1 完成 - 辅助函数实现并通过基本验证
- [ ] **Checkpoint 2**: Phase 2 完成 - `format_tool_use()` 测试全部通过
- [ ] **Checkpoint 3**: Phase 3 完成 - `format_user_question()` 测试全部通过
- [ ] **Checkpoint 4**: Phase 4 完成 - `format_error()` 测试全部通过
- [ ] **Checkpoint 5**: Phase 5 完成 - 所有测试通过，消息长度验证通过

---

## Test File Structure

```python
# tests/scripts/python/test_notify_telegram.py

import pytest
from scripts.python.notify_telegram import (
    format_code_block,
    format_tool_entry,
    format_tool_use,
    format_user_question,
    format_error,
)

class TestFormatCodeBlock:
    """测试 format_code_block() 辅助函数"""
    def test_normal_content(self): ...
    def test_empty_content(self): ...
    def test_truncation(self): ...
    def test_html_escape(self): ...

class TestFormatToolEntry:
    """测试 format_tool_entry() 辅助函数"""
    def test_normal_details(self): ...
    def test_empty_details(self): ...
    def test_special_characters(self): ...

class TestFormatToolUse:
    """测试 format_tool_use() 重构"""
    def test_single_tool(self): ...      # TC-001
    def test_multiple_tools(self): ...   # TC-002
    def test_exceed_limit(self): ...     # TC-003
    def test_empty_tools(self): ...      # Edge Case 1
    def test_missing_fields(self): ...   # Edge Case 2

class TestFormatUserQuestion:
    """测试 format_user_question() 优化"""
    def test_single_question(self): ...  # TC-004
    def test_multiple_options(self): ... # TC-005
    def test_multiple_questions(self): ...
    def test_no_options(self): ...

class TestFormatError:
    """测试 format_error() 优化"""
    def test_error_format(self): ...     # TC-006
    def test_with_tool_name(self): ...
    def test_without_tool_name(self): ...
    def test_long_message_truncation(self): ...

class TestIntegration:
    """集成测试"""
    def test_message_length_limit(self): ...  # NFR-001
    def test_long_content_truncation(self): ... # TC-007
```

---

## Notes

1. **TDD 调整**: 由于这是修改现有代码而非新功能开发，测试任务放在对应实现任务之前，但实现后立即验证

2. **并行任务**: 标记 `[P]` 的测试任务可以并行编写，它们共享对 `format_code_block()` 的依赖

3. **单文件修改**: 所有实现任务都在 `scripts/python/notify_telegram.py` 中完成

4. **测试文件**: 如果 `tests/scripts/python/test_notify_telegram.py` 不存在，需要创建目录结构
