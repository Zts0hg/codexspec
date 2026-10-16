"""Behavioral checks for repository-only multilingual workflow assets."""

import copy
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath, PureWindowsPath

import pytest

from internal import workflow_diagrams as wd


@pytest.fixture(autouse=True)
def non_utf8_default_text_codec(monkeypatch):
    """Exercise every file boundary with Windows-style implicit text encoding."""
    read_text, write_text = Path.read_text, Path.write_text

    def read(path, encoding=None, errors=None, **kwargs):
        return read_text(path, encoding=encoding or "cp1252", errors=errors, **kwargs)

    def write(path, data, encoding=None, errors=None, **kwargs):
        return write_text(path, data, encoding=encoding or "cp1252", errors=errors, **kwargs)

    monkeypatch.setattr(Path, "read_text", read)
    monkeypatch.setattr(Path, "write_text", write)


@pytest.fixture
def inputs():
    return wd.load(Path(__file__).resolve().parents[1])


def test_ts01_generate_all_native_graphs_and_theme_parity(inputs):
    template, catalog, layout = inputs
    outputs = wd.generate(template, catalog, layout)
    assert set(outputs) == set(wd.LOCALES)
    for data in outputs.values():
        pages = list(ET.fromstring(data))
        assert len(pages) == 2
        shapes = [
            {
                c.get("id"): ET.tostring(c.find("mxGeometry"))
                for c in p.iter("mxCell")
                if c.find("mxGeometry") is not None
            }
            for p in pages
        ]
        assert shapes[0] == shapes[1]
        assert len(shapes[0]) == 114
        assert len([c for c in pages[0].iter("mxCell") if c.get("edge") == "1"]) == 35


@pytest.mark.parametrize("kind", ["missing", "unknown"])
def test_ts02_catalog_keys_are_exact(inputs, kind):
    template, catalog, layout = copy.deepcopy(inputs)
    if kind == "missing":
        del catalog["wf-title"]["translations"]["de"]
    else:
        catalog["unknown-cell"] = copy.deepcopy(catalog["wf-title"])
    with pytest.raises(wd.DiagramError, match="wf-title|unknown-cell"):
        wd.generate(template, catalog, layout)


def test_ts03_stale_translation(inputs):
    template, catalog, layout = copy.deepcopy(inputs)
    catalog["wf-title"]["en"] += " changed"
    with pytest.raises(wd.DiagramError, match="stale.*wf-title"):
        wd.generate(template, catalog, layout)


def test_ts04_protected_tokens(inputs):
    template, catalog, layout = copy.deepcopy(inputs)
    catalog["wf-profile"]["translations"]["fr"]["text"] = "Texte incomplet"
    with pytest.raises(wd.DiagramError, match="protected.*wf-profile"):
        wd.generate(template, catalog, layout)


def test_ts05_stale_generated_file(tmp_path, inputs):
    output = wd.generate(*inputs)
    wd.write_generated(tmp_path, output)
    wd.check_generated(tmp_path, output)
    (tmp_path / "internal/workflow_diagrams/generated/en.drawio").write_text("changed", encoding="utf-8")
    with pytest.raises(wd.DiagramError, match="en.drawio"):
        wd.check_generated(tmp_path, output)


def test_ts05_asset_hash_and_source_drift(tmp_path):
    image = tmp_path / "a.png"
    image.write_bytes(b"image")
    manifest = {"source": "original", "assets": {"a.png": wd.digest(image.read_bytes())}}
    wd.check_manifest(tmp_path, manifest, "original", expected={"a.png"})
    for source in ["changed", "original"]:
        if source == "original":
            image.write_bytes(b"changed")
        with pytest.raises(wd.DiagramError, match="stale"):
            wd.check_manifest(tmp_path, manifest, source, expected={"a.png"})


def test_ts06_bad_layout_target(inputs):
    template, catalog, layout = copy.deepcopy(inputs)
    layout["en"]["cells"] = {"unknown-cell": {"width": 99}}
    with pytest.raises(wd.DiagramError, match="unknown-cell"):
        wd.generate(template, catalog, layout)


def test_ts06_overlap_not_intentional_containment():
    assert not wd.overlap((0, 0, 100, 100), (10, 10, 20, 20))
    assert wd.overlap((0, 0, 100, 100), (90, 10, 20, 20))
    assert not wd.overlap((0, 0, 100, 100), (100, 0, 20, 20))


@pytest.mark.parametrize("timeout", [False, True])
def test_ts07_renderer_failure_preserves_manifest(tmp_path, monkeypatch, timeout):
    monkeypatch.setattr(wd, "source_digest", lambda root: "source")

    def fail(*args, **kwargs):
        if timeout:
            raise subprocess.TimeoutExpired(args[0], 120)
        raise subprocess.CalledProcessError(1, args[0], stderr="renderer failed")

    monkeypatch.setattr(subprocess, "run", fail)
    with pytest.raises(wd.DiagramError, match="render"):
        wd.render(tmp_path, "/unused/drawio")
    assert not (tmp_path / "assets/workflow/manifest.json").exists()


def test_ts08_wrong_readme_locale(tmp_path):
    for lang in wd.LOCALES:
        name = "README.md" if lang == "en" else f"README.{lang}.md"
        (tmp_path / name).write_text(wd.picture(lang, "Workflow", "Full size"), encoding="utf-8")
    wd.check_readmes(tmp_path)
    p = tmp_path / "README.de.md"
    p.write_text(p.read_text(encoding="utf-8").replace("workflow-de-", "workflow-en-"), encoding="utf-8")
    with pytest.raises(wd.DiagramError, match="README.de.md"):
        wd.check_readmes(tmp_path)


def test_output_symlink_is_rejected(tmp_path, inputs):
    destination = tmp_path / "internal"
    outside = tmp_path / "outside"
    outside.mkdir()
    destination.symlink_to(outside, target_is_directory=True)
    with pytest.raises(wd.DiagramError, match="symlink"):
        wd.write_generated(tmp_path, wd.generate(*inputs))


def test_ts06_theme_graph_mismatch(inputs):
    template, catalog, layout = copy.deepcopy(inputs)
    node = next(c for c in template[1].iter("mxCell") if c.get("id") == "wf-spec")
    node.find("mxGeometry").set("width", "999")
    with pytest.raises(wd.DiagramError, match="theme.*wf-spec"):
        wd.generate(template, catalog, layout)


def test_ts06_negative_width(inputs):
    template, catalog, layout = copy.deepcopy(inputs)
    layout["en"].setdefault("cells", {})["wf-spec"] = {"width": -1}
    with pytest.raises(wd.DiagramError, match="geometry.*wf-spec"):
        wd.generate(template, catalog, layout)


def test_ts08_theme_source_must_be_in_workflow_block(tmp_path):
    for lang in wd.LOCALES:
        name = "README.md" if lang == "en" else f"README.{lang}.md"
        (tmp_path / name).write_text(wd.picture(lang, "Workflow", "Full size"), encoding="utf-8")
    path = tmp_path / "README.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            'srcset="assets/workflow/workflow-en-dark.png"', 'srcset="assets/workflow/workflow-en-light.png"'
        ),
        encoding="utf-8",
    )
    with pytest.raises(wd.DiagramError, match="README.md"):
        wd.check_readmes(tmp_path)


def test_shared_layout_overrides_stay_local():
    data = {
        "profiles": {"shared": {"scale": [1, 1], "cells": {"box": {"x": 1, "width": 20}}}},
        "locales": {lang: {"profile": "shared"} for lang in wd.LOCALES},
    }
    data["locales"]["de"].update({"cells": {"box": {"width": 30}}, "points": {"edge": [[1, 2]]}})
    before = copy.deepcopy(data)
    result = wd.resolve_layout(data)
    assert result["de"]["cells"]["box"] == {"x": 1, "width": 30}
    assert result["en"]["cells"]["box"]["width"] == 20
    result["de"]["points"]["edge"][0][0] = 99
    assert data == before
    assert result["en"]["points"] == {}


def test_unknown_layout_profile_is_reported():
    data = {"profiles": {}, "locales": {lang: {"profile": "missing"} for lang in wd.LOCALES}}
    with pytest.raises(wd.DiagramError, match="unknown layout profile en: missing"):
        wd.resolve_layout(data)


def test_source_fingerprint_uses_portable_path_identity(monkeypatch):
    root = Path(__file__).resolve().parents[1]
    fingerprints = []
    for path_type in (PurePosixPath, PureWindowsPath):
        monkeypatch.setattr(wd, "SOURCE", path_type("internal/workflow_diagrams"))
        fingerprints.append(wd.source_digest(root))
    assert fingerprints[0] == fingerprints[1]


@pytest.mark.parametrize("attribute", ["source", "target", "parent"])
def test_unresolved_graph_references_are_rejected(inputs, attribute):
    template, catalog, layout = copy.deepcopy(inputs)
    edge_id = next(c.get("id") for c in template[0].iter("mxCell") if c.get("edge") == "1")
    for page in template:
        edge = next(c for c in page.iter("mxCell") if c.get("id") == edge_id)
        edge.set(attribute, "missing-cell")
    with pytest.raises(wd.DiagramError, match=f"{edge_id}.*{attribute}.*missing-cell"):
        wd.generate(template, catalog, layout)
