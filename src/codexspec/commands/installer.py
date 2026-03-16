"""Command installer module for CodexSpec.

This module provides functions for installing, detecting, and migrating
CodexSpec slash commands.
"""

import shutil
from pathlib import Path
from typing import Optional, TypedDict

from codexspec.translator import extract_frontmatter_fields, load_translation_cache, translate_template_frontmatter

# Constants
COMMANDS_SUBDIR = "codexspec"  # Subdirectory name for commands
OLD_COMMAND_PREFIX = "codexspec."  # Prefix for old structure command files


class CommandMetadata(TypedDict):
    """Command metadata structure.

    Attributes:
        name: Command name without prefix (e.g., "constitution")
        display_name: Full display name (e.g., "/codexspec.constitution")
        description: Command description for list-commands output
        category: Command category ("core", "enhanced", or "git")
        file_name: Template file name (e.g., "constitution.md")
    """

    name: str
    display_name: str
    description: str
    category: str
    file_name: str


def get_commands_metadata() -> list[CommandMetadata]:
    """Get metadata for all available CodexSpec commands.

    Returns a list of command metadata sorted by category, used for:
    - list-commands CLI command output formatting
    - init command installed commands summary display

    Returns:
        List of CommandMetadata dictionaries sorted by category priority:
        core (9) -> enhanced (4) -> git (3)
    """
    return [
        # Core Commands (9)
        {
            "name": "constitution",
            "display_name": "/codexspec.constitution",
            "description": "创建或更新项目宪法，定义开发原则和规范",
            "category": "core",
            "file_name": "constitution.md",
        },
        {
            "name": "specify",
            "display_name": "/codexspec.specify",
            "description": "通过交互式问答明确需求，探索'做什么'和'为什么'",
            "category": "core",
            "file_name": "specify.md",
        },
        {
            "name": "generate-spec",
            "display_name": "/codexspec.generate-spec",
            "description": "从已明确的需求生成详细的 spec.md 规格文档",
            "category": "core",
            "file_name": "generate-spec.md",
        },
        {
            "name": "spec-to-plan",
            "display_name": "/codexspec.spec-to-plan",
            "description": "将功能规格转换为技术实现计划",
            "category": "core",
            "file_name": "spec-to-plan.md",
        },
        {
            "name": "plan-to-tasks",
            "display_name": "/codexspec.plan-to-tasks",
            "description": "将技术计划分解为可执行的任务列表",
            "category": "core",
            "file_name": "plan-to-tasks.md",
        },
        {
            "name": "review-spec",
            "display_name": "/codexspec.review-spec",
            "description": "审查功能规格的完整性和质量",
            "category": "core",
            "file_name": "review-spec.md",
        },
        {
            "name": "review-plan",
            "display_name": "/codexspec.review-plan",
            "description": "审查技术计划的可行性和对齐度",
            "category": "core",
            "file_name": "review-plan.md",
        },
        {
            "name": "review-tasks",
            "display_name": "/codexspec.review-tasks",
            "description": "审查任务分解的完整性和 TDD 合规性",
            "category": "core",
            "file_name": "review-tasks.md",
        },
        {
            "name": "implement-tasks",
            "description": "按 TDD 流程执行任务实现",
            "display_name": "/codexspec.implement-tasks",
            "category": "core",
            "file_name": "implement-tasks.md",
        },
        # Enhanced Commands (4)
        {
            "name": "clarify",
            "display_name": "/codexspec.clarify",
            "description": "在技术规划前提出澄清问题",
            "category": "enhanced",
            "file_name": "clarify.md",
        },
        {
            "name": "analyze",
            "display_name": "/codexspec.analyze",
            "description": "跨工件一致性和质量分析",
            "category": "enhanced",
            "file_name": "analyze.md",
        },
        {
            "name": "checklist",
            "display_name": "/codexspec.checklist",
            "description": "生成需求质量检查清单",
            "category": "enhanced",
            "file_name": "checklist.md",
        },
        {
            "name": "tasks-to-issues",
            "display_name": "/codexspec.tasks-to-issues",
            "description": "将任务转换为 GitHub Issues",
            "category": "enhanced",
            "file_name": "tasks-to-issues.md",
        },
        # Git Workflow Commands (3)
        {
            "name": "commit",
            "display_name": "/codexspec.commit",
            "description": "生成符合 Conventional Commits 规范的提交信息",
            "category": "git",
            "file_name": "commit.md",
        },
        {
            "name": "commit-staged",
            "display_name": "/codexspec.commit-staged",
            "description": "从暂存更改生成提交信息",
            "category": "git",
            "file_name": "commit-staged.md",
        },
        {
            "name": "pr",
            "display_name": "/codexspec.pr",
            "description": "生成 PR/MR 描述",
            "category": "git",
            "file_name": "pr.md",
        },
    ]


def get_installed_commands_metadata() -> list[CommandMetadata]:
    """Get metadata from installed command files with fallback to defaults.

    This function reads the frontmatter from installed command files to get
    translated descriptions. If a command file doesn't exist or doesn't have
    a description in its frontmatter, falls back to the hardcoded default.

    Returns:
        List of CommandMetadata with descriptions from installed files when available.
    """
    # Get hardcoded default metadata
    default_metadata = get_commands_metadata()

    # Find installed commands directory
    commands_dir = Path.cwd() / ".claude" / "commands" / COMMANDS_SUBDIR

    if not commands_dir.exists():
        return default_metadata

    result: list[CommandMetadata] = []
    for cmd in default_metadata:
        cmd_file = commands_dir / cmd["file_name"]

        if cmd_file.exists():
            # Read frontmatter from installed file
            content = cmd_file.read_text(encoding="utf-8")
            fields = extract_frontmatter_fields(content)

            if fields.get("description"):
                # Use translated description from installed file
                result.append({**cmd, "description": fields["description"]})
            else:
                result.append(cmd)
        else:
            result.append(cmd)

    return result


def detect_old_structure(claude_dir: Path) -> list[Path]:
    """Detect old structure command files that need migration.

    Looks for files with the OLD_COMMAND_PREFIX in the .claude/commands/
    root directory (not in subdirectories).

    Args:
        claude_dir: Path to the .claude directory

    Returns:
        List of Path objects for old structure command files
    """
    commands_dir = claude_dir / "commands"
    if not commands_dir.exists():
        return []

    old_files = []
    for file_path in commands_dir.iterdir():
        # Only check files in root commands directory, not subdirectories
        if file_path.is_file() and file_path.name.startswith(OLD_COMMAND_PREFIX):
            old_files.append(file_path)

    return sorted(old_files)


def migrate_old_commands(
    claude_dir: Path,
    old_files: list[Path],
) -> bool:
    """Migrate old structure commands to new subdirectory.

    Pure file operation without user interaction. Moves old command files
    from .claude/commands/ to .claude/commands/codexspec/.

    Args:
        claude_dir: Path to the .claude directory
        old_files: List of old command file paths to migrate

    Returns:
        True if migration succeeded, False if any error occurred

    Note:
        This function performs pure file operations. User confirmation
        and output prompts should be handled in the CLI layer.
    """
    if not old_files:
        return True

    commands_dir = claude_dir / "commands"
    target_dir = commands_dir / COMMANDS_SUBDIR

    try:
        # Ensure target directory exists
        target_dir.mkdir(parents=True, exist_ok=True)

        for old_file in old_files:
            # Remove prefix to get new filename
            # e.g., "codexspec.constitution.md" -> "constitution.md"
            new_name = old_file.name.replace(OLD_COMMAND_PREFIX, "")
            target_path = target_dir / new_name

            # Move file (shutil.move handles cross-filesystem moves)
            shutil.move(str(old_file), str(target_path))

        return True
    except Exception:
        return False


def install_commands_to_subdir(
    target_dir: Path,
    templates_dir: Path,
    force: bool = False,
    language: str = "en",
    translations_dir: Optional[Path] = None,
) -> int:
    """Install command templates to subdirectory with optional translation.

    Pure file operation without user interaction. Copies template files
    from the templates directory to the target subdirectory, applying
    frontmatter translation if a non-English language is specified.

    Args:
        target_dir: Target directory (.claude/commands/codexspec)
        templates_dir: Source templates directory
        force: If True, overwrite existing files; if False, skip existing
        language: Target language for frontmatter translation (default: "en")
        translations_dir: Custom translations directory (for testing)

    Returns:
        Number of commands installed

    Note:
        This function performs pure file operations. User confirmation
        and output prompts should be handled in the CLI layer.
    """
    if not templates_dir.exists():
        return 0

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    # Load translation cache if needed
    translation_cache = None
    if language != "en":
        translation_cache = load_translation_cache(language, translations_dir)

    installed_count = 0
    for template_file in templates_dir.glob("*.md"):
        target_path = target_dir / template_file.name

        # Skip if exists and not forcing
        if target_path.exists() and not force:
            continue

        # Read template content
        content = template_file.read_text(encoding="utf-8")

        # Apply translation if available
        template_name = template_file.stem  # filename without extension
        content = translate_template_frontmatter(content, template_name, language, translation_cache)

        # Write to target
        target_path.write_text(content, encoding="utf-8")
        installed_count += 1

    return installed_count


def should_update_commands(codexspec_dir: Path) -> bool:
    """Check if commands need updating (subdirectory already exists).

    Args:
        codexspec_dir: Path to the .codexspec directory

    Returns:
        True if the commands subdirectory exists, indicating update mode
    """
    # Check if .claude/commands/codexspec exists
    claude_commands_subdir = codexspec_dir.parent / ".claude" / "commands" / COMMANDS_SUBDIR
    return claude_commands_subdir.exists()
