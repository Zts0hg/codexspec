#!/usr/bin/env python3
"""
Claude Code Session Monitor
监听 Claude Code 执行状态，在执行完成时输出最后内容
"""

import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    print("Error: watchdog is required. Install with: pip install watchdog")
    exit(1)


@dataclass
class SessionState:
    """Session 状态追踪"""

    session_id: str
    last_stop_reason: Optional[str] = None
    last_output: Optional[str] = None
    is_executing: bool = False


class ClaudeSessionMonitor(FileSystemEventHandler):
    """监听 Claude Code session 文件变化"""

    # 表示执行完成的 stop_reason
    STOP_REASONS_COMPLETE = ("end_turn", "stop_sequence", "max_tokens")
    # 表示可能正在执行的 stop_reason（需要结合文件修改时间判断）
    STOP_REASONS_MAYBE_EXECUTING = ("tool_use",)
    # 表示流式输出中的 stop_reason
    STOP_REASON_STREAMING = None

    # 判断为活跃的时间窗口（秒）
    ACTIVE_THRESHOLD_SECONDS = 3.0

    def __init__(
        self,
        project_dir: Optional[Path] = None,
        quiet: bool = False,
        on_complete: Optional[callable] = None,
    ):
        self.project_dir = project_dir or self._detect_current_project()
        self.quiet = quiet
        self.on_complete = on_complete
        self.sessions: dict[str, SessionState] = {}
        self._file_positions: dict[str, int] = {}  # 记录每个文件的读取位置
        self._observer: Optional[Observer] = None

    def _detect_current_project(self) -> Path:
        """检测当前项目目录"""
        projects_dir = Path.home() / ".claude" / "projects"
        if not projects_dir.exists():
            raise FileNotFoundError(f"Claude projects directory not found: {projects_dir}")

        # 获取所有项目目录
        project_dirs = [p for p in projects_dir.iterdir() if p.is_dir()]
        if not project_dirs:
            raise FileNotFoundError("No Claude projects found")

        # 找到最新修改的项目
        return max(project_dirs, key=lambda p: p.stat().st_mtime)

    def _get_session_files(self) -> list[Path]:
        """获取所有 session 文件"""
        return list(self.project_dir.glob("*.jsonl"))

    def _initialize_from_existing_files(self):
        """初始化时读取现有文件的状态"""
        for session_file in self._get_session_files():
            self._process_existing_file(session_file)

    def _process_existing_file(self, session_file: Path):
        """处理现有文件，获取最后状态但不触发回调"""
        session_id = session_file.stem

        try:
            with open(session_file, "r") as f:
                # 读取文件末尾，获取最后状态
                lines = f.readlines()
                self._file_positions[str(session_file)] = f.tell()
        except (IOError, json.JSONDecodeError):
            return

        # 从后往前找到最后的 assistant 消息
        for line in reversed(lines):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                if data.get("type") == "assistant":
                    self._update_session_state(session_id, data, silent=True)
                    break
            except json.JSONDecodeError:
                continue

    def on_modified(self, event):
        """文件修改事件处理"""
        if event.is_directory:
            return

        if not event.src_path.endswith(".jsonl"):
            return

        self.process_session_file(Path(event.src_path))

    def on_created(self, event):
        """文件创建事件处理"""
        if event.is_directory:
            return

        if not event.src_path.endswith(".jsonl"):
            return

        # 新 session 文件创建，初始化位置为 0
        session_file = Path(event.src_path)
        self._file_positions[str(session_file)] = 0
        if not self.quiet:
            print(f"[New Session] {session_file.stem[:8]}...")

    def process_session_file(self, session_file: Path):
        """处理 session 文件的新内容"""
        session_id = session_file.stem
        last_pos = self._file_positions.get(str(session_file), 0)

        try:
            with open(session_file, "r") as f:
                f.seek(last_pos)
                new_lines = f.readlines()
                self._file_positions[str(session_file)] = f.tell()
        except IOError:
            return

        for line in new_lines:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                self._process_message(session_id, data)
            except json.JSONDecodeError:
                continue

    def _process_message(self, session_id: str, data: dict):
        """处理单条消息"""
        if data.get("type") != "assistant":
            return

        self._update_session_state(session_id, data, silent=False)

    def _update_session_state(self, session_id: str, data: dict, silent: bool = False):
        """更新 session 状态"""
        message = data.get("message", {})
        stop_reason = message.get("stop_reason")
        content = message.get("content", [])

        # 提取文本内容
        text_content = self._extract_text(content)

        # 更新 session 状态
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(session_id=session_id)

        state = self.sessions[session_id]
        previous_executing = state.is_executing

        state.last_stop_reason = stop_reason
        state.last_output = text_content

        # 判断是否正在执行
        # 1. stop_reason=None 表示流式输出中，正在执行
        # 2. stop_reason=tool_use 需要结合文件修改时间判断
        # 3. 其他情况表示执行完成
        if stop_reason == self.STOP_REASON_STREAMING:
            state.is_executing = True
        elif stop_reason in self.STOP_REASONS_MAYBE_EXECUTING:
            # 检查文件最近是否被修改
            state.is_executing = self._is_session_recently_active(session_id)
        else:
            state.is_executing = False

        # 检测从执行中变为完成（状态变化）
        if not silent and previous_executing and not state.is_executing:
            self._on_execution_complete(session_id, state)
        # 检测直接完成的消息
        elif not silent and stop_reason in self.STOP_REASONS_COMPLETE:
            self._on_execution_complete(session_id, state)

    def _is_session_recently_active(self, session_id: str) -> bool:
        """检查 session 文件是否在最近活跃"""
        session_file = self.project_dir / f"{session_id}.jsonl"
        if not session_file.exists():
            return False

        try:
            mtime = session_file.stat().st_mtime
            import time

            return (time.time() - mtime) < self.ACTIVE_THRESHOLD_SECONDS
        except OSError:
            return False

    def _extract_text(self, content: list) -> str:
        """提取消息中的文本内容"""
        texts = []
        for item in content:
            if item.get("type") == "text":
                texts.append(item.get("text", ""))
            elif item.get("type") == "thinking":
                # 可选：包含 thinking 内容
                thinking_text = item.get("thinking", "")
                if thinking_text:
                    texts.append(f"[Thinking]\n{thinking_text}")
        return "\n".join(texts)

    def _on_execution_complete(self, session_id: str, state: SessionState):
        """执行完成时的回调"""
        if self.quiet:
            return

        # 调用自定义回调
        if self.on_complete:
            self.on_complete(session_id, state)
            return

        # 默认输出格式
        self._print_completion(session_id, state)

    def _print_completion(self, session_id: str, state: SessionState):
        """打印完成信息"""
        print(f"\n{'=' * 60}")
        print(f"[Session: {session_id[:8]}] Execution Complete")
        print(f"Stop reason: {state.last_stop_reason}")
        print(f"{'=' * 60}")
        if state.last_output:
            # 限制输出长度，避免过长
            output = state.last_output
            if len(output) > 2000:
                output = output[:2000] + "\n... (truncated)"
            print(output)
        print(f"{'=' * 60}\n")

    def start(self):
        """启动监听"""
        # 先初始化现有文件的状态
        self._initialize_from_existing_files()

        # 启动文件监听
        self._observer = Observer()
        self._observer.schedule(self, str(self.project_dir), recursive=False)
        self._observer.start()

        if not self.quiet:
            print(f"Monitoring: {self.project_dir}")

            # 获取最近活跃的 session 状态
            active_session = self._get_active_session()
            if active_session:
                state = self.sessions.get(active_session)
                if state:
                    if state.is_executing:
                        print(f"Status: EXECUTING (Session: {active_session[:8]}...)")
                        print("Waiting for execution to complete...")
                    else:
                        print(f"Status: IDLE (Session: {active_session[:8]}...)")
                        print("Listening for new executions...")
            else:
                print("Status: No active session found")
                print("Listening for new sessions...")

            print("Press Ctrl+C to stop\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def _get_active_session(self) -> Optional[str]:
        """获取最近活跃的 session ID"""
        if not self.sessions:
            return None

        # 找到最近修改的 session 文件
        try:
            session_files = sorted(
                self._get_session_files(),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if session_files:
                return session_files[0].stem
        except Exception:
            pass

        # 回退到 sessions 字典中的第一个
        return next(iter(self.sessions.keys()), None)

    def stop(self):
        """停止监听"""
        if self._observer:
            self._observer.stop()
            self._observer.join()
            self._observer = None

    def get_session_state(self, session_id: str) -> Optional[SessionState]:
        """获取指定 session 的状态"""
        return self.sessions.get(session_id)

    def get_all_sessions(self) -> dict[str, SessionState]:
        """获取所有 session 状态"""
        return self.sessions.copy()

    def get_executing_sessions(self) -> list[SessionState]:
        """获取正在执行的 sessions"""
        return [s for s in self.sessions.values() if s.is_executing]


def list_projects():
    """列出所有可用的 Claude 项目"""
    projects_dir = Path.home() / ".claude" / "projects"
    if not projects_dir.exists():
        print("No Claude projects directory found")
        return

    projects = []
    for project_dir in sorted(projects_dir.iterdir()):
        if project_dir.is_dir():
            # 统计 session 文件数量
            session_count = len(list(project_dir.glob("*.jsonl")))
            mtime = project_dir.stat().st_mtime
            projects.append((project_dir.name, session_count, mtime))

    if not projects:
        print("No Claude projects found")
        return

    print("Available Claude projects:")
    print("-" * 60)
    for name, count, mtime in sorted(projects, key=lambda x: x[2], reverse=True):
        # 显示项目名称（截断过长的名称）
        display_name = name[:50] + "..." if len(name) > 50 else name
        print(f"  {display_name}")
        print(f"    Sessions: {count}, Last modified: {time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))}")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor Claude Code sessions and output content when execution completes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Monitor the most recently active project
  python claude_monitor.py

  # Monitor a specific project
  python claude_monitor.py -p -Users-xiaoming-code-myproject

  # Quiet mode (no output, useful for scripting)
  python claude_monitor.py -q

  # List all available projects
  python claude_monitor.py --list
        """,
    )

    parser.add_argument(
        "--project",
        "-p",
        type=Path,
        help="Project directory to monitor (default: most recent)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress output (useful when using as library)",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all available Claude projects",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output completion events as JSON (one per line)",
    )

    args = parser.parse_args()

    if args.list:
        list_projects()
        return

    # 创建自定义回调用于 JSON 输出
    on_complete = None
    if args.json:

        def json_callback(session_id: str, state: SessionState):
            output = {
                "session_id": session_id,
                "stop_reason": state.last_stop_reason,
                "timestamp": time.time(),
                "output": state.last_output,
            }
            print(json.dumps(output, ensure_ascii=False))

        on_complete = json_callback

    try:
        monitor = ClaudeSessionMonitor(
            project_dir=args.project,
            quiet=args.quiet or args.json,
            on_complete=on_complete,
        )
        monitor.start()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")


if __name__ == "__main__":
    main()
