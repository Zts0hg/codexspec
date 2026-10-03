"""Behavioral coverage for isolated feature and maintenance workspaces."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from codexspec.automation import AutomationError, GitRunner, locate_repository
from codexspec.worktrees import WorkspaceManager, read_worktrees, write_destination, write_worktrees
from tests.automation_test_support import git, make_bare_remote, make_repo

FEATURE = "2026-1003-2049ab-alpha"
OTHER = "2026-1003-2049cd-beta"


def configured(path: Path, enabled: bool = True) -> Path:
    repo = make_repo(path.resolve())
    cfg = repo / ".codexspec/config.yml"
    cfg.parent.mkdir()
    cfg.write_text(f"language:\n  output: en\nworkflow:\n  worktrees: {str(enabled).lower()}\n")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "configure")
    return repo


def commit(repo: Path, name: str, text: str = "new\n") -> str:
    (repo / name).write_text(text)
    git(repo, "add", name)
    git(repo, "commit", "-m", name)
    return git(repo, "rev-parse", "HEAD").stdout.strip()


@pytest.mark.parametrize(
    "body,expected",
    [
        ("", True),
        ("language:\n  output: en\n", True),
        ("workflow:\n  worktrees: false\n", False),
        ("workflow:\n  worktrees: true\n", True),
        ("project:\n  worktrees: false\n", True),
        ('workflow:\n  worktrees: "false"\n', True),
    ],
)
def test_s001_setting_default_and_optout(tmp_path, body, expected):
    cfg = tmp_path / "config.yml"
    assert read_worktrees(cfg)
    cfg.write_text(body)
    assert read_worktrees(cfg) is expected


def test_s002_s003_write_preserves_independent_config(tmp_path):
    a = tmp_path / "a.yml"
    b = tmp_path / "b.yml"
    a.write_text("# comment\nlanguage:\n  output: en # keep\nworkflow:\n  auto_next: true\n")
    b.write_text(a.read_text())
    write_worktrees(a, False)
    assert not read_worktrees(a) and read_worktrees(b)
    assert "# comment" in a.read_text() and "output: en # keep" in a.read_text()
    assert "auto_next: true" in a.read_text()
    write_worktrees(a, True)
    assert read_worktrees(a) and a.read_text().count("worktrees:") == 1


def test_s004_s006_parent_and_fixed_automation(tmp_path):
    repo = configured(tmp_path / "repo")
    linked = tmp_path / "linked"
    git(repo, "worktree", "add", "-b", "topic", str(linked))
    nested = linked / ".codexspec"
    expected = tmp_path.resolve() / "repo-codexspec-worktrees" / "worktree-for-codexspec-auto-dev"
    for path in (repo, linked, nested):
        assert locate_repository(path).worktree_path == expected
    git(repo, "branch", "-m", "unidentified-topic")
    with pytest.raises(AutomationError):
        WorkspaceManager(repo)


def test_s005_bare_parent(tmp_path):
    source = configured(tmp_path / "source")
    bare = make_bare_remote(tmp_path / "repo.git", source)
    linked = tmp_path / "linked"
    git(bare, "worktree", "add", str(linked), "main")
    a = locate_repository(bare)
    b = locate_repository(linked)
    assert a.repository_root == b.repository_root == bare.resolve()
    assert (
        a.worktree_path
        == b.worktree_path
        == Path(str(bare.resolve()) + "-codexspec-worktrees") / "worktree-for-codexspec-auto-dev"
    )


def test_s007_s008_s009_s012_independent_creation_and_reuse(tmp_path):
    repo = configured(tmp_path / "repo")
    (repo / "README.md").write_text("staged\n")
    git(repo, "add", "README.md")
    (repo / "README.md").write_text("unstaged\n")
    (repo / "untracked").write_text("mine")
    before = (
        git(repo, "rev-parse", "HEAD").stdout,
        git(repo, "symbolic-ref", "HEAD").stdout,
        git(repo, "diff", "--cached").stdout,
        git(repo, "diff").stdout,
    )
    manager = WorkspaceManager(repo)
    a = manager.create(FEATURE)
    b = manager.create(OTHER)
    assert a["status"] == b["status"] == "ready"
    work = Path(a["workspace"])
    assert work.name == FEATURE and work.parent == Path(str(repo) + "-codexspec-worktrees")
    assert Path(a["requirements_file"]).is_file() and Path(b["workspace"]) != work
    Path(a["requirements_file"]).write_text("confirmed original\n")
    (work / "local.txt").write_text("keep")
    again = WorkspaceManager(Path(b["workspace"])).resolve(FEATURE)
    assert again["workspace"] == a["workspace"] and Path(a["requirements_file"]).read_text() == "confirmed original\n"
    assert (work / "local.txt").read_text() == "keep"
    after = (
        git(repo, "rev-parse", "HEAD").stdout,
        git(repo, "symbolic-ref", "HEAD").stdout,
        git(repo, "diff", "--cached").stdout,
        git(repo, "diff").stdout,
    )
    assert before == after and (repo / "untracked").read_text() == "mine"
    assert git(repo, "branch", "--show-current").stdout.strip() == "main"
    assert FEATURE in git(repo, "worktree", "list").stdout


def test_s010_occupied_and_invalid_destinations(tmp_path):
    repo = configured(tmp_path / "repo")
    m = WorkspaceManager(repo)
    occupied = m.parent / FEATURE
    occupied.mkdir(parents=True)
    (occupied / "mine").write_text("keep")
    with pytest.raises(AutomationError, match="occupied"):
        m.create(FEATURE)
    assert (occupied / "mine").read_text() == "keep"
    with pytest.raises(AutomationError, match="feature"):
        m.create("../escape")
    assert not (repo / ".codexspec/specs").exists()
    git(repo, "branch", OTHER)
    git(repo, "worktree", "add", str(tmp_path / "elsewhere"), OTHER)
    with pytest.raises(AutomationError, match="mismatch"):
        m.create(OTHER)


def test_s011_maintenance_routing_and_reuse(tmp_path):
    repo = configured(tmp_path / "repo")
    dest = write_destination(repo)
    assert dest.name == "worktree-for-codexspec-maintenance"
    assert write_destination(repo) == dest
    feature = Path(WorkspaceManager(repo).create(FEATURE)["workspace"])
    assert write_destination(feature) == feature
    write_worktrees(repo / ".codexspec/config.yml", False)
    assert write_destination(repo) == repo


def test_s013_concurrent_same_feature_reuses_one_registration(tmp_path):
    repo = configured(tmp_path / "repo")
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: WorkspaceManager(repo).create(FEATURE), range(2)))
    assert results[0]["workspace"] == results[1]["workspace"]
    assert git(repo, "worktree", "list").stdout.count(FEATURE) == 2  # path + branch, one registration


@pytest.mark.parametrize("direction", ["equal", "local", "remote"])
def test_s014_ancestry_selection(tmp_path, direction, monkeypatch):
    repo = configured(tmp_path / "repo")
    remote = make_bare_remote(tmp_path / "remote.git", repo)
    expected = git(repo, "rev-parse", "HEAD").stdout.strip()
    # Deliberately older commit dates must not outrank ancestry.
    monkeypatch.setenv("GIT_AUTHOR_DATE", "2000-01-01T00:00:00Z")
    monkeypatch.setenv("GIT_COMMITTER_DATE", "2000-01-01T00:00:00Z")
    if direction == "local":
        expected = commit(repo, "local.txt")
    if direction == "remote":
        peer = tmp_path / "peer"
        git(remote, "worktree", "add", str(peer), "main")
        expected = commit(peer, "remote.txt")
    result = WorkspaceManager(repo).create(FEATURE)
    assert git(Path(result["workspace"]), "rev-parse", "HEAD").stdout.strip() == expected


class FailedFetch(GitRunner):
    def __init__(self):
        super().__init__()
        self.fetches = 0

    def run(self, repository, *args, **kwargs):
        if args and args[0] == "fetch":
            import subprocess

            self.fetches += 1
            return subprocess.CompletedProcess(args, 1, "", "offline")
        return super().run(repository, *args, **kwargs)


def test_s015_fetch_failure_fallback_and_retry(tmp_path):
    repo = configured(tmp_path / "repo")
    make_bare_remote(tmp_path / "remote.git", repo)
    runner = FailedFetch()
    m = WorkspaceManager(repo, runner=runner)
    for name in (FEATURE, OTHER):
        result = m.create(name)
        assert result["status"] == "ready" and result["warnings"] and "stale" in str(result["warnings"])
    assert runner.fetches == 2


def test_s016_missing_baseline_stops(tmp_path):
    repo = configured(tmp_path / "repo")
    git(repo, "update-ref", "-d", "refs/heads/main")
    with pytest.raises(AutomationError):
        WorkspaceManager(repo).create(FEATURE)
    assert not (repo / ".codexspec/specs").exists()


def diverged(tmp_path, conflict=False):
    repo = configured(tmp_path / "repo")
    remote = make_bare_remote(tmp_path / "remote.git", repo)
    peer = tmp_path / "peer"
    git(remote, "worktree", "add", str(peer), "main")
    local = commit(repo, "README.md" if conflict else "local.txt", "local\n")
    other = commit(peer, "README.md" if conflict else "remote.txt", "remote\n")
    return repo, local, other


def evidence(work):
    return {
        "head": git(work, "rev-parse", "HEAD").stdout.strip(),
        "tree": git(work, "rev-parse", "HEAD^{tree}").stdout.strip(),
        "checks": [{"command": "project checks", "exit_code": 0}],
    }


def test_s017_s019_merge_requires_verification_and_resumes(tmp_path):
    repo, local, remote = diverged(tmp_path)
    m = WorkspaceManager(repo)
    result = m.create(FEATURE)
    work = Path(result["workspace"])
    assert result["status"] == "merge_requires_verification"
    assert not Path(result["requirements_file"]).exists()
    assert m.resolve(FEATURE)["status"] == result["status"]
    assert git(work, "merge-base", "--is-ancestor", local, "HEAD").returncode == 0
    assert git(work, "merge-base", "--is-ancestor", remote, "HEAD").returncode == 0
    bad = evidence(work)
    bad["checks"][0]["exit_code"] = 1
    with pytest.raises(AutomationError, match="verification"):
        m.finish(FEATURE, bad)
    bad = evidence(work)
    bad["head"] = "0" * 40
    with pytest.raises(AutomationError, match="verification"):
        m.finish(FEATURE, bad)
    done = m.finish(FEATURE, evidence(work))
    assert done["status"] == "ready" and Path(done["requirements_file"]).exists()
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == local


def test_s018_conflict_must_be_resolved_before_finish(tmp_path):
    repo, local, _ = diverged(tmp_path, True)
    m = WorkspaceManager(repo)
    result = m.create(FEATURE)
    work = Path(result["workspace"])
    assert result["status"] == "merge_requires_resolution"
    with pytest.raises(AutomationError):
        m.finish(FEATURE, evidence(work))
    (work / "README.md").write_text("both\n")
    git(work, "add", "README.md")
    git(work, "commit", "-m", "resolve")
    assert m.finish(FEATURE, evidence(work))["status"] == "ready"
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == local


def test_s013_invalid_preparation_metadata_is_not_adopted(tmp_path):
    import json

    repo = configured(tmp_path / "repo")
    manager = WorkspaceManager(repo)
    manager.create(FEATURE)
    record = manager.records / f"{FEATURE}.json"
    data = json.loads(record.read_text())
    data["baselines"] = [12]
    record.write_text(json.dumps(data))
    with pytest.raises(AutomationError, match="invalid_workspace_state"):
        manager.resolve(FEATURE)


class InterruptedCreation(GitRunner):
    def __init__(self, phase):
        super().__init__()
        self.phase = phase

    def run(self, repository, *args, **kwargs):
        if self.phase == "before_add" and args[:2] == ("worktree", "add"):
            raise AutomationError("interrupted")
        result = super().run(repository, *args, **kwargs)
        if self.phase == "after_add" and args[:2] == ("worktree", "add"):
            raise AutomationError("interrupted")
        if self.phase == "after_merge" and args[:1] == ("merge",):
            raise AutomationError("interrupted")
        return result


@pytest.mark.parametrize("phase", ["before_add", "after_add"])
def test_s013_interrupted_creation_resumes_owned_state(tmp_path, phase):
    repo = configured(tmp_path / "repo")
    manager = WorkspaceManager(repo, runner=InterruptedCreation(phase))
    with pytest.raises(AutomationError, match="interrupted"):
        manager.create(FEATURE)
    recovered = WorkspaceManager(repo).create(FEATURE)
    assert recovered["status"] == "ready"
    assert Path(recovered["requirements_file"]).is_file()
    assert git(repo, "branch", "--show-current").stdout.strip() == "main"


def test_s013_interrupted_creation_cannot_adopt_changed_head(tmp_path):
    repo = configured(tmp_path / "repo")
    manager = WorkspaceManager(repo, runner=InterruptedCreation("after_add"))
    with pytest.raises(AutomationError, match="interrupted"):
        manager.create(FEATURE)
    work = manager.parent / FEATURE
    commit(work, "user.txt")
    with pytest.raises(AutomationError, match="workspace_state_mismatch"):
        WorkspaceManager(repo).create(FEATURE)
    assert (work / "user.txt").read_text() == "new\n"
    assert not (work / ".codexspec/specs" / FEATURE).exists()


def test_s019_interrupted_merge_keeps_verification_obligation(tmp_path):
    repo, local, _ = diverged(tmp_path)
    manager = WorkspaceManager(repo, runner=InterruptedCreation("after_merge"))
    with pytest.raises(AutomationError, match="interrupted"):
        manager.create(FEATURE)
    manager = WorkspaceManager(repo)
    result = manager.create(FEATURE)
    assert result["status"] == "merge_requires_verification"
    assert not Path(result["requirements_file"]).exists()
    assert git(repo, "rev-parse", "HEAD").stdout.strip() == local
    assert manager.finish(FEATURE, evidence(Path(result["workspace"])))["status"] == "ready"


def test_remote_default_branch_with_slash_preserves_identity(tmp_path):
    repo = configured(tmp_path / "repo")
    make_bare_remote(tmp_path / "remote.git", repo)
    git(repo, "branch", "-m", "stable/main")
    git(repo, "push", "origin", "stable/main")
    git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/stable/main")
    context = locate_repository(repo)
    assert context.default_branch == "stable/main"
    result = WorkspaceManager(repo).create(FEATURE)
    assert result["status"] == "ready"


@pytest.mark.parametrize("body", ["{}\n", "{language: {output: en}} # keep\n", "workflow: {}\n"])
def test_setting_writer_supports_flow_yaml_without_losing_fields(tmp_path, body):
    import yaml

    config = tmp_path / "config.yml"
    config.write_text(body)
    original = yaml.safe_load(body)
    write_worktrees(config, False)
    result = yaml.safe_load(config.read_text())
    assert result["workflow"]["worktrees"] is False
    if "language" in original:
        assert result["language"] == original["language"]
        assert "# keep" in config.read_text()


@pytest.mark.parametrize("action", ["create", "resolve"])
@pytest.mark.parametrize("replacement", ["directory", "foreign_repo", "missing"])
def test_stale_worktree_registration_cannot_adopt_replacement(tmp_path, action, replacement):
    repo = configured(tmp_path / "repo")
    manager = WorkspaceManager(repo)
    data = manager.create(FEATURE)
    work = Path(data["workspace"])
    work.rename(tmp_path / "saved")
    if replacement == "directory":
        work.mkdir()
        (work / "sentinel").write_text("foreign")
    elif replacement == "foreign_repo":
        make_repo(work)
    with pytest.raises(AutomationError):
        getattr(manager, action)(FEATURE)
    assert not Path(data["requirements_file"]).exists()


@pytest.mark.parametrize(
    "body",
    [
        "workflow:\n  worktrees: &isolation true\nother: *isolation # keep\n",
        "defaults: &defaults\n  worktrees: true\nworkflow: *defaults\nother: *defaults # keep\n",
        "workflow: &defaults {worktrees: true, auto_next: false}\nother: *defaults # keep\n",
        "---\nlanguage: {output: en} # keep\n...\n",
        "---\n{} # keep\n...\n",
    ],
)
def test_worktree_setting_preserves_yaml_aliases_and_document_boundaries(tmp_path, body):
    import yaml

    path = tmp_path / "config.yml"
    path.write_text(body)
    expected = yaml.safe_load(body)
    expected = {**expected, "workflow": {**expected.get("workflow", {}), "worktrees": False}}
    write_worktrees(path, False)
    assert yaml.safe_load(path.read_text()) == expected
    assert not read_worktrees(path)
    assert "# keep" in path.read_text()


@pytest.mark.parametrize("action", ["create", "resolve", "finish"])
@pytest.mark.parametrize(
    "relative",
    [".codexspec", ".codexspec/specs", f".codexspec/specs/{FEATURE}", f".codexspec/specs/{FEATURE}/requirements.md"],
)
def test_feature_entry_points_reject_redirected_artifact_paths(tmp_path, action, relative):
    import shutil

    repo = configured(tmp_path / "repo")
    manager = WorkspaceManager(repo)
    result = manager.create(FEATURE)
    work = Path(result["workspace"])
    protected = repo / f".codexspec/specs/{FEATURE}/requirements.md"
    protected.parent.mkdir(parents=True)
    protected.write_text("protected main\n")
    target = work / relative
    directory = target.is_dir()
    if directory:
        shutil.rmtree(target)
    else:
        target.unlink()
    try:
        target.symlink_to(repo / relative, target_is_directory=directory)
    except OSError:
        pytest.skip("symlink creation requires platform support")
    with pytest.raises(AutomationError, match="unsafe_feature_path"):
        if action == "finish":
            manager.finish(FEATURE, evidence(work))
        else:
            getattr(manager, action)(FEATURE)
    assert protected.read_text() == "protected main\n"


@pytest.mark.parametrize("action", ["create", "resolve", "finish"])
def test_feature_entry_points_reject_hardlinked_requirements(tmp_path, action):
    repo = configured(tmp_path / "repo")
    manager = WorkspaceManager(repo)
    result = manager.create(FEATURE)
    work = Path(result["workspace"])
    target = Path(result["requirements_file"])
    protected = repo / "protected.md"
    protected.write_text("protected main\n")
    target.unlink()
    target.hardlink_to(protected)
    with pytest.raises(AutomationError, match="unsafe_feature_path"):
        if action == "finish":
            manager.finish(FEATURE, evidence(work))
        else:
            getattr(manager, action)(FEATURE)
    assert protected.read_text() == "protected main\n"


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.parametrize(
    "before,after",
    [
        ("workflow:\n  worktrees: true # keep\n", "workflow:\n  worktrees: false # keep\n"),
        ("workflow:\n  auto_next: true\n", "workflow:\n  worktrees: false\n  auto_next: true\n"),
        ("language: {output: en}\n", "language: {output: en}\nworkflow:\n  worktrees: false\n"),
        ("---\nlanguage: {output: en}\n...\n", "---\nlanguage: {output: en}\nworkflow:\n  worktrees: false\n...\n"),
    ],
)
def test_worktree_setting_preserves_line_endings(tmp_path, newline, before, after):
    config = tmp_path / "config.yml"
    comment = "# Preserve café and line endings\n"
    original = (comment + before).replace("\n", newline).encode("utf-8")
    expected = (comment + after).replace("\n", newline).encode("utf-8")
    config.write_bytes(original)
    write_worktrees(config, False)
    assert config.read_bytes() == expected
    assert not read_worktrees(config)
    if "worktrees: true" in before:
        write_worktrees(config, True)
        assert config.read_bytes() == original
