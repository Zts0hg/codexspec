# Task Breakdown: 通知脚本日志优化

## Overview

- **Total tasks**: 21
- **Parallelizable tasks**: 8
- **Estimated phases**: 5
- **Feature ID**: 2026-0312-1544jt-notify-script-logging-optimization

## Phase 1: Foundation - 测试框架与配置模块

### Task 1.1: 创建测试文件框架 ✅

- **Type**: Setup
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 创建单元测试文件框架，包含 pytest 配置和基础测试结构
- **Dependencies**: None
- **Est. Complexity**: Low
- **Status**: Completed
- **Acceptance Criteria**:
  - [x] 测试文件可被 pytest 识别
  - [x] 包含必要的 import 和 fixture 设置

### Task 1.2: 编写 Config 类测试用例 [P] ✅

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写 Config 类的单元测试，覆盖环境变量读取、默认值、类型转换
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Status**: Completed
- **Test Cases**:
  - [x] TC-CFG-001: 读取所有环境变量
  - [x] TC-CFG-002: 默认值验证
  - [x] TC-CFG-003: 类型转换（bool/int）

### Task 1.3: 实现 Config 类 ✅

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 创建 Config 类，集中管理所有配置参数，从环境变量读取
- **Dependencies**: Task 1.2
- **Est. Complexity**: Low
- **Status**: Completed
- **Acceptance Criteria**:
  - [x] 支持现有环境变量 (BOT_TOKEN, CHAT_ID, PROXY)
  - [x] 支持新环境变量 (LOG_FILE, RETRY_COUNT, RETRY_INTERVAL)
  - [x] 支持通知开关 (NOTIFY_ON_*)

### Task 1.4: 编写 Logger 基础格式化测试 [P] ✅

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写 Logger 基础格式化的单元测试，覆盖时间戳、Emoji 映射、格式化输出
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Status**: Completed
- **Test Cases**:
  - [x] TC-LOG-001: 时间戳格式验证 (%Y-%m-%d %H:%M:%S)
  - [x] TC-LOG-002: Emoji 映射正确性
  - [x] TC-LOG-003: 主消息 + 详细信息行格式

### Task 1.5: 实现 Logger 基础格式化 ✅

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 创建 Logger 类框架，实现时间戳格式化、Emoji 映射、基本日志格式化、stderr 双输出
- **Dependencies**: Task 1.4
- **Est. Complexity**: Medium
- **Status**: Completed
- **Acceptance Criteria**:
  - [x] 时间戳格式: `%Y-%m-%d %H:%M:%S`
  - [x] Emoji 映射: 🚀(启动), ℹ️(等待), ✅(成功), ⚠️(重试), ❌(失败)
  - [x] 同时输出到 stderr 和日志文件

## Phase 2: Core - 日志文件管理

### Task 2.1: 编写日志文件路径解析测试

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写日志文件路径解析的单元测试，覆盖 ~ 展开、默认路径、自定义路径
- **Dependencies**: Task 1.5
- **Est. Complexity**: Low
- **Test Cases**:
  - TC-PATH-001: ~ 展开为用户主目录
  - TC-PATH-002: 默认路径规则验证
  - TC-PATH-003: 自定义路径 (TELEGRAM_LOG_FILE)

### Task 2.2: 实现日志文件路径解析

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 实现日志文件路径解析逻辑，支持 ~ 展开、默认路径规则、自定义路径
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - 默认路径: `{脚本所在目录}/logs/notify_{YYYY-MM-DD}.log`
  - 支持 `~` 展开
  - 支持 `TELEGRAM_LOG_FILE` 环境变量

### Task 2.3: 编写日志文件操作测试 [P]

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写日志文件操作的单元测试，覆盖目录创建、文件写入、句柄管理
- **Dependencies**: Task 2.1
- **Est. Complexity**: Low
- **Test Cases**:
  - TC-FILE-001: 目录自动创建
  - TC-FILE-002: 追加写入模式
  - TC-FILE-003: 文件句柄管理

### Task 2.4: 实现日志文件操作

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 实现日志目录自动创建、文件追加写入模式、文件句柄管理
- **Dependencies**: Task 2.3
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - logs 目录不存在时自动创建
  - 使用追加模式写入
  - 文件句柄正确管理，避免资源泄露

### Task 2.5: 编写日志轮转测试 [P]

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写日志轮转的单元测试，覆盖按日期分割、按大小分割
- **Dependencies**: Task 2.1
- **Est. Complexity**: Medium
- **Test Cases**:
  - TC-ROTATE-001: 日期变化时创建新文件
  - TC-ROTATE-002: 文件超过 10MB 时创建新文件
  - TC-ROTATE-003: 混合轮转场景

### Task 2.6: 实现日志轮转

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 实现混合轮转策略，按日期分割 + 按大小分割 (10MB)
- **Dependencies**: Task 2.5
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - 按日期分割: 每天创建新文件
  - 按大小分割: 单文件超过 10MB 追加序号
  - 文件名格式: `notify_{YYYY-MM-DD}.log`, `notify_{YYYY-MM-DD}_1.log`

## Phase 3: Core - 重试机制

### Task 3.1: 编写 RetryHandler 测试

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写 RetryHandler 类的单元测试，覆盖重试逻辑、间隔等待、回调机制
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Test Cases**:
  - TC-RETRY-001: 首次成功不重试
  - TC-RETRY-002: 失败后重试最多 3 次
  - TC-RETRY-003: 成功后立即停止重试
  - TC-RETRY-004: 重试间隔验证

### Task 3.2: 实现 RetryHandler 类

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 创建 RetryHandler 类，封装重试逻辑，支持可配置的重试次数和间隔
- **Dependencies**: Task 3.1
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - 最大重试次数: 3 (可通过 TELEGRAM_RETRY_COUNT 配置)
  - 重试间隔: 1 秒 (可通过 TELEGRAM_RETRY_INTERVAL 配置)
  - 返回 (success, retry_count, last_error)

### Task 3.3: 编写 send_with_retry 集成测试

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写 send_telegram_message 与 RetryHandler 集成的测试
- **Dependencies**: Task 3.2
- **Est. Complexity**: Medium
- **Test Cases**:
  - TC-INT-001: 发送成功无重试
  - TC-INT-002: 发送失败后重试成功
  - TC-INT-003: 发送失败后重试耗尽

## Phase 4: Integration - 整合与日志输出

### Task 4.1: 编写启动日志测试

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写启动日志输出的单元测试 (TC-001)
- **Dependencies**: Task 1.5
- **Est. Complexity**: Low
- **Test Cases**:
  - TC-001: 启动日志包含 Chat ID (脱敏)、Proxy、日志文件路径
  - 验证等待状态日志

### Task 4.2: 实现启动日志输出

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 实现 log_startup 和 log_waiting 方法，输出启动信息到 stderr 和日志文件
- **Dependencies**: Task 4.1
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - Chat ID 脱敏显示 (****6789)
  - 包含 Proxy 地址和日志文件路径
  - 进入事件监听后输出"等待事件中..."

### Task 4.3: 编写成功/失败日志测试 [P]

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写成功和失败日志输出的单元测试 (TC-002, TC-003, TC-004)
- **Dependencies**: Task 1.5
- **Est. Complexity**: Low
- **Test Cases**:
  - TC-002: 成功发送日志 (✅ + 类型 + Session ID + 原因)
  - TC-003: 失败重试日志 (⚠️ + 重试进度 + 错误)
  - TC-004: 最终失败日志 (❌ + 总重试次数)

### Task 4.4: 实现成功/失败日志输出

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 实现 log_success、log_retry、log_failure 方法
- **Dependencies**: Task 4.3
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - 成功: ✅ + 类型 + Session ID (前8位) + 附加信息
  - 重试: ⚠️ + 重试进度 (1/3) + 错误详情
  - 失败: ❌ + 总重试次数 + 错误详情

### Task 4.5: 编写降级处理测试

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写降级处理的单元测试 (TC-009, EC-001, EC-002)
- **Dependencies**: Task 2.4
- **Est. Complexity**: Low
- **Test Cases**:
  - TC-009: 日志文件不可写时降级为 stderr
  - EC-001: 目录权限不足
  - EC-002: 磁盘空间不足

### Task 4.6: 实现降级处理

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 实现日志写入失败时的降级处理，确保不影响核心通知功能
- **Dependencies**: Task 4.5
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - 日志写入失败时降级为仅 stderr
  - 不因日志问题影响通知发送
  - 捕获 IOError 并优雅处理

### Task 4.7: 编写特殊字符处理测试 [P]

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写特殊字符处理的单元测试 (EC-004, EC-005)
- **Dependencies**: Task 1.1
- **Est. Complexity**: Low
- **Test Cases**:
  - EC-004: 超长错误消息截断 (500 字符)
  - EC-005: 特殊字符转义 (换行符等)

### Task 4.8: 实现特殊字符处理

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 实现错误消息截断和特殊字符转义
- **Dependencies**: Task 4.7
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - 错误消息超过 500 字符时截断，添加 `...` 后缀
  - 换行符等特殊字符转义为安全字符

### Task 4.9: 重构 main() 函数

- **Type**: Implementation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 重构 main() 函数使用新模块 (Config, Logger, RetryHandler)
- **Dependencies**: Task 3.3, Task 4.2, Task 4.4, Task 4.6
- **Est. Complexity**: Medium
- **Acceptance Criteria**:
  - 使用 Config 类管理配置
  - 使用 Logger 类输出日志
  - 使用 RetryHandler 处理重试
  - 保持与现有 claude_monitor.py 的兼容性

## Phase 5: Testing & Documentation

### Task 5.1: 端到端测试

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 编写端到端测试，模拟完整的 stdin 输入流程
- **Dependencies**: Task 4.9
- **Est. Complexity**: Medium
- **Test Cases**:
  - TC-E2E-001: 完整运行流程模拟
  - 验证所有日志格式符合 FR-001 规范

### Task 5.2: 手动测试边界情况

- **Type**: Testing
- **Files**: N/A (手动测试)
- **Description**: 手动测试权限、磁盘空间、并发写入等边界情况
- **Dependencies**: Task 4.9
- **Est. Complexity**: Low
- **Test Checklist**:
  - [ ] 日志目录权限不足
  - [ ] 磁盘空间不足
  - [ ] 并发写入同一日志文件
  - [ ] 跨平台路径处理

### Task 5.3: 性能验证

- **Type**: Testing
- **Files**: `scripts/python/tests/test_notify.py`
- **Description**: 验证单条日志写入延迟 < 10ms
- **Dependencies**: Task 4.9
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - 单条日志写入延迟 < 10ms
  - 不阻塞通知发送流程

### Task 5.4: 代码审查和注释完善

- **Type**: Documentation
- **Files**: `scripts/python/notify_telegram.py`
- **Description**: 完善代码注释，确保符合项目文档规范
- **Dependencies**: Task 4.9
- **Est. Complexity**: Low
- **Acceptance Criteria**:
  - 所有类和方法有 docstring
  - 复杂逻辑有行内注释
  - 符合现有代码风格

## Execution Order

```
Phase 1: Task 1.1 ──► ┌─► Task 1.2 [P] ──► Task 1.3
                      │
                      └─► Task 1.4 [P] ──► Task 1.5
                                                │
Phase 2: ┌─────────────────────────────────────┴───────────────┐
         │                                                     │
    Task 2.1 ──► Task 2.2                              Task 2.3 [P]
         │                                                     │
         │                                             Task 2.4
         │                                                     │
         │                                             Task 2.5 [P]
         │                                                     │
         │                                             Task 2.6
         │                                                     │
Phase 3: │                                              (parallel)
         │                                                     │
    Task 3.1 ──► Task 3.2 ──► Task 3.3                        │
                                        │                      │
Phase 4: ┌──────────────────────────────┴──────────────────────┤
         │                                                     │
    Task 4.1 ──► Task 4.2                              Task 4.3 [P]
                                                        │
                                                Task 4.4
                                                        │
    Task 4.5 ──► Task 4.6                              Task 4.7 [P]
                                                        │
                                                Task 4.8
                                                        │
                                        Task 4.9
                                             │
Phase 5: ┌────────────────────────────────────┴────────────────┐
         │                                                    │
    Task 5.1                                             Task 5.2
         │                                                    │
    Task 5.3                                             Task 5.4
```

## Checkpoints

- [x] **Checkpoint 1**: After Phase 1 - 验证 Config 和 Logger 基础框架 ✅
- [x] **Checkpoint 2**: After Phase 2 - 验证日志文件管理和轮转功能 ✅
- [x] **Checkpoint 3**: After Phase 3 - 验证重试机制正常工作 ✅
- [x] **Checkpoint 4**: After Phase 4 - 验证完整集成和日志输出格式 ✅
- [x] **Checkpoint 5**: After Phase 5 - 验证端到端测试和文档完善 ✅

## User Story Mapping

| User Story | Related Tasks | Acceptance |
|------------|---------------|------------|
| Story 1: 开发者查看日志 | 1.4, 1.5, 4.1, 4.2, 4.3, 4.4 | TC-001 ~ TC-004 |
| Story 2: 运维人员排查问题 | 2.1 ~ 2.6 | TC-005 ~ TC-008 |
| Story 3: 系统自动恢复 | 3.1, 3.2, 3.3 | TC-003, TC-004 |

## Quality Checklist

- [x] 所有 plan 项都已覆盖
- [x] 每个任务只涉及一个主要文件（原子粒度）
- [x] TDD 强制执行：测试任务先于实现任务
- [x] 依赖关系正确识别
- [x] 可并行任务已标记 `[P]`
- [x] 文件路径具体准确
- [x] 复杂度估计合理
- [x] 检查点已定义在阶段边界
