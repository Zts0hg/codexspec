"""Distribution contract tests for project-local review helpers."""

import os
import tarfile
import zipfile
from io import BytesIO
from pathlib import Path

import pytest

from internal.command_template_fragments import has_fragment_directive_line, portable_name_key

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
        members: dict[str, bytes] = {}
        for name in archive.namelist():
            if name.endswith("/"):
                continue
            assert name not in members, f"duplicate archive member path: {name}"
            members[name] = archive.read(name)
        return members


def _sdist_members(path: Path) -> dict[str, bytes]:
    members: dict[str, bytes] = {}
    with tarfile.open(path, "r:gz") as archive:
        for member in archive.getmembers():
            if not member.isfile():
                continue
            assert member.name not in members, f"duplicate archive member path: {member.name}"
            extracted = archive.extractfile(member)
            assert extracted is not None
            members[member.name] = extracted.read()
    return members


def _expected_command_templates() -> dict[str, bytes]:
    commands = ROOT / "templates" / "commands"
    return {path.name: path.read_bytes() for path in sorted(commands.glob("*.md"))}


def _assert_packaged_commands(members: dict[str, bytes], expected: dict[str, bytes]) -> None:
    packaged: dict[str, bytes] = {}
    marker = "/templates/commands/"
    for archive_name, content in members.items():
        normalized = f"/{archive_name}"
        if marker not in normalized:
            continue
        command_path = normalized.split(marker, 1)[1]
        assert command_path and "/" not in command_path, f"unexpected command archive path: {archive_name}"
        assert command_path not in packaged, f"duplicate command archive path: {archive_name}"
        packaged[command_path] = content
    assert set(packaged) == set(expected), (
        f"packaged command set drifted; missing={sorted(set(expected) - set(packaged))}, "
        f"unexpected={sorted(set(packaged) - set(expected))}"
    )
    portable_names = [portable_name_key(name) for name in packaged]
    assert len(portable_names) == len(set(portable_names)), "portable command names collide"
    for name, expected_content in expected.items():
        assert packaged[name] == expected_content, f"packaged command bytes drifted: {name}"
        assert not has_fragment_directive_line(packaged[name]), f"unresolved fragment directive packaged: {name}"


def _assert_internal_authoring_absent(members: dict[str, bytes]) -> None:
    forbidden = [
        name
        for name in members
        if "/internal/command_templates/" in f"/{name}" or name.endswith("/internal/command_template_fragments.py")
    ]
    assert not forbidden, f"maintainer-only fragment authoring files were packaged: {forbidden}"


@pytest.mark.parametrize(
    ("defect", "expected_failure"),
    [
        ("missing", "packaged command set drifted"),
        ("unexpected", "packaged command set drifted"),
        ("stale", "packaged command bytes drifted: two\\.md"),
        ("directive", "unresolved fragment directive packaged: two\\.md"),
        ("near-miss-directive", "unresolved fragment directive packaged: two\\.md"),
        ("namespace-comment", "unresolved fragment directive packaged: two\\.md"),
        ("bom-directive", "unresolved fragment directive packaged: two\\.md"),
    ],
)
def test_packaged_command_validation_rejects_distribution_drift(defect: str, expected_failure: str) -> None:
    expected = {"one.md": b"one\n", "two.md": b"two\n"}
    members = {
        "package/templates/commands/one.md": b"one\n",
        "package/templates/commands/two.md": b"two\n",
    }
    if defect == "missing":
        members.pop("package/templates/commands/two.md")
    elif defect == "unexpected":
        members["package/templates/commands/extra.md"] = b"extra\n"
    elif defect == "stale":
        members["package/templates/commands/two.md"] = b"stale\n"
    elif defect == "directive":
        members["package/templates/commands/two.md"] = b"<!-- CODEXSPEC:INCLUDE two.md -->\n"
    elif defect == "near-miss-directive":
        members["package/templates/commands/two.md"] = b"<!--  CODEXSPEC:INCLUDE two.md -->\n"
    elif defect == "bom-directive":
        members["package/templates/commands/two.md"] = b"\xef\xbb\xbf<!-- CODEXSPEC:INCLUDE two.md -->\n"
    elif defect == "namespace-comment":
        members["package/templates/commands/two.md"] = b"<!-- CODEXSPEC fragment note -->\n"
    if defect in {"directive", "near-miss-directive", "namespace-comment", "bom-directive"}:
        # Directive-class defects are byte-consistent with the expectation, so only the
        # standalone-directive guard can reject them; keep the expected bytes identical.
        expected = dict(expected)
        expected["two.md"] = members["package/templates/commands/two.md"]

    with pytest.raises(AssertionError, match=expected_failure):
        _assert_packaged_commands(members, expected)


def test_packaged_command_validation_allows_inline_directive_example() -> None:
    content = b"Example: <!-- CODEXSPEC:INCLUDE shared.md --> stays literal.\n"

    _assert_packaged_commands({"package/templates/commands/one.md": content}, {"one.md": content})


def test_packaged_command_validation_rejects_portable_name_collisions() -> None:
    members = {
        "package/templates/commands/Foo.md": b"one\n",
        "package/templates/commands/foo.md": b"two\n",
    }

    with pytest.raises(AssertionError, match=r"portable command names collide"):
        _assert_packaged_commands(members, {"Foo.md": b"one\n", "foo.md": b"two\n"})


def test_packaged_command_validation_rejects_nested_duplicate_member() -> None:
    members = {
        "package/templates/commands/foo.md": b"same\n",
        "package/templates/commands/nested/foo.md": b"same\n",
    }

    with pytest.raises(AssertionError, match=r"unexpected command archive path"):
        _assert_packaged_commands(members, {"foo.md": b"same\n"})


def test_wheel_member_loader_rejects_exact_duplicate_archive_paths(tmp_path: Path) -> None:
    wheel = tmp_path / "duplicate.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr("package/templates/commands/foo.md", b"old\n")
        with pytest.warns(UserWarning, match=r"Duplicate name"):
            archive.writestr("package/templates/commands/foo.md", b"new\n")

    with pytest.raises(AssertionError, match=r"duplicate archive member path"):
        _wheel_members(wheel)


def test_sdist_member_loader_rejects_exact_duplicate_archive_paths(tmp_path: Path) -> None:
    sdist = tmp_path / "duplicate.tar.gz"
    with tarfile.open(sdist, "w:gz") as archive:
        for content in [b"old\n", b"new\n"]:
            payload = BytesIO(content)
            member = tarfile.TarInfo("package/templates/commands/foo.md")
            member.size = len(content)
            archive.addfile(member, payload)

    with pytest.raises(AssertionError, match=r"duplicate archive member path"):
        _sdist_members(sdist)


def test_built_archives_contain_resolvers_and_all_current_command_templates() -> None:
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
    expected_commands = _expected_command_templates()

    for members in [_wheel_members(wheels[0]), _sdist_members(sdists[0])]:
        assert _archive_member(members, "/scripts/bash/review-context.sh") == expected_bash
        assert _archive_member(members, "/scripts/powershell/review-context.ps1") == expected_powershell
        _assert_packaged_commands(members, expected_commands)
        _assert_internal_authoring_absent(members)
        packaged_review = _archive_member(members, "/templates/commands/review-code.md")
        assert b"strict defect gate" in packaged_review
        assert b"review-code --audit {paths}" in packaged_review
