"""Inventory first, then optionally prepare and apply individually checked upgrades."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import httpx
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from codexspec.i18n import get_interaction_language
from codexspec.translator import translate

from .discovery import discover
from .release import acquire_release
from .upgrade import UnsafeProjectError, apply_plan, preflight, prepare_plan, project_options, state


def is_interactive() -> bool:
    return sys.stdin.isatty()


def run_scan(start: Path, *, upgrade: bool, yes: bool, console: Console) -> int:
    language = get_interaction_language()

    def message(key: str, **values) -> str:
        full_key = f"cli.scan.{key}"
        result = translate(full_key, language, **values)
        return translate(full_key, "en", **values) if result == full_key else result

    def report(key: str, **values) -> None:
        console.print(message(key, **values), markup=False, highlight=False)

    if yes and not upgrade:
        report("yes_requires_upgrade")
        return 2
    if upgrade and not yes and not is_interactive():
        report("noninteractive")
        return 2
    try:
        inventory = discover(start)
    except (OSError, ValueError) as exc:
        report("error", reason=str(exc))
        return 2
    table = Table(title=message("title"))
    for key in ("repository", "path", "version", "content"):
        table.add_column(message(key), overflow="fold")
    for item in inventory.installations:
        check = item.inspection
        table.add_row(
            Text(item.repository or message("no_git")),
            Text(str(item.path)),
            Text(check.version or message("unknown")),
            Text(message(check.state)),
        )
    if inventory.installations:
        console.print(table)
    else:
        report("empty")
    for item in inventory.installations:
        if item.inspection.differences:
            report("differences", path=item.path, files=", ".join(item.inspection.differences))
        if item.inspection.reason:
            report("detail", path=item.path, reason=item.inspection.reason)
    for issue in inventory.issues:
        report("incomplete", reason=issue)
    if not upgrade and any(
        item.inspection.state in {"inconsistent", "no_baseline"} for item in inventory.installations
    ):
        report("upgrade_hint")
    if not upgrade or not inventory.installations:
        return int(bool(inventory.issues))

    upgraded = skipped = failed = current = 0
    problem = bool(inventory.issues)
    all_remaining = yes
    cancelled = False
    try:
        report("acquiring")
        with acquire_release() as release:
            report("target", version=release.version)
            for index, item in enumerate(inventory.installations):
                root = item.path
                try:
                    # Preserve inputs captured before target rendering, including during prompts.
                    inputs = {
                        name: state(root, name)
                        for name in (
                            ".codexspec/config.yml",
                            "CLAUDE.md",
                            "AGENTS.md",
                            ".codexspec/.gitignore",
                        )
                    }
                    ai, language_choice = project_options(root)
                    files = release.render(root, ai, language_choice)
                    plan = prepare_plan(root, release.version, ai, language_choice, files)
                    plan.inputs = inputs
                    preflight(plan)
                except (OSError, ValueError, subprocess.SubprocessError) as exc:
                    skipped += 1
                    problem = True
                    report("skipped", path=root, reason=str(exc))
                    continue
                if not plan.changes:
                    current += 1
                    report("current", path=root)
                    continue
                if not all_remaining:
                    choice = Prompt.ask(
                        Text(message("prompt", path=root)), choices=["y", "n", "a", "q"], default="n", console=console
                    )
                    if choice == "q":
                        skipped += len(inventory.installations) - index
                        cancelled = True
                        report("cancelled")
                        break
                    if choice == "n":
                        skipped += 1
                        report("declined", path=root)
                        continue
                    all_remaining = choice == "a"
                try:
                    apply_plan(plan)
                except UnsafeProjectError as exc:
                    skipped += 1
                    problem = True
                    report("skipped", path=root, reason=str(exc))
                    continue
                except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
                    failed += 1
                    problem = True
                    report("failed", path=root, reason=str(exc))
                    continue
                upgraded += 1
                report("upgraded", path=root)
    except (OSError, ValueError, httpx.HTTPError, subprocess.SubprocessError) as exc:
        report("acquisition_failed", reason=str(exc))
        return 1
    except (KeyboardInterrupt, EOFError):
        report("cancelled")
        cancelled = True
    report("summary", upgraded=upgraded, current=current, skipped=skipped, failed=failed)
    return 1 if problem or cancelled else 0
