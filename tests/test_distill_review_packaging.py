"""Installed-distribution gates for the offline distill-review runtime."""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from tests.test_package_contents import _sdist_members, _wheel_members

ROOT = Path(__file__).parent.parent
RUNTIME_ROOT = ROOT / "src" / "codexspec" / "distill_review"


def _distribution_paths() -> tuple[Path, Path]:
    dist_value = os.environ.get("CODEXSPEC_DIST_DIR")
    if not dist_value:
        pytest.skip("set CODEXSPEC_DIST_DIR to validate freshly built distill-review packages")
    dist = Path(dist_value).resolve()
    wheels = list(dist.glob("*.whl"))
    sdists = list(dist.glob("*.tar.gz"))
    assert len(wheels) == 1
    assert len(sdists) == 1
    return wheels[0], sdists[0]


def _expected_runtime() -> dict[str, bytes]:
    return {
        path.relative_to(RUNTIME_ROOT).as_posix(): path.read_bytes()
        for path in sorted(RUNTIME_ROOT.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def _packaged_runtime(members: dict[str, bytes]) -> dict[str, bytes]:
    marker = "/codexspec/distill_review/"
    packaged: dict[str, bytes] = {}
    for name, content in members.items():
        normalized = f"/{name}"
        if marker in normalized:
            packaged[normalized.split(marker, 1)[1]] = content
    return packaged


def test_built_archives_contain_complete_distill_review_runtime() -> None:
    wheel, sdist = _distribution_paths()
    expected = _expected_runtime()
    for members in (_wheel_members(wheel), _sdist_members(sdist)):
        packaged = _packaged_runtime(members)
        assert set(packaged) == set(expected)
        assert packaged == expected
        assert not any("/internal/" in f"/{name}" or "/scripts/python/" in f"/{name}" for name in members)


def test_installed_wheel_initializes_and_runs_offline_review(tmp_path: Path) -> None:
    wheel, _ = _distribution_paths()
    environment = tmp_path / "installed-wheel"
    if importlib.util.find_spec("pip") is not None:
        install = [sys.executable, "-m", "pip", "install", "--force-reinstall"]
    else:
        uv = shutil.which("uv")
        assert uv is not None, "installed-distribution gate requires pip or uv"
        install = [uv, "pip", "install", "--reinstall"]
    subprocess.run(
        [*install, "--target", str(environment), "--no-index", "--no-deps", str(wheel)],
        check=True,
        capture_output=True,
        text=True,
    )
    installed_env = os.environ.copy()
    installed_env["PYTHONPATH"] = str(environment)
    cli = [sys.executable, "-c", "from codexspec import main; main()"]
    imported = subprocess.run(
        [sys.executable, "-c", "import codexspec; print(codexspec.__file__)"],
        check=True,
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=installed_env,
    ).stdout.strip()
    assert str(environment) in imported
    assert str(ROOT / "src") not in imported

    project = tmp_path / "installed-project"
    init = subprocess.run(
        [*cli, "init", str(project), "--ai", "codex", "--no-git", "--force", "--lang", "en"],
        check=True,
        capture_output=True,
        text=True,
        cwd=tmp_path,
        env=installed_env,
    )
    assert init.returncode == 0
    assert (project / ".codexspec/.gitignore").read_text(encoding="utf-8").count(".runtime/") == 1

    record_id = "P-2026-0929-1200aa-1"
    record = project / ".codexspec/profile/pitfalls" / f"{record_id}-installed-review.md"
    record.write_text(
        f"### {record_id}: Installed review\n\n"
        "- claim: The installed runtime can review this record.\n"
        "- type: pitfall\n"
        "- scope/when: installed package review\n"
        "- root-cause: Package assets may be omitted.\n"
        "- workaround: Validate the installed artifact.\n"
        "- lesson: Test the shipped package.\n"
        '- evidence.facts: "installed fixture"\n'
        "- evidence.state: observed but not yet verified\n"
        "- provenance: packaging gate\n"
        "- status: candidate\n",
        encoding="utf-8",
    )
    guard = tmp_path / "network-guard"
    guard.mkdir()
    (guard / "sitecustomize.py").write_text(
        "import socket\n"
        "_connect = socket.socket.connect\n"
        "def guarded(self, address):\n"
        "    host = address[0] if isinstance(address, tuple) else ''\n"
        "    if host not in {'127.0.0.1', '::1', 'localhost'}:\n"
        "        raise RuntimeError(f'external network disabled: {address!r}')\n"
        "    return _connect(self, address)\n"
        "socket.socket.connect = guarded\n",
        encoding="utf-8",
    )
    child_env = installed_env.copy()
    child_env["PYTHONPATH"] = os.pathsep.join((str(guard), str(environment)))
    for key in list(child_env):
        if key.lower().endswith("_proxy") or key.lower() == "no_proxy":
            child_env.pop(key)
    review = subprocess.run(
        [*cli, "_distill-review-helper", "--project-root", str(project), "--mode", "text"],
        input="v\n完整测试套件已通过。\ny\na\n",
        check=True,
        capture_output=True,
        text=True,
        cwd=project,
        env=child_env,
    )
    assert '"status":"applied"' in review.stdout
    assert "- status: vetted" in record.read_text(encoding="utf-8")
