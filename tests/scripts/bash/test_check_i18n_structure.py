"""Tests for i18n structure check script."""

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
class TestCheckI18nStructure:
    """Tests for the structure consistency check script."""

    def test_script_exists(self):
        """Script should exist at scripts/bash/check-i18n-structure.sh."""
        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-structure.sh"
        assert script_path.exists(), f"Script not found at {script_path}"

    def test_script_is_executable(self):
        """Script should be executable."""
        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-structure.sh"
        if script_path.exists():
            result = subprocess.run(["bash", "-n", str(script_path)], capture_output=True, text=True)
            # bash -n checks syntax without execution
            assert result.returncode == 0, f"Script has syntax errors: {result.stderr}"

    def test_correct_structure_passes(self, tmp_path):
        """Test that correct structure passes validation."""
        # Create correct structure
        en_dir = tmp_path / "docs" / "en"
        zh_dir = tmp_path / "docs" / "zh"

        en_dir.mkdir(parents=True)
        zh_dir.mkdir(parents=True)

        # Create matching files
        (en_dir / "index.md").write_text("# Test\nContent", encoding="utf-8")
        (en_dir / "guide.md").write_text("# Guide\nContent", encoding="utf-8")
        (zh_dir / "index.md").write_text("# 测试\n内容", encoding="utf-8")
        (zh_dir / "guide.md").write_text("# 指南\n内容", encoding="utf-8")

        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-structure.sh"
        if script_path.exists():
            result = subprocess.run(["bash", str(script_path), str(tmp_path / "docs")], capture_output=True, text=True)
            assert result.returncode == 0, f"Expected pass, got: {result.stdout}"

    def test_missing_file_fails(self, tmp_path):
        """Test that missing files are detected."""
        en_dir = tmp_path / "docs" / "en"
        zh_dir = tmp_path / "docs" / "zh"

        en_dir.mkdir(parents=True)
        zh_dir.mkdir(parents=True)

        # Create files in en but not in zh
        (en_dir / "index.md").write_text("# Test\nContent", encoding="utf-8")
        (en_dir / "guide.md").write_text("# Guide\nContent", encoding="utf-8")
        (zh_dir / "index.md").write_text("# 测试\n内容", encoding="utf-8")
        # guide.md missing in zh

        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-structure.sh"
        if script_path.exists():
            result = subprocess.run(["bash", str(script_path), str(tmp_path / "docs")], capture_output=True, text=True)
            assert result.returncode != 0, "Should fail when files are missing"

    def test_extra_file_detected(self, tmp_path):
        """Test that extra files in translation directories are detected."""
        en_dir = tmp_path / "docs" / "en"
        zh_dir = tmp_path / "docs" / "zh"

        en_dir.mkdir(parents=True)
        zh_dir.mkdir(parents=True)

        # Create matching files
        (en_dir / "index.md").write_text("# Test\nContent", encoding="utf-8")
        (zh_dir / "index.md").write_text("# 测试\n内容", encoding="utf-8")
        # Extra file in zh
        (zh_dir / "extra.md").write_text("# 额外\n内容", encoding="utf-8")

        script_path = PROJECT_ROOT / "scripts/bash/check-i18n-structure.sh"
        if script_path.exists():
            result = subprocess.run(["bash", str(script_path), str(tmp_path / "docs")], capture_output=True, text=True)
            # Extra files might be a warning or error depending on strictness
            assert "extra" in result.stdout.lower() or result.returncode != 0
