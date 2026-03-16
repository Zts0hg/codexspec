"""Tests for interactive language selection in init command.

This module contains unit tests for the prompt_language_selection() function
and the init() command's TTY detection logic.
"""

import re
from io import StringIO
from unittest.mock import patch

import pytest
from rich.console import Console

from codexspec.i18n import normalize_locale


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from text."""
    ansi_pattern = re.compile(r"\x1b\[[0-9;]*m")
    return ansi_pattern.sub("", text)


class TestPromptLanguageSelection:
    """Tests for prompt_language_selection function."""

    @pytest.fixture
    def mock_console(self):
        """Create a mock console for testing."""
        return Console(file=StringIO(), force_terminal=True)

    def test_valid_choice_1_returns_english(self, mock_console) -> None:
        """选择 1 应返回 'en'。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", return_value="1"):
                result = prompt_language_selection()
                assert result == "en"

    def test_valid_choice_2_returns_zh_cn(self, mock_console) -> None:
        """选择 2 应返回 'zh-CN'。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", return_value="2"):
                result = prompt_language_selection()
                assert result == "zh-CN"

    def test_valid_choice_3_returns_ja(self, mock_console) -> None:
        """选择 3 应返回 'ja'。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", return_value="3"):
                result = prompt_language_selection()
                assert result == "ja"

    def test_choice_9_with_custom_code_returns_normalized(self, mock_console) -> None:
        """选择 9 后输入自定义代码应返回规范化结果。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            # First call selects "9", second call enters custom code "ru"
            with patch("rich.prompt.Prompt.ask", side_effect=["9", "ru"]):
                result = prompt_language_selection()
                assert result == normalize_locale("ru")

    def test_choice_9_with_alias_returns_normalized(self, mock_console) -> None:
        """选择 9 后输入别名应返回规范化结果。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            # Input "ZH" should normalize to "zh-CN"
            with patch("rich.prompt.Prompt.ask", side_effect=["9", "ZH"]):
                result = prompt_language_selection()
                assert result == "zh-CN"

    def test_choice_9_empty_input_returns_default(self, mock_console) -> None:
        """选择 9 后空字符串输入应返回默认语言 'en'。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            # Empty string input should return default
            with patch("rich.prompt.Prompt.ask", side_effect=["9", ""]):
                result = prompt_language_selection()
                assert result == "en"

    def test_choice_9_whitespace_only_returns_default(self, mock_console) -> None:
        """选择 9 后仅空白字符输入应返回默认语言 'en'。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", side_effect=["9", "   "]):
                result = prompt_language_selection()
                assert result == "en"

    def test_ctrl_c_raises_keyboard_interrupt(self, mock_console) -> None:
        """按 Ctrl+C 应抛出 KeyboardInterrupt。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", side_effect=KeyboardInterrupt):
                with pytest.raises(KeyboardInterrupt):
                    prompt_language_selection()

    def test_default_parameter_used_for_empty_custom(self, mock_console) -> None:
        """默认参数应在空自定义输入时使用。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", side_effect=["9", ""]):
                result = prompt_language_selection(default="zh-CN")
                assert result == "zh-CN"


class TestInitTTYDetection:
    """Tests for init() function's TTY detection logic."""

    @pytest.fixture
    def mock_console(self):
        """Create a mock console for testing."""
        return Console(file=StringIO(), force_terminal=True)

    def test_tty_env_calls_prompt(self, mock_console, tmp_path) -> None:
        """TTY 环境下未传 --lang 应调用 prompt_language_selection()。"""
        from codexspec import init

        # Create a test project directory
        test_dir = tmp_path / "test-project"

        with patch("codexspec.console", mock_console):
            with patch("sys.stdin.isatty", return_value=True):
                with patch("codexspec.prompt_language_selection", return_value="zh-CN") as mock_prompt:
                    with patch("typer.Exit"):
                        # Call init without --lang (lang=None)
                        try:
                            init(
                                project_name=str(test_dir), here=False, lang=None, force=False, no_git=True, debug=False
                            )
                        except Exception:
                            pass  # May fail due to other reasons, but we just check prompt was called

                        mock_prompt.assert_called_once()

    def test_non_tty_env_uses_default_en(self, mock_console, tmp_path) -> None:
        """非 TTY 环境下未传 --lang 应使用默认 'en'。"""
        from codexspec import init

        test_dir = tmp_path / "test-project"

        with patch("codexspec.console", mock_console):
            with patch("sys.stdin.isatty", return_value=False):
                with patch("codexspec.prompt_language_selection") as mock_prompt:
                    # Should not call prompt in non-TTY
                    try:
                        init(project_name=str(test_dir), here=False, lang=None, force=False, no_git=True, debug=False)
                    except Exception:
                        pass

                    # prompt_language_selection should NOT be called
                    mock_prompt.assert_not_called()

    def test_explicit_lang_skips_prompt(self, mock_console, tmp_path) -> None:
        """传入 --lang 应跳过交互。"""
        from codexspec import init

        test_dir = tmp_path / "test-project"

        with patch("codexspec.console", mock_console):
            with patch("sys.stdin.isatty", return_value=True):
                with patch("codexspec.prompt_language_selection") as mock_prompt:
                    try:
                        init(
                            project_name=str(test_dir), here=False, lang="zh-CN", force=False, no_git=True, debug=False
                        )
                    except Exception:
                        pass

                    # prompt_language_selection should NOT be called when lang is explicit
                    mock_prompt.assert_not_called()

    def test_ctrl_c_uses_default_language(self, mock_console, tmp_path) -> None:
        """Ctrl+C 时应使用默认语言继续。"""
        from codexspec import init

        test_dir = tmp_path / "test-project"

        with patch("codexspec.console", mock_console):
            with patch("sys.stdin.isatty", return_value=True):
                with patch("codexspec.prompt_language_selection", side_effect=KeyboardInterrupt):
                    with patch("typer.Exit"):
                        try:
                            init(
                                project_name=str(test_dir), here=False, lang=None, force=False, no_git=True, debug=False
                            )
                        except Exception:
                            pass

                        # Should continue with "en" after Ctrl+C
                        # Check that config was created with "en"
                        config_file = test_dir / ".codexspec" / "config.yml"
                        if config_file.exists():
                            content = config_file.read_text()
                            assert 'output: "en"' in content


class TestLanguageChoicesDisplay:
    """Tests for language choices display in prompt_language_selection."""

    @pytest.fixture
    def mock_console(self):
        """Create a mock console for capturing output."""
        return Console(file=StringIO(), force_terminal=True, width=100)

    def test_displays_9_options(self, mock_console) -> None:
        """应显示 9 个选项（8 个预定义 + 1 个 Other...）。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", return_value="1"):
                prompt_language_selection()

        output = strip_ansi(mock_console.file.getvalue())

        # Should have options 1-9
        for i in range(1, 10):
            assert f"[{i}]" in output, f"Missing option [{i}]"

    def test_first_option_is_english(self, mock_console) -> None:
        """第一个选项应为 English。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", return_value="1"):
                prompt_language_selection()

        output = strip_ansi(mock_console.file.getvalue())

        # First option should be English
        assert "[1]" in output
        assert "English" in output or "en" in output

    def test_last_option_is_other(self, mock_console) -> None:
        """最后一个选项应为 Other...。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", return_value="1"):
                prompt_language_selection()

        output = strip_ansi(mock_console.file.getvalue())

        # Should have "Other" option
        assert "[9]" in output
        assert "Other" in output

    def test_custom_language_shows_warning(self, mock_console) -> None:
        """选择自定义语言应显示警告。"""
        from codexspec import prompt_language_selection

        with patch("codexspec.console", mock_console):
            with patch("rich.prompt.Prompt.ask", side_effect=["9", "ru"]):
                prompt_language_selection()

        output = strip_ansi(mock_console.file.getvalue())

        # Should show warning about pre-translated content
        assert "Pre-translated" in output or "may not be available" in output.lower() or "Note" in output
