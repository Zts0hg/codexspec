#!/usr/bin/env python3
"""
Claude Code Controller (claude-ctl)
远程控制运行在 tmux 会话中的 Claude Code

用法:
    claude-ctl --session <name> --message "继续工作"
    claude-ctl --session <name> --select "A,B,C"
    claude-ctl --session <name> --approve
    claude-ctl --session <name> --reject
    claude-ctl --list-sessions
    claude-ctl --list-panes [--session <name>]
    claude-ctl --version

session 格式支持:
    claude-main              # session 级别
    claude-main:0            # window 级别
    claude-main:0.1          # pane 级别
"""

import argparse
import subprocess
import sys

# Version management
try:
    from importlib.metadata import version

    __version__ = version("claude-ctl")
except Exception:
    __version__ = "0.0.0-dev"

# Exit codes
EXIT_SUCCESS = 0
EXIT_SESSION_NOT_FOUND = 1
EXIT_INVALID_ARGS = 2
EXIT_TMUX_ERROR = 3


class TmuxClient:
    """封装 tmux 命令调用"""

    @staticmethod
    def session_exists(name: str) -> bool:
        """检查 tmux session 是否存在"""
        try:
            result = subprocess.run(
                ["tmux", "has-session", "-t", name],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    @staticmethod
    def list_sessions() -> list[str]:
        """列出所有 tmux session"""
        try:
            result = subprocess.run(
                ["tmux", "list-sessions", "-F", "#{session_name}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return [s.strip() for s in result.stdout.strip().split("\n") if s.strip()]
            return []
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []

    @staticmethod
    def send_keys(session: str, text: str, literal: bool = True) -> bool:
        """向 tmux session 发送按键"""
        try:
            cmd = ["tmux", "send-keys", "-t", session]
            if literal:
                cmd.append("-l")
            cmd.append(text)
            result = subprocess.run(cmd, capture_output=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    @staticmethod
    def send_enter(session: str) -> bool:
        """向 tmux session 发送 Enter 键"""
        try:
            result = subprocess.run(
                ["tmux", "send-keys", "-t", session, "Enter"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    @staticmethod
    def list_panes(target: str = "") -> list[str]:
        """列出所有 pane，返回详细信息

        Args:
            target: 可选的目标，格式为 session、session:window 或 session:window.pane
                   空字符串表示列出所有 pane

        Returns:
            pane 信息列表，格式为 "session:window.pane  PID: xxx  Command: xxx"
        """
        try:
            cmd = [
                "tmux",
                "list-panes",
                "-F",
                "#{session_name}:#{window_index}.#{pane_index}  PID: #{pane_pid}  Command: #{pane_current_command}",
            ]
            if target:
                cmd.extend(["-t", target])
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
            return []
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        prog="claude-ctl",
        description="Claude Code 远程控制工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    claude-ctl --session claude-main --message "继续工作"
    claude-ctl --session claude-main --select "A,B,C"
    claude-ctl --session claude-main --approve
    claude-ctl --session claude-main --reject
    claude-ctl --list-sessions
    claude-ctl --list-panes
    claude-ctl --list-panes --session claude-main
    claude-ctl --session claude-main:0.1 --message "hello pane 1"
        """,
    )

    parser.add_argument(
        "--session",
        type=str,
        help="目标 tmux 会话名称",
    )
    parser.add_argument(
        "--message",
        type=str,
        help="发送文本消息",
    )
    parser.add_argument(
        "--select",
        type=str,
        help="选择选项（支持逗号分隔多选）",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="批准权限请求",
    )
    parser.add_argument(
        "--reject",
        action="store_true",
        help="拒绝权限请求",
    )
    parser.add_argument(
        "--list-sessions",
        action="store_true",
        help="列出所有 tmux 会话",
    )
    parser.add_argument(
        "--list-panes",
        action="store_true",
        help="列出所有 pane（可选 --session 指定范围）",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="显示版本号",
    )

    args = parser.parse_args()

    # 验证互斥性
    action_count = sum(
        [
            args.message is not None,
            args.select is not None,
            args.approve,
            args.reject,
        ]
    )

    if action_count > 1:
        # 找出冲突的参数
        actions = []
        if args.message is not None:
            actions.append("--message")
        if args.select is not None:
            actions.append("--select")
        if args.approve:
            actions.append("--approve")
        if args.reject:
            actions.append("--reject")
        print(
            f"Error: Cannot use {actions[0]} and {actions[1]} together. Please specify only one action.",
            file=sys.stderr,
        )
        sys.exit(EXIT_INVALID_ARGS)

    return args


def handle_message(session: str, text: str) -> int:
    """处理 --message 命令"""
    if not TmuxClient.session_exists(session):
        print(f"Error: Session '{session}' not found", file=sys.stderr)
        return EXIT_SESSION_NOT_FOUND

    # 空消息允许（仅发送 Enter）
    if text:
        if not TmuxClient.send_keys(session, text, literal=True):
            print(f"Error: Failed to send message to session '{session}'", file=sys.stderr)
            return EXIT_TMUX_ERROR

    if not TmuxClient.send_enter(session):
        print(f"Error: Failed to send Enter to session '{session}'", file=sys.stderr)
        return EXIT_TMUX_ERROR

    print(f"Message sent to session: {session}")
    return EXIT_SUCCESS


def handle_select(session: str, options: str) -> int:
    """处理 --select 命令"""
    if not options:
        print("Error: Option cannot be empty", file=sys.stderr)
        return EXIT_INVALID_ARGS

    if not TmuxClient.session_exists(session):
        print(f"Error: Session '{session}' not found", file=sys.stderr)
        return EXIT_SESSION_NOT_FOUND

    # 解析逗号分隔的选项，去除每个选项的首尾空格
    option_list = [opt.strip() for opt in options.split(",")]

    # 检查是否有空选项
    for opt in option_list:
        if not opt:
            print("Error: Option cannot be empty", file=sys.stderr)
            return EXIT_INVALID_ARGS

    # 依次发送每个选项
    for opt in option_list:
        if not TmuxClient.send_keys(session, opt, literal=True):
            print(f"Error: Failed to send option '{opt}' to session '{session}'", file=sys.stderr)
            return EXIT_TMUX_ERROR
        if not TmuxClient.send_enter(session):
            print(f"Error: Failed to send Enter to session '{session}'", file=sys.stderr)
            return EXIT_TMUX_ERROR

    print(f"Message sent to session: {session}")
    return EXIT_SUCCESS


def handle_approve(session: str) -> int:
    """处理 --approve 命令"""
    if not TmuxClient.session_exists(session):
        print(f"Error: Session '{session}' not found", file=sys.stderr)
        return EXIT_SESSION_NOT_FOUND

    if not TmuxClient.send_keys(session, "Y", literal=True):
        print(f"Error: Failed to send approval to session '{session}'", file=sys.stderr)
        return EXIT_TMUX_ERROR

    if not TmuxClient.send_enter(session):
        print(f"Error: Failed to send Enter to session '{session}'", file=sys.stderr)
        return EXIT_TMUX_ERROR

    print(f"Message sent to session: {session}")
    return EXIT_SUCCESS


def handle_reject(session: str) -> int:
    """处理 --reject 命令"""
    if not TmuxClient.session_exists(session):
        print(f"Error: Session '{session}' not found", file=sys.stderr)
        return EXIT_SESSION_NOT_FOUND

    if not TmuxClient.send_keys(session, "n", literal=True):
        print(f"Error: Failed to send rejection to session '{session}'", file=sys.stderr)
        return EXIT_TMUX_ERROR

    if not TmuxClient.send_enter(session):
        print(f"Error: Failed to send Enter to session '{session}'", file=sys.stderr)
        return EXIT_TMUX_ERROR

    print(f"Message sent to session: {session}")
    return EXIT_SUCCESS


def handle_list_sessions() -> int:
    """处理 --list-sessions 命令"""
    sessions = TmuxClient.list_sessions()
    for session in sessions:
        print(session)
    return EXIT_SUCCESS


def handle_list_panes(session: str | None = None) -> int:
    """处理 --list-panes 命令

    Args:
        session: 可选的 session/window/pane 目标，格式支持:
                - None 或 "": 列出所有 pane
                - "session": 列出指定 session 的所有 pane
                - "session:window": 列出指定 window 的所有 pane
    """
    target = session if session else ""
    panes = TmuxClient.list_panes(target)
    for pane in panes:
        print(pane)
    return EXIT_SUCCESS


def handle_version() -> int:
    """处理 --version 命令"""
    print(f"claude-ctl version {__version__}")
    return EXIT_SUCCESS


def main() -> None:
    """主入口"""
    args = parse_args()

    # --version
    if args.version:
        sys.exit(handle_version())

    # --list-sessions
    if args.list_sessions:
        sys.exit(handle_list_sessions())

    # --list-panes
    if args.list_panes:
        sys.exit(handle_list_panes(args.session))

    # 需要 --session 的操作
    if args.message is not None:
        if not args.session:
            print("Error: --session is required for --message", file=sys.stderr)
            sys.exit(EXIT_INVALID_ARGS)
        sys.exit(handle_message(args.session, args.message))

    if args.select is not None:
        if not args.session:
            print("Error: --session is required for --select", file=sys.stderr)
            sys.exit(EXIT_INVALID_ARGS)
        sys.exit(handle_select(args.session, args.select))

    if args.approve:
        if not args.session:
            print("Error: --session is required for --approve", file=sys.stderr)
            sys.exit(EXIT_INVALID_ARGS)
        sys.exit(handle_approve(args.session))

    if args.reject:
        if not args.session:
            print("Error: --session is required for --reject", file=sys.stderr)
            sys.exit(EXIT_INVALID_ARGS)
        sys.exit(handle_reject(args.session))

    # 没有指定任何操作
    print(
        "Error: Must specify one of: --message, --select, --approve, "
        "--reject, --list-sessions, --list-panes, --version",
        file=sys.stderr,
    )
    sys.exit(EXIT_INVALID_ARGS)


if __name__ == "__main__":
    main()
