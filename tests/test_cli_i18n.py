"""Tests for CLI i18n functionality."""

import json
import time
from unittest.mock import patch

from codexspec.translator import (
    _CLI_MESSAGES_EN,
    load_cli_translations,
    translate,
)


class TestLoadCliTranslations:
    """Tests for load_cli_translations function."""

    def test_load_cli_translations_file_exists(self, tmp_path):
        """Test loading from an existing translation file."""
        # Create a mock translation file
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)

        en_json = translations_dir / "en.json"
        en_json.write_text(
            json.dumps(
                {
                    "cli": {
                        "init": {
                            "migration_found": "Found {count} old structure command files",
                        },
                        "list_commands": {
                            "header": "Commands List ({count})",
                            "no_project": "No project found",
                        },
                        "set_language": {
                            "language_set": "Language set to: {lang} ({name})",
                        },
                    }
                }
            ),
            encoding="utf-8",
        )

        # Call the function
        result = load_cli_translations("en", translations_dir=translations_dir)

        assert result["init"]["migration_found"] == "Found {count} old structure command files"
        assert result["list_commands"]["header"] == "Commands List ({count})"
        assert result["list_commands"]["no_project"] == "No project found"
        assert result["set_language"]["language_set"] == "Language set to: {lang} ({name})"

    def test_load_cli_translations_file_not_exists(self, tmp_path):
        """Test fallback to code baseline when file doesn't exist."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)

        result = load_cli_translations("nonexistent", translations_dir=translations_dir)
        # Should fall back to code baseline
        assert result == _CLI_MESSAGES_EN

    def test_load_cli_translations_file_corrupted(self, tmp_path):
        """Test fallback when JSON file is corrupted."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        en_json = translations_dir / "en.json"
        en_json.write_text("invalid json content", encoding="utf-8")

        result = load_cli_translations("en", translations_dir=translations_dir)
        # Should fall back to code baseline
        assert result == _CLI_MESSAGES_EN

    def test_load_cli_translations_empty_language(self, tmp_path):
        """Test fallback to code baseline when language code is empty."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)

        result = load_cli_translations("", translations_dir=translations_dir)
        # Should fall back to code baseline
        assert result == _CLI_MESSAGES_EN

    def test_load_cli_translations_missing_cli_key(self, tmp_path):
        """Test partial translations are loaded correctly."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        en_json = translations_dir / "en.json"
        en_json.write_text(
            json.dumps(
                {
                    "cli": {
                        "init": {
                            "migration_found": "Found {count} old files",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        result = load_cli_translations("en", translations_dir=translations_dir)

        # Should have init.migration_found
        assert result["init"]["migration_found"] == "Found {count} old files"
        # Should not have migration_confirm
        assert "migration_confirm" not in result["init"]


class TestTranslate:
    """Tests for translate function."""

    @patch("codexspec.translator.get_translations_dir")
    def test_translate_basic(self, mock_get_translations_dir, tmp_path):
        """Test basic translation functionality."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        mock_get_translations_dir.return_value = translations_dir

        # Create a mock translation file
        en_json = translations_dir / "en.json"
        en_json.write_text(
            json.dumps(
                {
                    "cli": {
                        "init": {
                            "migration_found": "Found {count} old files",
                            "migration_complete": "✓ Migration complete",
                        },
                        "list_commands": {
                            "header": "Commands List ({count})",
                            "no_project": "No project found",
                        },
                        "set_language": {
                            "language_set": "Language set to: {lang} ({name})",
                        },
                    }
                }
            ),
            encoding="utf-8",
        )

        result = translate("cli.init.migration_found", "en", count=3)
        assert result == "Found 3 old files"

        result = translate("cli.init.migration_complete", "en")
        assert result == "✓ Migration complete"

        result = translate("cli.list_commands.header", "en", count=5)
        assert result == "Commands List (5)"

        result = translate("cli.set_language.language_set", "en", lang="zh-CN", name="中文")
        assert result == "Language set to: zh-CN (中文)"

    @patch("codexspec.translator.get_translations_dir")
    def test_translate_missing_param(self, mock_get_translations_dir, tmp_path):
        """Test parameterized message with missing parameter."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        mock_get_translations_dir.return_value = translations_dir

        en_json = translations_dir / "en.json"
        en_json.write_text(
            json.dumps(
                {
                    "cli": {
                        "init": {
                            "migration_found": "Found {count} old files",
                        },
                    }
                }
            ),
            encoding="utf-8",
        )

        result = translate("cli.init.migration_found", "en")
        # Missing parameter - should return original template string
        assert result == "Found {count} old files"

    @patch("codexspec.translator.get_translations_dir")
    def test_translate_unknown_language(self, mock_get_translations_dir, tmp_path):
        """Test translation for unknown language falls back to English."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        mock_get_translations_dir.return_value = translations_dir

        result = translate("cli.init.migration_found", "nonexistent", count=3)
        # Falls back to English baseline
        assert result == "Found 3 old structure command files"

    @patch("codexspec.translator.get_translations_dir")
    def test_translate_missing_key(self, mock_get_translations_dir, tmp_path):
        """Test missing key returns the key itself."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        mock_get_translations_dir.return_value = translations_dir

        result = translate("cli.init.nonexistent_key", "en")
        # Key not found - returns the key itself
        assert result == "cli.init.nonexistent_key"


class TestEdgeCases:
    """Tests for edge cases (Task 5.1)."""

    def test_none_language_parameter(self, tmp_path):
        """Test that None language falls back to English baseline."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)

        result = load_cli_translations(None, translations_dir=translations_dir)
        # Should fall back to code baseline
        assert result == _CLI_MESSAGES_EN

    def test_empty_json_file(self, tmp_path):
        """Test handling of empty JSON file."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        en_json = translations_dir / "en.json"
        en_json.write_text("{}", encoding="utf-8")

        result = load_cli_translations("en", translations_dir=translations_dir)
        # Empty object has no "cli" key, should fall back to baseline
        assert result == _CLI_MESSAGES_EN

    def test_json_with_wrong_structure(self, tmp_path):
        """Test handling of JSON with wrong structure (no cli key)."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        en_json = translations_dir / "en.json"
        en_json.write_text(json.dumps({"messages": {"greeting": "Hello"}}), encoding="utf-8")

        result = load_cli_translations("en", translations_dir=translations_dir)
        # No "cli" key, should fall back to baseline
        assert result == _CLI_MESSAGES_EN

    def test_unicode_in_translations(self, tmp_path):
        """Test handling of Unicode characters in translations."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        en_json = translations_dir / "zh-CN.json"
        en_json.write_text(
            json.dumps(
                {
                    "cli": {
                        "init": {
                            "success_message": "项目初始化成功！🎉",
                            "tips_header": "💡 提示：",
                        }
                    }
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

        result = load_cli_translations("zh-CN", translations_dir=translations_dir)
        assert result["init"]["success_message"] == "项目初始化成功！🎉"
        assert result["init"]["tips_header"] == "💡 提示："

    def test_special_characters_in_params(self, tmp_path):
        """Test handling of special characters in parameter values."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)
        en_json = translations_dir / "en.json"
        en_json.write_text(
            json.dumps(
                {
                    "cli": {
                        "init": {
                            "created_directory": "Created directory: {path}",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        with patch("codexspec.translator.get_translations_dir") as mock_get:
            mock_get.return_value = translations_dir
            result = translate("cli.init.created_directory", "en", path="/path/with spaces/and'quotes")
            assert result == "Created directory: /path/with spaces/and'quotes"

    def test_invalid_key_format(self, tmp_path):
        """Test handling of invalid key format."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)

        with patch("codexspec.translator.get_translations_dir") as mock_get:
            mock_get.return_value = translations_dir

            # Key with only one part - should return the key
            result = translate("invalid", "en")
            assert result == "invalid"

            # Key with only two parts - should return the key
            result = translate("cli.init", "en")
            assert result == "cli.init"

    def test_very_long_language_code(self, tmp_path):
        """Test handling of very long language codes."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)

        # Very long code that doesn't exist
        result = load_cli_translations("xx-XX-very-long-suffix", translations_dir=translations_dir)
        # Should fall back to baseline
        assert result == _CLI_MESSAGES_EN


class TestPerformance:
    """Tests for performance requirements (Task 5.2)."""

    def test_translation_cache_load_performance(self, tmp_path):
        """Test that translation cache loads in < 50ms."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)

        # Create a reasonably sized translation file
        en_json = translations_dir / "en.json"
        en_json.write_text(
            json.dumps(
                {
                    "cli": {
                        "init": {f"key_{i}": f"Message {i}" for i in range(100)},
                        "list_commands": {f"key_{i}": f"Message {i}" for i in range(50)},
                        "set_language": {f"key_{i}": f"Message {i}" for i in range(20)},
                    }
                }
            ),
            encoding="utf-8",
        )

        # Measure load time
        start_time = time.perf_counter()
        for _ in range(10):  # Run 10 times to get more accurate measurement
            load_cli_translations("en", translations_dir=translations_dir)
        end_time = time.perf_counter()

        avg_time_ms = (end_time - start_time) * 100  # Convert to ms (total/10 * 1000)
        assert avg_time_ms < 50, f"Translation cache load took {avg_time_ms:.2f}ms, expected < 50ms"

    def test_translate_function_performance(self, tmp_path):
        """Test that translate function is performant."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)

        en_json = translations_dir / "en.json"
        en_json.write_text(
            json.dumps(
                {
                    "cli": {
                        "init": {
                            "migration_found": "Found {count} old files",
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        with patch("codexspec.translator.get_translations_dir") as mock_get:
            mock_get.return_value = translations_dir

            # Measure translate time
            start_time = time.perf_counter()
            for i in range(100):
                translate("cli.init.migration_found", "en", count=i)
            end_time = time.perf_counter()

            avg_time_ms = (end_time - start_time) * 10  # Convert to ms (total/100 * 1000)
            assert avg_time_ms < 5, f"Translate function took {avg_time_ms:.2f}ms per call, expected < 5ms"
