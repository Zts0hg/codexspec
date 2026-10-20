# Implementation Plan: Command Descriptions

## Context

Implement [design.md](design.md) within the confirmed 28-command content scope.
Use current command instructions as evidence; preserve behavior, argument hints
and existing distribution architecture.

## P1: Read commands and author English descriptions

Covers: REQ-001, REQ-002, REQ-004, NFR-001; Design: C1, D2.

Read all current command sources and referenced rules relevant to descriptive
claims. Consult historical requirements for meaningful behavior evolution.
Record per-command source evidence and important distinctions in inventory.md.
Apply the approved compact English and Chinese strings verbatim; rewrite only
the description line in each internal authoring source. The bilingual review
required by CON-002 is complete.

## P2: Translate and synchronize metadata

Covers: REQ-003, NFR-001; Design: C2, D1.

Update description fields in templates/translations/{en,zh-CN,ja,ko,de,fr,es,pt-BR}.json.
Preserve keys, hints and other content. Align installer.py fallback descriptions
with zh-CN. Review every translated sentence for faithful, natural expression.

## P3: Regenerate, verify and review

Covers: REQ-001, REQ-002, REQ-003, NFR-001; Design: C3, D2.

Render complete templates using the existing fragment tool and regenerate host
entries through the normal installer. Run distribution checks, relevant existing
translation/installer/Codex tests and lint for changed Python/Markdown/JSON files.
Exercise actual installation in a temporary project and inspect command listing
output. Verify diff preservation of bodies, hints, command membership and versions.
Run the required independent final review after evidence is stable.

## Plan-Level Decisions

Content edits, including Python string metadata, use direct editing and existing
verification rather than new tests pinning every new phrase. Test selection covers
the changed distribution and translation paths, not unrelated execution features.
No commit, push or release is part of this plan.

## Risks and Verification

Semantic drift is controlled through current-source evidence and locale-by-locale
reading. YAML punctuation and generated drift are controlled by parsing and
distribution checks. Long fallback strings must satisfy existing Python lint via
adjacent string literals, without changing values.

## Coverage

| Requirement | Plan | Design |
| --- | --- | --- |
| REQ-001 | P1, P3 | C1, C3 |
| REQ-002 | P1, P3 | C1, D2 |
| REQ-003 | P2, P3 | C2, C3 |
| REQ-004 | P1, P2, P3 | C1, C2 |
| NFR-001 | P1, P2, P3 | C1, C2, D2 |
