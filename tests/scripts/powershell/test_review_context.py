"""Contract tests for scripts/powershell/review-context.ps1."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from tests.review_context_cases import (
    FEATURE,
    create_feature_artifacts,
    create_feature_change,
    git,
    init_repository,
    inventory_by_path,
    normalize_manifest,
    parse_manifest,
    repository_snapshot,
    write,
)


@pytest.fixture
def resolver(powershell_scripts_dir: Path) -> Path:
    return powershell_scripts_dir / "review-context.ps1"


def test_powershell_resolver_source_exists(resolver: Path) -> None:
    assert resolver.exists()
    source = resolver.read_text(encoding="utf-8")
    assert "ConvertTo-Json" in source
    assert "schema_version" in source
    assert "ls-remote" in source


def run_resolver(run_powershell_script, resolver: Path, repo: Path, *args: str):
    result = run_powershell_script(resolver, list(args), cwd=repo)
    return result, parse_manifest(result.stdout)


def test_default_feature_target_matches_shared_contract(tmp_path: Path, resolver: Path, run_powershell_script) -> None:
    repo = init_repository(tmp_path)
    feature_dir = create_feature_change(repo)
    before = repository_snapshot(repo)

    result, manifest = run_resolver(run_powershell_script, resolver, repo)

    assert result.returncode == 0, result.stderr
    assert manifest["selector"] == "default"
    assert manifest["target"]["base_ref"] == "main"
    assert manifest["target"]["complete_feature"] is True
    assert Path(manifest["feature"]["path"]) == feature_dir
    inventory = inventory_by_path(manifest)
    assert inventory["src/layered.txt"]["segments"] == ["committed", "staged", "unstaged"]
    assert inventory["src/untracked.txt"]["segments"] == ["untracked"]
    assert "ignored.tmp" not in inventory
    assert repository_snapshot(repo) == before


@pytest.mark.parametrize("selector", ["--committed", "--uncommitted"])
def test_explicit_branch_selectors_are_isolated(
    tmp_path: Path, resolver: Path, run_powershell_script, selector: str
) -> None:
    repo = init_repository(tmp_path)
    create_feature_change(repo)

    result, manifest = run_resolver(run_powershell_script, resolver, repo, selector)

    assert result.returncode == 0
    inventory = inventory_by_path(manifest)
    if selector == "--committed":
        assert "src/committed.txt" in inventory
        assert "src/untracked.txt" not in inventory
    else:
        assert "src/committed.txt" not in inventory
        assert "src/untracked.txt" in inventory


def test_commit_parent_and_override_match_git(tmp_path: Path, resolver: Path, run_powershell_script) -> None:
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

    _, default = run_resolver(run_powershell_script, resolver, repo, "--commit", merge)
    _, overridden = run_resolver(run_powershell_script, resolver, repo, "--commit", merge, "--parent", "2")

    assert default["target"]["parent_sha"] == first_parent
    assert overridden["target"]["parent_sha"] == second_parent


def test_special_inventory_kinds_and_paths(tmp_path: Path, resolver: Path, run_powershell_script) -> None:
    repo = init_repository(tmp_path)
    git(repo, "switch", "-c", FEATURE)
    os.symlink("base.txt", repo / "src" / "link name")
    write(repo, "src/binary.bin", b"\x00\x01binary")
    write(repo, "src/semi;quote'$.txt", "special\n")
    git(repo, "add", "-A")

    result, manifest = run_resolver(run_powershell_script, resolver, repo, "--uncommitted")

    assert result.returncode == 0
    inventory = inventory_by_path(manifest)
    assert inventory["src/link name"]["kind"] == "symlink"
    assert inventory["src/binary.bin"]["kind"] == "binary"
    assert "src/semi;quote'$.txt" in inventory


@pytest.mark.parametrize(
    ("args", "code"),
    [
        (("src/",), "bare_path_argument"),
        (("--committed", "--uncommitted"), "conflicting_selectors"),
        (("--uncommitted", "--base", "main"), "invalid_base_modifier"),
        (("--parent", "2"), "parent_requires_commit"),
        (("--commit", "missing"), "commit_not_found"),
    ],
)
def test_error_codes_match_bash_contract(
    tmp_path: Path, resolver: Path, run_powershell_script, args: tuple[str, ...], code: str
) -> None:
    repo = init_repository(tmp_path)

    result, manifest = run_resolver(run_powershell_script, resolver, repo, *args)

    assert result.returncode != 0
    assert manifest["error"]["code"] == code


def test_explicit_feature_focus_and_empty_target(tmp_path: Path, resolver: Path, run_powershell_script) -> None:
    repo = init_repository(tmp_path)
    feature_dir = create_feature_artifacts(repo)
    focus = "check $(touch should-not-exist); quotes ' and \""

    result, manifest = run_resolver(
        run_powershell_script,
        resolver,
        repo,
        "--uncommitted",
        "--feature",
        str(feature_dir),
        "--focus",
        focus,
    )

    assert result.returncode == 0
    assert manifest["arguments"]["focus"] == [focus]
    assert manifest["feature"]["status"] == "resolved"
    assert manifest["target"]["empty"] is False  # feature artifacts are untracked
    assert not (repo / "should-not-exist").exists()


def test_normalized_shape_is_platform_neutral(tmp_path: Path, resolver: Path, run_powershell_script) -> None:
    repo = init_repository(tmp_path)
    create_feature_change(repo)

    _, manifest = run_resolver(run_powershell_script, resolver, repo)
    normalized = normalize_manifest(manifest)

    assert normalized["repository"]["root"] == "<repo>"
    assert all("\\" not in entry["path"] for entry in normalized["inventory"])
