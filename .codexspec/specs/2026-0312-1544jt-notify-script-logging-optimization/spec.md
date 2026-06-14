# Feature: 通知脚本日志优化

## Overview

优化 `notify_telegram.py` 的日志输出格式，使其提供更丰富的上下文信息，包括时间戳、事件类型、Session ID、通知类型等，同时支持日志文件持久化和自动重试机制。

## Goals

- 提供详细、可读性强的日志输出
- 支持日志文件持久化存储
- 实现智能的日志轮转策略
- 添加自动重试机制提高可靠性
- 保持与现有功能的完全兼容

## User Stories

### Story 1: 开发者查看日志

**As a** 使用 Claude Monitor 的开发者
**I want** 在日志中看到详细的通知发送信息
**So that** 我可以快速定位问题和了解系统状态

**Acceptance Criteria:**

- [ ] 日志包含精确到秒的时间戳
- [ ] 日志显示通知类型（任务完成、用户询问、错误、权限请求）
- [ ] 日志显示 Session ID 便于追踪
- [ ] 失败时显示错误详情
- [ ] 重试时显示重试进度

### Story 2: 运维人员排查问题

**As a** 运维人员
**I want** 日志持久化到文件
**So that** 我可以在事后进行问题分析

**Acceptance Criteria:**

- [ ] 日志自动写入文件
- [ ] 日志文件路径可配置
- [ ] 日志文件按日期命名
- [ ] 大文件自动轮转
- [ ] 历史日志可追溯

### Story 3: 系统自动恢复

**As a** 系统管理员
**I want** 通知发送失败时自动重试
**So that** 临时网络问题不会导致通知丢失

**Acceptance Criteria:**

- [ ] 失败后自动重试最多 3 次
- [ ] 每次重试记录日志
- [ ] 最终失败时记录完整错误信息
- [ ] 成功后立即停止重试

## Functional Requirements

### FR-001: 日志输出格式

日志采用可读性优先的格式，包含以下元素：

**格式规范：**

```
[YYYY-MM-DD HH:MM:SS] {emoji} {主消息}
    └─ {详细信息}
```

**时间戳格式：** `%Y-%m-%d %H:%M:%S`

**日志级别与 Emoji：**

| 级别 | Emoji | 场景 |
|------|-------|------|
| INFO | 🚀 | 启动 |
| INFO | ℹ️ | 等待状态 |
| INFO | ✅ | 发送成功 |
| WARNING | ⚠️ | 发送失败（含重试中） |
| ERROR | ❌ | 最终失败（重试耗尽后） |

### FR-002: 启动日志

**输出到：** stderr 和日志文件

**格式示例：**

```
[2026-03-12 14:30:15] 🚀 Telegram Notifier 启动
    └─ Chat ID: ****6789 | Proxy: http://127.0.0.1:7890
    └─ 日志文件: /path/to/logs/notify_2026-03-12.log
[2026-03-12 14:30:15] ℹ️ 等待事件中...
```

**必须包含：**

- 启动信息：Chat ID（脱敏显示后4位，如 `****6789`）、代理地址、日志文件路径
- 等待状态：进入事件监听循环后输出"等待事件中..."

### FR-003: 成功日志

**输出到：** stderr 和日志文件

**格式示例：**

```
[2026-03-12 14:30:20] ✅ 通知发送成功
    └─ 类型: 任务完成 | Session: abc12345 | 原因: end_turn
```

**必须包含：**

- 通知类型（任务完成/用户询问/错误通知/权限请求）
- Session ID（前8位）
- 类型相关的附加信息

### FR-004: 失败日志（带重试）

**输出到：** stderr 和日志文件

**格式示例：**

```
[2026-03-12 14:30:21] ⚠️ 发送失败 (重试 1/3)
    └─ 类型: 用户询问 | Session: def67890 | 错误: The read operation timed out
[2026-03-12 14:30:22] ⚠️ 发送失败 (重试 2/3)
    └─ 类型: 用户询问 | Session: def67890 | 错误: The read operation timed out
[2026-03-12 14:30:23] ❌ 发送最终失败
    └─ 类型: 用户询问 | Session: def67890 | 错误: The read operation timed out | 重试次数: 3
```

**必须包含：**

- 重试进度（当前/总数）
- 错误详情
- 最终失败时显示总重试次数

### FR-005: 日志文件配置

**环境变量：** `TELEGRAM_LOG_FILE`（可选）

**默认路径规则：**

```
{脚本所在目录}/logs/notify_{YYYY-MM-DD}.log
```

**示例：**

- 脚本路径：`/home/user/scripts/notify_telegram.py`
- 日志路径：`/home/user/scripts/logs/notify_2026-03-12.log`

**行为：**

- 如果 `logs` 目录不存在，自动创建
- 如果指定了 `TELEGRAM_LOG_FILE`，使用指定路径
- 路径支持 `~` 展开（用户主目录）

### FR-006: 日志轮转策略

**混合轮转规则：**

1. **按日期分割**：每天创建新的日志文件
   - 文件名格式：`notify_{YYYY-MM-DD}.log`

2. **按大小分割**：单文件超过 10MB 后追加序号
   - 新文件名：`notify_{YYYY-MM-DD}_1.log`
   - 继续增长：`notify_{YYYY-MM-DD}_2.log`，以此类推

**示例：**

```
logs/
├── notify_2026-03-11.log        (昨天，5MB)
├── notify_2026-03-12.log        (今天，8MB)
├── notify_2026-03-12_1.log      (今天，已满10MB)
└── notify_2026-03-12_2.log      (今天，当前写入)
```

### FR-007: 重试机制

**配置：**

- 最大重试次数：3 次
- 重试间隔：1 秒（可配置）

**行为：**

1. 发送失败后等待 1 秒
2. 重试发送，记录重试日志
3. 重复步骤 1-2，最多 3 次
4. 如果所有重试都失败，记录最终失败日志
5. 如果任意一次成功，立即停止重试，记录成功日志

**环境变量：**

- `TELEGRAM_RETRY_COUNT`：最大重试次数（默认 3）
- `TELEGRAM_RETRY_INTERVAL`：重试间隔秒数（默认 1）

## Non-Functional Requirements

### NFR-001: 性能

- 日志写入不应阻塞通知发送流程
- 日志文件写入采用追加模式，避免全文件读取
- 单条日志写入延迟 < 10ms

### NFR-002: 可靠性

- 日志写入失败时降级为仅输出 stderr
- 不因日志问题影响核心通知功能
- 日志文件句柄正确管理，避免资源泄露

### NFR-003: 兼容性

- 保持与现有 `claude_monitor.py` 的完全兼容
- 不改变 stdin JSON 输入格式
- 不改变 Telegram 消息内容格式
- 环境变量命名遵循现有约定（`TELEGRAM_*`）

### NFR-004: 可维护性

- 日志格式化逻辑独立封装
- 配置参数集中管理
- 代码添加适当注释

## Acceptance Criteria (Test Cases)

### TC-001: 基本启动日志

**Given** 环境变量已正确配置
**When** 启动 `notify_telegram.py`
**Then** stderr 和日志文件都包含启动信息，包括 Chat ID、Proxy、日志文件路径

### TC-002: 成功发送日志

**Given** Telegram API 可达
**When** 收到 `TASK_COMPLETE` 事件
**Then** 日志显示 ✅ 成功标记，包含类型、Session ID、停止原因

### TC-003: 失败重试日志

**Given** Telegram API 暂时不可达
**When** 发送失败
**Then** 日志显示 ⚠️ 重试标记，显示重试进度和错误信息

### TC-004: 最终失败日志

**Given** Telegram API 持续不可达
**When** 重试 3 次后仍失败
**Then** 日志显示 ❌ 最终失败标记，显示总重试次数

### TC-005: 日志文件创建

**Given** `logs` 目录不存在
**When** 启动脚本
**Then** 自动创建 `logs` 目录和当日日志文件

### TC-006: 自定义日志路径

**Given** 设置了 `TELEGRAM_LOG_FILE=/custom/path/notify.log`
**When** 启动脚本
**Then** 日志写入指定路径

### TC-007: 日志文件大小轮转

**Given** 日志文件接近 10MB
**When** 写入新日志
**Then** 创建新的带序号日志文件（`_1.log`）

### TC-008: 日期轮转

**Given** 跨越午夜
**When** 写入新日志
**Then** 创建新日期的日志文件

### TC-009: 降级处理

**Given** 日志文件不可写（权限问题）
**When** 尝试写入日志
**Then** 仅输出到 stderr，不中断程序运行

## Edge Cases

### EC-001: 日志目录权限不足

**场景：** `logs` 目录无法创建（权限被拒绝）
**处理：** 输出警告到 stderr，降级为仅 stderr 输出，继续运行

### EC-002: 磁盘空间不足

**场景：** 日志文件写入时磁盘已满
**处理：** 捕获异常，降级为仅 stderr 输出

### EC-003: 并发写入

**场景：** 多个脚本实例同时写入同一日志文件
**处理：** 依赖操作系统文件锁，追加模式写入

### EC-004: 超长错误消息

**场景：** 错误消息超过 500 字符
**处理：** 截断至 500 字符，添加 `...` 后缀

### EC-005: 特殊字符处理

**场景：** 日志内容包含换行符或特殊字符
**处理：** 转义或替换为安全字符，确保单行日志的可读性

## Output Examples

### 完整运行示例

```
[2026-03-12 14:30:15] 🚀 Telegram Notifier 启动
    └─ Chat ID: ****6789 | Proxy: http://127.0.0.1:7890
    └─ 日志文件: /Users/user/scripts/logs/notify_2026-03-12.log
[2026-03-12 14:30:15] ℹ️ 等待事件中...
[2026-03-12 14:30:20] ✅ 通知发送成功
    └─ 类型: 任务完成 | Session: abc12345 | 原因: end_turn
[2026-03-12 14:30:25] ⚠️ 发送失败 (重试 1/3)
    └─ 类型: 用户询问 | Session: def67890 | 错误: The read operation timed out
[2026-03-12 14:30:26] ✅ 通知发送成功 (重试后)
    └─ 类型: 用户询问 | Session: def67890 | 重试次数: 1
[2026-03-12 14:35:00] ⚠️ 发送失败 (重试 1/3)
    └─ 类型: 错误通知 | Session: ghi11111 | 错误: Connection refused
[2026-03-12 14:35:01] ⚠️ 发送失败 (重试 2/3)
    └─ 类型: 错误通知 | Session: ghi11111 | 错误: Connection refused
[2026-03-12 14:35:02] ⚠️ 发送失败 (重试 3/3)
    └─ 类型: 错误通知 | Session: ghi11111 | 错误: Connection refused
[2026-03-12 14:35:03] ❌ 发送最终失败
    └─ 类型: 错误通知 | Session: ghi11111 | 错误: Connection refused | 重试次数: 3
```

## Out of Scope

- 远程日志收集（如 ELK、Syslog）
- 日志加密
- 日志压缩归档
- 日志搜索功能
- Web UI 查看日志
- 短信/邮件通知日志告警
- 多 Chat ID 支持
- 消息队列缓冲

## Dependencies

- Python 3.8+（使用标准库，无额外依赖）
- 现有 `claude_monitor.py` 的 JSON 输出格式
- 现有环境变量配置（`TELEGRAM_BOT_TOKEN`、`TELEGRAM_CHAT_ID`）

## References

- 源文件：`scripts/python/notify_telegram.py`
- 相关监控脚本：`scripts/python/claude_monitor.py`
