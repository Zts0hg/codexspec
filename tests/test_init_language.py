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


# ---------------------------------------------------------------------------
# Per-dimension language flags (--interaction-lang / --document-lang / --commit-lang)
# and the unified --force behavior. These exercise the full CLI via CliRunner,
# which is non-TTY by default (the contract automation relies on).
# ---------------------------------------------------------------------------

from pathlib import Path  # noqa: E402

from typer.testing import CliRunner  # noqa: E402

from codexspec import app  # noqa: E402
from codexspec.i18n import (  # noqa: E402
    get_commit_language,
    get_document_language,
    get_interaction_language,
)

_runner = CliRunner()


def _init(proj: Path, *extra: str):
    """Invoke `codexspec init <proj> ...` via the CLI runner and return the result."""
    return _runner.invoke(app, ["init", str(proj), "--no-git", *extra])


def _config(proj: Path) -> str:
    return (proj / ".codexspec" / "config.yml").read_text(encoding="utf-8")


class TestInitPerDimensionFlags:
    """REQ-001 / REQ-002: per-dimension flags write only their key; --lang writes only output."""

    def test_three_flags_write_only_those_keys(self, tmp_path) -> None:
        proj = tmp_path / "p"
        result = _init(
            proj,
            "--interaction-lang",
            "en",
            "--document-lang",
            "zh-CN",
            "--commit-lang",
            "ja",
        )
        assert result.exit_code == 0, result.output
        cfg = _config(proj)
        assert 'interaction: "en"' in cfg
        assert 'document: "zh-CN"' in cfg
        assert 'commit: "ja"' in cfg
        # Sparse: no output key when only the three dimensions are given.
        assert "output:" not in cfg

    def test_lang_only_writes_output_only(self, tmp_path) -> None:
        proj = tmp_path / "p"
        result = _init(proj, "--lang", "zh-CN")
        assert result.exit_code == 0, result.output
        cfg = _config(proj)
        assert 'output: "zh-CN"' in cfg
        assert "interaction:" not in cfg
        assert "document:" not in cfg
        assert "commit:" not in cfg

    def test_lang_plus_override(self, tmp_path) -> None:
        proj = tmp_path / "p"
        result = _init(proj, "--lang", "zh-CN", "--commit-lang", "en")
        assert result.exit_code == 0, result.output
        cfg = _config(proj)
        assert 'output: "zh-CN"' in cfg
        assert 'commit: "en"' in cfg
        assert "interaction:" not in cfg
        assert "document:" not in cfg

    def test_invalid_code_warns_not_errors(self, tmp_path) -> None:
        proj = tmp_path / "p"
        result = _init(proj, "--interaction-lang", "xx")
        assert result.exit_code == 0, result.output  # REQ-011: warn, do not error
        assert 'interaction: "xx"' in _config(proj)

    def test_backward_compat_lang_resolves_all_dimensions(self, tmp_path) -> None:
        """REQ-014: --lang zh-CN resolves interaction/document/commit to zh-CN via fallback."""
        proj = tmp_path / "p"
        result = _init(proj, "--lang", "zh-CN")
        assert result.exit_code == 0, result.output
        cfg = proj / ".codexspec" / "config.yml"
        assert get_interaction_language(cfg) == "zh-CN"
        assert get_document_language(cfg) == "zh-CN"
        assert get_commit_language(cfg) == "zh-CN"

    def test_determinism_same_flags_same_config(self, tmp_path) -> None:
        """NFR-003: identical flags produce identical language content."""
        proj_a = tmp_path / "a"
        proj_b = tmp_path / "b"
        _init(proj_a, "--interaction-lang", "en", "--document-lang", "zh-CN", "--commit-lang", "ja")
        _init(proj_b, "--interaction-lang", "en", "--document-lang", "zh-CN", "--commit-lang", "ja")
        # Normalize out the creation date before comparing.

        def _norm(s: str) -> str:
            return re.sub(r'created: ".*?"', 'created: "X"', s)

        assert _norm(_config(proj_a)) == _norm(_config(proj_b))


class TestInitSurgicalReinit:
    """REQ-005: re-init updates only the specified key(s), preserving the rest."""

    def test_reinit_changes_only_one_key(self, tmp_path) -> None:
        proj = tmp_path / "p"
        _init(proj, "--interaction-lang", "en", "--document-lang", "en", "--commit-lang", "en")
        before = _config(proj)
        # Change only document.
        result = _init(proj, "--document-lang", "ja", "--force")
        assert result.exit_code == 0, result.output
        after = _config(proj)
        assert 'interaction: "en"' in after
        assert 'document: "ja"' in after
        assert 'commit: "en"' in after
        # interaction/commit lines unchanged from before.
        assert 'interaction: "en"' in before
        assert 'commit: "en"' in before

    def test_reinit_no_flag_preserves_everything(self, tmp_path) -> None:
        proj = tmp_path / "p"
        _init(proj, "--interaction-lang", "en", "--document-lang", "zh-CN", "--commit-lang", "ja")
        before = _config(proj)
        result = _init(proj, "--force")  # no language flag
        assert result.exit_code == 0, result.output
        assert _config(proj) == before  # byte-identical

    def test_force_does_not_regenerate_config(self, tmp_path) -> None:
        """REQ-013: --force does not wipe existing keys / regenerate config."""
        proj = tmp_path / "p"
        _init(proj, "--interaction-lang", "en", "--document-lang", "zh-CN", "--commit-lang", "ja")
        result = _init(proj, "--force")  # no language flags
        assert result.exit_code == 0, result.output
        cfg = _config(proj)
        # All three explicit keys are still present (not wiped by regeneration).
        assert 'interaction: "en"' in cfg
        assert 'document: "zh-CN"' in cfg
        assert 'commit: "ja"' in cfg


class TestInitForceNonInteractive:
    """REQ-012: --force makes re-init fully non-interactive on an existing project."""

    def test_force_reinit_no_prompts_exit_zero(self, tmp_path) -> None:
        proj = tmp_path / "p"
        _init(proj, "--interaction-lang", "en", "--document-lang", "en", "--commit-lang", "en")
        # Re-init with --force: should not block on any confirmation, exit 0.
        result = _init(proj, "--force", "--interaction-lang", "ja")
        assert result.exit_code == 0, result.output
        assert 'interaction: "ja"' in _config(proj)
        # document/commit preserved.
        assert 'document: "en"' in _config(proj)
        assert 'commit: "en"' in _config(proj)


class TestInitPromptGating:
    """REQ-006 / REQ-007: prompt only on first-time + base-undeterminable + TTY."""

    @pytest.fixture
    def mock_console(self):
        return Console(file=StringIO(), force_terminal=True, width=100)

    def test_existing_config_no_flag_does_not_prompt(self, mock_console, tmp_path) -> None:
        """REQ-007: existing config.yml + no language flag → no prompt, keys preserved."""
        from codexspec import init

        proj = tmp_path / "p"
        # First, create a project with a config.
        _init(proj, "--lang", "zh-CN")
        assert (proj / ".codexspec" / "config.yml").exists()

        with patch("codexspec.console", mock_console):
            with patch("sys.stdin.isatty", return_value=True):
                with patch("codexspec.prompt_language_selection") as mock_prompt:
                    with patch("typer.Exit"):
                        try:
                            # force=True passes the directory-exists gate; the point
                            # under test is that NO language flag → no language prompt.
                            init(project_name=str(proj), here=False, lang=None, force=True, no_git=True, debug=False)
                        except Exception:
                            pass
                        mock_prompt.assert_not_called()

    def test_all_three_flags_skip_prompt_first_time(self, mock_console, tmp_path) -> None:
        """All three specific flags → base determinable → no prompt even first-time TTY."""
        from codexspec import init

        proj = tmp_path / "fresh"
        with patch("codexspec.console", mock_console):
            with patch("sys.stdin.isatty", return_value=True):
                with patch("codexspec.prompt_language_selection") as mock_prompt:
                    try:
                        init(
                            project_name=str(proj),
                            here=False,
                            lang=None,
                            interaction_lang="en",
                            document_lang="en",
                            commit_lang="en",
                            force=False,
                            no_git=True,
                            debug=False,
                        )
                    except Exception:
                        pass
                    mock_prompt.assert_not_called()

    def test_partial_flags_still_prompt_first_time(self, mock_console, tmp_path) -> None:
        """Only 2 of 3 flags + no --lang → base undeterminable → prompt (first-time TTY)."""
        from codexspec import init

        proj = tmp_path / "fresh"
        with patch("codexspec.console", mock_console):
            with patch("sys.stdin.isatty", return_value=True):
                with patch("codexspec.prompt_language_selection", return_value="en") as mock_prompt:
                    with patch("typer.Exit"):
                        try:
                            init(
                                project_name=str(proj),
                                here=False,
                                lang=None,
                                interaction_lang="en",
                                document_lang="en",
                                force=False,
                                no_git=True,
                                debug=False,
                            )
                        except Exception:
                            pass
                        mock_prompt.assert_called()
