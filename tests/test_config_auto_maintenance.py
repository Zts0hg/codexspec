"""Persistent maintenance policy, including the real configuration boundary."""

from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

import codexspec
from codexspec.automation import AutomationError
from codexspec.i18n import generate_config_content
from codexspec.review_maintenance import read_auto_maintenance, write_auto_maintenance
from tests.test_worktrees import configured

runner = CliRunner()


def config_file(tmp_path: Path, content: str) -> Path:
    path = tmp_path / ".codexspec/config.yml"
    path.parent.mkdir(exist_ok=True)
    path.write_bytes(content.encode("utf-8"))
    return path


@pytest.mark.parametrize(
    "body, expected",
    [
        ("", True),
        ("workflow: {auto_next: false}", True),
        ("workflow: {auto_maintenance: true}", True),
        ("workflow: {auto_maintenance: false}", False),
        ("project: {auto_maintenance: false}", True),
    ],
)
def test_p01_read_policy(tmp_path, body, expected):
    assert read_auto_maintenance(config_file(tmp_path, body)) is expected


def test_p01_missing_and_fresh_default(tmp_path):
    assert read_auto_maintenance(tmp_path / "absent.yml") is True
    assert yaml.safe_load(generate_config_content())["workflow"]["auto_maintenance"] is True


@pytest.mark.parametrize(
    "token, expected",
    [
        ("on", True),
        ("TRUE", True),
        (" 1 ", True),
        ("Yes", True),
        ("off", False),
        ("FALSE", False),
        (" 0 ", False),
        ("No", False),
    ],
)
def test_p02_cli_aliases(tmp_path, monkeypatch, token, expected):
    path = config_file(tmp_path, "workflow: {worktrees: false, auto_next: false}\n")
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(codexspec.app, ["config", "--auto-maintenance", token])
    assert result.exit_code == 0, result.output
    data = yaml.safe_load(path.read_bytes())
    assert data["workflow"]["auto_maintenance"] is expected
    assert data["workflow"]["auto_next"] is False


def test_p02_invalid_input_does_not_write(tmp_path, monkeypatch):
    path = config_file(tmp_path, "workflow: {worktrees: false}\n")
    before = path.read_bytes()
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(codexspec.app, ["config", "--auto-maintenance", "maybe"])
    assert result.exit_code != 0
    assert path.read_bytes() == before


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
@pytest.mark.parametrize(
    "body",
    [
        "# 中文\nworkflow:\n  auto_next: true # advance\n  auto_maintenance: true # repair\n",
        "# 中文\nworkflow: {auto_next: true, auto_maintenance: true} # repair\n",
    ],
)
def test_p03_surgical_round_trip(tmp_path, newline, body):
    path = config_file(tmp_path, body.replace("\n", newline))
    before = path.read_bytes()
    write_auto_maintenance(path, False)
    assert read_auto_maintenance(path) is False
    assert yaml.safe_load(path.read_bytes())["workflow"]["auto_next"] is True
    write_auto_maintenance(path, True)
    assert path.read_bytes() == before


def test_p04_toggle_and_display(tmp_path, monkeypatch):
    path = config_file(tmp_path, "workflow: {worktrees: false, auto_next: true}\n")
    monkeypatch.chdir(tmp_path)
    # Optional-value normalization is performed by the real entry point.
    import subprocess

    result = subprocess.run(["codexspec", "config", "--auto-maintenance"], cwd=tmp_path, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert read_auto_maintenance(path) is False
    shown = runner.invoke(codexspec.app, ["config"])
    assert shown.exit_code == 0 and "auto_maintenance: false" in shown.output
    assert yaml.safe_load(path.read_bytes())["workflow"]["auto_next"] is True


def test_p04_routing_preserves_source(tmp_path, monkeypatch):
    repo = configured(tmp_path / "repo")
    before = (repo / ".codexspec/config.yml").read_bytes()
    monkeypatch.chdir(repo)
    result = runner.invoke(codexspec.app, ["config", "--auto-maintenance", "off"])
    assert result.exit_code == 0, result.output
    dest = Path(str(repo) + "-codexspec-worktrees") / "worktree-for-codexspec-maintenance"
    assert read_auto_maintenance(dest / ".codexspec/config.yml") is False
    assert (repo / ".codexspec/config.yml").read_bytes() == before
    assert str(dest) in result.output


@pytest.mark.parametrize(
    "body",
    [
        'workflow: {auto_maintenance: "false"}',
        "workflow: {auto_maintenance: null}",
        "workflow: [false]",
        "workflow: {auto_maintenance: false, auto_maintenance: true}",
        "workflow: [",
    ],
)
def test_p05_invalid_stored_policy(tmp_path, body):
    with pytest.raises((AutomationError, ValueError)):
        read_auto_maintenance(config_file(tmp_path, body))


@pytest.mark.parametrize("kind", ["dangling", "cycle"])
def test_p06_present_unreadable_link_refuses_policy(tmp_path, kind):
    config = tmp_path / ".codexspec/config.yml"
    config.parent.mkdir()
    target = tmp_path / "missing.yml" if kind == "dangling" else config
    try:
        config.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable on this host")
    assert config.is_symlink() and not config.exists()
    link_before = config.readlink()
    with pytest.raises(AutomationError):
        read_auto_maintenance(config)
    assert config.is_symlink() and config.readlink() == link_before


@pytest.mark.parametrize("value", [True, False])
def test_p06_readable_link_preserves_explicit_policy(tmp_path, value):
    target = config_file(tmp_path, f"workflow: {{auto_maintenance: {str(value).lower()}}}")
    config = tmp_path / "linked-config.yml"
    try:
        config.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable on this host")
    before = target.read_bytes()
    link_before = config.readlink()
    assert read_auto_maintenance(config) is value
    assert target.read_bytes() == before
    assert config.is_symlink() and config.readlink() == link_before
