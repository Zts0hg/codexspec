"""Installation contracts for the design-to-plan rename (feature scenarios S1, S4-S9)."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from codexspec import app, get_templates_dir
from codexspec.commands.installer import get_commands_metadata, install_commands_to_subdir
from codexspec.integrations.codex import CodexIntegration

OLD = "spec-to-plan"
NEW = "design-to-plan"


def entry(root, integration, name):
    if integration == "claude":
        return root / ".claude" / "commands" / "codexspec" / f"{name}.md"
    return root / ".agents" / "skills" / f"codexspec-{name}" / "SKILL.md"


def seed(path, content="old planner"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def install(root, integration, templates, force=False):
    if integration == "claude":
        return install_commands_to_subdir(entry(root, integration, NEW).parent, templates, force=force)
    return CodexIntegration().install_skills(root, templates, force=force)


@pytest.fixture
def templates(tmp_path):
    result = tmp_path / "templates"
    seed(result / f"{NEW}.md", "---\ndescription: Build the design\n---\n# Design to Plan Converter\n")
    return result


def test_registry_replaces_old_identity():
    names = [item["name"] for item in get_commands_metadata()]
    assert NEW in names
    assert OLD not in names
    assert names.index("spec-to-design") + 1 == names.index(NEW)
    assert names.index(NEW) + 1 == names.index("plan-to-tasks")


@pytest.mark.parametrize("integration", ["claude", "codex"])
def test_fresh_distribution_has_only_new_entry(tmp_path, integration):
    install(tmp_path, integration, get_templates_dir() / "commands")
    assert entry(tmp_path, integration, NEW).is_file()
    assert not entry(tmp_path, integration, OLD).exists()


@pytest.mark.parametrize("integration", ["claude", "codex"])
@pytest.mark.parametrize("force", [False, True])
def test_update_retires_entry_and_preserves_unrelated_files(tmp_path, templates, integration, force):
    old = entry(tmp_path, integration, OLD)
    seed(old)
    unrelated = entry(tmp_path, integration, "custom")
    seed(unrelated, "keep command")
    resource = old.parent / "notes.txt"
    seed(resource, "keep resource")
    install(tmp_path, integration, templates, force)
    install(tmp_path, integration, templates, force)
    assert not old.exists()
    assert entry(tmp_path, integration, NEW).is_file()
    assert unrelated.read_text() == "keep command"
    assert resource.read_text() == "keep resource"


@pytest.mark.parametrize("integration", ["claude", "codex"])
def test_partial_distribution_does_not_retire_entry(tmp_path, templates, integration):
    old = entry(tmp_path, integration, OLD)
    seed(old)
    (templates / f"{NEW}.md").unlink()
    seed(templates / "other.md", "# Other")
    install(tmp_path, integration, templates)
    assert old.read_text() == "old planner"


@pytest.mark.parametrize("integration", ["claude", "codex"])
def test_replacement_write_failure_preserves_old_entry(tmp_path, templates, integration, monkeypatch):
    old = entry(tmp_path, integration, OLD)
    new = entry(tmp_path, integration, NEW)
    seed(old)
    original = Path.write_text

    def fail_new(path, *args, **kwargs):
        if path == new:
            raise PermissionError("replacement write denied")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", fail_new)
    with pytest.raises(PermissionError, match="replacement write denied"):
        install(tmp_path, integration, templates)
    assert old.read_text() == "old planner"


@pytest.mark.parametrize("integration", ["claude", "codex"])
def test_retirement_failure_is_not_silenced(tmp_path, templates, integration, monkeypatch):
    old = entry(tmp_path, integration, OLD)
    seed(old)
    original = Path.unlink

    def fail_old(path, *args, **kwargs):
        if path == old:
            raise PermissionError("retirement denied")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "unlink", fail_old)
    with pytest.raises(PermissionError, match="retirement denied"):
        install(tmp_path, integration, templates)
    assert old.read_text() == "old planner"


@pytest.mark.parametrize("integration", ["claude", "codex"])
def test_retirement_entry_symlink_does_not_delete_target(tmp_path, templates, integration):
    old = entry(tmp_path, integration, OLD)
    target = tmp_path / "external.md"
    seed(target, "external")
    old.parent.mkdir(parents=True)
    try:
        old.symlink_to(target)
    except OSError:
        pytest.skip("symlinks unavailable")
    install(tmp_path, integration, templates)
    assert not old.is_symlink()
    assert target.read_text() == "external"


@pytest.mark.parametrize("integration", ["claude", "codex"])
def test_linked_retirement_parent_is_refused(tmp_path, templates, integration):
    root = tmp_path / "project"
    old = entry(root, integration, OLD)
    external = tmp_path / "external"
    external.mkdir()
    external_old = external / old.name
    seed(external_old)
    old.parent.parent.mkdir(parents=True)
    try:
        old.parent.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(OSError, match="[Ss]ymlink|[Ss]ymbolic"):
        install(root, integration, templates)
    assert external_old.read_text() == "old planner"


@pytest.mark.parametrize("selected", ["claude", "codex", "both"])
def test_cli_update_retires_only_selected_integrations(tmp_path, selected):
    root = tmp_path / "project"
    for integration in ("claude", "codex"):
        seed(entry(root, integration, OLD))
    result = CliRunner().invoke(app, ["init", str(root), "--force", "--ai", selected, "--lang", "en"])
    assert result.exit_code == 0, result.output
    for integration in ("claude", "codex"):
        if selected in (integration, "both"):
            assert not entry(root, integration, OLD).exists()
            assert entry(root, integration, NEW).exists()
        else:
            assert entry(root, integration, OLD).read_text() == "old planner"
            assert not entry(root, integration, NEW).exists()


@pytest.mark.parametrize("integration", ["claude", "codex"])
def test_alias_above_installation_root_is_supported(tmp_path, templates, integration):
    actual = tmp_path / "actual"
    actual.mkdir()
    alias = tmp_path / "alias"
    try:
        alias.symlink_to(actual, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    root = alias / "project"
    seed(entry(root, integration, OLD))
    install(root, integration, templates)
    assert not entry(actual / "project", integration, OLD).exists()
    assert entry(actual / "project", integration, NEW).is_file()


@pytest.mark.parametrize("integration", ["claude", "codex"])
@pytest.mark.parametrize("force", [False, True])
def test_non_file_replacement_reports_failure(tmp_path, templates, integration, force):
    old = entry(tmp_path, integration, OLD)
    new = entry(tmp_path, integration, NEW)
    seed(old)
    seed(new / "keep.txt", "occupied directory")
    with pytest.raises(OSError):
        install(tmp_path, integration, templates, force)
    assert old.read_text() == "old planner"
    assert (new / "keep.txt").read_text() == "occupied directory"


@pytest.mark.parametrize("integration", ["claude", "codex"])
@pytest.mark.parametrize("force", [False, True])
def test_replacement_link_to_old_entry_reports_failure(tmp_path, templates, integration, force):
    old = entry(tmp_path, integration, OLD)
    new = entry(tmp_path, integration, NEW)
    seed(old)
    new.parent.mkdir(parents=True, exist_ok=True)
    try:
        new.symlink_to(old)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(OSError):
        install(tmp_path, integration, templates, force)
    assert old.read_text() == "old planner"
    assert new.is_symlink()


@pytest.mark.parametrize("force", [False, True])
def test_replacement_skill_directory_link_reports_failure(tmp_path, templates, force):
    old = entry(tmp_path, "codex", OLD)
    new = entry(tmp_path, "codex", NEW)
    seed(old)
    try:
        new.parent.symlink_to(old.parent, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(OSError):
        install(tmp_path, "codex", templates, force)
    assert old.read_text() == "old planner"
    assert new.parent.is_symlink()
