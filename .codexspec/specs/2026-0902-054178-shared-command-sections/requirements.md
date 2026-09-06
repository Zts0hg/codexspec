# Confirmed Requirements: shared-command-sections

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0902-054178`
**Status**: Confirmed
**Last Confirmed**: 2026-09-02

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Maintain shared command text in one place

- **Status**: confirmed
- **Statement**: Provide a generic maintainer-side fragment reuse mechanism so that one literal block of text can be maintained once and reused by any number of command templates.
- **Rationale**: Repeated manual copy-and-paste makes common command text harder to maintain consistently.
- **User Evidence**: The user wants common portions of multiple commands to be maintained centrally without changing command behavior.
- **Confirmed At**: 2026-09-02

### NEED-002: Prevent fragment copies from drifting

- **Status**: confirmed
- **Statement**: The project must reliably synchronize or validate every command location that references a shared fragment when that fragment changes.
- **Rationale**: Central maintenance is only effective when all resulting command content remains consistent.
- **User Evidence**: The user confirmed that project-level tests and CI should detect problems early.
- **Confirmed At**: 2026-09-02

## Constraints

### CON-001: Keep `codexspec init` unaware of fragments

- **Status**: confirmed
- **Statement**: `codexspec init` must remain unaware of the fragment mechanism. Its interface, workflow, error behavior, user experience, and observable effects must not change because of this feature.
- **User Evidence**: "codexspec init 应该无感知。"

### CON-002: Preserve generated command content byte for byte

- **Status**: confirmed
- **Statement**: For content maintained through the fragment mechanism, the complete command files consumed by existing distribution and initialization paths must remain byte-for-byte identical to the equivalent manually duplicated content.
- **User Evidence**: The user selected byte-for-byte compatibility rather than semantic compatibility alone.

### CON-003: Detect fragment defects before distribution

- **Status**: confirmed
- **Statement**: Normal project tests/CI and the packaging or release process must both act as mandatory gates. Missing fragments, forbidden nesting, stale synchronized content, or other fragment integrity failures must be detected before a user can receive the affected distribution; user invocation of `codexspec init` must never be the first detection point.
- **User Evidence**: "我不允许用户使用安装命令的时候才报错。"

## Decisions

### DEC-001: Use a generic mechanism

- **Status**: confirmed
- **Decision**: The fragment mechanism must work generically for arbitrary command templates and fragments; it must not hard-code particular commands or section names.
- **Alternatives Rejected**: A mechanism limited to a fixed set of known common sections.
- **Reason**: Future common text should be reusable without extending mechanism-specific code for every section.
- **User Evidence**: The user chose a general-purpose fragment mechanism.

### DEC-002: Support literal fragments only in the first version

- **Status**: confirmed
- **Decision**: A fragment is inserted as literal text and accepts no parameters.
- **Alternatives Rejected**: Parameterized fragments with command-specific variables.
- **Reason**: Literal reuse keeps the first version simple and supports exact output preservation.
- **User Evidence**: The user selected literal fragments only.

### DEC-003: Disallow nested fragments in the first version

- **Status**: confirmed
- **Decision**: Command sources may reference fragments, but fragments must not reference other fragments.
- **Alternatives Rejected**: Nested fragment composition with recursive expansion and cycle detection.
- **Reason**: A single reference level avoids recursive resolution and cyclic dependencies.
- **User Evidence**: The user selected no nesting for the first version.

## Out of Scope

### OUT-001: Selecting or extracting common command content

- **Status**: confirmed
- **Statement**: This feature does not decide which command content should become a fragment and does not perform the user's content extraction work.
- **Reason**: The user will select and extract the desired common portions separately.
- **User Evidence**: "提取我来提取，你不要考虑提取的事情。"

### OUT-002: User-side fragment parsing

- **Status**: confirmed
- **Statement**: Parsing, expanding, or validating fragment references during `codexspec init` or command execution is excluded.
- **Reason**: The mechanism is solely an internal project-maintenance concern and must not affect users.
- **User Evidence**: The user repeatedly required `codexspec init` to be unaware of the mechanism.

## Open Questions

None.

## Design-Stage Freedom

The source layout, synchronization tool shape, and version-control treatment of derived files are intentionally deferred to design. Any design choice must satisfy every confirmed need, constraint, decision, and exclusion above.

## Confirmation Log

### Session 2026-09-02

- **Summary Presented**: A generic, maintainer-only, literal, non-nested fragment mechanism with byte-identical command output, two pre-distribution validation gates, no `codexspec init` awareness, and no responsibility for selecting or extracting content.
- **User Confirmation**: "确认"
- **Entries Confirmed**: NEED-001, NEED-002, CON-001, CON-002, CON-003, DEC-001, DEC-002, DEC-003, OUT-001, OUT-002
