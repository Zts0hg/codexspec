#!/usr/bin/env python3
"""
CodexSpec - A Spec-Driven Development (SDD) toolkit for Claude Code.

This toolkit provides a structured approach to software development using
executable specifications that guide AI-assisted implementation.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from .commands.installer import (
    COMMANDS_SUBDIR,
    detect_old_structure,
    get_commands_metadata,
    get_installed_commands_metadata,
    install_commands_to_subdir,
    migrate_old_commands,
    should_update_commands,
)
from .i18n import (
    generate_config_content,
    get_commit_language,
    get_language_name,
    get_project_language,
    get_supported_languages,
    is_supported_language,
    normalize_locale,
    update_config_language,
    update_output_language,
)
from .translator import translate

# Version info
__version__ = "0.4.1"
__author__ = "CodexSpec Team"

# Constitution file path constants
CONSTITUTION_IMPORT_PATH = "@.codexspec/memory/constitution.md"
CONSTITUTION_FILE_PATH = ".codexspec/memory/constitution.md"
MARKDOWNLINT_DISABLE_MD041 = "<!-- markdownlint-disable MD041 -->\n"

app = typer.Typer(
    name="codexspec",
    help="CodexSpec - A Spec-Driven Development (SDD) toolkit for Claude Code",
    add_completion=False,
)
console = Console()


def get_version() -> str:
    """Return the current version of codexspec."""
    return __version__


def get_templates_dir() -> Path:
    """Get the templates directory path.

    This function handles multiple installation scenarios:
    1. Wheel install: templates are in codexspec/templates (same level as __init__.py)
    2. Development: templates are in project root (../templates from src/codexspec)
    3. Editable install: templates are in project root
    """
    # Path 1: Wheel install - templates packaged inside codexspec package
    # __file__ = site-packages/codexspec/__init__.py
    # parent / "templates" = site-packages/codexspec/templates
    installed_templates = Path(__file__).parent / "templates"
    if installed_templates.exists():
        return installed_templates

    # Path 2: Development/editable install - templates in project root
    # __file__ = .../src/codexspec/__init__.py
    # parent.parent.parent = .../ (project root)
    dev_templates = Path(__file__).parent.parent.parent / "templates"
    if dev_templates.exists():
        return dev_templates

    # Path 3: Fallback - return the installed path (will trigger warning if not exists)
    return installed_templates


def get_scripts_dir() -> Path:
    """Get the scripts directory path.

    Similar to get_templates_dir(), handles multiple installation scenarios:
    1. Wheel install: scripts are in codexspec/scripts (same level as __init__.py)
    2. Development: scripts are in project root (../scripts from src/codexspec)
    3. Editable install: scripts are in project root
    """
    # Path 1: Wheel install - scripts packaged inside codexspec package
    installed_scripts = Path(__file__).parent / "scripts"
    if installed_scripts.exists():
        return installed_scripts

    # Path 2: Development/editable install - scripts in project root
    dev_scripts = Path(__file__).parent.parent.parent / "scripts"
    if dev_scripts.exists():
        return dev_scripts

    # Path 3: Fallback - return the installed path (will trigger warning if not exists)
    return installed_scripts


def check_command_exists(command: str) -> bool:
    """Check if a command is available in PATH."""
    try:
        subprocess.run(
            ["which", command] if sys.platform != "win32" else ["where", command],
            capture_output=True,
            check=False,
        )
        return True
    except Exception:
        return False


@app.command()
def version() -> None:
    """Display version and system information."""
    console.print(
        Panel.fit(
            f"[bold blue]CodexSpec[/bold blue] version [green]{__version__}[/green]\n"
            f"Python: {sys.version.split()[0]}\n"
            f"Platform: {sys.platform}",
            title="Version Info",
        )
    )


@app.command()
def check() -> None:
    """Check for installed tools and dependencies."""
    table = Table(title="Tool Check")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Path", style="dim")

    tools = [
        ("git", "Git version control"),
        ("claude", "Claude Code CLI"),
        ("uv", "UV package manager"),
        ("python", "Python interpreter"),
    ]

    for cmd, desc in tools:
        exists = check_command_exists(cmd)
        status = "[green]Installed[/green]" if exists else "[red]Not Found[/red]"
        path = ""
        if exists:
            try:
                result = subprocess.run(
                    ["which", cmd] if sys.platform != "win32" else ["where", cmd],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                path = result.stdout.strip().split("\n")[0] if result.stdout else ""
            except Exception:
                path = "Unknown"
        table.add_row(f"{cmd} ({desc})", status, path)

    console.print(table)


@app.command()
def config(
    set_lang: Optional[str] = typer.Option(
        None,
        "--set-lang",
        "-l",
        help="Set the output language (e.g., en, zh-CN, ja)",
    ),
    set_commit_lang: Optional[str] = typer.Option(
        None,
        "--set-commit-lang",
        "-c",
        help="Set the commit message language (defaults to output language)",
    ),
    list_langs: bool = typer.Option(
        False,
        "--list-langs",
        help="List all supported languages",
    ),
) -> None:
    """
    View or modify CodexSpec project configuration.

    This command displays the current configuration or allows you to modify
    settings such as the output language for internationalization.

    Examples:
        codexspec config                       # Show current configuration
        codexspec config --set-lang zh-CN      # Set language to Chinese
        codexspec config --set-commit-lang en  # Set commit messages to English
        codexspec config --list-langs          # List supported languages
    """
    # Handle list languages
    if list_langs:
        table = Table(title="Supported Languages")
        table.add_column("Code", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="dim")

        for code, name in get_supported_languages():
            table.add_row(code, name, "Supported")
        console.print(table)
        return

    # Find config file
    config_file = Path.cwd() / ".codexspec" / "config.yml"

    if not config_file.exists():
        console.print("[yellow]No CodexSpec project found in current directory.[/yellow]")
        console.print("Run [cyan]codexspec init[/cyan] to create a new project.")
        raise typer.Exit(1)

    # Handle set language
    if set_lang:
        normalized = normalize_locale(set_lang)
        if not is_supported_language(normalized):
            console.print(f"[yellow]Warning: '{set_lang}' is not in the list of commonly supported languages.[/yellow]")
            console.print(
                "It may still work if Claude supports it. "
                "Run [cyan]codexspec config --list-langs[/cyan] to see supported languages."
            )

        # Read existing config
        config_content = config_file.read_text(encoding="utf-8")

        # Update language setting using simple string replacement
        lines = config_content.split("\n")
        new_lines = []
        in_language_section = False
        updated = False

        for line in lines:
            if line.strip().startswith("language:"):
                in_language_section = True
                new_lines.append(line)
            elif in_language_section and line.strip().startswith("output:"):
                # Update the output line
                indent = len(line) - len(line.lstrip())
                new_lines.append(" " * indent + f'output: "{normalized}"')
                updated = True
                in_language_section = False
            else:
                new_lines.append(line)

        if updated:
            config_file.write_text("\n".join(new_lines), encoding="utf-8")
            lang_name = get_language_name(normalized)
            console.print(f"[green]Language set to:[/green] {normalized} ({lang_name})")
        else:
            console.print("[red]Failed to update language setting[/red]")
            raise typer.Exit(1)
        return

    # Handle set commit language
    if set_commit_lang:
        normalized = normalize_locale(set_commit_lang)
        if not is_supported_language(normalized):
            console.print(
                f"[yellow]Warning: '{set_commit_lang}' is not in the list of commonly supported languages.[/yellow]"
            )
            console.print(
                "It may still work if Claude supports it. "
                "Run [cyan]codexspec config --list-langs[/cyan] to see supported languages."
            )

        # Read existing config
        config_content = config_file.read_text(encoding="utf-8")

        # Update or add commit language setting
        lines = config_content.split("\n")
        new_lines = []
        in_language_section = False
        found_commit = False
        output_indent = 2  # Default indent for language section

        for i, line in enumerate(lines):
            if line.strip().startswith("language:"):
                in_language_section = True
                new_lines.append(line)
            elif in_language_section and line.strip().startswith("output:"):
                output_indent = len(line) - len(line.lstrip())
                new_lines.append(line)
            elif in_language_section and line.strip().startswith("commit:"):
                # Update existing commit line
                indent = len(line) - len(line.lstrip())
                new_lines.append(" " * indent + f'commit: "{normalized}"')
                found_commit = True
                in_language_section = False
            elif in_language_section and (
                line.strip().startswith("templates:")
                or (not line.strip().startswith(" ") and line.strip() and not line.strip().startswith("#"))
            ):
                # We've reached templates or another section without finding commit
                # Insert commit before templates
                if not found_commit:
                    new_lines.append(" " * output_indent + f'commit: "{normalized}"')
                    found_commit = True
                new_lines.append(line)
                in_language_section = False
            else:
                new_lines.append(line)

        # If we never found a place to add commit, append it after output
        if not found_commit and in_language_section:
            new_lines.append(" " * output_indent + f'commit: "{normalized}"')

        config_file.write_text("\n".join(new_lines), encoding="utf-8")
        lang_name = get_language_name(normalized)
        console.print(f"[green]Commit message language set to:[/green] {normalized} ({lang_name})")
        return

    # Display current configuration
    console.print(
        Panel(
            config_file.read_text(encoding="utf-8"),
            title=f"Configuration: {config_file}",
            border_style="blue",
        )
    )


@app.command("list-commands")
def list_commands() -> None:
    """List all available CodexSpec slash commands.

    This command displays all available CodexSpec slash commands grouped by category,
    showing their display names and descriptions.
    """

    # Get user's language preference
    language = get_project_language()

    metadata = get_installed_commands_metadata()

    # Group by category
    categories: dict[str, list] = {
        "core": [],
        "enhanced": [],
        "git": [],
        "review": [],
        "utility": [],
    }
    for cmd in metadata:
        cat = cmd["category"]
        if cat in categories:
            categories[cat].append(cmd)

    console.print()
    console.print(f"[bold]{translate('cli.list_commands.header', language, count=len(metadata))}[/bold]")
    console.print()

    for cat, commands in categories.items():
        if commands:
            cat_msg = translate(f"cli.list_commands.category_{cat}", language, count=len(commands))
            console.print(f"[bold cyan]{cat_msg}[/bold cyan]")
            for cmd in commands:
                console.print(f"  {cmd['display_name']:<30} [dim]{cmd['description']}[/dim]")
            console.print()

    console.print(f"[dim]{translate('cli.list_commands.usage_hint', language)}[/dim]")


@app.command()
def init(
    project_name: Optional[str] = typer.Argument(
        None,
        help="Name for your new project directory (use '.' or --here for current directory)",
    ),
    here: bool = typer.Option(
        False,
        "--here",
        "-h",
        help="Initialize project in the current directory",
    ),
    ai: str = typer.Option(
        "claude",
        "--ai",
        "-a",
        help="AI assistant to use (default: claude)",
    ),
    lang: Optional[str] = typer.Option(
        None,
        "--lang",
        "-l",
        help="Output language (e.g., en, zh-CN, ja). Interactive prompt if not specified in TTY.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force merge/overwrite when initializing in current directory",
    ),
    no_git: bool = typer.Option(
        False,
        "--no-git",
        help="Skip git repository initialization",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable detailed debug output",
    ),
) -> None:
    """
    Initialize a new CodexSpec project.

    This command sets up the directory structure and installs the necessary
    slash commands for Claude Code to use the CodexSpec workflow.

    Examples:
        codexspec init my-project
        codexspec init my-project --ai claude
        codexspec init my-project --lang zh-CN
        codexspec init . --ai claude
        codexspec init --here --ai claude
        codexspec init . --force --ai claude
    """
    # Handle interactive language selection when --lang not specified
    if lang is None:
        if sys.stdin.isatty():
            # TTY environment: show interactive prompt
            try:
                lang = prompt_language_selection()
            except KeyboardInterrupt:
                console.print()
                console.print("[yellow]Selection cancelled, using default language (en)[/yellow]")
                lang = "en"
        else:
            # Non-TTY environment: use default
            lang = "en"

    # Normalize language code early for use throughout the function
    normalized_lang = normalize_locale(lang)

    # Determine target directory
    if here or project_name == ".":
        target_dir = Path.cwd()
    elif project_name:
        target_dir = Path.cwd() / project_name
    else:
        console.print(f"[red]{translate('cli.init.error_no_project_name', normalized_lang)}[/red]")
        raise typer.Exit(1)

    if debug:
        console.print(f"[dim]Target directory: {target_dir}[/dim]")
        console.print(f"[dim]AI assistant: {ai}[/dim]")
        console.print(f"[dim]Language: {lang} (normalized: {normalized_lang})[/dim]")

    # Check if directory exists and handle accordingly
    if target_dir.exists() and not here and project_name != ".":
        if not force:
            console.print(f"[red]{translate('cli.init.error_dir_exists', normalized_lang, path=target_dir)}[/red]")
            console.print(translate("cli.init.error_use_force", normalized_lang))
            raise typer.Exit(1)

    # Create directory if needed
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        console.print(f"[green]Created directory:[/green] {target_dir}")

    # Create .codexspec directory structure
    codexspec_dir = target_dir / ".codexspec"
    codexspec_dir.mkdir(exist_ok=True)

    # Create subdirectories
    (codexspec_dir / "memory").mkdir(exist_ok=True)
    (codexspec_dir / "specs").mkdir(exist_ok=True)
    (codexspec_dir / "templates").mkdir(exist_ok=True)
    (codexspec_dir / "templates" / "docs").mkdir(exist_ok=True)
    (codexspec_dir / "scripts").mkdir(exist_ok=True)

    # Copy helper scripts based on platform
    scripts_source_dir = get_scripts_dir()
    if scripts_source_dir.exists():
        if sys.platform == "win32":
            # Windows: copy PowerShell scripts
            ps_scripts = scripts_source_dir / "powershell"
            if ps_scripts.exists():
                for script_file in ps_scripts.glob("*.ps1"):
                    dest_file = codexspec_dir / "scripts" / script_file.name
                    dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
                    console.print(f"[green]Copied script:[/green] {script_file.name}")
            else:
                console.print("[yellow]Warning: PowerShell scripts directory not found[/yellow]")
        else:
            # macOS/Linux: copy Bash scripts
            bash_scripts = scripts_source_dir / "bash"
            if bash_scripts.exists():
                for script_file in bash_scripts.glob("*.sh"):
                    dest_file = codexspec_dir / "scripts" / script_file.name
                    dest_file.write_text(script_file.read_text(encoding="utf-8"), encoding="utf-8")
                    console.print(f"[green]Copied script:[/green] {script_file.name}")
            else:
                console.print("[yellow]Warning: Bash scripts directory not found[/yellow]")
    else:
        console.print("[yellow]Warning: Scripts directory not found[/yellow]")

    # Copy docs templates
    docs_templates_dir = get_templates_dir() / "docs"
    if docs_templates_dir.exists():
        for template_file in docs_templates_dir.glob("*.md"):
            dest_file = codexspec_dir / "templates" / "docs" / template_file.name
            dest_file.write_text(template_file.read_text(encoding="utf-8"), encoding="utf-8")
            console.print(f"[green]Copied template:[/green] {template_file.name}")
    else:
        console.print("[yellow]Warning: Docs templates directory not found[/yellow]")

    # Create .claude/commands directory for slash commands
    claude_dir = target_dir / ".claude"
    claude_commands_dir = claude_dir / "commands"
    claude_commands_dir.mkdir(parents=True, exist_ok=True)

    # Target subdirectory for CodexSpec commands
    codexspec_commands_dir = claude_commands_dir / COMMANDS_SUBDIR

    # Get templates directory
    templates_dir = get_templates_dir() / "commands"

    # Check for old structure and migrate if needed
    old_files = detect_old_structure(claude_dir)
    migration_happened = False
    if old_files:
        console.print()
        console.print(
            f"[yellow]{translate('cli.init.migration_found', normalized_lang, count=len(old_files))}[/yellow]"
        )
        console.print(f"[dim]{translate('cli.init.migration_old_structure', normalized_lang)}[/dim]")
        console.print(f"[dim]{translate('cli.init.migration_new_structure', normalized_lang)}[/dim]")

        if Confirm.ask(translate("cli.init.migration_confirm", normalized_lang), default=True):
            if migrate_old_commands(claude_dir, old_files):
                console.print(f"[green]{translate('cli.init.migration_complete', normalized_lang)}[/green]")
                migration_happened = True
            else:
                console.print(f"[red]{translate('cli.init.migration_failed', normalized_lang)}[/red]")
        else:
            console.print(f"[dim]{translate('cli.init.migration_skipped', normalized_lang)}[/dim]")

    # Install or update commands (translate after migration if user wants)
    if migration_happened:
        # Migration moved files, ask if user wants to update/translate them
        if Confirm.ask(translate("cli.init.update_confirm", normalized_lang), default=True):
            count = install_commands_to_subdir(
                codexspec_commands_dir, templates_dir, force=True, language=normalized_lang
            )
            console.print(f"[green]{translate('cli.init.commands_updated', normalized_lang, count=count)}[/green]")
    elif should_update_commands(codexspec_dir):
        console.print()
        if Confirm.ask(translate("cli.init.update_confirm", normalized_lang), default=True):
            count = install_commands_to_subdir(
                codexspec_commands_dir, templates_dir, force=True, language=normalized_lang
            )
            console.print(f"[green]{translate('cli.init.commands_updated', normalized_lang, count=count)}[/green]")
    else:
        if not templates_dir.exists():
            # Templates directory is part of the wheel; if it's missing the
            # install is broken and we cannot recover.
            console.print(
                f"[red]{translate('cli.init.error_templates_missing', normalized_lang, path=str(templates_dir))}[/red]"
            )
            raise typer.Exit(1)

        count = install_commands_to_subdir(codexspec_commands_dir, templates_dir, language=normalized_lang)
        cmd_path = f".claude/commands/{COMMANDS_SUBDIR}/"
        msg = translate("cli.init.commands_installed", normalized_lang, count=count, path=cmd_path)
        console.print(f"[green]{msg}[/green]")

    # Create constitution template
    constitution_file = codexspec_dir / "memory" / "constitution.md"
    if not constitution_file.exists():
        constitution_file.write_text(_get_default_constitution(), encoding="utf-8")
        msg = translate("cli.init.created_file", normalized_lang, file=".codexspec/memory/constitution.md")
        console.print(f"[green]{msg}[/green]")

    # Create config.yml with language settings
    config_file = codexspec_dir / "config.yml"
    if not config_file.exists() or force:
        config_content = generate_config_content(
            language=normalized_lang,
            created=datetime.now().strftime("%Y-%m-%d"),
        )
        config_file.write_text(config_content, encoding="utf-8")
        lang_name = get_language_name(normalized_lang)
        msg = translate(
            "cli.init.created_file",
            normalized_lang,
            file=f".codexspec/config.yml (language: {lang_name})",
        )
        console.print(f"[green]{msg}[/green]")
    elif lang != "en":  # User explicitly provided --lang (not default)
        # Check if commit language differs from selected language
        current_commit_lang = get_commit_language(config_file)
        if current_commit_lang and current_commit_lang != normalized_lang:
            # Prompt user to update commit language
            msg = translate(
                "cli.init.commit_lang_differs",
                normalized_lang,
                current=current_commit_lang,
                selected=normalized_lang,
            )
            if Confirm.ask(msg, default=True):
                update_config_language(config_file, normalized_lang)
                console.print(
                    f"[green]{translate('cli.init.commit_lang_updated', normalized_lang, lang=normalized_lang)}[/green]"
                )
            else:
                # Update only output language, keep commit language
                update_output_language(config_file, normalized_lang)
                console.print(
                    f"[dim]{translate('cli.init.commit_lang_kept', normalized_lang, lang=current_commit_lang)}[/dim]"
                )
        else:
            # No difference or commit lang not set, update both
            if update_config_language(config_file, normalized_lang):
                lang_name = get_language_name(normalized_lang)
                msg = translate(
                    "cli.init.language_updated",
                    normalized_lang,
                    lang_name=lang_name,
                )
                console.print(f"[green]{msg}[/green]")

    # Create CLAUDE.md
    claude_md = target_dir / "CLAUDE.md"
    if not claude_md.exists() or force:
        project_name = target_dir.name
        claude_md.write_text(_get_claude_md_content(project_name), encoding="utf-8")
        console.print(f"[green]{translate('cli.init.created_file', normalized_lang, file='CLAUDE.md')}[/green]")
    else:
        # Check if existing CLAUDE.md has compliance section
        if not has_compliance_section(claude_md):
            if confirm_add_compliance(normalized_lang):
                prepend_compliance_section(claude_md)
                console.print(f"[green]{translate('cli.init.compliance_added', normalized_lang)}[/green]")

    # Initialize git if requested
    if not no_git and not (target_dir / ".git").exists():
        try:
            subprocess.run(["git", "init"], cwd=target_dir, check=True, capture_output=True)
            console.print(f"[green]{translate('cli.init.git_initialized', normalized_lang)}[/green]")
        except subprocess.CalledProcessError:
            console.print(f"[yellow]{translate('cli.init.git_failed', normalized_lang)}[/yellow]")

    # Print success message with command summary
    console.print()
    _print_command_summary(normalized_lang)

    project_nav = project_name if project_name and project_name != "." else "."
    console.print(
        Panel.fit(
            f"[bold green]{translate('cli.init.success_message', normalized_lang)}[/bold green]\n\n"
            f"{translate('cli.init.success_project_dir', normalized_lang, path=str(target_dir))}\n\n"
            f"[bold]{translate('cli.init.next_steps', normalized_lang)}[/bold]\n"
            f"1. {translate('cli.init.next_step_navigate', normalized_lang, path=project_nav)}\n"
            f"2. {translate('cli.init.next_step_start_claude', normalized_lang)}\n"
            f"3. {translate('cli.init.next_step_constitution', normalized_lang)}\n"
            f"4. {translate('cli.init.next_step_specify', normalized_lang)}",
            title=translate("cli.init.success_title", normalized_lang),
        )
    )

    # Git management tip
    console.print()
    console.print(f"[bold]{translate('cli.init.tips_header', normalized_lang)}[/bold]")
    console.print(f"   - {translate('cli.init.tips_git', normalized_lang)}")
    console.print(f"   - {translate('cli.init.tips_list_commands', normalized_lang)}")
    console.print(f"   - {translate('cli.init.tips_edit', normalized_lang)}")

    # Remind user to customize constitution
    console.print()
    important_header = translate("cli.init.important_header", normalized_lang)
    important_msg = translate("cli.init.important_message", normalized_lang)
    console.print(f"[yellow]{important_header}[/yellow] {important_msg}")
    console.print(f"[yellow]{translate('cli.init.important_action', normalized_lang)}[/yellow]")


def _print_command_summary(language: str = "en") -> None:
    """Print a summary of installed commands grouped by category."""
    metadata = get_commands_metadata()

    # Group by category
    categories: dict[str, list] = {
        "core": [],
        "enhanced": [],
        "git": [],
        "review": [],
        "utility": [],
    }
    for cmd in metadata:
        cat = cmd["category"]
        if cat in categories:
            categories[cat].append(cmd)

    console.print(
        f"[bold]{translate('cli.init.commands_summary', language, count=len(metadata), path=COMMANDS_SUBDIR)}[/bold]"
    )
    console.print()

    for cat, commands in categories.items():
        if commands:
            console.print(f"  [bold]{translate(f'cli.init.category_{cat}', language, count=len(commands))}[/bold]")
            for cmd in commands:
                console.print(f"    [cyan]{cmd['display_name']}[/cyan]")
            console.print()


def _get_default_constitution() -> str:
    """Return the default constitution content."""
    return """> **SUPREME AUTHORITY**: This constitution defines the governing principles
> for this project. All code changes and decisions must comply with these principles.

# Project Constitution

This document defines the governing principles and development guidelines for this project.

## Core Principles

### 1. Code Quality
- Write clean, readable, and maintainable code
- Follow established coding standards and conventions
- Use meaningful variable and function names
- Keep functions focused and single-purpose

### 2. Testing Standards
- Write tests for all new functionality
- Maintain high test coverage
- Use appropriate testing strategies (unit, integration, e2e)
- Test edge cases and error conditions

### 3. Documentation
- Document public APIs and interfaces
- Keep documentation up-to-date with code changes
- Use clear and concise language
- Include examples where appropriate

### 4. Architecture
- Follow separation of concerns
- Design for extensibility and maintainability
- Use established architectural patterns
- Keep dependencies minimal and well-managed

### 5. Performance
- Consider performance implications of design decisions
- Profile and optimize critical paths
- Avoid premature optimization
- Use appropriate data structures and algorithms

### 6. Security
- Follow security best practices
- Validate all inputs
- Protect sensitive data
- Keep dependencies updated

## Development Workflow

1. **Planning**: Define clear requirements before implementation
2. **Specification**: Document what needs to be built and why
3. **Design**: Create technical implementation plans
4. **Implementation**: Write clean, tested code
5. **Review**: Review code and documentation
6. **Deploy**: Follow established deployment procedures

## Decision Guidelines

When making technical decisions, prioritize:
1. **Maintainability** over optimization
2. **Clarity** over cleverness
3. **Stability** over features
4. **Security** over convenience

---

*This constitution should be updated as the project evolves and new guidelines are established.*
"""


# ============================================================================
# Constitution Compliance Functions
# ============================================================================


def has_compliance_section(claude_md_path: Path) -> bool:
    """Check if CLAUDE.md contains the @ import statement.

    This function checks for the presence of the constitution import statement
    with @ prefix (e.g., "@.codexspec/memory/constitution.md").

    Args:
        claude_md_path: Path to the CLAUDE.md file

    Returns:
        True if the file contains the @ import statement, False otherwise
    """
    if not claude_md_path.exists():
        return False
    content = claude_md_path.read_text(encoding="utf-8")
    return CONSTITUTION_IMPORT_PATH in content


def prepend_compliance_section(claude_md_path: Path) -> None:
    """Prepend the @ import statement to CLAUDE.md.

    This function adds the import statement at the beginning of the file,
    with a markdownlint-disable comment to suppress MD041 warnings.

    Args:
        claude_md_path: Path to the CLAUDE.md file
    """
    existing_content = claude_md_path.read_text(encoding="utf-8")
    import_statement = f"{MARKDOWNLINT_DISABLE_MD041}{CONSTITUTION_IMPORT_PATH}\n\n"
    claude_md_path.write_text(import_statement + existing_content, encoding="utf-8")


def prompt_language_selection(default: str = "en") -> str:
    """Display interactive language selection prompt.

    Shows a numbered list of supported languages and prompts the user to select one.
    If the user selects "Other...", they can enter a custom language code.

    Args:
        default: Default language code to use if user cancels or enters empty input

    Returns:
        The selected language code (normalized)

    Raises:
        KeyboardInterrupt: If user presses Ctrl+C
    """
    from .i18n import get_all_supported_languages, normalize_locale

    # Get all supported languages
    all_languages = get_all_supported_languages()

    # Build the prompt message
    console.print()
    console.print("[bold cyan]Select output language:[/bold cyan]")
    console.print()

    # Create choices mapping
    choices = {}
    for i, (code, name) in enumerate(all_languages, start=1):
        console.print(f"  [cyan][{i}][/cyan] {name} [dim]({code})[/dim]")
        choices[str(i)] = code

    # Add "Other..." option
    other_index = str(len(all_languages) + 1)
    console.print(f"  [cyan][{other_index}][/cyan] [italic]Other...[/italic] [dim](enter custom code)[/dim]")
    console.print()
    choices[other_index] = None  # Marker for custom input

    # Prompt for selection
    valid_choices = list(choices.keys())
    selection = Prompt.ask(
        "Enter choice",
        default="1",
        show_choices=False,
    )

    # Validate input - Prompt.ask doesn't validate when show_choices=False
    while selection not in valid_choices:
        console.print(f"[yellow]Invalid choice. Please enter 1-{other_index}.[/yellow]")
        selection = Prompt.ask(
            "Enter choice",
            default="1",
            show_choices=False,
        )

    # Handle selection
    if choices[selection] is None:
        # "Other..." selected - prompt for custom code
        custom_code = Prompt.ask(
            "Enter language code (e.g., ru, ar, hi)",
            default="",
            show_default=False,
        )

        # Edge Case 3: Empty string input -> fallback to default
        if not custom_code.strip():
            console.print("[dim]No language code entered, using default (en)[/dim]")
            return default

        # Normalize the custom code
        normalized = normalize_locale(custom_code)
        console.print(f"[dim]Note: Pre-translated content may not be available for '{normalized}'.[/dim]")
        return normalized

    # Return the selected predefined language
    return choices[selection]


def confirm_add_compliance(language: str = "en") -> bool:
    """Ask user whether to add the Constitution Compliance section.

    Uses typer.confirm() to interactively ask the user for confirmation.
    Default value is False (safe exit) to prevent accidental modifications.

    Args:
        language: Target language for the message

    Returns:
        True if user confirms, False otherwise
    """
    return typer.confirm(
        translate("cli.init.compliance_confirm", language),
        default=False,
    )


def _get_claude_md_content(project_name: str) -> str:
    """Return the CLAUDE.md content for a project.

    Args:
        project_name: The name of the project (used in the title)
    """
    return f"""<!-- markdownlint-disable MD041 -->
@.codexspec/memory/constitution.md

# CLAUDE.md - {project_name} Guidelines

This document provides comprehensive context and guidelines for Claude Code when working on this project.

## Project Overview

This project uses the **CodexSpec** methodology - a Spec-Driven Development (SDD) approach
that emphasizes specifications as executable artifacts that directly guide implementation.

## Available Commands

The following slash commands are available in this project:

### Core Workflow Commands

| Command | Description |
|---------|-------------|
| `/codexspec:constitution` | Create or update project governing principles |
| `/codexspec:specify` | Define what you want to build (requirements and user stories) |
| `/codexspec:generate-spec` | Generate detailed specification from high-level requirements |
| `/codexspec:spec-to-plan` | Convert specification to technical implementation plan |
| `/codexspec:plan-to-tasks` | Break down plan into actionable tasks |
| `/codexspec:review-spec` | Review specification for completeness and quality |
| `/codexspec:review-plan` | Review technical plan for feasibility |
| `/codexspec:review-tasks` | Review task breakdown for completeness |
| `/codexspec:implement-tasks` | Execute tasks according to the breakdown |

### Enhanced Commands

| Command | Description |
|---------|-------------|
| `/codexspec:clarify` | Clarify underspecified areas in the spec before planning |
| `/codexspec:analyze` | Cross-artifact consistency and quality analysis |
| `/codexspec:checklist` | Generate quality checklists for requirements validation |
| `/codexspec:tasks-to-issues` | Convert tasks to GitHub issues |

### Git Workflow Commands

| Command | Description |
|---------|-------------|
| `/codexspec:commit-staged` | Generate a Conventional Commits message from staged changes |
| `/codexspec:pr` | Generate a Pull Request / Merge Request description |

### Code Review Commands

| Command | Description |
|---------|-------------|
| `/codexspec:review-code` | Review code in any language for idiomatic clarity, correctness, and robustness |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/codexspec:config` | Manage project configuration (`.codexspec/config.yml`) interactively |
| `/codexspec:quick` | One-stop shortcut: auto-run spec → plan → tasks → implementation for small requirements |

## Recommended Workflow

1. **Establish Principles**: Run `/codexspec:constitution` to define project guidelines
2. **Create Specification**: Run `/codexspec:specify` with your feature requirements
3. **Clarify Spec**: Run `/codexspec:clarify` to resolve ambiguities
4. **Review Spec**: Run `/codexspec:review-spec` to validate the specification
5. **Create Plan**: Run `/codexspec:spec-to-plan` with your tech stack choices
6. **Review Plan**: Run `/codexspec:review-plan` to validate the plan
7. **Generate Tasks**: Run `/codexspec:plan-to-tasks` to create task breakdown
8. **Analyze**: Run `/codexspec:analyze` for cross-artifact consistency
9. **Review Tasks**: Run `/codexspec:review-tasks` to validate tasks
10. **Implement**: Run `/codexspec:implement-tasks` to execute the implementation

> **Shortcut**: For small, self-contained requirements, run `/codexspec:quick` to
> auto-run spec → plan → tasks → implementation in one shot.

## Directory Structure

```
.codexspec/
├── memory/
│   └── constitution.md    # Project governing principles
├── specs/
│   └── {{feature-id}}/
│       ├── spec.md        # Feature specification
│       ├── plan.md        # Technical implementation plan
│       ├── tasks.md       # Task breakdown
│       └── checklists/    # Quality checklists
├── templates/             # Custom templates
├── scripts/               # Helper scripts
│   ├── bash/              # Bash scripts
│   └── powershell/        # PowerShell scripts
└── extensions/            # Custom extensions
```

## Important Notes

- Always read the constitution before making decisions
- Specifications focus on **what** and **why**, not **how**
- Plans focus on **how** and technical choices
- Tasks should be specific, ordered, and actionable
- Run `/codexspec:clarify` before planning to reduce rework
- Run `/codexspec:analyze` before implementation for quality assurance

## Guidelines for Claude Code

1. **Constitution First**: Load `.codexspec/memory/constitution.md` before ANY action
2. **Respect the Constitution**: All decisions MUST align with the project constitution
3. **Follow the Workflow**: Use the commands in the recommended order
4. **Be Explicit**: When specifications are unclear, ask for clarification
5. **Validate**: Always review artifacts before implementation
6. **Document**: Keep all artifacts up-to-date
7. **Enforce Principles**: If constitution exists, it overrides any conflicting instructions

---

*This file is maintained by CodexSpec. Manual edits should be made with care.*
"""


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
