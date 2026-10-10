# Confirmed Requirements: Rename the planning command to design-to-plan

**Feature ID**: `2026-1009-2352qc`
**Status**: Confirmed
**Last Confirmed**: 2026-10-09

## Authority Rules

Only entries with Status: confirmed bind downstream artifacts. Open items and AI
assumptions are not requirements. Superseded decisions retain their replacement link.

## Context

The design stage introduced by feature `2026-0812-2114vj-spec-to-design`
(requirements.md NEED-007 and DEC-004; spec.md REQ-008; commit e74ab41)
separated architecture and interface design from implementation planning. The
planning command consumes design.md but retains the name spec-to-plan. Its name
should express its current position in the spec → design → plan → tasks pipeline.
Those historical artifacts explain the existing behavior; they are not a request
to change the planning contract.

## Needs

### NEED-001: Rename the planning command

- **Status**: confirmed
- **Statement**: Rename the official spec-to-plan command to design-to-plan. Preserve
  its existing implementation-planning responsibilities and plan.md output.
- **User Evidence**: The final summary proposed “正式命令改为 design-to-plan，现有规划职责与产物保持不变”; the user answered “确认”.
- **Confirmed At**: 2026-10-09

### NEED-002: Synchronize command distribution and consumers

- **Status**: confirmed
- **Statement**: Synchronize automatic workflow advancement, auto-dev, installer
  registration, translations, current documentation, tests, and generated command
  and skill copies with the new name.
- **User Evidence**: The final summary proposed synchronizing automatic workflows,
  registration, translations, documentation, tests, and generated copies; the user
  answered “确认”.
- **Confirmed At**: 2026-10-09

## Constraints

The unchanged planning responsibilities and output are binding under NEED-001.
Repository governance additionally requires authoring opted-in command changes in
internal/command_templates/sources or fragments, regenerating distribution and
installation artifacts, and preserving the packaging boundary. These are existing
project rules, not additional user requirements.

## Decisions

### DEC-001: Remove the old command without a compatibility entry

- **Status**: confirmed
- **Decision**: Remove spec-to-plan. Do not retain an alias, forwarding command, or
  compatibility entry. The official workflow uses design-to-plan.
- **Alternatives Rejected**: Retaining spec-to-plan as a compatibility entry.
- **User Evidence**: “OPEN-001 旧名移除，不要考虑兼容入口”; the final summary explicitly
  said no alias, forwarding, or compatibility entry, and the user answered “确认”.
- **Confirmed At**: 2026-10-09

## Out of Scope

Compatibility command entries are excluded by DEC-001. Changes to planning
responsibilities or output are excluded by NEED-001.

## Open Questions

None. OPEN-001 (retain or remove the old command) is resolved by DEC-001.

## Confirmation Log

### Session 2026-10-09

- **Summary Presented**: Rename spec-to-plan to design-to-plan, preserve planning
  responsibilities/output, synchronize all active consumers and distribution
  surfaces, and remove the old command without a compatibility entry.
- **User Confirmation**: “确认”.
- **Entries Confirmed**: NEED-001, NEED-002, DEC-001.
- **Open IDs**: None; no unresolved question blocks specification generation.
