"""Tests for CodexSpec i18n module."""

import os

from codexspec.i18n import (
    generate_config_content,
    get_language_from_env,
    get_language_name,
    get_supported_languages,
    is_supported_language,
    normalize_locale,
)


class TestNormalizeLocale:
    """Tests for normalize_locale function."""

    def test_normalize_none_returns_en(self) -> None:
        """None input should return 'en'."""
        assert normalize_locale(None) == "en"

    def test_normalize_empty_returns_en(self) -> None:
        """Empty string should return 'en'."""
        assert normalize_locale("") == "en"

    def test_normalize_chinese_aliases(self) -> None:
        """Chinese language aliases should normalize to zh-CN."""
        assert normalize_locale("zh") == "zh-CN"
        assert normalize_locale("zh-cn") == "zh-CN"
        assert normalize_locale("ZH-CN") == "zh-CN"
        assert normalize_locale("zh-Hans") == "zh-CN"
        assert normalize_locale("chinese") == "zh-CN"
        assert normalize_locale("chinese-simplified") == "zh-CN"

    def test_normalize_traditional_chinese(self) -> None:
        """Traditional Chinese should normalize to zh-TW."""
        assert normalize_locale("zh-tw") == "zh-TW"
        assert normalize_locale("zh-Hant") == "zh-TW"
        assert normalize_locale("chinese-traditional") == "zh-TW"

    def test_normalize_japanese_aliases(self) -> None:
        """Japanese language aliases should normalize to ja."""
        assert normalize_locale("ja") == "ja"
        assert normalize_locale("jp") == "ja"
        assert normalize_locale("japanese") == "ja"
        assert normalize_locale("JA") == "ja"

    def test_normalize_korean_aliases(self) -> None:
        """Korean language aliases should normalize to ko."""
        assert normalize_locale("ko") == "ko"
        assert normalize_locale("kr") == "ko"
        assert normalize_locale("korean") == "ko"

    def test_normalize_english_aliases(self) -> None:
        """English language aliases should normalize to en."""
        assert normalize_locale("en") == "en"
        assert normalize_locale("en-US") == "en"
        assert normalize_locale("en-GB") == "en"
        assert normalize_locale("english") == "en"

    def test_normalize_unknown_locale(self) -> None:
        """Unknown locales should be normalized to lowercase with proper casing."""
        assert normalize_locale("XX-YY") == "xx-YY"
        assert normalize_locale("abc") == "abc"

    def test_normalize_preserves_format(self) -> None:
        """Unknown locales with region should preserve format."""
        result = normalize_locale("custom-REGION")
        assert result == "custom-REGION"


class TestGetLanguageFromEnv:
    """Tests for get_language_from_env function."""

    def test_codexspec_lang_env(self, clean_env: None) -> None:
        """CODEXSPEC_LANG environment variable should be used."""
        os.environ["CODEXSPEC_LANG"] = "zh-CN"
        assert get_language_from_env() == "zh-CN"

    def test_codexspec_lang_overrides_lang(self, clean_env: None) -> None:
        """CODEXSPEC_LANG should take precedence over LANG."""
        os.environ["CODEXSPEC_LANG"] = "ja"
        os.environ["LANG"] = "en_US.UTF-8"
        assert get_language_from_env() == "ja"

    def test_lang_env_unix_format(self, clean_env: None) -> None:
        """LANG environment variable in Unix format should be parsed."""
        os.environ["LANG"] = "zh_CN.UTF-8"
        assert get_language_from_env() == "zh-CN"

    def test_lang_env_english(self, clean_env: None) -> None:
        """English LANG should be normalized."""
        os.environ["LANG"] = "en_US.UTF-8"
        assert get_language_from_env() == "en"

    def test_no_env_returns_none(self, clean_env: None) -> None:
        """No environment variables should return None."""
        assert get_language_from_env() is None


class TestIsSupportedLanguage:
    """Tests for is_supported_language function."""

    def test_supported_languages(self) -> None:
        """Common languages should be supported."""
        assert is_supported_language("en") is True
        assert is_supported_language("zh-CN") is True
        assert is_supported_language("ja") is True
        assert is_supported_language("ko") is True
        assert is_supported_language("es") is True
        assert is_supported_language("fr") is True

    def test_aliases_are_supported(self) -> None:
        """Language aliases should be recognized as supported."""
        assert is_supported_language("zh") is True
        assert is_supported_language("jp") is True
        assert is_supported_language("chinese") is True

    def test_unsupported_language(self) -> None:
        """Unknown languages should not be marked as supported."""
        assert is_supported_language("xx") is False
        assert is_supported_language("unknown") is False


class TestGetLanguageName:
    """Tests for get_language_name function."""

    def test_english_name(self) -> None:
        """English should return correct name."""
        assert get_language_name("en") == "English"

    def test_chinese_simplified_name(self) -> None:
        """Simplified Chinese should return correct name."""
        assert get_language_name("zh-CN") == "Chinese (Simplified)"

    def test_chinese_traditional_name(self) -> None:
        """Traditional Chinese should return correct name."""
        assert get_language_name("zh-TW") == "Chinese (Traditional)"

    def test_japanese_name(self) -> None:
        """Japanese should return correct name."""
        assert get_language_name("ja") == "Japanese"

    def test_unknown_language_returns_code(self) -> None:
        """Unknown languages should return the code itself."""
        assert get_language_name("xx") == "xx"


class TestGetSupportedLanguages:
    """Tests for get_supported_languages function."""

    def test_returns_list(self) -> None:
        """Should return a list of tuples."""
        languages = get_supported_languages()
        assert isinstance(languages, list)
        assert all(isinstance(lang, tuple) and len(lang) == 2 for lang in languages)

    def test_contains_common_languages(self) -> None:
        """Should contain common languages."""
        languages = get_supported_languages()
        codes = [code for code, _ in languages]

        assert "en" in codes
        assert "zh-CN" in codes
        assert "ja" in codes
        assert "ko" in codes

    def test_all_have_names(self) -> None:
        """All languages should have non-empty names."""
        languages = get_supported_languages()

        for code, name in languages:
            assert isinstance(name, str)
            assert len(name) > 0


class TestGenerateConfigContent:
    """Tests for generate_config_content function."""

    def test_default_config(self) -> None:
        """Default config should use English."""
        content = generate_config_content()
        assert 'output: "en"' in content
        assert 'version: "1.0"' in content

    def test_custom_language(self) -> None:
        """Custom language should be normalized and included."""
        content = generate_config_content(language="zh")
        assert 'output: "zh-CN"' in content

    def test_custom_date(self) -> None:
        """Custom date should be included."""
        content = generate_config_content(created="2025-01-15")
        assert 'created: "2025-01-15"' in content

    def test_contains_templates_setting(self) -> None:
        """Config should include templates setting."""
        content = generate_config_content()
        assert 'templates: "en"' in content

    def test_contains_project_section(self) -> None:
        """Config should include project section."""
        content = generate_config_content()
        assert "project:" in content
        assert 'ai: "claude"' in content
