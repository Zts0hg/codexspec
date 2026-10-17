import os
import subprocess

import pytest

from codexspec.installations.metadata import METADATA, inspect_installation, publish_metadata
from codexspec.installations.upgrade import apply_plan, preflight, prepare_plan, project_options


def git(root, *args):
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True).stdout


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init")
    file = root / ".codexspec/scripts/common.sh"
    file.parent.mkdir(parents=True)
    file.write_bytes(b"old\n")
    git(root, "add", ".")
    git(root, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "initial")
    return root


def plan(root):
    return prepare_plan(root, "1.2.3", "claude", "en", {".codexspec/scripts/common.sh": b"new\n"})


def snapshot(root):
    return {
        str(p.relative_to(root)): (p.lstat().st_mode, p.read_bytes() if p.is_file() else None) for p in root.rglob("*")
    }


def test_t04_s01_s08_clean_legacy_and_unrelated_changes(repo):
    (repo / "business.py").write_text("uncommitted business\n")
    p = plan(repo)
    preflight(p)
    assert not (repo / METADATA).exists()


@pytest.mark.parametrize("change", ["unstaged", "staged", "deleted", "untracked", "ignored", "assume", "skip"])
def test_t04_s02_s03_s04_modified_paths_are_unchanged(repo, change):
    file = repo / ".codexspec/scripts/common.sh"
    if change in {"untracked", "ignored"}:
        git(repo, "rm", "--cached", str(file))
        git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "untrack")
    if change == "ignored":
        (repo / ".gitignore").write_text(".codexspec/scripts/\n")
    if change in {"assume", "skip"}:
        git(repo, "update-index", "--assume-unchanged" if change == "assume" else "--skip-worktree", str(file))
    if change == "deleted":
        file.unlink()
    else:
        file.write_text("user work\n")
    if change == "staged":
        git(repo, "add", str(file))
    before = snapshot(repo)
    with pytest.raises(ValueError):
        preflight(plan(repo))
    assert snapshot(repo) == before


def test_t04_s03_missing_git_is_not_permission(tmp_path):
    (tmp_path / ".codexspec").mkdir()
    with pytest.raises(ValueError):
        preflight(plan(tmp_path))
    assert not (tmp_path / METADATA).exists()


def test_t04_s05_inherited_git_environment_is_ignored(repo, tmp_path, monkeypatch):
    foreign = tmp_path / "foreign"
    foreign.mkdir()
    git(foreign, "init")
    monkeypatch.setenv("GIT_DIR", str(foreign / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(foreign))
    monkeypatch.setenv("GIT_INDEX_FILE", str(foreign / ".git/index"))
    preflight(plan(repo))


def test_t04_s06_options_preserved_and_unknown_rejected(repo):
    config = repo / ".codexspec/config.yml"
    config.write_text("project:\n  ai: both\nlanguage:\n  interaction: zh-CN\n")
    assert project_options(repo) == ("both", "zh-CN")
    config.write_text("project:\n  ai: invalid\n")
    with pytest.raises(ValueError):
        project_options(repo)


@pytest.mark.parametrize("kind", ["symlink", "hardlink", "directory"])
def test_t04_s07_invalid_destination(repo, tmp_path, kind):
    path = repo / ".codexspec/scripts/common.sh"
    data = path.read_bytes()
    path.unlink()
    if kind == "directory":
        path.mkdir()
    elif kind == "hardlink":
        external = tmp_path / "external"
        external.write_bytes(data)
        path.hardlink_to(external)
    else:
        try:
            path.symlink_to(tmp_path / "missing")
        except OSError:
            pytest.skip("symlinks unavailable")
    with pytest.raises(ValueError):
        preflight(plan(repo))


def test_t04_s09_no_downgrade(repo):
    files = {".codexspec/scripts/common.sh": b"old\n"}
    publish_metadata(repo, "9.0.0", "claude", "en", files)
    with pytest.raises(ValueError, match="newer"):
        plan(repo)


def test_t05_s01_success_publishes_metadata_last(repo, monkeypatch):
    from codexspec.installations import upgrade

    events = []
    original = upgrade.atomic_write

    def write(path, data, mode=None):
        events.append(path.relative_to(repo).as_posix())
        original(path, data, mode)

    monkeypatch.setattr(upgrade, "atomic_write", write)
    apply_plan(plan(repo))
    assert events[-1] == METADATA
    assert inspect_installation(repo).state == "consistent"


def test_t05_s02_s04_stale_plan_is_no_write(repo):
    p = plan(repo)
    (repo / ".codexspec/scripts/common.sh").write_text("changed after preparation\n")
    before = snapshot(repo)
    with pytest.raises(ValueError):
        apply_plan(p)
    assert snapshot(repo) == before


def test_t05_s03_failure_does_not_publish_metadata(repo, monkeypatch):
    from codexspec.installations import upgrade

    original = upgrade.atomic_write

    def write(path, data, mode=None):
        if path.name == "extra.sh":
            raise OSError("disk full")
        return original(path, data, mode)

    monkeypatch.setattr(upgrade, "atomic_write", write)
    p = prepare_plan(
        repo,
        "1.2.3",
        "claude",
        "en",
        {
            ".codexspec/scripts/common.sh": b"new\n",
            ".codexspec/scripts/extra.sh": b"another\n",
        },
    )
    with pytest.raises(RuntimeError, match="partial"):
        apply_plan(p)
    assert not (repo / METADATA).exists()


def test_t05_s05_retirement_preserves_extensions(repo):
    files = {".codexspec/scripts/common.sh": b"old\n"}
    publish_metadata(repo, "1.0", "claude", "en", files)
    extension = repo / ".codexspec/scripts/custom.sh"
    extension.write_text("custom\n")
    git(repo, "add", ".")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "metadata")
    p = prepare_plan(repo, "1.2.3", "claude", "en", {".codexspec/scripts/replacement.sh": b"new\n"})
    apply_plan(p)
    assert not (repo / ".codexspec/scripts/common.sh").exists()
    assert extension.read_text() == "custom\n"


def test_t04_s02_unmerged_index_refused(repo):
    name = ".codexspec/scripts/common.sh"
    oid = git(repo, "rev-parse", "HEAD:" + name).decode().strip()
    git(repo, "update-index", "--force-remove", name)
    subprocess.run(
        ["git", "-C", str(repo), "update-index", "--index-info"],
        input=f"100644 {oid} 1\t{name}\n100644 {oid} 2\t{name}\n".encode(),
        check=True,
    )
    before = snapshot(repo)
    with pytest.raises(ValueError, match="unmerged"):
        apply_plan(plan(repo))
    assert snapshot(repo) == before


def test_t04_s05_nested_and_worktree_scope(repo, tmp_path, monkeypatch):
    linked = tmp_path / "linked"
    git(repo, "worktree", "add", "-b", "linked", str(linked))
    monkeypatch.setenv("GIT_DIR", str(repo / ".git"))
    apply_plan(plan(linked))
    assert (repo / ".codexspec/scripts/common.sh").read_bytes() == b"old\n"
    nested = repo / "nested"
    path = nested / ".codexspec/scripts/common.sh"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"old\n")
    git(repo, "add", "nested")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "nested")
    apply_plan(plan(nested))
    assert path.read_bytes() == b"new\n"
    assert (repo / ".codexspec/scripts/common.sh").read_bytes() == b"old\n"


def test_t04_s08_same_version_discard_is_repairable(repo):
    p = plan(repo)
    apply_plan(p)
    git(repo, "add", ".")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "upgrade")
    command = repo / ".codexspec/scripts/common.sh"
    command.write_bytes(b"old\n")
    assert inspect_installation(repo).state == "inconsistent"
    with pytest.raises(ValueError, match="unstaged"):
        apply_plan(plan(repo))
    git(repo, "add", ".")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "partial discard")
    apply_plan(plan(repo))
    assert inspect_installation(repo).state == "consistent"


@pytest.mark.parametrize("change", ["config", "index"])
def test_t05_s02_stale_input_or_index(repo, change):
    p = plan(repo)
    if change == "config":
        (repo / ".codexspec/config.yml").write_text("project: {ai: codex}\n")
    else:
        command = repo / ".codexspec/scripts/common.sh"
        command.write_bytes(b"staged\n")
        git(repo, "add", ".")
        command.write_bytes(b"old\n")
    before = snapshot(repo)
    index = (repo / ".git/index").read_bytes()
    with pytest.raises(ValueError):
        apply_plan(p)
    assert snapshot(repo) == before
    assert (repo / ".git/index").read_bytes() == index


def test_t04_s06_context_body_cannot_be_replaced(repo):
    (repo / "AGENTS.md").write_text("User rules\n")
    with pytest.raises(ValueError, match="project-owned"):
        prepare_plan(repo, "1.2.3", "codex", "en", {"AGENTS.md": b"Replaced\n"})


def test_t05_s05_legacy_retired_planning_command(repo):
    retired = repo / ".claude/commands/codexspec/spec-to-plan.md"
    retired.parent.mkdir(parents=True)
    retired.write_bytes(b"old planning command\n")
    git(repo, "add", ".")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "legacy")
    p = prepare_plan(repo, "1.2.3", "claude", "en", {".claude/commands/codexspec/design-to-plan.md": b"new planning\n"})
    apply_plan(p)
    assert not retired.exists()


@pytest.mark.parametrize("choice", ["[codex]", "{bad: codex}", "42", "null"])
def test_t04_s06_malformed_integration_choice_is_reportable(repo, choice):
    (repo / ".codexspec/config.yml").write_text(f"project:\n  ai: {choice}\n")
    with pytest.raises(ValueError):
        project_options(repo)


@pytest.mark.parametrize(
    ("autocrlf", "attributes", "clean"),
    [
        ("false", "!text !eol", False),
        ("false", "-text", False),
        ("true", "-text", False),
        ("true", "!text !eol", True),
        ("input", "!text !eol", True),
        ("false", "text", True),
        ("false", "text=auto", True),
        ("false", "eol=crlf", True),
        ("false", "eol=lf", True),
    ],
)
@pytest.mark.parametrize("binary", [False, True])
def test_t04_s02_s04_crlf_protection_follows_git_policy(repo, autocrlf, attributes, clean, binary):
    name = ".codexspec/scripts/common.sh"
    git(repo, "config", "core.autocrlf", autocrlf)
    git(repo, "config", "core.attributesfile", os.devnull)
    (repo / ".gitattributes").write_text(f"{name} {attributes}\n")
    original = b"old\x00\n" if binary else b"old\n"
    (repo / name).write_bytes(original)
    clean = clean and (not binary or attributes in {"text", "eol=crlf", "eol=lf"})
    git(repo, "add", ".")
    git(repo, "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "policy")
    (repo / name).write_bytes(original.replace(b"\n", b"\r\n"))
    assert bool(git(repo, "diff", "--name-only", "--", name)) is not clean
    before = snapshot(repo)
    if clean:
        apply_plan(plan(repo))
        assert (repo / name).read_bytes() == b"new\n"
    else:
        with pytest.raises(ValueError, match="unstaged"):
            apply_plan(plan(repo))
        assert snapshot(repo) == before
