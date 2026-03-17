#!/usr/bin/env python3
"""
Claude Code Session Monitor
监听 Claude Code 执行状态，在执行完成时输出最后内容
"""

import argparse
import atexit
import json
import os
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

# 延迟导入 watchdog，避免在导入模块时就失败
if TYPE_CHECKING:
    from watchdog.observers import Observer

# 单实例锁文件
PID_FILE = Path("/tmp/claude_monitor.pid")


def _is_process_running(pid: int) -> bool:
    """检查进程是否存在（跨平台，支持 macOS）"""
    try:
        os.kill(pid, 0)  # 信号 0 不会真的杀死进程
        return True
    except OSError:
        return False
    except ValueError:
        return False


def _check_single_instance() -> None:
    """确保只有一个实例运行"""
    if PID_FILE.exists():
        try:
            old_pid = int(PID_FILE.read_text().strip())
            if _is_process_running(old_pid):
                print(f"[ERROR] Another instance is running (PID: {old_pid})", file=sys.stderr)
                print(f"[ERROR] Run 'kill {old_pid}' to stop it, or remove {PID_FILE} if stale", file=sys.stderr)
                sys.exit(1)
        except (ValueError, PermissionError):
            pass  # PID 文件损坏或无法读取，继续

    # 写入当前 PID
    PID_FILE.write_text(str(os.getpid()))


def _cleanup_pid_file() -> None:
    """清理 PID 文件"""
    try:
        if PID_FILE.exists():
            current_pid = int(PID_FILE.read_text().strip())
            if current_pid == os.getpid():
                PID_FILE.unlink()
    except (ValueError, PermissionError):
        pass


def _check_watchdog_available() -> bool:
    """检查 watchdog 是否可用"""
    try:
        from watchdog.events import FileSystemEventHandler  # noqa: F401
        from watchdog.observers import Observer  # noqa: F401

        return True
    except ImportError:
        return False


# ============================================================================
# 数据模型定义 (Phase 1: Foundation)
# ============================================================================


class SessionStatus(Enum):
    """Session 状态枚举"""

    STREAMING = "STREAMING"  # 流式输出中
    TOOL_USE = "TOOL_USE"  # 工具调用中
    PENDING_PERMISSION = "PENDING_PERMISSION"  # 等待权限确认
    USER_QUESTION = "USER_QUESTION"  # 等待用户回答
    ERROR_STOP = "ERROR_STOP"  # 出错停止
    TASK_COMPLETE = "TASK_COMPLETE"  # 任务完成
    IDLE = "IDLE"  # 空闲状态


@dataclass
class QuestionOption:
    """用户询问选项"""

    label: str
    description: str


@dataclass
class ToolUseInfo:
    """工具调用信息"""

    tool_name: str
    tool_id: str
    tool_input: dict[str, Any]
    description: Optional[str] = None


@dataclass
class QuestionInfo:
    """用户询问的详细信息"""

    question: str
    header: str
    options: list[QuestionOption]
    multi_select: bool = False


@dataclass
class ErrorInfo:
    """错误信息"""

    error_type: str
    message: str
    tool_name: Optional[str] = None
    tool_input: Optional[dict[str, Any]] = None


@dataclass
class SessionState:
    """Session 状态追踪"""

    session_id: str
    status: SessionStatus = SessionStatus.IDLE
    last_stop_reason: Optional[str] = None
    last_output: Optional[str] = None
    is_executing: bool = False
    questions: list[QuestionInfo] = field(default_factory=list)
    pending_tools: list[ToolUseInfo] = field(default_factory=list)
    error_info: Optional[ErrorInfo] = None


# ============================================================================
# 状态检测器 (Phase 2: Core Implementation)
# ============================================================================


class StateDetector:
    """状态检测器 - 检测消息状态并分类"""

    # 正常完成的 stop_reason
    STOP_REASONS_COMPLETE = ("end_turn", "stop_sequence", "max_tokens")

    @staticmethod
    def detect(
        message: dict,
    ) -> tuple[SessionStatus, Optional[QuestionInfo], list[ToolUseInfo], Optional[ErrorInfo]]:
        """
        检测消息状态

        Args:
            message: Claude API 响应消息

        Returns:
            tuple: (状态, 问题信息, 工具调用列表, 错误信息)
        """
        stop_reason = message.get("stop_reason")
        content = message.get("content", [])

        # 1. 流式输出中 (stop_reason=null)
        if stop_reason is None:
            return SessionStatus.STREAMING, None, [], None

        # 2. 检查是否为用户询问 (AskUserQuestion 工具)
        question_info = StateDetector._extract_question(content)
        if question_info:
            return SessionStatus.USER_QUESTION, question_info, [], None

        # 3. 检查是否为工具调用
        # 注意: stop_reason == "tool_use" 表示 Claude 正在使用工具
        # 大多数工具（Bash, Read, Write 等）会自动执行，不需要用户确认
        # 只有真正需要权限的工具才应该触发 PENDING_PERMISSION 通知
        if stop_reason == "tool_use":
            # 提取所有工具调用信息
            tool_infos = StateDetector._extract_tool_uses(content)
            # 返回 TOOL_USE 而不是 PENDING_PERMISSION
            # 避免对每个工具调用都发送权限请求通知
            return SessionStatus.TOOL_USE, None, tool_infos if tool_infos else [], None

        # 4. 检查是否出错
        error_info = StateDetector._extract_error(message)
        if error_info and stop_reason not in StateDetector.STOP_REASONS_COMPLETE:
            # 有错误且不是正常完成
            if stop_reason in ("refusal", "error") or (stop_reason not in StateDetector.STOP_REASONS_COMPLETE):
                return SessionStatus.ERROR_STOP, None, [], error_info

        # 5. 任务完成
        return SessionStatus.TASK_COMPLETE, None, [], None

    @staticmethod
    def _extract_tool_uses(content: list) -> list[ToolUseInfo]:
        """
        从 content 中提取所有 tool_use 信息

        Args:
            content: 消息内容列表

        Returns:
            ToolUseInfo 列表
        """
        tool_infos = []
        if not content:
            return tool_infos

        for item in content:
            if item.get("type") != "tool_use":
                continue

            tool_name = item.get("name", "")
            tool_id = item.get("id", "")
            tool_input = item.get("input", {})

            # 提取描述（如果存在）
            description = tool_input.get("description") if isinstance(tool_input, dict) else None

            tool_infos.append(
                ToolUseInfo(
                    tool_name=tool_name,
                    tool_id=tool_id,
                    tool_input=tool_input,
                    description=description,
                )
            )

        return tool_infos

    @staticmethod
    def _extract_question(content: list) -> Optional[QuestionInfo]:
        """
        从 content 中提取 AskUserQuestion 信息

        Args:
            content: 消息内容列表

        Returns:
            QuestionInfo 或 None
        """
        if not content:
            return None

        for item in content:
            if item.get("type") != "tool_use":
                continue
            if item.get("name") != "AskUserQuestion":
                continue

            input_data = item.get("input", {})

            # 修复：Claude API 的 AskUserQuestion 将问题放在 input.questions 数组中
            questions_data = input_data.get("questions", [])
            if not questions_data:
                return None

            # 取第一个问题（当前实现只支持单问题）
            first_question = questions_data[0]
            options_data = first_question.get("options", [])

            options = [
                QuestionOption(
                    label=opt.get("label", ""),
                    description=opt.get("description", ""),
                )
                for opt in options_data
            ]

            return QuestionInfo(
                question=first_question.get("question", ""),
                header=first_question.get("header", ""),
                options=options,
                multi_select=first_question.get("multiSelect", False),
            )

        return None

    @staticmethod
    def _extract_error(message: dict) -> Optional[ErrorInfo]:
        """
        从消息中提取错误信息

        Args:
            message: 完整的消息对象

        Returns:
            ErrorInfo 或 None
        """
        content = message.get("content", [])
        stop_reason = message.get("stop_reason")

        # 检查 refusal
        if stop_reason == "refusal":
            # 从 content 中提取 refusal 文本
            refusal_text = ""
            for item in content:
                if item.get("type") == "text":
                    refusal_text = item.get("text", "")
                    break
            return ErrorInfo(
                error_type="refusal",
                message=refusal_text or "Request was refused",
            )

        # 检查 tool_result 中的错误
        for item in content:
            if item.get("type") != "tool_result":
                continue
            if not item.get("is_error"):
                continue

            error_content = item.get("content", "")
            tool_use_id = item.get("tool_use_id", "")

            return ErrorInfo(
                error_type="tool_execution_error",
                message=str(error_content) if error_content else "Tool execution failed",
                tool_name=tool_use_id,  # 实际使用时可能需要从 tool_use_id 映射
            )

        # 检查 stop_reason 为 error
        if stop_reason == "error":
            error_text = ""
            for item in content:
                if item.get("type") == "text":
                    error_text = item.get("text", "")
                    break
            return ErrorInfo(
                error_type="execution_error",
                message=error_text or "Execution error occurred",
            )

        return None


# ============================================================================
# 输出格式化器 (Phase 2: Core Implementation)
# ============================================================================


class OutputFormatter:
    """输出格式化器 - 格式化各种状态的输出"""

    SEPARATOR = "=" * 60

    @staticmethod
    def format_pending_permission(session_id: str, tools: list[ToolUseInfo]) -> str:
        """
        格式化等待权限确认的输出

        Args:
            session_id: Session ID
            tools: 工具调用列表

        Returns:
            格式化的输出字符串
        """
        lines = [
            "",
            OutputFormatter.SEPARATOR,
            f"[Session: {session_id[:8]}] Status: PENDING_PERMISSION",
            OutputFormatter.SEPARATOR,
            "Tools waiting for permission:",
        ]

        for i, tool in enumerate(tools, 1):
            lines.append(f"  [{i}] {tool.tool_name}")
            if tool.description:
                lines.append(f"      Description: {tool.description}")
            # 显示工具输入参数
            if tool.tool_input:
                lines.append("      Input:")
                for key, value in tool.tool_input.items():
                    value_str = str(value)
                    if len(value_str) > 200:
                        value_str = value_str[:200] + "..."
                    lines.append(f"        {key}: {value_str}")

        lines.append(OutputFormatter.SEPARATOR)
        return "\n".join(lines)

    @staticmethod
    def format_user_question(session_id: str, questions: list[QuestionInfo]) -> str:
        """
        格式化用户询问输出

        Args:
            session_id: Session ID
            questions: 问题列表

        Returns:
            格式化的输出字符串
        """
        lines = [
            "",
            OutputFormatter.SEPARATOR,
            f"[Session: {session_id[:8]}] Status: USER_QUESTION",
            OutputFormatter.SEPARATOR,
            "Questions:",
        ]

        for i, q in enumerate(questions, 1):
            lines.append(f"  [{i}] {q.question}")
            lines.append(f"      Header: {q.header}")
            lines.append("      Options:")
            for opt in q.options:
                lines.append(f"        • {opt.label} - {opt.description}")
            if q.multi_select:
                lines.append("      (Multi-select enabled)")

        lines.append(OutputFormatter.SEPARATOR)
        return "\n".join(lines)

    @staticmethod
    def format_error_stop(session_id: str, error_info: ErrorInfo) -> str:
        """
        格式化错误停止输出

        Args:
            session_id: Session ID
            error_info: 错误信息

        Returns:
            格式化的输出字符串
        """
        lines = [
            "",
            OutputFormatter.SEPARATOR,
            f"[Session: {session_id[:8]}] Status: ERROR_STOP",
            OutputFormatter.SEPARATOR,
            f"Error Type: {error_info.error_type}",
            f"Message: {error_info.message}",
        ]

        if error_info.tool_name:
            lines.append(f"Tool: {error_info.tool_name}")

        if error_info.tool_input:
            lines.append(f"Input: {json.dumps(error_info.tool_input, ensure_ascii=False)}")

        lines.append(OutputFormatter.SEPARATOR)
        return "\n".join(lines)

    @staticmethod
    def format_task_complete(session_id: str, state: "SessionState") -> str:
        """
        格式化任务完成输出（保持现有格式）

        Args:
            session_id: Session ID
            state: Session 状态

        Returns:
            格式化的输出字符串
        """
        lines = [
            "",
            OutputFormatter.SEPARATOR,
            f"[Session: {session_id[:8]}] Status: TASK_COMPLETE",
            OutputFormatter.SEPARATOR,
            f"Stop reason: {state.last_stop_reason}",
        ]

        if state.last_output:
            # 限制输出长度
            output = state.last_output
            if len(output) > 2000:
                output = output[:2000] + "\n... (truncated)"
            lines.append("Output:")
            lines.append(f"  {output}")

        lines.append(OutputFormatter.SEPARATOR)
        return "\n".join(lines)


def _get_filesystem_event_handler():
    """延迟获取 FileSystemEventHandler 基类"""
    try:
        from watchdog.events import FileSystemEventHandler

        return FileSystemEventHandler
    except ImportError:

        class _DummyHandler:
            """当 watchdog 不可用时的占位基类"""

            pass

        return _DummyHandler


class ClaudeSessionMonitor(_get_filesystem_event_handler()):
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
        on_user_question: Optional[callable] = None,
        on_error_stop: Optional[callable] = None,
        on_pending_permission: Optional[callable] = None,
    ):
        self.project_dir = project_dir or self._detect_current_project()
        self.quiet = quiet
        self.on_complete = on_complete
        self.on_user_question = on_user_question
        self.on_error_stop = on_error_stop
        self.on_pending_permission = on_pending_permission
        self.sessions: dict[str, SessionState] = {}
        self._file_positions: dict[str, int] = {}  # 记录每个文件的读取位置
        self._observer: "Optional[Observer]" = None

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
        # data 可能是完整的事件 {"type": "assistant", "message": {...}}
        # 或者直接是 message 内容 {"stop_reason": ..., "content": [...]}
        message = data.get("message", data)
        stop_reason = message.get("stop_reason")
        content = message.get("content", [])

        # 提取文本内容
        text_content = self._extract_text(content)

        # 使用 StateDetector 检测状态
        detected_status, question_info, tool_infos, error_info = StateDetector.detect(message)

        # 更新 session 状态
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(session_id=session_id)

        state = self.sessions[session_id]
        _ = state.status  # Track for future use
        previous_executing = state.is_executing

        state.last_stop_reason = stop_reason
        state.last_output = text_content
        state.status = detected_status

        # 根据检测结果更新问题/错误/工具信息
        if question_info:
            state.questions = [question_info]
        else:
            state.questions = []

        state.pending_tools = tool_infos
        state.error_info = error_info

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

        # 触发状态变化回调
        if not silent:
            # 检测等待权限确认状态
            if detected_status == SessionStatus.PENDING_PERMISSION:
                self._on_pending_permission(session_id, state.pending_tools)

            # 检测用户询问状态
            elif detected_status == SessionStatus.USER_QUESTION:
                self._on_user_question(session_id, state.questions)

            # 检测错误停止状态
            elif detected_status == SessionStatus.ERROR_STOP:
                self._on_error_stop(session_id, state.error_info)

            # 检测从执行中变为完成（状态变化）
            elif previous_executing and not state.is_executing:
                self._on_execution_complete(session_id, state)
            # 检测直接完成的消息
            elif stop_reason in self.STOP_REASONS_COMPLETE:
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
        # 调用自定义回调（即使在 quiet 模式下也调用）
        if self.on_complete:
            self.on_complete(session_id, state)
            return

        # quiet 模式下不输出默认格式
        if self.quiet:
            return

        # 默认输出格式
        self._print_completion(session_id, state)

    def _on_user_question(self, session_id: str, questions: list[QuestionInfo]):
        """用户询问时的回调"""
        # 调用自定义回调（即使在 quiet 模式下也调用）
        if self.on_user_question:
            self.on_user_question(session_id, questions)
            return

        # quiet 模式下不输出默认格式
        if self.quiet:
            return

        # 默认输出格式
        output = OutputFormatter.format_user_question(session_id, questions)
        print(output)

    def _on_error_stop(self, session_id: str, error_info: ErrorInfo):
        """出错停止时的回调"""
        # 调用自定义回调（即使在 quiet 模式下也调用）
        if self.on_error_stop:
            self.on_error_stop(session_id, error_info)
            return

        # quiet 模式下不输出默认格式
        if self.quiet:
            return

        # 默认输出格式
        output = OutputFormatter.format_error_stop(session_id, error_info)
        print(output)

    def _on_pending_permission(self, session_id: str, tools: list[ToolUseInfo]):
        """等待权限确认时的回调"""
        # 调用自定义回调（即使在 quiet 模式下也调用）
        if self.on_pending_permission:
            self.on_pending_permission(session_id, tools)
            return

        # quiet 模式下不输出默认格式
        if self.quiet:
            return

        # 默认输出格式
        output = OutputFormatter.format_pending_permission(session_id, tools)
        print(output)

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

    def start(self, json_mode: bool = False):
        """启动监听"""
        # 检查 watchdog 是否可用
        if not _check_watchdog_available():
            print("Error: watchdog is required. Install with: pip install watchdog", file=sys.stderr)
            sys.exit(1)

        # 先初始化现有文件的状态
        self._initialize_from_existing_files()

        # 延迟导入 Observer
        from watchdog.observers import Observer

        # 启动文件监听
        self._observer = Observer()
        self._observer.schedule(self, str(self.project_dir), recursive=False)
        self._observer.start()

        # 获取最近活跃的 session 状态
        active_session = self._get_active_session()

        if json_mode:
            # JSON 模式输出
            output = {
                "type": "startup",
                "project": str(self.project_dir),
                "timestamp": time.time(),
            }
            if active_session:
                state = self.sessions.get(active_session)
                output["session_id"] = active_session
                output["status"] = state.status.value if state else "UNKNOWN"
                output["is_executing"] = state.is_executing if state else False
            else:
                output["session_id"] = None
                output["status"] = "NO_SESSION"
                output["is_executing"] = False
            print(json.dumps(output, ensure_ascii=False), flush=True)
        elif not self.quiet:
            # 普通模式输出
            print(f"Monitoring: {self.project_dir}")

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
    # 确保只有一个实例运行
    atexit.register(_cleanup_pid_file)
    _check_single_instance()

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
    on_user_question = None
    on_error_stop = None
    on_pending_permission = None

    if args.json:

        def json_complete_callback(session_id: str, state: SessionState):
            output = {
                "session_id": session_id,
                "status": state.status.value,
                "stop_reason": state.last_stop_reason or "unknown",
                "timestamp": time.time(),
                "output": state.last_output or "",
            }
            print(json.dumps(output, ensure_ascii=False), flush=True)

        def json_user_question_callback(session_id: str, questions: list[QuestionInfo]):
            output = {
                "session_id": session_id,
                "status": SessionStatus.USER_QUESTION.value,
                "timestamp": time.time(),
                "questions": [
                    {
                        "question": q.question,
                        "header": q.header,
                        "options": [{"label": opt.label, "description": opt.description} for opt in q.options],
                        "multi_select": q.multi_select,
                    }
                    for q in questions
                ],
            }
            print(json.dumps(output, ensure_ascii=False), flush=True)

        def json_error_stop_callback(session_id: str, error_info: ErrorInfo):
            output = {
                "session_id": session_id,
                "status": SessionStatus.ERROR_STOP.value,
                "timestamp": time.time(),
                "error": {
                    "type": error_info.error_type,
                    "message": error_info.message,
                    "tool_name": error_info.tool_name,
                    "tool_input": error_info.tool_input,
                },
            }
            print(json.dumps(output, ensure_ascii=False), flush=True)

        def json_pending_permission_callback(session_id: str, tools: list[ToolUseInfo]):
            output = {
                "session_id": session_id,
                "status": SessionStatus.PENDING_PERMISSION.value,
                "timestamp": time.time(),
                "tools": [
                    {
                        "name": t.tool_name,
                        "id": t.tool_id,
                        "input": t.tool_input,
                        "description": t.description,
                    }
                    for t in tools
                ],
            }
            print(json.dumps(output, ensure_ascii=False), flush=True)

        on_complete = json_complete_callback
        on_user_question = json_user_question_callback
        on_error_stop = json_error_stop_callback
        on_pending_permission = json_pending_permission_callback

    try:
        monitor = ClaudeSessionMonitor(
            project_dir=args.project,
            quiet=args.quiet or args.json,
            on_complete=on_complete,
            on_user_question=on_user_question,
            on_error_stop=on_error_stop,
            on_pending_permission=on_pending_permission,
        )
        monitor.start(json_mode=args.json)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")


if __name__ == "__main__":
    main()
