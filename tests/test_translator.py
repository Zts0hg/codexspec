"""Tests for translator module."""

import json

from codexspec.translator import (
    SUPPORTED_LANGUAGES,
    apply_translations_to_template,
    extract_frontmatter_fields,
    get_translation_cache_path,
    load_translation_cache,
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

    def test_install_without_translation(self, tmp_path):
        """Test that unsupported language keeps original content."""
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
