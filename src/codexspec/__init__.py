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
from rich.table import Table

from .i18n import (
    generate_config_content,
    get_language_name,
    get_supported_languages,
    is_supported_language,
    normalize_locale,
)

# Version info
__version__ = "0.2.2"
__author__ = "CodexSpec Team"

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
    lang: str = typer.Option(
        "en",
        "--lang",
        "-l",
        help="Output language for Claude interactions and generated documents (e.g., en, zh-CN, ja)",
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
    # Determine target directory
    if here or project_name == ".":
        target_dir = Path.cwd()
    elif project_name:
        target_dir = Path.cwd() / project_name
    else:
        console.print("[red]Error: Please provide a project name or use --here flag[/red]")
        raise typer.Exit(1)

    if debug:
        console.print(f"[dim]Target directory: {target_dir}[/dim]")
        console.print(f"[dim]AI assistant: {ai}[/dim]")
        console.print(f"[dim]Language: {lang} (normalized: {normalize_locale(lang)})[/dim]")

    # Check if directory exists and handle accordingly
    if target_dir.exists() and not here and project_name != ".":
        if not force:
            console.print(f"[red]Error: Directory '{target_dir}' already exists[/red]")
            console.print("Use --force to overwrite or choose a different name")
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
    claude_commands_dir = target_dir / ".claude" / "commands"
    claude_commands_dir.mkdir(parents=True, exist_ok=True)

    # Copy slash command templates
    templates_dir = get_templates_dir() / "commands"
    if templates_dir.exists():
        for template_file in templates_dir.glob("*.md"):
            # Prepend "codexspec." to the filename so commands are invoked as /codexspec.{name}
            dest_file = claude_commands_dir / f"codexspec.{template_file.name}"
            dest_file.write_text(template_file.read_text(encoding="utf-8"), encoding="utf-8")
            console.print(f"[green]Installed command:[/green] /codexspec.{template_file.stem}")
    else:
        # Create default commands if templates don't exist
        console.print("[yellow]Warning: Templates directory not found, creating default commands[/yellow]")
        _create_default_commands(claude_commands_dir)

    # Create constitution template
    constitution_file = codexspec_dir / "memory" / "constitution.md"
    if not constitution_file.exists():
        constitution_file.write_text(_get_default_constitution(), encoding="utf-8")
        console.print("[green]Created:[/green] .codexspec/memory/constitution.md")

    # Create config.yml with language settings
    config_file = codexspec_dir / "config.yml"
    normalized_lang = normalize_locale(lang)
    if not config_file.exists() or force:
        config_content = generate_config_content(
            language=normalized_lang,
            created=datetime.now().strftime("%Y-%m-%d"),
        )
        config_file.write_text(config_content, encoding="utf-8")
        lang_name = get_language_name(normalized_lang)
        console.print(f"[green]Created:[/green] .codexspec/config.yml (language: {lang_name})")

    # Create CLAUDE.md
    claude_md = target_dir / "CLAUDE.md"
    if not claude_md.exists() or force:
        project_name = target_dir.name
        claude_md.write_text(_get_claude_md_content(project_name), encoding="utf-8")
        console.print("[green]Created:[/green] CLAUDE.md")
    else:
        # Check if existing CLAUDE.md has compliance section
        if not has_compliance_section(claude_md):
            if confirm_add_compliance():
                prepend_compliance_section(claude_md)
                console.print("[green]Updated:[/green] CLAUDE.md (added Constitution Compliance section)")

    # Initialize git if requested
    if not no_git and not (target_dir / ".git").exists():
        try:
            subprocess.run(["git", "init"], cwd=target_dir, check=True, capture_output=True)
            console.print("[green]Initialized:[/green] Git repository")
        except subprocess.CalledProcessError:
            console.print("[yellow]Warning: Failed to initialize git repository[/yellow]")

    # Print success message
    console.print()
    project_nav = project_name if project_name and project_name != "." else "."
    console.print(
        Panel.fit(
            "[bold green]CodexSpec project initialized successfully![/bold green]\n\n"
            f"Project directory: [cyan]{target_dir}[/cyan]\n\n"
            "[bold]Next steps:[/bold]\n"
            f"1. Navigate to your project: [cyan]cd {project_nav}[/cyan]\n"
            "2. Start Claude Code: [cyan]claude[/cyan]\n"
            "3. Use [cyan]/codexspec.constitution[/cyan] to establish project principles\n"
            "4. Use [cyan]/codexspec.specify[/cyan] to create your first specification",
            title="Success",
        )
    )

    # Remind user to customize constitution
    console.print()
    console.print("[yellow]Important:[/yellow] The constitution is the foundation of your SDD workflow.")
    console.print(
        "[yellow]Run [bold]/codexspec.constitution[/bold] to customize it for your project and team.[/yellow]"
    )


def _create_default_commands(commands_dir: Path) -> None:
    """Create default slash commands."""
    commands = {
        "constitution": _get_constitution_command(),
        "specify": _get_specify_command(),
        "generate-spec": _get_generate_spec_command(),
        "spec-to-plan": _get_spec_to_plan_command(),
        "plan-to-tasks": _get_plan_to_tasks_command(),
        "review-spec": _get_review_spec_command(),
        "review-plan": _get_review_plan_command(),
        "review-tasks": _get_review_tasks_command(),
        "implement-tasks": _get_implement_tasks_command(),
        "clarify": _get_clarify_command(),
        "analyze": _get_analyze_command(),
        "checklist": _get_checklist_command(),
        "tasks-to-issues": _get_tasks_to_issues_command(),
    }

    for name, content in commands.items():
        # Prepend "codexspec." to the filename so commands are invoked as /codexspec.{name}
        cmd_file = commands_dir / f"codexspec.{name}.md"
        cmd_file.write_text(content, encoding="utf-8")
        console.print(f"[green]Installed command:[/green] /codexspec.{name}")


def _get_constitution_command() -> str:
    """Return the constitution command template."""
    return """---
description: Create or update the project constitution - the governing principles that guide all development decisions
handoffs:
  - agent: claude
    step: Analyze project context and generate constitution
---

# Project Constitution Generator

## User Input

$ARGUMENTS

## Instructions

You are tasked with creating or updating the project constitution.
The constitution serves as the foundational document that guides all technical decisions
and implementation choices throughout the project lifecycle.

### Steps

1. **Analyze the Request**: Understand the user's requirements for project principles,
   coding standards, and governance rules.

2. **Review Existing Context**: Check `.codexspec/memory/constitution.md` if it exists for current principles.

3. **Generate Constitution**: Create a comprehensive constitution document that includes:
   - Core development principles
   - Code quality standards
   - Testing requirements
   - Documentation guidelines
   - Architecture decisions
   - Performance requirements
   - Security considerations

4. **Save the Constitution**: Write the constitution to `.codexspec/memory/constitution.md`

### Output Format

The constitution should be structured as a markdown document with clear sections and actionable guidelines.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
"""


def _get_specify_command() -> str:
    """Return the specify command template."""
    return """---
description: Create a new feature specification describing what to build and why
handoffs:
  - agent: claude
    step: Generate feature specification from user requirements
---

# Feature Specification Generator

## User Input

$ARGUMENTS

## Instructions

You are tasked with creating a detailed feature specification.
Focus on the **what** and **why**, not the technical implementation.

### Steps

1. **Understand Requirements**: Parse the user's input to understand what feature they want to build.

2. **Create Feature Branch**: Create a new feature branch (e.g., `001-feature-name`).

3. **Generate Specification**: Create a comprehensive spec document including:
   - Feature overview
   - User stories
   - Functional requirements
   - Non-functional requirements
   - Acceptance criteria
   - Edge cases and constraints

4. **Save Specification**: Write to `.codexspec/specs/{feature-id}/spec.md`

### Output Format

The specification should follow the template in `.codexspec/templates/spec-template.md`.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
"""


def _get_generate_spec_command() -> str:
    """Return the generate-spec command template."""
    return """---
description: Generate a detailed specification document from high-level requirements
handoffs:
  - agent: claude
    step: Transform requirements into detailed specification
---

# Specification Generator

## User Input

$ARGUMENTS

## Instructions

Generate a detailed specification document from the provided high-level requirements.

### Steps

1. **Analyze Input**: Parse and understand the high-level requirements.

2. **Expand Requirements**: Convert high-level ideas into detailed, actionable specifications.

3. **Add Context**: Include relevant context, assumptions, and constraints.

4. **Generate Document**: Create a structured specification document.

### Output

A comprehensive specification document saved to the appropriate location.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
"""


def _get_spec_to_plan_command() -> str:
    """Return the spec-to-plan command template."""
    return """---
description: Convert a feature specification into a technical implementation plan
handoffs:
  - agent: claude
    step: Generate technical plan from specification
---

# Specification to Plan Converter

## User Input

$ARGUMENTS

## Instructions

Convert the feature specification into a detailed technical implementation plan.

### Steps

1. **Read Specification**: Load the specification from `.codexspec/specs/{feature-id}/spec.md`.

2. **Define Tech Stack**: Based on user input, define the technologies and frameworks to use.

3. **Create Architecture**: Design the system architecture and component structure.

4. **Generate Plan**: Create a comprehensive implementation plan including:
   - Technology choices
   - Architecture overview
   - Component breakdown
   - Data models
   - API contracts
   - Implementation phases

5. **Save Plan**: Write to `.codexspec/specs/{feature-id}/plan.md`

### Output

A detailed technical implementation plan.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
"""


def _get_plan_to_tasks_command() -> str:
    """Return the plan-to-tasks command template."""
    return """---
description: Break down a technical implementation plan into actionable tasks
handoffs:
  - agent: claude
    step: Generate task breakdown from plan
---

# Plan to Tasks Converter

## User Input

$ARGUMENTS

## Instructions

Break down the technical implementation plan into specific, actionable tasks.

### Steps

1. **Read Plan**: Load the plan from `.codexspec/specs/{feature-id}/plan.md`.

2. **Identify Tasks**: Parse the plan and identify all implementation tasks.

3. **Order Tasks**: Organize tasks in the correct dependency order.

4. **Mark Parallelizable**: Identify tasks that can be executed in parallel.

5. **Generate Task List**: Create a comprehensive task breakdown including:
   - Task descriptions
   - File paths for each task
   - Dependencies between tasks
   - Estimated complexity
   - Parallel execution markers

6. **Save Tasks**: Write to `.codexspec/specs/{feature-id}/tasks.md`

### Output

A structured task list ready for implementation.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
"""


def _get_review_spec_command() -> str:
    """Return the review-spec command template."""
    return """---
description: Review and validate a feature specification for completeness and quality
handoffs:
  - agent: claude
    step: Review specification against quality criteria
---

# Specification Reviewer

## User Input

$ARGUMENTS

## Instructions

Review the feature specification for completeness, clarity, and consistency.

### Steps

1. **Load Specification**: Read the spec from `.codexspec/specs/{feature-id}/spec.md`.

2. **Check Completeness**: Verify all required sections are present and complete.

3. **Validate Clarity**: Ensure requirements are clear and unambiguous.

4. **Check Consistency**: Verify no contradictions exist in the specification.

5. **Generate Report**: Create a review report with:
   - Completeness score
   - Identified issues
   - Improvement suggestions
   - Quality checklist results

### Output

A comprehensive review report with actionable feedback.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
"""


def _get_review_plan_command() -> str:
    """Return the review-plan command template."""
    return """---
description: Review and validate a technical implementation plan
handoffs:
  - agent: claude
    step: Review plan against best practices and requirements
---

# Plan Reviewer

## User Input

$ARGUMENTS

## Instructions

Review the technical implementation plan for completeness, feasibility, and alignment with the specification.

### Steps

1. **Load Plan**: Read the plan from `.codexspec/specs/{feature-id}/plan.md`.

2. **Check Alignment**: Verify the plan aligns with the specification requirements.

3. **Evaluate Feasibility**: Assess technical feasibility of proposed solutions.

4. **Review Architecture**: Check architectural decisions for best practices.

5. **Generate Report**: Create a review report with:
   - Alignment score
   - Technical concerns
   - Risk assessment
   - Improvement suggestions

### Output

A comprehensive review report with actionable feedback.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
"""


def _get_review_tasks_command() -> str:
    """Return the review-tasks command template."""
    return """---
description: Review and validate the task breakdown for completeness and correct ordering
handoffs:
  - agent: claude
    step: Review tasks against plan and dependencies
---

# Tasks Reviewer

## User Input

$ARGUMENTS

## Instructions

Review the task breakdown for completeness, correct ordering, and proper dependency management.

### Steps

1. **Load Tasks**: Read the tasks from `.codexspec/specs/{feature-id}/tasks.md`.

2. **Check Coverage**: Verify all plan items are covered by tasks.

3. **Validate Dependencies**: Ensure task dependencies are correct and complete.

4. **Check Ordering**: Verify tasks are in the correct execution order.

5. **Generate Report**: Create a review report with:
   - Coverage analysis
   - Dependency validation results
   - Ordering concerns
   - Improvement suggestions

### Output

A comprehensive review report with actionable feedback.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
"""


def _get_implement_tasks_command() -> str:
    """Return the implement-tasks command template."""
    return """---
description: Execute the implementation tasks according to the task breakdown
handoffs:
  - agent: claude
    step: Implement tasks following the defined order and dependencies
---

# Task Implementer

## User Input

$ARGUMENTS

## Instructions

Execute the implementation tasks in the correct order, following the task breakdown.

### Steps

1. **Load Prerequisites**: Verify constitution, spec, plan, and tasks exist.

2. **Parse Tasks**: Read and parse the task breakdown from `.codexspec/specs/{feature-id}/tasks.md`.

3. **Execute Tasks**: Implement each task in order:
   - Follow the task description
   - Create/modify files as specified
   - Respect dependencies
   - Handle parallelizable tasks appropriately

4. **Validate Progress**: After each task, validate the implementation.

5. **Report Progress**: Provide clear progress updates throughout implementation.

### Output

Complete implementation of all tasks with progress reporting.

> [!NOTE]
> This is a placeholder command. The full implementation will be added in future versions.
"""


def _get_clarify_command() -> str:
    """Return the clarify command template."""
    return """---
description: Identify underspecified areas in the current feature spec by asking targeted clarification questions
handoffs:
  - agent: claude
    step: Ask clarification questions and update spec
---

# Specification Clarifier

## User Input

$ARGUMENTS

## Instructions

You are tasked with identifying and resolving ambiguities in the feature specification.

### Steps

1. **Load Specification**: Read the spec from `.codexspec/specs/{feature-id}/spec.md`.

2. **Identify Ambiguities**: Scan for:
   - Vague terms (fast, good, user-friendly)
   - Missing edge cases
   - Underspecified requirements
   - Conflicting statements

3. **Ask Questions**: Present targeted questions one at a time (max 5).

4. **Update Spec**: Record answers in a `## Clarifications` section.

> [!NOTE]
> This command should run BEFORE `/codexspec.spec-to-plan`.
"""


def _get_analyze_command() -> str:
    """Return the analyze command template."""
    return """---
description: Perform cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md
---

# Cross-Artifact Analyzer

## User Input

$ARGUMENTS

## Instructions

Perform a read-only analysis of all specification artifacts.

### Analysis Categories

1. **Duplication Detection**: Identify near-duplicate requirements
2. **Ambiguity Detection**: Flag vague or underspecified items
3. **Coverage Gaps**: Requirements without tasks, tasks without requirements
4. **Constitution Alignment**: Check against project principles
5. **Inconsistency**: Terminology drift, conflicting requirements

### Output

A structured analysis report with severity levels (CRITICAL, HIGH, MEDIUM, LOW).

> [!NOTE]
> This command runs AFTER `/codexspec.plan-to-tasks` and BEFORE `/codexspec.implement-tasks`.
"""


def _get_checklist_command() -> str:
    """Return the checklist command template."""
    return """---
description: Generate a custom quality checklist for validating requirements completeness and clarity
---

# Requirements Quality Checklist Generator

## User Input

$ARGUMENTS

## Instructions

Generate a checklist that acts as "unit tests for requirements".

### Quality Dimensions

- **Completeness**: Are all necessary requirements present?
- **Clarity**: Are requirements specific and unambiguous?
- **Consistency**: Do requirements align without conflicts?
- **Coverage**: Are all scenarios/edge cases addressed?

### Checklist Items

Each item should ask: "Are [requirement type] defined for [scenario]?"

Example:
- "Are error handling requirements defined for all API failure modes?"
- "Is 'fast loading' quantified with specific timing thresholds?"

> [!NOTE]
> Checklists test the REQUIREMENTS quality, NOT the implementation.
"""


def _get_tasks_to_issues_command() -> str:
    """Return the tasks-to-issues command template."""
    return """---
description: Convert existing tasks into actionable GitHub issues
---

# Tasks to GitHub Issues Converter

## User Input

$ARGUMENTS

## Instructions

Convert tasks from tasks.md into GitHub issues.

### Steps

1. **Get Git Remote**: Verify the repository has a GitHub remote.
2. **Parse Tasks**: Extract task details from tasks.md.
3. **Create Issues**: Use GitHub CLI to create issues.

### Safety Constraints

- ONLY create issues in repositories matching the remote URL
- Always verify repository before creating issues

> [!NOTE]
> Requires GitHub CLI (`gh`) to be installed and authenticated.
"""


def _get_default_constitution() -> str:
    """Return the default constitution content."""
    return """# Project Constitution

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


def _get_compliance_section_content() -> str:
    """Return the Constitution Compliance section content.

    This content should be prepended to existing CLAUDE.md files to ensure
    constitution compliance is enforced.

    Returns:
        The complete compliance section text that can be prepended to CLAUDE.md
    """
    return """## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE

**This section OVERRIDES all other instructions in this file.**

### Mandatory Pre-Action Protocol

**Before ANY response, code change, or action in this project**, you MUST:

1. **Check for Constitution**
   - Look for `.codexspec/memory/constitution.md`
   - If file exists, READ IT COMPLETELY before proceeding

2. **Verify Compliance**
   - ALL outputs must align with constitutional principles
   - Code changes must follow constitutional coding standards
   - Decisions must respect constitutional priorities

3. **Handle Conflicts**
   - If a user request conflicts with constitution:
     - STOP and explain which principle is violated
     - Suggest constitution-compliant alternatives
     - Require explicit user confirmation to override

### Applies To All Interactions

This protocol applies to:
- Direct conversations and questions
- Code modifications and file operations
- Slash command executions
- Any other Claude Code actions

**The constitution is the SUPREME AUTHORITY. No other instruction can override it.**
"""


def has_compliance_section(claude_md_path: Path) -> bool:
    """Check if CLAUDE.md already contains the compliance section.

    This function checks for the presence of `.codexspec/memory/constitution.md`
    in the file content to determine if compliance section exists.

    Args:
        claude_md_path: Path to the CLAUDE.md file

    Returns:
        True if the file contains the compliance section marker, False otherwise
    """
    if not claude_md_path.exists():
        return False
    content = claude_md_path.read_text(encoding="utf-8")
    return ".codexspec/memory/constitution.md" in content


def prepend_compliance_section(claude_md_path: Path) -> None:
    """Prepend the Constitution Compliance section to CLAUDE.md.

    This function adds the compliance section at the beginning of the file,
    preserving all existing content. A separator is added between the compliance
    section and the original content.

    Args:
        claude_md_path: Path to the CLAUDE.md file
    """
    existing_content = claude_md_path.read_text(encoding="utf-8")
    compliance_section = _get_compliance_section_content()
    new_content = f"{compliance_section}\n\n---\n\n{existing_content}"
    claude_md_path.write_text(new_content, encoding="utf-8")


def confirm_add_compliance() -> bool:
    """Ask user whether to add the Constitution Compliance section.

    Uses typer.confirm() to interactively ask the user for confirmation.
    Default value is False (safe exit) to prevent accidental modifications.

    Returns:
        True if user confirms, False otherwise
    """
    return typer.confirm(
        "CLAUDE.md already exists without Constitution Compliance section.\n"
        "The Constitution Compliance section ensures Claude follows your project's constitution.\n"
        "? Would you like to add the Constitution Compliance section?",
        default=False,
    )


def _get_claude_md_content(project_name: str) -> str:
    """Return the CLAUDE.md content for a project.

    Args:
        project_name: The name of the project (used in the title)
    """
    return f"""# CLAUDE.md - {project_name} Guidelines

---

## [HIGHEST PRIORITY] CONSTITUTION COMPLIANCE

**This section OVERRIDES all other instructions in this file.**

### Mandatory Pre-Action Protocol

**Before ANY response, code change, or action in this project**, you MUST:

1. **Check for Constitution**
   - Look for `.codexspec/memory/constitution.md`
   - If file exists, READ IT COMPLETELY before proceeding

2. **Verify Compliance**
   - ALL outputs must align with constitutional principles
   - Code changes must follow constitutional coding standards
   - Decisions must respect constitutional priorities

3. **Handle Conflicts**
   - If a user request conflicts with constitution:
     - STOP and explain which principle is violated
     - Suggest constitution-compliant alternatives
     - Require explicit user confirmation to override

### Applies To All Interactions

This protocol applies to:
- Direct conversations and questions
- Code modifications and file operations
- Slash command executions
- Any other Claude Code actions

**The constitution is the SUPREME AUTHORITY. No other instruction can override it.**

---

## Project Overview

This project uses the **CodexSpec** methodology - a Spec-Driven Development (SDD) approach
that emphasizes specifications as executable artifacts that directly guide implementation.

## Available Commands

The following slash commands are available in this project:

### Core Workflow Commands

| Command | Description |
|---------|-------------|
| `/codexspec.constitution` | Create or update project governing principles |
| `/codexspec.specify` | Define what you want to build (requirements and user stories) |
| `/codexspec.generate-spec` | Generate detailed specification from high-level requirements |
| `/codexspec.spec-to-plan` | Convert specification to technical implementation plan |
| `/codexspec.plan-to-tasks` | Break down plan into actionable tasks |
| `/codexspec.review-spec` | Review specification for completeness and quality |
| `/codexspec.review-plan` | Review technical plan for feasibility |
| `/codexspec.review-tasks` | Review task breakdown for completeness |
| `/codexspec.implement-tasks` | Execute tasks according to the breakdown |

### Enhanced Commands

| Command | Description |
|---------|-------------|
| `/codexspec.clarify` | Clarify underspecified areas in the spec before planning |
| `/codexspec.analyze` | Cross-artifact consistency and quality analysis |
| `/codexspec.checklist` | Generate quality checklists for requirements validation |
| `/codexspec.tasks-to-issues` | Convert tasks to GitHub issues |

## Recommended Workflow

1. **Establish Principles**: Run `/codexspec.constitution` to define project guidelines
2. **Create Specification**: Run `/codexspec.specify` with your feature requirements
3. **Clarify Spec**: Run `/codexspec.clarify` to resolve ambiguities
4. **Review Spec**: Run `/codexspec.review-spec` to validate the specification
5. **Create Plan**: Run `/codexspec.spec-to-plan` with your tech stack choices
6. **Review Plan**: Run `/codexspec.review-plan` to validate the plan
7. **Generate Tasks**: Run `/codexspec.plan-to-tasks` to create task breakdown
8. **Analyze**: Run `/codexspec.analyze` for cross-artifact consistency
9. **Review Tasks**: Run `/codexspec.review-tasks` to validate tasks
10. **Implement**: Run `/codexspec.implement-tasks` to execute the implementation

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
- Run `/codexspec.clarify` before planning to reduce rework
- Run `/codexspec.analyze` before implementation for quality assurance

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
