"""Read-only inventory and Markdown checks for repository translations."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from unicodedata import normalize
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

LANGUAGES = ("zh", "ja", "ko", "es", "fr", "de", "pt-BR")
ALIASES = {**{name.lower(): name for name in LANGUAGES}, "zh-cn": "zh", "pt": "pt-BR"}
README_CODES = {**{name: name for name in LANGUAGES}, "zh": "zh-CN"}
LANGUAGE_LABELS = {
    "zh": "中文",
    "ja": "日本語",
    "ko": "한국어",
    "es": "Español",
    "fr": "Français",
    "de": "Deutsch",
    "pt-BR": "Português",
}
MARKDOWN = MarkdownIt("commonmark").enable("table")


class TranslationError(ValueError):
    """Report an unusable translation selection."""


def checked_root(root: Path) -> Path:
    root = root.absolute()
    for ancestor in (root, *root.parents):
        if ancestor.is_symlink():
            raise TranslationError(f"Redirected repository root: {ancestor}")
        if ancestor.exists() and not ancestor.is_dir():
            raise TranslationError(f"Non-directory root component: {ancestor}")
    if not root.is_dir():
        raise TranslationError(f"Repository root missing: {root}")
    return root


def checked_path(root: Path, value: str | Path, *, missing: bool = False) -> Path:
    root = checked_root(root)
    path = Path(value)
    if ".." in path.parts:
        raise TranslationError(f"Parent traversal is not allowed: {value}")
    path = path if path.is_absolute() else root / path
    metadata = root.stat()
    root_identity = (metadata.st_dev, metadata.st_ino)
    root_anchor = None
    for ancestor in (path, *path.parents):
        if ancestor.is_symlink():
            raise TranslationError(f"Redirected selected path: {ancestor}")
        if ancestor != path and ancestor.exists() and not ancestor.is_dir():
            raise TranslationError(f"Non-directory path component: {ancestor}")
        if root_anchor is None and ancestor.is_dir():
            metadata = ancestor.stat()
            if (metadata.st_dev, metadata.st_ino) == root_identity:
                root_anchor = ancestor
    if root_anchor is None:
        raise TranslationError(f"Path escapes selected checkout: {value}")
    path = root.joinpath(*path.relative_to(root_anchor).parts)
    if not missing and not path.exists():
        raise TranslationError(f"Selected source missing: {path}")
    if path.exists() and not (path.is_dir() or path.is_file()):
        raise TranslationError(f"Selected path is not a regular file/directory: {path}")
    if path.is_file() and path.stat().st_nlink != 1:
        raise TranslationError(f"Hard-linked selected file: {path}")
    return path


def canonical_source(root: Path, value: str | Path) -> Path:
    """Use actual directory-entry names without following redirected paths."""
    path = checked_path(root, value, missing=True)
    current = root
    for name in path.relative_to(root).parts:
        candidate = current / name
        if candidate.exists():
            entries = list(current.iterdir())
            exact = next((entry for entry in entries if entry.name == name), None)
            if exact is None:
                exact = next(entry for entry in entries if not entry.is_symlink() and entry.samefile(candidate))
            candidate = exact
        current = candidate
    return checked_path(root, current, missing=True)


def namespace_folds_case(root: Path) -> bool:
    """Check a real docs-directory alias before reserving folded fallback names."""
    namespace, alias = root / "docs", root / "DOCS"
    return namespace.is_dir() and alias.is_dir() and not alias.is_symlink() and namespace.samefile(alias)


def normalize_languages(value: str) -> list[str]:
    if value.strip().lower() == "all":
        return list(LANGUAGES)
    result = []
    for name in value.split(","):
        normalized = ALIASES.get(name.strip().lower())
        if normalized is None:
            raise TranslationError(f"Unsupported translation language: {name!r}; use {', '.join(LANGUAGES)}")
        if normalized in result:
            raise TranslationError(f"Duplicate translation language after alias normalization: {name}")
        result.append(normalized)
    return result


def inventory(
    root: Path,
    *,
    source: str | Path | None = None,
    readme: bool = False,
    languages: str = "all",
    incremental: bool = False,
) -> list[dict[str, str]]:
    root = checked_root(root)
    selected_languages = normalize_languages(languages)
    if source is None:
        selected = checked_path(root, "README.md" if readme else "docs/en")
    else:
        raw = Path(source)
        candidate = canonical_source(root, raw)
        folds_case = namespace_folds_case(root)
        reserved_readme = folds_case and len(raw.parts) == 1 and raw.name.casefold() == "readme.md"
        readme = readme or raw.parts == ("README.md",) or (reserved_readme and not candidate.exists())
        prefix = raw.parts[0].casefold() if folds_case and raw.parts else (raw.parts[0] if raw.parts else "")
        explicit_docs = prefix == "docs"
        if not candidate.exists() and not raw.is_absolute() and not readme and not explicit_docs:
            candidate = canonical_source(root, Path("docs/en") / raw)
        selected = checked_path(root, candidate)
    root_readme = root / "README.md"
    is_root_readme = not root_readme.is_symlink() and root_readme.exists() and selected.samefile(root_readme)
    readme = readme or is_root_readme
    if readme and not is_root_readme:
        raise TranslationError("README mode requires the root README.md source")
    if readme:
        selected = checked_path(root, root_readme)
    if readme and not selected.is_file():
        raise TranslationError("Root README.md source must be a regular file")
    if not readme and selected == root:
        raise TranslationError("Site mode needs an explicit documentation source, not the entire checkout")
    if selected.is_file():
        sources = [selected]
    else:
        sources = sorted(selected.rglob("*.md"))
    if not sources:
        raise TranslationError(f"No Markdown sources found: {selected}")
    sources = [checked_path(root, path) for path in sources]
    source_identities = set()
    for path in sources:
        if not path.is_file() or path.suffix != ".md":
            raise TranslationError(f"Source must be a Markdown file: {path}")
        metadata = path.stat()
        source_identities.add((metadata.st_dev, metadata.st_ino))
    english_docs = root / "docs/en"
    english_identity = None
    if english_docs.is_dir() and not english_docs.is_symlink():
        metadata = english_docs.stat()
        english_identity = (metadata.st_dev, metadata.st_ino)
    result = []
    destinations = set()
    destination_folds_case = namespace_folds_case(root)
    for path in sources:
        english_parent = None
        if not readme and english_identity is not None:
            for parent in path.parents:
                if parent == root:
                    break
                metadata = parent.stat()
                if (metadata.st_dev, metadata.st_ino) == english_identity:
                    english_parent = parent
                    break
        if readme:
            relative = Path("README.md")
        elif english_parent is not None:
            relative = path.relative_to(english_parent)
        else:
            relative = path.relative_to(selected) if selected.is_dir() else Path(path.name)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        for language in selected_languages:
            target = Path(f"README.{README_CODES[language]}.md") if readme else Path("docs") / language / relative
            destination = checked_path(root, target, missing=True)
            if destination.exists():
                if not destination.is_file():
                    raise TranslationError(f"Target must be a regular file: {destination}")
                metadata = destination.stat()
                if (metadata.st_dev, metadata.st_ino) in source_identities:
                    raise TranslationError(f"Translation target overlaps a selected source: {destination}")
            destination_key = tuple(
                normalize("NFC", part).casefold() if destination_folds_case else part
                for part in destination.relative_to(root).parts
            )
            if destination_key in destinations:
                raise TranslationError(f"Translation target has multiple sources: {destination}")
            destinations.add(destination_key)
            if incremental and destination.exists() and path.stat().st_mtime_ns <= destination.stat().st_mtime_ns:
                continue
            result.append(
                {
                    "surface": "readme" if readme else "docs",
                    "language": language,
                    "source": path.relative_to(root).as_posix(),
                    "target": target.as_posix(),
                    "source_sha256": digest,
                }
            )
    return result


def slug(text: str) -> str:
    text = re.sub(r"<[^>]*>", "", text).lower()
    text = re.sub(r"[^\w\-\s]", "", text)
    return re.sub(r"\s", "-", text)


def heading_anchors(tokens: list) -> set[str]:
    result = set()
    for index, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        children = tokens[index + 1].children or []
        text = "".join(child.content for child in children if child.type in {"text", "code_inline"})
        base = slug(text)
        candidate, suffix = base, 0
        while candidate in result:
            suffix += 1
            candidate = f"{base}-{suffix}"
        result.add(candidate)
    return result


class HTMLLinks(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        for key in ("id", "name"):
            if values.get(key):
                self.anchors.add(values[key])
        for key in ("href", "src"):
            if values.get(key):
                self.links.append(values[key])
        if values.get("srcset"):
            self.links.extend(item.strip().split()[0] for item in values["srcset"].split(",") if item.strip())


def document(content: str) -> dict:
    tokens = MARKDOWN.parse(content)
    headings, examples, code, tables, links = [], [], [], [], []
    table = None
    cells = 0
    html = HTMLLinks()
    for token in tokens:
        if token.type == "heading_open":
            headings.append(token.tag)
        elif token.type in {"fence", "code_block"}:
            examples.append((token.type, token.info, token.content))
        elif token.type == "table_open":
            table = []
        elif token.type == "tr_open":
            cells = 0
        elif token.type in {"th_open", "td_open"}:
            cells += 1
        elif token.type == "tr_close" and table is not None:
            table.append(cells)
        elif token.type == "table_close":
            tables.append(table)
            table = None
        if token.type == "html_block":
            html.feed(token.content)
        if token.type == "inline":
            for child in token.children or []:
                if child.type == "code_inline":
                    code.append(child.content)
                elif child.type in {"link_open", "image"}:
                    value = child.attrGet("href" if child.type == "link_open" else "src")
                    if value:
                        links.append(value)
                elif child.type == "html_inline":
                    html.feed(child.content)
    # The parser may truncate extra table cells; verify the raw Markdown row width.
    raw_widths = []
    in_fence = False
    marker = ""
    for line in content.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            if not in_fence:
                in_fence, marker = True, match.group(1)[0]
            elif match.group(1)[0] == marker:
                in_fence = False
            continue
        if not in_fence and line.strip().startswith("|"):
            row = line.strip().strip("|")
            raw_widths.append(len(re.split(r"(?<!\\)\|", row)))
    return {
        "headings": headings,
        "examples": examples,
        "inline": Counter(code),
        "tables": tables,
        "row_widths": raw_widths,
        "links": links + html.links,
        "anchors": heading_anchors(tokens) | html.anchors,
    }


def link_errors(root: Path, target: Path, analysis: dict) -> list[str]:
    errors = []
    for destination in analysis["links"]:
        url = urlsplit(destination)
        if url.scheme or url.netloc:
            continue
        raw_path, anchor = unquote(url.path), unquote(url.fragment)
        path = (
            target
            if not raw_path
            else (root / raw_path.lstrip("/") if raw_path.startswith("/") else target.parent / raw_path)
        )
        # Relative documentation references legitimately use ../ within the checkout.
        resolved = path.resolve()
        if not resolved.is_relative_to(root):
            errors.append(f"local link escapes checkout: {destination}")
            continue
        if not resolved.exists():
            errors.append(f"local link missing: {destination}")
            continue
        if anchor and resolved.is_file() and resolved.suffix == ".md":
            anchors = (
                analysis["anchors"] if resolved == target else document(resolved.read_text(encoding="utf-8"))["anchors"]
            )
            if anchor not in anchors:
                errors.append(f"heading anchor missing: {destination}")
    return errors


def verify_pairs(root: Path, pairs: list[dict[str, str]]) -> list[dict[str, str]]:
    root = checked_root(root)
    errors = []
    for pair in pairs:
        source = checked_path(root, pair["source"])
        target = checked_path(root, pair["target"], missing=True)
        problems = []
        if hashlib.sha256(source.read_bytes()).hexdigest() != pair["source_sha256"]:
            problems.append("source changed since inventory")
        if not target.is_file():
            problems.append("translation target missing")
        else:
            source_text = source.read_text(encoding="utf-8")
            target_text = target.read_text(encoding="utf-8")
            before, after = document(source_text), document(target_text)
            for key, diagnostic in (
                ("headings", "heading hierarchy differs"),
                ("examples", "fenced code/example differs"),
                ("inline", "inline technical tokens differ"),
                ("tables", "table structure differs"),
                ("row_widths", "table row widths differ"),
            ):
                if before[key] != after[key]:
                    problems.append(diagnostic)
            problems.extend(link_errors(root, target, after))
            if pair["surface"] == "readme" and 'href="README.zh-CN.md"' in source_text:
                label = LANGUAGE_LABELS[pair["language"]]
                if f"<b>{label}</b>" not in target_text:
                    problems.append("active language navigation is incorrect")
                for code in ("", ".zh-CN", ".ja", ".ko", ".es", ".fr", ".de", ".pt-BR"):
                    name = f"README{code}.md"
                    if name == target.name:
                        continue
                    if f'href="{name}"' not in target_text:
                        problems.append(f"language navigation missing: {name}")
        errors.extend(
            {
                "language": pair["language"],
                "source": pair["source"],
                "target": pair["target"],
                "problem": problem,
            }
            for problem in problems
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("inventory", "verify"))
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parents[1])
    parser.add_argument("--readme", action="store_true")
    parser.add_argument("--source")
    parser.add_argument("--lang", "-l", default="all")
    parser.add_argument("--incremental", "-i", action="store_true")
    parser.add_argument("--dry-run", "-d", action="store_true")
    args = parser.parse_args(argv)
    try:
        root = checked_root(args.root)
        pairs = inventory(
            root,
            source=args.source,
            readme=args.readme,
            languages=args.lang,
            incremental=args.incremental,
        )
        errors = verify_pairs(root, pairs) if args.operation == "verify" else []
        print(
            json.dumps(
                {
                    "root": str(root),
                    "operation": args.operation,
                    "pairs": pairs,
                    "errors": errors,
                    "dry_run": args.dry_run,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1 if errors else 0
    except (TranslationError, OSError, UnicodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
