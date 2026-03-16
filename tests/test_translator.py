"""Tests for translator module."""

import json

from codexspec.translator import (
    _CLI_MESSAGES_EN,
    SUPPORTED_LANGUAGES,
    apply_translations_to_template,
    extract_frontmatter_fields,
    get_translation_cache_path,
    load_cli_translations,
    load_translation_cache,
    translate,
)


class TestSupportedLanguages:
    """Test supported language constants."""

    def test_supported_languages_list(self):
        """Should contain 7 supported languages."""
        assert len(SUPPORTED_LANGUAGES) == 7
        assert "zh-CN" in SUPPORTED_LANGUAGES
        assert "ja" in SUPPORTED_LANGUAGES
        assert "ko" in SUPPORTED_LANGUAGES
        assert "es" in SUPPORTED_LANGUAGES
        assert "fr" in SUPPORTED_LANGUAGES
        assert "de" in SUPPORTED_LANGUAGES
        assert "pt-BR" in SUPPORTED_LANGUAGES


class TestTranslationCachePath:
    """Test translation cache path resolution."""

    def test_cache_path_for_language(self):
        """Should return correct cache file path."""
        result = get_translation_cache_path("zh-CN")
        assert result.name == "zh-CN.json"


class TestLoadTranslationCache:
    """Test translation cache loading."""

    def test_load_existing_cache(self, tmp_path):
        """Should load cache from existing file."""
        cache_dir = tmp_path / "translations"
        cache_dir.mkdir()
        cache_file = cache_dir / "zh-CN.json"
        cache_data = {"test": {"description": "测试"}}
        cache_file.write_text(json.dumps(cache_data), encoding="utf-8")

        result = load_translation_cache("zh-CN", cache_dir)
        assert result == cache_data

    def test_load_missing_cache(self, tmp_path):
        """Should return None for missing cache."""
        cache_dir = tmp_path / "translations"
        cache_dir.mkdir()

        result = load_translation_cache("missing-lang", cache_dir)
        assert result is None


class TestExtractFrontmatter:
    """Test frontmatter extraction."""

    def test_extract_simple_frontmatter(self):
        """Should extract description and argument-hint."""
        content = """---
description: Test description
argument-hint: Test hint
---

# Content"""
        result = extract_frontmatter_fields(content)
        assert result["description"] == "Test description"
        assert result["argument-hint"] == "Test hint"

    def test_extract_multiline_hint(self):
        """Should handle multiline argument-hint."""
        content = """---
description: Test
argument-hint: |
  Line 1
  Line 2
---

# Content"""
        result = extract_frontmatter_fields(content)
        assert result["description"] == "Test"
        assert "Line 1" in result["argument-hint"]
        assert "Line 2" in result["argument-hint"]

    def test_extract_without_hint(self):
        """Should handle missing argument-hint."""
        content = """---
description: Test only
---

# Content"""
        result = extract_frontmatter_fields(content)
        assert result["description"] == "Test only"
        assert result.get("argument-hint") is None

    def test_extract_quoted_hint(self):
        """Should handle quoted argument-hint."""
        content = """---
description: Test
argument-hint: "Describe your initial idea"
---

# Content"""
        result = extract_frontmatter_fields(content)
        assert result["description"] == "Test"
        assert result["argument-hint"] == "Describe your initial idea"


class TestApplyTranslations:
    """Test applying translations to template."""

    def test_apply_translation_simple(self):
        """Should replace description and argument-hint."""
        content = """---
description: Original description
argument-hint: Original hint
---

# Content"""
        translations = {"description": "翻译后的描述", "argument-hint": "翻译后的提示"}
        result = apply_translations_to_template(content, translations)
        assert "翻译后的描述" in result
        assert "翻译后的提示" in result
        assert "Original description" not in result

    def test_preserve_markdown_content(self):
        """Should not modify markdown content."""
        content = """---
description: Test
---

# Header

Some content here."""
        translations = {"description": "测试"}
        result = apply_translations_to_template(content, translations)
        assert "# Header" in result
        assert "Some content here." in result

    def test_apply_multiline_translation(self):
        """Should handle multiline argument-hint translation."""
        content = """---
description: Test
argument-hint: |
  Original line 1
  Original line 2
---

# Content"""
        translations = {"description": "测试", "argument-hint": "第一行\n第二行"}
        result = apply_translations_to_template(content, translations)
        assert "第一行" in result
        assert "第二行" in result


class TestIntegration:
    """End-to-end integration tests."""

    def test_full_translation_flow(self, tmp_path):
        """Test complete translation flow from template to installed file."""
        from codexspec.commands.installer import install_commands_to_subdir

        # Setup template
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "specify.md").write_text(
            """---
description: Clarify requirements through interactive Q&A
argument-hint: "Describe your initial idea"
---

# Content""",
            encoding="utf-8",
        )

        # Setup translation cache
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir()
        (translations_dir / "zh-CN.json").write_text(
            json.dumps({"specify": {"description": "通过交互式问答澄清需求", "argument-hint": "描述你的初始想法"}}),
            encoding="utf-8",
        )

        # Install with translation
        target_dir = tmp_path / "target"
        count = install_commands_to_subdir(
            target_dir, templates_dir, language="zh-CN", translations_dir=translations_dir
        )

        # Verify
        assert count == 1
        content = (target_dir / "specify.md").read_text(encoding="utf-8")
        assert "通过交互式问答澄清需求" in content
        assert "描述你的初始想法" in content
        assert "# Content" in content  # Markdown preserved

    def test_install_without_translation(self, tmp_path, monkeypatch):
        """Test that unsupported language keeps original content."""
        from codexspec import translator
        from codexspec.commands.installer import install_commands_to_subdir

        # Mock translate_with_claude_cli to avoid slow subprocess call
        monkeypatch.setattr(translator, "translate_with_claude_cli", lambda *args, **kwargs: None)

        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "test.md").write_text(
            """---
description: Test description
---

# Content""",
            encoding="utf-8",
        )

        target_dir = tmp_path / "target"
        count = install_commands_to_subdir(target_dir, templates_dir, language="unsupported-lang")

        assert count == 1
        content = (target_dir / "test.md").read_text(encoding="utf-8")
        assert "Test description" in content
        assert "# Content" in content

    def test_install_english_no_translation(self, tmp_path):
        """Test that English skips translation entirely."""
        from codexspec.commands.installer import install_commands_to_subdir

        templates_dir = tmp_path / "templates"
        templates_dir.mkdir()
        (templates_dir / "test.md").write_text(
            """---
description: Test description
---

# Content""",
            encoding="utf-8",
        )

        target_dir = tmp_path / "target"
        count = install_commands_to_subdir(target_dir, templates_dir, language="en")

        assert count == 1
        content = (target_dir / "test.md").read_text(encoding="utf-8")
        assert "Test description" in content


class TestCliMessagesBaseline:
    """Tests for CLI messages English baseline (Task 5.3)."""

    def test_baseline_has_init_messages(self):
        """Should have init command messages in baseline."""
        assert "init" in _CLI_MESSAGES_EN
        assert "migration_found" in _CLI_MESSAGES_EN["init"]
        assert "migration_complete" in _CLI_MESSAGES_EN["init"]
        assert "success_message" in _CLI_MESSAGES_EN["init"]
        assert "next_steps" in _CLI_MESSAGES_EN["init"]

    def test_baseline_has_list_commands_messages(self):
        """Should have list_commands messages in baseline."""
        assert "list_commands" in _CLI_MESSAGES_EN
        assert "header" in _CLI_MESSAGES_EN["list_commands"]
        assert "no_project" in _CLI_MESSAGES_EN["list_commands"]

    def test_baseline_has_set_language_messages(self):
        """Should have set_language messages in baseline."""
        assert "set_language" in _CLI_MESSAGES_EN
        assert "language_set" in _CLI_MESSAGES_EN["set_language"]
        assert "language_failed" in _CLI_MESSAGES_EN["set_language"]

    def test_baseline_messages_have_placeholders(self):
        """Should have parameterized messages with placeholders."""
        # Check that some messages use {key} syntax
        migration_found = _CLI_MESSAGES_EN["init"]["migration_found"]
        assert "{count}" in migration_found

        language_set = _CLI_MESSAGES_EN["set_language"]["language_set"]
        assert "{lang}" in language_set
        assert "{name}" in language_set

        commands_installed = _CLI_MESSAGES_EN["init"]["commands_installed"]
        assert "{count}" in commands_installed
        assert "{path}" in commands_installed


class TestCliTranslationIntegration:
    """Integration tests for CLI message translation (Task 5.3)."""

    def test_translate_init_messages_english(self):
        """Test translating init command messages in English."""
        result = translate("cli.init.migration_found", "en", count=5)
        assert result == "Found 5 old structure command files"

        result = translate("cli.init.migration_complete", "en")
        assert "✓" in result
        assert "Migration complete" in result

    def test_translate_list_commands_messages_english(self):
        """Test translating list_commands messages in English."""
        result = translate("cli.list_commands.header", "en", count=10)
        assert result == "CodexSpec Available Commands (10)"

        result = translate("cli.list_commands.no_project", "en")
        assert "No CodexSpec project found" in result

    def test_translate_set_language_messages_english(self):
        """Test translating set_language messages in English."""
        result = translate("cli.set_language.language_set", "en", lang="zh-CN", name="Chinese")
        assert result == "Language set to: zh-CN (Chinese)"

        result = translate("cli.set_language.language_failed", "en")
        assert "Failed to update language" in result

    def test_fallback_to_baseline_on_missing_file(self, tmp_path):
        """Test that missing translation file falls back to baseline."""
        translations_dir = tmp_path / "translations"
        translations_dir.mkdir(parents=True, exist_ok=True)

        # No translation file exists
        result = load_cli_translations("en", translations_dir=translations_dir)
        assert result == _CLI_MESSAGES_EN

    def test_all_cli_keys_accessible(self):
        """Test that all CLI keys can be accessed through translate()."""
        # Test a sample of keys from each namespace
        init_keys = ["migration_found", "migration_complete", "success_message"]
        for key in init_keys:
            result = translate(f"cli.init.{key}", "en")
            assert result != f"cli.init.{key}"  # Should not return the key itself

        list_keys = ["header", "no_project", "usage_hint"]
        for key in list_keys:
            result = translate(f"cli.list_commands.{key}", "en")
            assert result != f"cli.list_commands.{key}"

        lang_keys = ["language_set", "language_failed", "commit_lang_set"]
        for key in lang_keys:
            result = translate(f"cli.set_language.{key}", "en")
            assert result != f"cli.set_language.{key}"
