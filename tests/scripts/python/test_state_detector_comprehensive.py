#!/usr/bin/env python3
"""
Comprehensive StateDetector Tests

Tests StateDetector.detect() with:
- Real message samples extracted from actual JSONL files
- Edge cases and boundary conditions
- All message types: STREAMING, TOOL_USE, USER_QUESTION, ERROR_STOP, TASK_COMPLETE
"""

import sys
from pathlib import Path

import pytest

# Add project path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from claude_monitor import (
    SessionStatus,
    StateDetector,
)


class TestStateDetectorStreaming:
    """Test STREAMING state detection."""

    def test_streaming_when_stop_reason_is_null(self, sample_messages):
        """stop_reason=null should be detected as STREAMING."""
        message = sample_messages["STREAMING"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.STREAMING
        assert question is None
        assert tools == []
        assert error is None

    def test_streaming_when_no_stop_reason_field(self):
        """Missing stop_reason field should also be STREAMING."""
        message = {"content": [{"type": "text", "text": "Hello"}]}
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.STREAMING

    def test_streaming_with_thinking_content(self):
        """STREAMING with thinking content."""
        message = {
            "stop_reason": None,
            "content": [
                {"type": "thinking", "thinking": "Let me think about this..."},
                {"type": "text", "text": "Working on it..."},
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.STREAMING

    def test_streaming_with_real_messages(self, real_messages):
        """Test STREAMING detection with real extracted messages."""
        streaming_msgs = real_messages.get("STREAMING", [])
        for msg in streaming_msgs[:3]:  # Test first 3
            status, question, tools, error = StateDetector.detect(msg)
            assert status == SessionStatus.STREAMING, f"Expected STREAMING, got {status}"


class TestStateDetectorToolUse:
    """Test TOOL_USE state detection."""

    def test_tool_use_read_tool(self, sample_messages):
        """Read tool should be detected as TOOL_USE."""
        message = sample_messages["TOOL_USE_READ"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TOOL_USE
        assert len(tools) == 1
        assert tools[0].tool_name == "Read"
        assert tools[0].tool_input["file_path"] == "/tmp/test.txt"
        assert question is None
        assert error is None

    def test_tool_use_bash_tool(self, sample_messages):
        """Bash tool should be detected as TOOL_USE."""
        message = sample_messages["TOOL_USE_BASH"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TOOL_USE
        assert len(tools) == 1
        assert tools[0].tool_name == "Bash"
        assert tools[0].tool_input["command"] == "ls -la"

    def test_tool_use_write_tool(self, sample_messages):
        """Write tool should be detected as TOOL_USE."""
        message = sample_messages["TOOL_USE_WRITE"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TOOL_USE
        assert len(tools) == 1
        assert tools[0].tool_name == "Write"

    def test_multiple_tool_uses(self):
        """Multiple tool uses should all be extracted."""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {"type": "tool_use", "name": "Read", "id": "t1", "input": {"file_path": "/a.txt"}},
                {"type": "tool_use", "name": "Write", "id": "t2", "input": {"file_path": "/b.txt", "content": "..."}},
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TOOL_USE
        assert len(tools) == 2
        assert tools[0].tool_name == "Read"
        assert tools[1].tool_name == "Write"

    def test_tool_use_with_description(self):
        """Tool use with description should preserve description."""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "Bash",
                    "id": "t1",
                    "input": {"command": "ls", "description": "List files"},
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TOOL_USE
        assert tools[0].description == "List files"

    def test_tool_use_with_real_messages(self, real_messages):
        """Test TOOL_USE detection with real extracted messages."""
        tool_use_msgs = real_messages.get("TOOL_USE", [])
        for msg in tool_use_msgs[:3]:
            status, question, tools, error = StateDetector.detect(msg)
            # TOOL_USE or USER_QUESTION if it's AskUserQuestion
            assert status in (SessionStatus.TOOL_USE, SessionStatus.USER_QUESTION)


class TestStateDetectorUserQuestion:
    """Test USER_QUESTION state detection."""

    def test_user_question_single_select(self, sample_messages):
        """AskUserQuestion with single select should be USER_QUESTION."""
        message = sample_messages["USER_QUESTION_SINGLE"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.USER_QUESTION
        assert question is not None
        assert "output format" in question.question.lower()
        assert question.header == "Format"
        assert len(question.options) == 2
        assert question.options[0].label == "JSON"
        assert question.multi_select is False

    def test_user_question_multi_select(self, sample_messages):
        """AskUserQuestion with multi-select."""
        message = sample_messages["USER_QUESTION_MULTI"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.USER_QUESTION
        assert question is not None
        assert question.multi_select is True

    def test_user_question_not_triggered_for_other_tools(self, sample_messages):
        """Other tools should not trigger USER_QUESTION."""
        message = sample_messages["TOOL_USE_READ"]
        status, question, tools, error = StateDetector.detect(message)
        assert status != SessionStatus.USER_QUESTION
        assert question is None

    def test_user_question_with_many_options(self):
        """AskUserQuestion with many options."""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [
                            {
                                "question": "Choose one",
                                "header": "Choice",
                                "options": [
                                    {"label": f"Option {i}", "description": f"Description {i}"} for i in range(10)
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
        assert len(question.options) == 10

    def test_user_question_empty_options(self):
        """AskUserQuestion with empty options list."""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [
                            {
                                "question": "Enter your name",
                                "header": "Name",
                                "options": [],
                                "multiSelect": False,
                            }
                        ]
                    },
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.USER_QUESTION
        assert question.options == []


class TestStateDetectorErrorStop:
    """Test ERROR_STOP state detection."""

    def test_error_stop_refusal(self, sample_messages):
        """Refusal stop_reason should be ERROR_STOP."""
        message = sample_messages["ERROR_REFUSAL"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.ERROR_STOP
        assert error is not None
        assert error.error_type == "refusal"
        assert "cannot help" in error.message.lower()

    def test_error_stop_tool_result_error(self, sample_messages):
        """Tool result with is_error=True should be ERROR_STOP."""
        message = sample_messages["ERROR_TOOL_RESULT"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.ERROR_STOP
        assert error is not None
        assert error.error_type == "tool_execution_error"
        assert "File not found" in error.message

    def test_error_stop_execution_error(self, sample_messages):
        """Execution error stop_reason should be ERROR_STOP."""
        message = sample_messages["ERROR_EXECUTION"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.ERROR_STOP
        assert error is not None
        assert error.error_type == "execution_error"

    def test_not_error_stop_for_end_turn(self, sample_messages):
        """end_turn should not be ERROR_STOP."""
        message = sample_messages["TASK_COMPLETE_END_TURN"]
        status, question, tools, error = StateDetector.detect(message)
        assert status != SessionStatus.ERROR_STOP

    def test_error_stop_with_tool_info(self):
        """Error with tool information preserved."""
        message = {
            "stop_reason": "error",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "tool_read_123",
                    "content": "Permission denied",
                    "is_error": True,
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.ERROR_STOP
        assert error.tool_name == "tool_read_123"


class TestStateDetectorTaskComplete:
    """Test TASK_COMPLETE state detection."""

    def test_task_complete_end_turn(self, sample_messages):
        """end_turn should be TASK_COMPLETE."""
        message = sample_messages["TASK_COMPLETE_END_TURN"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE
        assert question is None
        assert error is None

    def test_task_complete_stop_sequence(self, sample_messages):
        """stop_sequence should be TASK_COMPLETE."""
        message = sample_messages["TASK_COMPLETE_STOP_SEQUENCE"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_task_complete_max_tokens(self, sample_messages):
        """max_tokens should be TASK_COMPLETE."""
        message = sample_messages["TASK_COMPLETE_MAX_TOKENS"]
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_task_complete_with_thinking(self):
        """TASK_COMPLETE with thinking content."""
        message = {
            "stop_reason": "end_turn",
            "content": [
                {"type": "thinking", "thinking": "All done!"},
                {"type": "text", "text": "Task finished."},
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_task_complete_with_real_messages(self, real_messages):
        """Test TASK_COMPLETE detection with real extracted messages."""
        complete_msgs = real_messages.get("TASK_COMPLETE", [])
        for msg in complete_msgs[:3]:
            status, question, tools, error = StateDetector.detect(msg)
            assert status == SessionStatus.TASK_COMPLETE, f"Expected TASK_COMPLETE, got {status}"


class TestStateDetectorEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_content(self):
        """Empty content should be handled gracefully."""
        message = {"stop_reason": "end_turn", "content": []}
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_missing_content_field(self):
        """Missing content field should be handled."""
        message = {"stop_reason": "end_turn"}
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_unknown_stop_reason(self):
        """Unknown stop_reason without error should be TASK_COMPLETE."""
        message = {
            "stop_reason": "unknown_reason",
            "content": [{"type": "text", "text": "Something"}],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_mixed_content_types(self):
        """Mixed content types should be processed correctly."""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {"type": "text", "text": "Let me read that."},
                {"type": "thinking", "thinking": "Need to check file..."},
                {"type": "tool_use", "name": "Read", "id": "t1", "input": {"file_path": "/tmp/x"}},
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TOOL_USE
        assert len(tools) == 1

    def test_content_with_special_characters(self):
        """Content with special characters should be handled."""
        message = {
            "stop_reason": "end_turn",
            "content": [{"type": "text", "text": "特殊字符: 中文、日本語、한국어、emoji 🎉"}],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE

    def test_very_long_content(self):
        """Very long content should be handled without errors."""
        message = {
            "stop_reason": "end_turn",
            "content": [{"type": "text", "text": "x" * 100000}],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.TASK_COMPLETE


class TestStateDetectorPriority:
    """Test detection priority and ordering."""

    def test_user_question_takes_priority_over_tool_use(self):
        """AskUserQuestion should be USER_QUESTION, not TOOL_USE."""
        message = {
            "stop_reason": "tool_use",
            "content": [
                {
                    "type": "tool_use",
                    "name": "AskUserQuestion",
                    "input": {
                        "questions": [{"question": "Choose", "header": "Choice", "options": [], "multiSelect": False}]
                    },
                }
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.USER_QUESTION
        assert question is not None

    def test_error_takes_priority_for_error_stop_reason(self):
        """Error stop_reason should trigger ERROR_STOP even with other content."""
        message = {
            "stop_reason": "error",
            "content": [
                {"type": "text", "text": "Something went wrong"},
                {"type": "tool_use", "name": "Read", "id": "t1", "input": {}},
            ],
        }
        status, question, tools, error = StateDetector.detect(message)
        assert status == SessionStatus.ERROR_STOP


class TestExtractQuestion:
    """Test _extract_question method directly."""

    def test_extract_question_with_valid_input(self):
        """Extract question from valid input."""
        content = [
            {
                "type": "tool_use",
                "name": "AskUserQuestion",
                "input": {
                    "questions": [
                        {
                            "question": "Choose color",
                            "header": "Color",
                            "options": [
                                {"label": "Red", "description": "Red color"},
                                {"label": "Blue", "description": "Blue color"},
                            ],
                            "multiSelect": False,
                        }
                    ]
                },
            }
        ]
        question = StateDetector._extract_question(content)
        assert question is not None
        assert question.question == "Choose color"
        assert question.header == "Color"
        assert len(question.options) == 2

    def test_extract_question_no_ask_user_question(self):
        """Return None when no AskUserQuestion."""
        content = [{"type": "tool_use", "name": "Read", "input": {"file_path": "/tmp/x"}}]
        question = StateDetector._extract_question(content)
        assert question is None

    def test_extract_question_empty_content(self):
        """Return None for empty content."""
        question = StateDetector._extract_question([])
        assert question is None


class TestExtractError:
    """Test _extract_error method directly."""

    def test_extract_error_from_refusal(self):
        """Extract error from refusal."""
        message = {
            "stop_reason": "refusal",
            "content": [{"type": "text", "text": "I refuse this."}],
        }
        error = StateDetector._extract_error(message)
        assert error is not None
        assert error.error_type == "refusal"

    def test_extract_error_from_tool_result(self):
        """Extract error from tool_result."""
        message = {"content": [{"type": "tool_result", "tool_use_id": "t1", "content": "Failed", "is_error": True}]}
        error = StateDetector._extract_error(message)
        assert error is not None
        assert error.error_type == "tool_execution_error"

    def test_extract_error_no_error(self):
        """Return None when no error."""
        message = {"content": [{"type": "text", "text": "Success"}], "stop_reason": "end_turn"}
        error = StateDetector._extract_error(message)
        assert error is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
