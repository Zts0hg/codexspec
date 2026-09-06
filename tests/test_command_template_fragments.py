"""Tests for maintainer-only shared command template fragments."""

from __future__ import annotations

import os
import stat
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from codexspec.integrations.claude import ClaudeIntegration
from codexspec.integrations.codex import CodexIntegration
from internal import command_template_fragments
from internal.command_template_fragments import (
    FragmentError,
    check_outputs,
    check_self_bootstrap,
    main,
    render_sources,
    write_outputs,
)

ROOT = Path(__file__).parent.parent


def _roots(tmp_path: Path) -> tuple[Path, Path, Path]:
    sources = tmp_path / "sources"
    fragments = tmp_path / "fragments"
    outputs = tmp_path / "outputs"
    sources.mkdir()
    fragments.mkdir()
    outputs.mkdir()
    return sources, fragments, outputs


def _directive(name: str, newline: bytes = b"\n") -> bytes:
    return f"<!-- CODEXSPEC:INCLUDE {name} -->".encode() + newline


def test_render_sources_inserts_literal_fragment_bytes_for_arbitrary_commands(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"shared\n")
    (sources / "first.md").write_bytes(b"before\n" + _directive("shared.md") + b"after\n")
    (sources / "second.md").write_bytes(_directive("shared.md") * 2)

    rendered = render_sources(sources, fragments)

    assert rendered == {
        Path("first.md"): b"before\nshared\nafter\n",
        Path("second.md"): b"shared\nshared\n",
    }


def test_render_sources_preserves_fragment_order_and_all_other_source_bytes(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (fragments / "one.md").write_bytes(b"ONE")
    (fragments / "two.md").write_bytes(b"TWO\n")
    source = b"\xef\xbb\xbfstart\r\n" + _directive("one.md", b"\r\n") + b"middle\n" + _directive("two.md", b"")
    (sources / "ordered.md").write_bytes(source)

    rendered = render_sources(sources, fragments)

    assert rendered[Path("ordered.md")] == b"\xef\xbb\xbfstart\r\nONEmiddle\nTWO\n"


def test_render_sources_preserves_utf8_crlf_and_directive_at_eof(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    fragment = "共享内容\r\n".encode()
    (fragments / "utf8.md").write_bytes(fragment)
    (sources / "crlf.md").write_bytes(b"head\r\n" + _directive("utf8.md", b"\r\n") + b"tail\r\n")
    (sources / "eof.md").write_bytes(b"head\n" + _directive("utf8.md", b""))

    rendered = render_sources(sources, fragments)

    assert rendered[Path("crlf.md")] == b"head\r\n" + fragment + b"tail\r\n"
    assert rendered[Path("eof.md")] == b"head\n" + fragment


def test_render_sources_rejects_missing_fragment(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (sources / "broken.md").write_bytes(_directive("missing.md"))

    with pytest.raises(FragmentError, match=r"broken\.md.*missing\.md.*does not exist"):
        render_sources(sources, fragments)


def test_render_sources_rejects_nested_fragment(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (sources / "broken.md").write_bytes(_directive("outer.md"))
    (fragments / "outer.md").write_bytes(b"outer\n" + _directive("inner.md"))
    (fragments / "inner.md").write_bytes(b"inner\n")

    with pytest.raises(FragmentError, match=r"outer\.md.*nested fragment directives are forbidden"):
        render_sources(sources, fragments)


def test_render_sources_allows_inline_directive_examples_as_literal_bytes(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    inline = b"Example: <!-- CODEXSPEC:INCLUDE example.md --> stays literal.\n"
    (fragments / "shared.md").write_bytes(inline)
    (sources / "example.md").write_bytes(inline + _directive("shared.md"))

    rendered = render_sources(sources, fragments)

    assert rendered[Path("example.md")] == inline + inline


def test_render_sources_preserves_non_directive_standalone_comments(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    source = (
        b"<!-- DECODEXED build note -->\n"
        b"<!-- ASPECT:INCLUDED for context -->\n"
        b"<!-- SPECIFICATION includes examples -->\n"
    )
    (sources / "comments.md").write_bytes(source)

    rendered = render_sources(sources, fragments)

    assert rendered[Path("comments.md")] == source


@pytest.mark.parametrize(
    "fragment_name",
    [
        "",
        "/absolute.md",
        ".",
        "./dot.md",
        "../escape.md",
        "nested/../escape.md",
        r"..\escape.md",
        "C:/absolute.md",
        "C:drive-relative.md",
        "shared.md:stream",
        "CON.md",
    ],
)
def test_render_sources_rejects_unsafe_fragment_paths(tmp_path: Path, fragment_name: str) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (sources / "broken.md").write_bytes(_directive(fragment_name))

    with pytest.raises(FragmentError, match=r"broken\.md.*(?:fragment path|malformed fragment directive)"):
        render_sources(sources, fragments)


def test_render_sources_rejects_symlink_that_escapes_fragment_root(tmp_path: Path) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    sources, fragments, _ = _roots(tmp_path)
    outside = tmp_path / "outside.md"
    outside.write_bytes(b"outside\n")
    try:
        (fragments / "link.md").symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")
    (sources / "broken.md").write_bytes(_directive("link.md"))

    with pytest.raises(FragmentError, match=r"link\.md.*symbolic link"):
        render_sources(sources, fragments)


def test_render_sources_rejects_fragment_symlink_inside_fragment_root(tmp_path: Path) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    sources, fragments, _ = _roots(tmp_path)
    (fragments / "target.md").write_bytes(b"target\n")
    try:
        (fragments / "link.md").symlink_to("target.md")
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")
    (sources / "broken.md").write_bytes(_directive("link.md"))

    with pytest.raises(FragmentError, match=r"link\.md.*symbolic link"):
        render_sources(sources, fragments)


def test_render_sources_rejects_symlinked_fragment_parent(tmp_path: Path) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    sources, fragments, _ = _roots(tmp_path)
    real_directory = fragments / "real"
    real_directory.mkdir()
    (real_directory / "shared.md").write_bytes(b"shared\n")
    try:
        (fragments / "linked").symlink_to(real_directory, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")
    (sources / "broken.md").write_bytes(_directive("linked/shared.md"))

    with pytest.raises(FragmentError, match=r"linked.*symbolic link"):
        render_sources(sources, fragments)


def test_render_sources_rejects_symlinked_source(tmp_path: Path) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    sources, fragments, _ = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"shared\n")
    outside = tmp_path / "outside-source.md"
    outside.write_bytes(_directive("shared.md"))
    try:
        (sources / "linked.md").symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")

    with pytest.raises(FragmentError, match=r"linked\.md.*symbolic link"):
        render_sources(sources, fragments)


@pytest.mark.parametrize(
    "source",
    [
        b"<!-- CODEXSPEC:INCLUDE shared.md-->\n",
        b"<!-- CODEXSPEC:INCLUDE  shared.md -->\n",
        b"<!-- CODEXSPEC:INCLUDE shared.md --> suffix\n",
        b"<!--  CODEXSPEC:INCLUDE shared.md -->\n",
        b"<!-- CODEXSPEC :INCLUDE shared.md -->\n",
        b" <!-- CODEXSPEC:INCLUDE shared.md -->\n",
        b"<!-- codexspec:include shared.md -->\n",
        b"<!-- CODEXSPEC:INCLUD shared.md -->\n",
        b"<!-- CODEXSPEC:INCLD shared.md -->\n",
        b"<!-- CODEXSPEC:EXCLUDE shared.md -->\n",
        b"<!-- CODEXSPEC:INSERT shared.md -->\n",
        b"<!-- CODEXSPEC fragment note -->\n",
        b"<!-- CODXSPEC:INCLUDE shared.md -->\n",
        b"<!-- CODEXSPC:INCLUDE shared.md -->\n",
        b"<!-- CODEYSPEC:INCLUDE shared.md -->\n",
        b"<!-- CODE.SPEC:INCLUDE shared.md -->\n",
        b"<!-- CODE$SPEC:INCLUDE shared.md -->\n",
        b"<!-- CODESPEC:INCLUDE shared.md -->\n",
        b"<!-- CODEXSPE:INCLUDE shared.md -->\n",
        b"<!-- CODEXSPECX:INCLUDE shared.md -->\n",
        b"<!-- CODEXSPEC:INCLUDE shared.md -->\r",
        b"\xef\xbb\xbf<!-- CODEXSPEC:INCLUDE shared.md -->\n",
    ],
)
def test_render_sources_rejects_malformed_directive_like_text(tmp_path: Path, source: bytes) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"shared\n")
    (sources / "broken.md").write_bytes(source)

    with pytest.raises(FragmentError, match=r"broken\.md.*malformed fragment directive"):
        render_sources(sources, fragments)


@pytest.mark.parametrize(
    "fragment_name",
    ["bad?.md", "bad*.md", "bad<.md", "bad|.md", 'bad".md', "CONIN$.md", "CONOUT$.md", "COM¹.md"],
)
def test_render_sources_rejects_windows_forbidden_fragment_characters(
    tmp_path: Path,
    fragment_name: str,
) -> None:
    sources, fragments, _ = _roots(tmp_path)
    try:
        (fragments / fragment_name).write_bytes(b"shared\n")
    except OSError as exc:
        pytest.skip(f"host filesystem cannot create the portable-name counterexample: {exc}")
    (sources / "broken.md").write_bytes(_directive(fragment_name))

    with pytest.raises(FragmentError, match=r"broken\.md.*unsafe fragment path"):
        render_sources(sources, fragments)


@pytest.mark.parametrize(
    "source_name",
    [
        ".md",
        "CON.md",
        "AUX.md",
        "bad?.md",
        pytest.param(
            "C:drive.md",
            marks=pytest.mark.skipif(
                sys.platform == "win32",
                reason="a drive-anchored name resolves outside the temporary root on Windows",
            ),
        ),
    ],
)
def test_render_sources_rejects_unsafe_source_basenames(tmp_path: Path, source_name: str) -> None:
    sources, fragments, _ = _roots(tmp_path)
    try:
        (sources / source_name).write_bytes(b"content\n")
    except OSError as exc:
        pytest.skip(f"host filesystem cannot create the portable-name counterexample: {exc}")

    with pytest.raises(FragmentError, match=r"unsafe command source name"):
        render_sources(sources, fragments)


def test_render_sources_rejects_non_regular_markdown_source_entry(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (sources / "not-a-file.md").mkdir()

    with pytest.raises(FragmentError, match=r"not-a-file\.md.*not a regular file"):
        render_sources(sources, fragments)


def test_render_sources_rejects_case_colliding_source_basenames(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (sources / "Command.md").write_bytes(b"one\n")
    try:
        (sources / "command.md").write_bytes(b"two\n")
    except OSError as exc:
        pytest.skip(f"host filesystem is already case-insensitive: {exc}")
    if len(list(sources.glob("*.md"))) < 2:
        pytest.skip("host filesystem is already case-insensitive")

    with pytest.raises(FragmentError, match=r"case-colliding command source names"):
        render_sources(sources, fragments)


def test_render_sources_rejects_unreferenced_unsafe_fragment_name(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (sources / "command.md").write_bytes(b"content\n")
    try:
        (fragments / "bad?.md").write_bytes(b"unused\n")
    except OSError as exc:
        pytest.skip(f"host filesystem cannot create the portable-name counterexample: {exc}")

    with pytest.raises(FragmentError, match=r"unsafe fragment entry name"):
        render_sources(sources, fragments)


def test_render_sources_rejects_nested_directive_in_unreferenced_fragment(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (sources / "command.md").write_bytes(b"content\n")
    (fragments / "unused.md").write_bytes(_directive("other.md"))

    with pytest.raises(FragmentError, match=r"unused\.md.*nested fragment directives are forbidden"):
        render_sources(sources, fragments)


def test_render_sources_supports_standard_macos_tempfile_physical_alias() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        sources, fragments, _ = _roots(root)
        (fragments / "shared.md").write_bytes(b"fragment\r\n")
        (sources / "command.md").write_bytes(b"before\r\n" + _directive("shared.md") + b"after\n")

        rendered = render_sources(sources, fragments)

    assert rendered[Path("command.md")] == b"before\r\nfragment\r\nafter\n"


def test_render_sources_rejects_fragment_reference_with_non_exact_spelling(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"shared\n")
    (sources / "command.md").write_bytes(_directive("Shared.md"))

    with pytest.raises(FragmentError, match=r"Shared\.md.*exact stored spelling"):
        render_sources(sources, fragments)


@pytest.mark.parametrize("fragment_name", ["shared.MD", "shared.txt", "shared"])
def test_render_sources_rejects_fragment_references_without_lowercase_md_extension(
    tmp_path: Path,
    fragment_name: str,
) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (fragments / fragment_name).write_bytes(b"shared\n")
    (sources / "command.md").write_bytes(_directive(fragment_name))

    with pytest.raises(FragmentError, match=r"unsafe fragment path"):
        render_sources(sources, fragments)


@pytest.mark.parametrize("fragment_name", ["unused.MD", "unused.txt", "unused"])
def test_render_sources_rejects_unreferenced_fragment_files_without_lowercase_md_extension(
    tmp_path: Path,
    fragment_name: str,
) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (sources / "command.md").write_bytes(b"content\n")
    (fragments / fragment_name).write_bytes(b"unused\n")

    with pytest.raises(FragmentError, match=r"unsafe fragment entry name"):
        render_sources(sources, fragments)


def test_render_sources_rejects_uppercase_markdown_source_extension(tmp_path: Path) -> None:
    sources, fragments, _ = _roots(tmp_path)
    (sources / "command.MD").write_bytes(b"content\n")

    with pytest.raises(FragmentError, match=r"unsafe command source name.*command\.MD"):
        render_sources(sources, fragments)


def test_render_sources_rejects_symlinked_root_ancestor(tmp_path: Path) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    real_parent = tmp_path / "real-parent"
    sources = real_parent / "sources"
    fragments = real_parent / "fragments"
    sources.mkdir(parents=True)
    fragments.mkdir()
    (sources / "command.md").write_bytes(b"content\n")
    alias = tmp_path / "alias"
    try:
        alias.symlink_to(real_parent, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")

    with pytest.raises(FragmentError, match=r"symbolic link"):
        render_sources(alias / "sources", alias / "fragments")


def test_check_outputs_reports_missing_and_stale_outputs_without_writing(tmp_path: Path) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"new\n")
    (sources / "missing.md").write_bytes(_directive("shared.md"))
    (sources / "stale.md").write_bytes(_directive("shared.md"))
    stale = outputs / "stale.md"
    stale.write_bytes(b"old\n")

    with pytest.raises(FragmentError) as captured:
        check_outputs(sources, fragments, outputs)

    message = str(captured.value)
    assert "missing.md: generated output is missing" in message
    assert "stale.md: generated output is stale" in message
    assert stale.read_bytes() == b"old\n"
    assert not (outputs / "missing.md").exists()


def test_write_outputs_prevalidates_every_source_before_writing(tmp_path: Path) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"new\n")
    (sources / "first.md").write_bytes(_directive("shared.md"))
    (sources / "second.md").write_bytes(_directive("missing.md"))
    first = outputs / "first.md"
    first.write_bytes(b"old\n")

    with pytest.raises(FragmentError, match=r"second\.md.*missing\.md"):
        write_outputs(sources, fragments, outputs)

    assert first.read_bytes() == b"old\n"
    assert not (outputs / "second.md").exists()


def test_write_outputs_replaces_only_changed_opted_in_outputs_atomically(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"new\n")
    (sources / "changed.md").write_bytes(_directive("shared.md"))
    (sources / "same.md").write_bytes(b"same\n")
    (outputs / "changed.md").write_bytes(b"old\n")
    (outputs / "same.md").write_bytes(b"same\n")
    unmanaged = outputs / "unmanaged.md"
    unmanaged.write_bytes(b"keep\n")
    replace_calls: list[tuple[Path, Path]] = []
    real_replace = os.replace

    def recording_replace(source: str | os.PathLike[str], destination: str | os.PathLike[str]) -> None:
        replace_calls.append((Path(source), Path(destination)))
        real_replace(source, destination)

    monkeypatch.setattr("internal.command_template_fragments.os.replace", recording_replace)

    changed = write_outputs(sources, fragments, outputs)

    assert changed == [Path("changed.md")]
    assert (outputs / "changed.md").read_bytes() == b"new\n"
    assert (outputs / "same.md").read_bytes() == b"same\n"
    assert unmanaged.read_bytes() == b"keep\n"
    assert [destination for _, destination in replace_calls] == [outputs / "changed.md"]


@pytest.mark.parametrize("operation", ["check", "write"])
def test_output_operations_reject_symlinked_outputs_without_mutating_target(
    tmp_path: Path,
    operation: str,
) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"new\n")
    (sources / "linked.md").write_bytes(_directive("shared.md"))
    outside = tmp_path / "outside-output.md"
    outside.write_bytes(b"old\n")
    try:
        (outputs / "linked.md").symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")

    function = check_outputs if operation == "check" else write_outputs
    with pytest.raises(FragmentError, match=r"linked\.md.*symbolic link"):
        function(sources, fragments, outputs)

    assert outside.read_bytes() == b"old\n"


def test_write_outputs_prevalidates_all_output_symlinks_before_writing(tmp_path: Path) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"new\n")
    (sources / "first.md").write_bytes(_directive("shared.md"))
    (sources / "second.md").write_bytes(_directive("shared.md"))
    first = outputs / "first.md"
    first.write_bytes(b"old\n")
    outside = tmp_path / "outside-output.md"
    outside.write_bytes(b"old\n")
    try:
        (outputs / "second.md").symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")

    with pytest.raises(FragmentError, match=r"second\.md.*symbolic link"):
        write_outputs(sources, fragments, outputs)

    assert first.read_bytes() == b"old\n"
    assert outside.read_bytes() == b"old\n"


@pytest.mark.parametrize("invalid_kind", ["directory", "fifo"])
def test_write_outputs_prevalidates_all_non_regular_outputs_before_writing(
    tmp_path: Path,
    invalid_kind: str,
) -> None:
    if invalid_kind == "fifo" and not hasattr(os, "mkfifo"):
        pytest.skip("FIFOs are unavailable")
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"new\n")
    (sources / "first.md").write_bytes(_directive("shared.md"))
    (sources / "second.md").write_bytes(_directive("shared.md"))
    first = outputs / "first.md"
    first.write_bytes(b"old\n")
    invalid = outputs / "second.md"
    if invalid_kind == "directory":
        invalid.mkdir()
    else:
        os.mkfifo(invalid)

    with pytest.raises(FragmentError, match=r"second\.md.*not a regular file"):
        write_outputs(sources, fragments, outputs)

    assert first.read_bytes() == b"old\n"


def test_write_outputs_rejects_output_root_with_symlinked_ancestor(tmp_path: Path) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    sources, fragments, _ = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"new\n")
    (sources / "command.md").write_bytes(_directive("shared.md"))
    real_parent = tmp_path / "real-output-parent"
    real_output = real_parent / "outputs"
    real_output.mkdir(parents=True)
    target = real_output / "command.md"
    target.write_bytes(b"old\n")
    alias = tmp_path / "output-alias"
    try:
        alias.symlink_to(real_parent, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")

    with pytest.raises(FragmentError, match=r"symbolic link"):
        write_outputs(sources, fragments, alias / "outputs")

    assert target.read_bytes() == b"old\n"


def test_write_outputs_rejects_case_collision_with_unmanaged_output(tmp_path: Path) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"new-owned\n")
    (sources / "Foo.md").write_bytes(_directive("shared.md"))
    unmanaged = outputs / "foo.md"
    unmanaged.write_bytes(b"unmanaged-old\n")

    with pytest.raises(FragmentError, match=r"Foo\.md.*collides.*foo\.md"):
        write_outputs(sources, fragments, outputs)

    assert unmanaged.read_bytes() == b"unmanaged-old\n"


def test_check_outputs_rejects_non_regular_unmanaged_command_entry(tmp_path: Path) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (outputs / "not-a-file.md").mkdir()

    with pytest.raises(FragmentError, match=r"not-a-file\.md.*not a regular file"):
        check_outputs(sources, fragments, outputs)


@pytest.mark.parametrize("alias_name", ["FOO.MD", "foo.md.", "foo.md "])
@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Windows strips trailing dots and spaces and ignores name case, so the alias fixtures cannot exist",
)
def test_write_outputs_rejects_output_alias_outside_lowercase_md_glob(
    tmp_path: Path,
    alias_name: str,
) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"generated\n")
    (sources / "foo.md").write_bytes(_directive("shared.md"))
    alias = outputs / alias_name
    alias.write_bytes(b"unmanaged\n")

    with pytest.raises(FragmentError, match=r"unsafe command output name|collides"):
        write_outputs(sources, fragments, outputs)

    assert alias.read_bytes() == b"unmanaged\n"


def test_write_outputs_rejects_output_changed_in_place_after_prevalidation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"generated\n")
    (sources / "command.md").write_bytes(_directive("shared.md"))
    output = outputs / "command.md"
    output.write_bytes(b"old-value\n")
    real_atomic_write = command_template_fragments._atomic_write

    def change_then_write(*args: object, **kwargs: object) -> None:
        output.write_bytes(b"concurrent\n")
        real_atomic_write(*args, **kwargs)

    monkeypatch.setattr(command_template_fragments, "_atomic_write", change_then_write)

    with pytest.raises(FragmentError, match=r"changed after prevalidation"):
        write_outputs(sources, fragments, outputs)

    assert output.read_bytes() == b"concurrent\n"


def test_write_outputs_rechecks_sources_after_output_prevalidation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    fragment = fragments / "shared.md"
    fragment.write_bytes(b"generated\n")
    (sources / "command.md").write_bytes(_directive("shared.md"))
    output = outputs / "command.md"
    output.write_bytes(b"old\n")
    real_inspect = command_template_fragments._inspect_output

    def inspect_then_change(*args: object, **kwargs: object) -> object:
        inspected = real_inspect(*args, **kwargs)
        fragment.write_bytes(b"concurrent\n")
        return inspected

    monkeypatch.setattr(command_template_fragments, "_inspect_output", inspect_then_change)

    with pytest.raises(FragmentError, match=r"sources or fragments changed before writing"):
        write_outputs(sources, fragments, outputs)

    assert output.read_bytes() == b"old\n"


def test_write_outputs_rejects_replaced_output_root_before_creating_missing_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"generated\n")
    (sources / "command.md").write_bytes(_directive("shared.md"))
    moved_outputs = tmp_path / "outputs-moved"
    real_named_temporary_file = command_template_fragments.tempfile.NamedTemporaryFile
    replaced = False

    def replace_root_then_create_temp(*args: object, **kwargs: object) -> object:
        nonlocal replaced
        if not replaced:
            outputs.rename(moved_outputs)
            outputs.mkdir()
            replaced = True
        return real_named_temporary_file(*args, **kwargs)

    monkeypatch.setattr(
        command_template_fragments.tempfile,
        "NamedTemporaryFile",
        replace_root_then_create_temp,
    )

    with pytest.raises(FragmentError, match=r"output root.*directory changed"):
        write_outputs(sources, fragments, outputs)

    assert not (outputs / "command.md").exists()
    assert not (moved_outputs / "command.md").exists()
    assert not list(outputs.iterdir())


def test_write_outputs_rejects_same_byte_fragment_replacement_after_prevalidation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    fragment = fragments / "shared.md"
    fragment.write_bytes(b"generated\n")
    (sources / "command.md").write_bytes(_directive("shared.md"))
    output = outputs / "command.md"
    output.write_bytes(b"old\n")
    real_inspect = command_template_fragments._inspect_output

    def inspect_then_replace(*args: object, **kwargs: object) -> object:
        inspected = real_inspect(*args, **kwargs)
        replacement = fragments / "replacement.tmp"
        replacement.write_bytes(fragment.read_bytes())
        os.replace(replacement, fragment)
        return inspected

    monkeypatch.setattr(command_template_fragments, "_inspect_output", inspect_then_replace)

    with pytest.raises(FragmentError, match=r"sources or fragments changed before writing"):
        write_outputs(sources, fragments, outputs)

    assert output.read_bytes() == b"old\n"


def test_check_outputs_binds_content_to_returned_output_signature(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (sources / "command.md").write_bytes(b"expected\n")
    output = outputs / "command.md"
    output.write_bytes(b"expected\n")
    real_read = command_template_fragments._read_stable_file_snapshot

    def read_then_change(
        path: Path,
        root: Path,
        display: str,
    ) -> tuple[bytes, command_template_fragments.StatSignature]:
        snapshot = real_read(path, root, display)
        if path == output:
            output.write_bytes(b"changed!\n")
        return snapshot

    monkeypatch.setattr(command_template_fragments, "_read_stable_file_snapshot", read_then_change)

    with pytest.raises(FragmentError, match=r"changed during prevalidation"):
        check_outputs(sources, fragments, outputs)


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Windows chmod only toggles the read-only bit, so the 0o644 mode contract is POSIX-only",
)
def test_write_outputs_preserves_existing_output_permissions(tmp_path: Path) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (fragments / "shared.md").write_bytes(b"new\n")
    (sources / "command.md").write_bytes(_directive("shared.md"))
    output = outputs / "command.md"
    output.write_bytes(b"old\n")
    output.chmod(0o644)

    write_outputs(sources, fragments, outputs)

    assert stat.S_IMODE(output.stat().st_mode) == 0o644


def test_check_outputs_ignores_gitkeep_and_unmanaged_templates(tmp_path: Path) -> None:
    sources, fragments, outputs = _roots(tmp_path)
    (sources / ".gitkeep").write_bytes(b"")
    (fragments / ".gitkeep").write_bytes(b"")
    unmanaged = outputs / "unmanaged.md"
    unmanaged.write_bytes(b"complete\n")

    check_outputs(sources, fragments, outputs)

    assert unmanaged.read_bytes() == b"complete\n"


def test_repository_check_is_read_only_with_empty_opt_in_scaffold() -> None:
    commands = ROOT / "templates" / "commands"
    before = {path.name: path.read_bytes() for path in commands.glob("*.md")}

    result = main(["--check", "--root", str(ROOT)])

    after = {path.name: path.read_bytes() for path in commands.glob("*.md")}
    assert result == 0
    assert after == before


def test_cli_reports_fragment_errors_with_nonzero_status(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    sources = tmp_path / "internal" / "command_templates" / "sources"
    fragments = tmp_path / "internal" / "command_templates" / "fragments"
    outputs = tmp_path / "templates" / "commands"
    sources.mkdir(parents=True)
    fragments.mkdir(parents=True)
    outputs.mkdir(parents=True)
    (sources / "broken.md").write_bytes(_directive("missing.md"))

    result = main(["--check", "--root", str(tmp_path)])

    captured = capsys.readouterr()
    assert result == 1
    assert "broken.md" in captured.err
    assert "missing.md" in captured.err


def _self_bootstrap_fixture(tmp_path: Path) -> Path:
    root = tmp_path / "repository"
    templates = root / "templates" / "commands"
    templates.mkdir(parents=True)
    (root / "internal" / "command_templates" / "sources").mkdir(parents=True)
    (root / "internal" / "command_templates" / "fragments").mkdir(parents=True)
    (templates / "specify.md").write_text(
        "---\ndescription: Capture requirements\n---\n\nUse $ARGUMENTS then /codexspec:generate-spec.\n",
        encoding="utf-8",
    )
    (templates / "scripted.md").write_text(
        "---\ndescription: Run helper\nscripts:\n  sh: bash helper.sh\n  ps: pwsh helper.ps1\n---\n\nRun `{SCRIPT}`.\n",
        encoding="utf-8",
    )
    with patch("codexspec.integrations.codex.sys.platform", "linux"):
        ClaudeIntegration().install(root, templates, force=True, language="en")
        CodexIntegration().install_skills(root, templates, force=True, language="en")
    for artifact in (root / ".claude" / "commands" / "codexspec").glob("*.md"):
        artifact.write_bytes(artifact.read_bytes().replace(b"\r\n", b"\n"))
    for artifact in (root / ".agents" / "skills").glob("codexspec-*/SKILL.md"):
        artifact.write_bytes(artifact.read_bytes().replace(b"\r\n", b"\n"))
    return root


def test_self_bootstrap_check_accepts_expected_claude_and_codex_artifacts(tmp_path: Path) -> None:
    root = _self_bootstrap_fixture(tmp_path)

    check_self_bootstrap(root, language="en")


def test_self_bootstrap_check_is_independent_of_ambient_platform(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("codexspec.integrations.codex.sys.platform", "win32")
    root = _self_bootstrap_fixture(tmp_path)

    check_self_bootstrap(root, language="en")


def test_self_bootstrap_check_allows_documented_non_template_claude_commands(tmp_path: Path) -> None:
    root = _self_bootstrap_fixture(tmp_path)
    commands = root / ".claude" / "commands" / "codexspec"
    (commands / "translate-docs.md").write_text("internal\n", encoding="utf-8")
    (commands / "check-i18n-semantics.md").write_text("internal\n", encoding="utf-8")
    (commands / "review-python-code.md").write_text("compatibility\n", encoding="utf-8")
    (commands / "review-react-code.md").write_text("compatibility\n", encoding="utf-8")

    check_self_bootstrap(root, language="en")

    (commands / "specify.md").unlink()
    with pytest.raises(FragmentError, match=r"Claude.*missing.*specify\.md"):
        check_self_bootstrap(root, language="en")


@pytest.mark.parametrize("defect", ["stale", "missing", "unexpected"])
def test_self_bootstrap_check_rejects_claude_artifact_drift(tmp_path: Path, defect: str) -> None:
    root = _self_bootstrap_fixture(tmp_path)
    commands = root / ".claude" / "commands" / "codexspec"
    if defect == "stale":
        (commands / "specify.md").write_text("stale\n", encoding="utf-8")
    elif defect == "missing":
        (commands / "specify.md").unlink()
    else:
        (commands / "unexpected.md").write_text("unexpected\n", encoding="utf-8")

    with pytest.raises(FragmentError, match=rf"Claude.*{defect}"):
        check_self_bootstrap(root, language="en")


@pytest.mark.parametrize("defect", ["stale", "missing", "unexpected"])
def test_self_bootstrap_check_rejects_codex_artifact_drift(tmp_path: Path, defect: str) -> None:
    root = _self_bootstrap_fixture(tmp_path)
    skills = root / ".agents" / "skills"
    skill = skills / "codexspec-specify" / "SKILL.md"
    if defect == "stale":
        skill.write_text("stale\n", encoding="utf-8")
    elif defect == "missing":
        skill.unlink()
    else:
        unexpected = skills / "codexspec-unexpected"
        unexpected.mkdir()
        (unexpected / "SKILL.md").write_text("unexpected\n", encoding="utf-8")

    with pytest.raises(FragmentError, match=rf"Codex.*{defect}"):
        check_self_bootstrap(root, language="en")


@pytest.mark.parametrize("channel", ["claude", "codex"])
def test_self_bootstrap_check_rejects_crlf_only_byte_drift(tmp_path: Path, channel: str) -> None:
    root = _self_bootstrap_fixture(tmp_path)
    if channel == "claude":
        artifact = root / ".claude" / "commands" / "codexspec" / "specify.md"
        expected_error = "Claude.*stale"
    else:
        artifact = root / ".agents" / "skills" / "codexspec-specify" / "SKILL.md"
        expected_error = "Codex.*stale"
    artifact.write_bytes(artifact.read_bytes().replace(b"\n", b"\r\n"))

    with pytest.raises(FragmentError, match=expected_error):
        check_self_bootstrap(root, language="en")


@pytest.mark.parametrize("channel", ["claude", "codex"])
def test_self_bootstrap_check_rejects_symlinked_artifacts(tmp_path: Path, channel: str) -> None:
    if not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    root = _self_bootstrap_fixture(tmp_path)
    if channel == "claude":
        artifact = root / ".claude" / "commands" / "codexspec" / "specify.md"
    else:
        artifact = root / ".agents" / "skills" / "codexspec-specify" / "SKILL.md"
    outside = tmp_path / f"outside-{channel}.md"
    outside.write_bytes(artifact.read_bytes())
    artifact.unlink()
    try:
        artifact.symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symlink creation is unavailable: {exc}")

    with pytest.raises(FragmentError, match=r"symbolic link"):
        check_self_bootstrap(root, language="en")


def test_self_bootstrap_check_rejects_unsafe_claude_artifact_alias(tmp_path: Path) -> None:
    root = _self_bootstrap_fixture(tmp_path)
    artifact = root / ".claude" / "commands" / "codexspec" / "UNEXPECTED.MD"
    artifact.write_text("unexpected\n", encoding="utf-8")

    with pytest.raises(FragmentError, match=r"unsafe Claude artifact name"):
        check_self_bootstrap(root, language="en")


def test_self_bootstrap_check_rejects_non_regular_claude_artifact_before_open(tmp_path: Path) -> None:
    if not hasattr(os, "mkfifo"):
        pytest.skip("FIFOs are unavailable")
    root = _self_bootstrap_fixture(tmp_path)
    fifo = root / ".claude" / "commands" / "codexspec" / "fifo.md"
    os.mkfifo(fifo)

    with pytest.raises(FragmentError, match=r"Claude artifact fifo\.md.*not a regular file"):
        check_self_bootstrap(root, language="en")


@pytest.mark.skipif(
    sys.platform == "win32",
    reason="Windows strips the trailing dot, so the codexspec-alias. fixture cannot be created as named",
)
def test_self_bootstrap_check_rejects_unsafe_codex_artifact_alias(tmp_path: Path) -> None:
    root = _self_bootstrap_fixture(tmp_path)
    artifact = root / ".agents" / "skills" / "codexspec-alias."
    artifact.mkdir()
    (artifact / "SKILL.md").write_text("unexpected\n", encoding="utf-8")

    with pytest.raises(FragmentError, match=r"unsafe Codex artifact name"):
        check_self_bootstrap(root, language="en")


def test_self_bootstrap_check_rejects_non_directory_codex_artifact(tmp_path: Path) -> None:
    root = _self_bootstrap_fixture(tmp_path)
    artifact = root / ".agents" / "skills" / "codexspec-alias"
    artifact.write_text("unexpected\n", encoding="utf-8")

    with pytest.raises(FragmentError, match=r"Codex artifact codexspec-alias.*not a directory"):
        check_self_bootstrap(root, language="en")


@pytest.mark.parametrize("entry_kind", ["file", "directory", "symlink", "fifo"])
def test_self_bootstrap_check_rejects_extra_entries_inside_codex_artifacts(
    tmp_path: Path,
    entry_kind: str,
) -> None:
    if entry_kind == "symlink" and not hasattr(os, "symlink"):
        pytest.skip("symlinks are unavailable")
    if entry_kind == "fifo" and not hasattr(os, "mkfifo"):
        pytest.skip("FIFOs are unavailable")
    root = _self_bootstrap_fixture(tmp_path)
    skill = root / ".agents" / "skills" / "codexspec-specify"
    entry = skill / "extra.md"
    if entry_kind == "file":
        entry.write_text("unexpected\n", encoding="utf-8")
    elif entry_kind == "directory":
        entry.mkdir()
    elif entry_kind == "symlink":
        target = tmp_path / "outside-extra.md"
        target.write_text("unexpected\n", encoding="utf-8")
        try:
            entry.symlink_to(target)
        except OSError as exc:
            pytest.skip(f"symlink creation is unavailable: {exc}")
    else:
        os.mkfifo(entry)

    with pytest.raises(FragmentError, match=r"Codex artifact codexspec-specify/extra\.md.*(?:unexpected|symbolic)"):
        check_self_bootstrap(root, language="en")


@pytest.mark.parametrize("channel", ["claude", "codex"])
def test_self_bootstrap_check_rejects_artifact_content_changed_after_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    channel: str,
) -> None:
    root = _self_bootstrap_fixture(tmp_path)
    if channel == "claude":
        artifact = root / ".claude" / "commands" / "codexspec" / "specify.md"
        expected = r"Claude artifact specify\.md.*changed during operation"
    else:
        artifact = root / ".agents" / "skills" / "codexspec-specify" / "SKILL.md"
        expected = r"Codex artifact codexspec-specify/SKILL\.md.*changed during operation"
    real_read = command_template_fragments._read_stable_file_snapshot

    def read_then_change(
        path: Path,
        read_root: Path,
        display: str,
    ) -> tuple[bytes, command_template_fragments.StatSignature]:
        snapshot = real_read(path, read_root, display)
        if path == artifact:
            artifact.write_bytes(b"changed\n")
        return snapshot

    monkeypatch.setattr(command_template_fragments, "_read_stable_file_snapshot", read_then_change)

    with pytest.raises(FragmentError, match=expected):
        check_self_bootstrap(root, language="en")


def test_self_bootstrap_check_rejects_templates_changed_during_generation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = _self_bootstrap_fixture(tmp_path)
    template = root / "templates" / "commands" / "specify.md"
    real_install = CodexIntegration.install_skills

    def install_then_change(self: CodexIntegration, *args: object, **kwargs: object) -> object:
        result = real_install(self, *args, **kwargs)
        template.write_bytes(b"changed\n")
        return result

    monkeypatch.setattr(CodexIntegration, "install_skills", install_then_change)

    with pytest.raises(FragmentError, match=r"distributed command templates changed during operation"):
        check_self_bootstrap(root, language="en")


def test_repository_self_bootstrap_artifacts_match_existing_generators() -> None:
    check_self_bootstrap(ROOT, language=command_template_fragments._interaction_language(ROOT))


def test_cli_distribution_check_combines_fragment_and_self_bootstrap_preflight(tmp_path: Path) -> None:
    root = _self_bootstrap_fixture(tmp_path)

    assert main(["--check-distribution", "--root", str(root)]) == 0

    (root / ".claude" / "commands" / "codexspec" / "specify.md").write_text("stale\n", encoding="utf-8")
    assert main(["--check-distribution", "--root", str(root)]) == 1
