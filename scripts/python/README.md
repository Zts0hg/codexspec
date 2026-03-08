# Claude Code Session Monitor

监听 Claude Code 执行状态，在执行完成时输出最后内容。

## 安装依赖

```bash
# 使用 pip
pip install watchdog

# 或使用 uv
uv pip install watchdog

# 或安装 codexspec 的 monitor 扩展
uv pip install "codexspec[monitor]"
```

## 使用方式

```bash
# 监听最近活跃的项目
python claude_monitor.py

# 指定项目目录
python claude_monitor.py -p ~/.claude/projects/-Users-xiaoming-code-myproject

# 静默模式（用于脚本集成）
python claude_monitor.py -q

# 列出所有可用项目
python claude_monitor.py --list

# JSON 输出模式（用于程序化处理）
python claude_monitor.py --json
```

## 工作原理

### Claude Code 状态检测

Claude Code 的 session 文件（`.jsonl` 格式）中，每条 assistant 消息都有一个 `stop_reason` 字段：

| stop_reason   | 含义             | 判断逻辑     |
|---------------|------------------|----------|
| `null`        | 流式输出中       | **执行中** |
| `tool_use`    | 需要调用工具     | 结合文件修改时间判断 |
| `end_turn`    | 一轮对话正常结束 | **空闲** |
| `stop_sequence` | 遇到停止序列   | **空闲** |
| `max_tokens`  | 达到 token 限制  | **空闲** |

**状态判断逻辑**：
1. `stop_reason=null`：流式输出中，判定为**执行中**
2. `stop_reason=tool_use`：
   - 如果文件在 3 秒内被修改过 → **执行中**
   - 否则 → **空闲**
3. 其他情况（`end_turn`、`stop_sequence`、`max_tokens`）：**空闲**

脚本通过监听文件变化，检测 `stop_reason` 从执行中状态变为完成状态，然后输出最后的内容。

### 作为库使用

```python
from claude_monitor import ClaudeSessionMonitor

def on_complete(session_id: str, state: SessionState):
    print(f"Session {session_id} completed!")
    print(f"Output: {state.last_output}")

monitor = ClaudeSessionMonitor(on_complete=on_complete)
monitor.start()
```

## 文件结构

```
~/.claude/
├── projects/
│   └── -Users-xiaoming-code-[project]/
│       ├── [session-id].jsonl      # Session 日志
│       └── sessions-index.json      # Session 索引
├── tasks/[session-id]/              # 任务数据
└── history.jsonl                    # 全局历史
```

## 注意事项

1. **权限**：需要读取 `~/.claude/` 目录权限
2. **性能**：使用 watchdog 进行高效的文件监听
3. **跨平台**：支持 macOS/Linux/Windows
4. **多 Session**：支持同时监听多个 session 文件
