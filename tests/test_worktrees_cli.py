"""CLI contracts for workspace routing and checkout-local configuration."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

import codexspec
from codexspec.worktrees import WorkspaceManager, read_worktrees
from tests.test_worktrees import FEATURE, configured, diverged, evidence

runner = CliRunner()


def test_s020_helper_paths_and_finish(tmp_path, monkeypatch):
    repo = configured(tmp_path / "repo")
    monkeypatch.chdir(repo)
    result = runner.invoke(codexspec.app, ["_worktree-helper", "create", "--name", "new feature"])
    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    assert data["status"] == "ready" and Path(data["requirements_file"]).is_file()
    resolved = runner.invoke(codexspec.app, ["_worktree-helper", "resolve", "--feature", data["branch"]])
    assert json.loads(resolved.output)["workspace"] == data["workspace"]
    bad = runner.invoke(codexspec.app, ["_worktree-helper", "resolve", "--feature", "../bad"])
    assert bad.exit_code != 0 and "invalid_feature_name" in bad.output


def test_s020_finish_cli(tmp_path, monkeypatch):
    repo, _, _ = diverged(tmp_path)
    monkeypatch.chdir(repo)
    result = WorkspaceManager(repo).create(FEATURE)
    proof = tmp_path / "proof.json"
    proof.write_text(json.dumps(evidence(Path(result["workspace"]))))
    result = runner.invoke(
        codexspec.app, ["_worktree-helper", "finish", "--feature", FEATURE, "--verification", str(proof)]
    )
    assert result.exit_code == 0 and json.loads(result.output)["status"] == "ready"


def test_s021_checkout_local_routed_config_and_toggle(tmp_path, monkeypatch):
    repo = configured(tmp_path / "repo")
    monkeypatch.chdir(repo)
    result = runner.invoke(codexspec.app, ["config", "--worktrees", "off"])
    assert result.exit_code == 0, result.output
    dest = Path(str(repo) + "-codexspec-worktrees") / "worktree-for-codexspec-maintenance"
    assert read_worktrees(repo / ".codexspec/config.yml")
    assert not read_worktrees(dest / ".codexspec/config.yml")
    assert str(dest) in result.output
    result = runner.invoke(codexspec.app, ["config", "--worktrees=__toggle_worktrees__"])
    assert result.exit_code == 0 and read_worktrees(dest / ".codexspec/config.yml")
    assert read_worktrees(repo / ".codexspec/config.yml")


def test_s022_display_optout_and_feature_config(tmp_path, monkeypatch):
    repo = configured(tmp_path / "repo", False)
    monkeypatch.chdir(repo)
    before = (repo / ".codexspec/config.yml").read_bytes()
    assert runner.invoke(codexspec.app, ["config"]).exit_code == 0
    assert (repo / ".codexspec/config.yml").read_bytes() == before
    assert not Path(str(repo) + "-codexspec-worktrees").exists()
    assert runner.invoke(codexspec.app, ["config", "--set-document-lang", "zh-CN"]).exit_code == 0
    assert "zh-CN" in (repo / ".codexspec/config.yml").read_text()
    feature = Path(WorkspaceManager(repo).create(FEATURE)["workspace"])
    monkeypatch.chdir(feature)
    assert runner.invoke(codexspec.app, ["config", "--auto-next", "on"]).exit_code == 0
    assert "auto_next: true" in (feature / ".codexspec/config.yml").read_text()
    assert "auto_next: true" not in (repo / ".codexspec/config.yml").read_text()


def test_s023_mutable_review_is_routed_before_session(tmp_path, monkeypatch):
    from codexspec.distill_review.session import SessionError
    from tests.automation_test_support import git

    repo = configured(tmp_path / "repo")
    profile = repo / ".codexspec/profile"
    profile.mkdir()
    (profile / ".gitkeep").write_text("")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "profile")
    seen = []

    class ProbeLease:
        def __init__(self, root):
            seen.append(root)

        def acquire(self, metadata):
            raise SessionError("probe stopped before writes")

    monkeypatch.setattr(codexspec, "ReviewLease", ProbeLease)
    result = runner.invoke(codexspec.app, ["_distill-review-helper", "--project-root", str(repo), "--mode", "text"])
    assert result.exit_code == 2 and seen
    assert seen[0].name == "worktree-for-codexspec-maintenance"
    assert not (repo / ".codexspec/profile/.runtime").exists()


def test_s024_init_first_and_update_are_exempt(tmp_path):
    target = tmp_path / "project"
    args = ["init", str(target), "--ai", "codex", "--lang", "en", "--no-git"]
    first = runner.invoke(codexspec.app, args)
    assert first.exit_code == 0, first.output
    config = target / ".codexspec/config.yml"
    before = config.read_bytes()
    second = runner.invoke(codexspec.app, args + ["--force"])
    assert second.exit_code == 0, second.output
    assert config.read_bytes() == before
    assert not Path(str(target) + "-codexspec-worktrees").exists()


def test_s025_missing_repository_cannot_write(tmp_path, monkeypatch):
    cfg = tmp_path / ".codexspec/config.yml"
    cfg.parent.mkdir()
    cfg.write_text("workflow:\n  worktrees: true\n")
    monkeypatch.chdir(tmp_path)
    before = cfg.read_bytes()
    result = runner.invoke(codexspec.app, ["config", "--worktrees", "off"])
    assert result.exit_code != 0 and cfg.read_bytes() == before


def test_s025_nonready_maintenance_blocks_config_and_review(tmp_path, monkeypatch):
    repo, _, _ = diverged(tmp_path)
    (repo / ".codexspec/profile").mkdir()
    monkeypatch.chdir(repo)
    original = (repo / ".codexspec/config.yml").read_bytes()
    result = runner.invoke(codexspec.app, ["config", "--worktrees", "off"])
    assert result.exit_code != 0 and "merge_requires_verification" in result.output
    dest = Path(str(repo) + "-codexspec-worktrees") / "worktree-for-codexspec-maintenance"
    assert (repo / ".codexspec/config.yml").read_bytes() == original
    assert (dest / ".codexspec/config.yml").read_bytes() == original
    result = runner.invoke(codexspec.app, ["_distill-review-helper", "--project-root", str(repo), "--mode", "text"])
    assert result.exit_code != 0
    assert not (repo / ".codexspec/profile/.runtime").exists()
    assert not (dest / ".codexspec/profile/.runtime").exists()


@pytest.mark.parametrize("bare_layout", [False, True])
def test_s035_end_to_end_shared_parent_and_retained_feature(tmp_path, monkeypatch, bare_layout):
    from codexspec.automation import ensure_dedicated_workspace, locate_repository
    from codexspec.worktrees import write_destination, write_worktrees
    from tests.automation_test_support import git, make_bare_remote

    main = configured(tmp_path / "main")
    primary = main
    if bare_layout:
        primary = make_bare_remote(tmp_path / "repo.git", main).resolve()
        main = (tmp_path / "linked-main").resolve()
        git(primary, "worktree", "add", str(main), "main")
    before = git(main, "status", "--porcelain").stdout
    monkeypatch.chdir(main)
    result = runner.invoke(codexspec.app, ["_worktree-helper", "create", "--name", "e2e"])
    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    feature = Path(data["workspace"])
    assert feature.parent == Path(str(primary) + "-codexspec-worktrees")
    assert write_destination(feature) == feature
    Path(data["requirements_file"]).write_text("confirmed\n")
    resolved = WorkspaceManager(main).resolve(data["branch"])
    assert resolved["workspace"] == str(feature)
    maintenance = write_destination(main)
    assert maintenance.parent == feature.parent
    write_worktrees(main / ".codexspec/config.yml", False)
    automatic = ensure_dedicated_workspace(locate_repository(main))
    assert automatic.path.parent == feature.parent
    assert automatic.path.name == "worktree-for-codexspec-auto-dev"
    assert write_destination(automatic.path) == automatic.path
    write_worktrees(main / ".codexspec/config.yml", True)
    assert git(main, "status", "--porcelain").stdout == before
    assert git(main, "branch", "--show-current").stdout.strip() == "main"
    assert Path(resolved["requirements_file"]).read_text() == "confirmed\n"


def test_s004_nested_helper_honors_checkout_optout(tmp_path, monkeypatch):
    repo = configured(tmp_path / "repo", False)
    monkeypatch.chdir(repo / ".codexspec")
    result = runner.invoke(codexspec.app, ["_worktree-helper", "setting"])
    assert result.exit_code == 0 and json.loads(result.output)["enabled"] is False
    result = runner.invoke(codexspec.app, ["_worktree-helper", "create", "--name", "nested"])
    assert result.exit_code == 0 and json.loads(result.output)["status"] == "disabled"
    assert not Path(str(repo) + "-codexspec-worktrees").exists()


def test_s020_resume_interrupted_creation_by_returned_identity(tmp_path, monkeypatch):
    from tests.test_worktrees import InterruptedCreation

    repo = configured(tmp_path / "repo")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(codexspec, "feature_name", lambda _: FEATURE)
    original = codexspec.WorkspaceManager
    monkeypatch.setattr(
        codexspec, "WorkspaceManager", lambda root: original(root, runner=InterruptedCreation("before_add"))
    )
    failed = runner.invoke(codexspec.app, ["_worktree-helper", "create", "--name", "resume"])
    assert failed.exit_code == 1, failed.output
    data = json.loads(failed.output)
    assert data["branch"] == FEATURE
    monkeypatch.setattr(codexspec, "WorkspaceManager", original)
    done = runner.invoke(codexspec.app, ["_worktree-helper", "create", "--feature", data["branch"]])
    assert done.exit_code == 0, done.output
    assert json.loads(done.output)["branch"] == FEATURE


def test_new_feature_name_collision_does_not_adopt_existing_feature(tmp_path, monkeypatch):
    repo = configured(tmp_path / "repo")
    previous = WorkspaceManager(repo).create(FEATURE)
    Path(previous["requirements_file"]).write_text("existing feature\n")
    monkeypatch.chdir(repo)
    monkeypatch.setattr(codexspec, "feature_name", lambda _: FEATURE)
    result = runner.invoke(codexspec.app, ["_worktree-helper", "create", "--name", "new"])
    assert result.exit_code == 1 and "feature_identity_collision" in result.output
    assert Path(previous["requirements_file"]).read_text() == "existing feature\n"


@pytest.mark.parametrize("option", ["--set-lang", "--set-interaction-lang"])
def test_language_routing_includes_command_frontmatter(tmp_path, monkeypatch, option):
    from tests.automation_test_support import git

    repo = configured(tmp_path / "repo")
    command = Path(".claude/commands/codexspec/specify.md")
    (repo / command).parent.mkdir(parents=True)
    (repo / command).write_bytes((codexspec.get_templates_dir() / "commands/specify.md").read_bytes())
    git(repo, "add", ".")
    git(repo, "commit", "-m", "install command")
    original = (repo / command).read_bytes()
    monkeypatch.chdir(repo)
    result = runner.invoke(codexspec.app, ["config", option, "zh-CN"])
    assert result.exit_code == 0, result.output
    destination = Path(str(repo) + "-codexspec-worktrees") / "worktree-for-codexspec-maintenance"
    assert (repo / command).read_bytes() == original
    assert (destination / command).read_bytes() != original
    assert git(repo, "status", "--porcelain").stdout == ""


@pytest.mark.parametrize("link_kind", ["directory", "config"])
@pytest.mark.parametrize(
    "option,value",
    [
        ("--worktrees", "off"),
        ("--auto-next", "on"),
        ("--auto-distill", "off"),
        ("--set-lang", "zh-CN"),
        ("--set-interaction-lang", "zh-CN"),
        ("--set-document-lang", "zh-CN"),
        ("--set-commit-lang", "zh-CN"),
    ],
)
def test_config_rejects_destination_symlinks(tmp_path, monkeypatch, link_kind, option, value):
    import shutil

    from codexspec.worktrees import write_destination

    repo = configured(tmp_path / "repo")
    dest = write_destination(repo)
    relative = ".codexspec" if link_kind == "directory" else ".codexspec/config.yml"
    target = dest / relative
    if target.is_dir():
        shutil.rmtree(target)
    else:
        target.unlink()
    try:
        target.symlink_to(repo / relative, target_is_directory=link_kind == "directory")
    except OSError:
        pytest.skip("symlink creation requires platform support")
    original = (repo / ".codexspec/config.yml").read_bytes()
    monkeypatch.chdir(repo)
    result = runner.invoke(codexspec.app, ["config", option, value])
    assert result.exit_code != 0, result.output
    assert (repo / ".codexspec/config.yml").read_bytes() == original


@pytest.mark.parametrize("relative", [".claude", ".claude/commands/codexspec/specify.md"])
def test_routed_frontmatter_rejects_symlink_targets_before_any_write(tmp_path, monkeypatch, relative):
    import shutil

    from codexspec.worktrees import write_destination
    from tests.automation_test_support import git

    repo = configured(tmp_path / "repo")
    command = Path(".claude/commands/codexspec/specify.md")
    (repo / command).parent.mkdir(parents=True)
    (repo / command).write_bytes((codexspec.get_templates_dir() / "commands/specify.md").read_bytes())
    git(repo, "add", ".")
    git(repo, "commit", "-m", "commands")
    dest = write_destination(repo)
    path = dest / relative
    directory = path.is_dir()
    if directory:
        shutil.rmtree(path)
    else:
        path.unlink()
    try:
        path.symlink_to(repo / relative, target_is_directory=directory)
    except OSError:
        pytest.skip("symlink creation requires platform support")
    originals = [
        (p, p.read_bytes()) for p in (repo / command, repo / ".codexspec/config.yml", dest / ".codexspec/config.yml")
    ]
    monkeypatch.chdir(repo)
    result = runner.invoke(codexspec.app, ["config", "--set-interaction-lang", "zh-CN"])
    assert result.exit_code != 0, result.output
    assert all(path.read_bytes() == content for path, content in originals)


@pytest.mark.parametrize(
    "option,value",
    [
        ("--worktrees", "off"),
        ("--auto-next", "on"),
        ("--auto-distill", "off"),
        ("--set-lang", "zh-CN"),
        ("--set-interaction-lang", "zh-CN"),
        ("--set-document-lang", "zh-CN"),
        ("--set-commit-lang", "zh-CN"),
    ],
)
def test_routed_config_rejects_hardlinks_before_writing(tmp_path, monkeypatch, option, value):
    from codexspec.worktrees import write_destination

    repo = configured(tmp_path / "repo")
    dest = write_destination(repo)
    source = repo / ".codexspec/config.yml"
    target = dest / ".codexspec/config.yml"
    original = source.read_bytes()
    target.unlink()
    target.hardlink_to(source)
    monkeypatch.chdir(repo)
    result = runner.invoke(codexspec.app, ["config", option, value])
    assert result.exit_code != 0 and "unsafe_write_path" in result.output, result.output
    assert source.read_bytes() == target.read_bytes() == original


@pytest.mark.parametrize("option", ["--set-lang", "--set-interaction-lang"])
def test_routed_frontmatter_rejects_hardlinks_before_any_write(tmp_path, monkeypatch, option):
    from codexspec.worktrees import write_destination
    from tests.automation_test_support import git

    repo = configured(tmp_path / "repo")
    command = Path(".claude/commands/codexspec/specify.md")
    (repo / command).parent.mkdir(parents=True)
    (repo / command).write_bytes((codexspec.get_templates_dir() / "commands/specify.md").read_bytes())
    git(repo, "add", ".")
    git(repo, "commit", "-m", "commands")
    dest = write_destination(repo)
    (dest / command).unlink()
    (dest / command).hardlink_to(repo / command)
    originals = [
        (p, p.read_bytes()) for p in (repo / command, repo / ".codexspec/config.yml", dest / ".codexspec/config.yml")
    ]
    monkeypatch.chdir(repo)
    result = runner.invoke(codexspec.app, ["config", option, "zh-CN"])
    assert result.exit_code != 0 and "unsafe_write_path" in result.output, result.output
    assert all(path.read_bytes() == content for path, content in originals)
