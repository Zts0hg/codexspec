# Feature: Claude Code Session 状态检测增强

## Overview

扩展现有的 `claude_monitor.py` 脚本，增加对更多 Claude Code 执行状态的检测能力，包括用户询问状态和出错停止状态。该功能将使脚本能够更全面地监控 Claude Code 的执行过程，为自动化集成提供更丰富的状态信息。

## Integration Scenario (使用场景)

### 当前版本的使用模式

本脚本采用**进程间通信**模式，监控脚本作为独立进程运行，输出状态信息供其他程序消费：

```
┌─────────────────────┐         ┌─────────────────────┐
│  claude_monitor.py  │  输出   │   其他程序          │
│  (独立进程)         │────────▶│   (独立进程)        │
│                     │  stdout │                     │
│  检测到状态变化      │  或文件  │  执行相应行为       │
└─────────────────────┘         └─────────────────────┘
```

### 典型使用方式

```bash
# 方式 1: 管道传输
python claude_monitor.py | other_program

# 方式 2: 文件传输
python claude_monitor.py > events.txt &
# 其他程序读取 events.txt

# 方式 3: JSON 输出（便于程序解析）
python claude_monitor.py --json | jq '.status'
```

### 设计决策

基于上述使用场景，当前版本的设计决策：

| 特性 | 当前版本 | 未来扩展 |
|------|----------|----------|
| 回调类型 | 仅同步回调 | 可扩展支持异步回调 |
| 输出方式 | stdout/文件 | 可扩展支持 HTTP webhook |
| 进程模型 | 单进程 | 可扩展支持多进程/分布式 |

**注意**: 异步回调 API 支持留待未来有需求时再扩展，当前版本不需要考虑。

## Goals

- 检测 Claude Code 向用户发起询问的状态（AskUserQuestion）
- 检测 Claude Code 因错误而停止的状态
- 保持现有文本输出格式，增加新的状态类型
- 为后续自动化集成提供可靠的状态监控基础

## User Stories

### Story 1: 用户询问状态检测

**作为** 自动化流程开发者
**我想要** 知道 Claude Code 何时向用户发起询问
**以便于** 在自动化流程中触发相应的通知或处理逻辑

**Acceptance Criteria:**

- [ ] 能够检测到 `AskUserQuestion` 工具的调用
- [ ] 能够提取问题的完整内容（问题文本、选项列表）
- [ ] 在检测到用户询问时输出格式化的通知信息

### Story 2: 出错停止状态检测

**作为** 自动化流程开发者
**我想要** 知道 Claude Code 何时因错误而停止执行
**以便于** 在自动化流程中进行错误处理或告警

**Acceptance Criteria:**

- [ ] 能够区分"工具调用错误但继续执行"和"错误导致停止"
- [ ] 能够提取错误信息内容
- [ ] 在检测到出错停止时输出格式化的错误信息

### Story 3: 状态监控集成

**作为** 系统集成工程师
**我想要** 通过统一的接口获取 Claude Code 的各种状态
**以便于** 与其他系统（如通知服务、工作流引擎）集成

**Acceptance Criteria:**

- [ ] 所有状态变化都有对应的回调函数
- [ ] 状态输出格式一致且易于解析
- [ ] 支持自定义回调处理

## Functional Requirements

### REQ-001: 用户询问状态检测

脚本应检测 Claude Code 发起用户询问的状态：

- **检测条件**: `assistant` 消息中包含 `tool_use` 类型的内容，且工具名为 `AskUserQuestion`
- **提取信息**:
  - 问题文本 (`question`)
  - 分类标签 (`header`)
  - 选项列表 (`options`)：包含 `label` 和 `description`
  - 是否多选 (`multiSelect`)

### REQ-002: 出错停止状态检测

脚本应检测 Claude Code 因错误而停止的状态：

- **检测条件**:
  - 不算出错：工具调用返回错误但 Claude 继续执行或重试
  - 算作出错：错误导致 Claude 无法继续执行任务
- **判断逻辑**:
  - 检测 `stop_reason` 为非正常完成值
  - 检测消息内容中包含错误信息
  - 结合后续是否有继续执行来判断

### REQ-003: 状态输出格式

保持现有文本格式，为新增状态类型添加相应的输出模板：

```
============================================================
[Session: {session_id}] Status: {status_type}
============================================================
{status_content}
============================================================
```

### REQ-004: 回调机制

为每种状态类型提供回调接口，允许使用者自定义处理逻辑：

- `on_execution_complete(session_id, state)` - 任务完成回调
- `on_user_question(session_id, questions)` - 用户询问回调
- `on_error_stop(session_id, error_info)` - 出错停止回调

## Non-Functional Requirements

### NFR-001: 性能要求

- 状态检测延迟 < 100ms
- 文件监听不应影响 Claude Code 的正常执行
- 内存占用应保持在合理范围内（< 50MB）

### NFR-002: 可靠性要求

- 状态检测准确率 > 99%
- 不应漏报重要状态变化
- 不应误报状态

### NFR-003: 可扩展性要求

- 新增状态类型应易于添加
- 输出格式应保持向后兼容
- **回调接口**: 当前版本仅支持同步回调（async callback 留待未来扩展）
  - 原因：当前使用场景为进程间通信，监控脚本只需输出状态信息
  - 扩展预留：接口设计应保持足够的灵活性，便于未来添加异步支持

## State Detection Logic

### 状态分类

| 状态 | stop_reason | 附加条件 | 优先级 |
|------|-------------|----------|--------|
| **STREAMING** | `null` | - | 1 (最高) |
| **USER_QUESTION** | `tool_use` | 工具名为 `AskUserQuestion` | 2 |
| **ERROR_STOP** | 非 `end_turn`/`tool_use`/`null` | 或有错误标记 | 3 |
| **TASK_COMPLETE** | `end_turn`/`stop_sequence`/`max_tokens` | - | 4 |

### 状态判断流程

```
1. 读取 assistant 消息
2. 检查 stop_reason
   - null → STREAMING
   - tool_use → 检查工具名
     - AskUserQuestion → USER_QUESTION
     - 其他 → 检查文件活跃度
   - end_turn/stop_sequence/max_tokens → TASK_COMPLETE
   - 其他 → 检查是否有错误标记
     - 有错误 → ERROR_STOP
     - 无错误 → TASK_COMPLETE
```

## Acceptance Criteria (Test Cases)

### TC-001: 用户询问检测

**前置条件**: Claude Code 执行中发起用户询问

**步骤**:

1. 启动 monitor 脚本
2. 触发 Claude Code 发起 AskUserQuestion

**预期结果**:

- 脚本输出包含 `Status: USER_QUESTION`
- 输出包含问题内容和选项列表

### TC-002: 正常任务完成检测

**前置条件**: Claude Code 正常完成任务

**步骤**:

1. 启动 monitor 脚本
2. 让 Claude Code 完成一个简单任务

**预期结果**:

- 脚本输出包含 `Status: TASK_COMPLETE`
- 输出包含最后的执行结果

### TC-003: 出错停止检测

**前置条件**: Claude Code 因错误无法继续执行

**步骤**:

1. 启动 monitor 脚本
2. 触发一个会导致 Claude Code 出错停止的场景

**预期结果**:

- 脚本输出包含 `Status: ERROR_STOP`
- 输出包含错误信息

### TC-004: 工具错误但继续执行

**前置条件**: Claude Code 工具调用失败但继续执行

**步骤**:

1. 启动 monitor 脚本
2. 触发一个工具调用失败但 Claude 会重试的场景

**预期结果**:

- 脚本不输出 ERROR_STOP
- 状态保持为 STREAMING 或变为 TOOL_USE

### TC-005: 回调函数触发

**前置条件**: 使用脚本作为库，注册自定义回调

**步骤**:

1. 编写测试代码，注册 `on_user_question` 回调
2. 触发用户询问场景

**预期结果**:

- 回调函数被正确调用
- 回调参数包含完整的问题信息

## Edge Cases

### Edge Case 1: 连续多个用户询问

**场景**: Claude Code 连续发起多个问题

**处理方式**:

- 每个问题单独触发一次回调
- 输出中区分不同的问题

### Edge Case 2: 用户询问后立即出错

**场景**: Claude Code 发起询问后，用户未响应导致超时或出错

**处理方式**:

- 先输出 USER_QUESTION 状态
- 如果后续检测到错误，再输出 ERROR_STOP 状态

### Edge Case 3: 多 Session 并发

**场景**: 同时有多个 session 文件在被监听

**处理方式**:

- 每个 session 独立追踪状态
- 输出中明确标识 session ID

### Edge Case 4: Session 文件被删除

**场景**: 监听过程中 session 文件被删除

**处理方式**:

- 优雅处理文件不存在的情况
- 从内存中清理相关状态

## Output Examples

### 用户询问输出示例

```
============================================================
[Session: 91bba6d2] Status: USER_QUESTION
============================================================
Questions:
  [1] 你希望使用哪种输出格式？
      Options:
        • JSON 格式 - 便于程序解析
        • 文本格式 - 便于人工阅读
        • 两者都支持 - 灵活切换
============================================================
```

### 出错停止输出示例

```
============================================================
[Session: 91bba6d2] Status: ERROR_STOP
============================================================
Error Type: ToolExecutionError
Message: Failed to execute tool: file not found
Tool: Read
Input: /path/to/nonexistent/file.txt
============================================================
```

### 任务完成输出示例（现有格式保持不变）

```
============================================================
[Session: 91bba6d2] Status: TASK_COMPLETE
============================================================
Stop reason: end_turn
Output:
  [最后输出内容]
============================================================
```

## Out of Scope

- **重试状态检测**: 不检测 Claude Code 的重试行为
- **进度百分比**: 不提供执行进度百分比
- **远程监控**: 不支持通过网络远程监控
- **历史记录存储**: 不持久化状态变化历史
- **UI 界面**: 不提供图形界面，仅命令行输出

## Dependencies

- Python 3.11+
- watchdog >= 3.0.0
- 现有 `claude_monitor.py` 脚本

## Implementation Notes

1. 建议在 `SessionState` dataclass 中添加新字段来存储用户询问和错误信息
2. **回调机制**: 当前版本仅实现同步回调，异步支持留待未来扩展
   - 当前使用场景：监控脚本输出状态，其他程序通过管道/文件读取
   - 未来如需在回调中调用异步 API（如 HTTP 请求），再添加异步支持
3. 考虑添加 `--format` 参数支持 JSON 输出（为未来扩展预留）

## Future Extensions (未来扩展)

以下功能不在当前版本范围内，留待有需求时再实现：

| 扩展项 | 触发条件 | 实现复杂度 |
|--------|----------|------------|
| 异步回调支持 | 需要在回调中调用异步 API | 中 |
| HTTP Webhook 输出 | 需要推送到远程服务 | 中 |
| 状态持久化 | 需要历史记录分析 | 低 |
| 多进程分布式监控 | 需要监控多台机器 | 高 |

---

## Clarifications

### Session 2026-03-09

**Q1**: 异步回调 API 是否需要在当前版本实现？
**A1**: 不需要。当前使用场景为进程间通信模式，监控脚本作为独立进程输出状态信息，其他程序通过管道或文件读取。异步回调支持留待未来有需求时再扩展。
**Impact**: NFR-003, Implementation Notes, 新增 Integration Scenario 章节
