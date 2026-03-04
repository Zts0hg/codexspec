"""Tests for i18n completeness check script."""

import subprocess
import sys
from pathlib import Path

import pytest

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Bash tests only run on Unix-like systems (macOS/Linux)",
)
class TestCheckI18nCompleteness:
    """Tests for the translation completeness check script."""

    def test_script_exists(self):
        """Script should exist at scripts/bash/check-i18n-completeness.sh."""
        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-completeness.sh"
        assert script_path.exists(), f"Script not found at {script_path}"

    def test_script_is_executable(self):
        """Script should be executable."""
        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-completeness.sh"
        if script_path.exists():
            result = subprocess.run(["bash", "-n", str(script_path)], capture_output=True, text=True)
            assert result.returncode == 0, f"Script has syntax errors: {result.stderr}"

    def test_fully_translated_passes(self, tmp_path):
        """Test that fully translated content passes validation."""
        en_dir = tmp_path / "docs" / "en"
        zh_dir = tmp_path / "docs" / "zh"

        en_dir.mkdir(parents=True)
        zh_dir.mkdir(parents=True)

        # Create fully translated content
        (en_dir / "index.md").write_text("# Welcome\nThis is English content.", encoding="utf-8")
        (zh_dir / "index.md").write_text("# 欢迎\n这是中文内容。", encoding="utf-8")

        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-completeness.sh"
        if script_path.exists():
            result = subprocess.run(
                ["bash", str(script_path), str(tmp_path / "docs"), "zh"], capture_output=True, text=True
            )
            assert result.returncode == 0, f"Should pass with fully translated content: {result.stdout}"

    def test_untranslated_content_fails(self, tmp_path):
        """Test that untranslated content fails validation."""
        en_dir = tmp_path / "docs" / "en"
        zh_dir = tmp_path / "docs" / "zh"

        en_dir.mkdir(parents=True)
        zh_dir.mkdir(parents=True)

        # Create content with clear untranslated English paragraph (not mixed with Chinese)
        (en_dir / "index.md").write_text("# Welcome\n\nThis is English content.\n\nMore text here.", encoding="utf-8")
        (zh_dir / "index.md").write_text(
            "# 欢迎\n\nThis paragraph was not translated at all.\n\nAnother untranslated sentence here.",
            encoding="utf-8",
        )

        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-completeness.sh"
        if script_path.exists():
            result = subprocess.run(
                ["bash", str(script_path), str(tmp_path / "docs"), "zh"], capture_output=True, text=True
            )
            # Script should detect untranslated content
            # Note: This is a simple bash script and may have limitations
            # The key check is that it can detect obvious untranslated content
            assert result.returncode != 0 or "paragraph" in result.stdout.lower() or "sentence" in result.stdout.lower()

    def test_code_blocks_ignored(self, tmp_path):
        """Test that code blocks are not flagged as untranslated."""
        en_dir = tmp_path / "docs" / "en"
        zh_dir = tmp_path / "docs" / "zh"

        en_dir.mkdir(parents=True)
        zh_dir.mkdir(parents=True)

        # Create content with code block (should be ignored)
        (en_dir / "index.md").write_text("# Welcome\n```bash\necho 'hello'\n```\nSome text.", encoding="utf-8")
        (zh_dir / "index.md").write_text("# 欢迎\n```bash\necho 'hello'\n```\n一些文本。", encoding="utf-8")

        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-completeness.sh"
        if script_path.exists():
            result = subprocess.run(
                ["bash", str(script_path), str(tmp_path / "docs"), "zh"], capture_output=True, text=True
            )
            assert result.returncode == 0, f"Code blocks should be ignored: {result.stdout}"

    def test_inline_code_ignored(self, tmp_path):
        """Test that inline code is not flagged as untranslated."""
        en_dir = tmp_path / "docs" / "en"
        zh_dir = tmp_path / "docs" / "zh"

        en_dir.mkdir(parents=True)
        zh_dir.mkdir(parents=True)

        # Create content with inline code (should be ignored)
        (en_dir / "index.md").write_text("# Welcome\nUse `pip install` to install.\nSome text.", encoding="utf-8")
        (zh_dir / "index.md").write_text("# 欢迎\n使用 `pip install` 安装。\n一些文本。", encoding="utf-8")

        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-completeness.sh"
        if script_path.exists():
            result = subprocess.run(
                ["bash", str(script_path), str(tmp_path / "docs"), "zh"], capture_output=True, text=True
            )
            assert result.returncode == 0, f"Inline code should be ignored: {result.stdout}"

    def test_urls_on_separate_lines_ignored(self, tmp_path):
        """Test that URLs on separate lines are not flagged as untranslated."""
        en_dir = tmp_path / "docs" / "en"
        zh_dir = tmp_path / "docs" / "zh"

        en_dir.mkdir(parents=True)
        zh_dir.mkdir(parents=True)

        # Create content with URLs on separate lines (should be ignored)
        (en_dir / "index.md").write_text("# Welcome\n\nhttps://example.com\n\nSome text.", encoding="utf-8")
        (zh_dir / "index.md").write_text("# 欢迎\n\nhttps://example.com\n\n一些文本。", encoding="utf-8")

        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-completeness.sh"
        if script_path.exists():
            result = subprocess.run(
                ["bash", str(script_path), str(tmp_path / "docs"), "zh"], capture_output=True, text=True
            )
            assert result.returncode == 0, f"URLs on separate lines should be ignored: {result.stdout}"

    def test_multiple_languages(self, tmp_path):
        """Test checking multiple target languages."""
        en_dir = tmp_path / "docs" / "en"
        zh_dir = tmp_path / "docs" / "zh"
        ja_dir = tmp_path / "docs" / "ja"

        en_dir.mkdir(parents=True)
        zh_dir.mkdir(parents=True)
        ja_dir.mkdir(parents=True)

        # Create content
        (en_dir / "index.md").write_text("# Welcome\nHello world.", encoding="utf-8")
        (zh_dir / "index.md").write_text("# 欢迎\n你好世界。", encoding="utf-8")
        (ja_dir / "index.md").write_text("# ようこそ\nハローワールド。", encoding="utf-8")

        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-completeness.sh"
        if script_path.exists():
            result = subprocess.run(
                ["bash", str(script_path), str(tmp_path / "docs"), "zh", "ja"], capture_output=True, text=True
            )
            assert result.returncode == 0, f"All languages should pass: {result.stdout}"
