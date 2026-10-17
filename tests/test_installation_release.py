import json
import sys

import pytest

from codexspec.installations.release import Release, acquire_release, resolve_latest, validate_worker_result


def test_t06_s01_resolve_stable(monkeypatch):
    import httpx

    payload = {
        "releases": {
            "1.0": [{"yanked": False}],
            "1.1": [{"yanked": False}],
            "2.0rc1": [{"yanked": False}],
            "1.2": [{"yanked": True}],
            "3.0": [],
        }
    }
    monkeypatch.setattr(
        httpx,
        "get",
        lambda *a, **k: httpx.Response(200, json=payload, request=httpx.Request("GET", "https://pypi.org")),
    )
    assert resolve_latest() == "1.1"


def test_t06_s02_acquisition_failure_no_project_mutation(tmp_path, monkeypatch):
    from codexspec.installations import release

    monkeypatch.setattr(release, "resolve_latest", lambda: "1.2.3")
    monkeypatch.setattr(
        release, "run_process", lambda *a, **k: (_ for _ in ()).throw(ValueError("runtime unavailable"))
    )
    before = list(tmp_path.iterdir())
    with pytest.raises(ValueError):
        with acquire_release():
            pytest.fail("acquisition succeeded")
    assert list(tmp_path.iterdir()) == before


def test_t06_s03_s04_real_worker_renders_outside_project(tmp_path):
    from codexspec import __version__

    project = tmp_path / "project"
    project.mkdir()
    (project / "AGENTS.md").write_text("# Project\nMy custom rules.\n")
    release = Release(__version__, sys.executable)
    files = release.render(project, "codex", "zh-CN")
    assert b"My custom rules." in files["AGENTS.md"]
    assert "讨论、确认并固化权威的需求记录" in files[".agents/skills/codexspec-specify/SKILL.md"].decode("utf-8")
    assert sorted(p.name for p in project.iterdir()) == ["AGENTS.md"]


@pytest.mark.parametrize(
    "payload",
    [
        {"protocol": 2, "version": "1.2.3", "files": {".codexspec/scripts/common.sh": "YQ=="}},
        {"protocol": 1, "version": "0.1", "files": {".codexspec/scripts/common.sh": "YQ=="}},
        {"protocol": 1, "version": "1.2.3", "files": {"../outside": "YQ=="}},
    ],
)
def test_t06_s05_refuse_worker_results(payload):
    with pytest.raises(ValueError):
        validate_worker_result(json.dumps(payload).encode(), "1.2.3")


@pytest.mark.parametrize("ai", ["claude", "both"])
def test_t06_s04_s06_worker_integrations_and_cleanup(tmp_path, monkeypatch, ai):
    from codexspec import __version__
    from codexspec.installations import release

    original = release.run_process
    outputs = []

    def run(command, **kwargs):
        outputs.append(kwargs["cwd"])
        original(command, **kwargs)

    monkeypatch.setattr(release, "run_process", run)
    (tmp_path / "CLAUDE.md").write_text("# Project\nCustom rules\n")
    (tmp_path / ".codexspec").mkdir()
    config = tmp_path / ".codexspec/config.yml"
    config.write_text("project: {ai: both}\n")
    files = Release(__version__, sys.executable).render(tmp_path, ai, "en")
    assert b"Custom rules" in files["CLAUDE.md"]
    assert ".claude/commands/codexspec/specify.md" in files
    assert (".agents/skills/codexspec-specify/SKILL.md" in files) == (ai == "both")
    assert config.read_text() == "project: {ai: both}\n"
    assert outputs and all(not path.exists() for path in outputs)


@pytest.mark.parametrize("payload", [None, {}, {"releases": []}, {"releases": {"1.0": [{"yanked": True}]}}])
def test_t06_s02_invalid_release_data(monkeypatch, payload):
    import httpx

    monkeypatch.setattr(
        httpx,
        "get",
        lambda *a, **k: httpx.Response(200, json=payload, request=httpx.Request("GET", "https://pypi.org")),
    )
    with pytest.raises(ValueError):
        resolve_latest()


def test_t06_s02_network_error(monkeypatch):
    import httpx

    monkeypatch.setattr(httpx, "get", lambda *a, **k: (_ for _ in ()).throw(httpx.ConnectError("offline")))
    with pytest.raises(httpx.ConnectError):
        with acquire_release():
            pytest.fail("offline acquisition succeeded")


def test_t06_s05_nonzero_worker_and_corrupt_result(tmp_path):
    from codexspec.installations.release import run_process

    with pytest.raises(ValueError, match="exit 7"):
        run_process([sys.executable, "-c", "raise SystemExit(7)"], cwd=tmp_path)
    with pytest.raises(ValueError):
        validate_worker_result(b"{bad json", "1.2.3")


@pytest.mark.parametrize("fail_install", [False, True])
def test_t06_s01_s02_s06_pinned_runtime_and_cleanup(tmp_path, monkeypatch, fail_install):
    from codexspec.installations import release

    versions = []
    commands = []
    roots = []

    def resolve():
        versions.append("resolved")
        return "1.2.3"

    def run(command, *, cwd, **kwargs):
        commands.append(command)
        roots.append(cwd)
        assert not cwd.is_relative_to(tmp_path)
        if "pip" in command and fail_install:
            raise ValueError("dependency installation failed")

    probes = []

    def render(self, project, ai, language):
        probes.append((self.version, project, ai, language))
        return {".codexspec/scripts/common.sh": b"new\n"}

    monkeypatch.setattr(release, "resolve_latest", resolve)
    monkeypatch.setattr(release, "run_process", run)
    monkeypatch.setattr(release.Release, "render", render)
    if fail_install:
        with pytest.raises(ValueError, match="dependency"):
            with acquire_release():
                pytest.fail("failed installation yielded a runtime")
        assert not probes
    else:
        with acquire_release() as target:
            assert target.version == "1.2.3"
            assert probes[0][0] == "1.2.3"
            assert probes[0][1].exists()
    assert versions == ["resolved"]
    assert commands[1][-1] == "codexspec==1.2.3"
    assert "--index-url" in commands[1]
    assert roots and all(not root.exists() for root in roots)
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize("boundary", ["worker", "provider"])
def test_t06_s02_s05_deep_json_is_reportable(monkeypatch, boundary):
    import httpx

    raw = b"[" * 10_000 + b"0" + b"]" * 10_000
    if boundary == "worker":
        with pytest.raises(ValueError, match="nesting"):
            validate_worker_result(raw, "1.2.3")
    else:
        monkeypatch.setattr(
            httpx,
            "get",
            lambda *a, **k: httpx.Response(200, content=raw, request=httpx.Request("GET", "https://pypi.org")),
        )
        with pytest.raises(ValueError, match="nesting"):
            resolve_latest()
