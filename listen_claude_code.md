# Claude Code Session 状态监听脚本设计方案

## 背景

用户需要一个 Python 脚本来持续监听 Claude Code 的运行状态，并在 Claude Code 处于 stop 状态（执行完成状态）时获取 session 内容的最后输出。

Stop 状态定义：用户在一个 session 中发送指令后，Claude Code 执行完成的状态。从用户视角，执行中显示橙色文本提示，完成显示灰色文本提示。

Claude Code 状态管理机制

数据存储位置

~/.claude/
├── projects/
│   └── -Users-xiaoming-code-[project]/
│       ├── [session-id].jsonl      # Session 日志 (JSONL 格式)
│       └── sessions-index.json      # Session 索引
├── tasks/[session-id]/              # 任务数据
├── history.jsonl                    # 全局历史
└── statusline.sh                    # 状态行脚本

Session 文件格式 (JSONL)

每行是一个 JSON 对象：
{
  "type": "user|assistant|progress",
  "sessionId": "uuid",
  "timestamp": "ISO-8601",
  "message": {
    "role": "assistant",
    "stop_reason": "end_turn|tool_use|stop_sequence|max_tokens|null",
    "content": [{"type": "text|tool_use|thinking", ...}]
  }
}

关键发现：stop_reason 字段

通过分析 session 文件，发现 stop_reason 是判断执行状态的关键：

┌─────────────────┬──────────────────┬────────┐
│   stop_reason   │       含义       │  状态  │
├─────────────────┼──────────────────┼────────┤
│ null            │ 流式输出中       │ 执行中 │
├─────────────────┼──────────────────┼────────┤
│ "tool_use"      │ 需要调用工具     │ 执行中 │
├─────────────────┼──────────────────┼────────┤
│ "end_turn"      │ 一轮对话正常结束 │ 完成 ✓ │
├─────────────────┼──────────────────┼────────┤
│ "stop_sequence" │ 遇到停止序列     │ 完成 ✓ │
├─────────────────┼──────────────────┼────────┤
│ "max_tokens"    │ 达到 token 限制  │ 完成 ✓ │
└─────────────────┴──────────────────┴────────┘

判断 Stop 状态的逻辑：
def is_execution_complete(stop_reason: str | None) -> bool:
    """判断是否执行完成"""
    return stop_reason in ("end_turn", "stop_sequence", "max_tokens")

推荐实现方案

核心脚本：claude_monitor.py

#!/usr/bin/env python3
"""
Claude Code Session Monitor
监听 Claude Code 执行状态，在执行完成时输出最后内容
"""

import json
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dataclasses import dataclass
from typing import Optional

@dataclass
class SessionState:
    session_id: str
    last_stop_reason: Optional[str] = None
    last_output: Optional[str] = None
    is_executing: bool = False

class ClaudeSessionMonitor(FileSystemEventHandler):
    """监听 Claude Code session 文件变化"""

    # 表示执行完成的 stop_reason
    STOP_REASONS_COMPLETE = ("end_turn", "stop_sequence", "max_tokens")
    # 表示执行中的 stop_reason
    STOP_REASONS_EXECUTING = (None, "tool_use")

    def __init__(self, project_dir: Optional[Path] = None, quiet: bool = False):
        self.project_dir = project_dir or self._detect_current_project()
        self.quiet = quiet
        self.sessions: dict[str, SessionState] = {}
        self._file_positions: dict[str, int] = {}  # 记录每个文件的读取位置

    def _detect_current_project(self) -> Path:
        """检测当前项目目录"""
        projects_dir = Path.home() / ".claude" / "projects"
        # 找到最新修改的项目
        return max(projects_dir.iterdir(), key=lambda p: p.stat().st_mtime)

    def on_modified(self, event):
        """文件修改事件处理"""
        if not event.src_path.endswith('.jsonl'):
            return

        self.process_session_file(Path(event.src_path))

    def process_session_file(self, session_file: Path):
        """处理 session 文件的新内容"""
        session_id = session_file.stem
        last_pos = self._file_positions.get(str(session_file), 0)

        with open(session_file, 'r') as f:
            f.seek(last_pos)
            new_lines = f.readlines()
            self._file_positions[str(session_file)] = f.tell()

        for line in new_lines:
            if not line.strip():
                continue
            self._process_message(session_id, json.loads(line))

    def _process_message(self, session_id: str, data: dict):
        """处理单条消息"""
        if data.get('type') != 'assistant':
            return

        message = data.get('message', {})
        stop_reason = message.get('stop_reason')
        content = message.get('content', [])

        # 提取文本内容
        text_content = self._extract_text(content)

        # 更新 session 状态
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(session_id=session_id)

        state = self.sessions[session_id]
        state.last_stop_reason = stop_reason
        state.last_output = text_content
        state.is_executing = stop_reason in self.STOP_REASONS_EXECUTING

        # 检测执行完成
        if stop_reason in self.STOP_REASONS_COMPLETE:
            self._on_execution_complete(session_id, state)

    def _extract_text(self, content: list) -> str:
        """提取消息中的文本内容"""
        texts = []
        for item in content:
            if item.get('type') == 'text':
                texts.append(item.get('text', ''))
        return '\n'.join(texts)

    def _on_execution_complete(self, session_id: str, state: SessionState):
        """执行完成时的回调"""
        if self.quiet:
            return

        print(f"\n{'='*60}")
        print(f"[Session: {session_id[:8]}] Execution Complete")
        print(f"Stop reason: {state.last_stop_reason}")
        print(f"{'='*60}")
        if state.last_output:
            print(state.last_output)
        print(f"{'='*60}\n")

    def start(self):
        """启动监听"""
        observer = Observer()
        observer.schedule(self, str(self.project_dir), recursive=False)
        observer.start()

        print(f"Monitoring: {self.project_dir}")
        print("Waiting for Claude Code execution to complete...")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Monitor Claude Code sessions")
    parser.add_argument("--project", "-p", type=Path, help="Project directory to monitor")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress output")

    args = parser.parse_args()
    monitor = ClaudeSessionMonitor(project_dir=args.project, quiet=args.quiet)
    monitor.start()

实现步骤

Step 1: 创建基础监听脚本

- 使用 watchdog 监听 ~/.claude/projects/[project]/ 目录
- 检测 .jsonl 文件变化
- 增量读取文件内容（避免重复处理）

Step 2: 状态检测逻辑

- 解析 stop_reason 字段
- 区分执行中 (null, tool_use) 和完成 (end_turn, stop_sequence, max_tokens)
- 状态变化时触发回调

Step 3: 输出提取

- 解析 JSONL 格式
- 提取 assistant 类型消息中的文本内容
- 终端打印输出

Step 4: 命令行接口

- 参数配置 (项目目录、静默模式)
- 实时状态显示
- 可选：后台运行模式 (daemonize)

依赖

pip install watchdog

或使用 uv：
uv pip install watchdog

使用方式

# 监听当前项目
python claude_monitor.py

# 指定项目目录
python claude_monitor.py --project ~/.claude/projects/-Users-xiaoming-code-myproject

# 静默模式（可用于管道）
python claude_monitor.py --quiet

验证方式

1. 启动监听脚本
2. 在另一个终端启动 Claude Code 并执行一个任务
3. 等待 Claude Code 执行完成（状态变灰）
4. 确认监听脚本正确输出最后内容

注意事项

1. 权限：需要读取 ~/.claude/ 目录权限
2. 性能：watchdog 是高效的文件监听方案，基于操作系统原生事件
3. 跨平台：watchdog 支持 macOS/Linux/Windows
4. 多 Session：支持同时监听多个 session 文件
