import subprocess
import sys
from contextlib import contextmanager

import pytest
from rich.console import Console
from typer.testing import CliRunner

from codexspec import __version__, app, get_scripts_dir
from codexspec.installations import cli
from codexspec.installations.metadata import METADATA, inspect_installation
from codexspec.installations.release import Release


@pytest.fixture(autouse=True)
def invoking_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)


def test_t07_s01_s06_scan_offline(tmp_path, monkeypatch):
    (tmp_path / "project/.codexspec").mkdir(parents=True)
    monkeypatch.setattr(cli, "acquire_release", lambda: (_ for _ in ()).throw(AssertionError("network")))
    result = CliRunner().invoke(app, ["scan", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "unknown" in result.output.lower()
    assert not (tmp_path / "project" / METADATA).exists()


def test_t07_s04_invalid_modes(tmp_path):
    runner = CliRunner()
    assert runner.invoke(app, ["scan", str(tmp_path), "--yes"]).exit_code == 2
    assert runner.invoke(app, ["scan", str(tmp_path), "--upgrade"]).exit_code == 2


def test_t07_s03_s05_real_bulk_upgrade_and_skip(tmp_path, monkeypatch):
    runner = CliRunner()
    for name in ["clean", "dirty"]:
        project = tmp_path / name
        assert runner.invoke(app, ["init", str(project), "--ai", "codex", "--lang", "en"]).exit_code == 0
        (project / METADATA).unlink()
        command = project / ".agents/skills/codexspec-specify/SKILL.md"
        command.write_text("old committed command\n")
        subprocess.run(["git", "-C", str(project), "add", "."], check=True, capture_output=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(project),
                "-c",
                "user.name=Test",
                "-c",
                "user.email=test@example.invalid",
                "commit",
                "-m",
                "initial",
            ],
            check=True,
            capture_output=True,
        )
        if name == "dirty":
            command.write_text("uncommitted user work\n")

    @contextmanager
    def acquire():
        yield Release(__version__, sys.executable)

    monkeypatch.setattr(cli, "acquire_release", acquire)
    result = runner.invoke(app, ["scan", str(tmp_path), "--upgrade", "--yes"])
    assert result.exit_code == 1, result.output
    assert inspect_installation(tmp_path / "clean").state == "consistent", result.output
    assert not (tmp_path / "dirty" / METADATA).exists()
    assert (tmp_path / "dirty/.agents/skills/codexspec-specify/SKILL.md").read_text() == "uncommitted user work\n"
    assert "1 upgraded" in result.output


@pytest.fixture
def small_projects(tmp_path, monkeypatch):
    for name in ["a", "b", "c"]:
        root = tmp_path / name
        (root / ".codexspec/scripts").mkdir(parents=True)
        (root / ".codexspec/scripts/common.sh").write_bytes(b"old\n")
        (root / ".codexspec/config.yml").write_text("project: {ai: codex}\n")
        for args in [
            ["init"],
            ["add", "."],
            ["-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "initial"],
        ]:
            subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)

    class Target:
        version = "1.2.3"

        def render(self, *args):
            return {".codexspec/scripts/common.sh": b"new\n"}

    calls = []

    @contextmanager
    def acquire():
        calls.append("acquire")
        yield Target()

    monkeypatch.setattr(cli, "acquire_release", acquire)
    monkeypatch.setattr(cli, "is_interactive", lambda: True)
    return tmp_path, calls


@pytest.mark.parametrize(
    ("answers", "changed", "exit_code"), [("y\nn\ny\n", ["a", "c"], 0), ("a\n", ["a", "b", "c"], 0), ("q\n", [], 1)]
)
def test_t07_s02_selection(small_projects, answers, changed, exit_code):
    root, calls = small_projects
    result = CliRunner().invoke(app, ["scan", str(root), "--upgrade"], input=answers)
    assert result.exit_code == exit_code, result.output
    assert calls == ["acquire"]
    for name in ["a", "b", "c"]:
        assert (root / name / METADATA).exists() == (name in changed)
        assert (root / name / ".codexspec/scripts/common.sh").read_bytes() == (
            b"new\n" if name in changed else b"old\n"
        )


def test_t07_s02_all_still_protects_dirty_project(small_projects):
    root, _ = small_projects
    dirty = root / "b/.codexspec/scripts/common.sh"
    dirty.write_bytes(b"user work\n")
    result = CliRunner().invoke(app, ["scan", str(root), "--upgrade"], input="a\n")
    assert result.exit_code == 1, result.output
    assert (root / "a" / METADATA).exists()
    assert (root / "c" / METADATA).exists()
    assert not (root / "b" / METADATA).exists()
    assert dirty.read_bytes() == b"user work\n"


def test_t07_s05_failure_continues(small_projects, monkeypatch):
    root, _ = small_projects
    apply = cli.apply_plan

    def fail_one(plan):
        if plan.root.name == "a":
            raise OSError("disk full")
        return apply(plan)

    monkeypatch.setattr(cli, "apply_plan", fail_one)
    result = CliRunner().invoke(app, ["scan", str(root), "--upgrade", "--yes"])
    assert result.exit_code == 1
    assert "1 failed" in result.output
    assert (root / "b" / METADATA).exists() and (root / "c" / METADATA).exists()


@pytest.mark.parametrize(("language", "expected"), [("zh-CN", "未发现"), ("xx", "No CodexSpec")])
def test_t07_s06_s07_empty_and_language(tmp_path, monkeypatch, language, expected):
    config = tmp_path / ".codexspec/config.yml"
    config.parent.mkdir()
    config.write_text(f"language:\n  interaction: {language}\n")
    empty = tmp_path / "empty"
    empty.mkdir()
    result = CliRunner().invoke(app, ["scan", str(empty)])
    assert result.exit_code == 0
    assert expected in result.output
    assert not (empty / ".codexspec").exists()


@pytest.mark.parametrize("columns", [64, 80, 120])
def test_t07_s06_incomplete_and_content_mismatch(small_projects, monkeypatch, columns):
    monkeypatch.setenv("COLUMNS", str(columns))
    root, _ = small_projects
    assert CliRunner().invoke(app, ["scan", str(root), "--upgrade", "--yes"]).exit_code == 0
    (root / "a/.codexspec/scripts/common.sh").write_bytes(b"discarded\n")
    discover = cli.discover

    def incomplete(path):
        result = discover(path)
        result.issues.append("unreadable child")
        return result

    monkeypatch.setattr(cli, "discover", incomplete)
    result = CliRunner().invoke(app, ["scan", str(root)])
    assert result.exit_code == 1
    output = " ".join(result.output.split())
    assert "Scan incomplete" in output
    assert "missing or changed" in output
    assert "codexspec scan <path> --upgrade" in output


def test_t07_s05_input_changed_during_render_is_not_applied(small_projects, monkeypatch):
    root, _ = small_projects

    class Target:
        version = "1.2.3"

        def render(self, project, *args):
            (project / ".codexspec/config.yml").write_text("project: {ai: both}\n")
            return {".codexspec/scripts/common.sh": b"new\n"}

    @contextmanager
    def acquire():
        yield Target()

    monkeypatch.setattr(cli, "acquire_release", acquire)
    result = CliRunner().invoke(app, ["scan", str(root), "--upgrade", "--yes"])
    assert result.exit_code == 1
    assert all(not (root / name / METADATA).exists() for name in ["a", "b", "c"])


@pytest.mark.parametrize("legacy_windows", [False, True])
def test_t07_s06_long_installation_paths_remain_visible(tmp_path, monkeypatch, legacy_windows):
    monkeypatch.setattr("codexspec.console", Console(width=80, legacy_windows=legacy_windows))
    project = tmp_path / ("long-parent-" * 6) / "installed-project"
    (project / ".codexspec").mkdir(parents=True)
    result = CliRunner().invoke(app, ["scan", str(tmp_path)])
    lines = result.output.splitlines()
    body_start = next(i for i, line in enumerate(lines) if line.startswith(("├", "┡")))
    path_column = "".join(line.split("│")[2].strip() for line in lines[body_start + 1 :] if line.startswith("│"))
    assert path_column == str(project), result.output


def test_t07_s02_edits_while_prompting_are_reported_as_skip(small_projects, monkeypatch):
    root, _ = small_projects
    path = root / "a/.codexspec/scripts/common.sh"

    def choose(*args, **kwargs):
        path.write_bytes(b"user edit while choosing\n")
        return "a"

    monkeypatch.setattr(cli.Prompt, "ask", choose)
    result = CliRunner().invoke(app, ["scan", str(root), "--upgrade"])
    assert result.exit_code == 1
    assert "1 skipped; 0 failed" in result.output
    assert path.read_bytes() == b"user edit while choosing\n"
    assert not (root / "a" / METADATA).exists()


@pytest.mark.parametrize("boundary", ["metadata", "configuration"])
def test_t07_s05_deep_project_input_does_not_abort_siblings(small_projects, boundary):
    root, _ = small_projects
    project = root / "a"
    name = METADATA if boundary == "metadata" else ".codexspec/config.yml"
    (project / name).write_text("[" * 10_000 + "0" + "]" * 10_000)
    if boundary == "metadata":
        scan = CliRunner().invoke(app, ["scan", str(root)])
        assert scan.exception is None, repr(scan.exception)
        assert {item.path for item in cli.discover(root).installations} == {root / name for name in ("a", "b", "c")}
        assert "nesting" in scan.output
    result = CliRunner().invoke(app, ["scan", str(root), "--upgrade", "--yes"])
    assert result.exit_code == 1, result.output
    assert "1 skipped" in result.output
    assert "nesting" in result.output
    assert (project / name).read_text() == "[" * 10_000 + "0" + "]" * 10_000
    assert (project / ".codexspec/scripts/common.sh").read_bytes() == b"old\n"
    assert (root / "b" / METADATA).exists() and (root / "c" / METADATA).exists()


@pytest.mark.parametrize("path_form", ["parent", "result.json"])
def test_t06_s04_t07_s03_valid_project_paths(small_projects, monkeypatch, path_form):
    root, _ = small_projects
    project = root / "a"
    if path_form == "parent":
        child = project / "child"
        child.mkdir()
        monkeypatch.chdir(child)
        argument = ".."
    else:
        project = project.rename(root / path_form)
        argument = str(project)

    @contextmanager
    def acquire():
        yield Release(__version__, sys.executable)

    monkeypatch.setattr(cli, "acquire_release", acquire)
    result = CliRunner().invoke(app, ["scan", argument, "--upgrade", "--yes"])
    assert result.exit_code == 0, result.output
    assert inspect_installation(project).state == "consistent", result.output
    platform_dir, script_name = ("powershell", "common.ps1") if sys.platform == "win32" else ("bash", "common.sh")
    assert (project / ".codexspec/scripts" / script_name).read_bytes() == (
        get_scripts_dir() / platform_dir / script_name
    ).read_bytes()
    assert (project / ".agents/skills/codexspec-specify/SKILL.md").is_file()
    for name in ["b", "c"]:
        assert not (root / name / METADATA).exists()
        assert (root / name / ".codexspec/scripts/common.sh").read_bytes() == b"old\n"
