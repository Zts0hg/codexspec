#!/usr/bin/env python3
"""
OutputFormatter 单元测试
Task 2.3: 编写 OutputFormatter 单元测试
"""

import sys
from pathlib import Path

import pytest

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from claude_monitor import (
    ErrorInfo,
    OutputFormatter,
    QuestionInfo,
    QuestionOption,
    SessionState,
    SessionStatus,
)


class TestFormatUserQuestion:
    """测试 format_user_question 输出格式"""

    def test_basic_user_question_output(self):
        """测试基本的用户询问输出格式"""
        questions = [
            QuestionInfo(
                question="你希望使用哪种输出格式？",
                header="Output Format",
                options=[
                    QuestionOption(label="JSON", description="便于程序解析"),
                    QuestionOption(label="Text", description="便于人工阅读"),
                ],
                multi_select=False,
            )
        ]

        output = OutputFormatter.format_user_question("91bba6d2-test", questions)

        # 验证输出包含必要信息
        assert "91bba6d2" in output
        assert "USER_QUESTION" in output
        assert "你希望使用哪种输出格式？" in output
        assert "Output Format" in output
        assert "JSON" in output
        assert "便于程序解析" in output
        assert "Text" in output
        assert "便于人工阅读" in output

    def test_multi_select_question_output(self):
        """测试多选问题的输出格式"""
        questions = [
            QuestionInfo(
                question="选择要启用的功能",
                header="Features",
                options=[
                    QuestionOption(label="A", description="功能A"),
                    QuestionOption(label="B", description="功能B"),
                ],
                multi_select=True,
            )
        ]

        output = OutputFormatter.format_user_question("test1234", questions)

        assert "Multi-select" in output or "multi-select" in output.lower()

    def test_multiple_questions_output(self):
        """测试多个问题的输出格式"""
        questions = [
            QuestionInfo(
                question="第一个问题",
                header="Q1",
                options=[QuestionOption(label="A", description="选项A")],
            ),
            QuestionInfo(
                question="第二个问题",
                header="Q2",
                options=[QuestionOption(label="B", description="选项B")],
            ),
        ]

        output = OutputFormatter.format_user_question("test1234", questions)

        assert "[1]" in output
        assert "[2]" in output
        assert "第一个问题" in output
        assert "第二个问题" in output

    def test_separator_format(self):
        """测试分隔符格式"""
        questions = [
            QuestionInfo(
                question="测试问题",
                header="Test",
                options=[QuestionOption(label="A", description="选项A")],
            )
        ]

        output = OutputFormatter.format_user_question("test1234", questions)

        # 验证分隔符
        assert "=" * 60 in output
        # 验证输出以分隔符开始和结束
        lines = output.strip().split("\n")
        assert lines[0] == "=" * 60
        assert lines[-1] == "=" * 60


class TestFormatErrorStop:
    """测试 format_error_stop 输出格式"""

    def test_basic_error_output(self):
        """测试基本的错误停止输出格式"""
        error_info = ErrorInfo(
            error_type="ToolExecutionError",
            message="Failed to execute tool: file not found",
        )

        output = OutputFormatter.format_error_stop("91bba6d2-test", error_info)

        # 验证输出包含必要信息
        assert "91bba6d2" in output
        assert "ERROR_STOP" in output
        assert "ToolExecutionError" in output
        assert "file not found" in output

    def test_error_with_tool_info(self):
        """测试包含工具信息的错误输出"""
        error_info = ErrorInfo(
            error_type="ToolExecutionError",
            message="Permission denied",
            tool_name="Read",
            tool_input={"file_path": "/etc/passwd"},
        )

        output = OutputFormatter.format_error_stop("test1234", error_info)

        assert "Read" in output
        assert "/etc/passwd" in output

    def test_error_separator_format(self):
        """测试错误输出分隔符格式"""
        error_info = ErrorInfo(
            error_type="TestError",
            message="Test error message",
        )

        output = OutputFormatter.format_error_stop("test1234", error_info)

        # 验证分隔符
        assert "=" * 60 in output


class TestFormatTaskComplete:
    """测试 format_task_complete 输出格式（向后兼容）"""

    def test_basic_task_complete_output(self):
        """测试基本的任务完成输出格式"""
        state = SessionState(
            session_id="test1234",
            status=SessionStatus.TASK_COMPLETE,
            last_stop_reason="end_turn",
            last_output="任务已完成",
        )

        output = OutputFormatter.format_task_complete("test1234", state)

        # 验证输出包含必要信息
        assert "test1234" in output
        assert "TASK_COMPLETE" in output
        assert "end_turn" in output
        assert "任务已完成" in output

    def test_task_complete_with_long_output(self):
        """测试长输出的截断"""
        long_output = "A" * 3000  # 超过 2000 字符
        state = SessionState(
            session_id="test1234",
            status=SessionStatus.TASK_COMPLETE,
            last_stop_reason="end_turn",
            last_output=long_output,
        )

        output = OutputFormatter.format_task_complete("test1234", state)

        # 验证输出被截断
        assert "truncated" in output
        assert len(output) < 4000  # 输出应该比原始内容短

    def test_task_complete_no_output(self):
        """测试没有输出内容的情况"""
        state = SessionState(
            session_id="test1234",
            status=SessionStatus.TASK_COMPLETE,
            last_stop_reason="end_turn",
            last_output=None,
        )

        output = OutputFormatter.format_task_complete("test1234", state)

        # 应该正常输出，不包含 Output: 行
        assert "test1234" in output
        assert "end_turn" in output

    def test_backward_compatibility(self):
        """测试向后兼容性 - 确保输出格式与之前一致"""
        state = SessionState(
            session_id="91bba6d2-test",
            status=SessionStatus.TASK_COMPLETE,
            last_stop_reason="end_turn",
            last_output="Hello World",
        )

        output = OutputFormatter.format_task_complete("91bba6d2", state)

        # 验证基本格式
        lines = output.strip().split("\n")
        assert "=" * 60 in lines
        assert any("91bba6d2" in line for line in lines)


class TestOutputConsistency:
    """测试输出格式一致性"""

    def test_all_formats_use_separator(self):
        """验证所有格式都使用相同的分隔符"""
        questions = [
            QuestionInfo(
                question="测试",
                header="Test",
                options=[QuestionOption(label="A", description="选项A")],
            )
        ]
        error_info = ErrorInfo(error_type="Test", message="Test")
        state = SessionState(
            session_id="test",
            status=SessionStatus.TASK_COMPLETE,
            last_stop_reason="end_turn",
            last_output="Test",
        )

        q_output = OutputFormatter.format_user_question("test", questions)
        e_output = OutputFormatter.format_error_stop("test", error_info)
        t_output = OutputFormatter.format_task_complete("test", state)

        separator = "=" * 60
        assert separator in q_output
        assert separator in e_output
        assert separator in t_output

    def test_session_id_truncation(self):
        """验证 session ID 被正确截断为前 8 位"""
        long_session_id = "abcdefghijklmnopqrstuvwxyz1234567890"

        questions = [
            QuestionInfo(
                question="测试",
                header="Test",
                options=[QuestionOption(label="A", description="选项A")],
            )
        ]

        output = OutputFormatter.format_user_question(long_session_id, questions)

        # 应该只显示前 8 位
        assert "abcdefgh" in output
        # 不应该显示完整的 session ID
        assert "abcdefghijklmnopqrstuvwxyz" not in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
