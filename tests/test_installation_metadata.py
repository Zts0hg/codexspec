import json

import pytest

from codexspec.installations.metadata import inspect_installation, publish_metadata
from codexspec.installations.render import render_installation


def install_files(root, files):
    for name, data in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)


@pytest.mark.parametrize("ai", ["claude", "codex", "both"])
def test_t01_s01_s02_render_and_verify(tmp_path, ai):
    files = render_installation(tmp_path, ai, "zh-CN")
    for name, content in files.items():
        if name.endswith("/specify.md") or name.endswith("codexspec-specify/SKILL.md"):
            assert "澄清功能目标、范围和约束，将确认的需求整理为 requirements.md。" in content.decode("utf-8")
    assert any(name.startswith(".codexspec/scripts/") for name in files)
    install_files(tmp_path, files)
    publish_metadata(tmp_path, "1.2.3", ai, "zh-CN", files)
    result = inspect_installation(tmp_path)
    assert result.version == "1.2.3"
    assert result.state == "consistent"
    assert bool(list((tmp_path / ".agents/skills").glob("*/SKILL.md"))) == (ai != "claude")
    assert bool(list((tmp_path / ".claude/commands/codexspec").glob("*.md"))) == (ai != "codex")


def test_t01_s03_s04_missing_version_still_checks_content(tmp_path):
    files = {".codexspec/scripts/example.sh": b"echo hello\n"}
    install_files(tmp_path, files)
    publish_metadata(tmp_path, "1.2.3", "claude", "en", files)
    metadata = tmp_path / ".codexspec/installation.json"
    data = json.loads(metadata.read_text())
    del data["installed_version"]
    metadata.write_text(json.dumps(data))
    assert inspect_installation(tmp_path).state == "consistent"
    (tmp_path / next(iter(files))).unlink()
    result = inspect_installation(tmp_path)
    assert result.version is None
    assert result.state == "inconsistent"
    assert next(iter(files)) in result.differences


@pytest.mark.parametrize("bad", ["../outside", "/tmp/outside", ".codexspec/installation.json", "business.py"])
def test_t01_s05_reject_invalid_metadata_paths(tmp_path, bad):
    (tmp_path / ".codexspec").mkdir()
    assert inspect_installation(tmp_path).state == "no_baseline"
    path = tmp_path / ".codexspec/installation.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "representation": "utf8-lf-managed-v1",
                "installed_version": "1",
                "files": {bad: "0" * 64},
            }
        )
    )
    assert inspect_installation(tmp_path).state == "invalid"


def test_t01_s06_custom_context_does_not_change_projection(tmp_path):
    (tmp_path / "AGENTS.md").write_text("# My project\nKeep my rules.\n")
    files = render_installation(tmp_path, "codex", "en")
    assert b"Keep my rules." in files["AGENTS.md"]
    install_files(tmp_path, files)
    publish_metadata(tmp_path, "1.2.3", "codex", "en", files)
    with (tmp_path / "AGENTS.md").open("a") as stream:
        stream.write("\nMore custom rules.\n")
    assert inspect_installation(tmp_path).state == "consistent"


def test_t01_s07_refuse_baseline_over_changed_files(tmp_path):
    files = {".codexspec/scripts/example.sh": b"expected\n"}
    install_files(tmp_path, {next(iter(files)): b"user changes\n"})
    with pytest.raises(ValueError, match="match"):
        publish_metadata(tmp_path, "1.2.3", "claude", "en", files)
    assert not (tmp_path / ".codexspec/installation.json").exists()


@pytest.mark.parametrize("ai", ["claude", "codex", "both"])
def test_t02_s01_s02_init_records_real_release(tmp_path, ai):
    from typer.testing import CliRunner

    from codexspec import __version__, app

    project = tmp_path / ai
    result = CliRunner().invoke(app, ["init", str(project), "--ai", ai, "--no-git", "--lang", "en"])
    assert result.exit_code == 0, result.output
    assert inspect_installation(project).version == __version__
    assert inspect_installation(project).state == "consistent"


def test_t02_s03_s04_nonforce_does_not_bless_edits(tmp_path, monkeypatch):
    from typer.testing import CliRunner

    from codexspec import app

    project = tmp_path / "project"
    runner = CliRunner()
    assert runner.invoke(app, ["init", str(project), "--ai", "codex", "--lang", "en", "--no-git"]).exit_code == 0
    metadata = project / ".codexspec/installation.json"
    before = metadata.read_bytes()
    skill = project / ".agents/skills/codexspec-specify/SKILL.md"
    skill.write_text("my custom command\n")
    constitution = project / ".codexspec/memory/constitution.md"
    constitution.write_text("my constitution\n")
    monkeypatch.chdir(project)
    result = runner.invoke(app, ["init", ".", "--ai", "codex", "--no-git"])
    assert result.exit_code == 0, result.output
    assert metadata.read_bytes() == before
    assert skill.read_text() == "my custom command\n"
    assert constitution.read_text() == "my constitution\n"
    assert inspect_installation(project).state == "inconsistent"


def test_t02_s02_force_replaces_and_records_expected(tmp_path):
    from typer.testing import CliRunner

    from codexspec import app

    project = tmp_path / "project"
    runner = CliRunner()
    assert runner.invoke(app, ["init", str(project), "--ai", "both", "--lang", "en", "--no-git"]).exit_code == 0
    skill = project / ".agents/skills/codexspec-specify/SKILL.md"
    skill.write_text("old command\n")
    assert inspect_installation(project).state == "inconsistent"
    assert runner.invoke(app, ["init", str(project), "--force", "--ai", "both", "--no-git"]).exit_code == 0
    assert inspect_installation(project).state == "consistent"
    assert skill.read_text() != "old command\n"


def test_t02_s05_incomplete_install_does_not_publish(tmp_path, monkeypatch):
    from typer.testing import CliRunner

    from codexspec import app
    from codexspec.integrations.codex import CodexIntegration

    monkeypatch.setattr(CodexIntegration, "install", lambda *a, **k: 0)
    project = tmp_path / "incomplete"
    result = CliRunner().invoke(app, ["init", str(project), "--ai", "codex", "--lang", "en", "--no-git"])
    assert not (project / ".codexspec/installation.json").exists(), result.output


def test_t01_s05_duplicate_metadata_keys_rejected(tmp_path):
    directory = tmp_path / ".codexspec"
    directory.mkdir()
    (directory / "installation.json").write_text('{"schema_version":1,"schema_version":1}')
    assert inspect_installation(tmp_path).state == "invalid"
