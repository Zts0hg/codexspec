"""Tests for Codex integration support."""

import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from codexspec import app
from codexspec.integrations import get_integrations
from codexspec.integrations.codex import CodexIntegration

ROOT = Path(__file__).parent.parent
COMMANDS = ROOT / "templates" / "commands"


def test_codex_integration_renders_skill_from_template(tmp_path: Path) -> None:
    """Codex templates should render as SKILL.md files with $ invocations."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    (templates_dir / "specify.md").write_text(
        """---
description: Capture requirements
argument-hint: "Describe the requirement"
scripts:
  sh: .codexspec/scripts/create-new-feature.sh
---

## User Input

`$ARGUMENTS`

Next: /codexspec:generate-spec <feature-dir>
""",
        encoding="utf-8",
    )

    target = tmp_path / "project"
    target.mkdir()
    count = CodexIntegration().install_skills(target, templates_dir)

    assert count == 1
    skill_file = target / ".agents" / "skills" / "codexspec-specify" / "SKILL.md"
    assert skill_file.exists()

    content = skill_file.read_text(encoding="utf-8")
    assert "name: codexspec:specify" in content
    assert "description: Capture requirements" in content
    assert "argument-hint:" not in content
    assert "scripts:" not in content
    assert "$ARGUMENTS" not in content
    assert "/codexspec:" not in content
    assert "$codexspec:generate-spec" in content
    assert "text after the $codexspec:specify skill mention" in content


def test_codex_integration_renders_each_platform_script_command(tmp_path: Path) -> None:
    """Codex rendering should not replace PowerShell examples with sh commands."""
    template = """---
description: Capture requirements
scripts:
  sh: .codexspec/scripts/create-new-feature.sh
  ps: .codexspec/scripts/create-new-feature.ps1
---

Run:
- Bash: `{SCRIPT} --name "<feature-name>"`
- PowerShell: `{SCRIPT} -ShortName "<feature-name>" "<description>"`
"""

    content = CodexIntegration().render_skill("specify", template)

    assert 'Bash: `.codexspec/scripts/create-new-feature.sh --name "<feature-name>"`' in content
    assert (
        'PowerShell: `.codexspec/scripts/create-new-feature.ps1 -ShortName "<feature-name>" "<description>"`' in content
    )
    assert ".sh -ShortName" not in content


def test_codex_integration_renders_review_code_contract() -> None:
    """Codex strips command frontmatter while preserving the review protocol."""
    template = (COMMANDS / "review-code.md").read_text(encoding="utf-8")

    content = CodexIntegration().render_skill("review-code", template)

    assert "name: codexspec:review-code" in content
    assert "description: Review a selected change as a strict defect gate" in content
    assert "argument-hint:" not in content
    assert "scripts:" not in content
    assert "allowed-tools:" not in content
    assert "$ARGUMENTS" not in content
    assert "{SCRIPT}" not in content
    assert "the text after the $codexspec:review-code skill mention" in content
    assert ".codexspec/scripts/review-context.sh" in content
    assert ".codexspec/scripts/review-context.ps1" in content
    assert "$codexspec:review-code --audit {paths}" in content
    assert "/codexspec:review-code" not in content
    assert "missing resolver" in content
    assert "unsupported schema" in content
    assert "INCONCLUSIVE" in content


@pytest.mark.parametrize(
    ("ai", "expect_claude", "expect_codex"),
    [
        ("claude", True, False),
        ("codex", False, True),
        ("both", True, True),
    ],
)
def test_review_code_contract_installs_for_each_integration(
    tmp_path: Path,
    ai: str,
    expect_claude: bool,
    expect_codex: bool,
) -> None:
    """Every supported install shape receives the same fail-closed contract."""
    runner = CliRunner()

    result = runner.invoke(
        app,
        ["init", str(tmp_path / f"proj-{ai}"), "--ai", ai, "--no-git", "--lang", "en"],
    )

    assert result.exit_code == 0, result.stdout
    project = tmp_path / f"proj-{ai}"
    claude_command = project / ".claude" / "commands" / "codexspec" / "review-code.md"
    codex_skill = project / ".agents" / "skills" / "codexspec-review-code" / "SKILL.md"
    assert claude_command.exists() is expect_claude
    assert codex_skill.exists() is expect_codex

    for artifact in [path for path in [claude_command, codex_skill] if path.exists()]:
        content = artifact.read_text(encoding="utf-8")
        assert ".codexspec/scripts/review-context.sh" in content
        assert ".codexspec/scripts/review-context.ps1" in content
        assert "missing resolver" in content
        assert "unsupported schema" in content
        assert "update or re-run `codexspec init`" in content
        assert "MUST NOT reconstruct or guess Git scope" in content
        assert "{SCRIPT}" not in content

    if expect_claude:
        claude_content = claude_command.read_text(encoding="utf-8")
        assert "argument-hint:" in claude_content
        assert "scripts:" in claude_content
        assert "$ARGUMENTS" in claude_content
        assert "/codexspec:review-code --audit {paths}" in claude_content

    if expect_codex:
        codex_content = codex_skill.read_text(encoding="utf-8")
        assert "argument-hint:" not in codex_content
        assert "scripts:" not in codex_content
        assert "$ARGUMENTS" not in codex_content
        assert "$codexspec:review-code --audit {paths}" in codex_content

    local_script = "review-context.ps1" if sys.platform == "win32" else "review-context.sh"
    opposite_script = "review-context.sh" if local_script.endswith(".ps1") else "review-context.ps1"
    assert (project / ".codexspec" / "scripts" / local_script).exists()
    assert not (project / ".codexspec" / "scripts" / opposite_script).exists()


def test_codex_integration_upserts_agents_md_without_overwriting_user_content(tmp_path: Path) -> None:
    """AGENTS.md should keep user content and contain a managed CodexSpec section."""
    target = tmp_path / "project"
    target.mkdir()
    agents_md = target / "AGENTS.md"
    agents_md.write_text("# Project Notes\n\nKeep this paragraph.\n", encoding="utf-8")

    CodexIntegration().ensure_context_file(target)

    content = agents_md.read_text(encoding="utf-8")
    assert "# Project Notes" in content
    assert "Keep this paragraph." in content
    assert "<!-- CODEXSPEC START -->" in content
    assert "<!-- CODEXSPEC END -->" in content
    assert "$codexspec:specify" in content
    assert ".codexspec/memory/constitution.md" in content


def test_get_integrations_supports_both() -> None:
    """The registry should resolve both to Claude and Codex integrations."""
    integrations = get_integrations("both")

    assert [integration.key for integration in integrations] == ["claude", "codex"]


def test_init_ai_codex_installs_codex_skills_only(tmp_path: Path) -> None:
    """--ai codex should install Codex skills and avoid Claude command files."""
    runner = CliRunner()

    result = runner.invoke(app, ["init", str(tmp_path / "proj"), "--ai", "codex", "--no-git", "--lang", "en"])

    assert result.exit_code == 0, result.stdout
    project = tmp_path / "proj"
    assert (project / ".agents" / "skills" / "codexspec-specify" / "SKILL.md").exists()
    assert (project / "AGENTS.md").exists()
    assert not (project / ".claude" / "commands" / "codexspec").exists()
    assert ".claude/commands" not in result.stdout

    skill_content = (project / ".agents" / "skills" / "codexspec-quick" / "SKILL.md").read_text(encoding="utf-8")
    assert "$codexspec:generate-spec" in skill_content
    assert "/codexspec:" not in skill_content


def test_init_ai_both_installs_claude_commands_and_codex_skills(tmp_path: Path) -> None:
    """--ai both should install both target-specific entrypoints."""
    runner = CliRunner()

    result = runner.invoke(app, ["init", str(tmp_path / "proj"), "--ai", "both", "--no-git", "--lang", "en"])

    assert result.exit_code == 0, result.stdout
    project = tmp_path / "proj"
    assert (project / ".claude" / "commands" / "codexspec" / "specify.md").exists()
    assert (project / ".agents" / "skills" / "codexspec-specify" / "SKILL.md").exists()
    assert (project / "CLAUDE.md").exists()
    assert (project / "AGENTS.md").exists()
