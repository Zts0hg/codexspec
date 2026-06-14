# Implementation Plan: 通知脚本日志优化

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.8+ | 使用标准库，无额外依赖 |
| Logging | 自定义 Logger | - | 基于 io/write，支持 Emoji 和缩进格式 |
| File Ops | pathlib, os | - | 日志文件和目录操作 |
| Time | datetime | - | 时间戳格式化 |
| Config | os.environ | - | 环境变量配置 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| Code Quality | ✅ | 日志格式化逻辑独立封装为 Logger 类，配置参数集中管理 |
| Testing Standards | ✅ | 规格中已定义 9 个测试用例，需编写单元测试 |
| Documentation | ✅ | 代码添加适当注释，保持现有 docstring 风格 |
| Architecture | ✅ | 遵循单一职责原则，Logger 模块与业务逻辑分离 |
| Performance | ✅ | 使用追加模式写入，单条日志延迟 < 10ms |
| Security | ✅ | Chat ID 脱敏显示，特殊字符转义处理 |

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     notify_telegram.py                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Config    │    │   Logger    │    │  Notifier   │     │
│  │   配置模块   │    │   日志模块   │    │   通知模块   │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                  │                  │             │
│         │    ┌─────────────┴─────────────┐    │             │
│         └───▶│      Retry Handler        │◀───┘             │
│              │      重试处理器            │                  │
│              └───────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Log Files      │
                    │  (logs/*.log)   │
                    └─────────────────┘
```

## 4. Component Structure

```
scripts/python/
├── notify_telegram.py      # 主脚本（重构）
│   ├── Config 类           # 配置管理
│   ├── Logger 类           # 日志处理器
│   ├── RetryHandler 类     # 重试逻辑
│   ├── TelegramNotifier 类 # 通知发送（重构自现有代码）
│   └── main()              # 主入口
└── tests/
    └── test_notify.py      # 单元测试（新增）
```

## 5. Module Dependency Graph

```
┌─────────────┐
│    main()   │
└──────┬──────┘
       │ uses
       ▼
┌─────────────────────────────────────┐
│         TelegramNotifier            │
│  (消息格式化 + 发送逻辑)              │
└──────┬─────────────────────┬────────┘
       │ depends on          │ depends on
       ▼                     ▼
┌─────────────┐       ┌─────────────┐
│   Config    │       │   Logger    │
│  (配置管理)  │       │  (日志处理)  │
└─────────────┘       └──────┬──────┘
                             │ uses
                             ▼
                      ┌─────────────┐
                      │RetryHandler │
                      │ (重试逻辑)   │
                      └─────────────┘
```

## 6. Module Specifications

### Module: Config

- **Responsibility**: 集中管理所有配置参数，从环境变量读取
- **Dependencies**: os, pathlib
- **Interface**:

  ```python
  class Config:
      BOT_TOKEN: str
      CHAT_ID: str
      PROXY: str
      LOG_FILE: Optional[str]
      RETRY_COUNT: int
      RETRY_INTERVAL: int
      # 通知开关
      NOTIFY_ON_COMPLETE: bool
      NOTIFY_ON_USER_QUESTION: bool
      NOTIFY_ON_ERROR: bool
      NOTIFY_ON_PENDING_PERMISSION: bool
  ```

- **Files**: `notify_telegram.py` (内嵌类)

### Module: Logger

- **Responsibility**: 格式化日志输出，管理日志文件，处理轮转
- **Dependencies**: logging, pathlib, datetime, os
- **Interface**:

  ```python
  class Logger:
      def __init__(self, config: Config): ...
      def log_startup(self, chat_id: str, proxy: str, log_path: str): ...
      def log_waiting(self): ...
      def log_success(self, event_type: str, session_id: str, details: dict, retry_count: int = 0): ...
      def log_retry(self, event_type: str, session_id: str, error: str, attempt: int, max_attempts: int): ...
      def log_failure(self, event_type: str, session_id: str, error: str, retry_count: int): ...
      def _rotate_if_needed(self): ...  # 检查并执行轮转
      def _format_timestamp(self) -> str: ...
  ```

- **Files**: `notify_telegram.py` (内嵌类)

### Module: RetryHandler

- **Responsibility**: 封装重试逻辑，支持可配置的重试次数和间隔
- **Dependencies**: time
- **Interface**:

  ```python
  class RetryHandler:
      def __init__(self, max_retries: int, interval: float): ...
      def execute_with_retry(self, func: Callable[[], bool], on_retry: Callable[[int, str], None]) -> tuple[bool, int, Optional[str]]:
          """
          执行函数并在失败时重试

          Args:
              func: 要执行的函数，返回 bool 表示成功/失败
              on_retry: 重试时的回调，接收 (attempt, error_message)

          Returns:
              (success, retry_count, last_error)
          """
  ```

- **Files**: `notify_telegram.py` (内嵌类)

### Module: TelegramNotifier

- **Responsibility**: 格式化 Telegram 消息，发送通知，协调日志和重试
- **Dependencies**: urllib, json, Logger, RetryHandler, Config
- **Interface**:

  ```python
  class TelegramNotifier:
      def __init__(self, config: Config, logger: Logger): ...
      def send(self, message: str, event_type: str, session_id: str) -> bool: ...
      def process_event(self, line: str) -> Optional[str]: ...
      # 现有的消息格式化函数保持不变
      def format_task_complete(self, data: dict) -> str: ...
      def format_user_question(self, data: dict) -> str: ...
      def format_error(self, data: dict) -> str: ...
      def format_pending_permission(self, data: dict) -> str: ...
  ```

- **Files**: `notify_telegram.py` (重构现有代码)

## 7. Data Models

### LogEntry (内部使用)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| timestamp | str | 时间戳 | 格式: `%Y-%m-%d %H:%M:%S` |
| level | str | 日志级别 | INFO / WARNING / ERROR |
| emoji | str | Emoji 标识 | 🚀 / ℹ️ / ✅ / ⚠️ / ❌ |
| message | str | 主消息 | 最大 200 字符 |
| details | dict | 详细信息键值对 | 可选 |

### NotificationEvent (内部使用)

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| event_type | str | 事件类型 | task_complete / user_question / error / pending_permission |
| session_id | str | 会话 ID | 前 8 位 |
| details | dict | 附加详情 | 可选 |

## 8. Implementation Phases

### Phase 1: Foundation - Config + Logger 框架

- [ ] 创建 `Config` 类
- [ ] 迁移现有环境变量读取
- [ ] 添加新环境变量支持（`TELEGRAM_LOG_FILE`, `TELEGRAM_RETRY_COUNT`, `TELEGRAM_RETRY_INTERVAL`）
- [ ] 创建 `Logger` 类框架
- [ ] 实现时间戳格式化 (`%Y-%m-%d %H:%M:%S`)
- [ ] 实现 Emoji 映射表
- [ ] 实现基本日志格式化（主消息 + 详细信息行）
- [ ] 实现 stderr 双输出
- [ ] 单元测试：Config 加载、日志格式验证

### Phase 2: Core - 日志文件管理

- [ ] 实现日志文件路径解析（支持 `~` 展开）
- [ ] 实现日志目录自动创建
- [ ] 实现文件追加写入模式
- [ ] 实现按日期分割（检查日期变化）
- [ ] 实现按大小分割（10MB 阈值）
- [ ] 实现文件句柄管理（延迟打开，异常处理）
- [ ] 单元测试：文件创建、轮转逻辑

### Phase 3: Core - 重试机制

- [ ] 创建 `RetryHandler` 类
- [ ] 实现重试循环逻辑
- [ ] 实现重试间隔等待
- [ ] 集成到 `send_telegram_message`
- [ ] 单元测试：重试逻辑验证

### Phase 4: Integration - 整合与日志输出

- [ ] 重构 `main()` 函数使用新模块
- [ ] 集成启动日志输出
- [ ] 集成成功/失败日志输出
- [ ] 实现降级处理（日志文件不可写时）
- [ ] 实现特殊字符转义（EC-005）
- [ ] 实现错误消息截断（EC-004）
- [ ] 集成测试：端到端验证

### Phase 5: Testing & Polish

- [ ] 编写完整单元测试套件
- [ ] 手动测试边界情况（权限、磁盘空间等）
- [ ] 性能测试（确保 < 10ms 写入延迟）
- [ ] 代码审查和注释完善

## 9. Technical Decisions

### Decision 1: 使用 Python 标准库 logging 模块 vs 自定义日志

- **Choice**: 自定义 Logger 类（不使用 logging 模块）
- **Rationale**:
  - 需要特定的可读性格式（Emoji + 缩进详情）
  - 需要同时输出到 stderr 和文件
  - 标准库 logging 配置复杂度高，对本项目过度设计
- **Alternatives**:
  - 使用 `logging.handlers.RotatingFileHandler` - 但格式定制困难
  - 使用 `logging.handlers.TimedRotatingFileHandler` - 不支持混合轮转
- **Trade-offs**: 放弃了 logging 模块的成熟功能（如日志级别过滤），换取格式灵活性

### Decision 2: 日志轮转实现方式

- **Choice**: 每次写入前检查文件大小和日期
- **Rationale**:
  - 简单直接，无额外依赖
  - 性能开销小（仅 stat 调用）
  - 支持按日期和按大小混合轮转
- **Alternatives**:
  - 使用 `logging.handlers.RotatingFileHandler` - 不支持日期轮转
  - 使用第三方库 `loguru` - 引入额外依赖
- **Trade-offs**: 需要自行管理文件句柄，但保持了零依赖

### Decision 3: 重试机制设计

- **Choice**: 同步阻塞重试，带固定间隔
- **Rationale**:
  - 脚本为单线程管道处理，异步无意义
  - 固定间隔简单可靠
  - 通知场景对延迟不敏感
- **Alternatives**:
  - 指数退避重试 - 对短时间网络波动意义不大
  - 异步重试 - 增加复杂度，收益有限
- **Trade-offs**: 可能阻塞后续事件处理，但保证了顺序性和简单性

### Decision 4: 代码组织方式

- **Choice**: 单文件多类（而非多文件模块）
- **Rationale**:
  - 脚本为单一用途，不需要模块化
  - 便于部署（单文件拷贝）
  - 类之间紧密耦合，分离意义不大
- **Alternatives**:
  - 拆分为 `notify/` 包 - 对 CLI 工具过度设计
- **Trade-offs**: 单文件可能较长，但保持简单性

## 10. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| 日志文件权限问题 | 降级为仅 stderr 输出，不影响核心功能 |
| 磁盘空间不足 | 捕获 IOError，降级处理 |
| 并发写入冲突 | 使用追加模式 + OS 文件锁 |
| 跨平台路径问题 | 使用 `pathlib.Path` 处理路径 |

## 11. Acceptance Checklist

在实现完成后，验证以下内容：

- [ ] 日志格式符合 FR-001 规范（时间戳、Emoji、详细信息）
- [ ] 启动日志包含 Chat ID（脱敏）、Proxy、日志文件路径
- [ ] 成功日志包含类型、Session ID、附加信息
- [ ] 失败日志显示重试进度和错误详情
- [ ] 日志文件自动创建（目录和文件）
- [ ] 日志文件按日期命名
- [ ] 日志文件超过 10MB 自动轮转
- [ ] 重试机制正常工作（最多 3 次，间隔 1 秒）
- [ ] 环境变量 `TELEGRAM_LOG_FILE` 生效
- [ ] 环境变量 `TELEGRAM_RETRY_COUNT` 生效
- [ ] 环境变量 `TELEGRAM_RETRY_INTERVAL` 生效
- [ ] 日志文件不可写时降级为 stderr
- [ ] 特殊字符正确转义
- [ ] 与现有 `claude_monitor.py` 兼容
