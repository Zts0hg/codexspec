"""Distribution contract tests for project-local review helpers."""

import os
import tarfile
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent


def test_review_context_resolvers_exist_in_packaged_script_sources() -> None:
    scripts = ROOT / "scripts"

    assert (scripts / "bash" / "review-context.sh").is_file()
    assert (scripts / "powershell" / "review-context.ps1").is_file()


def test_build_configuration_includes_both_platform_script_trees() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert '"scripts/bash" = "codexspec/scripts/bash"' in pyproject
    assert '"scripts/powershell" = "codexspec/scripts/powershell"' in pyproject
    assert '"/scripts/bash"' in pyproject
    assert '"/scripts/powershell"' in pyproject


def _archive_member(members: dict[str, bytes], suffix: str) -> bytes:
    matches = [content for name, content in members.items() if name.endswith(suffix)]
    assert len(matches) == 1, f"expected exactly one {suffix!r}, found {len(matches)}"
    return matches[0]


def _wheel_members(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in archive.namelist() if not name.endswith("/")}


def _sdist_members(path: Path) -> dict[str, bytes]:
    members: dict[str, bytes] = {}
    with tarfile.open(path, "r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            extracted = archive.extractfile(member)
            assert extracted is not None
            members[member.name] = extracted.read()
    return members


def test_built_archives_contain_resolvers_and_current_review_template() -> None:
    """CI supplies a fresh dist directory after building wheel and sdist."""
    dist_value = os.environ.get("CODEXSPEC_DIST_DIR")
    if not dist_value:
        pytest.skip("set CODEXSPEC_DIST_DIR to inspect freshly built archives")

    dist = Path(dist_value).resolve()
    wheels = list(dist.glob("*.whl"))
    sdists = list(dist.glob("*.tar.gz"))
    assert len(wheels) == 1
    assert len(sdists) == 1

    expected_bash = (ROOT / "scripts" / "bash" / "review-context.sh").read_bytes()
    expected_powershell = (ROOT / "scripts" / "powershell" / "review-context.ps1").read_bytes()
    expected_template = (ROOT / "templates" / "commands" / "review-code.md").read_bytes()

    for members in [_wheel_members(wheels[0]), _sdist_members(sdists[0])]:
        assert _archive_member(members, "/scripts/bash/review-context.sh") == expected_bash
        assert _archive_member(members, "/scripts/powershell/review-context.ps1") == expected_powershell
        packaged_template = _archive_member(members, "/templates/commands/review-code.md")
        assert packaged_template == expected_template
        assert b"strict defect gate" in packaged_template
        assert b"review-code --audit {paths}" in packaged_template
