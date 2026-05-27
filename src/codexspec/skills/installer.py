"""Skill installer module for CodexSpec.

This module adapts the distributed command templates into Codex-compatible
skills by installing one `SKILL.md` per workflow command.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional, TypedDict

from codexspec.commands.installer import get_commands_metadata
from codexspec.translator import (
    extract_frontmatter_fields,
    load_translation_cache,
    translate_template_frontmatter,
)


class SkillMetadata(TypedDict):
    """Metadata for an installed Codex skill."""

    name: str
    description: str
    source_template: str


def get_skills_metadata() -> list[SkillMetadata]:
    """Return the Codex skill set derived from distributed command templates."""
    skills: list[SkillMetadata] = []
    for command in get_commands_metadata():
        skills.append(
            {
                "name": f"codexspec-{command['name']}",
                "description": command["description"],
                "source_template": command["file_name"],
            }
        )
    return skills


def _replace_frontmatter(content: str, frontmatter: str) -> str:
    """Replace leading YAML frontmatter while preserving the markdown body."""
    match = re.match(r"^---\n.*?\n---\n?", content, re.DOTALL)
    body = content[match.end() :] if match else content
    return f"---\n{frontmatter}\n---\n\n{body.lstrip()}"


def render_skill_content(template_content: str, skill_name: str) -> str:
    """Convert a command template into a Codex SKILL.md document."""
    fields = extract_frontmatter_fields(template_content)
    description = fields["description"] or skill_name
    frontmatter = "\n".join(
        [
            f"name: {skill_name}",
            f"description: {json.dumps(description, ensure_ascii=False)}",
        ]
    )
    return _replace_frontmatter(template_content, frontmatter)


def install_skills_from_templates(
    target_dir: Path,
    templates_dir: Path,
    force: bool = False,
    language: str = "en",
    translations_dir: Optional[Path] = None,
) -> int:
    """Install Codex skills by converting command templates into `SKILL.md` files."""
    if not templates_dir.exists():
        return 0

    target_dir.mkdir(parents=True, exist_ok=True)

    translation_cache = None
    if language != "en":
        translation_cache = load_translation_cache(language, translations_dir)

    installed_count = 0
    for template_file in templates_dir.glob("*.md"):
        translated = translate_template_frontmatter(
            template_file.read_text(encoding="utf-8"),
            template_file.stem,
            language,
            translation_cache,
        )

        skill_name = f"codexspec-{template_file.stem}"
        skill_dir = target_dir / skill_name
        skill_file = skill_dir / "SKILL.md"

        if skill_file.exists() and not force:
            continue

        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_file.write_text(render_skill_content(translated, skill_name), encoding="utf-8")
        installed_count += 1

    return installed_count
