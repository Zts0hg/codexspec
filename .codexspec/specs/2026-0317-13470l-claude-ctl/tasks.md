# Task Breakdown: claude-ctl

## Overview

- **Total tasks**: 16
- **Parallelizable tasks**: 6
- **Estimated phases**: 5
- **Primary files**: 2 (`claude_ctl.py`, `test_claude_ctl.py`)

## User Story Mapping

| User Story | Tasks |
|------------|-------|
| US-001: 继续对话 | 1.1, 1.2, 2.1-2.4, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2 |
| US-002: 回答问题/选择方案 | 1.1, 1.2, 2.1-2.4, 3.3, 3.4, 4.1, 4.2, 5.1, 5.2 |
| US-003: 权限控制 | 1.1, 1.2, 2.1-2.4, 3.5, 3.6, 4.1, 4.2, 5.1, 5.2 |

## Phase 1: Foundation

### Task 1.1: 创建主文件结构

- **Type**: Setup
- **Files**: `scripts/python/claude_ctl.py`
- **Description**: 创建主文件，添加 shebang、文件头注释、版本号管理和基本 main() 入口
- **Acceptance Criteria**:
  - 文件存在且可执行
  - 包含 shebang `#!/usr/bin/env python3`
  - 包含版本号管理代码（importlib.metadata + fallback）
- **Dependencies**: None
- **Est. Complexity**: Low

### Task 1.2: 创建测试文件结构 [P]

- **Type**: Setup
- **Files**: `scripts/python/tests/test_claude_ctl.py`
- **Description**: 创建测试文件，添加基本测试框架和 fixtures
- **Acceptance Criteria**:
  - 测试文件存在
  - 包含 pytest 导入和基本 fixtures
  - 包含 mock tmux 命令的 fixture
- **Dependencies**: None
- **Est. Complexity**: Low

## Phase 2: Core Implementation (TDD)

### Task 2.1: 编写 CLI 参数解析测试

- **Type**: Testing
- **Files**: `scripts/python/tests/test_claude_ctl.py`
- **Description**: 编写 argparse 参数解析的单元测试
- **Acceptance Criteria**:
  - 测试所有参数正确解析
  - 测试必需参数缺失情况
  - 测试互斥参数冲突
- **Dependencies**: Task 1.2
- **Est. Complexity**: Low

### Task 2.2: 实现 CLI 参数解析

- **Type**: Implementation
- **Files**: `scripts/python/claude_ctl.py`
- **Description**: 实现 `parse_args()` 函数，包含所有命令行参数定义
- **Acceptance Criteria**:
  - 通过 Task 2.1 的所有测试
  - 支持 --session, --message, --select, --approve, --reject, --version, --list-sessions, --help
  - 实现互斥性验证
- **Dependencies**: Task 2.1
- **Est. Complexity**: Medium

### Task 2.3: 编写 TmuxClient 测试 [P]

- **Type**: Testing
- **Files**: `scripts/python/tests/test_claude_ctl.py`
- **Description**: 编写 TmuxClient 类的单元测试（使用 mock）
- **Acceptance Criteria**:
  - 测试 `session_exists()` 成功/失败场景
  - 测试 `list_sessions()` 返回会话列表
  - 测试 `send_keys()` 和 `send_enter()`
  - 测试 tmux 命令失败时的错误处理
- **Dependencies**: Task 1.2
- **Est. Complexity**: Medium

### Task 2.4: 实现 TmuxClient 类

- **Type**: Implementation
- **Files**: `scripts/python/claude_ctl.py`
- **Description**: 实现 `TmuxClient` 类，封装所有 tmux 命令调用
- **Acceptance Criteria**:
  - 通过 Task 2.3 的所有测试
  - 实现 `session_exists()`, `list_sessions()`, `send_keys()`, `send_enter()`
  - 使用 subprocess 调用 tmux
  - 正确处理命令失败情况
- **Dependencies**: Task 2.3
- **Est. Complexity**: Medium

## Phase 3: Action Handlers (TDD)

### Task 3.1: 编写 handle_message 测试 [P]

- **Type**: Testing
- **Files**: `scripts/python/tests/test_claude_ctl.py`
- **Description**: 编写 `handle_message()` 函数的单元测试
- **Acceptance Criteria**:
  - 测试正常消息发送
  - 测试包含空格的消息
  - 测试包含特殊字符的消息
  - 测试空消息（允许）
  - 测试 session 不存在情况
- **Dependencies**: Task 2.4
- **Est. Complexity**: Low

### Task 3.2: 实现 handle_message

- **Type**: Implementation
- **Files**: `scripts/python/claude_ctl.py`
- **Description**: 实现 `handle_message()` 函数
- **Acceptance Criteria**:
  - 通过 Task 3.1 的所有测试
  - 检查 session 存在性
  - 使用 send-keys -l 发送消息
  - 发送 Enter 键提交
  - 返回正确的 exit code
- **Dependencies**: Task 3.1
- **Est. Complexity**: Low

### Task 3.3: 编写 handle_select 测试 [P]

- **Type**: Testing
- **Files**: `scripts/python/tests/test_claude_ctl.py`
- **Description**: 编写 `handle_select()` 函数的单元测试
- **Acceptance Criteria**:
  - 测试单选场景
  - 测试多选场景（逗号分隔）
  - 测试选项包含首尾空格
  - 测试空选项（拒绝）
  - 测试重复选项（按原样发送）
- **Dependencies**: Task 2.4
- **Est. Complexity**: Medium

### Task 3.4: 实现 handle_select

- **Type**: Implementation
- **Files**: `scripts/python/claude_ctl.py`
- **Description**: 实现 `handle_select()` 函数
- **Acceptance Criteria**:
  - 通过 Task 3.3 的所有测试
  - 解析逗号分隔的选项
  - 去除每个选项的首尾空格
  - 依次发送每个选项 + Enter
  - 拒绝空选项
- **Dependencies**: Task 3.3
- **Est. Complexity**: Medium

### Task 3.5: 编写 handle_approve/reject 测试 [P]

- **Type**: Testing
- **Files**: `scripts/python/tests/test_claude_ctl.py`
- **Description**: 编写 `handle_approve()` 和 `handle_reject()` 函数的单元测试
- **Acceptance Criteria**:
  - 测试批准操作（发送 "Y"）
  - 测试拒绝操作（发送 "n"）
  - 测试 session 不存在情况
- **Dependencies**: Task 2.4
- **Est. Complexity**: Low

### Task 3.6: 实现 handle_approve 和 handle_reject

- **Type**: Implementation
- **Files**: `scripts/python/claude_ctl.py`
- **Description**: 实现 `handle_approve()` 和 `handle_reject()` 函数
- **Acceptance Criteria**:
  - 通过 Task 3.5 的所有测试
  - 批准操作发送 "Y" + Enter
  - 拒绝操作发送 "n" + Enter
  - 返回正确的 exit code
- **Dependencies**: Task 3.5
- **Est. Complexity**: Low

### Task 3.7: 编写 handle_list_sessions 测试 [P]

- **Type**: Testing
- **Files**: `scripts/python/tests/test_claude_ctl.py`
- **Description**: 编写 `handle_list_sessions()` 函数的单元测试
- **Acceptance Criteria**:
  - 测试成功列出会话
  - 测试无会话时的输出
  - 测试 tmux 不可用时的错误处理
- **Dependencies**: Task 2.4
- **Est. Complexity**: Low

### Task 3.8: 实现 handle_list_sessions

- **Type**: Implementation
- **Files**: `scripts/python/claude_ctl.py`
- **Description**: 实现 `handle_list_sessions()` 函数
- **Acceptance Criteria**:
  - 通过 Task 3.7 的所有测试
  - 调用 TmuxClient.list_sessions()
  - 每行输出一个会话名称
  - 返回正确的 exit code
- **Dependencies**: Task 3.7
- **Est. Complexity**: Low

## Phase 4: Integration

### Task 4.1: 实现 main() 控制器

- **Type**: Implementation
- **Files**: `scripts/python/claude_ctl.py`
- **Description**: 实现 `main()` 函数，整合所有组件
- **Acceptance Criteria**:
  - 解析命令行参数
  - 根据参数调用对应的 handler
  - 正确处理 exit code
  - 调用 `sys.exit()` 返回状态码
- **Dependencies**: Task 2.2, Task 3.2, Task 3.4, Task 3.6, Task 3.8
- **Est. Complexity**: Medium

### Task 4.2: 编写集成测试

- **Type**: Testing
- **Files**: `scripts/python/tests/test_claude_ctl.py`
- **Description**: 编写端到端集成测试（使用 mock tmux）
- **Acceptance Criteria**:
  - 测试完整命令执行流程
  - 测试所有 11 个测试用例（TC-001 到 TC-011）
  - 验证 exit code 正确性
  - 验证输出格式正确性
- **Dependencies**: Task 4.1
- **Est. Complexity**: Medium

## Phase 5: Testing & Documentation

### Task 5.1: 边界场景测试

- **Type**: Testing
- **Files**: `scripts/python/tests/test_claude_ctl.py`
- **Description**: 补充边界场景测试用例
- **Acceptance Criteria**:
  - 覆盖所有 6 个边界场景（EC-001 到 EC-006）
  - 确保所有测试通过
- **Dependencies**: Task 4.2
- **Est. Complexity**: Low

### Task 5.2: 代码质量检查 [P]

- **Type**: Quality
- **Files**: `scripts/python/claude_ctl.py`, `scripts/python/tests/test_claude_ctl.py`
- **Description**: 运行 ruff 检查并修复问题
- **Acceptance Criteria**:
  - `ruff check` 无错误
  - `ruff format` 格式化完成
  - 代码符合 PEP 8 规范
- **Dependencies**: Task 4.2
- **Est. Complexity**: Low

## Execution Order

```
Phase 1: Task 1.1 ─────────────────────────────┐
                                               │
        Task 1.2 [P] ◄─────────────────────────┤
                                               │
Phase 2: Task 2.1 ──► Task 2.2                 │
                                               │
        Task 2.3 [P] ──► Task 2.4              │
                                     │         │
Phase 3: ┌────────────────────────────┼─────────┤
         │                │           │         │
    Task 3.1 [P]    Task 3.3 [P]  Task 3.5 [P] │
         │                │           │         │
    Task 3.2        Task 3.4     Task 3.6      │
         │                │           │         │
    Task 3.7 [P] ◄────────┴───────────┘         │
         │                                     │
    Task 3.8                                   │
         │                                     │
Phase 4: Task 4.1 ◄─────────────────────────────┘
         │
    Task 4.2
         │
Phase 5: ┌───────────────┴───────────────┐
         │                               │
    Task 5.1                        Task 5.2 [P]
```

## Checkpoints

- [ ] **Checkpoint 1** (After Phase 1): 验证文件结构正确，测试框架可用
- [ ] **Checkpoint 2** (After Phase 2): 验证 CLI 解析和 TmuxClient 测试全部通过
- [ ] **Checkpoint 3** (After Phase 3): 验证所有 handler 测试通过
- [ ] **Checkpoint 4** (After Phase 4): 验证集成测试通过，功能完整
- [ ] **Checkpoint 5** (After Phase 5): 验证代码质量检查通过

## Test Coverage Requirements

| Component | Test File | Min Coverage |
|-----------|-----------|--------------|
| CLI Parser | test_claude_ctl.py | 100% |
| TmuxClient | test_claude_ctl.py | 100% |
| Action Handlers | test_claude_ctl.py | 100% |
| main() | test_claude_ctl.py | 100% |

## Exit Code Summary

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Session not found |
| 2 | Invalid arguments |
| 3 | tmux command execution failed |

---

*Generated: 2026-03-17*
