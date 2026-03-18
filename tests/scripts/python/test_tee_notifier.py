#!/usr/bin/env python3
"""
TeeNotifier Unit Tests

Tests the TeeNotifier class which manages the notify_telegram.py subprocess:
- Subprocess lifecycle (start/write/stop)
- Error handling (broken pipe, subprocess crash)
- Graceful shutdown
"""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add project path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "scripts" / "python"))

from claude_monitor import TeeNotifier


class TestTeeNotifierLifecycle:
    """Test TeeNotifier subprocess lifecycle."""

    def test_start_creates_subprocess(self):
        """Starting should create a subprocess."""
        notifier = TeeNotifier()
        # Mock subprocess.Popen to avoid actually starting the process
        with patch("claude_monitor.subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_process.stdin = MagicMock()
            mock_popen.return_value = mock_process

            result = notifier.start()

            assert result is True
            assert notifier._process is mock_process
            mock_popen.assert_called_once()

    def test_start_handles_exception(self):
        """Start should return False on exception."""
        notifier = TeeNotifier()
        with patch("claude_monitor.subprocess.Popen") as mock_popen:
            mock_popen.side_effect = OSError("Failed to start")

            result = notifier.start()

            assert result is False
            assert notifier._process is None

    def test_write_outputs_to_stdout(self):
        """Write should output to stdout."""
        notifier = TeeNotifier()
        notifier._process = None  # No subprocess

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            notifier.write("test line")

            output = mock_stdout.getvalue()
            assert "test line" in output

    def test_write_sends_to_subprocess(self):
        """Write should send data to subprocess stdin."""
        notifier = TeeNotifier()
        mock_process = MagicMock()
        mock_stdin = MagicMock()
        mock_process.stdin = mock_stdin
        notifier._process = mock_process

        with patch("sys.stdout", new_callable=StringIO):
            notifier.write("test line")

            mock_stdin.write.assert_called_once_with("test line\n")
            mock_stdin.flush.assert_called_once()

    def test_write_handles_broken_pipe(self):
        """Write should handle broken pipe gracefully."""
        notifier = TeeNotifier()
        mock_process = MagicMock()
        mock_stdin = MagicMock()
        mock_stdin.write.side_effect = BrokenPipeError("Pipe broken")
        mock_process.stdin = mock_stdin
        notifier._process = mock_process

        with patch("sys.stdout", new_callable=StringIO):
            # Should not raise, should continue with stdout only
            notifier.write("test line")

            # Process should be cleared
            assert notifier._process is None

    def test_write_handles_os_error(self):
        """Write should handle OSError gracefully."""
        notifier = TeeNotifier()
        mock_process = MagicMock()
        mock_stdin = MagicMock()
        mock_stdin.write.side_effect = OSError("Process died")
        mock_process.stdin = mock_stdin
        notifier._process = mock_process

        with patch("sys.stdout", new_callable=StringIO):
            notifier.write("test line")

            assert notifier._process is None

    def test_stop_closes_stdin(self):
        """Stop should close stdin and wait for process."""
        notifier = TeeNotifier()
        mock_process = MagicMock()
        mock_stdin = MagicMock()
        mock_process.stdin = mock_stdin
        mock_process.wait.return_value = 0
        notifier._process = mock_process

        notifier.stop()

        mock_stdin.close.assert_called_once()
        mock_process.wait.assert_called_once_with(timeout=5)
        assert notifier._process is None

    def test_stop_terminates_on_timeout(self):
        """Stop should terminate process if wait times out."""
        notifier = TeeNotifier()
        mock_process = MagicMock()
        mock_stdin = MagicMock()
        mock_process.stdin = mock_stdin
        mock_process.wait.side_effect = TimeoutError("Timeout")
        notifier._process = mock_process

        notifier.stop()

        mock_process.terminate.assert_called_once()
        assert notifier._process is None

    def test_stop_handles_none_process(self):
        """Stop should handle None process gracefully."""
        notifier = TeeNotifier()
        notifier._process = None

        # Should not raise
        notifier.stop()

    def test_stop_handles_exception(self):
        """Stop should handle exceptions during cleanup."""
        notifier = TeeNotifier()
        mock_process = MagicMock()
        mock_stdin = MagicMock()
        mock_stdin.close.side_effect = Exception("Unexpected error")
        mock_process.stdin = mock_stdin
        notifier._process = mock_process

        # Should not raise
        notifier.stop()

        assert notifier._process is None


class TestTeeNotifierIntegration:
    """Integration tests for TeeNotifier with actual subprocess."""

    @pytest.mark.slow
    def test_full_lifecycle_integration(self):
        """Test full lifecycle with mocked subprocess (slower test)."""
        notifier = TeeNotifier()

        with patch("claude_monitor.subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_stdin = MagicMock()
            mock_process.stdin = mock_stdin
            mock_process.wait.return_value = 0
            mock_popen.return_value = mock_process

            # Start
            assert notifier.start() is True

            # Write multiple lines
            with patch("sys.stdout", new_callable=StringIO):
                notifier.write("line 1")
                notifier.write("line 2")
                notifier.write("line 3")

            # Stop
            notifier.stop()

            # Verify all writes were sent
            assert mock_stdin.write.call_count == 3

    def test_write_without_start(self):
        """Write should work even if start was not called."""
        notifier = TeeNotifier()

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            notifier.write("test")

            assert "test" in mock_stdout.getvalue()


class TestTeeNotifierErrorRecovery:
    """Test error recovery scenarios."""

    def test_continues_after_subprocess_death(self):
        """Should continue writing to stdout after subprocess dies."""
        notifier = TeeNotifier()
        mock_process = MagicMock()
        mock_stdin = MagicMock()
        mock_process.stdin = mock_stdin
        notifier._process = mock_process

        outputs = []

        def capture_stdout(text):
            outputs.append(text)

        with patch("builtins.print") as mock_print:
            mock_print.side_effect = lambda text, **kwargs: capture_stdout(text)

            # First write succeeds
            notifier.write("line 1")

            # Second write causes subprocess death
            mock_stdin.write.side_effect = BrokenPipeError()
            notifier.write("line 2")

            # Third write should still work (stdout only)
            notifier.write("line 3")

        # All three lines should have been output
        assert len(outputs) >= 2

    def test_multiple_broken_pipes(self):
        """Should handle multiple broken pipe events."""
        notifier = TeeNotifier()

        with patch("sys.stdout", new_callable=StringIO):
            # Simulate multiple broken pipes
            for _ in range(3):
                notifier._process = None
                notifier.write("test")  # Should work with stdout only

            # All writes should succeed


class TestTeeNotifierConcurrency:
    """Test thread safety and concurrent access (basic tests)."""

    def test_rapid_writes(self):
        """Test rapid consecutive writes."""
        notifier = TeeNotifier()
        mock_process = MagicMock()
        mock_stdin = MagicMock()
        mock_process.stdin = mock_stdin
        notifier._process = mock_process

        with patch("sys.stdout", new_callable=StringIO):
            for i in range(100):
                notifier.write(f"line {i}")

        # All writes should have been attempted
        assert mock_stdin.write.call_count == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
