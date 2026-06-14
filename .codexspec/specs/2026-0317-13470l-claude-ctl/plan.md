# Implementation Plan: claude-ctl

## 1. Tech Stack

| Category | Technology | Version | Notes |
|----------|------------|---------|-------|
| Language | Python | 3.11+ | 与项目现有脚本保持一致 |
| CLI Framework | argparse | stdlib | Python 标准库，与 `claude_monitor.py` 一致 |
| External Command | tmux | 2.0+ | 通过 subprocess 调用 |
| Testing | pytest | 7.x | 与项目现有配置一致 |
| Linting | ruff | latest | 与项目现有配置一致 |

## 2. Constitutionality Review

| Principle | Compliance | Notes |
|-----------|------------|-------|
| **1. Code Quality** | ✅ | 遵循 PEP 8，使用有意义的变量名，函数单一职责 |
| **2. Testing Standards** | ✅ | 为所有功能编写单元测试，覆盖边界场景 |
| **3. Documentation** | ✅ | 提供 --help 文档，函数使用 docstring |
| **4. Architecture** | ✅ | 分离关注点：CLI 解析、tmux 操作、错误处理各司其职 |
| **5. Performance** | ✅ | 直接调用 tmux，无额外开销，满足 < 100ms 要求 |
| **6. Security** | ✅ | 使用 `tmux send-keys -l` 防止注入，验证输入 |

## 3. Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         claude-ctl                                │
├──────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │   CLI Parser    │  │  TmuxClient     │  │  Output Handler │   │
│  │   (argparse)    │  │  (subprocess)   │  │  (print/sysexit)│   │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘   │
│           │                    │                    │             │
│           │  Action            │  Commands          │  Results    │
│           ▼                    ▼                    ▼             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                     Main Controller                          │ │
│  │  - validate_mutual_exclusion()                              │ │
│  │  - execute_action()                                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ subprocess.run()
                              ▼
                    ┌─────────────────┐
                    │   tmux server   │
                    └─────────────────┘
```

## 4. Component Structure

```
scripts/python/
├── claude_ctl.py           # 主入口文件（单文件实现）
└── tests/
    └── test_claude_ctl.py  # 单元测试
```

**设计决策：单文件实现**

由于功能相对简单（约 200-300 行代码），采用单文件实现：

- 降低维护成本
- 便于分发和安装
- 与 `claude_monitor.py` 风格一致

## 5. Module Specifications

### 5.1 CLI Parser Module (内联)

- **Responsibility**: 解析命令行参数，验证互斥性
- **Interface**:
  - `parse_args() -> argparse.Namespace`
- **Parameters**:
  - `--session`: 目标 tmux 会话名称
  - `--message`: 发送文本消息
  - `--select`: 选择选项（支持逗号分隔多选）
  - `--approve`: 批准权限
  - `--reject`: 拒绝权限
  - `--version`: 显示版本号
  - `--list-sessions`: 列出所有会话

### 5.2 TmuxClient Module (内联)

- **Responsibility**: 封装 tmux 命令调用
- **Interface**:
  - `session_exists(name: str) -> bool`
  - `list_sessions() -> list[str]`
  - `send_keys(session: str, text: str, literal: bool = True) -> bool`
  - `send_enter(session: str) -> bool`
- **Error Handling**: 捕获 subprocess 异常，返回 False 或空列表

### 5.3 Action Handlers (内联)

- **Responsibility**: 执行具体操作
- **Functions**:
  - `handle_message(session: str, text: str) -> int`
  - `handle_select(session: str, options: str) -> int`
  - `handle_approve(session: str) -> int`
  - `handle_reject(session: str) -> int`
  - `handle_list_sessions() -> int`
  - `handle_version() -> int`

### 5.4 Version Management

- **Strategy**: 使用 `importlib.metadata` 从 pyproject.toml 动态读取版本号
- **Fallback**: 如果无法获取（开发环境），使用硬编码默认值 `"0.0.0-dev"`
- **Implementation**:

  ```python
  try:
      from importlib.metadata import version
      __version__ = version("claude-ctl")
  except Exception:
      __version__ = "0.0.0-dev"
  ```

## 6. Data Models

不适用 - 本工具无持久化数据存储。

## 7. API Contracts

### Command Line Interface

#### 基本命令格式

```bash
claude-ctl --session <name> <--message|--select|--approve|--reject> [value]
claude-ctl --list-sessions
claude-ctl --version
claude-ctl --help
```

#### Exit Codes

| Code | Meaning | Applicable Commands |
|------|---------|---------------------|
| 0 | Success | All commands |
| 1 | Session not found | --message, --select, --approve, --reject |
| 2 | Invalid arguments (mutual exclusion violation, missing required args) | All except --help, --version |
| 3 | tmux command execution failed | All commands that call tmux |

**Note**: `--list-sessions`, `--version`, `--help` 命令：

- 成功时返回 exit code 0
- tmux 不可用时返回 exit code 3（仅 --list-sessions）

#### Output Format

| Scenario | Output |
|----------|--------|
| Success | `Message sent to session: <name>` |
| Session not found | `Error: Session '<name>' not found` |
| Mutual exclusion error | `Error: Cannot use --{a} and --{b} together` |
| Missing action | `Error: Must specify one of: --message, --select, --approve, --reject` |
| Empty select | `Error: Option cannot be empty` |
| List sessions | 每行一个会话名称 |

## 8. Implementation Phases

### Phase 1: Foundation (Setup)

- [ ] 创建 `scripts/python/claude_ctl.py` 文件
- [ ] 实现基本 CLI 参数解析（argparse）
- [ ] 实现 `--version` 和 `--help` 功能
- [ ] 添加 shebang 和文件头注释

### Phase 2: Core Implementation

- [ ] 实现 `TmuxClient` 类
  - `session_exists()` - 使用 `tmux has-session`
  - `list_sessions()` - 使用 `tmux list-sessions`
  - `send_keys()` - 使用 `tmux send-keys -l`
  - `send_enter()` - 使用 `tmux send-keys Enter`
- [ ] 实现会话存在性检查
- [ ] 实现 `--list-sessions` 功能

### Phase 3: Action Handlers

- [ ] 实现 `handle_message()` - 发送消息 + Enter
- [ ] 实现 `handle_select()` - 解析逗号分隔，依次发送
- [ ] 实现 `handle_approve()` - 发送 "Y" + Enter
- [ ] 实现 `handle_reject()` - 发送 "n" + Enter
- [ ] 实现互斥性验证

### Phase 4: Error Handling & Edge Cases

- [ ] 处理 session 不存在的情况
- [ ] 处理空消息（允许）和空选项（拒绝）
- [ ] 处理选项首尾空格
- [ ] 处理特殊字符（通过 `-l` 参数）
- [ ] 处理 tmux 命令执行失败

### Phase 5: Testing

- [ ] 创建 `tests/test_claude_ctl.py`
- [ ] 单元测试：参数解析
- [ ] 单元测试：互斥性验证
- [ ] 单元测试：选项解析（单选/多选/空格处理）
- [ ] 集成测试：mock tmux 命令
- [ ] 边界测试：空消息、空选项、特殊字符

## 9. Technical Decisions

### Decision 1: 单文件实现 vs 模块化

- **Choice**: 单文件实现 (`claude_ctl.py`)
- **Rationale**:
  - 功能简单，约 200-300 行代码
  - 与 `claude_monitor.py` 风格一致
  - 便于分发和安装
  - 降低维护成本
- **Alternatives**: 拆分为 `cli.py`, `tmux_client.py`, `handlers.py`
- **Trade-offs**: 牺牲了一定的模块化，但换来了简洁性

### Decision 2: tmux send-keys 策略

- **Choice**: 使用 `tmux send-keys -l` + 单独发送 Enter
- **Rationale**:
  - `-l` 参数按字面发送，避免特殊字符被解释为按键序列
  - 分开发送 Enter 确保消息提交
  - 这是 spec 中推荐的方式
- **Alternatives**:
  - 直接 `send-keys "message" Enter` - 有注入风险
  - 使用 `xargs` 或管道 - 复杂度高
- **Trade-offs**: 需要两次 tmux 调用，但确保了安全性

### Decision 3: 错误处理策略

- **Choice**: 使用 exit code 区分错误类型，输出人类可读的错误信息
- **Rationale**:
  - 便于脚本集成（可通过 exit code 判断）
  - 用户友好（错误信息清晰）
- **Alternatives**: 输出 JSON 格式错误 - 过度设计
- **Trade-offs**: 需要在文档中明确 exit code 含义

### Decision 4: 多选实现方式

- **Choice**: 依次发送每个选项（每个选项后按 Enter）
- **Rationale**:
  - Claude Code 的多选通常需要逐个确认
  - 简单直接，易于理解
- **Alternatives**: 一次性发送所有选项 - 可能不符合 Claude Code 的交互方式
- **Trade-offs**: 发送时间略长，但保证了正确性

## 10. File Checklist

### Files to Create

| File | Purpose |
|------|---------|
| `scripts/python/claude_ctl.py` | 主程序入口 |
| `scripts/python/tests/test_claude_ctl.py` | 单元测试 |

### Files to Reference

| File | Purpose |
|------|---------|
| `scripts/python/claude_monitor.py` | 代码风格参考 |
| `pyproject.toml` | 项目配置参考 |

## 11. Dependencies

### Runtime Dependencies

- Python 3.11+ (stdlib only, no external packages)
- tmux 2.0+

### Development Dependencies

- pytest (testing)
- ruff (linting)

---

*Generated: 2026-03-17*
