"""
CodexSpec Internationalization (i18n) Support.

This module provides language configuration utilities for the LLM-based
dynamic translation approach. Instead of maintaining multiple template
translations, we configure the output language and let Claude translate
at runtime.
"""

import os
import re
from pathlib import Path
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


# Lazy-loaded list of all supported languages (en + pre-translated)
_ALL_LANGUAGES_CACHE: list[str] | None = None


def get_all_supported_languages() -> list[tuple[str, str]]:
    """
    获取所有支持的语言列表（包括 en 和预翻译语言）。

    Returns:
        List of (code, name) tuples，en 排在首位，随后是预翻译语言
    """
    global _ALL_LANGUAGES_CACHE

    if _ALL_LANGUAGES_CACHE is None:
        # Lazy import to avoid circular dependency with translator.py
        from codexspec.translator import SUPPORTED_LANGUAGES

        _ALL_LANGUAGES_CACHE = ["en"] + list(SUPPORTED_LANGUAGES)

    return [(code, get_language_name(code)) for code in _ALL_LANGUAGES_CACHE]


# Default config.yml template
CONFIG_TEMPLATE = """# CodexSpec Configuration
# This file configures project-level settings for CodexSpec

version: "1.0"

# Language settings for internationalization (i18n)
language:
  # Interaction language - language for conversing with the user (LLM dialogue
  # and codexspec CLI terminal output). Supports any Claude-supported language.
  # Common values: en, zh-CN, zh-TW, ja, ko, es, fr, de, pt, ru
  interaction: "{language}"

  # Document language - language for generated artifact files
  # (requirements/spec/plan/tasks). Set this differently from interaction to
  # keep documents in one language while conversing in another.
  document: "{language}"

  # Output language (legacy) - fallback used when interaction/document are not
  # set. Kept for backward compatibility; prefer setting interaction/document.
  output: "{language}"

  # Commit message language - language for git commit messages
  # Defaults to output language if not specified
  # Set to "en" for English commit messages regardless of output language
  commit: "{language}"

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


def _read_language_key(content: str, key: str) -> Optional[str]:
    """Read a `key: value` language setting from config content (YAML-like regex).

    Returns the raw value (quotes stripped) or None if the key is absent.
    """
    match = re.search(rf"^\s*{re.escape(key)}:\s*['\"]?(\S+?)['\"]?\s*$", content, re.MULTILINE)
    return match.group(1) if match else None


def _resolve_language(config_file: Path, primary_key: str) -> str:
    """Resolve a language setting: primary_key -> output (legacy) -> 'en'.

    Args:
        config_file: Path to the project's config.yml.
        primary_key: The primary language key to try first ('interaction' or 'document').

    Returns:
        The normalized language code, defaulting to 'en'.
    """
    if not config_file.exists():
        return "en"
    try:
        content = config_file.read_text(encoding="utf-8")
        for key in (primary_key, "output"):
            value = _read_language_key(content, key)
            if value:
                return normalize_locale(value) or "en"
    except (OSError, re.error):
        pass
    return "en"


def _default_config_path() -> Path:
    return Path.cwd() / ".codexspec" / "config.yml"


def get_interaction_language(config_file: Optional[Path] = None) -> str:
    """Resolve the interaction language (user<->LLM conversation and CLI terminal).

    Resolution order: explicit `language.interaction` -> `language.output`
    (legacy) -> 'en'. Existing configs that only set `output` behave exactly as
    before.

    Args:
        config_file: Optional explicit path to config.yml; defaults to
            `.codexspec/config.yml` in the current working directory.

    Returns:
        The normalized interaction language code.
    """
    return _resolve_language(config_file or _default_config_path(), "interaction")


def get_document_language(config_file: Optional[Path] = None) -> str:
    """Resolve the document language (generated artifact files).

    Resolution order: explicit `language.document` -> `language.output`
    (legacy) -> 'en'. Existing configs that only set `output` behave exactly as
    before.

    Args:
        config_file: Optional explicit path to config.yml; defaults to
            `.codexspec/config.yml` in the current working directory.

    Returns:
        The normalized document language code.
    """
    return _resolve_language(config_file or _default_config_path(), "document")


def get_project_language(config_file: Optional[Path] = None) -> str:
    """Get the project language from .codexspec/config.yml.

    Backward-compatibility alias for the interaction language. Historically this
    returned the `output` language; it now resolves the interaction language,
    which falls back to `output` then `en` — so output-only configs are
    unaffected. Prefer :func:`get_interaction_language` / :func:`get_document_language`
    for new code.

    Returns:
        The configured language code, or "en" if not configured or file doesn't exist.
    """
    return get_interaction_language(config_file)


def get_commit_language(config_file: Path) -> Optional[str]:
    """Get the commit language from a config.yml file.

    Args:
        config_file: Path to the config.yml file

    Returns:
        The commit language code, or None if not found or file doesn't exist
    """
    import re

    if not config_file.exists():
        return None

    try:
        content = config_file.read_text(encoding="utf-8")
        # Parse the commit language setting from YAML-like format
        match = re.search(r"^\s*commit:\s*['\"]?(\S+?)['\"]?\s*$", content, re.MULTILINE)
        if match:
            return normalize_locale(match.group(1))
    except (OSError, re.error):
        pass

    return None


def update_language_field(config_file: Path, key: str, language: str) -> bool:
    """Update a single ``language.<key>`` setting in config.yml.

    Updates the value in place when ``key`` already exists; otherwise inserts
    ``<indent>{key}: "{language}"`` immediately after the ``language:`` line.
    The value is normalized via :func:`normalize_locale`.

    Args:
        config_file: Path to the project's config.yml.
        key: Language sub-key to set (e.g. "interaction", "document").
        language: New language code (will be normalized).

    Returns:
        True if updated or inserted; False if there is no ``language:`` section
        to insert into or the file cannot be written.
    """
    normalized = normalize_locale(language)
    try:
        content = config_file.read_text(encoding="utf-8")
        pattern = rf'^(\s*{re.escape(key)}:\s*)["\']?\S+?["\']?\s*$'
        new_content, count = re.subn(pattern, rf'\g<1>"{normalized}"', content, flags=re.MULTILINE)
        if count:
            config_file.write_text(new_content, encoding="utf-8")
            return True

        # Key absent: insert under the `language:` section.
        lang_match = re.search(r"^(\s*)language:\s*$", content, re.MULTILINE)
        if not lang_match:
            return False
        indent = lang_match.group(1) + "  "
        insert_line = f'{indent}{key}: "{normalized}"'
        end = lang_match.end()
        config_file.write_text(content[:end] + "\n" + insert_line + content[end:], encoding="utf-8")
        return True
    except (OSError, re.error):
        return False


def update_output_language(config_file: Path, language: str) -> bool:
    """Update only the output language setting in config.yml.

    Args:
        config_file: Path to the config.yml file
        language: New language code to set

    Returns:
        True if update was successful, False otherwise
    """
    import re

    normalized_lang = normalize_locale(language)

    try:
        content = config_file.read_text(encoding="utf-8")

        # Update output language only
        content = re.sub(
            r'^(\s*output:\s*)["\']?\S+?["\']?\s*$',
            rf'\g<1>"{normalized_lang}"',
            content,
            flags=re.MULTILINE,
        )

        config_file.write_text(content, encoding="utf-8")
        return True
    except (OSError, re.error):
        return False


def update_config_language(config_file: Path, language: str) -> bool:
    """Update the language setting in an existing config.yml file.

    Args:
        config_file: Path to the config.yml file
        language: New language code to set

    Returns:
        True if update was successful, False otherwise
    """
    import re

    normalized_lang = normalize_locale(language)

    try:
        content = config_file.read_text(encoding="utf-8")

        # Update output language
        content = re.sub(
            r'^(\s*output:\s*)["\']?\S+?["\']?\s*$',
            rf'\g<1>"{normalized_lang}"',
            content,
            flags=re.MULTILINE,
        )

        # Update commit language (defaults to output language)
        content = re.sub(
            r'^(\s*commit:\s*)["\']?\S+?["\']?\s*$',
            rf'\g<1>"{normalized_lang}"',
            content,
            flags=re.MULTILINE,
        )

        config_file.write_text(content, encoding="utf-8")
        return True
    except (OSError, re.error):
        return False
