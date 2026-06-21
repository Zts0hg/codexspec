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

# Language settings for internationalization (i18n).
# `output` is the base language. `interaction`, `document`, and `commit` override
# it when set; when absent they fall back to `output` (then "en"). Only the keys
# you choose are written, so a freshly initialized project is intentionally sparse.
language:
{language_lines}
  # Template language - keep as "en" for best compatibility
  # All command templates are in English and translated dynamically
  templates: "en"

# Project metadata
project:
  ai: "claude"
  created: "{created}"
"""


def generate_config_content(
    *,
    output: Optional[str] = None,
    interaction: Optional[str] = None,
    document: Optional[str] = None,
    commit: Optional[str] = None,
    created: Optional[str] = None,
) -> str:
    """Generate ``config.yml`` content, emitting only the specified language keys.

    Each provided key is normalized and written; omitted keys are intentionally
    not emitted (they resolve at read time via the ``output`` fallback). When no
    language key is specified at all, ``output`` defaults to ``"en"`` so the
    no-argument call still produces a valid base config.

    Args:
        output: Output (base) language code.
        interaction: Interaction language code.
        document: Document language code.
        commit: Commit message language code.
        created: Creation date string (defaults to today).

    Returns:
        Config file content as a string.
    """
    from datetime import datetime

    if created is None:
        created = datetime.now().strftime("%Y-%m-%d")

    keys: list[tuple[str, str]] = []
    if output is not None:
        keys.append(("output", normalize_locale(output)))
    if interaction is not None:
        keys.append(("interaction", normalize_locale(interaction)))
    if document is not None:
        keys.append(("document", normalize_locale(document)))
    if commit is not None:
        keys.append(("commit", normalize_locale(commit)))

    # No language specified at all: default the base to "en".
    if not keys:
        keys.append(("output", "en"))

    language_lines = "\n".join(f'  {key}: "{value}"' for key, value in keys)
    return CONFIG_TEMPLATE.format(language_lines=language_lines, created=created)


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


def get_explicit_language_key(config_file: Optional[Path], key: str) -> Optional[str]:
    """Return one explicitly configured ``language.<key>`` value, if present.

    This differs from the public language-resolution helpers because it never
    falls back to ``language.output`` or ``"en"``.
    """
    path = config_file or _default_config_path()
    if not path.exists():
        return None
    try:
        value = _read_language_key(path.read_text(encoding="utf-8"), key)
        if value:
            return normalize_locale(value) or None
    except (OSError, re.error):
        pass
    return None


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


def get_commit_language(config_file: Optional[Path] = None) -> str:
    """Resolve the commit language (git commit messages).

    Resolution order: explicit ``language.commit`` -> ``language.output``
    (legacy) -> ``"en"``. This aligns Python resolution with the fallback already
    documented in the ``commit-staged.md`` template and mirrors
    :func:`get_interaction_language` / :func:`get_document_language`, making
    ``output`` the true base for all four dimensions.

    Args:
        config_file: Optional explicit path to config.yml; defaults to
            ``.codexspec/config.yml`` in the current working directory.

    Returns:
        The normalized commit language code.
    """
    return _resolve_language(config_file or _default_config_path(), "commit")


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
