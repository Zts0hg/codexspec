# Design Document: Shared Command Sections

<!--
Language: Generate this document in the language specified in .codexspec/config.yml
If not configured, use English.

This is the design stage between spec.md and plan.md. It describes WHAT the system is
(architecture, components, interfaces, key design decisions) — NOT how to build it in
phases (that belongs in plan.md).
-->

**Related Spec**: `.codexspec/specs/2026-0902-054178-shared-command-sections/spec.md`
**Confirmed Requirements**: `.codexspec/specs/2026-0902-054178-shared-command-sections/requirements.md`
**Created**: 2026-09-02
**Status**: Draft

## Context

Distributed command templates currently live as complete Markdown files under `templates/commands/`. The installer copies those files and optionally translates frontmatter; Codex skill generation likewise consumes the complete templates. Packaging includes `templates/` directly, while maintainer-only tooling under `internal/` is excluded from wheel and sdist contents.

The fragment mechanism therefore sits entirely before the existing distribution boundary. Only commands that a maintainer explicitly opts into fragment management gain an internal source file. A maintainer renderer turns those sources into the same complete `templates/commands/*.md` files that the current installer, Codex integration, plugin self-bootstrap workflow, and package build already consume. This feature does not select or extract any shared command content.

## Architecture & Components

### Maintainer command-source store

- **Responsibility**: Hold source versions of only those distributed commands that maintainers explicitly opt into fragment reuse. A source has the same basename as its complete output under `templates/commands/` and may contain standalone literal-fragment directives.
- **Interface**: Maintainer-only files under `internal/command_templates/sources/*.md`. The presence of a source file declares its matching `templates/commands/<name>.md` to be generated rather than hand-maintained. Commands without a matching internal source remain unchanged and continue to be maintained directly in `templates/commands/`.
- **Covers**: REQ-001, REQ-004, NFR-002

### Literal fragment store

- **Responsibility**: Hold centrally maintained raw byte sequences for reuse by opted-in command sources.
- **Interface**: Maintainer-only files under `internal/command_templates/fragments/`. Fragment identifiers are safe relative paths within this directory. Fragment bytes are inserted without interpolation, parameter substitution, newline normalization, or text reformatting.
- **Covers**: REQ-001, REQ-002, NFR-001

### Fragment directive contract

- **Responsibility**: Provide a generic, parameterless reference from a command source to a fragment without embedding command or section knowledge in the renderer.
- **Interface**: The ASCII form `<!-- CODEXSPEC:INCLUDE <relative-fragment-path> -->`, occupying a complete source line, names exactly one fragment beneath the fragment root. The renderer replaces the directive line, including its LF or CRLF line terminator when present, with the fragment's raw bytes. Inline examples remain literal bytes, while a standalone comment in the reserved `CODEXSPEC` namespace that does not match exactly—including indentation, case, or misspelling variants—is rejected as malformed. Directives are valid only in command sources; any matching or malformed reserved directive line in any fragment, including an unused fragment, is rejected as forbidden nesting or malformed content. Empty paths, POSIX or Windows absolute/drive-qualified paths, `.` or `..` segments, backslash traversal, non-UTF-8 names, Windows forbidden characters/stream/device-name aliases, Unicode-normalized or case-colliding names, symlinked sources/fragments/outputs, and any resolved path outside the fragment root are invalid.
- **Covers**: REQ-001, REQ-002, REQ-003, REQ-005

### Maintainer renderer and verifier

- **Responsibility**: Render opted-in command sources deterministically and either synchronize or verify their complete distribution templates.
- **Interface**: A maintainer-only Python entry point under `internal/` exposes two explicit modes:
  - write mode prevalidates every source, fragment, and output identity, rejects portable-name collisions with the complete output namespace, revalidates source/fragment state before mutation, then atomically updates only its matching `templates/commands/<name>.md` output while preserving existing file permissions;
  - check mode performs no writes and fails when a source or fragment is invalid, nesting is present, a referenced fragment is missing or unsafe, a matching output is absent, or rendered bytes differ from tracked output bytes.
  Both modes operate on bytes. Their core renderer is callable from tests with temporary roots so error cases do not depend on real project fragments.
- **Covers**: REQ-003, REQ-004, REQ-005, NFR-001

### Project validation gate

- **Responsibility**: Detect fragment integrity and synchronization failures during normal local testing and the existing cross-platform CI test workflow.
- **Interface**: Automated tests exercise valid rendering and each required failure class, then run check mode against the repository. CI path filters include the maintainer source/fragment/tool paths so fragment-only changes trigger validation.
- **Covers**: REQ-004, REQ-005, NFR-003

### Distribution gate

- **Responsibility**: Independently prevent stale or unresolved fragment state from entering official packages or plugin-facing generated artifacts.
- **Interface**: The CI package-build job and `publish.sh` invoke check mode before building. Post-build package tests compare every packaged distributed command byte-for-byte with its complete tracked `templates/commands/` file and reject valid or malformed standalone fragment directives in packaged commands. A maintainer-side distribution check also uses the existing Claude installer and Codex skill generator against a temporary directory, fixes their expected snapshot semantics to the repository's canonical POSIX rendering regardless of the CI host, then byte-compares those expected artifacts with the tracked `.claude/commands/codexspec/` and `.agents/skills/` self-bootstrap artifacts; maintainer-only commands are excluded from that comparison. The existing generators continue to consume only complete tracked templates and receive no fragment logic.
- **Covers**: REQ-006, NFR-001, NFR-003

### Existing command consumers

- **Responsibility**: Continue copying, translating, or converting complete `templates/commands/*.md` files exactly as they do today.
- **Interface**: `install_commands_to_subdir`, `update_installed_command_frontmatter`, and the Codex integration receive no fragment API and contain no fragment parsing or validation code.
- **Covers**: REQ-007, NFR-002, NFR-003

### Maintainer guidance

- **Responsibility**: Make the two source-of-truth cases explicit: an opted-in command is edited through its internal source and rendered output, while a command without a same-named internal source remains directly editable under `templates/commands/`.
- **Interface**: The project constitution, `CLAUDE.md`, and repository-layout guidance describe the exception without changing downstream user documentation or presenting fragments as a user feature.
- **Covers**: REQ-004, REQ-007, NFR-002

## Key Design Decisions

### Decision 1: Keep complete tracked templates as the distribution boundary

- **Context**: Existing initialization, Codex integration, packaging, and plugin flows already consume complete files from `templates/commands/`. Making any of those consumers expand fragments would violate the confirmed boundary.
- **Decision**: Fragment-aware sources and fragments live in maintainer-only `internal/` paths. The renderer writes complete, tracked outputs to the existing `templates/commands/` paths, and all existing consumers remain fragment-unaware.
- **Alternatives**: Expand fragments in `codexspec init`; ship unresolved sources and expand during command execution; make packaging create an untracked temporary template tree.
- **Trade-offs**: Participating commands have a tracked generated output in addition to their maintainer source, but exact output is directly reviewable and all existing consumer paths remain unchanged.
- **Covers**: REQ-007, NFR-001, NFR-002, NFR-003

### Decision 2: Allow incremental opt-in by command

- **Context**: The user will decide which content to extract, and this feature must not make that selection or perform the extraction.
- **Decision**: Only a command with a same-named internal source participates in fragment rendering. The mechanism neither creates sources for all commands nor chooses any initial shared fragment.
- **Alternatives**: Duplicate every existing command into a new source tree as part of this feature; require every command to use the fragment renderer immediately.
- **Trade-offs**: The repository temporarily has two clearly documented authoring paths, but no command is migrated without the user's explicit extraction work and adoption can proceed incrementally.
- **Covers**: REQ-001, REQ-004

### Decision 3: Define replacement over raw bytes

- **Context**: Text-mode reading and writing can normalize newlines across operating systems, while the confirmed compatibility rule is byte-for-byte equality.
- **Decision**: The renderer reads fragments and sources as bytes, recognizes a narrowly defined ASCII directive line, substitutes raw fragment bytes, and writes or compares bytes without normalization. Candidate classification is line-oriented so malformed reserved lines cannot leak while inline examples remain ordinary content.
- **Alternatives**: Parse Markdown as text; use a general template engine; promise only semantic equivalence.
- **Trade-offs**: The directive grammar is intentionally small and fragments own all whitespace surrounding the inserted content, but output equality is deterministic on every supported platform.
- **Covers**: REQ-002, REQ-003, NFR-001

### Decision 4: Separate synchronization from validation

- **Context**: Maintainers need an intentional way to update complete templates, while CI and release paths must never repair a stale tree silently.
- **Decision**: Write mode is an explicit maintainer action; check mode is read-only and is the only mode used by tests, CI, packaging, and release gates.
- **Alternatives**: Auto-rewrite during tests or builds; validate only after package creation.
- **Trade-offs**: Maintainers must run one synchronization command after changing a source or fragment, but automated gates remain deterministic and never hide uncommitted generated changes.
- **Covers**: REQ-004, REQ-005, REQ-006

### Decision 5: Validate official package contents independently

- **Context**: A source/output check alone does not prove that wheel and sdist artifacts contain the intended complete files.
- **Decision**: Package-content tests enumerate exact, flat distributed command-template member paths in built archives, compare them with the tracked complete templates, and reject duplicates, aliases, nested members, or any unresolved directive marker. Before release, temporary outputs from the existing Claude and Codex generators are also compared with tracked self-bootstrap artifacts so the plugin-facing command tree cannot remain stale. Explicitly documented maintainer-only commands and the two pre-existing plugin-only review-command compatibility artifacts remain outside template-derived comparison and are preserved unchanged.
- **Alternatives**: Trust Hatch's existing force-include mapping without inspecting archives; rely only on unit tests.
- **Trade-offs**: The build job performs an additional archive scan, providing a distinct distribution gate with negligible cost for the current template set.
- **Covers**: REQ-006, NFR-001, NFR-003

## Interface Contracts

### Source-to-output mapping

- Each regular Markdown file `internal/command_templates/sources/<command-name>.md` maps to exactly `templates/commands/<command-name>.md`, matching the current flat command-template contract.
- Source, fragment, and output names must use their exact stored spelling, lowercase `.md` extension, and a portable, collision-free basename or relative path; aliases and entries outside the flat output namespace are invalid.
- Outputs with no corresponding internal source remain outside renderer ownership.
- **Covers**: REQ-001, REQ-004, REQ-005

### Check-mode result

- Success means every opted-in source resolved without nesting or unsafe paths and its rendered bytes equal its tracked complete output.
- Failure is non-mutating and identifies the source plus the failing fragment reference or mismatched output.
- Multiple references to the same literal fragment and references from multiple command sources are valid.
- **Covers**: REQ-001, REQ-003, REQ-004, REQ-005

### Write-mode result

- A fully validated render set is prepared before any output replacement begins.
- Only outputs mapped from opted-in sources are eligible for replacement.
- Each changed output is replaced atomically with its rendered bytes; unrelated complete templates are untouched.
- **Covers**: REQ-004, NFR-001

## Sequence & Data Flow

1. A maintainer explicitly opts a command into the internal source tree and, separately from this feature, chooses and extracts any desired common text into fragments.
2. Write mode validates all opted-in sources and fragments, renders raw bytes, and synchronizes the matching complete `templates/commands/` outputs.
3. Normal tests and CI run read-only check mode and reject invalid or stale state.
4. The official package/release path runs read-only check mode again, verifies tracked Claude and Codex self-bootstrap artifacts against temporary outputs from the existing generators, builds archives from the complete `templates/commands/`, and verifies the archived bytes.
5. `codexspec init`, Codex skill generation, and plugin self-bootstrap consume the same complete templates through their existing logic, with no fragment awareness.

## Risks & Trade-offs

| Risk | Impact | Mitigation |
|------|--------|------------|
| A maintainer edits a generated complete template instead of its opted-in source | Check mode reports byte drift and CI rejects the change | Document the per-file ownership rule and include the source path in mismatch diagnostics |
| A fragment-only change does not trigger CI because `internal/` is absent from current path filters | Stale output could pass pull-request automation | Extend CI path filters for the exact maintainer fragment paths |
| Platform newline conversion changes rendered files or expected self-bootstrap snapshots | Byte-compatibility failures across macOS, Linux, or Windows | Use byte-based rendering, canonical expected-generator semantics, raw-byte artifact comparison, and cross-platform tests |
| Filesystem aliases, portable-name collisions, or symlinks bypass source/output ownership | External bytes are read or generated outputs mutate unintended targets | Compare physical paths consistently, reject portable aliases and symlink components, bind reads to stable content/metadata signatures, revalidate source state, and prevalidate the complete output namespace before writing |
| Official archives omit, alias, nest, duplicate, or alter complete templates | Users receive content not represented by reviewed outputs | Enumerate exact flat archive member paths and byte-compare all packaged command templates after build |
| Plugin-facing self-bootstrap artifacts remain stale after a complete template changes | Marketplace users receive older command content than package users | Compare tracked distributed Claude/Codex artifacts with temporary outputs from the existing generators before release |

## Requirements Coverage

| Spec Requirement | Design Coverage |
|------------------|-----------------|
| REQ-001 | Maintainer command-source store; literal fragment store; directive contract; incremental opt-in decision |
| REQ-002 | Literal fragment store; directive contract; raw-byte replacement decision |
| REQ-003 | Directive contract; renderer/verifier; raw-byte replacement decision; check-mode contract |
| REQ-004 | Source store; renderer/verifier; project gate; guidance; incremental opt-in and synchronization decisions |
| REQ-005 | Directive contract; renderer/verifier; project gate; source mapping and check-mode contracts |
| REQ-006 | Distribution gate; synchronization/validation separation; independent package validation decision |
| REQ-007 | Existing command consumers; guidance; complete-template distribution decision |
| NFR-001 | Fragment store; renderer/verifier; distribution gate; raw-byte and package-validation decisions |
| NFR-002 | Source store; existing consumers; guidance; complete-template distribution decision |
| NFR-003 | Project gate; distribution gate; existing consumers; complete-template and package-validation decisions |
