"""The site must publish the same workflow images as the repository READMEs."""

from pathlib import Path
from types import SimpleNamespace

import pytest

pytest.importorskip("mkdocs")
from mkdocs.exceptions import PluginError
from mkdocs.structure.files import Files

from hooks.workflow_assets import on_files

ROOT = Path(__file__).resolve().parents[1]


def test_workflow_assets_keep_source_bytes_and_publish_under_assets(tmp_path):
    config = SimpleNamespace(docs_dir=str(ROOT / "docs"), site_dir=str(tmp_path), use_directory_urls=True)
    files = on_files(Files([]), config)
    assert len(files) == 16
    for file in files:
        assert Path(file.abs_src_path).is_relative_to(ROOT / "assets" / "workflow")
        assert file.dest_uri.startswith("assets/workflow/")
        file.copy_file()
        assert Path(file.abs_dest_path).read_bytes() == Path(file.abs_src_path).read_bytes()
    assert len(on_files(files, config)) == 16


def test_missing_theme_asset_stops_build(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()
    config = SimpleNamespace(docs_dir=str(docs), site_dir=str(tmp_path / "site"), use_directory_urls=True)
    with pytest.raises(PluginError, match="workflow-en-light.png"):
        on_files(Files([]), config)
