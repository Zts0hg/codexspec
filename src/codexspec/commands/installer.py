"""Command installer module for CodexSpec.

This module provides functions for installing, detecting, and migrating
CodexSpec slash commands.
"""

import shutil
from pathlib import Path
from typing import Optional, TypedDict

from codexspec.translator import (
    apply_translations_to_template,
    extract_frontmatter_fields,
    load_translation_cache,
    translate_template_frontmatter,
)

# Constants
COMMANDS_SUBDIR = "codexspec"  # Subdirectory name for commands
OLD_COMMAND_PREFIX = "codexspec."  # Prefix for old structure command files


class CommandMetadata(TypedDict):
    """Command metadata structure.

    Attributes:
        name: Command name without prefix (e.g., "constitution")
        display_name: Full display name (e.g., "/codexspec:constitution")
        description: Command description for list-commands output
        category: Command category ("core", "enhanced", "git", "review", or "utility")
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
        core (13) -> enhanced (9) -> git (3) -> review (1) -> utility (2)
        Total: 28 commands
    """
    return [
        # Core Commands (13)
        {
            "name": "constitution",
            "display_name": "/codexspec:constitution",
            "description": "制定或更新项目开发原则，写入 constitution.md 并检查相关文档的一致性。",
            "category": "core",
            "file_name": "constitution.md",
        },
        {
            "name": "specify",
            "display_name": "/codexspec:specify",
            "description": "澄清功能目标、范围和约束，将确认的需求整理为 requirements.md。",
            "category": "core",
            "file_name": "specify.md",
        },
        {
            "name": "blueprint",
            "display_name": "/codexspec:blueprint",
            "description": "规划多个功能，将确认的需求写入共享蓝图，并管理供 auto-dev 执行的待开发内容和顺序。",
            "category": "core",
            "file_name": "blueprint.md",
        },
        {
            "name": "generate-spec",
            "display_name": "/codexspec:generate-spec",
            "description": "将已确认需求编写为 spec.md，明确功能行为、异常处理和验收标准。",
            "category": "core",
            "file_name": "generate-spec.md",
        },
        {
            "name": "spec-to-design",
            "display_name": "/codexspec:spec-to-design",
            "description": "根据 spec.md 编写 design.md，定义组件、接口及关键技术决策。",
            "category": "core",
            "file_name": "spec-to-design.md",
        },
        {
            "name": "design-to-plan",
            "display_name": "/codexspec:design-to-plan",
            "description": "将 design.md 转化为 plan.md，安排实现阶段、执行顺序和验证步骤。",
            "category": "core",
            "file_name": "design-to-plan.md",
        },
        {
            "name": "plan-to-tasks",
            "display_name": "/codexspec:plan-to-tasks",
            "description": "将 plan.md 拆分为 tasks.md，明确具体工作、依赖和验证方法，并列出可测试任务的测试场景。",
            "category": "core",
            "file_name": "plan-to-tasks.md",
        },
        {
            "name": "review-spec",
            "display_name": "/codexspec:review-spec",
            "description": "审查 spec.md 的需求覆盖和验收标准，判断是否可进入设计阶段。",
            "category": "core",
            "file_name": "review-spec.md",
        },
        {
            "name": "review-design",
            "display_name": "/codexspec:review-design",
            "description": "审查 design.md 的需求覆盖与技术可行性，判断是否可制定实现计划。",
            "category": "core",
            "file_name": "review-design.md",
        },
        {
            "name": "review-plan",
            "display_name": "/codexspec:review-plan",
            "description": "审查 plan.md 的实现步骤、顺序和需求覆盖，判断是否可拆分任务。",
            "category": "core",
            "file_name": "review-plan.md",
        },
        {
            "name": "review-tasks",
            "display_name": "/codexspec:review-tasks",
            "description": "审查 tasks.md 的任务覆盖、依赖和验证方法，判断是否可开始实现。",
            "category": "core",
            "file_name": "review-tasks.md",
        },
        {
            "name": "implement-tasks",
            "description": "按 tasks.md 实现功能，执行测试与独立审查，并修复经核实的问题。",
            "display_name": "/codexspec:implement-tasks",
            "category": "core",
            "file_name": "implement-tasks.md",
        },
        {
            "name": "auto-dev",
            "display_name": "/codexspec:auto-dev",
            "description": "按蓝图顺序自动开发已确认需求，完成从规格到实现、验证和提交的流程。",
            "category": "core",
            "file_name": "auto-dev.md",
        },
        # Enhanced Commands (9)
        {
            "name": "clarify",
            "display_name": "/codexspec:clarify",
            "description": "通过问答澄清遗漏、歧义和矛盾，将确认结果同步到 requirements.md 和 spec.md。",
            "category": "enhanced",
            "file_name": "clarify.md",
        },
        {
            "name": "analyze",
            "display_name": "/codexspec:analyze",
            "description": "核对需求到任务的文档一致性，自动修复可由已确认需求确定的下游问题。",
            "category": "enhanced",
            "file_name": "analyze.md",
        },
        {
            "name": "checklist",
            "display_name": "/codexspec:checklist",
            "description": "生成需求质量检查清单，检查完整性、清晰度与场景覆盖，而非测试代码。",
            "category": "enhanced",
            "file_name": "checklist.md",
        },
        {
            "name": "tasks-to-issues",
            "display_name": "/codexspec:tasks-to-issues",
            "description": "将 tasks.md 中的任务创建为 GitHub Issue，附上相关文件、依赖及已有验收标准。",
            "category": "enhanced",
            "file_name": "tasks-to-issues.md",
        },
        {
            "name": "distill",
            "display_name": "/codexspec:distill",
            "description": "从工作交互中提取可复用经验，存入项目知识库，或审阅、修订和合并已有记录。",
            "category": "enhanced",
            "file_name": "distill.md",
        },
        {
            "name": "evolve",
            "display_name": "/codexspec:evolve",
            "description": "将已验证并认可的通用项目知识整理成命令或技能，经你确认后向上游提交 PR。",
            "category": "enhanced",
            "file_name": "evolve.md",
        },
        {
            "name": "onboard",
            "display_name": "/codexspec:onboard",
            "description": "扫描已有代码，将项目约定和明确限制记录到知识库，限制类记录经你审阅后保存。",
            "category": "enhanced",
            "file_name": "onboard.md",
        },
        {
            "name": "reverse-spec",
            "display_name": "/codexspec:reverse-spec",
            "description": "从已有代码生成架构概览或模块规格与设计；已有确认基线时报告差异。",
            "category": "enhanced",
            "file_name": "reverse-spec.md",
        },
        {
            "name": "debug",
            "display_name": "/codexspec:debug",
            "description": "复现报错或异常现象，定位根本原因，再进行最小修复并验证结果。",
            "category": "enhanced",
            "file_name": "debug.md",
        },
        # Git Workflow Commands (3)
        {
            "name": "commit-staged",
            "display_name": "/codexspec:commit-staged",
            "description": "仅根据暂存改动生成提交信息并执行已授权的提交；-p 只预览，不执行提交。",
            "category": "git",
            "file_name": "commit-staged.md",
        },
        {
            "name": "pr",
            "display_name": "/codexspec:pr",
            "description": "根据分支差异生成 GitHub PR 或 GitLab MR 的标题、说明与验证指引。",
            "category": "git",
            "file_name": "pr.md",
        },
        {
            "name": "release-notes",
            "display_name": "/codexspec:release-notes",
            "description": "根据 Git 历史增补 CHANGELOG.md 并生成发布说明，不执行发布。",
            "category": "git",
            "file_name": "release-notes.md",
        },
        # Code Review Commands (1)
        {
            "name": "review-code",
            "display_name": "/codexspec:review-code",
            "description": "审查 Git 改动并判断是否可合并；--audit 用于评估现有代码质量。",
            "category": "review",
            "file_name": "review-code.md",
        },
        # Utility Commands (2)
        {
            "name": "config",
            "display_name": "/codexspec:config",
            "description": "交互式设置语言、自动化和 worktree 等项目选项；--view 只查看配置。",
            "category": "utility",
            "file_name": "config.md",
        },
        {
            "name": "quick",
            "display_name": "/codexspec:quick",
            "description": "确认小范围需求后，自动完成规格、计划、任务、实现与审查。",
            "category": "utility",
            "file_name": "quick.md",
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


def validate_retired_planning_entry(entry: Path, boundary: Path) -> None:
    """Refuse to retire an entry through a symbolic-link parent directory."""
    entry.relative_to(boundary)
    for parent in entry.parents:
        if parent.is_symlink():
            raise OSError(f"Symbolic-link parent of planning command: {parent}")
        if parent == boundary:
            break


def validate_planning_replacement(entry: Path, boundary: Path) -> None:
    """Reject occupied or linked replacement paths before writing or retirement."""
    validate_retired_planning_entry(entry, boundary)
    if entry.is_symlink() or (entry.exists() and not entry.is_file()):
        raise OSError(f"Planning command replacement must be a regular file: {entry}")


def remove_retired_planning_entry(entry: Path, boundary: Path, *, remove_empty_parent: bool = False) -> None:
    """Remove only the retired entry; retain additional files in a skill directory."""
    validate_retired_planning_entry(entry, boundary)
    entry.unlink(missing_ok=True)
    if remove_empty_parent and entry.parent.is_dir() and not any(entry.parent.iterdir()):
        entry.parent.rmdir()


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

    replacement = templates_dir / "design-to-plan.md"
    retired_entry = target_dir / "spec-to-plan.md"
    replacement_entry = target_dir / replacement.name
    if replacement.is_file():
        validate_retired_planning_entry(retired_entry, target_dir)
        validate_planning_replacement(replacement_entry, target_dir)

    # Ensure target directory exists
    target_dir.mkdir(parents=True, exist_ok=True)

    if (templates_dir / "commit-staged.md").is_file():
        from codexspec.commit_guidance import install_plugin_commit_guidance
        from codexspec.commit_runtime import install_helper

        install_helper(target_dir)
        install_plugin_commit_guidance(target_dir)

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

    if replacement.is_file():
        validate_planning_replacement(replacement_entry, target_dir)
        if not replacement_entry.is_file():
            raise OSError(f"Planning command replacement was not installed: {replacement_entry}")
        remove_retired_planning_entry(retired_entry, target_dir)

    return installed_count


def update_installed_command_frontmatter(
    target_dir: Path,
    templates_dir: Path,
    language: str = "en",
    translations_dir: Optional[Path] = None,
) -> int:
    """Update frontmatter translations for already-installed command files.

    This preserves command bodies and any non-translated frontmatter while
    refreshing the language-specific ``description`` and ``argument-hint`` fields.
    Missing installed commands are intentionally skipped.
    """
    if not target_dir.exists() or not templates_dir.exists():
        return 0

    translation_cache = None
    if language != "en":
        translation_cache = load_translation_cache(language, translations_dir)

    updated_count = 0
    for template_file in templates_dir.glob("*.md"):
        target_path = target_dir / template_file.name
        if not target_path.exists():
            continue

        template_content = template_file.read_text(encoding="utf-8")
        template_name = template_file.stem
        rendered_template = translate_template_frontmatter(template_content, template_name, language, translation_cache)
        fields = {
            key: value for key, value in extract_frontmatter_fields(rendered_template).items() if value is not None
        }
        if not fields:
            continue

        current_content = target_path.read_text(encoding="utf-8")
        updated_content = apply_translations_to_template(current_content, fields)
        if updated_content != current_content:
            target_path.write_text(updated_content, encoding="utf-8")
            updated_count += 1

    return updated_count


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
