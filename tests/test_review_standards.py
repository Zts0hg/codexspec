"""Shared review resources survive installation and update byte-for-byte."""

import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

import codexspec
from codexspec.automation import AutomationError
from codexspec.review_standards import install_review_standards

ROOT = Path(__file__).resolve().parent.parent


def source(tmp_path):
    root = tmp_path / "source"
    root.mkdir()
    (root / "index.md").write_bytes(b"# Index\n")
    (root / "common.md").write_bytes("# 通用\n".encode())
    (root / "dimensions").mkdir()
    (root / "dimensions/logic.md").write_bytes(b"# Logic\n")
    return root


def test_d01_byte_identical_copy(tmp_path):
    src = source(tmp_path)
    project = tmp_path / "project"
    assert install_review_standards(src, project) == 3
    for path in src.rglob("*.md"):
        assert (project / ".codexspec/review-code" / path.relative_to(src)).read_bytes() == path.read_bytes()


def test_d02_preserve_then_refresh(tmp_path):
    src = source(tmp_path)
    project = tmp_path / "project"
    install_review_standards(src, project)
    installed = project / ".codexspec/review-code"
    (installed / "common.md").write_bytes(b"project edit")
    (installed / "custom.md").write_bytes(b"extension")
    install_review_standards(src, project)
    assert (installed / "common.md").read_bytes() == b"project edit"
    install_review_standards(src, project, force=True)
    assert (installed / "common.md").read_bytes() == (src / "common.md").read_bytes()
    assert (installed / "custom.md").read_bytes() == b"extension"


@pytest.mark.parametrize("link", ["symlink", "hardlink"])
def test_d03_unsafe_destination_preflight(tmp_path, link):
    src = source(tmp_path)
    project = tmp_path / "project"
    installed = project / ".codexspec/review-code"
    installed.mkdir(parents=True)
    victim = tmp_path / "victim.md"
    victim.write_bytes(b"preserve")
    try:
        if link == "symlink":
            (installed / "index.md").symlink_to(victim)
        else:
            os.link(victim, installed / "index.md")
    except OSError:
        pytest.skip("links unavailable on this host")
    with pytest.raises((AutomationError, ValueError)):
        install_review_standards(src, project, force=True)
    assert victim.read_bytes() == b"preserve"
    assert not (installed / "common.md").exists()


@pytest.mark.parametrize("ai", ["claude", "codex", "both"])
def test_d04_real_init_shares_resources(tmp_path, ai):
    result = CliRunner().invoke(
        codexspec.app,
        [
            "init",
            str(tmp_path / "project"),
            "--force",
            "--ai",
            ai,
            "--lang",
            "en",
            "--no-git",
        ],
    )
    assert result.exit_code == 0, result.output
    src = ROOT / "templates/review-code"
    assert (src / "index.md").is_file()
    for path in src.rglob("*.md"):
        target = tmp_path / "project/.codexspec/review-code" / path.relative_to(src)
        assert target.read_bytes() == path.read_bytes()


def test_c01_index_paths_and_loading_units():
    import re

    resources = ROOT / "templates/review-code"
    index = (resources / "index.md").read_text(encoding="utf-8")
    paths = re.findall(r"^\| [^|]+ \| ([a-zA-Z0-9/.-]+\.md) \|", index, re.MULTILINE)
    assert paths
    for relative in paths:
        path = resources / relative
        assert path.resolve().is_relative_to(resources.resolve())
        assert path.is_file(), relative
    entry = (ROOT / "templates/commands/review-code.md").read_text(encoding="utf-8")
    assert "Runtime Standards Loading" in entry
    for path in ["common.md", "change-review.md", "quality-assessment.md"]:
        assert path in entry
    for body in ["### Stage 1: Scope Pass", "### Scoring Rubrics", "### GO-EXEC"]:
        assert body not in entry
    for directory in ["topics", "languages/go"]:
        assert not (resources / directory).exists()
    dimensions = resources / "dimensions"
    assert {p.stem for p in dimensions.glob("*.md")} == {
        "logic",
        "business-semantics",
        "security",
        "concurrency",
        "robustness",
        "performance",
        "maintainability",
    }
    for path in dimensions.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for contract in ["Applicability", "Non-Applicability", "Necessary Evidence", "Completion", "Checkpoints"]:
            assert contract in text


def test_c01_source_items_retain_concrete_destinations():
    import re

    feature = ROOT / ".codexspec/specs/2026-1011-105126-review-code-standards/references"
    original = (feature / "review-dimensions.original.txt").read_text(encoding="utf-8")
    mapping = (feature / "checklist-integration.md").read_text(encoding="utf-8")
    bullets = [(i, line[2:]) for i, line in enumerate(original.splitlines(), 1) if line.startswith("- ")]
    rows = [line for line in mapping.splitlines() if line.startswith("| SRC-")]
    assert len(rows) == len(bullets) == 87
    for ordinal, ((line_number, intent), row) in enumerate(zip(bullets, rows), 1):
        assert f"SRC-{ordinal:03d}" in row and f"| {line_number} |" in row
        assert intent.replace("|", "\\|") in row
        destinations = re.findall(r"(templates/review-code/[a-z/.-]+\.md)(?:#([a-z0-9-]+))?", row)
        assert destinations
        for relative, anchor in destinations:
            path = ROOT / relative
            text = path.read_text(encoding="utf-8")
            if anchor:
                assert re.search(r"^### " + re.escape(anchor) + r"$", text, re.MULTILINE | re.IGNORECASE)


def test_c02_caller_consumes_policy_and_companion_without_forwarding():
    caller = (ROOT / "templates/commands/implement-tasks.md").read_text(encoding="utf-8")
    assert "workflow.auto_maintenance" in caller
    assert "parse_maintenance_result" in caller
    assert "read_auto_maintenance" in caller
    assert "no unfinished independently verified maintenance" in caller
    assert "no per-run override" in caller
    assert "reported_only" in caller
    review = (ROOT / "templates/review-code/change-review.md").read_text(encoding="utf-8")
    assert "Maintenance alone never changes finding counts" in review
    assert '"schema_version": "3"' in review
    assert "target_fingerprint" in review
    assert "missing/duplicate blocks" in review
    for name in ["quick", "auto-dev", "plan-to-tasks", "generate-spec"]:
        text = (ROOT / f"templates/commands/{name}.md").read_text(encoding="utf-8")
        assert "--auto-maintenance" not in text


def test_c02_plugin_root_contains_resources_and_commands():
    assert (ROOT / ".claude/commands/codexspec").is_dir()
    assert (ROOT / ".claude/commands/codexspec/hooks/hooks.json").is_file()
    assert (ROOT / "templates/review-code/index.md").is_file()


def test_marketplace_layout_matches_selected_release():
    import json

    entry = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))["plugins"][0]
    assert entry["source"]["ref"] == f"v{entry['version']}"
    if entry["source"]["ref"] == "v0.7.23":
        # This immutable release's command resolves its helper at the plugin
        # root, so changing only the root while retaining this tag breaks it.
        assert entry["source"].get("path") == ".claude/commands/codexspec"
        assert entry["commands"] == "./"
        assert entry.get("hooks") in (None, "./hooks/hooks.json")
    else:
        assert "path" not in entry["source"]
        assert entry["commands"] == ["./.claude/commands/codexspec/"]
        assert entry["hooks"] == "./.claude/commands/codexspec/hooks/hooks.json"


@pytest.mark.parametrize("force", [False, True])
@pytest.mark.parametrize("relative", ["index.md", "dimensions/logic.md"])
def test_d05_nonfile_destination_preflight_preserves_group(tmp_path, force, relative):
    src = source(tmp_path)
    project = tmp_path / "project"
    installed = project / ".codexspec/review-code"
    occupied = installed / relative
    occupied.mkdir(parents=True)
    (occupied / "owned.txt").write_bytes(b"project-owned content")

    def snapshot():
        return {
            path.relative_to(installed): path.read_bytes() if path.is_file() else None for path in installed.rglob("*")
        }

    before = snapshot()
    with pytest.raises(AutomationError, match="unsafe_write_path"):
        install_review_standards(src, project, force=force)
    assert snapshot() == before


def test_d06_init_reports_nonfile_standard_destination_before_copy(tmp_path):
    project = tmp_path / "project"
    installed = project / ".codexspec/review-code"
    occupied = installed / "index.md"
    occupied.mkdir(parents=True)
    (occupied / "owned.txt").write_bytes(b"project-owned content")

    result = CliRunner().invoke(
        codexspec.app,
        ["init", str(project), "--force", "--ai", "both", "--lang", "en", "--no-git"],
    )

    assert result.exit_code == 1, result.output
    assert "unsafe_write_path" in result.output
    assert occupied.is_dir()
    assert (occupied / "owned.txt").read_bytes() == b"project-owned content"
    assert not (installed / "common.md").exists()
