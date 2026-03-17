#!/usr/bin/env python3
"""
ClaudeSessionMonitor 扩展单元测试
Task 3.1: 为 ClaudeSessionMonitor 的新回调功能编写单元测试
"""

import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from claude_monitor import (
    ClaudeSessionMonitor,
    SessionStatus,
)


class TestMonitorCallbacks:
    """测试 ClaudeSessionMonitor 回调功能"""

    def test_on_user_question_callback_triggered(self):
        """测试 on_user_question 回调触发"""
        callback = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
                on_user_question=callback,
            )

            # 模拟 AskUserQuestion 消息 (使用 questions 数组格式)
            message = {
                "type": "assistant",
                "message": {
                    "stop_reason": "tool_use",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "AskUserQuestion",
                            "input": {
                                "questions": [
                                    {
                                        "question": "选择格式",
                                        "header": "Format",
                                        "options": [
                                            {"label": "JSON", "description": "JSON 格式"},
                                        ],
                                        "multiSelect": False,
                                    }
                                ]
                            },
                        }
                    ],
                },
            }

            monitor._process_message("test-session-001", message)

            # 验证回调被触发
            assert callback.called
            call_args = callback.call_args
            assert call_args[0][0] == "test-session-001"
            questions = call_args[0][1]
            assert len(questions) == 1
            assert questions[0].question == "选择格式"

    def test_on_error_stop_callback_triggered(self):
        """测试 on_error_stop 回调触发"""
        callback = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
                on_error_stop=callback,
            )

            # 模拟错误停止消息
            message = {
                "type": "assistant",
                "message": {
                    "stop_reason": "refusal",
                    "content": [
                        {
                            "type": "text",
                            "text": "I cannot help with that request.",
                        }
                    ],
                },
            }

            monitor._process_message("test-session-002", message)

            # 验证回调被触发
            assert callback.called
            call_args = callback.call_args
            assert call_args[0][0] == "test-session-002"
            error_info = call_args[0][1]
            assert error_info.error_type == "refusal"

    def test_on_complete_callback_still_works(self):
        """测试现有的 on_complete 回调仍然工作"""
        callback = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
                on_complete=callback,
            )

            # 模拟任务完成消息
            message = {
                "type": "assistant",
                "message": {
                    "stop_reason": "end_turn",
                    "content": [
                        {
                            "type": "text",
                            "text": "Task completed successfully.",
                        }
                    ],
                },
            }

            monitor._process_message("test-session-003", message)

            # 验证回调被触发
            assert callback.called


class TestStateChangeDetection:
    """测试状态变化检测逻辑"""

    def test_status_updated_in_session_state(self):
        """测试 SessionState 中的 status 字段被正确更新"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
            )

            # 模拟流式输出消息
            message = {
                "type": "assistant",
                "message": {
                    "stop_reason": None,
                    "content": [{"type": "text", "text": "Streaming..."}],
                },
            }

            monitor._process_message("test-session", message)

            state = monitor.get_session_state("test-session")
            assert state is not None
            assert state.status == SessionStatus.STREAMING

    def test_status_transitions_correctly(self):
        """测试状态正确转换"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
            )

            # 1. 流式输出
            message1 = {
                "type": "assistant",
                "message": {
                    "stop_reason": None,
                    "content": [{"type": "text", "text": "Working..."}],
                },
            }
            monitor._process_message("test-session", message1)
            state = monitor.get_session_state("test-session")
            assert state.status == SessionStatus.STREAMING

            # 2. 工具调用 - 现在返回 PENDING_PERMISSION
            message2 = {
                "type": "assistant",
                "message": {
                    "stop_reason": "tool_use",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Read",
                            "input": {"file_path": "/tmp/test.txt"},
                        }
                    ],
                },
            }
            monitor._process_message("test-session", message2)
            state = monitor.get_session_state("test-session")
            # 工具调用现在返回 TOOL_USE (而不是 PENDING_PERMISSION)
            # 大多数工具自动执行，不需要用户确认
            assert state.status == SessionStatus.TOOL_USE

            # 3. 任务完成
            message3 = {
                "type": "assistant",
                "message": {
                    "stop_reason": "end_turn",
                    "content": [{"type": "text", "text": "Done!"}],
                },
            }
            monitor._process_message("test-session", message3)
            state = monitor.get_session_state("test-session")
            assert state.status == SessionStatus.TASK_COMPLETE

    def test_questions_stored_in_state(self):
        """测试问题信息被存储在 SessionState 中"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
            )

            message = {
                "type": "assistant",
                "message": {
                    "stop_reason": "tool_use",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "AskUserQuestion",
                            "input": {
                                "questions": [
                                    {
                                        "question": "选择颜色",
                                        "header": "Color",
                                        "options": [
                                            {"label": "Red", "description": "红色"},
                                            {"label": "Blue", "description": "蓝色"},
                                        ],
                                        "multiSelect": False,
                                    }
                                ]
                            },
                        }
                    ],
                },
            }

            monitor._process_message("test-session", message)

            state = monitor.get_session_state("test-session")
            assert state is not None
            assert len(state.questions) == 1
            assert state.questions[0].question == "选择颜色"
            assert state.status == SessionStatus.USER_QUESTION

    def test_error_info_stored_in_state(self):
        """测试错误信息被存储在 SessionState 中"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
            )

            message = {
                "type": "assistant",
                "message": {
                    "stop_reason": "refusal",
                    "content": [
                        {
                            "type": "text",
                            "text": "I cannot help with that.",
                        }
                    ],
                },
            }

            monitor._process_message("test-session", message)

            state = monitor.get_session_state("test-session")
            assert state is not None
            assert state.error_info is not None
            assert state.error_info.error_type == "refusal"
            assert state.status == SessionStatus.ERROR_STOP


class TestMultipleQuestions:
    """测试连续多个询问的边界情况"""

    def test_consecutive_questions_trigger_separate_callbacks(self):
        """测试连续多个问题各自触发回调"""
        callback = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
                on_user_question=callback,
            )

            # 第一个问题
            message1 = {
                "type": "assistant",
                "message": {
                    "stop_reason": "tool_use",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "AskUserQuestion",
                            "input": {
                                "questions": [
                                    {
                                        "question": "第一个问题",
                                        "header": "Q1",
                                        "options": [{"label": "A", "description": "选项A"}],
                                        "multiSelect": False,
                                    }
                                ]
                            },
                        }
                    ],
                },
            }
            monitor._process_message("test-session", message1)

            # 第二个问题
            message2 = {
                "type": "assistant",
                "message": {
                    "stop_reason": "tool_use",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "AskUserQuestion",
                            "input": {
                                "questions": [
                                    {
                                        "question": "第二个问题",
                                        "header": "Q2",
                                        "options": [{"label": "B", "description": "选项B"}],
                                        "multiSelect": False,
                                    }
                                ]
                            },
                        }
                    ],
                },
            }
            monitor._process_message("test-session", message2)

            # 验证回调被触发两次
            assert callback.call_count == 2

    def test_state_tracks_all_questions(self):
        """测试状态追踪所有问题"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
            )

            # 发送两个问题
            for i in range(1, 3):
                message = {
                    "type": "assistant",
                    "message": {
                        "stop_reason": "tool_use",
                        "content": [
                            {
                                "type": "tool_use",
                                "name": "AskUserQuestion",
                                "input": {
                                    "questions": [
                                        {
                                            "question": f"问题{i}",
                                            "header": f"Q{i}",
                                            "options": [{"label": f"Opt{i}", "description": f"选项{i}"}],
                                            "multiSelect": False,
                                        }
                                    ]
                                },
                            }
                        ],
                    },
                }
                monitor._process_message("test-session", message)

            state = monitor.get_session_state("test-session")
            # 注意：每次新消息会重置 questions 列表
            # 所以只有最后一个问题
            assert len(state.questions) == 1
            assert state.questions[0].question == "问题2"


class TestBackwardCompatibility:
    """测试向后兼容性"""

    def test_init_without_new_callbacks(self):
        """测试不传新回调参数时的兼容性"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # 不传新回调参数
            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
            )

            # 应该正常工作
            assert monitor is not None
            assert monitor.on_user_question is None
            assert monitor.on_error_stop is None

    def test_on_complete_still_works_with_new_callbacks(self):
        """测试 on_complete 与新回调共存"""
        user_question_callback = MagicMock()
        error_stop_callback = MagicMock()
        complete_callback = MagicMock()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            monitor = ClaudeSessionMonitor(
                project_dir=tmpdir,
                quiet=True,
                on_user_question=user_question_callback,
                on_error_stop=error_stop_callback,
                on_complete=complete_callback,
            )

            # 模拟任务完成
            message = {
                "type": "assistant",
                "message": {
                    "stop_reason": "end_turn",
                    "content": [{"type": "text", "text": "Done"}],
                },
            }
            monitor._process_message("test-session", message)

            # on_complete 应该被触发
            assert complete_callback.called


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
