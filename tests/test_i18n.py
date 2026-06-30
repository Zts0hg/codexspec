"""Tests for CodexSpec i18n module."""

import os

from codexspec.i18n import (
    generate_config_content,
    get_all_supported_languages,
    get_commit_language,
    get_document_language,
    get_interaction_language,
    get_language_from_env,
    get_language_name,
    get_project_language,
    get_supported_languages,
    is_supported_language,
    normalize_locale,
    update_language_field,
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


class TestGetAllSupportedLanguages:
    """Tests for get_all_supported_languages function."""

    def test_returns_list_of_tuples(self) -> None:
        """Should return a list of (code, name) tuples."""
        languages = get_all_supported_languages()
        assert isinstance(languages, list)
        assert all(isinstance(lang, tuple) and len(lang) == 2 for lang in languages)

    def test_first_element_is_english(self) -> None:
        """First element should be ('en', 'English')."""
        languages = get_all_supported_languages()
        assert languages[0] == ("en", "English")

    def test_contains_all_pretranslated_languages(self) -> None:
        """Should contain all pre-translated languages from translator."""
        from codexspec.translator import SUPPORTED_LANGUAGES

        languages = get_all_supported_languages()
        codes = [code for code, _ in languages]

        # Should contain English
        assert "en" in codes

        # Should contain all pre-translated languages
        for lang in SUPPORTED_LANGUAGES:
            assert lang in codes, f"Missing pre-translated language: {lang}"

    def test_language_names_correct(self) -> None:
        """All language names should be correctly retrieved."""
        languages = get_all_supported_languages()

        for code, name in languages:
            expected_name = get_language_name(code)
            assert name == expected_name, f"Name mismatch for {code}: {name} != {expected_name}"

    def test_returns_correct_count(self) -> None:
        """Should return correct count of languages."""
        from codexspec.translator import SUPPORTED_LANGUAGES

        languages = get_all_supported_languages()
        expected_count = 1 + len(SUPPORTED_LANGUAGES)  # en + pre-translated

        assert len(languages) == expected_count


class TestGenerateConfigContent:
    """Tests for generate_config_content (sparse, per-dimension signature)."""

    def test_default_config_is_sparse_output_only(self) -> None:
        """No-arg default writes only `output: "en"` (sparse, not all four keys)."""
        content = generate_config_content()
        assert 'output: "en"' in content
        assert 'version: "1.0"' in content
        # Sparse: the other dimensions are intentionally absent.
        assert "interaction:" not in content
        assert "document:" not in content
        assert "commit:" not in content

    def test_output_only_is_normalized(self) -> None:
        """output is normalized and written alone."""
        content = generate_config_content(output="zh")
        assert 'output: "zh-CN"' in content
        assert "interaction:" not in content
        assert "document:" not in content
        assert "commit:" not in content

    def test_specific_keys_only(self) -> None:
        """Passing only specific dimensions writes exactly those keys, no output."""
        content = generate_config_content(interaction="en", document="zh-CN", commit="en")
        assert 'interaction: "en"' in content
        assert 'document: "zh-CN"' in content
        assert 'commit: "en"' in content
        assert "output:" not in content

    def test_output_plus_overrides(self) -> None:
        """output can be combined with specific dimensions."""
        content = generate_config_content(output="en", commit="ja")
        assert 'output: "en"' in content
        assert 'commit: "ja"' in content
        assert "interaction:" not in content
        assert "document:" not in content

    def test_custom_date(self) -> None:
        """Custom date should be included."""
        content = generate_config_content(created="2025-01-15")
        assert 'created: "2025-01-15"' in content

    def test_contains_templates_setting(self) -> None:
        """Config should always include the templates setting."""
        content = generate_config_content()
        assert 'templates: "en"' in content

    def test_contains_project_section(self) -> None:
        """Config should include the project section."""
        content = generate_config_content()
        assert "project:" in content
        assert 'ai: "claude"' in content


class TestLanguageResolution:
    """Tests for get_interaction_language / get_document_language resolution."""

    @staticmethod
    def _write_config(tmp_path, body: str):
        cfg = tmp_path / ".codexspec" / "config.yml"
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text(body, encoding="utf-8")
        return cfg

    def test_explicit_interaction_and_document(self, tmp_path) -> None:
        """Explicit interaction/document should win over output."""
        cfg = self._write_config(tmp_path, 'language:\n  interaction: "zh-CN"\n  document: "en"\n  output: "en"\n')
        assert get_interaction_language(cfg) == "zh-CN"
        assert get_document_language(cfg) == "en"

    def test_fallback_to_output_when_primary_absent(self, tmp_path) -> None:
        """Missing primary field should fall back to output (legacy)."""
        cfg = self._write_config(tmp_path, 'language:\n  output: "zh-CN"\n')
        assert get_interaction_language(cfg) == "zh-CN"
        assert get_document_language(cfg) == "zh-CN"

    def test_explicit_overrides_output(self, tmp_path) -> None:
        """Explicit primary should override output."""
        cfg = self._write_config(tmp_path, 'language:\n  interaction: "ja"\n  output: "en"\n')
        assert get_interaction_language(cfg) == "ja"

    def test_defaults_to_en_when_nothing_set(self, tmp_path) -> None:
        """No interaction/document/output should resolve to en."""
        cfg = self._write_config(tmp_path, 'language:\n  templates: "en"\n')
        assert get_interaction_language(cfg) == "en"
        assert get_document_language(cfg) == "en"

    def test_missing_config_file_returns_en(self, tmp_path) -> None:
        """A non-existent config file should resolve to en."""
        cfg = tmp_path / "does-not-exist.yml"
        assert get_interaction_language(cfg) == "en"
        assert get_document_language(cfg) == "en"

    def test_normalizes_aliases(self, tmp_path) -> None:
        """Resolved values should be normalized (alias -> canonical)."""
        cfg = self._write_config(tmp_path, 'language:\n  interaction: "chinese"\n  document: "jp"\n')
        assert get_interaction_language(cfg) == "zh-CN"
        assert get_document_language(cfg) == "ja"

    def test_unquoted_values(self, tmp_path) -> None:
        """Unquoted YAML values should be read correctly."""
        cfg = self._write_config(tmp_path, "language:\n  document: ko\n")
        assert get_document_language(cfg) == "ko"

    def test_unknown_workflow_section_does_not_break_resolution(self, tmp_path) -> None:
        """A `workflow.auto_next` key (the auto-next feature) is ignored by i18n: the
        config still parses and interaction/document resolution is unaffected. Guards
        backwards-compatibility for opt-in feature keys (NFR-001)."""
        import yaml

        cfg = self._write_config(
            tmp_path,
            'version: "1.0"\n'
            "language:\n"
            '  output: "en"\n'
            '  interaction: "zh-CN"\n'
            '  document: "en"\n'
            "workflow:\n"
            "  auto_next: true\n",
        )
        # The config parses cleanly and the unknown key round-trips.
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
        assert data["workflow"]["auto_next"] is True
        # i18n resolution is unaffected by the unknown workflow section.
        assert get_interaction_language(cfg) == "zh-CN"
        assert get_document_language(cfg) == "en"

    def test_output_only_config_no_deprecation(self, tmp_path, capsys) -> None:
        """NFR-001/NFR-002: output-only config resolves identically for all three
        accessors and emits no deprecation warning."""
        cfg = self._write_config(tmp_path, 'language:\n  output: "zh-CN"\n')
        assert get_interaction_language(cfg) == "zh-CN"
        assert get_document_language(cfg) == "zh-CN"
        assert get_project_language(cfg) == "zh-CN"
        captured = capsys.readouterr()
        assert "deprecat" not in captured.out.lower()
        assert "deprecat" not in captured.err.lower()

    def test_project_language_is_interaction_alias(self, tmp_path) -> None:
        """get_project_language should mirror interaction (backward-compat alias)."""
        cfg = self._write_config(tmp_path, 'language:\n  interaction: "ko"\n  output: "en"\n')
        assert get_project_language(cfg) == "ko"
        # output-only legacy config: alias returns output (behavior unchanged)
        cfg_legacy = self._write_config(tmp_path, 'language:\n  output: "fr"\n')
        assert get_project_language(cfg_legacy) == "fr"

    def test_commit_explicit_wins(self, tmp_path) -> None:
        """Explicit commit should override output."""
        cfg = self._write_config(tmp_path, 'language:\n  commit: "ja"\n  output: "en"\n')
        assert get_commit_language(cfg) == "ja"

    def test_commit_falls_back_to_output(self, tmp_path) -> None:
        """REQ-004: missing commit should fall back to output."""
        cfg = self._write_config(tmp_path, 'language:\n  output: "zh-CN"\n')
        assert get_commit_language(cfg) == "zh-CN"

    def test_commit_defaults_to_en(self, tmp_path) -> None:
        """Neither commit nor output should resolve to en (matches other accessors)."""
        cfg = self._write_config(tmp_path, 'language:\n  templates: "en"\n')
        assert get_commit_language(cfg) == "en"

    def test_commit_missing_config_file_returns_en(self, tmp_path) -> None:
        """A non-existent config file should resolve commit to en."""
        cfg = tmp_path / "does-not-exist.yml"
        assert get_commit_language(cfg) == "en"


class TestUpdateLanguageField:
    """Tests for update_language_field (update-or-insert)."""

    def test_update_existing_field(self, tmp_path) -> None:
        cfg = tmp_path / "config.yml"
        cfg.write_text('language:\n  interaction: "en"\n  output: "en"\n', encoding="utf-8")
        assert update_language_field(cfg, "interaction", "zh-CN") is True
        assert 'interaction: "zh-CN"' in cfg.read_text(encoding="utf-8")

    def test_insert_when_absent(self, tmp_path) -> None:
        cfg = tmp_path / "config.yml"
        cfg.write_text('language:\n  output: "en"\n', encoding="utf-8")
        assert update_language_field(cfg, "document", "ja") is True
        content = cfg.read_text(encoding="utf-8")
        assert 'document: "ja"' in content
        assert content.index("language:") < content.index('document: "ja"')

    def test_returns_false_without_language_section(self, tmp_path) -> None:
        cfg = tmp_path / "config.yml"
        cfg.write_text('version: "1.0"\n', encoding="utf-8")
        assert update_language_field(cfg, "interaction", "en") is False

    def test_normalizes_value(self, tmp_path) -> None:
        cfg = tmp_path / "config.yml"
        cfg.write_text('language:\n  interaction: "en"\n', encoding="utf-8")
        update_language_field(cfg, "interaction", "chinese")
        assert 'interaction: "zh-CN"' in cfg.read_text(encoding="utf-8")
