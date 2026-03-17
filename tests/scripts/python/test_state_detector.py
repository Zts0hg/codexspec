#!/usr/bin/env python3
"""
StateDetector 单元测试
Task 2.1: 编写 StateDetector 单元测试
"""

import sys
from pathlib import Path

import pytest

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from claude_monitor import (
    SessionStatus,
    StateDetector,
)


class TestStateDetectorStreaming:
    """测试 STREAMING 状态检测"""

    def test_streaming_when_stop_reason_is_null(self):
        """stop_reason=null 时应为 STREAMING"""
        message = {
            "stop_reason": None,
            "content": [{"type": "text", "text": "Hello"}],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.STREAMING
        assert question is None
        assert error is None
        assert tools == []

    def test_streaming_when_no_stop_reason_field(self):
        """没有 stop_reason 字段时也应为 STREAMING"""
        message = {
            "content": [{"type": "text", "text": "Hello"}],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.STREAMING


class TestStateDetectorUserQuestion:
    """测试 USER_QUESTION 状态检测"""

    def test_user_question_with_ask_user_question_tool(self):
        """检测 AskUserQuestion 工具调用"""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [
                            {
                                "question": "你希望使用哪种输出格式？",
                                "header": "Output Format",
                                "options": [
                                    {"label": "JSON", "description": "便于程序解析"},
                                    {"label": "Text", "description": "便于人工阅读"},
                                ],
                                "multiSelect": False,
                            }
                        ]
                    },
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.USER_QUESTION
        assert question is not None
        assert question.question == "你希望使用哪种输出格式？"
        assert question.header == "Output Format"
        assert len(question.options) == 2
        assert question.options[0].label == "JSON"
        assert question.options[0].description == "便于程序解析"
        assert question.multi_select is False

    def test_user_question_with_multi_select(self):
        """检测多选问题的 AskUserQuestion"""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [
                            {
                                "question": "选择要启用的功能",
                                "header": "Features",
                                "options": [
                                    {"label": "A", "description": "功能A"},
                                    {"label": "B", "description": "功能B"},
                                ],
                                "multiSelect": True,
                            }
                        ]
                    },
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.USER_QUESTION
        assert question is not None
        assert question.multi_select is True

    def test_not_user_question_for_other_tools(self):
        """其他工具调用不应触发 USER_QUESTION"""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "Read",
                    "input": {"file_path": "/tmp/test.txt"},
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status != SessionStatus.USER_QUESTION
        assert question is None


class TestStateDetectorErrorStop:
    """测试 ERROR_STOP 状态检测"""

    def test_error_stop_with_refusal(self):
        """检测 refusal 类型的错误停止"""
        message = {
            "stop_reason": "refusal",
            "content": [
                {
                    "type": "text",
                    "text": "I cannot help with that request.",
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.ERROR_STOP
        assert error is not None

        assert error.error_type == "refusal"

    def test_error_stop_with_error_content(self):
        """检测包含错误信息的停止"""
        message = {
            "stop_reason": "error",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "xxx",
                    "content": "Error: File not found",
                    "is_error": True,
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.ERROR_STOP
        assert error is not None

    def test_not_error_stop_for_normal_tool_use(self):
        """正常工具调用不应触发 ERROR_STOP"""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "Read",
                    "input": {"file_path": "/tmp/test.txt"},
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status != SessionStatus.ERROR_STOP

    def test_not_error_stop_for_end_turn(self):
        """end_turn 不应是 ERROR_STOP"""
        message = {
            "stop_reason": "end_turn",
            "content": [{"type": "text", "text": "Done"}],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status != SessionStatus.ERROR_STOP


class TestStateDetectorTaskComplete:
    """测试 TASK_COMPLETE 状态检测"""

    def test_task_complete_with_end_turn(self):
        """end_turn 应为 TASK_COMPLETE"""
        message = {
            "stop_reason": "end_turn",
            "content": [{"type": "text", "text": "Task completed"}],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_task_complete_with_stop_sequence(self):
        """stop_sequence 应为 TASK_COMPLETE"""
        message = {
            "stop_reason": "stop_sequence",
            "content": [{"type": "text", "text": "Stopped"}],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_task_complete_with_max_tokens(self):
        """max_tokens 应为 TASK_COMPLETE"""
        message = {
            "stop_reason": "max_tokens",
            "content": [{"type": "text", "text": "Truncated"}],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE


class TestStateDetectorToolUse:
    """测试 TOOL_USE 状态检测"""

    def test_tool_use_for_normal_tool(self):
        """普通工具调用应返回 TOOL_USE（大多数工具自动执行）"""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "Read",
                    "input": {"file_path": "/tmp/test.txt"},
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        # 工具调用时返回 TOOL_USE，而不是 PENDING_PERMISSION
        # 避免对每个工具调用都发送权限请求通知
        assert status == SessionStatus.TOOL_USE
        assert len(tools) == 1
        assert tools[0].tool_name == "Read"

    def test_tool_use_for_bash_tool(self):
        """Bash 工具调用应返回 TOOL_USE"""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "Bash",
                    "input": {"command": "ls -la"},
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TOOL_USE
        assert len(tools) == 1
        assert tools[0].tool_name == "Bash"


class TestStateDetectorEdgeCases:
    """测试边界情况"""

    def test_empty_content(self):
        """空内容处理"""
        message = {
            "stop_reason": "end_turn",
            "content": [],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_multiple_tool_uses(self):
        """多个工具调用的处理"""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "Read",
                    "input": {"file_path": "/tmp/a.txt"},
                },
                {
                    "type": "tool_use",
                    "name": "Write",
                    "input": {"file_path": "/tmp/b.txt", "content": "..."},
                },
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        # 工具调用返回 TOOL_USE
        assert status == SessionStatus.TOOL_USE
        assert len(tools) == 2

    def test_mixed_content_types(self):
        """混合内容类型的处理"""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {"type": "text", "text": "Let me read that file."},
                {
                    "type": "tool_use",
                    "name": "Read",
                    "input": {"file_path": "/tmp/test.txt"},
                },
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        # 工具调用返回 TOOL_USE
        assert status == SessionStatus.TOOL_USE

    def test_unknown_stop_reason(self):
        """未知 stop_reason 处理"""
        message = {
            "stop_reason": "unknown_reason",
            "content": [{"type": "text", "text": "Something"}],
        }
        status, question, tools, error = StateDetector.detect(message)
        # 未知原因，没有错误内容，应该是 TASK_COMPLETE
        assert status == SessionStatus.TASK_COMPLETE


class TestExtractQuestion:
    """测试 _extract_question 方法"""

    def test_extract_question_with_valid_input(self):
        """测试正常提取问题信息"""
        content = [
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
        ]
        question = StateDetector._extract_question(content)
        assert question is not None
        assert question.question == "选择颜色"
        assert question.header == "Color"
        assert len(question.options) == 2

    def test_extract_question_no_ask_user_question(self):
        """没有 AskUserQuestion 时返回 None"""
        content = [
            {
                "type": "tool_use",
                "name": "Read",
                "input": {"file_path": "/tmp/test.txt"},
            }
        ]
        question = StateDetector._extract_question(content)
        assert question is None

    def test_extract_question_empty_content(self):
        """空内容返回 None"""
        question = StateDetector._extract_question([])
        assert question is None


class TestExtractError:
    """测试 _extract_error 方法"""

    def test_extract_error_from_tool_result(self):
        """从 tool_result 提取错误"""
        content = [
            {
                "type": "tool_result",
                "tool_use_id": "xxx",
                "content": "Error: Permission denied",
                "is_error": True,
            }
        ]
        message = {"content": content, "stop_reason": "error"}
        error = StateDetector._extract_error(message)
        assert error is not None
        assert "Error" in error.message or "Permission" in error.message

        assert error.error_type == "tool_execution_error"

    def test_extract_error_no_error(self):
        """没有错误时返回 None"""
        content = [{"type": "text", "text": "Success"}]
        message = {"content": content, "stop_reason": "end_turn"}
        error = StateDetector._extract_error(message)
        assert error is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
