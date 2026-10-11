"""Marketplace-only installs load the same commit rule without project init."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from codexspec.commands.installer import install_commands_to_subdir
from tests.automation_test_support import git, make_repo

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("installation", ["plugin", "init"])
@pytest.mark.parametrize("repository", [False, True])
def test_session_start_emits_commit_rule_without_cli(tmp_path, installation, repository):
    from codexspec.commit_guidance import render_commit_guidance

    plugin = tmp_path / "plugin cache ' $ space"
    if installation == "plugin":
        manifest = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        assert manifest["plugins"][0]["commands"] == "./"
        shutil.copytree(ROOT / manifest["plugins"][0]["source"]["path"], plugin)
        assert (plugin / "commit-staged.md").is_file()
    else:
        install_commands_to_subdir(plugin, ROOT / "templates/commands", force=True)
    project = tmp_path / "project"
    if repository:
        make_repo(project)
        (project / "README.md").write_text("staged\n")
        git(project, "add", "README.md")
        before = git(project, "write-tree").stdout, git(project, "rev-parse", "HEAD").stdout
    else:
        project.mkdir()
    original = {p.relative_to(project): p.read_bytes() for p in project.rglob("*") if p.is_file()}
    config = json.loads((plugin / "hooks/hooks.json").read_text())
    handlers = config["hooks"]["SessionStart"]
    assert len(handlers) == 1 and handlers[0].get("matcher", "") == ""
    (hook,) = handlers[0]["hooks"]
    env = os.environ.copy()
    env["PATH"] = os.pathsep.join([str(Path(shutil.which("git")).parent), os.defpath])
    assert shutil.which("codexspec", path=env["PATH"]) is None
    result = subprocess.run(
        [hook["command"], *hook["args"]],
        cwd=project,
        env=env,
        input='{"source":"startup"}',
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == render_commit_guidance("/codexspec:commit-staged") + "\n"
    assert "Before creating an authorized Git commit" in result.stdout
    assert "Command\navailability alone is not an invocation" in result.stdout
    assert {p.relative_to(project): p.read_bytes() for p in project.rglob("*") if p.is_file()} == original
    if repository:
        assert (git(project, "write-tree").stdout, git(project, "rev-parse", "HEAD").stdout) == before


@pytest.mark.parametrize("link", ["file", "directory", "hardlink"])
def test_plugin_hook_install_rejects_shared_destination(tmp_path, link):
    from codexspec.commit_guidance import install_plugin_commit_guidance
    from codexspec.commit_runtime import AutomationError

    outside = tmp_path / "outside"
    outside.mkdir()
    sentinel = outside / "hooks.json"
    sentinel.write_text("caller-owned")
    plugin = tmp_path / "plugin"
    plugin.mkdir()
    if link == "directory":
        (plugin / "hooks").symlink_to(outside, target_is_directory=True)
    else:
        (plugin / "hooks").mkdir()
        target = plugin / "hooks/hooks.json"
        if link == "hardlink":
            os.link(sentinel, target)
        else:
            target.symlink_to(sentinel)
    with pytest.raises(AutomationError, match="linked_commit_guidance|shared_commit_guidance"):
        install_plugin_commit_guidance(plugin)
    assert sentinel.read_text() == "caller-owned"
