"""Init-wiring tests for profile consumption (T-002).

Scenario numbers refer to T-002 in
.codexspec/specs/2026-0812-14054p-profile-consumption/tasks.md.
"""

from pathlib import Path

from typer.testing import CliRunner

from codexspec import app
from codexspec.profile import PROFILE_BLOCK_START, PROFILE_FILES

runner = CliRunner()


def _init(target: Path, ai: str) -> None:
    # tmp_path already exists (pytest creates it), so --force is required.
    result = runner.invoke(app, ["init", str(target), "--ai", ai, "--no-git", "--force"])
    assert result.exit_code == 0, result.stdout


def test_init_claude_injects_import_profile_block(tmp_path: Path) -> None:
    """Scenario 1: project.ai=claude → CLAUDE.md has one PROFILE block using @import."""
    _init(tmp_path, "claude")
    claude_md = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert claude_md.count(PROFILE_BLOCK_START) == 1
    # constraints via @import within the block
    block = claude_md.split(PROFILE_BLOCK_START, 1)[1]
    assert "@.codexspec/profile/constraints.md" in block


def test_init_creates_profile_scaffold_unconditionally(tmp_path: Path) -> None:
    """Scenario 2: scaffold (dir + four files) exists even on an empty project."""
    _init(tmp_path, "claude")
    profile_dir = tmp_path / ".codexspec" / "profile"
    assert profile_dir.is_dir()
    for name in PROFILE_FILES:
        assert (profile_dir / name).exists()


def test_init_profile_block_after_compliance_import(tmp_path: Path) -> None:
    """Scenario 3: the PROFILE block does not clobber the constitution compliance @import."""
    _init(tmp_path, "claude")
    claude_md = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert "@.codexspec/memory/constitution.md" in claude_md  # compliance import preserved
    assert PROFILE_BLOCK_START in claude_md


def test_init_is_idempotent_outside_markers(tmp_path: Path) -> None:
    """Scenario 4: re-init updates the block in place; outside content byte-identical."""
    _init(tmp_path, "claude")
    claude_md = tmp_path / "CLAUDE.md"
    first = claude_md.read_text(encoding="utf-8")
    outside_first = first.split(PROFILE_BLOCK_START, 1)[0]

    result = runner.invoke(app, ["init", str(tmp_path), "--ai", "claude", "--no-git", "--force"])
    assert result.exit_code == 0, result.stdout

    second = claude_md.read_text(encoding="utf-8")
    assert second.count(PROFILE_BLOCK_START) == 1
    assert second.split(PROFILE_BLOCK_START, 1)[0] == outside_first


def test_init_preserves_existing_user_content(tmp_path: Path) -> None:
    """Scenario 5: an existing CLAUDE.md body is preserved; only the block is added."""
    tmp_path.mkdir(exist_ok=True)
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("# My Project\n\nMy own house rules.\n", encoding="utf-8")

    result = runner.invoke(app, ["init", str(tmp_path), "--ai", "claude", "--no-git", "--force"])
    assert result.exit_code == 0, result.stdout

    content = claude_md.read_text(encoding="utf-8")
    assert "My own house rules." in content
    assert content.count(PROFILE_BLOCK_START) == 1
