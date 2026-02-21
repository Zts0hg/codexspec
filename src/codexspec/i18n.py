"""
CodexSpec Internationalization (i18n) Support.

This module provides language configuration utilities for the LLM-based
dynamic translation approach. Instead of maintaining multiple template
translations, we configure the output language and let Claude translate
at runtime.
"""

import os
from typing import Optional

# Supported language codes with their normalized forms
# Format: (primary_code, aliases)
LANGUAGE_ALIASES = {
    "en": ("en", ["en", "en-US", "en-GB", "english"]),
    "zh-CN": ("zh-CN", ["zh", "zh-cn", "zh-Hans", "chinese", "chinese-simplified"]),
    "zh-TW": ("zh-TW", ["zh-tw", "zh-Hant", "chinese-traditional"]),
    "ja": ("ja", ["ja", "jp", "japanese"]),
    "ko": ("ko", ["ko", "kr", "korean"]),
    "es": ("es", ["es", "spa", "spanish"]),
    "fr": ("fr", ["fr", "fra", "french"]),
    "de": ("de", ["de", "deu", "german"]),
    "pt": ("pt", ["pt", "por", "portuguese"]),
    "ru": ("ru", ["ru", "rus", "russian"]),
    "it": ("it", ["it", "ita", "italian"]),
    "ar": ("ar", ["ar", "ara", "arabic"]),
    "hi": ("hi", ["hi", "hin", "hindi"]),
}

# Build reverse lookup: alias -> primary code
_ALIAS_TO_PRIMARY = {}
for primary, (_, aliases) in LANGUAGE_ALIASES.items():
    for alias in aliases:
        _ALIAS_TO_PRIMARY[alias.lower()] = primary


def normalize_locale(lang_code: Optional[str]) -> str:
    """
    Normalize a language code to its canonical form.

    Args:
        lang_code: A language code (e.g., "zh", "zh-CN", "en-US")

    Returns:
        The normalized language code (e.g., "zh-CN", "en")

    Examples:
        >>> normalize_locale("zh")
        'zh-CN'
        >>> normalize_locale("ZH-CN")
        'zh-CN'
        >>> normalize_locale("english")
        'en'
        >>> normalize_locale(None)
        'en'
    """
    if not lang_code:
        return "en"

    # Normalize to lowercase for lookup
    normalized = lang_code.strip().lower()

    # Check if it's a known alias
    if normalized in _ALIAS_TO_PRIMARY:
        return _ALIAS_TO_PRIMARY[normalized]

    # If not found, return as-is (may be a custom/unsupported locale)
    # Preserve original casing convention (xx-XX)
    parts = lang_code.split("-")
    if len(parts) == 2:
        return f"{parts[0].lower()}-{parts[1].upper()}"
    return lang_code.lower()


def get_language_from_env() -> Optional[str]:
    """
    Get language preference from environment variables.

    Checks the following environment variables in order:
    1. CODEXSPEC_LANG - CodexSpec-specific language setting
    2. LANG - Standard Unix locale (extracts language part)

    Returns:
        Normalized language code or None if not set

    Examples:
        >>> import os
        >>> os.environ["CODEXSPEC_LANG"] = "zh-CN"
        >>> get_language_from_env()
        'zh-CN'
    """
    # Check CodexSpec-specific env var first
    codexspec_lang = os.environ.get("CODEXSPEC_LANG")
    if codexspec_lang:
        return normalize_locale(codexspec_lang)

    # Check standard LANG environment variable
    lang = os.environ.get("LANG", "")
    if lang:
        # LANG format is typically "en_US.UTF-8" or "zh_CN.UTF-8"
        # Extract the locale part before the encoding
        locale_part = lang.split(".")[0]
        # Convert from en_US to en-US format
        if "_" in locale_part:
            parts = locale_part.split("_")
            # Normalize (e.g., en_US -> en-US)
            return normalize_locale(f"{parts[0]}-{parts[1]}")

    return None


def is_supported_language(lang_code: str) -> bool:
    """
    Check if a language code is supported.

    Args:
        lang_code: Language code to check

    Returns:
        True if the language is supported, False otherwise
    """
    normalized = normalize_locale(lang_code)
    return normalized in LANGUAGE_ALIASES


def get_language_name(lang_code: str) -> str:
    """
    Get the human-readable name for a language code.

    Args:
        lang_code: Language code

    Returns:
        Human-readable language name
    """
    language_names = {
        "en": "English",
        "zh-CN": "Chinese (Simplified)",
        "zh-TW": "Chinese (Traditional)",
        "ja": "Japanese",
        "ko": "Korean",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "pt": "Portuguese",
        "ru": "Russian",
        "it": "Italian",
        "ar": "Arabic",
        "hi": "Hindi",
    }
    normalized = normalize_locale(lang_code)
    return language_names.get(normalized, normalized)


def get_supported_languages() -> list[tuple[str, str]]:
    """
    Get list of supported languages.

    Returns:
        List of (code, name) tuples for all supported languages
    """
    return [(code, get_language_name(code)) for code in LANGUAGE_ALIASES.keys()]


# Default config.yml template
CONFIG_TEMPLATE = """# CodexSpec Configuration
# This file configures project-level settings for CodexSpec

version: "1.0"

# Language settings for internationalization (i18n)
language:
  # Output language - Claude will use this language for interactions
  # and generated documents. Supports any Claude-supported language.
  # Common values: en, zh-CN, zh-TW, ja, ko, es, fr, de, pt, ru
  output: "{language}"

  # Template language - keep as "en" for best compatibility
  # All command templates are in English and translated dynamically
  templates: "en"

# Project metadata
project:
  ai: "claude"
  created: "{created}"
"""


def generate_config_content(language: str = "en", created: str = None) -> str:
    """
    Generate config.yml content.

    Args:
        language: Output language code (will be normalized)
        created: Creation date string (defaults to today)

    Returns:
        Config file content as string
    """
    from datetime import datetime

    normalized_lang = normalize_locale(language)
    if created is None:
        created = datetime.now().strftime("%Y-%m-%d")

    return CONFIG_TEMPLATE.format(language=normalized_lang, created=created)
