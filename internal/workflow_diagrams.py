"""Generate repository README workflow diagrams; never installed by codexspec init."""

import argparse
import copy
import hashlib
import html
import json
import math
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

LOCALES = ("en", "zh-CN", "ja", "ko", "de", "fr", "es", "pt-BR")
SOURCE = Path("internal/workflow_diagrams")
ASSETS = Path("assets/workflow")
FONTS = {"zh-CN": "PingFang SC", "ja": "Hiragino Sans", "ko": "Apple SD Gothic Neo"}


class DiagramError(ValueError):
    """An actionable generation/validation failure."""


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(root, relative):
    root = Path(root).absolute()
    path = root / relative
    if not path.is_relative_to(root) or ".." in Path(relative).parts:
        raise DiagramError(f"outside output root: {path}")
    for part in [path, *path.parents]:
        if part.is_symlink():
            raise DiagramError(f"symlink path: {part}")
        if part == root:
            break
    if path.is_file() and path.stat().st_nlink != 1:
        raise DiagramError(f"hard-linked output: {path}")
    return path


def write(root, relative, data):
    path = safe_path(root, relative)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def resolve_layout(data):
    """Copy a shared profile, then apply only the selected locale's overrides."""
    if set(data["locales"]) != set(LOCALES):
        raise DiagramError("layout locale inventory differs")
    result = {}
    for locale, overrides in data["locales"].items():
        profile = overrides.get("profile")
        if profile not in data["profiles"]:
            raise DiagramError(f"unknown layout profile {locale}: {profile}")
        if set(overrides) - {"profile", "scale", "cells", "points"}:
            raise DiagramError(f"unknown layout override: {locale}")
        config = copy.deepcopy(data["profiles"][profile])
        if "scale" in overrides:
            config["scale"] = copy.deepcopy(overrides["scale"])
        for cell_id, geometry in overrides.get("cells", {}).items():
            config.setdefault("cells", {}).setdefault(cell_id, {}).update(geometry)
        config.setdefault("points", {}).update(copy.deepcopy(overrides.get("points", {})))
        result[locale] = config
    return result


def load(root):
    return (
        ET.parse(safe_path(root, SOURCE / "template.drawio")).getroot(),
        json.loads(safe_path(root, SOURCE / "catalog.json").read_text(encoding="utf-8")),
        resolve_layout(json.loads(safe_path(root, SOURCE / "layout.json").read_text(encoding="utf-8"))),
    )


def style(cell):
    return dict(pair.split("=", 1) for pair in cell.get("style", "").split(";") if "=" in pair)


def set_style(cell, **changes):
    existing = style(cell)
    existing.update({k: str(v) for k, v in changes.items()})
    # Preserve bare mxGraph style names (for example text).
    names = [p for p in cell.get("style", "").split(";") if p and "=" not in p]
    cell.set("style", ";".join(names + [f"{k}={v}" for k, v in existing.items()]) + ";")


def translated(entry, locale, cell_id):
    if locale == "en" or entry.get("literal"):
        return entry["en"]
    item = entry["translations"].get(locale)
    if not item or not isinstance(item.get("text"), str) or not item["text"].strip():
        raise DiagramError(f"missing translation {locale}: {cell_id}")
    if item.get("source") != entry["en"]:
        raise DiagramError(f"stale translation {locale}: {cell_id}; review against current English")
    for token in entry["protected"]:
        if token not in item["text"]:
            raise DiagramError(f"protected token {token!r} missing in {locale}: {cell_id}")
    return item["text"]


def label(text, locale, cell_id, original=""):
    if locale == "zh-CN":
        original = original.replace(" · 原始手写图见参考页", "")
        plain = html.unescape(re.sub("<[^>]+>", "", re.sub(r"<br\s*/?>|</div>", "\n", original))).strip()
        plain = re.sub(r"\n{3,}", "\n\n", plain)
        if plain == text:
            return f'<div lang="zh-CN">{original}</div>'
    lines = text.split("\n")
    # Chinese keeps its approved character-stacked review labels.
    escaped = "<br>".join(html.escape(line) for line in lines)
    wrapping = ";word-break:keep-all" if locale == "ko" else ""
    return f'<div lang="{locale}" style="line-height:1.25{wrapping}">{escaped}</div>'


def apply_layout(page, config, locale):
    cells = {c.get("id"): c for c in page.iter("mxCell")}
    for cell_id in config.get("cells", {}):
        if cell_id not in cells:
            raise DiagramError(f"unknown layout cell {locale}: {cell_id}")
    sx, sy = config.get("scale", [1, 1])
    if not all(isinstance(n, (int, float)) and math.isfinite(n) and n > 0 for n in (sx, sy)):
        raise DiagramError(f"invalid layout scale: {locale}")
    for c in cells.values():
        g = c.find("mxGeometry")
        if g is None:
            continue
        if c.get("vertex") == "1":
            for k, scale in [("x", sx), ("y", sy), ("width", sx), ("height", sy)]:
                g.set(k, f"{float(g.get(k, 0)) * scale:g}")
            set_style(c, fontFamily=FONTS.get(locale, "Arial"))
        for point in g.iter("mxPoint"):
            for k, scale in [("x", sx), ("y", sy)]:
                if k in point.attrib:
                    point.set(k, f"{float(point.get(k)) * scale:g}")
        overrides = config.get("cells", {}).get(c.get("id"), {})
        for k, v in overrides.items():
            if k not in {"x", "y", "width", "height"} or not isinstance(v, (int, float)) or not math.isfinite(v):
                raise DiagramError(f"invalid geometry {locale}: {c.get('id')} {k}")
            if k in {"width", "height"} and v <= 0:
                raise DiagramError(f"invalid geometry {locale}: {c.get('id')} {k}")
            g.set(k, str(v))
    for cell_id, points in config.get("points", {}).items():
        if cell_id not in cells:
            raise DiagramError(f"unknown waypoint cell: {cell_id}")
        actual = list(cells[cell_id].iter("mxPoint"))
        if len(actual) != len(points):
            raise DiagramError(f"waypoint count: {cell_id}")
        for point, coords in zip(actual, points):
            for k, v in zip(("x", "y"), coords):
                point.set(k, str(v))
    model = page.find("mxGraphModel")
    for key, scale in [("pageWidth", sx), ("pageHeight", sy)]:
        model.set(key, str(float(model.get(key)) * scale))


def generate(template, catalog, layout):
    pages = list(template)
    if len(pages) != 2 or [p.get("name") for p in pages] != ["light", "dark"]:
        raise DiagramError("template must contain exactly light and dark workflow pages")
    graphs = []
    for page in pages:
        graph = {}
        for cell in page.iter("mxCell"):
            cell_id = cell.get("id")
            if cell_id in graph:
                raise DiagramError(f"duplicate cell: {cell_id}")
            geometry = cell.find("mxGeometry")
            graph[cell_id] = (
                tuple(cell.get(k) for k in ("parent", "source", "target", "vertex", "edge")),
                ET.tostring(geometry) if geometry is not None else None,
                bool(cell.get("value")),
            )
        for cell_id, (references, _, _) in graph.items():
            for attribute, reference in zip(("parent", "source", "target"), references[:3]):
                if reference is not None and reference not in graph:
                    raise DiagramError(f"unknown graph reference {page.get('name')}: {cell_id} {attribute}={reference}")
        graphs.append(graph)
    differences = [key for key in graphs[0].keys() | graphs[1].keys() if graphs[0].get(key) != graphs[1].get(key)]
    if differences:
        raise DiagramError(f"theme graph/geometry mismatch: {sorted(differences)}")
    keys = {c.get("id") for c in pages[0].iter("mxCell") if c.get("value")}
    if keys != set(catalog):
        raise DiagramError(f"catalog keys differ: {sorted(keys ^ set(catalog))}")
    if set(layout) != set(LOCALES):
        raise DiagramError("layout locale inventory differs")
    result = {}
    for locale in LOCALES:
        root = copy.deepcopy(template)
        for page in root:
            page.set("id", f"{locale}-{page.get('name')}")
            for cell in page.iter("mxCell"):
                if cell.get("value"):
                    cell_id = cell.get("id")
                    cell.set(
                        "value",
                        label(translated(catalog[cell_id], locale, cell_id), locale, cell_id, cell.get("value")),
                    )
            apply_layout(page, layout[locale], locale)
        ET.indent(root)
        result[locale] = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    return result


def write_generated(root, outputs):
    for locale, data in outputs.items():
        write(root, SOURCE / "generated" / f"{locale}.drawio", data)


def check_generated(root, outputs):
    for locale, expected in outputs.items():
        path = safe_path(root, SOURCE / "generated" / f"{locale}.drawio")
        if not path.exists() or path.read_bytes() != expected:
            raise DiagramError(f"stale generated diagram: {path}")


def overlap(a, b):
    x, y, w, h = a
    xx, yy, ww, hh = b
    if (x <= xx and y <= yy and x + w >= xx + ww and y + h >= yy + hh) or (
        xx <= x and yy <= y and xx + ww >= x + w and yy + hh >= y + h
    ):
        return False  # Intentional panel nesting; rendered text is checked separately.
    return min(x + w, xx + ww) - max(x, xx) > 1 and min(y + h, yy + hh) - max(y, yy) > 1


def geometry_findings(data):
    cells = []
    for c in ET.fromstring(data)[0].iter("mxCell"):
        if c.get("vertex") == "1":
            g = c.find("mxGeometry")
            cells.append((c.get("id"), tuple(float(g.get(k, 0)) for k in ("x", "y", "width", "height"))))
    return [(a, b) for i, (a, ga) in enumerate(cells) for b, gb in cells[i + 1 :] if overlap(ga, gb)]


def source_digest(root):
    names = [SOURCE / p for p in ("template.drawio", "catalog.json", "layout.json")]
    names.append(Path("internal/workflow_diagrams.py"))
    return digest(b"".join(p.as_posix().encode("utf-8") + b"\0" + safe_path(root, p).read_bytes() for p in names))


def asset_names():
    return {f"workflow-{lang}-{theme}.png" for lang in LOCALES for theme in ("light", "dark")}


def check_manifest(folder, manifest, source, expected=None):
    if manifest.get("source") != source:
        raise DiagramError("stale rendered assets: inputs changed; render and inspect again")
    expected = asset_names() if expected is None else expected
    if set(manifest.get("assets", {})) != expected:
        raise DiagramError("rendered asset inventory differs")
    for name, checksum in manifest["assets"].items():
        p = safe_path(folder, name)
        if not p.exists() or digest(p.read_bytes()) != checksum:
            raise DiagramError(f"stale or missing rendered asset: {name}")


def render(root, drawio):
    source = source_digest(root)
    folder = safe_path(root, ASSETS)
    folder.mkdir(parents=True, exist_ok=True)
    # Publish no images/manifest unless the complete export batch succeeds.
    with tempfile.TemporaryDirectory(prefix=".render-", dir=folder) as tmp:
        files = {}
        for locale in LOCALES:
            diagram = safe_path(root, SOURCE / "generated" / f"{locale}.drawio")
            for index, theme in enumerate(("light", "dark"), 1):
                name = f"workflow-{locale}-{theme}.png"
                output = Path(tmp) / name
                command = [
                    str(drawio),
                    "--export",
                    "--format",
                    "png",
                    "--page-index",
                    str(index),
                    "--scale",
                    "1",
                    "--border",
                    "24",
                    "--output",
                    str(output),
                    str(diagram),
                ]
                try:
                    subprocess.run(command, check=True, capture_output=True, text=True, timeout=120)
                    if not output.exists() or not output.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
                        raise DiagramError(f"render produced no PNG: {name}")
                except (OSError, subprocess.SubprocessError) as exc:
                    raise DiagramError(f"render failed for {name}: {exc}") from exc
                files[name] = output.read_bytes()
                print(f"rendered {name}", flush=True)
        if source_digest(root) != source:
            raise DiagramError("inputs changed during rendering; retry")
        for name, data in files.items():
            write(root, ASSETS / name, data)
        manifest = {"source": source, "assets": {n: digest(d) for n, d in files.items()}}
        write(root, ASSETS / "manifest.json", (json.dumps(manifest, indent=2) + "\n").encode())


def picture(locale, alt, full_size):
    light, dark = (f"assets/workflow/workflow-{locale}-{theme}.png" for theme in ("light", "dark"))
    return (
        f"<!-- workflow-diagram:start -->\n<picture>\n"
        f'  <source media="(prefers-color-scheme: dark)" srcset="{dark}">\n'
        f'  <img alt="{html.escape(alt, quote=True)}" src="{light}">\n</picture>\n\n'
        f"{full_size}: [☀️]({light}) · [🌙]({dark})\n<!-- workflow-diagram:end -->\n"
    )


class PictureParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.sources = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag == "source":
            self.sources.append(dict(attrs))
        elif tag == "img":
            self.images.append(dict(attrs))


def check_readmes(root):
    for locale in LOCALES:
        name = "README.md" if locale == "en" else f"README.{locale}.md"
        path = safe_path(root, name)
        text = path.read_text(encoding="utf-8")
        start, end = "<!-- workflow-diagram:start -->", "<!-- workflow-diagram:end -->"
        if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
            raise DiagramError(f"missing/duplicate workflow block: {name}")
        block = text.split(start)[1].split(end)[0]
        parser = PictureParser()
        parser.feed(block)
        dark = f"assets/workflow/workflow-{locale}-dark.png"
        light = f"assets/workflow/workflow-{locale}-light.png"
        if (
            len(parser.sources) != 1
            or len(parser.images) != 1
            or parser.sources[0].get("media") != "(prefers-color-scheme: dark)"
            or parser.sources[0].get("srcset") != dark
            or parser.images[0].get("src") != light
            or not parser.images[0].get("alt")
        ):
            raise DiagramError(f"incorrect workflow picture/theme: {name}")
        for theme in ("light", "dark"):
            if f"assets/workflow/workflow-{locale}-{theme}.png" not in text:
                raise DiagramError(f"missing {locale}/{theme} reference: {name}")
        if "prefers-color-scheme: dark" not in text or "<!-- workflow-diagram:start -->" not in text:
            raise DiagramError(f"missing themed picture: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--drawio", default="/Applications/draw.io.app/Contents/MacOS/draw.io")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        outputs = generate(*load(root))
        if args.write:
            write_generated(root, outputs)
        if args.render:
            check_generated(root, outputs)
            render(root, args.drawio)
        if args.check:
            check_generated(root, outputs)
            for locale, data in outputs.items():
                findings = geometry_findings(data)
                if findings:
                    raise DiagramError(f"overlapping shapes {locale}: {findings}")
            check_readmes(root)
            manifest = json.loads(safe_path(root, ASSETS / "manifest.json").read_text(encoding="utf-8"))
            check_manifest(root / ASSETS, manifest, source_digest(root))
        print("Workflow diagram checks passed." if args.check else "Workflow diagram sources validated.")
    except (DiagramError, OSError, ET.ParseError, json.JSONDecodeError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
