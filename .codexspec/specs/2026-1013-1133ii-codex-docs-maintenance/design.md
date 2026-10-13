# Design: Codex Documentation Maintenance

## Context

Implement [spec.md](spec.md) within the confirmed maintainer-only scope. The
existing Claude maintenance files remain authoritative entry sources. Native
Codex entries are derived using the existing `CodexIntegration.render_skill`.
No public command registration, package allowlist or init behavior changes.

## Architecture and Components

### Shared maintenance instructions

`internal/references/doc-translation.md` holds repository-specific surface
selection, glossary/meaning preservation, navigation, translation, semantic
review and reporting rules. The two authored Claude entries select translator
or reviewer behavior and load this shared reference. Independent interaction
preferences and target-language content are distinguished.

Covers: REQ-001, REQ-002, REQ-003, NFR-001.

### Native entry rendering and repository checks

`internal/maintainer_doc_skills.py` renders the two named Claude entries into
`.agents/skills/codexspec-translate-docs/SKILL.md` and
`.agents/skills/codexspec-check-i18n-semantics/SKILL.md`. Explicit write mode
creates/updates only these derived files; check mode is read-only and rejects
missing/stale entries. Preflight forbids symlinked paths, non-regular files and
hard-linked outputs before any write. Reuse the existing Codex renderer to
convert argument references and invocation prefixes.

The existing `internal/command_template_fragments.py --check-distribution`
compares these expected maintainer entries, derived from the authored Claude
sources, alongside the unchanged distributed entries. Unknown extras remain
errors. Fixtures with no maintainer sources still verify their public set;
a present maintainer source requires its corresponding current Codex entry.
Maintainer guidance distinguishes authored Claude files from derived Codex
files and keeps both outside public installation.

Covers: REQ-001, REQ-005, NFR-001.

### Deterministic selection and Markdown verification

`internal/doc_translation.py` supplies read-only `inventory` and `verify`
operations. Inventory resolves explicit README mode or existing docs selection
into source/target pairs. It accepts the seven existing resource languages and
Chinese/Portuguese aliases appropriate to root/site paths; unsupported or
duplicate normalized targets and missing sources fail before translation.
Docs retain directory-relative mapping and timestamp-based incremental selection;
a full README synchronization selects every target rather than using timestamps
as semantic evidence. A dry run prints the inventory without writes.

Verification reads source/targets and checks preserved fenced examples, inline
technical tokens, heading hierarchy, table structure, local Markdown/HTML links,
anchors and language navigation. It reports errors without modifying documents.
These mechanics complement semantic review and never claim to prove meaning.
Path resolution rejects escaping source/target locations and redirected selected
files. Reports and translation writes use the selected feature workspace.

Covers: REQ-002, REQ-003, REQ-005, NFR-001.

### Seven-language translation execution and semantic assessment

The Codex translator reads the new native entry explicitly from this feature
workspace, obtains the README inventory, and writes each entire translation.
The English source's immutable examples, code spans, file references and brand
assets are preserved. Prose, headings and table text are translated naturally;
TOC links target the translated headings; language navigation marks its own
language and retains all eight root README destinations.

The Codex semantic reviewer then reads the new checker entry explicitly and
assesses all seven complete source/target pairs. It compares section intent,
conditions/defaults/order, exclusions, capability/command coverage, terminology,
notes and natural phrasing. `translation-review.md` records per-language evidence
and repaired findings; `verification.md` records actual deterministic commands
and the final repository checks. The English source hash is pinned to baseline.

Covers: REQ-003, REQ-004, REQ-005, NFR-001.

## Key Design Decisions

### Decision 1: Keep authored host entries and share maintained guidance

Retain the existing Claude-only authoring exception and derive Codex entries
rather than hand-editing generated skills. A small internal renderer and shared
reference avoid adding these tools to public templates or cloning lengthy rules.
Update the maintainer-only constitution/guide wording to reflect the confirmed
Codex extension; do not change downstream generic constitutions.

Covers: REQ-001, REQ-005, NFR-001.

### Decision 2: Explicit README mode alongside compatible site selection

Use `--readme` (or an explicit root README.md source) for root variants; default
site mode remains docs/en with seven localized docs directories. README Chinese
uses README.zh-CN.md while site Chinese uses docs/zh; Portuguese resources use
pt-BR and may accept pt as an alias. No language directory is inferred from the
13-language runtime configuration list.

Covers: REQ-002, REQ-003, REQ-005.

### Decision 3: Verify mechanics and meaning separately

A deterministic checker covers observable preservation/navigation invariants.
The semantic command covers propositions and readable native prose. The final
report requires both kinds of evidence; matching counts alone cannot close a
missing-content finding. The translator repairs problems before acceptance.

Covers: REQ-003, REQ-004, NFR-001.

## Risks and Trade-offs

- Host command discovery is checkout-local: explicit skill-file loading is
  required in this session; do not claim main automatically acquires new entries.
- Translated heading slugs differ: reconstruct target TOC/anchor links while
  retaining external URLs and source-linked local references.
- Internal tooling adds no user runtime dependencies. Existing Python/Codex
  rendering and Markdown dependencies are sufficient for maintainer checks.
- Full translations can reveal pre-existing localized drift. Use the complete
  current English source rather than patching old sections selectively.

## Coverage

| Requirement | Components / Decisions |
|-------------|-------------------------|
| REQ-001 | Shared instructions; entry rendering/checks; Decision 1 |
| REQ-002 | Shared instructions; selection/checker; Decision 2 |
| REQ-003 | Shared instructions; checker; execution; Decisions 2–3 |
| REQ-004 | Translation/semantic execution; Decision 3 |
| REQ-005 | Rendering/checks; selection; execution; Decisions 1–2 |
| NFR-001 | Shared instructions; rendering; checker; semantic evidence |
