#!/usr/bin/env python3
"""
Tests for claude_ctl.py

测试覆盖:
- CLI 参数解析
- TmuxClient 方法
- Action handlers
- 集成测试
- 边界场景
"""

import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

import claude_ctl

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def mock_subprocess_run():
    """Mock subprocess.run for tmux commands"""
    with patch("claude_ctl.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
        yield mock_run


@pytest.fixture
def tmux_client():
    """TmuxClient instance for testing"""
    return claude_ctl.TmuxClient()


# ============================================================================
# CLI Parser Tests (Task 2.1)
# ============================================================================


class TestParseArgs:
    """测试 CLI 参数解析"""

    def test_parse_session_and_message(self):
        """测试 --session 和 --message 解析"""
        with patch("sys.argv", ["claude-ctl", "--session", "test-session", "--message", "hello"]):
            args = claude_ctl.parse_args()
            assert args.session == "test-session"
            assert args.message == "hello"

    def test_parse_session_and_select(self):
        """测试 --session 和 --select 解析"""
        with patch("sys.argv", ["claude-ctl", "--session", "test-session", "--select", "A,B,C"]):
            args = claude_ctl.parse_args()
            assert args.session == "test-session"
            assert args.select == "A,B,C"

    def test_parse_approve(self):
        """测试 --approve 解析"""
        with patch("sys.argv", ["claude-ctl", "--session", "test-session", "--approve"]):
            args = claude_ctl.parse_args()
            assert args.session == "test-session"
            assert args.approve is True

    def test_parse_reject(self):
        """测试 --reject 解析"""
        with patch("sys.argv", ["claude-ctl", "--session", "test-session", "--reject"]):
            args = claude_ctl.parse_args()
            assert args.session == "test-session"
            assert args.reject is True

    def test_parse_list_sessions(self):
        """测试 --list-sessions 解析"""
        with patch("sys.argv", ["claude-ctl", "--list-sessions"]):
            args = claude_ctl.parse_args()
            assert args.list_sessions is True

    def test_parse_version(self):
        """测试 --version 解析"""
        with patch("sys.argv", ["claude-ctl", "--version"]):
            args = claude_ctl.parse_args()
            assert args.version is True

    def test_mutual_exclusion_message_and_approve(self):
        """测试 --message 和 --approve 互斥"""
        with patch("sys.argv", ["claude-ctl", "--session", "test", "--message", "hi", "--approve"]):
            with pytest.raises(SystemExit) as exc_info:
                claude_ctl.parse_args()
            assert exc_info.value.code == claude_ctl.EXIT_INVALID_ARGS

    def test_mutual_exclusion_message_and_reject(self):
        """测试 --message 和 --reject 互斥"""
        with patch("sys.argv", ["claude-ctl", "--session", "test", "--message", "hi", "--reject"]):
            with pytest.raises(SystemExit) as exc_info:
                claude_ctl.parse_args()
            assert exc_info.value.code == claude_ctl.EXIT_INVALID_ARGS

    def test_mutual_exclusion_select_and_approve(self):
        """测试 --select 和 --approve 互斥"""
        with patch("sys.argv", ["claude-ctl", "--session", "test", "--select", "A", "--approve"]):
            with pytest.raises(SystemExit) as exc_info:
                claude_ctl.parse_args()
            assert exc_info.value.code == claude_ctl.EXIT_INVALID_ARGS

    def test_mutual_exclusion_approve_and_reject(self):
        """测试 --approve 和 --reject 互斥"""
        with patch("sys.argv", ["claude-ctl", "--session", "test", "--approve", "--reject"]):
            with pytest.raises(SystemExit) as exc_info:
                claude_ctl.parse_args()
            assert exc_info.value.code == claude_ctl.EXIT_INVALID_ARGS


# ============================================================================
# TmuxClient Tests (Task 2.3)
# ============================================================================


class TestTmuxClientSessionExists:
    """测试 TmuxClient.session_exists()"""

    def test_session_exists_true(self, mock_subprocess_run):
        """测试 session 存在"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        result = claude_ctl.TmuxClient.session_exists("test-session")
        assert result is True
        mock_subprocess_run.assert_called_once()

    def test_session_exists_false(self, mock_subprocess_run):
        """测试 session 不存在"""
        mock_subprocess_run.return_value = MagicMock(returncode=1)
        result = claude_ctl.TmuxClient.session_exists("nonexistent")
        assert result is False

    def test_session_exists_timeout(self, mock_subprocess_run):
        """测试 tmux 命令超时"""
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired(cmd="tmux", timeout=5)
        result = claude_ctl.TmuxClient.session_exists("test-session")
        assert result is False

    def test_session_exists_tmux_not_found(self, mock_subprocess_run):
        """测试 tmux 命令不存在"""
        mock_subprocess_run.side_effect = FileNotFoundError
        result = claude_ctl.TmuxClient.session_exists("test-session")
        assert result is False


class TestTmuxClientListSessions:
    """测试 TmuxClient.list_sessions()"""

    def test_list_sessions_success(self, mock_subprocess_run):
        """测试成功列出 sessions"""
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="session1\nsession2\nsession3\n", stderr="")
        result = claude_ctl.TmuxClient.list_sessions()
        assert result == ["session1", "session2", "session3"]

    def test_list_sessions_empty(self, mock_subprocess_run):
        """测试无 sessions"""
        mock_subprocess_run.return_value = MagicMock(returncode=1, stdout="", stderr="")
        result = claude_ctl.TmuxClient.list_sessions()
        assert result == []

    def test_list_sessions_tmux_error(self, mock_subprocess_run):
        """测试 tmux 命令失败"""
        mock_subprocess_run.side_effect = subprocess.TimeoutExpired(cmd="tmux", timeout=5)
        result = claude_ctl.TmuxClient.list_sessions()
        assert result == []


class TestTmuxClientSendKeys:
    """测试 TmuxClient.send_keys()"""

    def test_send_keys_literal(self, mock_subprocess_run):
        """测试按字面发送"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        result = claude_ctl.TmuxClient.send_keys("test-session", "hello world", literal=True)
        assert result is True
        # Verify -l flag is used
        call_args = mock_subprocess_run.call_args[0][0]
        assert "-l" in call_args

    def test_send_keys_non_literal(self, mock_subprocess_run):
        """测试非字面发送"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        result = claude_ctl.TmuxClient.send_keys("test-session", "hello", literal=False)
        assert result is True

    def test_send_keys_failure(self, mock_subprocess_run):
        """测试发送失败"""
        mock_subprocess_run.return_value = MagicMock(returncode=1)
        result = claude_ctl.TmuxClient.send_keys("test-session", "hello")
        assert result is False


class TestTmuxClientSendEnter:
    """测试 TmuxClient.send_enter()"""

    def test_send_enter_success(self, mock_subprocess_run):
        """测试发送 Enter 成功"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        result = claude_ctl.TmuxClient.send_enter("test-session")
        assert result is True
        call_args = mock_subprocess_run.call_args[0][0]
        assert "Enter" in call_args

    def test_send_enter_failure(self, mock_subprocess_run):
        """测试发送 Enter 失败"""
        mock_subprocess_run.return_value = MagicMock(returncode=1)
        result = claude_ctl.TmuxClient.send_enter("test-session")
        assert result is False


# ============================================================================
# Handler Tests (Task 3.1, 3.3, 3.5, 3.7)
# ============================================================================


class TestHandleMessage:
    """测试 handle_message()"""

    def test_handle_message_success(self, mock_subprocess_run):
        """测试正常消息发送"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_message("test-session", "hello world")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_message_with_spaces(self, mock_subprocess_run):
        """测试包含空格的消息"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_message("test-session", "请帮我完成这个任务")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_message_with_special_chars(self, mock_subprocess_run):
        """测试包含特殊字符的消息"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_message("test-session", '测试引号"和反斜杠\\')
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_message_empty_allowed(self, mock_subprocess_run):
        """测试空消息（允许）"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_message("test-session", "")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_message_session_not_found(self, mock_subprocess_run):
        """测试 session 不存在"""
        with patch("claude_ctl.TmuxClient.session_exists", return_value=False):
            result = claude_ctl.handle_message("nonexistent", "hello")
        assert result == claude_ctl.EXIT_SESSION_NOT_FOUND


class TestHandleSelect:
    """测试 handle_select()"""

    def test_handle_select_single(self, mock_subprocess_run):
        """测试单选"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_select("test-session", "A")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_select_multiple(self, mock_subprocess_run):
        """测试多选"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_select("test-session", "A,B,C")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_select_with_spaces(self, mock_subprocess_run):
        """测试选项包含首尾空格"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_select("test-session", "A, B, C")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_select_empty_rejected(self, mock_subprocess_run):
        """测试空选项（拒绝）"""
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_select("test-session", "")
        assert result == claude_ctl.EXIT_INVALID_ARGS

    def test_handle_select_duplicate_options(self, mock_subprocess_run):
        """测试重复选项（按原样发送）"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_select("test-session", "A,A,B")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_select_session_not_found(self, mock_subprocess_run):
        """测试 session 不存在"""
        with patch("claude_ctl.TmuxClient.session_exists", return_value=False):
            result = claude_ctl.handle_select("nonexistent", "A")
        assert result == claude_ctl.EXIT_SESSION_NOT_FOUND


class TestHandleApproveReject:
    """测试 handle_approve() 和 handle_reject()"""

    def test_handle_approve_success(self, mock_subprocess_run):
        """测试批准操作"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_approve("test-session")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_reject_success(self, mock_subprocess_run):
        """测试拒绝操作"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_reject("test-session")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_approve_session_not_found(self, mock_subprocess_run):
        """测试批准操作 session 不存在"""
        with patch("claude_ctl.TmuxClient.session_exists", return_value=False):
            result = claude_ctl.handle_approve("nonexistent")
        assert result == claude_ctl.EXIT_SESSION_NOT_FOUND

    def test_handle_reject_session_not_found(self, mock_subprocess_run):
        """测试拒绝操作 session 不存在"""
        with patch("claude_ctl.TmuxClient.session_exists", return_value=False):
            result = claude_ctl.handle_reject("nonexistent")
        assert result == claude_ctl.EXIT_SESSION_NOT_FOUND


class TestHandleListSessions:
    """测试 handle_list_sessions()"""

    def test_handle_list_sessions_success(self, mock_subprocess_run):
        """测试成功列出 sessions"""
        mock_subprocess_run.return_value = MagicMock(returncode=0, stdout="session1\nsession2\n", stderr="")
        with patch("claude_ctl.TmuxClient.list_sessions", return_value=["session1", "session2"]):
            result = claude_ctl.handle_list_sessions()
        assert result == claude_ctl.EXIT_SUCCESS

    def test_handle_list_sessions_empty(self, mock_subprocess_run):
        """测试无 sessions"""
        with patch("claude_ctl.TmuxClient.list_sessions", return_value=[]):
            result = claude_ctl.handle_list_sessions()
        assert result == claude_ctl.EXIT_SUCCESS


# ============================================================================
# Integration Tests (Task 4.2)
# ============================================================================


class TestIntegration:
    """集成测试 - 测试完整命令流程"""

    def test_full_message_flow(self, mock_subprocess_run):
        """测试 TC-001: 发送简单消息"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("sys.argv", ["claude-ctl", "--session", "claude-main", "--message", "继续工作"]):
            with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
                with pytest.raises(SystemExit) as exc_info:
                    claude_ctl.main()
                assert exc_info.value.code == claude_ctl.EXIT_SUCCESS

    def test_full_select_flow(self, mock_subprocess_run):
        """测试 TC-004: 单选选项"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("sys.argv", ["claude-ctl", "--session", "claude-main", "--select", "A"]):
            with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
                with pytest.raises(SystemExit) as exc_info:
                    claude_ctl.main()
                assert exc_info.value.code == claude_ctl.EXIT_SUCCESS

    def test_full_approve_flow(self, mock_subprocess_run):
        """测试 TC-006: 批准权限"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("sys.argv", ["claude-ctl", "--session", "claude-main", "--approve"]):
            with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
                with pytest.raises(SystemExit) as exc_info:
                    claude_ctl.main()
                assert exc_info.value.code == claude_ctl.EXIT_SUCCESS

    def test_session_not_found_flow(self, mock_subprocess_run):
        """测试 TC-008: Session 不存在"""
        with patch("sys.argv", ["claude-ctl", "--session", "nonexistent", "--message", "test"]):
            with patch("claude_ctl.TmuxClient.session_exists", return_value=False):
                with pytest.raises(SystemExit) as exc_info:
                    claude_ctl.main()
                assert exc_info.value.code == claude_ctl.EXIT_SESSION_NOT_FOUND

    def test_mutual_exclusion_flow(self, mock_subprocess_run):
        """测试 TC-009: 互斥参数冲突"""
        with patch("sys.argv", ["claude-ctl", "--session", "claude-main", "--message", "test", "--approve"]):
            with pytest.raises(SystemExit) as exc_info:
                claude_ctl.main()
            assert exc_info.value.code == claude_ctl.EXIT_INVALID_ARGS

    def test_missing_action_flow(self, mock_subprocess_run):
        """测试 TC-010: 缺少操作参数"""
        with patch("sys.argv", ["claude-ctl", "--session", "claude-main"]):
            with pytest.raises(SystemExit) as exc_info:
                claude_ctl.main()
            assert exc_info.value.code == claude_ctl.EXIT_INVALID_ARGS

    def test_list_sessions_flow(self, mock_subprocess_run):
        """测试 TC-011: 列出会话"""
        with patch("sys.argv", ["claude-ctl", "--list-sessions"]):
            with patch("claude_ctl.TmuxClient.list_sessions", return_value=["session1", "session2"]):
                with pytest.raises(SystemExit) as exc_info:
                    claude_ctl.main()
                assert exc_info.value.code == claude_ctl.EXIT_SUCCESS

    def test_version_flow(self):
        """测试 --version"""
        with patch("sys.argv", ["claude-ctl", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                claude_ctl.main()
            assert exc_info.value.code == claude_ctl.EXIT_SUCCESS


# ============================================================================
# Edge Case Tests (Task 5.1)
# ============================================================================


class TestEdgeCases:
    """边界场景测试 - 覆盖 EC-001 到 EC-006"""

    def test_ec001_empty_message_allowed(self, mock_subprocess_run):
        """EC-001: 空消息（允许）"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_message("test-session", "")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_ec002_empty_option_rejected(self, mock_subprocess_run):
        """EC-002: 空选项（拒绝）"""
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_select("test-session", "")
        assert result == claude_ctl.EXIT_INVALID_ARGS

    def test_ec003_select_with_spaces(self, mock_subprocess_run):
        """EC-003: 多选包含空格"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_select("test-session", "A, B, C")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_ec004_duplicate_options(self, mock_subprocess_run):
        """EC-004: 多选重复选项"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_select("test-session", "A,A,B")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_ec005_session_name_with_special_chars(self, mock_subprocess_run):
        """EC-005: Session 名称包含特殊字符"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_message("my-session_123", "hello")
        assert result == claude_ctl.EXIT_SUCCESS

    def test_ec006_message_with_newline_literal(self, mock_subprocess_run):
        """EC-006: 消息包含换行符（字面发送）"""
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        with patch("claude_ctl.TmuxClient.session_exists", return_value=True):
            result = claude_ctl.handle_message("test-session", "第一行\\n第二行")
        assert result == claude_ctl.EXIT_SUCCESS


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
