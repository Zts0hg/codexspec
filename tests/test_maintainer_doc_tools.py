"""Behavior contracts for repo-only documentation maintenance tools."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
import yaml

from codexspec.commands.installer import get_commands_metadata
from codexspec.integrations.claude import ClaudeIntegration
from codexspec.integrations.codex import CodexIntegration
from internal import doc_translation, maintainer_doc_skills
from internal.command_template_fragments import FragmentError, check_self_bootstrap

COMMANDS = ("translate-docs", "check-i18n-semantics", "update-workflow-diagrams")


def seed_entries(root: Path) -> Path:
    root = root.resolve()
    commands = root / ".claude" / "commands" / "codexspec"
    commands.mkdir(parents=True, exist_ok=True)
    for name in COMMANDS:
        (commands / f"{name}.md").write_text(
            f"---\ndescription: Maintain repository docs\n---\n\nRead $ARGUMENTS. Then /codexspec:{name} --readme.\n",
            encoding="utf-8",
        )
    return root


def files(root: Path) -> dict[str, bytes]:
    return {str(path.relative_to(root)): path.read_bytes() for path in root.rglob("*") if path.is_file()}


@pytest.mark.parametrize("changed_command", COMMANDS)
def test_ts001_native_entries_use_existing_renderer_and_source_changes(tmp_path: Path, changed_command: str) -> None:
    root = seed_entries(tmp_path)
    changed = maintainer_doc_skills.sync(root, write=True)
    assert len(changed) == 3
    for name in COMMANDS:
        skill = root / ".agents" / "skills" / f"codexspec-{name}" / "SKILL.md"
        content = skill.read_text()
        frontmatter = yaml.safe_load(content.split("---", 2)[1])
        assert frontmatter["name"] == f"codexspec:{name}"
        assert f"$codexspec:{name} --readme" in content
        assert "$ARGUMENTS" not in content and "/codexspec:" not in content
    source = root / f".claude/commands/codexspec/{changed_command}.md"
    source.write_text(source.read_text() + "\nNew source rule.\n")
    before = files(root)
    with pytest.raises(maintainer_doc_skills.MaintainerSkillError, match="stale"):
        maintainer_doc_skills.sync(root)
    assert files(root) == before
    assert len(maintainer_doc_skills.sync(root, write=True)) == 1
    assert "New source rule." in (root / f".agents/skills/codexspec-{changed_command}/SKILL.md").read_text()


def test_ts002_missing_check_does_not_create_output(tmp_path: Path) -> None:
    root = seed_entries(tmp_path)
    before = files(root)
    with pytest.raises(maintainer_doc_skills.MaintainerSkillError, match="missing"):
        maintainer_doc_skills.sync(root)
    assert files(root) == before and not (root / ".agents").exists()
    maintainer_doc_skills.sync(root, write=True)
    assert maintainer_doc_skills.sync(root) == []


@pytest.mark.parametrize("defect", ["symlink", "hardlink", "directory", "parent_symlink", "parent_file"])
def test_ts003_writer_preflights_all_outputs_before_any_mutation(tmp_path: Path, defect: str) -> None:
    root = seed_entries(tmp_path / "repo")
    maintainer_doc_skills.sync(root, write=True)
    first = root / ".agents/skills/codexspec-check-i18n-semantics/SKILL.md"
    second = root / ".agents/skills/codexspec-translate-docs/SKILL.md"
    source = root / ".claude/commands/codexspec/check-i18n-semantics.md"
    source.write_text(source.read_text() + "\nChanged input.\n")
    original_first = first.read_bytes()
    outside = tmp_path / "outside.md"
    outside.write_text("outside\n")
    second.unlink()
    if defect == "symlink":
        second.symlink_to(outside)
    elif defect == "hardlink":
        os.link(outside, second)
    elif defect == "directory":
        second.mkdir()
    else:
        second.parent.rmdir()
        if defect == "parent_symlink":
            directory = tmp_path / "outside-directory"
            directory.mkdir()
            (directory / "SKILL.md").write_text("outside\n")
            second.parent.symlink_to(directory, target_is_directory=True)
        else:
            second.parent.write_text("not a directory\n")
    with pytest.raises(maintainer_doc_skills.MaintainerSkillError):
        maintainer_doc_skills.sync(root, write=True)
    assert first.read_bytes() == original_first and outside.read_text() == "outside\n"


def test_ts004_public_install_stays_public_only(tmp_path: Path) -> None:
    templates = Path(__file__).resolve().parents[1] / "templates/commands"
    count = CodexIntegration().install_skills(tmp_path, templates, force=True)
    names = {path.name for path in (tmp_path / ".agents/skills").iterdir()}
    assert count == len(get_commands_metadata()) == 28
    assert not {f"codexspec-{name}" for name in COMMANDS} & names
    ClaudeIntegration().install(tmp_path, templates, force=True, language="en")
    claude_names = {path.stem for path in (tmp_path / ".claude/commands/codexspec").glob("*.md")}
    assert not set(COMMANDS) & claude_names


@pytest.mark.parametrize("changed_command", COMMANDS)
def test_ts004_self_bootstrap_verifies_maintainer_entries(tmp_path: Path, changed_command: str) -> None:
    from tests.test_command_template_fragments import _self_bootstrap_fixture

    root = seed_entries(_self_bootstrap_fixture(tmp_path))
    with pytest.raises(FragmentError, match="Codex.*missing"):
        check_self_bootstrap(root, language="en")
    maintainer_doc_skills.sync(root, write=True)
    check_self_bootstrap(root, language="en")
    skill = root / f".agents/skills/codexspec-{changed_command}/SKILL.md"
    skill.write_text("stale\n")
    with pytest.raises(FragmentError, match="Codex.*stale"):
        check_self_bootstrap(root, language="en")
    maintainer_doc_skills.sync(root, write=True)
    unknown = root / ".agents/skills/codexspec-unknown/SKILL.md"
    unknown.parent.mkdir()
    unknown.write_text("unknown\n")
    with pytest.raises(FragmentError, match="Codex.*unexpected"):
        check_self_bootstrap(root, language="en")


def seed_readme(root: Path) -> Path:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    (root / "README.md").write_text(
        "# Guide\n\n- [Setup](#setup)\n\n## Setup\n\nUse `codexspec version`.\n\n"
        "```bash\ncodexspec version\n```\n\n| Option | Default |\n|---|---|\n| `auto_next` | `false` |\n",
        encoding="utf-8",
    )
    return root


def translated() -> str:
    return (
        "# 指南\n\n- [安装](#安装)\n\n## 安装\n\n使用 `codexspec version`。\n\n"
        "```bash\ncodexspec version\n```\n\n| 选项 | 默认值 |\n|---|---|\n| `auto_next` | `false` |\n"
    )


def test_ts005_readme_all_and_alias_mapping(tmp_path: Path) -> None:
    root = seed_readme(tmp_path)
    pairs = doc_translation.inventory(root, readme=True)
    assert len(pairs) == 7
    assert {item["source"] for item in pairs} == {"README.md"}
    assert {item["target"] for item in pairs} == {
        "README.zh-CN.md",
        "README.ja.md",
        "README.ko.md",
        "README.es.md",
        "README.fr.md",
        "README.de.md",
        "README.pt-BR.md",
    }
    aliases = doc_translation.inventory(root, readme=True, languages="zh-CN,pt")
    assert [item["target"] for item in aliases] == ["README.zh-CN.md", "README.pt-BR.md"]
    assert doc_translation.inventory(root, source="README.md") == pairs
    assert all(len(item["source_sha256"]) == 64 for item in pairs)


def test_ts006_site_relative_mapping_and_incremental(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    source = root / "docs/en/user-guide/setup.md"
    source.parent.mkdir(parents=True)
    source.write_text("# Setup\n")
    pairs = doc_translation.inventory(root, source="user-guide/setup.md", languages="zh-CN,pt")
    assert [pair["target"] for pair in pairs] == [
        "docs/zh/user-guide/setup.md",
        "docs/pt-BR/user-guide/setup.md",
    ]
    target = root / pairs[0]["target"]
    target.parent.mkdir(parents=True)
    target.write_text("# 安装\n", encoding="utf-8")
    os.utime(source, (100, 100))
    os.utime(target, (200, 200))
    assert doc_translation.inventory(root, languages="zh", incremental=True) == []
    os.utime(source, (300, 300))
    assert len(doc_translation.inventory(root, languages="zh", incremental=True)) == 1
    assert len(doc_translation.inventory(root, languages="ja", incremental=True)) == 1
    assert (
        doc_translation.inventory(root, source="docs/en/user-guide", languages="zh")[0]["target"] == pairs[0]["target"]
    )


@pytest.mark.parametrize("languages", ["xx", "ru", "zh,zh-CN", "pt,pt-BR", ""])
def test_ts007_invalid_and_duplicate_languages_are_read_only(tmp_path: Path, languages: str) -> None:
    root = seed_readme(tmp_path)
    before = files(root)
    with pytest.raises(doc_translation.TranslationError):
        doc_translation.inventory(root, readme=True, languages=languages)
    assert files(root) == before


@pytest.mark.parametrize("defect", ["missing", "source_symlink", "target_symlink", "escape"])
def test_ts008_invalid_selected_paths_preserve_bytes(tmp_path: Path, defect: str) -> None:
    root = seed_readme(tmp_path / "repo")
    outside = tmp_path / "outside.md"
    outside.write_text("# Outside\n")
    source = None
    if defect == "missing":
        (root / "README.md").unlink()
    elif defect == "source_symlink":
        (root / "README.md").unlink()
        (root / "README.md").symlink_to(outside)
    elif defect == "target_symlink":
        (root / "README.zh-CN.md").symlink_to(outside)
    else:
        source = "../outside.md"
    before = files(root)
    with pytest.raises(doc_translation.TranslationError):
        doc_translation.inventory(root, source=source, readme=True, languages="zh")
    assert files(root) == before and outside.read_text() == "# Outside\n"


def test_ts009_valid_translated_structure_and_tokens(tmp_path: Path) -> None:
    root = seed_readme(tmp_path)
    (root / "README.zh-CN.md").write_text(translated(), encoding="utf-8")
    pairs = doc_translation.inventory(root, readme=True, languages="zh")
    assert doc_translation.verify_pairs(root, pairs) == []


@pytest.mark.parametrize(
    ("defect", "diagnostic"),
    [
        ("code", "fenced"),
        ("inline", "inline"),
        ("heading", "heading"),
        ("table", "table"),
    ],
)
def test_ts010_technical_and_structure_drift_is_detected(tmp_path: Path, defect: str, diagnostic: str) -> None:
    root = seed_readme(tmp_path)
    text = translated()
    if defect == "code":
        text = text.replace("codexspec version\n```", "codexspec --version\n```")
    elif defect == "inline":
        text = text.replace("`false`", "false")
    elif defect == "heading":
        text = text.replace("## 安装\n", "")
    else:
        text = text.replace("| `auto_next` | `false` |", "| `auto_next` | `false` | extra |")
    (root / "README.zh-CN.md").write_text(text, encoding="utf-8")
    errors = doc_translation.verify_pairs(root, doc_translation.inventory(root, readme=True, languages="zh"))
    assert any(diagnostic in error["problem"] for error in errors)


@pytest.mark.parametrize("destination", ["missing.md", "#缺失", "#重复-2"])
def test_ts011_missing_links_and_duplicate_anchors_fail(tmp_path: Path, destination: str) -> None:
    root = seed_readme(tmp_path)
    source = root / "README.md"
    source.write_text(source.read_text() + "\n## Repeat\n\n## Repeat\n")
    text = translated() + f"\n## 重复\n\n## 重复\n\n[链接]({destination})\n"
    (root / "README.zh-CN.md").write_text(text, encoding="utf-8")
    errors = doc_translation.verify_pairs(root, doc_translation.inventory(root, readme=True, languages="zh"))
    assert any("link" in error["problem"] or "anchor" in error["problem"] for error in errors)


def test_ts011_unicode_duplicate_anchor_passes(tmp_path: Path) -> None:
    root = seed_readme(tmp_path)
    source = root / "README.md"
    source.write_text(source.read_text() + "\n## Repeat\n\n## Repeat\n")
    text = translated() + "\n## 重复\n\n## 重复\n\n[链接](#重复-1)\n"
    (root / "README.zh-CN.md").write_text(text, encoding="utf-8")
    assert doc_translation.verify_pairs(root, doc_translation.inventory(root, readme=True, languages="zh")) == []


def test_ts012_cli_inventory_verify_and_dry_run_do_not_write(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = seed_readme(tmp_path)
    (root / "README.zh-CN.md").write_text(translated(), encoding="utf-8")
    before = files(root)
    for operation in ("inventory", "verify"):
        args = [operation, "--root", str(root), "--readme", "--lang", "zh", "--dry-run"]
        assert doc_translation.main(args) == 0
        output = json.loads(capsys.readouterr().out)
        assert output["root"] == str(root) and output["pairs"]
    assert files(root) == before


@pytest.mark.parametrize(
    "defect",
    ["missing_root", "dangling_root", "missing_site", "dangling_site", "dangling_shorthand", "dangling_parent"],
)
def test_ts008_explicit_source_identity_is_checked_before_fallback(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], defect: str
) -> None:
    root = tmp_path.resolve()
    docs = root / "docs/en"
    docs.mkdir(parents=True)
    (docs / "README.md").write_text("# Different site source\n")
    (root / "README.ja.md").write_text("# Existing target\n")
    source = "README.md"
    if defect == "dangling_root":
        (root / source).symlink_to(root / "absent.md")
    elif defect in {"missing_site", "dangling_site"}:
        source = "docs/en/page.md"
        if defect == "dangling_site":
            (root / source).symlink_to(root / "absent.md")
        alternate = docs / source
        alternate.parent.mkdir(parents=True)
        alternate.write_text("# Different nested source\n")
    elif defect in {"dangling_shorthand", "dangling_parent"}:
        source = "guide/page.md"
        (docs / "guide").mkdir()
        (docs / source).write_text("# Different shorthand source\n")
        if defect == "dangling_parent":
            (root / "guide").symlink_to(root / "absent", target_is_directory=True)
        else:
            (root / "guide").mkdir()
            (root / source).symlink_to(root / "absent.md")
    before = files(root)
    with pytest.raises(doc_translation.TranslationError):
        doc_translation.inventory(root, source=source, languages="ja")
    assert doc_translation.main(["inventory", "--root", str(root), "--source", source, "--lang", "ja"]) == 2
    assert json.loads(capsys.readouterr().err)["error"]
    assert files(root) == before


@pytest.mark.parametrize("selection", ["flag", "relative", "absolute"])
def test_ts008_readme_directory_is_never_a_readme_source(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], selection: str
) -> None:
    root = tmp_path.resolve()
    (root / "README.md").mkdir()
    (root / "README.md/one.md").write_text("# One\n")
    (root / "README.md/two.md").write_text("# Two\n")
    (root / "README.ja.md").write_text("# Existing translation\n")
    source = None if selection == "flag" else ("README.md" if selection == "relative" else root / "README.md")
    before = files(root)
    with pytest.raises(doc_translation.TranslationError, match="regular file"):
        doc_translation.inventory(root, source=source, readme=selection == "flag", languages="ja")
    args = ["inventory", "--root", str(root), "--lang", "ja"]
    args += ["--readme"] if source is None else ["--source", str(source)]
    assert doc_translation.main(args) == 2
    assert "regular file" in json.loads(capsys.readouterr().err)["error"]
    assert files(root) == before


@pytest.mark.parametrize("selection", ["file", "directory", "cross_pair", "case_alias"])
def test_ts008_targets_cannot_overlap_any_selected_source(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], selection: str
) -> None:
    root = tmp_path.resolve()
    page = root / "docs/ja/page.md"
    page.parent.mkdir(parents=True)
    page.write_text("# English baseline\n")
    source = "docs/ja/page.md"
    if selection == "directory":
        source = "docs/ja"
    elif selection == "cross_pair":
        source = "docs"
        (root / "docs/en").mkdir()
        (root / "docs/en/page.md").write_text("# Other English source\n")
    elif selection == "case_alias":
        source = "docs/JA/page.md"
        if not (root / source).exists():
            pytest.skip("Filesystem has case-sensitive directory names")
        assert (root / source).samefile(page)
    before = files(root)
    for incremental in (False, True):
        with pytest.raises(doc_translation.TranslationError, match="source"):
            doc_translation.inventory(root, source=source, languages="ja", incremental=incremental)
    assert doc_translation.main(["inventory", "--root", str(root), "--source", source, "--lang", "ja"]) == 2
    assert "source" in json.loads(capsys.readouterr().err)["error"]
    assert files(root) == before


def test_ts006_custom_directory_cannot_map_multiple_sources_to_one_target(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    (root / "docs/en").mkdir(parents=True)
    (root / "docs/en/page.md").write_text("# English one\n")
    (root / "docs/page.md").write_text("# English two\n")
    before = files(root)
    with pytest.raises(doc_translation.TranslationError, match="multiple sources"):
        doc_translation.inventory(root, source="docs", languages="ja")
    assert files(root) == before


def test_ts006_disjoint_custom_source_remains_supported(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    page = root / "docs/ja/page.md"
    page.parent.mkdir(parents=True)
    page.write_text("# Custom English input\n")
    before = files(root)
    pairs = doc_translation.inventory(root, source="docs/ja/page.md", languages="zh")
    assert len(pairs) == 1
    assert pairs[0]["source"] == "docs/ja/page.md"
    assert pairs[0]["target"] == "docs/zh/page.md"
    assert files(root) == before


def test_ts006_inventory_paths_are_portable_across_path_representations(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from pathlib import PureWindowsPath

    root = tmp_path.resolve()
    source = root / "docs/en/guide/page.md"
    source.parent.mkdir(parents=True)
    source.write_text("# English\n")
    original = Path.relative_to

    # Model Windows' relative-path representation while retaining real local I/O.
    def windows_relative(path: Path, *other: Path) -> PureWindowsPath:
        return PureWindowsPath(*original(path, *other).parts)

    monkeypatch.setattr(Path, "relative_to", windows_relative)
    pairs = doc_translation.inventory(root, languages="ja")
    assert pairs[0]["source"] == "docs/en/guide/page.md"
    assert pairs[0]["target"] == "docs/ja/guide/page.md"


@pytest.mark.parametrize("selection", ["readme.md", "ReadMe.md", "README.MD", "absolute"])
def test_ts005_filesystem_equivalent_readme_sources_keep_root_mapping(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], selection: str
) -> None:
    root = seed_readme(tmp_path)
    source = root / "readme.md" if selection == "absolute" else selection
    alias = root / source
    if not alias.exists() or not alias.samefile(root / "README.md"):
        pytest.skip("Filesystem has case-sensitive source names")
    before = files(root)
    expected = doc_translation.inventory(root, readme=True, languages="ja")
    assert doc_translation.inventory(root, source=source, languages="ja") == expected
    args = ["inventory", "--root", str(root), "--source", str(source), "--lang", "ja"]
    assert doc_translation.main(args) == 0
    assert json.loads(capsys.readouterr().out)["pairs"] == expected
    assert files(root) == before


@pytest.mark.parametrize(
    "selection",
    ["DOCS/EN/guide/page.md", "docs/EN/GUIDE/PAGE.MD", "absolute", "DOCS/EN", "DOCS/EN/GUIDE"],
)
def test_ts006_filesystem_equivalent_english_sources_keep_relative_hierarchy(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], selection: str
) -> None:
    root = tmp_path.resolve()
    page = root / "docs/en/guide/page.md"
    page.parent.mkdir(parents=True)
    page.write_text("# English guide\n")
    source = root / "DOCS/EN/guide/page.md" if selection == "absolute" else selection
    alias = root / source
    canonical = page if alias.suffix else (page.parent if str(source).endswith("GUIDE") else page.parent.parent)
    if not alias.exists() or not alias.samefile(canonical):
        pytest.skip("Filesystem has case-sensitive source names")
    before = files(root)
    expected = doc_translation.inventory(root, source=page, languages="ja")
    assert expected[0]["target"] == "docs/ja/guide/page.md"
    assert doc_translation.inventory(root, source=source, languages="ja") == expected
    assert doc_translation.main(["inventory", "--root", str(root), "--source", str(source), "--lang", "ja"]) == 0
    assert json.loads(capsys.readouterr().out)["pairs"] == expected
    assert files(root) == before


@pytest.mark.parametrize("source", ["readme.md", "README.MD", "DOCS/en/page.md", "DOCS/EN/page.md", "docs/EN/page.md"])
def test_ts008_missing_reserved_source_spellings_never_select_alternate_inputs(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], source: str
) -> None:
    root = tmp_path.resolve()
    alternate = root / "docs/en" / source
    alternate.parent.mkdir(parents=True)
    alternate.write_text("# Alternate English input\n")
    if Path(source).parts[0] != "docs" and not doc_translation.namespace_folds_case(root):
        pytest.skip("These unavailable spellings are site shorthand on a case-sensitive namespace")
    before = files(root)
    with pytest.raises(doc_translation.TranslationError):
        doc_translation.inventory(root, source=source, languages="ja")
    assert doc_translation.main(["inventory", "--root", str(root), "--source", source, "--lang", "ja"]) == 2
    assert json.loads(capsys.readouterr().err)["error"]
    assert files(root) == before


@pytest.mark.parametrize("absolute", [False, True])
def test_ts008_filesystem_equivalent_readme_directory_is_rejected(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], absolute: bool
) -> None:
    root = tmp_path.resolve()
    directory = root / "README.md"
    directory.mkdir()
    (directory / "page.md").write_text("# Nested English input\n")
    source = root / "readme.md" if absolute else "readme.md"
    alias = root / source
    if not alias.exists() or not alias.samefile(directory):
        pytest.skip("Filesystem has case-sensitive source names")
    before = files(root)
    with pytest.raises(doc_translation.TranslationError, match="regular file"):
        doc_translation.inventory(root, source=source, languages="ja")
    assert doc_translation.main(["inventory", "--root", str(root), "--source", str(source), "--lang", "ja"]) == 2
    assert "regular file" in json.loads(capsys.readouterr().err)["error"]
    assert files(root) == before


def test_ts006_case_sensitive_distinct_readme_file_keeps_custom_mapping(tmp_path: Path) -> None:
    root = seed_readme(tmp_path)
    distinct = root / "readme.md"
    if distinct.exists() and distinct.samefile(root / "README.md"):
        pytest.skip("Filesystem folds the two README spellings")
    distinct.write_text("# Distinct custom input\n")
    before = files(root)
    pairs = doc_translation.inventory(root, source=distinct, languages="ja")
    assert pairs[0]["surface"] == "docs"
    assert pairs[0]["source"] == "readme.md" and pairs[0]["target"] == "docs/ja/readme.md"
    assert pairs[0]["source_sha256"] != doc_translation.inventory(root, readme=True, languages="ja")[0]["source_sha256"]
    assert files(root) == before
    distinct.unlink()
    page = root / "docs/en/readme.md"
    page.parent.mkdir(parents=True)
    page.write_text("# Shorthand English input\n")
    before = files(root)
    assert doc_translation.inventory(root, source="readme.md", languages="ja") == doc_translation.inventory(
        root, source=page, languages="ja"
    )
    assert files(root) == before


def test_ts006_case_sensitive_distinct_english_directory_keeps_custom_mapping(tmp_path: Path) -> None:
    root = tmp_path.resolve()
    english = root / "docs/en/guide/page.md"
    english.parent.mkdir(parents=True)
    english.write_text("# Standard English input\n")
    distinct_dir = root / "docs/EN"
    if distinct_dir.exists() and distinct_dir.samefile(english.parent.parent):
        pytest.skip("Filesystem folds the two English directory spellings")
    distinct = distinct_dir / "guide/page.md"
    distinct.parent.mkdir(parents=True)
    distinct.write_text("# Distinct custom input\n")
    before = files(root)
    pairs = doc_translation.inventory(root, source=distinct, languages="ja")
    assert pairs[0]["source"] == "docs/EN/guide/page.md" and pairs[0]["target"] == "docs/ja/page.md"
    original_pair = doc_translation.inventory(root, source=english, languages="ja")[0]
    assert pairs[0]["source_sha256"] != original_pair["source_sha256"]
    assert files(root) == before
    page = root / "docs/en/DOCS/en/page.md"
    page.parent.mkdir(parents=True)
    page.write_text("# Shorthand English input\n")
    before = files(root)
    assert doc_translation.inventory(root, source="DOCS/en/page.md", languages="ja") == doc_translation.inventory(
        root, source=page, languages="ja"
    )
    assert files(root) == before


@pytest.mark.parametrize("directory", ["DOCS/en", "docs/EN", "DOCS/EN"])
def test_ts006_english_directory_entry_case_retains_identity_mapping(tmp_path: Path, directory: str) -> None:
    root = tmp_path.resolve()
    page = root / directory / "guide/page.md"
    page.parent.mkdir(parents=True)
    page.write_text("# English guide\n")
    namespace = root / "docs/en"
    if not namespace.exists() or not namespace.samefile(page.parent.parent):
        pytest.skip("Filesystem has case-sensitive English directory names")
    before = files(root)
    for source in (page, "docs/en/guide/page.md", directory):
        pairs = doc_translation.inventory(root, source=source, languages="ja")
        assert pairs[0]["surface"] == "docs" and pairs[0]["target"] == "docs/ja/guide/page.md"
        assert (root / pairs[0]["source"]).samefile(page)
    assert files(root) == before


@pytest.mark.parametrize("source", ["readme.md", "DOCS/en/page.md"])
def test_ts006_case_sensitive_namespace_preserves_english_page_shorthand(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, source: str
) -> None:
    root = tmp_path.resolve()
    page = root / "docs/en" / source
    page.parent.mkdir(parents=True)
    page.write_text("# Intended English page\n")
    before = files(root)
    # Model case-sensitive namespace policy; all source/target file I/O stays real.
    monkeypatch.setattr(doc_translation, "namespace_folds_case", lambda _: False, raising=False)
    expected = doc_translation.inventory(root, source=page, languages="ja")
    assert doc_translation.inventory(root, source=source, languages="ja") == expected
    assert expected[0]["source"] == f"docs/en/{source}"
    assert expected[0]["target"] == f"docs/ja/{source}"
    assert files(root) == before


@pytest.mark.parametrize("prefix", ["checkout", "parent"])
@pytest.mark.parametrize("selection", ["readme", "site_file", "site_directory"])
def test_ts008_physical_checkout_prefix_alias_keeps_selected_source(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], prefix: str, selection: str
) -> None:
    root = seed_readme(tmp_path / "repo")
    page = root / "docs/en/guide/page.md"
    page.parent.mkdir(parents=True)
    page.write_text("# English guide\n")
    alias = (
        root.with_name("REPO") if prefix == "checkout" else root.parent.with_name(root.parent.name.swapcase()) / "repo"
    )
    if not alias.exists() or not alias.samefile(root):
        pytest.skip("Filesystem has case-sensitive checkout-prefix names")
    relative = "README.md" if selection == "readme" else "docs/en/guide/page.md"
    if selection == "site_directory":
        relative = "docs/en/guide"
    source, canonical = alias / relative, root / relative
    assert source.samefile(canonical) and not any(p.is_symlink() for p in (source, *source.parents))
    before = files(root)
    expected = doc_translation.inventory(root, source=canonical, languages="ja")
    assert doc_translation.inventory(root, source=source, languages="ja") == expected
    assert doc_translation.main(["inventory", "--root", str(root), "--source", str(source), "--lang", "ja"]) == 0
    assert json.loads(capsys.readouterr().out)["pairs"] == expected
    assert files(root) == before


@pytest.mark.parametrize("selection", ["redirected_prefix", "distinct_checkout"])
def test_ts008_prefix_identity_never_launders_redirects_or_other_checkouts(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], selection: str
) -> None:
    root = seed_readme(tmp_path / "repo")
    if selection == "redirected_prefix":
        redirect = tmp_path / "redirect"
        redirect.symlink_to(root.parent, target_is_directory=True)
        source = redirect / root.name / "README.md"
        assert source.samefile(root / "README.md") and redirect.is_symlink()
    else:
        outside = tmp_path / "other-checkout"
        outside.mkdir()
        source = outside / "README.md"
        source.write_bytes((root / "README.md").read_bytes())
        assert not outside.samefile(root) and not source.samefile(root / "README.md")
    before, outside_bytes = files(root), source.read_bytes()
    with pytest.raises(doc_translation.TranslationError):
        doc_translation.inventory(root, source=source, languages="ja")
    assert doc_translation.main(["inventory", "--root", str(root), "--source", str(source), "--lang", "ja"]) == 2
    assert json.loads(capsys.readouterr().err)["error"]
    assert files(root) == before and source.read_bytes() == outside_bytes


def prospective_destination_fixture(tmp_path: Path, variant: str) -> tuple[Path, list[str]]:
    root = (tmp_path / "repo").resolve()
    names = {
        "leaf": ("Page.md", "page.md"),
        "parent": ("GUIDE/page.md", "guide/page.md"),
        "empty_parent": ("GUIDE/page.md", "guide/page.md"),
        "unicode": ("café.md", "cafe\u0301.md"),
        "casefold_expansion": ("Straße.md", "STRASSE.md"),
    }
    first, second = names[variant]
    for relative, text in [
        (f"docs/{first}", "# First English input\n"),
        (f"docs/en/{second}", "# Second English input\n"),
    ]:
        page = root / relative
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(text, encoding="utf-8")
    if variant == "empty_parent":
        (root / "docs/JA/GUIDE").mkdir(parents=True)
    return root, [f"docs/ja/{first}", f"docs/ja/{second}"]


@pytest.mark.parametrize("variant", ["leaf", "parent", "empty_parent", "unicode", "casefold_expansion"])
@pytest.mark.parametrize("incremental", [False, True])
def test_ts006_prospective_destination_aliases_are_rejected_before_any_write(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], variant: str, incremental: bool
) -> None:
    root, targets = prospective_destination_fixture(tmp_path, variant)
    # Prove the real namespace premise outside the selected checkout.
    witness = tmp_path.resolve() / "namespace-witness"
    first, second = [witness / target for target in targets]
    first.parent.mkdir(parents=True)
    first.write_text("# Namespace witness\n")
    if not second.exists() or not first.samefile(second):
        pytest.skip("Filesystem preserves these destination spellings as distinct names")
    before = files(root)
    assert all(not (root / target).exists() for target in targets)
    with pytest.raises(doc_translation.TranslationError, match="multiple sources"):
        doc_translation.inventory(root, source="docs", languages="ja", incremental=incremental)
    args = ["inventory", "--root", str(root), "--source", "docs", "--lang", "ja"]
    if incremental:
        args.append("--incremental")
    assert doc_translation.main(args) == 2
    assert "multiple sources" in json.loads(capsys.readouterr().err)["error"]
    assert files(root) == before
    assert all(not (root / target).exists() for target in targets)


@pytest.mark.parametrize("variant", ["leaf", "unicode", "casefold_expansion"])
def test_ts006_case_sensitive_prospective_destinations_remain_distinct(tmp_path: Path, variant: str) -> None:
    root, targets = prospective_destination_fixture(tmp_path, variant)
    witness = tmp_path.resolve() / "namespace-witness"
    first, second = [witness / target for target in targets]
    first.parent.mkdir(parents=True)
    first.write_text("# Namespace witness\n")
    if second.exists() and first.samefile(second):
        pytest.skip("Filesystem aliases these two prospective destination spellings")
    before = files(root)
    pairs = doc_translation.inventory(root, source="docs", languages="ja")
    assert len(pairs) == 2 and {pair["target"] for pair in pairs} == set(targets)
    assert files(root) == before
    for index, pair in enumerate(pairs):
        target = root / pair["target"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"# Separate translation {index}\n")
    assert not (root / pairs[0]["target"]).samefile(root / pairs[1]["target"])


@pytest.mark.parametrize("variant", ["leaf", "unicode", "casefold_expansion"])
def test_ts006_case_sensitive_destination_namespace_policy_preserves_spelling(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, variant: str
) -> None:
    root, targets = prospective_destination_fixture(tmp_path, variant)
    # Model namespace policy only; real source I/O does not claim a native case-sensitive run.
    monkeypatch.setattr(doc_translation, "namespace_folds_case", lambda _: False)
    monkeypatch.setattr(doc_translation, "source_name_alias", lambda path, name: path.name == name, raising=False)
    before = files(root)
    pairs = doc_translation.inventory(root, source="docs", languages="ja")
    assert len(pairs) == 2 and {pair["target"] for pair in pairs} == set(targets)
    assert files(root) == before


@pytest.mark.parametrize("incremental", [False, True])
def test_ts006_disjoint_prospective_destinations_remain_supported(tmp_path: Path, incremental: bool) -> None:
    root, _ = prospective_destination_fixture(tmp_path, "leaf")
    original = root / "docs/Page.md"
    original.rename(root / "docs/Other.md")
    before = files(root)
    pairs = doc_translation.inventory(root, source="docs", languages="ja", incremental=incremental)
    assert len(pairs) == 2
    assert {pair["target"] for pair in pairs} == {"docs/ja/Other.md", "docs/ja/page.md"}
    assert files(root) == before


@pytest.mark.parametrize("variant", ["unicode", "casefold_expansion"])
@pytest.mark.parametrize("incremental", [False, True])
def test_ts006_case_folding_does_not_imply_other_name_equivalence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, variant: str, incremental: bool
) -> None:
    root, targets = prospective_destination_fixture(tmp_path, variant)
    # Model Windows-like case folding without canonical normalization or full Unicode folding.
    monkeypatch.setattr(doc_translation, "namespace_folds_case", lambda _: True)
    monkeypatch.setattr(
        doc_translation, "source_name_alias", lambda path, name: path.name.lower() == name.lower(), raising=False
    )
    before = files(root)
    pairs = doc_translation.inventory(root, source="docs", languages="ja", incremental=incremental)
    assert len(pairs) == 2 and {pair["target"] for pair in pairs} == set(targets)
    assert files(root) == before


@pytest.mark.parametrize("incremental", [False, True])
def test_ts006_canonical_aliases_are_rejected_independently_of_case_folding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, incremental: bool
) -> None:
    from unicodedata import normalize

    root, targets = prospective_destination_fixture(tmp_path, "unicode")
    # Model a case-sensitive volume that aliases canonical Unicode spellings.
    monkeypatch.setattr(doc_translation, "namespace_folds_case", lambda _: False)
    monkeypatch.setattr(
        doc_translation,
        "source_name_alias",
        lambda path, name: normalize("NFC", path.name) == normalize("NFC", name),
        raising=False,
    )
    before = files(root)
    with pytest.raises(doc_translation.TranslationError, match="multiple sources"):
        doc_translation.inventory(root, source="docs", languages="ja", incremental=incremental)
    assert files(root) == before and all(not (root / target).exists() for target in targets)
