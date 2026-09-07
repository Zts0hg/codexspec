# Confirmed Requirements: profile-filename-readability

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml.
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0907-1623rh`
**Status**: Confirmed
**Last Confirmed**: 2026-09-07

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Profile record filenames reveal the record's topic without opening the file

- **Status**: confirmed
- **Statement**: When browsing `.codexspec/profile/<category>/`, the filename must convey what the record is about. Today the filename is `{type}-{feature-id}-{seq}.md` (e.g. `P-2026-0902-054178-4.md`), whose unique part is a timestamp+random feature id that carries no content meaning, so a reader must open the file to learn its subject.
- **Rationale**: The profile is read by scanning directory listings (per the ambient profile block in CLAUDE.md and during `/distill review` / `/evolve`); opaque filenames force a file open per record and defeat at-a-glance recall.
- **User Evidence**: "我觉得目前 distill 命令生成的profile/ 目录下的文件的文件名可读性比较差,希望优化。"
- **Confirmed At**: 2026-09-07

### NEED-002: The filename stays resolvable to the record id

- **Status**: confirmed
- **Statement**: The mapping between a record's filename and its id must remain mechanical: the `### <id>: <title>` heading keeps the bare id, `[[id]]` cross-links between records keep working, and a reader (or agent) can locate a record's file from its id and back without ambiguity.
- **Rationale**: The id is referenced across the store (headings, `[[...]]` links, provenance lines) and is the anchor for dedup/replace/remove during distill; renaming semantics must not break those references.
- **User Evidence**: Confirmed as part of the stage summary the user answered (scheme selection implies preserving id-based addressing).
- **Confirmed At**: 2026-09-07

## Constraints

### CON-001: Parallel-branch conflict-free merging must be preserved

- **Status**: confirmed
- **Statement**: The uniqueness portion of the filename must not be derived from record content. Two feature branches distilling similar knowledge would then produce the same filename and collide on merge. The current scheme guarantees uniqueness by construction (feature id embeds timestamp+random chars, sequence distinguishes records within a feature); that property must survive the change.
- **User Evidence**: Confirmed via the stage summary; the user selected the scheme that keeps the existing unique id as the filename prefix (Option A) over content-derived naming (Option C, explicitly shown with its collision risk).
- **Confirmed At**: 2026-09-07

### CON-002: Filenames must be cross-platform-safe ASCII

- **Status**: confirmed
- **Statement**: The variable, human-readable part of the filename uses only lowercase ASCII letters, digits, and hyphens as separators (grammar `^[a-z0-9]+(-[a-z0-9]+)*$`, no leading/trailing hyphen). No spaces, no uppercase (Windows case-insensitivity), no CJK or other non-ASCII characters. When the record title is not ASCII, the slug is derived as English.
- **User Evidence**: Confirmed via the stage summary (constraint listed in the presented summary alongside the recommended option).
- **Confirmed At**: 2026-09-07

## Decisions

### DEC-001: Adopt `{id}-{slug}.md` — keep the existing unique id, append a semantic slug

- **Status**: confirmed
- **Decision**: A record's filename becomes `<id>-<slug>.md`. The `<id>` part is unchanged (`{type}-{feature-id}-{seq}`, e.g. `P-2026-0902-054178-4`); a semantic slug derived from the record title is appended, lowercase-ASCII kebab per CON-002, recommended maximum 50 characters. The slug appears only in the filename — the id, the `### <id>: <title>` heading, and `[[id]]` links are unchanged. Example: `P-2026-0902-054178-4-precommit-stash-untracked.md`. This mirrors Codex's proven pattern (`<timestamp>-<hash>-<slug>` in `rollout_summaries/`): uniqueness by unique prefix, readability by trailing slug.
- **Alternatives Rejected**:
  - Option B (slug first, unique tail last): scatters the id, sorts by topic instead of time, and complicates traceability.
  - Option C (Claude Code-style free naming `{type}_{topic}.md`): uniqueness would rest on the agent's attention; two parallel branches distilling similar topics collide on merge, and the scheme loses source-feature traceability. Claude Code compensates with a `MEMORY.md` always-loaded index plus a nightly consolidation pass — mechanisms CodexSpec deliberately does not have (see OUT-001/OUT-002).
- **Reason**: Under the no-index constraint, Codex's combination is the only researched design that provides both at-a-glance readability and construction-guaranteed uniqueness; our existing id already is that unique prefix, so this is the minimal delta.
- **User Evidence**: User selected "方案A:{id}-{slug}.md(推荐)" from the presented options.
- **Confirmed At**: 2026-09-07

### DEC-002: The rule applies to newly written records only — no migration of existing records

- **Status**: confirmed
- **Decision**: The ~15 existing records keep their current `{id}.md` filenames. Only records written after this change follow `{id}-{slug}.md`. Mixed old/new naming in a directory is expected and acceptable.
- **Alternatives Rejected**: One-time batch rename of existing records (rejected: it would require fixing `[[id]]` cross-links and any external path references, and breaks git blame at rename points).
- **Reason**: Zero risk and zero collateral edits; the directory converges naturally over time.
- **User Evidence**: User selected "只对新记录生效(推荐)".
- **Confirmed At**: 2026-09-07

## Out of Scope

### OUT-001: No central index file

- **Status**: confirmed
- **Statement**: No `MEMORY.md`-style always-loaded index is introduced. distill already forbids a central index (a merge-conflict magnet that breaks the conflict-free store).
- **Reason**: Readability is delivered by the filename itself; an index would reintroduce the conflict problem the one-file-per-record store was designed to avoid.
- **User Evidence**: Confirmed via the stage summary presented with the selected option.
- **Confirmed At**: 2026-09-07

### OUT-002: No background consolidation or rename-reconciliation machinery

- **Status**: confirmed
- **Statement**: No Claude Code-style nightly consolidation job and no automated rename/reconciliation process is introduced. The store's ledger remains git history; mutations stay the agent-executed add/replace/remove discipline.
- **Reason**: CodexSpec is a convention-driven template toolkit with no resident runtime; background machinery has nothing to run in.
- **User Evidence**: Confirmed via the stage summary presented with the selected option.
- **Confirmed At**: 2026-09-07

## Open Questions

### OPEN-001: Type-letter inconsistency (`C` vs `Con`) — normalize or keep

- **Status**: open
- **Why It Matters**: Cosmetic only. Constraints use `C-`, conventions use `Con-`, all other categories use a single letter. The category directory already disambiguates, so either choice works. Recommendation (non-binding): keep as-is.
- **Owner**: User
- **Blocking**: No — the spec can be written without resolving this.

## Confirmation Log

### Session 2026-09-07 (~16:30)

- **Summary Presented**: Three-way research comparison (Codex `timestamp+hash+slug`, Claude Code `type_topic` free naming backed by MEMORY.md index + nightly consolidation, current `{id}.md`); key inference that Codex's "unique prefix + semantic slug" combination is the only design compatible with the no-index, conflict-free constraints; stage summary with NEED-001/002, CON-001/002, DEC-001 (Option A), OUT-001/002, OPEN-001/002.
- **User Confirmation**: User selected "方案A:{id}-{slug}.md(推荐)" for the naming scheme and "只对新记录生效(推荐)" for legacy-record handling via structured questions.
- **Entries Confirmed**: NEED-001, NEED-002, CON-001, CON-002, DEC-001, DEC-002, OUT-001, OUT-002
