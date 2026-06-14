# Feature: claude-ctl - Claude Code 远程控制工具

## Overview

`claude-ctl` 是一个命令行工具，用于向运行在 tmux 会话中的 Claude Code 发送控制指令。它作为 Claude Code 远程控制/监控系统的控制端，与负责状态监控的 `claude_monitor.py` 配合使用，实现对 Claude Code 的完整远程交互能力。

## Goals

- 提供简洁的命令行接口，向指定 tmux 会话中的 Claude Code 发送输入
- 支持三种核心交互场景：发送消息、选择选项、权限控制
- 确保消息发送的准确性和可靠性（特殊字符处理）
- 保持单一职责：只负责发送控制，不负责状态监控

## User Stories

### Story 1: 继续对话

**As a** Claude Code 用户
**I want** 能够向已完成任务的会话发送新消息
**So that** 无需手动切换到 tmux 窗口即可继续对话

**Acceptance Criteria:**

- [ ] 可以通过 `--message` 参数发送任意文本消息
- [ ] 消息能够准确发送到指定的 tmux 会话
- [ ] 发送后返回简单反馈（成功/失败）

### Story 2: 回答问题/选择方案

**As a** Claude Code 用户
**I want** 能够远程回答 Claude 提出的问题或选择方案
**So that** 无需手动操作即可完成交互式决策

**Acceptance Criteria:**

- [ ] 支持单选：`--select "A"`
- [ ] 支持多选：`--select "A,B,C"`（逗号分隔）
- [ ] 选项能够准确发送到指定会话

### Story 3: 权限控制

**As a** Claude Code 用户
**I want** 能够远程批准或拒绝 Claude 的操作权限请求
**So that** 可以在远程安全地控制 Claude 的操作权限

**Acceptance Criteria:**

- [ ] 支持 `--approve` 批准权限请求
- [ ] 支持 `--reject` 拒绝权限请求
- [ ] 权限回复能够准确发送到指定会话

## Functional Requirements

### REQ-001: 会话定位

- **REQ-001.1**: 通过 tmux session 名称定位目标会话
- **REQ-001.2**: 每次执行必须显式指定 `--session` 参数
- **REQ-001.3**: 如果指定的 session 不存在，返回错误信息

### REQ-002: 消息发送

- **REQ-002.1**: `--message` 参数用于发送任意文本消息
- **REQ-002.2**: 支持包含空格的消息内容
- **REQ-002.3**: 自动处理特殊字符（引号、换行、反斜杠等），确保消息准确发送
- **REQ-002.4**: 消息发送后自动按 Enter 键提交

### REQ-003: 选项选择

- **REQ-003.1**: `--select` 参数用于选择选项
- **REQ-003.2**: 支持单选：`--select "A"`
- **REQ-003.3**: 支持多选：`--select "A,B,C"`（逗号分隔）
- **REQ-003.4**: 多选时，按顺序依次发送每个选项（每个选项后按 Enter）
- **REQ-003.5**: 选项字符串去除首尾空格

### REQ-004: 权限控制

- **REQ-004.1**: `--approve` 参数用于批准权限请求
- **REQ-004.2**: `--reject` 参数用于拒绝权限请求
- **REQ-004.3**: 批准操作发送 "Y" 并按 Enter（对应 Claude Code 的 `[Y/n]` 提示）
- **REQ-004.4**: 拒绝操作发送 "n" 并按 Enter（对应 Claude Code 的 `[Y/n]` 提示）

### REQ-005: 执行反馈

- **REQ-005.1**: 成功时输出 "Message sent to session: <session_name>"
- **REQ-005.2**: session 不存在时输出 "Error: Session '<name>' not found"
- **REQ-005.3**: tmux 命令执行失败时输出错误信息
- **REQ-005.4**: `--version` 参数输出工具版本号（格式：`claude-ctl version X.Y.Z`）
- **REQ-005.5**: `--list-sessions` 参数列出所有可用的 tmux 会话

### REQ-006: 互斥性

- **REQ-006.1**: `--message`、`--select`、`--approve`、`--reject` 互斥，每次只能使用其中一个
- **REQ-006.2**: 如果同时指定多个操作参数，返回错误提示

## Non-Functional Requirements

### NFR-001: 性能

- **NFR-001.1**: 命令执行时间 < 100ms（不包括 tmux 会话响应时间）

### NFR-002: 可靠性

- **NFR-002.1**: 消息发送成功率 100%（在 tmux session 存在的前提下）
- **NFR-002.2**: 特殊字符不会导致命令执行失败或注入风险

### NFR-003: 可用性

- **NFR-003.1**: 提供 `--help` 参数显示使用说明
- **NFR-003.2**: 错误信息清晰、可操作

### NFR-004: 兼容性

- **NFR-004.1**: 支持 macOS 和 Linux
- **NFR-004.2**: 需要 tmux 2.0+

## Acceptance Criteria (Test Cases)

### TC-001: 发送简单消息

```bash
claude-ctl --session claude-main --message "继续工作"
# Expected: Message sent to session: claude-main
```

### TC-002: 发送包含空格的消息

```bash
claude-ctl --session claude-main --message "请帮我完成这个任务"
# Expected: Message sent to session: claude-main
```

### TC-003: 发送包含特殊字符的消息

```bash
claude-ctl --session claude-main --message "测试引号\"和反斜杠\\"
# Expected: Message sent to session: claude-main
# 验证: 消息内容准确到达，无字符丢失或变形
```

### TC-004: 单选选项

```bash
claude-ctl --session claude-main --select "A"
# Expected: Message sent to session: claude-main
```

### TC-005: 多选选项

```bash
claude-ctl --session claude-main --select "A,B,C"
# Expected: Message sent to session: claude-main
# 验证步骤:
# 1. 命令返回成功状态
# 2. 通过 claude_monitor.py 或直接观察 tmux 窗口，确认以下输入依次发送:
#    - "A" + Enter
#    - "B" + Enter
#    - "C" + Enter
# 3. Claude Code 正确接收到三个选项
```

### TC-006: 批准权限

```bash
claude-ctl --session claude-main --approve
# Expected: Message sent to session: claude-main
```

### TC-007: 拒绝权限

```bash
claude-ctl --session claude-main --reject
# Expected: Message sent to session: claude-main
```

### TC-008: Session 不存在

```bash
claude-ctl --session nonexistent --message "test"
# Expected: Error: Session 'nonexistent' not found
```

### TC-009: 互斥参数冲突

```bash
claude-ctl --session claude-main --message "test" --approve
# Expected: Error: Cannot use --message and --approve together
```

### TC-010: 缺少操作参数

```bash
claude-ctl --session claude-main
# Expected: Error: Must specify one of: --message, --select, --approve, --reject
```

### TC-011: 列出会话

```bash
claude-ctl --list-sessions
# Expected: 列出所有 tmux 会话，格式如：
# claude-main
# claude-secondary
# ...
```

## Edge Cases

### EC-001: 空消息

- **场景**: `--message ""`
- **处理**: 允许发送空消息（仅发送 Enter）

### EC-002: 空选项

- **场景**: `--select ""`
- **处理**: 返回错误 "Error: Option cannot be empty"

### EC-003: 多选包含空格

- **场景**: `--select "A, B, C"`（选项间有空格）
- **处理**: 自动去除每个选项的首尾空格

### EC-004: 多选重复选项

- **场景**: `--select "A,A,B"`
- **处理**: 按原样发送，不做去重

### EC-005: Session 名称包含特殊字符

- **场景**: `--session "my-session_123"`
- **处理**: 正确处理，不影响 tmux 命令执行

### EC-006: 消息包含换行符

- **场景**: `--message "第一行\n第二行"`
- **处理**: 字面发送 `\n` 字符，不转换为实际换行

## Output Examples

### 成功发送消息

```
$ claude-ctl --session claude-main --message "继续工作"
Message sent to session: claude-main
```

### 成功选择选项

```
$ claude-ctl --session claude-main --select "A,B"
Message sent to session: claude-main
```

### Session 不存在

```
$ claude-ctl --session nonexistent --message "test"
Error: Session 'nonexistent' not found
```

### 参数冲突

```
$ claude-ctl --session claude-main --message "test" --approve
Error: Cannot use --message and --approve together. Please specify only one action.
```

## Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│  claude_monitor.py  │     │    claude-ctl       │
│  (状态监控)          │     │    (发送控制)        │
│                     │     │                     │
│  - 监听 session 文件 │     │  - 接收 CLI 参数    │
│  - 检测状态变化      │     │  - 转义特殊字符     │
│  - 输出状态事件      │     │  - 调用 tmux 命令   │
└─────────────────────┘     └─────────────────────┘
           │                         │
           │ 监听状态                 │ 发送指令
           ▼                         ▼
┌─────────────────────────────────────────────────┐
│              Claude Code (in tmux)               │
│                                                  │
│  ~/.claude/projects/<project>/<session>.jsonl   │
└─────────────────────────────────────────────────┘
```

## Out of Scope

- **状态监控**: 由 `claude_monitor.py` 负责，不在本工具范围内
- **会话管理**: 不创建、删除或管理 tmux 会话
- **输出读取**: 不读取 tmux 会话的输出内容
- **历史记录**: 不记录发送的命令历史
- **批量操作**: 不支持一次向多个会话发送消息
- **配置文件**: 不支持配置文件或环境变量默认值
- **交互模式**: 不提供交互式 TUI 界面

## Dependencies

- **tmux**: 版本 2.0+
- **Python**: 版本 3.11+（如使用 Python 实现）
- **操作系统**: macOS / Linux

## Implementation Notes

### tmux send-keys 用法

```bash
# 基本语法
tmux send-keys -t <session-name> "<message>" Enter

# 使用 -l 选项按字面发送（避免按键解释）
tmux send-keys -t <session-name> -l "<message>" && tmux send-keys -t <session-name> Enter
```

### 特殊字符处理策略

1. 使用 `tmux send-keys -l` 按字面发送消息内容
2. 单独发送 Enter 键
3. 这样可以避免特殊字符被 tmux 解释为按键序列

---

*Generated: 2026-03-17*
