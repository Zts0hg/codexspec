"""Reuse installed release renderers in temporary output, not a user's checkout."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from .metadata import checked_path, managed_path


def render_installation(project: Path, ai: str, language: str) -> dict[str, bytes]:
    from codexspec import (
        _get_claude_md_content,
        get_scripts_dir,
        get_templates_dir,
        has_compliance_section,
        prepend_compliance_section,
    )
    from codexspec.commands.installer import install_commands_to_subdir
    from codexspec.commit_guidance import inject_commit_guidance
    from codexspec.commit_runtime import install_helper
    from codexspec.distill_review.session import ensure_runtime_ignored
    from codexspec.integrations import get_integrations
    from codexspec.profile import inject_profile_block
    from codexspec.review_standards import install_review_standards
    from codexspec.specs_context import inject_specs_context

    integrations = get_integrations(ai)
    templates = get_templates_dir()
    scripts = get_scripts_dir() / ("powershell" if sys.platform == "win32" else "bash")
    if not (templates / "commands").is_dir() or not scripts.is_dir() or not (templates / "docs").is_dir():
        raise ValueError("release installation resources are incomplete")
    command_sources = list((templates / "commands").glob("*.md"))
    script_sources = list(scripts.glob("*.ps1" if sys.platform == "win32" else "*.sh"))
    doc_sources = list((templates / "docs").glob("*.md"))
    if not command_sources or not script_sources or not doc_sources:
        raise ValueError("release installation resources are empty")
    expected_paths = {".codexspec/scripts/commit-staged-helper.py", ".codexspec/.gitignore"}
    expected_paths.update(f".codexspec/scripts/{source.name}" for source in script_sources)
    expected_paths.update(f".codexspec/templates/docs/{source.name}" for source in doc_sources)
    if ai in {"claude", "both"}:
        expected_paths.add("CLAUDE.md")
        expected_paths.update(f".claude/commands/codexspec/{source.name}" for source in command_sources)
    if ai in {"codex", "both"}:
        expected_paths.add("AGENTS.md")
        expected_paths.update(f".agents/skills/codexspec-{source.stem}/SKILL.md" for source in command_sources)
    with tempfile.TemporaryDirectory(prefix="codexspec-render-") as temporary:
        output = Path(temporary).resolve()
        for name in ("CLAUDE.md", "AGENTS.md", ".codexspec/.gitignore"):
            original = checked_path(project, name)
            if original.exists():
                destination = output / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(original.read_bytes())
        for integration in integrations:
            if integration.key == "claude":
                install_commands_to_subdir(
                    output / ".claude/commands/codexspec", templates / "commands", force=True, language=language
                )
                context = output / "CLAUDE.md"
                if not context.exists():
                    context.write_text(_get_claude_md_content(project.name), encoding="utf-8")
                elif not has_compliance_section(context):
                    prepend_compliance_section(context)
                inject_profile_block(context)
                inject_commit_guidance(context, "/codexspec:commit-staged")
                inject_specs_context(context)
            else:
                integration.install(output, templates / "commands", force=True, language=language)
        script_output = output / ".codexspec/scripts"
        script_output.mkdir(parents=True, exist_ok=True)
        install_helper(script_output)
        extension = "*.ps1" if sys.platform == "win32" else "*.sh"
        for source in scripts.glob(extension):
            (script_output / source.name).write_bytes(source.read_bytes())
        docs_output = output / ".codexspec/templates/docs"
        docs_output.mkdir(parents=True, exist_ok=True)
        for source in (templates / "docs").glob("*.md"):
            (docs_output / source.name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
        install_review_standards(templates / "review-code", output, force=True)
        ensure_runtime_ignored(output, install_managed_file=True)
        files = {}
        for path in output.rglob("*"):
            if not path.is_file():
                continue
            name = path.relative_to(output).as_posix()
            if name == "CLAUDE.md" and ai == "codex" or name == "AGENTS.md" and ai == "claude":
                continue
            if managed_path(name):
                files[name] = path.read_bytes()
        missing = expected_paths - files.keys()
        if missing:
            raise ValueError(f"release rendering is incomplete: {', '.join(sorted(missing))}")
        return files
