# Task Breakdown: Claude Code Session 状态检测增强

## Overview

- **Total tasks**: 18
- **Parallelizable tasks**: 6
- **Estimated phases**: 5

## User Story Mapping

| User Story | Tasks |
|------------|-------|
| US-001: 用户询问状态检测 | 1.1-1.4, 2.1-2.4, 4.1-4.3 |
| US-002: 出错停止状态检测 | 1.1-1.4, 2.1-2.4, 4.1-4.3 |
| US-003: 状态监控集成 | 4.1-4.4, 5.1-5.4 |

## Phase 1: Foundation - 数据模型

### Task 1.1: 添加 SessionStatus 枚举类

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 添加 `SessionStatus` 枚举类，定义所有状态类型（STREAMING, TOOL_USE, USER_QUESTION, ERROR_STOP, TASK_COMPLETE, IDLE）
- **Dependencies**: None
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 枚举类包含所有 6 种状态
  - [ ] 每个状态有清晰的注释

### Task 1.2: 添加 QuestionOption dataclass [P]

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 添加 `QuestionOption` dataclass，包含 `label` 和 `description` 字段
- **Dependencies**: None
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 包含 `label: str` 和 `description: str` 字段

### Task 1.3: 添加 QuestionInfo dataclass [P]

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 添加 `QuestionInfo` dataclass，存储用户询问的详细信息
- **Dependencies**: Task 1.2
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 包含 `question`, `header`, `options`, `multi_select` 字段
  - [ ] `multi_select` 有默认值 `False`

### Task 1.4: 添加 ErrorInfo dataclass [P]

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 添加 `ErrorInfo` dataclass，存储错误信息
- **Dependencies**: None
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 包含 `error_type`, `message`, `tool_name`, `tool_input` 字段
  - [ ] 可选字段有正确的默认值

### Task 1.5: 扩展 SessionState dataclass

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 扩展现有的 `SessionState` dataclass，添加新字段
- **Dependencies**: Task 1.1, Task 1.3, Task 1.4
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 添加 `status: SessionStatus` 字段，默认 IDLE
  - [ ] 添加 `questions: list[QuestionInfo]` 字段
  - [ ] 添加 `error_info: Optional[ErrorInfo]` 字段
  - [ ] 保持向后兼容

## Phase 2: Core Implementation - 状态检测器 (TDD)

### Task 2.1: 编写 StateDetector 单元测试

- **Type**: Testing
- **Files**: `tests/scripts/python/test_state_detector.py`
- **Description**: 为 StateDetector 类编写全面的单元测试
- **Dependencies**: Phase 1 完成
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - [ ] 测试 STREAMING 状态检测（stop_reason=null）
  - [ ] 测试 USER_QUESTION 状态检测（AskUserQuestion）
  - [ ] 测试 ERROR_STOP 状态检测
  - [ ] 测试 TASK_COMPLETE 状态检测
  - [ ] 测试 TOOL_USE 状态检测
  - [ ] 测试边界情况

### Task 2.2: 实现 StateDetector 类

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 实现 StateDetector 类，包含状态检测逻辑
- **Dependencies**: Task 2.1
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - [ ] 实现 `detect()` 静态方法
  - [ ] 实现 `_extract_question()` 私有方法
  - [ ] 实现 `_extract_error()` 私有方法
  - [ ] 所有测试通过

### Task 2.3: 编写 OutputFormatter 单元测试 [P]

- **Type**: Testing
- **Files**: `tests/scripts/python/test_output_formatter.py`
- **Description**: 为 OutputFormatter 类编写单元测试
- **Dependencies**: Phase 1 完成
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - [ ] 测试 `format_user_question()` 输出格式
  - [ ] 测试 `format_error_stop()` 输出格式
  - [ ] 测试 `format_task_complete()` 输出格式（向后兼容）
  - [ ] 验证输出符合 spec 中的 Output Examples

### Task 2.4: 实现 OutputFormatter 类

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 实现 OutputFormatter 类，包含输出格式化逻辑
- **Dependencies**: Task 2.3
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - [ ] 实现 `format_user_question()` 方法
  - [ ] 实现 `format_error_stop()` 方法
  - [ ] 实现 `format_task_complete()` 方法（重构现有代码）
  - [ ] 所有测试通过

## Phase 3: Integration - 主监控类扩展

### Task 3.1: 编写 ClaudeSessionMonitor 扩展单元测试

- **Type**: Testing
- **Files**: `tests/scripts/python/test_monitor_callbacks.py`
- **Description**: 为 ClaudeSessionMonitor 的新回调功能编写单元测试
- **Dependencies**: Phase 2 完成
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - [ ] 测试 `on_user_question` 回调触发
  - [ ] 测试 `on_error_stop` 回调触发
  - [ ] 测试状态变化检测逻辑
  - [ ] 测试连续多个询问的边界情况

### Task 3.2: 扩展 ClaudeSessionMonitor 初始化

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 在 ClaudeSessionMonitor.**init** 中添加新的回调参数
- **Dependencies**: Task 3.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 添加 `on_user_question` 参数
  - [ ] 添加 `on_error_stop` 参数
  - [ ] 保持 `on_complete` 参数向后兼容

### Task 3.3: 实现状态变化检测逻辑

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 修改 `_update_session_state()` 使用 StateDetector
- **Dependencies**: Task 3.2
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - [ ] 集成 StateDetector.detect() 方法
  - [ ] 正确检测 USER_QUESTION 状态
  - [ ] 正确检测 ERROR_STOP 状态
  - [ ] 保持现有功能正常

### Task 3.4: 实现回调触发方法

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 实现 `_on_user_question()` 和 `_on_error_stop()` 回调方法
- **Dependencies**: Task 3.3
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - [ ] 实现 `_on_user_question()` 方法
  - [ ] 实现 `_on_error_stop()` 方法
  - [ ] 使用 OutputFormatter 格式化输出
  - [ ] 正确调用用户注册的回调函数

## Phase 4: Interface Layer - CLI 更新

### Task 4.1: 更新 CLI 参数支持新回调

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 更新 main() 函数，支持新的回调参数传递
- **Dependencies**: Phase 3 完成
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] `--json` 模式正确输出新状态类型
  - [ ] 回调参数正确传递给 ClaudeSessionMonitor

### Task 4.2: 更新 JSON 输出格式

- **Type**: Implementation
- **Files**: `scripts/python/claude_monitor.py`
- **Description**: 更新 JSON 输出回调，支持新状态类型
- **Dependencies**: Task 4.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] USER_QUESTION 状态输出包含 questions 字段
  - [ ] ERROR_STOP 状态输出包含 error_info 字段
  - [ ] 输出格式易于解析

## Phase 5: Testing & Documentation

### Task 5.1: 准备 Mock 数据文件

- **Type**: Testing
- **Files**: `tests/scripts/python/fixtures/`
- **Description**: 创建用于测试的 mock session 文件
- **Dependencies**: None
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] `mock_user_question.jsonl` - AskUserQuestion 场景
  - [ ] `mock_task_complete.jsonl` - 正常完成场景
  - [ ] `mock_error_stop.jsonl` - 出错停止场景
  - [ ] `mock_tool_error_continue.jsonl` - 工具错误继续场景
  - [ ] `mock_multiple_questions.jsonl` - 多询问场景

### Task 5.2: 编写集成测试

- **Type**: Testing
- **Files**: `tests/scripts/python/test_monitor_integration.py`
- **Description**: 编写端到端集成测试，使用 mock 数据验证完整流程
- **Dependencies**: Task 5.1, Phase 4 完成
- **Est. Complexity**: High
- **Acceptance Criteria**:
  - [ ] 测试 TC-001: 用户询问检测
  - [ ] 测试 TC-002: 正常任务完成检测
  - [ ] 测试 TC-003: 出错停止检测
  - [ ] 测试 TC-004: 工具错误但继续执行
  - [ ] 测试 TC-005: 回调函数触发

### Task 5.3: 更新 README 文档 [P]

- **Type**: Documentation
- **Files**: `scripts/python/README.md`
- **Description**: 更新 README，添加新状态的文档说明
- **Dependencies**: Phase 4 完成
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [ ] 添加 USER_QUESTION 输出示例
  - [ ] 添加 ERROR_STOP 输出示例
  - [ ] 更新状态检测逻辑说明
  - [ ] 更新使用示例

### Task 5.4: 运行完整测试并验证覆盖率 ✅

- **Type**: Testing
- **Files**: N/A (运行命令)
- **Description**: 运行所有测试， 验证覆盖率达标
- **Dependencies**: Task 5.2
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - [x] 所有测试通过
  - [x] 核心逻辑覆盖率 > 90%
  - [x] 整体覆盖率 > 80%

## Execution Order

```
Phase 1 (Foundation):
Task 1.1 ─────────────────────────────────────────────────┐
Task 1.2 [P] ──► Task 1.3                                │
Task 1.4 [P]                                              │
                                                          ▼
                                              Task 1.5 ◄──┘

Phase 2 (Core - TDD):
┌─► Task 2.1 ──► Task 2.2
│
└─► Task 2.3 [P] ──► Task 2.4

Phase 3 (Integration):
Task 3.1 ──► Task 3.2 ──► Task 3.3 ──► Task 3.4

Phase 4 (Interface):
Task 4.1 ──► Task 4.2

Phase 5 (Testing & Docs):
Task 5.1 [P] ──────────────────┐
Task 3.4 完成 ──► Task 5.2 ◄──┘
Task 4.2 完成 ──► Task 5.3 [P]
Task 5.2 完成 ──► Task 5.4
```

## Checkpoints

- [ ] **Checkpoint 1**: After Phase 1 - 验证数据模型定义正确，可导入无错误
- [ ] **Checkpoint 2**: After Phase 2 - 验证 StateDetector 和 OutputFormatter 测试全部通过
- [ ] **Checkpoint 3**: After Phase 3 - 验证 ClaudeSessionMonitor 扩展功能正常
- [ ] **Checkpoint 4**: After Phase 4 - 验证 CLI 输出格式正确
- [ ] **Checkpoint 5**: After Phase 5 - 验证集成测试通过，覆盖率达标

## Risk Mitigation

| 风险 | 缓解任务 | 说明 |
|------|----------|------|
| AskUserQuestion 格式变化 | Task 2.1 | 测试覆盖多种格式变体 |
| 误报错误状态 | Task 2.1, Task 3.1 | 5 秒等待确认逻辑测试 |
| 多 session 竞态 | Task 5.2 | 集成测试验证并发场景 |

---

*Generated on 2026-03-10 based on plan.md and spec.md*
