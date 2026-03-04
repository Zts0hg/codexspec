"""Tests for CodexSpec i18n glossary configuration.

This module tests the glossary.yml configuration file used for document translation.
The glossary defines:
- Terms that should remain in English (keep_english)
- Translations for specific terms (translations)
- Rules for intelligent term handling (rules)
"""

import re
from pathlib import Path

import pytest
import yaml

# Path to the glossary configuration file
GLOSSARY_PATH = Path(".codexspec/i18n/glossary.yml")


@pytest.fixture
def glossary_content():
    """Load glossary.yml content."""
    if not GLOSSARY_PATH.exists():
        pytest.skip("glossary.yml not found - this test should run before implementation")
    with open(GLOSSARY_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


class TestGlossaryStructure:
    """Tests for valid glossary YAML structure."""

    def test_glossary_file_exists(self):
        """Glossary file should exist at .codexspec/i18n/glossary.yml."""
        assert GLOSSARY_PATH.exists(), f"Glossary file not found at {GLOSSARY_PATH}"

    def test_glossary_is_valid_yaml(self):
        """Glossary file should be valid YAML."""
        with open(GLOSSARY_PATH, encoding="utf-8") as f:
            content = yaml.safe_load(f)
        assert content is not None, "Glossary file is empty or invalid YAML"

    def test_glossary_has_version(self, glossary_content):
        """Glossary should have a version field."""
        assert "version" in glossary_content, "Glossary missing 'version' field"
        assert glossary_content["version"] is not None

    def test_glossary_has_keep_english(self, glossary_content):
        """Glossary should have keep_english field."""
        assert "keep_english" in glossary_content, "Glossary missing 'keep_english' field"
        assert isinstance(glossary_content["keep_english"], list), "'keep_english' should be a list"

    def test_glossary_has_translations(self, glossary_content):
        """Glossary should have translations field."""
        assert "translations" in glossary_content, "Glossary missing 'translations' field"
        assert isinstance(glossary_content["translations"], dict), "'translations' should be a dict"

    def test_glossary_has_rules(self, glossary_content):
        """Glossary should have rules field."""
        assert "rules" in glossary_content, "Glossary missing 'rules' field"
        assert isinstance(glossary_content["rules"], list), "'rules' should be a list"


class TestKeepEnglishField:
    """Tests for keep_english field validation."""

    def test_keep_english_is_list_of_strings(self, glossary_content):
        """keep_english should be a list of strings."""
        keep_english = glossary_content.get("keep_english", [])
        for item in keep_english:
            assert isinstance(item, str), f"keep_english item '{item}' should be a string"

    def test_keep_english_has_common_terms(self, glossary_content):
        """keep_english should contain common technical terms."""
        keep_english = glossary_content.get("keep_english", [])
        # These are commonly used terms that should not be translated
        expected_patterns = [
            "CLI",  # Command Line Interface
            "API",  # Application Programming Interface
            "YAML",  # File format
            "JSON",  # File format
        ]
        for pattern in expected_patterns:
            assert pattern in keep_english, f"'{pattern}' should be in keep_english list"

    def test_keep_english_no_duplicates(self, glossary_content):
        """keep_english should not have duplicate entries."""
        keep_english = glossary_content.get("keep_english", [])
        assert len(keep_english) == len(set(keep_english)), "keep_english has duplicate entries"


class TestTranslationsField:
    """Tests for translations field validation."""

    def test_translations_is_dict_of_dicts(self, glossary_content):
        """translations should be a dict where each value is a dict."""
        translations = glossary_content.get("translations", {})
        for term, lang_translations in translations.items():
            assert isinstance(lang_translations, dict), (
                f"Translation for '{term}' should be a dict of language -> translation"
            )

    def test_translations_have_required_languages(self, glossary_content):
        """Each translation entry should have all required target languages."""
        translations = glossary_content.get("translations", {})
        required_languages = ["zh", "ja", "ko", "es", "fr", "de", "pt-BR"]

        for term, lang_translations in translations.items():
            for lang in required_languages:
                assert lang in lang_translations, f"Translation for '{term}' missing language '{lang}'"

    def test_translations_values_are_strings(self, glossary_content):
        """All translation values should be strings."""
        translations = glossary_content.get("translations", {})
        for term, lang_translations in translations.items():
            for lang, translation in lang_translations.items():
                assert isinstance(translation, str), f"Translation for '{term}' in '{lang}' should be a string"

    def test_translations_not_empty(self, glossary_content):
        """Translation strings should not be empty."""
        translations = glossary_content.get("translations", {})
        for term, lang_translations in translations.items():
            for lang, translation in lang_translations.items():
                assert len(translation.strip()) > 0, f"Translation for '{term}' in '{lang}' is empty"


class TestRulesField:
    """Tests for rules field validation."""

    def test_rules_is_list_of_dicts(self, glossary_content):
        """rules should be a list of dictionaries."""
        rules = glossary_content.get("rules", [])
        for rule in rules:
            assert isinstance(rule, dict), f"Rule '{rule}' should be a dict"

    def test_rules_have_required_fields(self, glossary_content):
        """Each rule should have pattern, description, and action fields."""
        rules = glossary_content.get("rules", [])
        required_fields = ["pattern", "description", "action"]

        for i, rule in enumerate(rules):
            for field in required_fields:
                assert field in rule, f"Rule {i} missing '{field}' field"

    def test_rules_patterns_are_valid_regex(self, glossary_content):
        """Each rule pattern should be a valid regular expression."""
        rules = glossary_content.get("rules", [])

        for i, rule in enumerate(rules):
            pattern = rule.get("pattern", "")
            try:
                re.compile(pattern)
            except re.error as e:
                pytest.fail(f"Rule {i} has invalid regex pattern '{pattern}': {e}")

    def test_rules_actions_are_valid(self, glossary_content):
        """Each rule action should be 'keep' or 'translate'."""
        rules = glossary_content.get("rules", [])
        valid_actions = ["keep", "translate"]

        for i, rule in enumerate(rules):
            action = rule.get("action", "")
            assert action in valid_actions, f"Rule {i} has invalid action '{action}'. Must be one of: {valid_actions}"


class TestGlossaryCompleteness:
    """Tests for overall glossary completeness."""

    def test_glossary_has_minimum_terms(self, glossary_content):
        """Glossary should have a minimum number of translated terms."""
        translations = glossary_content.get("translations", {})
        min_terms = 5  # At least 5 terms should be translated
        assert len(translations) >= min_terms, (
            f"Glossary should have at least {min_terms} translated terms, has {len(translations)}"
        )

    def test_glossary_has_minimum_keep_english(self, glossary_content):
        """Glossary should have a minimum number of keep_english terms."""
        keep_english = glossary_content.get("keep_english", [])
        min_terms = 10  # At least 10 terms should be kept in English
        assert len(keep_english) >= min_terms, (
            f"Glossary should have at least {min_terms} keep_english terms, has {len(keep_english)}"
        )

    def test_glossary_has_minimum_rules(self, glossary_content):
        """Glossary should have a minimum number of rules."""
        rules = glossary_content.get("rules", [])
        min_rules = 2  # At least 2 rules for intelligent handling
        assert len(rules) >= min_rules, f"Glossary should have at least {min_rules} rules, has {len(rules)}"


class TestGlossaryDomainRelevance:
    """Tests for domain-specific term coverage."""

    def test_has_codexspec_specific_terms(self, glossary_content):
        """Glossary should include CodexSpec-specific terms."""
        translations = glossary_content.get("translations", {})
        expected_terms = ["Specification", "Task", "Workflow"]

        for term in expected_terms:
            assert term in translations, f"CodexSpec-specific term '{term}' should be in translations"

    def test_keep_english_includes_tool_names(self, glossary_content):
        """keep_english should include tool and platform names."""
        keep_english = glossary_content.get("keep_english", [])
        tool_patterns = ["GitHub", "pytest", "uv"]

        for pattern in tool_patterns:
            assert pattern in keep_english, f"Tool name '{pattern}' should be in keep_english"
