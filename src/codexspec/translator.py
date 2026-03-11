"""Frontmatter translation module for CodexSpec.

This module provides translation capabilities for slash command template
frontmatter fields (description, argument-hint).
"""

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# Supported languages with pre-translated cache
SUPPORTED_LANGUAGES = ["zh-CN", "ja", "ko", "es", "fr", "de", "pt-BR"]


def get_translations_dir() -> Path:
    """Get the translations directory path.

    Returns:
        Path to templates/translations directory
    """
    # Path 1: Wheel install - templates packaged inside codexspec package
    # __file__ = site-packages/codexspec/translator.py
    # parent / "templates" / "translations" = site-packages/codexspec/templates/translations
    installed_translations = Path(__file__).parent / "templates" / "translations"
    if installed_translations.exists():
        return installed_translations

    # Path 2: Development/editable install - templates in project root
    dev_translations = Path(__file__).parent.parent.parent / "templates" / "translations"
    if dev_translations.exists():
        return dev_translations

    # Path 3: Fallback - return the installed path (for error messages)
    return installed_translations


def get_translation_cache_path(language: str) -> Path:
    """Get the translation cache file path for a language.

    Args:
        language: Target language code (e.g., "zh-CN")

    Returns:
        Path to the translation cache JSON file
    """
    return get_translations_dir() / f"{language}.json"


def load_translation_cache(language: str, translations_dir: Optional[Path] = None) -> Optional[dict]:
    """Load translation cache for a language.

    Args:
        language: Target language code
        translations_dir: Custom translations directory (for testing)

    Returns:
        Translation dictionary or None if cache doesn't exist
    """
    if translations_dir:
        cache_path = translations_dir / f"{language}.json"
    else:
        cache_path = get_translation_cache_path(language)

    if not cache_path.exists():
        return None

    try:
        return json.loads(cache_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def extract_frontmatter_fields(content: str) -> dict[str, Optional[str]]:
    """Extract description and argument-hint from YAML frontmatter.

    Args:
        content: Full template file content

    Returns:
        Dictionary with 'description' and 'argument-hint' keys
    """
    # Match YAML frontmatter
    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        return {"description": None, "argument-hint": None}

    frontmatter = frontmatter_match.group(1)
    result = {"description": None, "argument-hint": None}

    # Extract description (single line)
    desc_match = re.search(r"^description:\s*(.+)$", frontmatter, re.MULTILINE)
    if desc_match:
        result["description"] = desc_match.group(1).strip()

    # Extract argument-hint (can be multiline with |)
    # First try multiline format with |
    hint_match = re.search(r"^argument-hint:\s*\|\s*\n((?:  .+\n?)+)", frontmatter, re.MULTILINE)
    if hint_match:
        # Remove leading indentation from multiline strings
        hint_content = hint_match.group(1)
        lines = hint_content.rstrip("\n").split("\n")
        # Remove the 2-space indentation
        lines = [line[2:] if line.startswith("  ") else line for line in lines]
        result["argument-hint"] = "\n".join(lines).strip()
    else:
        # Try single-line argument-hint (with or without quotes)
        hint_match = re.search(r'^argument-hint:\s*"([^"]+)"', frontmatter, re.MULTILINE)
        if hint_match:
            result["argument-hint"] = hint_match.group(1).strip()
        else:
            # Try unquoted single-line
            hint_match = re.search(r"^argument-hint:\s*([^\n]+)", frontmatter, re.MULTILINE)
            if hint_match:
                result["argument-hint"] = hint_match.group(1).strip()

    return result


def apply_translations_to_template(content: str, translations: dict) -> str:
    """Apply translations to template frontmatter.

    Args:
        content: Original template content
        translations: Dictionary with translated values

    Returns:
        Template content with translated frontmatter
    """
    # Replace description
    if "description" in translations:
        content = re.sub(r"^(description:\s*).+$", rf"\g<1>{translations['description']}", content, flags=re.MULTILINE)

    # Replace argument-hint (handle both single-line and multiline)
    if "argument-hint" in translations:
        new_hint = translations["argument-hint"]
        # Check if original hint is multiline (uses |)
        if re.search(r"^argument-hint:\s*\|", content, re.MULTILINE):
            # Build new multiline content with proper indentation
            hint_lines = new_hint.split("\n")
            indented_hint = "\n  ".join(hint_lines)
            # Replace multiline hint - match the entire multiline block
            content = re.sub(
                r"(argument-hint:\s*\|)\s*\n((?:  .+\n?)+)", rf"\g<1>\n  {indented_hint}\n", content, flags=re.MULTILINE
            )
        else:
            # Replace single-line hint (with or without quotes)
            if re.search(r'^argument-hint:\s*"', content, re.MULTILINE):
                content = re.sub(r'^(argument-hint:\s*)"[^"]+"$', rf'\g<1>"{new_hint}"', content, flags=re.MULTILINE)
            else:
                content = re.sub(r"^(argument-hint:\s*).+$", rf"\g<1>{new_hint}", content, flags=re.MULTILINE)

    return content


def check_claude_cli_available() -> bool:
    """Check if Claude CLI is available.

    Returns:
        True if claude command is available
    """
    return shutil.which("claude") is not None


def translate_with_claude_cli(
    texts: dict[str, dict[str, str]], target_lang: str, timeout: int = 60
) -> Optional[dict[str, dict[str, str]]]:
    """Translate texts using Claude CLI.

    Args:
        texts: Dictionary of {command_name: {field: text}}
        target_lang: Target language code
        timeout: Timeout in seconds

    Returns:
        Translated dictionary or None on failure
    """
    if not check_claude_cli_available():
        return None

    # Build prompt
    input_json = json.dumps(texts, ensure_ascii=False, indent=2)
    prompt = f"""Translate the following JSON values to {target_lang}.
Keep all keys unchanged. Return only valid JSON with the same structure.
Do not translate technical terms like "spec.md", "plan.md", "TDD", etc.

{input_json}"""

    try:
        result = subprocess.run(["claude", "--print", prompt], capture_output=True, text=True, timeout=timeout)

        if result.returncode != 0:
            return None

        # Parse JSON from output
        output = result.stdout.strip()
        # Remove potential markdown code blocks
        if output.startswith("```"):
            output = re.sub(r"^```(?:json)?\n?", "", output)
            output = re.sub(r"\n?```$", "", output)

        return json.loads(output)

    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        return None


def translate_template_frontmatter(
    template_content: str, template_name: str, target_lang: str, cache: Optional[dict] = None
) -> str:
    """Translate template frontmatter fields.

    Args:
        template_content: Original template content
        template_name: Template name without extension (e.g., "constitution")
        target_lang: Target language code
        cache: Pre-loaded translation cache (optional)

    Returns:
        Template content with translated frontmatter (or original if translation fails)
    """
    # Skip translation for English
    if target_lang == "en":
        return template_content

    # Load cache if not provided
    if cache is None:
        cache = load_translation_cache(target_lang)

    # Try to use cache
    if cache and template_name in cache:
        return apply_translations_to_template(template_content, cache[template_name])

    # For non-cached languages, try dynamic translation
    if target_lang not in SUPPORTED_LANGUAGES:
        fields = extract_frontmatter_fields(template_content)
        if fields.get("description") or fields.get("argument-hint"):
            translations = translate_with_claude_cli({template_name: fields}, target_lang)
            if translations and template_name in translations:
                return apply_translations_to_template(template_content, translations[template_name])

    # Return original if all translation attempts fail
    return template_content
