#!/usr/bin/env python3
"""
Shared pytest fixtures for claude_monitor.py and notify_telegram.py tests.

These fixtures use static test data from fixtures/real_messages.py to avoid
depending on the real environment during testing.
"""

import json
import sys
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

# Import modules under test
from claude_monitor import (
    ErrorInfo,
    QuestionInfo,
    QuestionOption,
    SessionState,
    SessionStatus,
    ToolUseInfo,
)

# ============================================================================
# Sample Message Fixtures (static, from extracted real messages)
# ============================================================================

# Minimal sample messages for testing (not dependent on real environment)
SAMPLE_MESSAGES = {
    "STREAMING": {
        "stop_reason": None,
        "content": [{"type": "text", "text": "Thinking about this..."}],
    },
    "TOOL_USE_READ": {
        "stop_reason": "tool_use",
        "content": [
            {"type": "text", "text": "Let me read that file."},
            {"type": "tool_use", "name": "Read", "id": "tool_123", "input": {"file_path": "/tmp/test.txt"}},
        ],
    },
    "TOOL_USE_BASH": {
        "stop_reason": "tool_use",
        "content": [{"type": "tool_use", "name": "Bash", "id": "tool_456", "input": {"command": "ls -la"}}],
    },
    "TOOL_USE_WRITE": {
        "stop_reason": "tool_use",
        "content": [
            {
                "type": "tool_use",
                "name": "Write",
                "id": "tool_789",
                "input": {"file_path": "/tmp/out.txt", "content": "Hello"},
            }
        ],
    },
    "USER_QUESTION_SINGLE": {
        "stop_reason": "tool_use",
        "content": [
            {
                "type": "tool_use",
                "name": "AskUserQuestion",
                "id": "tool_ask_1",
                "input": {
                    "questions": [
                        {
                            "question": "Which output format do you prefer?",
                            "header": "Format",
                            "options": [
                                {"label": "JSON", "description": "Machine-readable"},
                                {"label": "Text", "description": "Human-readable"},
                            ],
                            "multiSelect": False,
                        }
                    ]
                },
            }
        ],
    },
    "USER_QUESTION_MULTI": {
        "stop_reason": "tool_use",
        "content": [
            {
                "type": "tool_use",
                "name": "AskUserQuestion",
                "id": "tool_ask_2",
                "input": {
                    "questions": [
                        {
                            "question": "Select features to enable",
                            "header": "Features",
                            "options": [
                                {"label": "A", "description": "Feature A"},
                                {"label": "B", "description": "Feature B"},
                            ],
                            "multiSelect": True,
                        }
                    ]
                },
            }
        ],
    },
    "ERROR_REFUSAL": {
        "stop_reason": "refusal",
        "content": [{"type": "text", "text": "I cannot help with that request."}],
    },
    "ERROR_TOOL_RESULT": {
        "stop_reason": "error",
        "content": [
            {"type": "tool_result", "tool_use_id": "tool_xxx", "content": "Error: File not found", "is_error": True}
        ],
    },
    "ERROR_EXECUTION": {
        "stop_reason": "error",
        "content": [{"type": "text", "text": "Execution failed due to timeout"}],
    },
    "TASK_COMPLETE_END_TURN": {
        "stop_reason": "end_turn",
        "content": [{"type": "text", "text": "Task completed successfully."}],
    },
    "TASK_COMPLETE_STOP_SEQUENCE": {
        "stop_reason": "stop_sequence",
        "content": [{"type": "text", "text": "Stopped at sequence."}],
    },
    "TASK_COMPLETE_MAX_TOKENS": {
        "stop_reason": "max_tokens",
        "content": [{"type": "text", "text": "Output truncated due to token limit..."}],
    },
}


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def sample_messages() -> dict[str, dict]:
    """Provide sample messages for testing."""
    return SAMPLE_MESSAGES


@pytest.fixture
def real_messages() -> dict[str, list[dict]]:
    """Load real extracted messages from fixtures file.

    Returns empty dict if file doesn't exist (for graceful degradation).
    """
    fixtures_path = Path(__file__).parent / "fixtures" / "real_messages.py"
    if not fixtures_path.exists():
        return {}

    # Import the REAL_MESSAGES from the fixtures file
    import importlib.util

    spec = importlib.util.spec_from_file_location("real_messages", fixtures_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "REAL_MESSAGES", {})


@pytest.fixture
def temp_session_dir():
    """Create a temporary directory for session files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_jsonl_file(temp_session_dir: Path):
    """Create a mock JSONL file with sample messages."""

    def _create_jsonl(session_id: str, messages: list[dict]) -> Path:
        """Create a JSONL file with the given messages.

        Args:
            session_id: Session ID for the filename
            messages: List of message dictionaries

        Returns:
            Path to the created JSONL file
        """
        jsonl_path = temp_session_dir / f"{session_id}.jsonl"
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for msg in messages:
                # Wrap in assistant envelope if needed
                data = {"type": "assistant", "message": msg}
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
        return jsonl_path

    return _create_jsonl


@pytest.fixture
def mock_telegram_api():
    """Mock urllib.request for Telegram API calls.

    Yields a mock object that can be configured to return specific responses.
    """
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"ok": true, "result": {"message_id": 123}}'
        mock_response.__enter__ = MagicMock(return_value=mock_response)
        mock_response.__exit__ = MagicMock(return_value=False)
        mock_urlopen.return_value = mock_response
        yield mock_urlopen


@pytest.fixture
def mock_telegram_api_failure():
    """Mock urllib.request for Telegram API failures."""
    import urllib.error

    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
        yield mock_urlopen


@pytest.fixture
def mock_stderr():
    """Capture stderr output."""
    with patch("sys.stderr", new_callable=StringIO) as mock:
        yield mock


@pytest.fixture
def mock_stdout():
    """Capture stdout output."""
    with patch("sys.stdout", new_callable=StringIO) as mock:
        yield mock


# ============================================================================
# Helper fixtures for creating test objects
# ============================================================================


@pytest.fixture
def sample_question_info() -> QuestionInfo:
    """Create a sample QuestionInfo object."""
    return QuestionInfo(
        question="Which format do you prefer?",
        header="Format",
        options=[
            QuestionOption(label="JSON", description="Machine-readable"),
            QuestionOption(label="Text", description="Human-readable"),
        ],
        multi_select=False,
    )


@pytest.fixture
def sample_error_info() -> ErrorInfo:
    """Create a sample ErrorInfo object."""
    return ErrorInfo(
        error_type="ToolExecutionError",
        message="Failed to execute tool: file not found",
        tool_name="Read",
        tool_input={"file_path": "/nonexistent/file.txt"},
    )


@pytest.fixture
def sample_tool_use_info() -> ToolUseInfo:
    """Create a sample ToolUseInfo object."""
    return ToolUseInfo(
        tool_name="Read",
        tool_id="tool_123",
        tool_input={"file_path": "/tmp/test.txt"},
        description="Reading test file",
    )


@pytest.fixture
def sample_session_state() -> SessionState:
    """Create a sample SessionState object."""
    return SessionState(
        session_id="abc12345def67890",
        status=SessionStatus.TASK_COMPLETE,
        last_stop_reason="end_turn",
        last_output="Task completed successfully",
        is_executing=False,
    )
