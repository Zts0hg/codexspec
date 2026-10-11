# Confirmed Requirements: Unified Staged Commit Analysis

**Feature ID**: `2026-1010-21225w`
**Status**: Confirmed
**Last Confirmed**: 2026-10-11

## Authority Rules

Only entries with `Status: confirmed` are binding downstream inputs. Open questions
and AI assumptions are not requirements. Replaced entries must retain their history
with `Status: superseded` and a reference to their replacement.

## Needs

### NEED-001: Use commit-staged analysis throughout agent commit workflows

- **Status**: confirmed
- **Statement**: When an agent creates a Git commit, it must proactively use
  `commit-staged` to analyze staged changes and generate an accurate, complete
  commit message, with the history-only merge exception defined in DEC-002.
  This covers direct agent commits, auto-dev feature commits,
  and blueprint commits, on the supported Codex and Claude integrations.
- **Rationale**: Installing or listing the command does not ensure agents use its
  analysis capability when they decide to commit. Internal helper execution must
  not exempt a workflow from that analysis.
- **User Evidence**: “本质上是要统一利用好 commit-stage的分析能力以生成更加准确完整的commit message，并且适配好 commit-staged 只针对暂存区进行分析的设计。”
  The user explicitly included blueprint commits with “纳入”, then confirmed
  the final four-entry summary with “确认”. `commit-stage` in the quotation refers
  to the existing `commit-staged` command.
- **Confirmed At**: 2026-10-10

### NEED-002: Ground messages in the actual staged changes

- **Status**: confirmed
- **Statement**: Commit messages must accurately and completely describe the
  actual staged changes, without incorporating unstaged changes or intent that
  exists only in conversation.
- **User Evidence**: The final confirmed summary requires messages to be based
  on staged changes and excludes unstaged content and conversation-only intent.
- **Confirmed At**: 2026-10-10

## Constraints

### CON-001: The caller prepares staging; commit-staged analyzes it

- **Status**: confirmed
- **Statement**: The calling workflow is responsible for preparing what will be
  staged for the commit. Preserve the boundary that `commit-staged` does not
  independently choose or stage files and analyzes only the staging area.
- **User Evidence**: “适配好 commit-staged 只针对暂存区进行分析的设计。” The user
  confirmed the final summary assigning staging preparation to the caller.
- **Confirmed At**: 2026-10-10

### CON-002: Match analysis to the committed content and preserve protections

- **Status**: confirmed
- **Statement**: The content actually committed must match the content analyzed.
  If that content changes, analyze it again before committing. Integration must
  preserve helpers' existing validation, concurrency protections, and recovery
  mechanisms.
- **User Evidence**: The user confirmed the final summary requiring content
  correspondence, reanalysis after changes, and preservation of helper safeguards.
- **Confirmed At**: 2026-10-10

## Decisions

### DEC-001: Preserve commits without a persistent CodexSpec CLI

- **Status**: confirmed
- **Statement**: Ship the same deterministic commit validation helper with
  installation artifacts so Claude plugin users and projects initialized once
  through uvx can preview and execute direct commits without a persistent
  `codexspec` executable. Python and Git remain prerequisites. Message generation
  remains with the agent's LLM through commit-staged.
- **User Evidence**: “保留无 CLI 提交：随安装产物提供同一校验 helper（推荐）”. After
  the division of responsibility and distribution approach were explained, the
  user replied “明白了，继续”.
- **Confirmed At**: 2026-10-10

### DEC-002: Analyze contentful merges and retain default messages for history-only merges

- **Status**: confirmed
- **Statement**: Agent-created merge commits with staged changes use commit-staged
  analysis, including default-branch synchronization, conflict resolution, and
  divergent baseline preparation. When the resulting tree equals the current
  HEAD tree, retain Git's default merge message while still validating the
  committed tree and merge parents. Fast-forward integration creates no commit
  and requires no message generation. Empty non-merge staging remains an error.
- **User Evidence**: “保留 Git 默认合并消息，但仍校验提交内容（推荐）”. After the
  concrete auto-dev and workspace initialization scenarios were explained, the
  user replied “明白了。继续”.
- **Confirmed At**: 2026-10-11

## Out of Scope

No additional exclusions were confirmed. Helper-driven blueprint commits are
explicitly included, not exempted as fixed-message operations.

## Open Questions

None. The blueprint coverage question is resolved by NEED-001.

## Superseded Entries

None.

## Repository Context (Evidence, Not Additional User Requirements)

At baseline `b72c0c5d8397a0ebfa2c398a8ab649fa24fe7aa7`:

- `src/codexspec/integrations/codex.py` installs skills and generates the Codex
  context entry; its workflow list has no commit-staged invocation rule.
- `src/codexspec/__init__.py` lists commit-staged in generated Claude context.
- `internal/command_templates/sources/implement-tasks.md` directs commits
  without routing their analysis through commit-staged.
- `internal/command_templates/sources/auto-dev.md` sends a type, description,
  and paths to the commit-feature helper.
- `src/codexspec/automation.py` formats feature commit messages from caller
  fields and blueprint messages from operation names; both execute Git directly.
- The project constitution requires distributed command edits in their authoring
  sources, with regenerated complete templates and installation artifacts.
- Profile constraint `C-2026-0902-054178-1` requires maintainer-only generation
  mechanisms to be validated before installation and to ship complete artifacts.

## Confirmation Log

### Session 2026-10-10

- **Summary Presented**: Proactively use commit-staged for direct, auto-dev, and
  blueprint commits; ground messages in staged changes; make callers prepare
  staging; preserve analyzed/committed content equality and helper safeguards.
- **User Confirmation**: “确认” following the final four-entry summary.
- **Entries Confirmed**: NEED-001, NEED-002, CON-001, CON-002.
- **Open IDs**: None; discovery is complete.

### CLI-free installation compatibility confirmation

- **User Confirmation**: Selected distribution of the same helper with installation
  artifacts, then explicitly authorized continuation after explanation.
- **Entries Confirmed**: DEC-001; NEED-001, NEED-002, CON-001 and CON-002 remain binding.
- **Open IDs**: None.

### Merge coverage confirmation, 2026-10-11

- **Entries Confirmed**: DEC-002, refining NEED-001 and CON-002 for merge commits.
- **User Confirmation**: Selected the default-message exception for history-only
  merges and authorized continuation after the affected scenarios were explained.
- **Open IDs**: None.
