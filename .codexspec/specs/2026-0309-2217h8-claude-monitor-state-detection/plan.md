# Implementation Plan: Claude Code Session 状态检测增强

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 与现有项目保持一致 |
| File Watching | watchdog | >= 3.0.0 | 已有依赖，用于文件监听 |
| CLI | argparse | stdlib | 已有，命令行参数解析 |
| Type Hints | typing | stdlib | 类型注解支持 |

**无新增依赖**：所有功能使用 Python 标准库和现有依赖实现。

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **Code Quality** | ✅ | 遵循现有代码风格，函数保持单一职责，使用 dataclass 管理状态 |
| **Testing Standards** | ✅ | 为新增功能编写单元测试，覆盖边界情况 |
| **Documentation** | ✅ | 更新 README.md，添加新状态的文档说明 |
| **Architecture** | ✅ | 扩展现有架构，使用回调模式保持解耦 |
| **Performance** | ✅ | 状态检测在文件解析时完成，无额外性能开销 |
| **Security** | ✅ | 仅读取本地文件，无安全敏感操作 |

## 3. Architecture Overview

### 集成场景（Integration Scenario）

本脚本采用**进程间通信**模式设计：

```
┌─────────────────────┐         ┌─────────────────────┐
│  claude_monitor.py  │  输出   │   其他程序          │
│  (独立进程)         │────────▶│   (独立进程)        │
│                     │  stdout │                     │
│  检测到状态变化      │  或文件  │  执行相应行为       │
└─────────────────────┘         └─────────────────────┘
```

**典型使用方式**:

```bash
# 管道传输
python claude_monitor.py | other_program

# JSON 输出（便于解析）
python claude_monitor.py --json | jq '.status'
```

### 状态机设计

```
                    ┌─────────────┐
                    │  STREAMING  │ (stop_reason=null)
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
     ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
     │ TOOL_USE    │ │USER_QUESTION│ │ ERROR_STOP   │
     │ (其他工具)   │ │ (AskUser)   │ │ (出错停止)    │
     └──────┬──────┘ └──────┬──────┘ └──────────────┘
            │               │
            │               ▼
            │        ┌─────────────┐
            │        │ WAITING_    │
            │        │ USER_INPUT  │
            │        └─────────────┘
            │
            ▼
     ┌─────────────┐
     │ TASK_       │
     │ COMPLETE    │
     └─────────────┘
```

### 组件交互流程

```
┌─────────────────────────────────────────────────────────────┐
│                    ClaudeSessionMonitor                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │ File Watcher │───▶│ JSONL Parser │───▶│ State Machine│   │
│  │ (watchdog)   │    │              │    │              │   │
│  └──────────────┘    └──────────────┘    └──────┬───────┘   │
│                                                  │           │
│                          ┌───────────────────────┼───────┐   │
│                          ▼                       ▼       ▼   │
│                   ┌────────────┐         ┌────────────┐      │
│                   │ Callbacks  │         │  Output    │      │
│                   │ Dispatcher │         │  Formatter │      │
│                   └────────────┘         └────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## 4. Component Structure

```
scripts/python/
├── claude_monitor.py          # 主脚本（修改）
│   ├── SessionState           # 数据类（扩展）
│   ├── SessionStatus          # 新增：状态枚举
│   ├── QuestionInfo           # 新增：问题信息数据类
│   ├── ErrorInfo              # 新增：错误信息数据类
│   ├── ClaudeSessionMonitor   # 主监控类（扩展）
│   ├── StateDetector          # 新增：状态检测器
│   ├── OutputFormatter        # 新增：输出格式化器
│   └── main()                 # CLI 入口（修改）
└── README.md                  # 文档（更新）
```

## 5. Module Dependency Graph

```
┌─────────────────┐
│     main()      │  CLI 入口
└────────┬────────┘
         │ uses
         ▼
┌─────────────────┐
│ ClaudeSession   │  主监控类
│    Monitor      │
└────────┬────────┘
         │ uses
         ▼
┌─────────────────┐     ┌─────────────────┐
│ StateDetector   │────▶│ SessionState    │
│                 │     │ QuestionInfo    │
│                 │     │ ErrorInfo       │
└────────┬────────┘     └─────────────────┘
         │ uses
         ▼
┌─────────────────┐
│ OutputFormatter │  格式化输出
└─────────────────┘
```

## 6. Module Specifications

### Module: SessionState (扩展)

- **Responsibility**: 存储 session 的完整状态信息
- **Dependencies**: 无
- **Interface**: dataclass 字段
- **Changes**:
  - 添加 `status: SessionStatus` 字段
  - 添加 `questions: list[QuestionInfo]` 字段
  - 添加 `error_info: Optional[ErrorInfo]` 字段

```python
@dataclass
class SessionState:
    session_id: str
    status: "SessionStatus" = SessionStatus.IDLE
    last_stop_reason: Optional[str] = None
    last_output: Optional[str] = None
    is_executing: bool = False
    questions: list["QuestionInfo"] = field(default_factory=list)
    error_info: Optional["ErrorInfo"] = None
```

### Module: SessionStatus (新增)

- **Responsibility**: 定义所有可能的状态枚举
- **Dependencies**: 无
- **Interface**: Enum 成员

```python
class SessionStatus(Enum):
    STREAMING = "STREAMING"           # 流式输出中
    TOOL_USE = "TOOL_USE"             # 工具调用中
    USER_QUESTION = "USER_QUESTION"   # 等待用户回答
    ERROR_STOP = "ERROR_STOP"         # 出错停止
    TASK_COMPLETE = "TASK_COMPLETE"   # 任务完成
    IDLE = "IDLE"                     # 空闲状态
```

### Module: QuestionInfo (新增)

- **Responsibility**: 存储用户询问的详细信息
- **Dependencies**: 无
- **Interface**: dataclass 字段

```python
@dataclass
class QuestionOption:
    label: str
    description: str

@dataclass
class QuestionInfo:
    question: str
    header: str
    options: list[QuestionOption]
    multi_select: bool = False
```

### Module: ErrorInfo (新增)

- **Responsibility**: 存储错误信息
- **Dependencies**: 无
- **Interface**: dataclass 字段

```python
@dataclass
class ErrorInfo:
    error_type: str
    message: str
    tool_name: Optional[str] = None
    tool_input: Optional[dict] = None
```

### Module: StateDetector (新增)

- **Responsibility**: 检测消息状态并分类
- **Dependencies**: SessionStatus, QuestionInfo, ErrorInfo
- **Interface**: `detect_state(message: dict) -> tuple[SessionStatus, Optional[QuestionInfo], Optional[ErrorInfo]]`

```python
class StateDetector:
    @staticmethod
    def detect(message: dict) -> tuple[SessionStatus, Optional[QuestionInfo], Optional[ErrorInfo]]:
        """检测消息状态"""
        stop_reason = message.get("stop_reason")
        content = message.get("content", [])

        # 1. 流式输出中
        if stop_reason is None:
            return SessionStatus.STREAMING, None, None

        # 2. 检查是否为用户询问
        question_info = StateDetector._extract_question(content)
        if question_info:
            return SessionStatus.USER_QUESTION, question_info, None

        # 3. 检查是否出错
        error_info = StateDetector._extract_error(message)
        if error_info and stop_reason not in ("end_turn", "tool_use"):
            return SessionStatus.ERROR_STOP, None, error_info

        # 4. 工具调用
        if stop_reason == "tool_use":
            return SessionStatus.TOOL_USE, None, None

        # 5. 任务完成
        return SessionStatus.TASK_COMPLETE, None, None
```

### Module: OutputFormatter (新增)

- **Responsibility**: 格式化各种状态的输出
- **Dependencies**: 无
- **Interface**: 静态格式化方法

```python
class OutputFormatter:
    SEPARATOR = "=" * 60

    @staticmethod
    def format_user_question(session_id: str, questions: list[QuestionInfo]) -> str:
        """格式化用户询问输出"""

    @staticmethod
    def format_error_stop(session_id: str, error_info: ErrorInfo) -> str:
        """格式化错误停止输出"""

    @staticmethod
    def format_task_complete(session_id: str, state: SessionState) -> str:
        """格式化任务完成输出（保持现有格式）"""
```

### Module: ClaudeSessionMonitor (扩展)

- **Responsibility**: 主监控逻辑，协调各组件
- **Dependencies**: StateDetector, OutputFormatter
- **Interface**:
  - `__init__(..., on_user_question: callable = None, on_error_stop: callable = None)`
  - `_on_user_question(session_id, questions)` - 新增
  - `_on_error_stop(session_id, error_info)` - 新增
- **Changes**:
  - 添加新的回调参数
  - 修改 `_update_session_state()` 使用 StateDetector
  - 添加状态变化检测逻辑

## 7. Data Models

### SessionState 数据模型

| 字段 | 类型 | 描述 | 约束 |
|------|------|-------------|------|
| session_id | str | Session 唯一标识 | 必填 |
| status | SessionStatus | 当前状态 | 默认 IDLE |
| last_stop_reason | str \| None | 最后的 stop_reason | - |
| last_output | str \| None | 最后的文本输出 | - |
| is_executing | bool | 是否正在执行 | 默认 False |
| questions | list[QuestionInfo] | 用户询问列表 | 默认空列表 |
| error_info | ErrorInfo \| None | 错误信息 | 默认 None |

### QuestionInfo 数据模型

| 字段 | 类型 | 描述 | 约束 |
|------|------|-------------|------|
| question | str | 问题文本 | 必填 |
| header | str | 分类标签 | 必填 |
| options | list[QuestionOption] | 选项列表 | 必填 |
| multi_select | bool | 是否多选 | 默认 False |

### ErrorInfo 数据模型

| 字段 | 类型 | 描述 | 约束 |
|------|------|-------------|------|
| error_type | str | 错误类型 | 必填 |
| message | str | 错误消息 | 必填 |
| tool_name | str \| None | 相关工具名 | 可选 |
| tool_input | dict \| None | 工具输入 | 可选 |

## 8. API Contracts

### 回调接口

#### on_user_question

```python
def on_user_question(session_id: str, questions: list[QuestionInfo]) -> None:
    """
    用户询问回调

    Args:
        session_id: Session ID（前8位用于显示）
        questions: 问题列表，包含问题文本、选项等
    """
```

#### on_error_stop

```python
def on_error_stop(session_id: str, error_info: ErrorInfo) -> None:
    """
    出错停止回调

    Args:
        session_id: Session ID（前8位用于显示）
        error_info: 错误信息，包含错误类型、消息等
    """
```

### CLI 接口

#### 命令参数

| 参数 | 类型 | 描述 | 默认值 |
|------|------|------|--------|
| --project, -p | Path | 项目目录 | 自动检测 |
| --quiet, -q | flag | 静默模式 | False |
| --list, -l | flag | 列出项目 | - |
| --json | flag | JSON 输出 | False |

#### 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 正常退出 |
| 1 | 错误（文件未找到等） |

## 9. Implementation Phases

### Phase 1: 数据模型扩展

- [ ] 添加 `SessionStatus` 枚举类
- [ ] 添加 `QuestionOption` dataclass
- [ ] 添加 `QuestionInfo` dataclass
- [ ] 添加 `ErrorInfo` dataclass
- [ ] 扩展 `SessionState` dataclass，添加新字段

### Phase 2: 状态检测器实现

- [ ] 创建 `StateDetector` 类
- [ ] 实现 `_extract_question()` 方法：从 content 中提取 AskUserQuestion 信息
- [ ] 实现 `_extract_error()` 方法：检测错误标记和提取错误信息
- [ ] 实现 `detect()` 方法：主状态检测逻辑
- [ ] 添加单元测试

### Phase 3: 输出格式化器实现

- [ ] 创建 `OutputFormatter` 类
- [ ] 实现 `format_user_question()` 方法
- [ ] 实现 `format_error_stop()` 方法
- [ ] 实现 `format_task_complete()` 方法（重构现有代码）
- [ ] 添加单元测试

### Phase 4: 主监控类扩展

- [ ] 添加 `on_user_question` 回调参数
- [ ] 添加 `on_error_stop` 回调参数
- [ ] 修改 `_update_session_state()` 使用 StateDetector
- [ ] 实现 `_on_user_question()` 回调方法
- [ ] 实现 `_on_error_stop()` 回调方法
- [ ] 添加状态变化检测逻辑
- [ ] 添加集成测试

### Phase 5: 文档和测试

- [ ] 更新 README.md
- [ ] 添加输出示例
- [ ] 编写测试用例（TC-001 到 TC-005）
- [ ] 代码审查

## 10. Technical Decisions

### Decision 1: 使用 Enum 定义状态

- **Choice**: 使用 `Enum` 而非常量字符串定义状态
- **Rationale**:
  - 类型安全，IDE 支持更好
  - 避免拼写错误
  - 便于扩展新状态
- **Alternatives**: 使用常量字符串（如 `STATUS_STREAMING = "STREAMING"`）
- **Trade-offs**: 需要额外导入 Enum，但收益大于成本

### Decision 2: 分离状态检测逻辑

- **Choice**: 创建独立的 `StateDetector` 类
- **Rationale**:
  - 遵循单一职责原则
  - 便于单元测试
  - 便于未来扩展（如添加新状态类型）
- **Alternatives**: 在 `ClaudeSessionMonitor` 中直接实现
- **Trade-offs**: 增加一个类，但提高可维护性

### Decision 3: 回调函数签名设计

- **Choice**: 每种状态类型有独立的回调函数签名
- **Rationale**:
  - 类型明确，便于使用者处理
  - 参数与状态相关，语义清晰
- **Alternatives**: 统一回调签名 `on_state_change(status, **kwargs)`
- **Trade-offs**: 需要注册多个回调，但更灵活

### Decision 4: 出错停止判断逻辑

- **Choice**: 结合 `stop_reason` 和消息内容判断
- **Rationale**:
  - `stop_reason` 单独不足以判断
  - 需要检测消息中是否有错误标记
  - 定义"出错停止"为：有错误且无后续继续执行的迹象
- **实现细节**:

  ```python
  # 出错停止条件：
  # 1. stop_reason 不是正常的完成值 (end_turn, tool_use, null)
  # 2. 消息内容中包含错误信息
  # 3. 或者后续 5 秒内无新消息（表示已停止）
  ```

- **Trade-offs**: 可能有少量延迟（等待确认是否继续）

### Decision 5: 向后兼容性

- **Choice**: 保持现有 API 和输出格式
- **Rationale**:
  - 现有用户无需修改代码
  - 新功能通过可选参数提供
- **实现方式**:
  - `on_complete` 回调保持不变
  - 新增 `on_user_question` 和 `on_error_stop` 可选回调
  - 默认输出格式保持兼容

### Decision 6: 仅支持同步回调（当前版本）

- **Choice**: 当前版本仅实现同步回调，不提供异步回调支持
- **Rationale**:
  - **使用场景**: 监控脚本作为独立进程运行，输出状态信息供其他程序消费（进程间通信模式）
  - **通信方式**: 通过 stdout 管道或文件输出，其他程序读取并执行相应行为
  - **解耦设计**: 监控脚本只负责检测和输出，不直接调用外部 API
- **Alternatives**:
  - 支持异步回调（如 `async def on_user_question(...)`）
  - 内置 HTTP webhook 输出
- **Trade-offs**:
  - 放弃了进程内直接调用异步 API 的便利性
  - 换来了更简单、更稳定的设计
  - 便于独立部署和水平扩展
- **扩展预留**: 如果未来需要在回调中调用异步 API，可添加 `asyncio` 支持

## 11. Risk Assessment

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| AskUserQuestion 格式变化 | 低 | 中 | 使用健壮的字段提取，提供默认值 |
| 误报错误状态 | 中 | 中 | 增加 5 秒等待确认，减少误报 |
| 性能影响 | 低 | 低 | 状态检测在解析时完成，无额外开销 |
| 多 session 竞态 | 低 | 中 | 每个 session 独立状态追踪 |

## 12. Testing Strategy

### 单元测试

| 测试文件 | 测试内容 | 覆盖目标 |
|----------|----------|----------|
| `test_state_detector.py` | StateDetector 状态检测逻辑 | > 95% |
| `test_output_formatter.py` | OutputFormatter 格式化输出 | > 90% |
| `test_data_models.py` | dataclass 验证和默认值 | > 90% |

### 集成测试

| 测试场景 | 测试方法 |
|----------|----------|
| 端到端状态检测 | 使用 mock session 文件模拟各种状态 |
| 多 session 并发 | 创建多个临时 session 文件，验证独立追踪 |
| 文件删除处理 | 测试 session 文件被删除时的优雅处理 |

### 测试覆盖率目标

- **核心逻辑** (StateDetector, OutputFormatter): > 90%
- **整体**: > 80%

### Mock 数据准备

需要准备以下类型的 mock session 文件用于测试：

| Mock 文件 | 场景 | 关键数据 |
|-----------|------|----------|
| `mock_user_question.jsonl` | AskUserQuestion 工具调用 | `tool_use` + `AskUserQuestion` |
| `mock_task_complete.jsonl` | 正常任务完成 | `stop_reason: end_turn` |
| `mock_error_stop.jsonl` | 出错停止场景 | 非 `end_turn`/`tool_use`/`null` |
| `mock_tool_error_continue.jsonl` | 工具错误但继续执行 | 有错误但后续有新消息 |
| `mock_multiple_questions.jsonl` | 连续多个用户询问 | 多个 `AskUserQuestion` |

## 13. Future Extensions

以下功能不在当前版本范围内，留待有需求时再实现：

| 扩展项 | 触发条件 | 实现复杂度 | 优先级 |
|--------|----------|------------|--------|
| 异步回调支持 | 需要在回调中调用异步 API | 中 | P2 |
| HTTP Webhook 输出 | 需要推送到远程服务 | 中 | P3 |
| 状态持久化 | 需要历史记录分析 | 低 | P4 |
| 多进程分布式监控 | 需要监控多台机器 | 高 | P5 |

---

*This plan was updated on 2026-03-09 based on the clarification session.*
