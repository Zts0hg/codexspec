#!/usr/bin/env python3
"""
Full Pipeline Integration Tests

Tests the complete flow:
1. JSONL message → StateDetector → OutputFormatter → JSON output
2. JSONL message → StateDetector → JSON → TeeNotifier → notify_telegram.py

Uses static fixtures to avoid dependency on real environment.
"""

import json
import sys
from pathlib import Path

import pytest

# Add project path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from claude_monitor import (
    ClaudeSessionMonitor,
    OutputFormatter,
    SessionState,
    SessionStatus,
    StateDetector,
)

# ============================================================================
# Test Data Builders
# ============================================================================


def make_assistant_message(stop_reason, content):
    """Create a properly formatted assistant message."""
    return {
        "type": "assistant",
        "message": {
            "stop_reason": stop_reason,
            "content": content,
        },
    }


def make_text_content(text):
    """Create text content block."""
    return {"type": "text", "text": text}


def make_tool_use(name, tool_id, input_data, description=None):
    """Create tool_use content block."""
    tool = {"type": "tool_use", "name": name, "id": tool_id, "input": input_data}
    if description:
        tool["description"] = description
    return tool


def make_ask_user_question(question, header, options, multi_select=False):
    """Create AskUserQuestion tool use."""
    return make_tool_use(
        "AskUserQuestion",
        "tool_ask_1",
        {
            "questions": [
                {
                    "question": question,
                    "header": header,
                    "options": options,
                    "multiSelect": multi_select,
                }
            ]
        },
    )


def make_tool_result(tool_use_id, content, is_error=False):
    """Create tool_result content block."""
    return {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": content,
        "is_error": is_error,
    }


# ============================================================================
# Pipeline Stage 1: JSONL → StateDetector
# ============================================================================


class TestPipelineStateDetection:
    """Test StateDetector as first stage of pipeline."""

    def test_streaming_message_detection(self):
        """Streaming message should be detected correctly."""
        message = {"stop_reason": None, "content": [make_text_content("Working...")]}

        status, question, tools, error = StateDetector.detect(message)

        assert status == SessionStatus.STREAMING
        assert question is None
        assert tools == []
        assert error is None

    def test_tool_use_message_detection(self):
        """Tool use message should be detected and tools extracted."""
        message = {
            "stop_reason": "tool_use",
            "content": [
                make_text_content("Let me read that."),
                make_tool_use("Read", "tool_1", {"file_path": "/tmp/test.txt"}),
            ],
        }

        status, question, tools, error = StateDetector.detect(message)

        assert status == SessionStatus.TOOL_USE
        assert len(tools) == 1
        assert tools[0].tool_name == "Read"
        assert tools[0].tool_input["file_path"] == "/tmp/test.txt"

    def test_user_question_detection(self):
        """User question should be detected with full details."""
        message = {
            "stop_reason": "tool_use",
            "content": [
                make_ask_user_question(
                    "Which format?",
                    "Format",
                    [
                        {"label": "JSON", "description": "Machine-readable"},
                        {"label": "Text", "description": "Human-readable"},
                    ],
                    multi_select=False,
                )
            ],
        }

        status, question, tools, error = StateDetector.detect(message)

        assert status == SessionStatus.USER_QUESTION
        assert question is not None
        assert question.question == "Which format?"
        assert question.header == "Format"
        assert len(question.options) == 2
        assert question.options[0].label == "JSON"

    def test_error_stop_detection(self):
        """Error stop should be detected with error info."""
        message = {
            "stop_reason": "refusal",
            "content": [make_text_content("I cannot help with that.")],
        }

        status, question, tools, error = StateDetector.detect(message)

        assert status == SessionStatus.ERROR_STOP
        assert error is not None
        assert error.error_type == "refusal"

    def test_task_complete_detection(self):
        """Task complete should be detected."""
        for stop_reason in ["end_turn", "stop_sequence", "max_tokens"]:
            message = {
                "stop_reason": stop_reason,
                "content": [make_text_content("Done")],
            }

            status, question, tools, error = StateDetector.detect(message)

            assert status == SessionStatus.TASK_COMPLETE


# ============================================================================
# Pipeline Stage 2: StateDetector → OutputFormatter
# ============================================================================


class TestPipelineOutputFormatting:
    """Test OutputFormatter as second stage of pipeline."""

    def test_format_user_question_pipeline(self):
        """User question should be formatted correctly."""
        # Stage 1: Detect
        message = {
            "stop_reason": "tool_use",
            "content": [
                make_ask_user_question(
                    "Choose output format",
                    "Format",
                    [{"label": "JSON", "description": "Machine-readable"}],
                )
            ],
        }
        status, question, tools, error = StateDetector.detect(message)

        # Stage 2: Format
        questions = [question] if question else []
        output = OutputFormatter.format_user_question("test1234", questions)

        assert "test1234" in output
        assert "USER_QUESTION" in output
        assert "Choose output format" in output
        assert "JSON" in output

    def test_format_error_stop_pipeline(self):
        """Error stop should be formatted correctly."""
        # Stage 1: Detect
        message = {
            "stop_reason": "error",
            "content": [make_tool_result("tool_1", "Error: File not found", is_error=True)],
        }
        status, question, tools, error = StateDetector.detect(message)

        # Stage 2: Format
        output = OutputFormatter.format_error_stop("test1234", error)

        assert "test1234" in output
        assert "ERROR_STOP" in output
        assert "Error: File not found" in output

    def test_format_task_complete_pipeline(self):
        """Task complete should be formatted correctly."""
        # Stage 1: Detect
        message = {
            "stop_reason": "end_turn",
            "content": [make_text_content("Task completed successfully")],
        }
        status, question, tools, error = StateDetector.detect(message)

        # Create session state
        state = SessionState(
            session_id="test1234",
            status=SessionStatus.TASK_COMPLETE,
            last_stop_reason="end_turn",
            last_output="Task completed successfully",
        )

        # Stage 2: Format
        output = OutputFormatter.format_task_complete("test1234", state)

        assert "test1234" in output
        assert "TASK_COMPLETE" in output
        assert "end_turn" in output
        assert "Task completed successfully" in output


# ============================================================================
# Pipeline Stage 3: Full Monitor Integration
# ============================================================================


class TestPipelineMonitorIntegration:
    """Test ClaudeSessionMonitor with callback integration."""

    def test_monitor_processes_message_correctly(self, temp_session_dir):
        """Monitor should process messages and update state."""
        # Track callback invocations
        callbacks = {"complete": [], "user_question": [], "error": []}

        def on_complete(session_id, state):
            callbacks["complete"].append((session_id, state))

        def on_user_question(session_id, questions):
            callbacks["user_question"].append((session_id, questions))

        def on_error(session_id, error_info):
            callbacks["error"].append((session_id, error_info))

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_complete=on_complete,
            on_user_question=on_user_question,
            on_error_stop=on_error,
        )

        # Process task complete message
        message = make_assistant_message(
            "end_turn",
            [make_text_content("Done")],
        )
        monitor._process_message("session-1", message)

        # Verify state was updated
        state = monitor.get_session_state("session-1")
        assert state is not None
        assert state.status == SessionStatus.TASK_COMPLETE
        assert state.last_stop_reason == "end_turn"

        # Verify callback was invoked
        assert len(callbacks["complete"]) == 1
        assert callbacks["complete"][0][0] == "session-1"

    def test_monitor_user_question_callback(self, temp_session_dir):
        """Monitor should invoke user question callback."""
        questions_received = []

        def on_user_question(session_id, questions):
            questions_received.extend(questions)

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_user_question=on_user_question,
        )

        message = make_assistant_message(
            "tool_use",
            [
                make_ask_user_question(
                    "Choose format",
                    "Format",
                    [{"label": "JSON", "description": "JSON format"}],
                )
            ],
        )
        monitor._process_message("session-2", message)

        assert len(questions_received) == 1
        assert questions_received[0].question == "Choose format"

    def test_monitor_error_callback(self, temp_session_dir):
        """Monitor should invoke error callback."""
        errors_received = []

        def on_error(session_id, error_info):
            errors_received.append(error_info)

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_error_stop=on_error,
        )

        message = make_assistant_message(
            "refusal",
            [make_text_content("I cannot help.")],
        )
        monitor._process_message("session-3", message)

        assert len(errors_received) == 1
        assert errors_received[0].error_type == "refusal"


# ============================================================================
# Pipeline Stage 4: JSON Output Mode
# ============================================================================


class TestPipelineJsonOutput:
    """Test JSON output mode of monitor."""

    def test_json_task_complete_output(self, temp_session_dir):
        """JSON output for task complete should have correct format."""
        json_outputs = []

        def capture_json(data):
            json_outputs.append(data)

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_complete=lambda sid, state: capture_json(
                {
                    "session_id": sid,
                    "status": state.status.value,
                    "stop_reason": state.last_stop_reason,
                    "output": state.last_output,
                }
            ),
        )

        message = make_assistant_message(
            "end_turn",
            [make_text_content("Task done")],
        )
        monitor._process_message("session-4", message)

        assert len(json_outputs) == 1
        output = json_outputs[0]
        assert output["session_id"] == "session-4"
        assert output["status"] == "TASK_COMPLETE"
        assert output["stop_reason"] == "end_turn"
        assert output["output"] == "Task done"

        # Verify it's valid JSON
        json_str = json.dumps(output)
        parsed = json.loads(json_str)
        assert parsed["session_id"] == "session-4"

    def test_json_user_question_output(self, temp_session_dir):
        """JSON output for user question should have correct format."""
        json_outputs = []

        def capture_json(data):
            json_outputs.append(data)

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_user_question=lambda sid, questions: capture_json(
                {
                    "session_id": sid,
                    "status": "USER_QUESTION",
                    "questions": [
                        {
                            "question": q.question,
                            "header": q.header,
                            "options": [{"label": o.label, "description": o.description} for o in q.options],
                            "multi_select": q.multi_select,
                        }
                        for q in questions
                    ],
                }
            ),
        )

        message = make_assistant_message(
            "tool_use",
            [
                make_ask_user_question(
                    "Select features",
                    "Features",
                    [{"label": "A", "description": "Feature A"}],
                    multi_select=True,
                )
            ],
        )
        monitor._process_message("session-5", message)

        assert len(json_outputs) == 1
        output = json_outputs[0]
        assert output["status"] == "USER_QUESTION"
        assert len(output["questions"]) == 1
        assert output["questions"][0]["multi_select"] is True


# ============================================================================
# Pipeline Stage 5: Full End-to-End
# ============================================================================


class TestPipelineEndToEnd:
    """End-to-end pipeline tests."""

    def test_complete_task_flow(self, temp_session_dir):
        """Test complete flow from message to formatted output."""
        outputs = []

        def capture_output(output_type, data):
            outputs.append((output_type, data))

        # Create monitor with all callbacks
        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_complete=lambda sid, state: capture_output(
                "complete",
                OutputFormatter.format_task_complete(sid, state),
            ),
            on_user_question=lambda sid, questions: capture_output(
                "question",
                OutputFormatter.format_user_question(sid, questions),
            ),
            on_error_stop=lambda sid, error: capture_output(
                "error",
                OutputFormatter.format_error_stop(sid, error),
            ),
        )

        # Process a sequence of messages
        # Note: tool_use with stop_reason doesn't trigger on_complete in current impl
        # Only end_turn, stop_sequence, max_tokens trigger on_complete
        messages = [
            # 1. Streaming (no output)
            make_assistant_message(None, [make_text_content("Thinking...")]),
            # 2. Task complete
            make_assistant_message("end_turn", [make_text_content("All done!")]),
        ]

        for msg in messages:
            monitor._process_message("session-e2e", msg)

        # Should have one complete output
        assert len(outputs) == 1
        assert outputs[0][0] == "complete"
        assert "TASK_COMPLETE" in outputs[0][1]
        assert "All done!" in outputs[0][1]

    def test_task_flow_with_tools(self, temp_session_dir):
        """Test flow with tool usage before completion."""
        outputs = []

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_complete=lambda sid, state: outputs.append(("complete", state.last_stop_reason)),
        )

        # Tool use doesn't trigger on_complete in current implementation
        message = make_assistant_message(
            "tool_use",
            [make_tool_use("Read", "t1", {"file_path": "/tmp/x"})],
        )
        monitor._process_message("session-tool", message)

        # No complete callback for tool_use
        assert len(outputs) == 0

    def test_error_flow(self, temp_session_dir):
        """Test error flow from message to formatted output."""
        outputs = []

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_error_stop=lambda sid, error: outputs.append(OutputFormatter.format_error_stop(sid, error)),
        )

        message = make_assistant_message(
            "error",
            [make_tool_result("t1", "Permission denied", is_error=True)],
        )
        monitor._process_message("session-err", message)

        assert len(outputs) == 1
        assert "ERROR_STOP" in outputs[0]
        assert "Permission denied" in outputs[0]


# ============================================================================
# Real Message Tests (using extracted fixtures)
# ============================================================================


class TestPipelineWithRealMessages:
    """Test pipeline with real extracted messages."""

    def test_real_streaming_messages(self, real_messages):
        """Test detection of real streaming messages."""
        streaming_msgs = real_messages.get("STREAMING", [])
        for msg in streaming_msgs[:3]:
            status, question, tools, error = StateDetector.detect(msg)
            assert status == SessionStatus.STREAMING

    def test_real_tool_use_messages(self, real_messages):
        """Test detection of real tool use messages."""
        tool_use_msgs = real_messages.get("TOOL_USE", [])
        for msg in tool_use_msgs[:3]:
            status, question, tools, error = StateDetector.detect(msg)
            # Could be TOOL_USE or USER_QUESTION depending on tool type
            assert status in (SessionStatus.TOOL_USE, SessionStatus.USER_QUESTION)

    def test_real_task_complete_messages(self, real_messages):
        """Test detection of real task complete messages."""
        complete_msgs = real_messages.get("TASK_COMPLETE", [])
        for msg in complete_msgs[:3]:
            status, question, tools, error = StateDetector.detect(msg)
            assert status == SessionStatus.TASK_COMPLETE


# ============================================================================
# Unicode and Special Character Tests
# ============================================================================


class TestPipelineUnicodeHandling:
    """Test pipeline with Unicode and special characters."""

    def test_chinese_characters(self, temp_session_dir):
        """Test handling of Chinese characters."""
        outputs = []

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_complete=lambda sid, state: outputs.append(state.last_output),
        )

        message = make_assistant_message("end_turn", [make_text_content("任务完成！这是一个测试。")])
        monitor._process_message("session-cn", message)

        assert len(outputs) == 1
        assert "任务完成" in outputs[0]

    def test_japanese_characters(self, temp_session_dir):
        """Test handling of Japanese characters."""
        outputs = []

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_complete=lambda sid, state: outputs.append(state.last_output),
        )

        message = make_assistant_message("end_turn", [make_text_content("タスク完了！テストです。")])
        monitor._process_message("session-jp", message)

        assert len(outputs) == 1
        assert "タスク完了" in outputs[0]

    def test_emoji_in_content(self, temp_session_dir):
        """Test handling of emoji in content."""
        outputs = []

        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
            on_complete=lambda sid, state: outputs.append(state.last_output),
        )

        message = make_assistant_message("end_turn", [make_text_content("Done! 🎉 🚀 ✅")])
        monitor._process_message("session-emoji", message)

        assert len(outputs) == 1
        assert "🎉" in outputs[0]

    def test_special_characters_in_file_path(self, temp_session_dir):
        """Test handling of special characters in tool input."""
        monitor = ClaudeSessionMonitor(
            project_dir=temp_session_dir,
            quiet=True,
        )

        message = make_assistant_message(
            "tool_use",
            [make_tool_use("Read", "t1", {"file_path": "/tmp/测试 文件.txt"})],
        )
        monitor._process_message("session-special", message)

        state = monitor.get_session_state("session-special")
        assert state is not None
        assert len(state.pending_tools) == 1
        assert "测试 文件" in state.pending_tools[0].tool_input["file_path"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
