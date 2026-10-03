"""Workspace handoff contracts across distributed agent entry points."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "internal/command_templates/sources"


def test_s030_all_commands_include_routing():
    sources = list(SOURCES.glob("*.md"))
    assert sources
    for source in sources:
        assert "<!-- CODEXSPEC:INCLUDE workspace-routing.md -->" in source.read_text(encoding="utf-8"), source.name
    for name in ("specify", "quick"):
        text = (SOURCES / f"{name}.md").read_text(encoding="utf-8")
        assert "workspace" in text and "requirements.md" in text


def test_s031_s032_s033_common_contract_has_exceptions_and_provenance():
    fragment = (ROOT / "internal/command_templates/fragments/workspace-routing.md").read_text(encoding="utf-8")
    for contract in (
        "workflow.worktrees",
        "SOURCE_ROOT",
        "OUTPUT_ROOT",
        "CODEXSPEC_AUTO_DEV_DELEGATION",
        "_worktree-helper",
        "merge_requires_verification",
        "init",
        "commit-staged",
        "checkout-local",
        "worktree-for-codexspec-maintenance",
    ):
        assert contract in fragment, contract
    assert "Do not copy, stash, stage, reset, or discard" in fragment
    config = (SOURCES / "config.md").read_text(encoding="utf-8")
    assert "--worktrees" in config and "Git integration" in config


def test_s029_powershell_checks_setting_before_mutation():
    text = (ROOT / "scripts/powershell/create-new-feature.ps1").read_text(encoding="utf-8")
    assert text.index("_worktree-helper setting") < text.index("$specsDir = Join-Path")
    assert "WORKTREE_PATH = $workspace.workspace" in text
    assert "if ($workspaceExit -ne 0)" in text
