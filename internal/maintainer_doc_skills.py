"""Generate/check repository-only Codex documentation maintenance skills."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Mapping

from codexspec.integrations.codex import CodexIntegration
from internal.doc_translation import TranslationError, checked_path, checked_root

COMMANDS = ("check-i18n-semantics", "translate-docs", "update-workflow-diagrams")


class MaintainerSkillError(ValueError):
    """Report invalid sources/outputs or stale maintainer entries."""


def expected_entries(sources: Mapping[str, bytes]) -> dict[str, bytes]:
    renderer = CodexIntegration()
    return {
        f"codexspec-{name}": renderer.render_skill(name, sources[f"{name}.md"].decode("utf-8")).encode("utf-8")
        for name in COMMANDS
        if f"{name}.md" in sources
    }


def sync(root: Path, *, write: bool = False) -> list[str]:
    try:
        root = checked_root(root)
        sources = {}
        for name in COMMANDS:
            path = checked_path(root, f".claude/commands/codexspec/{name}.md")
            if not path.is_file():
                raise MaintainerSkillError(f"Source must be a regular file: {path}")
            sources[f"{name}.md"] = path.read_bytes()
        expected = expected_entries(sources)
        prepared = []
        # Preflight every output and all parents before creating or changing any entry.
        for name, content in expected.items():
            path = checked_path(root, f".agents/skills/{name}/SKILL.md", missing=True)
            if path.exists() and not path.is_file():
                raise MaintainerSkillError(f"Output must be a regular file: {path}")
            current = path.read_bytes() if path.exists() else None
            if current != content:
                prepared.append((path, content, "missing" if current is None else "stale"))
        if not write and prepared:
            raise MaintainerSkillError("; ".join(f"{state}: {path.relative_to(root)}" for path, _, state in prepared))
        if write:
            # Refuse a changed source rather than writing obsolete expected content.
            for name, original in sources.items():
                path = checked_path(root, f".claude/commands/codexspec/{name}")
                if path.read_bytes() != original:
                    raise MaintainerSkillError(f"Source changed during generation: {name}")
            for path, content, _ in prepared:
                checked_path(root, path, missing=True)
                path.parent.mkdir(parents=True, exist_ok=True)
                checked_path(root, path, missing=True)
                path.write_bytes(content)
        return [str(path.relative_to(root)) for path, _, _ in prepared]
    except (TranslationError, OSError, UnicodeError) as exc:
        raise MaintainerSkillError(str(exc)) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).absolute().parents[1])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    try:
        changed = sync(args.root, write=args.write)
        print(json.dumps({"mode": "write" if args.write else "check", "changed": changed}))
        return 0
    except MaintainerSkillError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
