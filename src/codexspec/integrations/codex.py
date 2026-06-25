"""Codex CLI integration."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

from codexspec.commands.installer import get_commands_metadata
from codexspec.translator import load_translation_cache, translate_template_frontmatter

CODEXSPEC_CONTEXT_START = "<!-- CODEXSPEC START -->"
CODEXSPEC_CONTEXT_END = "<!-- CODEXSPEC END -->"


class CodexIntegration:
    """Installs CodexSpec as Codex skills."""

    key = "codex"
    display_name = "Codex CLI"
    context_file = "AGENTS.md"

    def invocation_for(self, command_name: str) -> str:
        """Return the Codex skill mention invocation."""
        return f"$codexspec:{command_name}"

    def skills_dir(self, target_dir: Path) -> Path:
        """Return the Codex skills destination."""
        return target_dir / ".agents" / "skills"

    def install(self, target_dir: Path, templates_dir: Path, *, force: bool = False, language: str = "en") -> int:
        """Install Codex skills and the Codex context file."""
        count = self.install_skills(target_dir, templates_dir, force=force, language=language)
        self.ensure_context_file(target_dir)
        return count

    def install_skills(
        self,
        target_dir: Path,
        templates_dir: Path,
        *,
        force: bool = False,
        language: str = "en",
    ) -> int:
        """Render command templates into Codex SKILL.md files."""
        if not templates_dir.exists():
            return 0

        descriptions = {cmd["file_name"]: cmd["description"] for cmd in get_commands_metadata()}
        translation_cache = None
        if language != "en":
            translation_cache = load_translation_cache(language)

        installed_count = 0
        for template_file in sorted(templates_dir.glob("*.md")):
            command_name = template_file.stem
            skill_dir = self.skills_dir(target_dir) / f"codexspec-{command_name}"
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists() and not force:
                continue

            content = template_file.read_text(encoding="utf-8")
            content = translate_template_frontmatter(content, command_name, language, translation_cache)
            skill_content = self.render_skill(command_name, content, descriptions.get(template_file.name, ""))
            skill_dir.mkdir(parents=True, exist_ok=True)
            skill_file.write_text(skill_content, encoding="utf-8")
            installed_count += 1

        return installed_count

    def ensure_context_file(self, target_dir: Path) -> None:
        """Create or update AGENTS.md with a managed CodexSpec section."""
        context_path = target_dir / self.context_file
        existing = context_path.read_text(encoding="utf-8") if context_path.exists() else ""
        section = self._context_section()

        pattern = re.compile(
            rf"{re.escape(CODEXSPEC_CONTEXT_START)}.*?{re.escape(CODEXSPEC_CONTEXT_END)}",
            re.DOTALL,
        )
        if pattern.search(existing):
            updated = pattern.sub(section.strip(), existing)
        elif existing.strip():
            updated = existing.rstrip() + "\n\n" + section
        else:
            updated = "# AGENTS.md\n\n" + section

        context_path.write_text(updated, encoding="utf-8")

    def render_skill(self, command_name: str, content: str, fallback_description: str = "") -> str:
        """Render one command template into a Codex SKILL.md."""
        frontmatter, body = _split_frontmatter(content)
        description = str(frontmatter.get("description") or fallback_description or f"CodexSpec {command_name}")
        body = _render_script_placeholders(body, frontmatter)
        body = _render_codex_body(command_name, body)

        return f"---\nname: codexspec:{command_name}\ndescription: {_yaml_scalar(description)}\n---\n\n{body.strip()}\n"

    def _context_section(self) -> str:
        return f"""{CODEXSPEC_CONTEXT_START}
## CodexSpec

This project uses CodexSpec for requirements-first spec-driven development.

Use these Codex skills when working on CodexSpec workflows:

- `$codexspec:constitution` to create or update project principles.
- `$codexspec:specify` to capture confirmed requirements.
- `$codexspec:generate-spec` to produce `spec.md`.
- `$codexspec:spec-to-plan` to produce `plan.md`.
- `$codexspec:plan-to-tasks` to produce `tasks.md`.
- `$codexspec:implement-tasks` to implement approved tasks.

Before making workflow decisions, read `.codexspec/memory/constitution.md`.
{CODEXSPEC_CONTEXT_END}
"""


def _split_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        parsed = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        parsed = {}
    if not isinstance(parsed, dict):
        parsed = {}
    return parsed, parts[2]


def _render_script_placeholders(body: str, frontmatter: dict[str, Any]) -> str:
    scripts = frontmatter.get("scripts")
    if not isinstance(scripts, dict):
        return body
    preferred = "ps" if sys.platform == "win32" else "sh"
    default_command = str(scripts.get(preferred) or scripts.get("sh") or scripts.get("ps") or "")
    sh_command = str(scripts.get("sh") or default_command)
    ps_command = str(scripts.get("ps") or default_command)

    lines: list[str] = []
    for line in body.splitlines(keepends=True):
        if "{SCRIPT}" not in line:
            lines.append(line)
        elif "PowerShell:" in line:
            lines.append(line.replace("{SCRIPT}", ps_command))
        elif "Bash:" in line:
            lines.append(line.replace("{SCRIPT}", sh_command))
        else:
            lines.append(line.replace("{SCRIPT}", default_command))
    return "".join(lines)


def _render_codex_body(command_name: str, body: str) -> str:
    arg_text = f"the text after the $codexspec:{command_name} skill mention"
    body = body.replace("$ARGUMENTS", arg_text)
    body = body.replace("{ARGS}", arg_text)
    return re.sub(r"/codexspec:([A-Za-z0-9-]+)", r"$codexspec:\1", body)


def _yaml_scalar(value: str) -> str:
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 _.,:/()'\"-]*", value):
        return value
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'
