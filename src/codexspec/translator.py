"""Frontmatter translation module for CodexSpec.

This module provides translation capabilities for slash command template
frontmatter fields (description, argument-hint).
"""

import json
import logging
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from codexspec.i18n import normalize_locale

logger = logging.getLogger(__name__)

# Supported languages with pre-translated cache
SUPPORTED_LANGUAGES = ["zh-CN", "ja", "ko", "es", "fr", "de", "pt-BR"]

# English baseline CLI messages (fallback when translation file is missing)
_CLI_MESSAGES_EN = {
    "init": {
        # Migration messages
        "migration_found": "Found {count} old structure command files",
        "migration_old_structure": "Old structure: .claude/commands/codexspec.*.md",
        "migration_new_structure": "New structure: .claude/commands/codexspec/*.md",
        "migration_confirm": "Migrate to new structure?",
        "migration_complete": "✓ Migration complete",
        "migration_failed": "✗ Migration failed",
        "migration_skipped": "Skipped migration",
        # Update messages
        "update_confirm": "Overwrite and update command templates?",
        "commands_updated": "✓ Updated {count} commands",
        "commands_installed": "✓ Installed {count} commands to .claude/commands/{path}/",
        "commands_installed_short": "✓ Installed {count} commands",
        # File operation messages
        "created_directory": "Created directory: {path}",
        "copied_script": "Copied script: {name}",
        "copied_template": "Copied template: {name}",
        "created_file": "Created: {file}",
        "updated_file": "Updated: {file} ({detail})",
        "git_initialized": "Initialized: Git repository",
        "git_failed": "Warning: Failed to initialize git repository",
        "warning_scripts_not_found": "Warning: Scripts directory not found",
        "warning_bash_scripts_not_found": "Warning: Bash scripts directory not found",
        "warning_powershell_scripts_not_found": "Warning: PowerShell scripts directory not found",
        "warning_docs_templates_not_found": "Warning: Docs templates directory not found",
        "warning_templates_not_found": "Warning: Templates directory not found, creating default commands",
        "installed_command": "Installed command: /codexspec.{name}",
        # Command summary
        "commands_summary": "📁 Installed {count} commands to .claude/commands/{path}/",
        "category_core": "Core Commands ({count})",
        "category_enhanced": "Enhanced Commands ({count})",
        "category_git": "Git Workflow ({count})",
        # Success panel
        "success_title": "Success",
        "success_message": "CodexSpec project initialized successfully!",
        "success_project_dir": "Project directory: {path}",
        "next_steps": "Next steps:",
        "next_step_navigate": "Navigate to your project: cd {path}",
        "next_step_start_claude": "Start Claude Code: claude",
        "next_step_constitution": "Use /codexspec.constitution to establish project principles",
        "next_step_specify": "Use /codexspec.specify to create your first specification",
        # Tips
        "tips_header": "💡 Tips:",
        "tips_git": "Add .claude/ to Git: git add .claude/",
        "tips_list_commands": "Run codexspec list-commands to see all available commands",
        "tips_edit": "Edit .md files directly to customize command behavior",
        # Important reminder
        "important_header": "Important:",
        "important_message": "The constitution is the foundation of your SDD workflow.",
        "important_action": "Run /codexspec.constitution to customize it for your project.",
        # Constitution compliance
        "compliance_confirm": (
            "CLAUDE.md already exists without Constitution Compliance section.\n"
            "The Constitution Compliance section ensures Claude follows your project's constitution.\n"
            "? Would you like to add the Constitution Compliance section?"
        ),
        "compliance_added": "Updated: CLAUDE.md (added Constitution Compliance section)",
        # Errors
        "error_dir_exists": "Error: Directory '{path}' already exists",
        "error_use_force": "Use --force to overwrite or choose a different name",
        "error_no_project_name": "Error: Please provide a project name or use --here flag",
    },
    "list_commands": {
        "header": "CodexSpec Available Commands ({count})",
        "table_header": "Command",
        "description_header": "Description",
        "category_core": "Core Commands ({count})",
        "category_enhanced": "Enhanced Commands ({count})",
        "category_git": "Git Workflow ({count})",
        "no_project": "No CodexSpec project found in current directory.",
        "run_init": "Run codexspec init to create a new project.",
        "usage_hint": "Use /codexspec.<command> to invoke these commands",
    },
    "set_language": {
        "language_set": "Language set to: {lang} ({name})",
        "language_failed": "Failed to update language setting",
        "language_warning": "Warning: '{lang}' is not in the list of commonly supported languages.",
        "language_warning_hint": (
            "It may still work if Claude supports it. Run codexspec config --list-langs to see supported languages."
        ),
        "commit_lang_set": "Commit message language set to: {lang}",
    },
}


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


def load_cli_translations(lang: str, translations_dir: Optional[Path] = None) -> dict:
    """Load CLI translations for a language.

    Args:
        lang: Target language code
        translations_dir: Custom translations directory (for testing)

    Returns:
        Dictionary of CLI messages. Falls back to code baseline
        _CLI_MESSAGES_EN if translation file doesn't exist or is corrupted.
    """
    # Normalize language code
    normalized_lang = normalize_locale(lang)

    # Fallback to code baseline for unknown languages
    if not normalized_lang:
        logger.warning(f"Using code baseline for {lang}")
        return _CLI_MESSAGES_EN

    # Resolve translations directory
    if translations_dir is None:
        translations_dir = get_translations_dir()

    # Check if translation file exists
    cache_path = translations_dir / f"{normalized_lang}.json"

    if not cache_path.exists():
        logger.warning(f"Using code baseline for {lang}")
        return _CLI_MESSAGES_EN

    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        # Extract CLI messages from the "cli" namespace
        if isinstance(data, dict) and "cli" in data:
            return data["cli"]
        # Fallback if structure is unexpected
        logger.warning(f"Translation file missing 'cli' key for {lang}, falling back to code baseline")
        return _CLI_MESSAGES_EN
    except (json.JSONDecodeError, OSError):
        logger.warning(f"Translation file corrupted for {lang}, falling back to code baseline")
        return _CLI_MESSAGES_EN


def translate(key: str, language: str = "en", **kwargs) -> str:
    """Translate a CLI message to the target language.

    Args:
        key: Message key in format "cli.{command}.{message_key}"
             e.g., "cli.init.migration_found"
        language: Target language code (default: "en")
        **kwargs: Format parameters for the message

    Returns:
        Translated and formatted message string

    Examples:
        >>> translate("cli.init.migration_found", "zh-CN", count=3)
        '发现 3 个旧结构命令文件'
        >>> translate("cli.init.migration_found", "en", count=3)
        'Found 3 old structure command files'
    """
    # Normalize language code
    normalized_lang = normalize_locale(language)

    # Load translations for the language
    translations = load_cli_translations(normalized_lang)

    # Extract message from translations dict
    # Key format: "cli.{command}.{message_key}"
    parts = key.split(".")
    if len(parts) < 3:
        return key

    # Navigate to nested key
    current = translations
    for part in parts[1:]:
        if part not in current:
            # Key not found, return the key itself
            return key
        current = current[part]

    # Get message template
    message_template = current

    # Format message with kwargs
    try:
        return message_template.format(**kwargs)
    except KeyError:
        # Missing parameter - return original template string
        logger.debug(f"Missing parameter in message template: {key}")
        return message_template


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
