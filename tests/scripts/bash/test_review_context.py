"""Contract tests for scripts/bash/review-context.sh."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from tests.review_context_cases import (
    FEATURE,
    create_feature_artifacts,
    create_feature_change,
    git,
    init_repository,
    inventory_by_path,
    parse_manifest,
    repository_snapshot,
    write,
)


def run_resolver(script: Path, repo: Path, *args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
    result = subprocess.run(["bash", str(script), *args], cwd=repo, text=True, capture_output=True)
    return result, parse_manifest(result.stdout)


@pytest.fixture
def resolver(bash_scripts_dir: Path) -> Path:
    return bash_scripts_dir / "review-context.sh"


def test_default_feature_target_includes_every_non_ignored_layer(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    feature_dir = create_feature_change(repo)
    before = repository_snapshot(repo)

    result, manifest = run_resolver(resolver, repo)

    assert result.returncode == 0, result.stderr
    assert manifest["selector"] == "default"
    assert manifest["mode"] == "defect"
    assert manifest["target"]["base_ref"] == "main"
    assert manifest["target"]["complete_feature"] is True
    assert manifest["target"]["empty"] is False
    assert manifest["feature"]["status"] == "resolved"
    assert Path(manifest["feature"]["path"]) == feature_dir
    assert all(item["readable"] for item in manifest["feature"]["artifacts"])

    inventory = inventory_by_path(manifest)
    assert "src/committed.txt" in inventory
    assert inventory["src/committed.txt"]["segments"] == ["committed"]
    assert inventory["src/staged.txt"]["segments"] == ["staged"]
    assert inventory["src/base.txt"]["segments"] == ["unstaged"]
    assert inventory["src/untracked.txt"]["segments"] == ["untracked"]
    assert inventory["src/layered.txt"]["segments"] == ["committed", "staged", "unstaged"]
    assert "ignored.tmp" not in inventory
    assert manifest["counts"]["total"] == len(inventory)
    assert repository_snapshot(repo) == before


def test_default_on_base_branch_selects_uncommitted_only(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    write(repo, "src/staged.txt", "staged\n")
    git(repo, "add", "src/staged.txt")
    write(repo, "src/base.txt", "changed\n")
    write(repo, "src/untracked.txt", "new\n")

    result, manifest = run_resolver(resolver, repo)

    assert result.returncode == 0
    assert manifest["selector"] == "default"
    assert manifest["target"]["complete_feature"] is False
    assert manifest["target"]["base_ref"] == "main"
    inventory = inventory_by_path(manifest)
    assert set(inventory) == {"src/base.txt", "src/staged.txt", "src/untracked.txt"}
    assert manifest["feature"]["status"] == "not_resolved"


def test_committed_excludes_uncommitted_and_degrades_completeness(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    create_feature_change(repo)

    result, manifest = run_resolver(resolver, repo, "--committed")

    assert result.returncode == 0
    assert manifest["selector"] == "committed"
    assert manifest["target"]["complete_feature"] is False
    inventory = inventory_by_path(manifest)
    assert "src/committed.txt" in inventory
    assert "src/staged.txt" not in inventory
    assert "src/base.txt" not in inventory
    assert "src/untracked.txt" not in inventory


def test_committed_is_complete_when_no_uncommitted_work_exists(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    git(repo, "switch", "-c", FEATURE)
    create_feature_artifacts(repo)
    write(repo, "src/committed.txt", "committed\n")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "feature")

    result, manifest = run_resolver(resolver, repo, "--committed")

    assert result.returncode == 0
    assert manifest["target"]["complete_feature"] is True


def test_uncommitted_includes_staged_unstaged_and_untracked(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    create_feature_change(repo)

    result, manifest = run_resolver(resolver, repo, "--uncommitted")

    assert result.returncode == 0
    assert manifest["selector"] == "uncommitted"
    assert manifest["target"]["base_ref"] is None
    assert manifest["target"]["complete_feature"] is False
    inventory = inventory_by_path(manifest)
    assert "src/committed.txt" not in inventory
    assert set(inventory["src/layered.txt"]["segments"]) == {"staged", "unstaged"}
    assert inventory["src/untracked.txt"]["segments"] == ["untracked"]


def test_commit_uses_parent_and_root_uses_empty_tree(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    root = git(repo, "rev-list", "--max-parents=0", "HEAD").stdout.strip()
    write(repo, "src/second.txt", "second\n")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "second")
    second = git(repo, "rev-parse", "HEAD").stdout.strip()
    parent = git(repo, "rev-parse", "HEAD^").stdout.strip()

    result, normal = run_resolver(resolver, repo, "--commit", second)
    root_result, root_manifest = run_resolver(resolver, repo, "--commit", root)

    assert result.returncode == root_result.returncode == 0
    assert normal["target"]["commit_sha"] == second
    assert normal["target"]["parent_sha"] == parent
    assert normal["target"]["parent_number"] == 1
    assert root_manifest["target"]["commit_sha"] == root
    assert root_manifest["target"]["parent_number"] == 0
    assert root_manifest["target"]["parent_sha"]


def test_merge_commit_defaults_first_parent_and_accepts_override(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    git(repo, "switch", "-c", "side")
    write(repo, "src/side.txt", "side\n")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "side")
    second_parent = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "switch", "main")
    write(repo, "src/main.txt", "main\n")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "main")
    first_parent = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "merge", "--no-ff", "side", "-m", "merge")
    merge = git(repo, "rev-parse", "HEAD").stdout.strip()

    _, default = run_resolver(resolver, repo, "--commit", merge)
    _, overridden = run_resolver(resolver, repo, "--commit", merge, "--parent", "2")

    assert default["target"]["parent_sha"] == first_parent
    assert default["target"]["parent_number"] == 1
    assert overridden["target"]["parent_sha"] == second_parent
    assert overridden["target"]["parent_number"] == 2


def test_explicit_base_and_remote_symbolic_head_are_reported(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path, branch="trunk")
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-b", "trunk", str(remote)], check=True, capture_output=True, text=True)
    git(repo, "remote", "add", "origin", str(remote))
    git(repo, "push", "-u", "origin", "trunk")
    git(repo, "remote", "set-head", "origin", "trunk")
    git(repo, "switch", "-c", FEATURE)
    write(repo, "src/change.txt", "change\n")

    _, inferred = run_resolver(resolver, repo)
    git(repo, "symbolic-ref", "--delete", "refs/remotes/origin/HEAD")
    before_remote_query = repository_snapshot(repo)
    _, queried = run_resolver(resolver, repo)
    _, explicit = run_resolver(resolver, repo, "--base", "trunk")

    assert inferred["target"]["base_ref"] == "origin/trunk"
    assert inferred["target"]["merge_base_sha"]
    assert queried["target"]["base_ref"] == "origin/trunk"
    assert repository_snapshot(repo) == before_remote_query
    assert explicit["target"]["base_ref"] == "trunk"


def test_inventory_preserves_rename_delete_symlink_binary_and_special_paths(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    write(repo, "src/delete.txt", "delete\n")
    write(repo, "src/rename-old.txt", "rename\n")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "fixture inputs")
    git(repo, "switch", "-c", FEATURE)
    git(repo, "mv", "src/rename-old.txt", "src/rename new.txt")
    (repo / "src" / "delete.txt").unlink()
    os.symlink("base.txt", repo / "src" / "link name")
    write(repo, "src/binary.bin", b"\x00\x01binary")
    write(repo, "src/semi;quote'$.txt", "special\n")
    write(repo, "src/line\nbreak.txt", "newline\n")
    git(repo, "add", "-A")

    result, manifest = run_resolver(resolver, repo, "--uncommitted")

    assert result.returncode == 0, result.stderr
    inventory = inventory_by_path(manifest)
    assert inventory["src/rename new.txt"]["old_path"] == "src/rename-old.txt"
    assert inventory["src/delete.txt"]["status"] == "D"
    assert inventory["src/link name"]["kind"] == "symlink"
    assert inventory["src/binary.bin"]["kind"] == "binary"
    assert "src/semi;quote'$.txt" in inventory
    assert "src/line\nbreak.txt" in inventory


def test_inventory_identifies_submodule_gitlink(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    dependency = tmp_path / "dependency"
    dependency.mkdir()
    git(dependency, "init", "-b", "main")
    write(dependency, "README.md", "dependency\n")
    git(dependency, "add", ".")
    git(dependency, "commit", "-m", "dependency")
    git(repo, "switch", "-c", FEATURE)
    git(repo, "-c", "protocol.file.allow=always", "submodule", "add", str(dependency), "vendor/dependency")

    result, manifest = run_resolver(resolver, repo, "--uncommitted")

    assert result.returncode == 0, result.stderr
    inventory = inventory_by_path(manifest)
    assert inventory["vendor/dependency"]["object_mode"] == "160000"
    assert inventory["vendor/dependency"]["kind"] == "submodule"


def test_clean_base_branch_has_empty_target(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)

    result, manifest = run_resolver(resolver, repo)

    assert result.returncode == 0
    assert manifest["target"]["empty"] is True
    assert manifest["counts"]["total"] == 0


def test_feature_manifest_discloses_missing_artifact(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    feature_dir = create_feature_artifacts(repo)
    (feature_dir / "tasks.md").unlink()

    result, manifest = run_resolver(resolver, repo, "--uncommitted", "--feature", str(feature_dir))

    assert result.returncode == 0
    artifacts = {item["name"]: item["readable"] for item in manifest["feature"]["artifacts"]}
    assert artifacts["requirements.md"] is True
    assert artifacts["tasks.md"] is False


def test_unresolved_default_base_fails_closed(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path, branch="trunk")
    git(repo, "switch", "-c", FEATURE)

    result, manifest = run_resolver(resolver, repo)

    assert result.returncode != 0
    assert manifest["error"]["code"] == "base_not_found"


@pytest.mark.parametrize(
    ("args", "code"),
    [
        (("src/",), "bare_path_argument"),
        (("--committed", "--uncommitted"), "conflicting_selectors"),
        (("--uncommitted", "--base", "main"), "invalid_base_modifier"),
        (("--parent", "2"), "parent_requires_commit"),
        (("--commit", "missing"), "commit_not_found"),
        (("--unknown",), "unknown_argument"),
    ],
)
def test_invalid_arguments_emit_actionable_error_manifest(
    tmp_path: Path, resolver: Path, args: tuple[str, ...], code: str
) -> None:
    repo = init_repository(tmp_path)

    result, manifest = run_resolver(resolver, repo, *args)

    assert result.returncode != 0
    assert manifest["status"] == "error"
    assert manifest["error"]["code"] == code
    assert manifest["error"]["message"]
    assert manifest["error"]["hint"]


def test_explicit_feature_and_repeated_focus_are_data(tmp_path: Path, resolver: Path) -> None:
    repo = init_repository(tmp_path)
    feature_dir = create_feature_artifacts(repo)
    focus = "check $(touch should-not-exist); quotes ' and \""

    result, manifest = run_resolver(
        resolver,
        repo,
        "--uncommitted",
        "--feature",
        str(feature_dir),
        "--focus",
        focus,
        "--focus",
        "second",
    )

    assert result.returncode == 0
    assert manifest["arguments"]["focus"] == [focus, "second"]
    assert manifest["feature"]["status"] == "resolved"
    assert not (repo / "should-not-exist").exists()
