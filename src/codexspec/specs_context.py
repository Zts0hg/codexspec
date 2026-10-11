"""Task-dependent historical-spec recall instructions for both agent integrations."""

import re
from pathlib import Path

START = "<!-- CODEXSPEC SPECS START -->"
END = "<!-- CODEXSPEC SPECS END -->"


_GUIDANCE = """## CodexSpec Historical Specs

Before substantive requirements, behavior, design, implementation, debugging, or
review judgments, actively recall relevant history under `.codexspec/specs/`.
This applies in ordinary conversation and SDD workflows. Prepare background before
questioning the user. Purely mechanical edits, such as spelling or formatting
with no substantive judgment, may omit recall.

Select related features by the task's capabilities, affected modules, interfaces,
and terminology; use directory names, artifact headings, and targeted text search
to find candidates. Read relevant requirements and follow earlier and later
additions, changes, and references. Do not stop at the first matching document or
load every historical artifact. Use feature-directory timestamps to reconstruct
the iteration timeline, together with explicit confirmation and replacement
records, including later revisions inside an older feature directory.

Confirmed content in each `requirements.md` is an authoritative user decision
record. Older unchanged requirements remain applicable; an unrelated later feature
does not replace them. Combine later additions with earlier requirements. A later
explicit change updates the same matter while retaining the earlier rationale
and unrelated requirements. Open proposals are not confirmed decisions. When a
relationship is unclear, explain the specific difference and ask a concise
question; do not assume an earlier requirement expired.

The user's latest explicit decision in the current interaction takes precedence
over historical specs: history must never override or replace it. Explain relevant
changes and implications. Do not ask again about the same explicit decision merely
because history differs. Use the owning requirements workflow to reflect changed
requirements before downstream artifacts rely on them, without repeating an
already answered question. Historical background must not silently rewrite current
requirements or broaden the selected target, permissions, or staged-only inputs.

Read to the depth needed for the scenario:

- Requirements discussion (including specify, quick, blueprint): reconstruct the
  requirements timeline; read design rationale when needed to explain a trade-off.
  Prepare known background, applicable requirements, and differences to confirm.
- Design and planning: use confirmed requirements plus relevant historical designs,
  alternatives, and trade-offs; consult plans when implementation experience matters.
- Implementation and debugging: establish expected behavior and its successive
  changes, then examine relevant design, code and tests; plans alone do not prove implementation.
- Code review: trace concrete changes and concerns to relevant requirements and
  designs, checking current requirements, compatibility, and repeated problems.

Reuse applicable established information instead of asking the user to reconstruct
it. If continued applicability needs confirmation, present the known background
and a short targeted question. If history is missing or incomplete, distinguish
what is known from what remains uncertain; never invent decisions or confirmation.
For legacy artifacts without requirements, use available evidence and disclose
that original user confirmation cannot be established from those artifacts alone.

Stop expanding retrieval when relevant requirements, decision evolution, and
applicability support the current judgment. Do not expand into unrelated history;
ask about any remaining material ambiguity instead of silently choosing an answer.
Reuse prepared background across workflow stages and duplicate entry points.
Supplement retrieval when scope changes, new evidence appears, or the background
is insufficient for the judgment required. Reuse never makes incomplete evidence
sufficient. Keep relevant source paths and decision relationships with the prepared
background so later stages can reuse it without reconstructing the entire history."""


def render_specs_context() -> str:
    """Return constant-size guidance; historical artifacts are read by the agent on demand."""
    return "\n".join((START, _GUIDANCE, END))


def inject_specs_context(path: Path) -> None:
    """Update only the bounded block, retaining surrounding UTF-8 text verbatim."""
    block = render_specs_context()
    existing = path.read_bytes().decode("utf-8") if path.exists() else ""
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if pattern.search(existing):
        updated = pattern.sub(lambda _match: block, existing)
    else:
        separator = "" if not existing else "\n" if existing.endswith("\n") else "\n\n"
        updated = existing + separator + block + "\n"
    path.write_bytes(updated.encode("utf-8"))
