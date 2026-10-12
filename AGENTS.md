# AGENTS.md

<!-- CODEXSPEC START -->
## CodexSpec

This project uses CodexSpec for requirements-first spec-driven development.

Use these Codex skills when working on CodexSpec workflows:

- `$codexspec:constitution` to create or update project principles.
- `$codexspec:specify` to capture confirmed requirements.
- `$codexspec:blueprint` to discuss and maintain confirmed requirements in the shared blueprint.
- `$codexspec:generate-spec` to produce `spec.md`.
- `$codexspec:spec-to-design` to produce `design.md`.
- `$codexspec:design-to-plan` to produce `plan.md`.
- `$codexspec:plan-to-tasks` to produce `tasks.md`.
- `$codexspec:implement-tasks` to implement approved tasks.
- `$codexspec:auto-dev` to develop pending blueprint requirements autonomously in document order.
- `$codexspec:distill` to capture reusable cross-feature knowledge into `.codexspec/profile/`.
- `$codexspec:evolve` to contribute vetted profile knowledge back upstream via a reviewed PR.

Before making workflow decisions, read `.codexspec/memory/constitution.md`.
<!-- CODEXSPEC END -->

## Maintainer Guide (developing CodexSpec itself)

This section is hand-authored (outside the managed block above) and applies whether you use Codex or Claude Code — the two context files are equal-status entry points.

The full maintainer development guide lives in **`CLAUDE.md`**: architecture and per-feature design notes, the self-bootstrap rule (edit `templates/` and `src/codexspec/`, never the derived `.claude/commands/` or `.agents/skills/`), and the two-constitutions distinction. It imports the project constitution (`.codexspec/memory/constitution.md`) and the repository layout / packaging boundary (`docs/internal/repository-layout.md`).

Read `CLAUDE.md` and `docs/internal/repository-layout.md` before changing templates, packaging, or `init` behavior.

<!-- CODEXSPEC PROFILE START -->
## CodexSpec Project Profile

**Project constraints (highest priority — read these FIRST):** before any non-trivial work you MUST read every record under `.codexspec/profile/constraints/` — the project's hard prohibitions (严禁 / 仅允许). Honor them before anything else.

**Actively recall relevant knowledge before non-trivial work.** Do not wait to stumble on it: scan the record headings and their `scope/when` (and, for strategies, `trigger`) lines across the categories below, and read every record whose condition matches the task you are about to start (each directory holds one record per file):

- `.codexspec/profile/conventions/` — cross-feature conventions / steering; read before adopting a pattern, structure, or naming choice.
- `.codexspec/profile/pitfalls/` — known traps and their workarounds; read before implementing or debugging in an area that may have bitten before.
- `.codexspec/profile/decisions/` — past cross-feature / architectural decisions; read before deciding in the same area, to reuse prior rationale rather than re-litigate it.
- `.codexspec/profile/strategies/` — metacognitive trigger→action rules (and `scope: self` notes on the agent's own recurring slips); read before choosing an approach or when a fix is not converging.
- `.codexspec/profile/runbooks/` — ordered multi-step procedures with failure recovery; read before carrying out a known multi-step task.

Read the full record — each carries a `status` of `candidate` or `vetted`; weight `candidate` items with appropriate caution. A directory may be empty until `/codexspec:distill` has captured knowledge.

**Capture knowledge as you go.** When this session produces reusable cross-feature knowledge — even in plain chat or a non-SDD fix — run `/codexspec:distill` near that moment rather than only at wrap-up. It is non-blocking and early-exits when there is nothing new.
<!-- CODEXSPEC PROFILE END -->

<!-- CODEXSPEC COMMITS START -->
## Commit Messages

Before creating an authorized Git commit, invoke `$codexspec:commit-staged` to analyze staged
changes and generate the message. This applies in plain conversation and SDD
workflows, including auto-dev feature commits and blueprint commits. Command
availability alone is not an invocation.

The calling workflow prepares staging. `commit-staged` must not choose or stage
files, and must not describe unstaged changes or conversation-only intent. Use a
body when needed to cover material staged changes accurately and completely.

For helper-owned commits, prepare the helper's explicit index first, invoke
`$codexspec:commit-staged -p` against that index, and pass the full message and analyzed tree
to the helper's finalization action. Keep ownership, path, locking, and recovery
checks. If content changes, prepare and analyze again before committing; never
fall back to a fixed message or direct Git execution to bypass a failed check.
This rule does not grant authorization to stage, commit, or push.
<!-- CODEXSPEC COMMITS END -->

<!-- CODEXSPEC SPECS START -->
## CodexSpec Historical Specs

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
background so later stages can reuse it without reconstructing the entire history.
<!-- CODEXSPEC SPECS END -->
