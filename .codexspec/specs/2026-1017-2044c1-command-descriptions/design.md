# Design: Command Descriptions

**Related Spec**: [spec.md](spec.md)
**Confirmed Requirements**: [requirements.md](requirements.md)
**Status**: Ready for planning

## Context

Revise descriptive metadata using the existing authoring, translation and
installation paths. No new runtime component, schema, API or dependency is needed.

## Architecture & Components

### C1: Evidence and authored descriptions

Covers: REQ-001, REQ-002, REQ-004, NFR-001.

Read all 28 current command sources and necessary referenced resources. Keep a
per-command evidence table in this feature directory. Author English description
scalars in internal/command_templates/sources/*.md using the exact approved
compact English text in description-proposals.md. Use the exact approved Chinese
text in the catalog; leave command bodies and argument hints intact.

### C2: Language catalogs and listing fallback

Covers: REQ-003, NFR-001.

Update only description values in the eight existing JSON catalogs (English and
seven localized languages). English matches source extraction exactly. Chinese
fallback strings in src/codexspec/commands/installer.py match zh-CN descriptions.
Keep the current lookup behavior; no metadata refactor is needed.

### C3: Complete distribution and installed host entries

Covers: REQ-003.

The existing fragment renderer produces templates/commands/*.md. Existing
installers produce tracked Claude commands and native Codex skills from those
complete templates and catalogs. Existing distribution checks verify generated
bytes. A temporary project exercises actual installation and listing behavior.

## Key Design Decisions

### D1: Keep existing metadata storage and generation

Covers: REQ-001, REQ-003.

Only text values change. A new centralized description registry would introduce
runtime and migration scope without improving the user's requested wording.
Accept existing duplication, synchronizing fallback strings with the catalog.

### D2: Separate semantic evidence from mechanical checks

Covers: REQ-002, NFR-001.

A feature-local inventory records current behavior evidence and editorial review.
Existing tests establish parsing, translation coverage and distribution fidelity;
they cannot establish that prose describes the right behavior. Review all locale
text for meaning rather than adding tests that merely pin new wording.

## Requirements Coverage

| Requirement | Design coverage |
| --- | --- |
| REQ-001 | C1, D1 |
| REQ-002 | C1, D2 |
| REQ-003 | C2, C3, D1 |
| REQ-004 | C1, C2 |
| NFR-001 | C1, C2, D2 |
