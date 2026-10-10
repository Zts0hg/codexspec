# Design: Rename the planning command

## Context

Implement spec.md REQ-001 through REQ-004 without changing planning behavior.
The existing template renderer and integration installers remain the architecture.

## Architecture & Components

### C1: Planning template and workflow references

**Covers: REQ-001, REQ-002, REQ-003**

Rename internal/command_templates/sources/spec-to-plan.md to design-to-plan.md;
change the title to Design to Plan Converter. Preserve its body contract and
frontmatter semantics. Render templates/commands/design-to-plan.md, retiring the
old complete template. Update spec-to-design, auto-dev, quick guidance and active
references. Rename registry and translation keys without increasing command counts.

### C2: Integration installation and retirement

**Covers: REQ-001, REQ-004**

Use existing install_commands_to_subdir in src/codexspec/commands/installer.py and
CodexIntegration.install_skills in src/codexspec/integrations/codex.py. Once the new
entry has been installed (or is already present as an independent regular file),
remove only the old Claude
spec-to-plan.md or Codex codexspec-spec-to-plan/SKILL.md. Remove an empty retired
skill directory but preserve any additional files. Do not recursively delete arbitrary
skill resources. Cleanup is enabled only when the distribution includes the new
design-to-plan template, so partial template installs are not unrelated cleanup jobs.
Selected integrations retain their existing installation-selection semantics.

Deletion is idempotent when the entry is absent. Filesystem failures propagate
through the existing installation error path; do not report a successful update
with the retired runnable entry still present. Check retirement path ancestry within the installation destination (the Claude
command directory or Codex skills directory) for symlinks and refuse linked parent
directories there. Caller path aliases above that destination remain supported.
Deleting a terminal old-entry symlink removes the entry, not its target. A
replacement entry that is a directory or symbolic link, or whose parent within
the installation destination is linked, fails explicitly before writing or
retirement; it must not be treated as an available independent replacement. This is narrow
retirement, not a generic stale-file sweep or command compatibility layer.

### C3: Current documentation and generated artifacts

**Covers: REQ-001, REQ-003**

Update README translations, current docs, context templates, active helper guidance,
and workflow tests. Retain historical feature records, historical release notes,
and profile evidence as historical references. Render complete command templates
with internal/command_template_fragments.py --write, then use the local checkout's
normal init flow to refresh Claude/Codex copies and managed context. No derived
command/skill file is hand-edited. Package paths and dependencies remain unchanged.

### C4: Verification contracts

**Covers: REQ-001, REQ-002, REQ-003, REQ-004**

Exercise installer registry, fresh installation, retirement on update, repeat
installation, unrelated-file preservation, failure propagation, both integrations,
translation keys, auto-next, and rendered distribution consistency. Existing planner
contract tests continue to assert design input, traceability and review behavior.

## Key Design Decisions

### D1: A rename replaces the old identity

**Covers: REQ-001, REQ-002, REQ-003**

Rename source/template/registry/catalog identities together. Keep the command count
unchanged and retain input behavior. An alias or forwarding template is rejected by
requirements.md DEC-001; a second implementation would also create drift.

### D2: Retire only exact installed entry files

**Covers: REQ-004**

An installer that only copies the new filename leaves the old command runnable.
Remove the exact retired entry after the replacement is present. Preserve unrelated
files and do not introduce broad directory deletion. A failed retirement is an
installation error rather than silently retaining compatibility.

### D3: Preserve historical provenance

**Covers: REQ-003**

Historical SDD records and release history describe the old shipped name and remain
unchanged. Operational documentation and active guidance use the new name. This
keeps provenance auditable while removing instructions to use the retired command.

## Requirements Coverage

| Requirement | Design Coverage |
| --- | --- |
| REQ-001 | C1, C2, C3, C4, D1 |
| REQ-002 | C1, C4, D1 |
| REQ-003 | C1, C3, C4, D1, D3 |
| REQ-004 | C2, C4, D2 |
