# Confirmed Requirements: debug-command

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml (document: en).
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0811-1418yq`
**Status**: Confirmed
**Last Confirmed**: 2026-08-11

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Needs

### NEED-001: Standalone `/codexspec:debug` command running a systematic root-cause discipline

- **Status**: confirmed
- **Statement**: Provide a standalone `/codexspec:debug` command that runs a systematic root-cause debugging discipline on a user-supplied symptom (an error, a failing test, or unexpected behavior). It is directly invocable at any time, independent of the SDD pipeline.
- **Rationale**: Replace blind guess-and-check with a root-cause-first discipline, and give an on-demand entry point usable anytime — not only from inside the pipeline.
- **User Evidence**: "单独执行 debug 命令的场景是怎样的，用户如何告诉debug命令具体的bug情况或者bug现象"
- **Confirmed At**: 2026-08-11

### NEED-002: The four-phase root-cause discipline (the single definition)

- **Status**: confirmed
- **Statement**: The discipline — authored once in `debug.md` — is a four-phase protocol:
  1. **Root-Cause Investigation** — a hard gate: no fix may be proposed until the root cause is understood (read the error, reproduce consistently, check recent changes, trace data flow backward).
  2. **Pattern Analysis** — compare against working references, identify all differences.
  3. **Hypothesis & Verification** — write a single hypothesis, change one variable at a time, verify before proceeding.
  4. **Fix** — write a failing test first, apply a single fix, verify without breaking other tests.
  - Hard gate: after **≥3 failed fixes, STOP and question the architecture**.
- **Rationale**: Borrowed from superpowers `systematic-debugging`; root-cause-first prevents symptom patching.
- **User Evidence**: "四阶段（根因调查硬门→模式比对→单一假设验证→先写failing test再单一修复；≥3次失败停下质疑架构）"
- **Confirmed At**: 2026-08-11

### NEED-003: A single reference-style hook in `implement-tasks` (two trip conditions)

- **Status**: confirmed
- **Statement**: `implement-tasks` carries one reference-style escalation into debug, firing on either trip condition:
  - **(a) TDD**: the green loop cannot close a red test after several attempts, or a fix breaks a previously-passing test, or guess-and-check is detected (§3 TDD Workflow).
  - **(b) Review repair**: while repairing a non-trivial functional/correctness defect surfaced by its own `review-code` call (§7.4 Apply Test-Safe Repairs).
  - On completion, control **explicitly resumes** the task.
- **Rationale**: `implement-tasks` is the single locus of all fixing — it runs TDD, calls `review-code`, and repairs `review-code`'s findings — so the escalation only needs to attach there.
- **User Evidence**: "本质其实只要加在 implement-tasks 一个命令中即可，因为implement-tasks包含了TDD的功能实现，也包含了 review-code 的调用以及对review-code检查出来的缺陷进行修复"
- **Confirmed At**: 2026-08-11

### NEED-004: One definition, two reach paths (DRY)

- **Status**: confirmed
- **Statement**: The discipline is written once in `debug.md` and reached via exactly two paths: (1) direct standalone invocation, and (2) the `implement-tasks` hook (which itself trips on the two conditions in NEED-003). The hooks never duplicate the discipline text.
- **Rationale**: Single source of truth; both entry points point at the same file.
- **User Evidence**: "一份根因纪律（只写在 debug.md）"; "DRY"
- **Confirmed At**: 2026-08-11

### NEED-005: Input contract — free-form symptom, reproduce-or-ask

- **Status**: confirmed
- **Statement**: The standalone command accepts a free-form symptom via `$ARGUMENTS` (plain description, error text, stack trace, or failing-test id) or reads error output already present in the session. When the report is too thin, Phase 1 **reproduces or asks** (attempts reproduction itself, or requests reproduction steps / expected-vs-actual / error text / when it started) before proposing any fix.
- **Rationale**: Low-friction intake; the root-cause-first gate still holds regardless of how the symptom arrives.
- **User Evidence**: "用户如何告诉debug命令具体的bug情况或者bug现象"
- **Confirmed At**: 2026-08-11

## Constraints

### CON-001: Single handoff primitive

- **Status**: confirmed
- **Statement**: The hook uses CodexSpec's only command-to-command primitive — a template line `Invoke /codexspec:debug` — the same verb used by `review-spec`/`review-plan`/`review-tasks`. No new mechanism is introduced.
- **User Evidence**: "codexspec 只有一个 handoff 原语"

### CON-002: The hook is conditional, non-gating, low-ceremony, with explicit resume

- **Status**: confirmed
- **Statement**: The escalation is (1) conditional (`IF <trip>`), (2) non-gating (it produces no PASS/FAIL that gates the chain), (3) low-ceremony (no forced notice line, does not interrupt the user), and (4) ends with an explicit "resume the task" instruction — because CodexSpec has no runtime stack, the return is written into the instruction, not popped by an engine.
- **User Evidence**: "引用式 = 同一个 Invoke，只是外包装为：有条件 + 不 gate + 低仪式 + 修完显式 then resume"

### CON-003: Trip condition (b) is narrowed; `review-code` stays review-only

- **Status**: confirmed
- **Statement**: Trip (b) applies only to functional/correctness (or robustness) defects whose fix is **non-trivial** (needs tracing across call chains, state, or data flow — not a mechanical local edit). It excludes idiomatic-clarity, architecture, constitution-alignment, style, and trivial mechanical fixes. `review-code` itself remains strictly review-only ("the outer caller owns any repair") and is **not modified**.
- **User Evidence**: review-code.md — "you do not edit files, apply fixes... **The outer caller owns any repair**" (so review-code is review-only and is NOT modified). The "correctness + non-trivial" narrowing is a limiter on trip **(b)** of the `implement-tasks` hook — not on any review-code hook. (The earlier "review-code hook" framing was superseded by the single-hook simplification; see DEC-003.)

### CON-004: Governance / self-bootstrap

- **Status**: confirmed
- **Statement**: Edit `templates/commands/` only; derived artifacts (`.claude/commands/`, `.agents/skills/`) are regenerated via publish → `codexspec init`. Templates are authored in English with a `## Language Preference` section.
- **User Evidence**: Project constitution — Slash Command Template Modification Rules; Self-Bootstrap.

### CON-005: No persistent debug artifact

- **Status**: confirmed
- **Statement**: `debug` produces no persistent artifact — no SDD artifact (requirements/spec/plan) and no debug trace/journal file. Reusable root causes are captured through the existing `distill` → `.codexspec/profile/pitfalls.md` channel (distill's responsibility, not debug's).
- **User Evidence**: "那就不额外留debug文件了，可选存档这个功能不是自动化默认开启的话就很鸡肋"

## Decisions

### DEC-001: Reference-style handoff

- **Status**: confirmed
- **Decision**: The hook uses a reference-style escalation (a conditional, non-gating, low-ceremony `Invoke /codexspec:debug` that resumes the caller).
- **Alternatives Rejected**: Explicit command handoff — emit a notice and pause for the user to trigger it, or fire a discrete auto-invoke as a visible chain step.
- **Reason**: "When stuck, just debug properly" should be a seamless continuation, not a ceremony that interrupts the user.
- **User Evidence**: "handoff 采用 引用式(最轻,推荐)"

### DEC-002: No `workflow.auto_debug` config key

- **Status**: confirmed
- **Decision**: Do not add a `workflow.auto_debug` configuration key.
- **Alternatives Rejected**: An opt-in gate analogous to `workflow.auto_next`.
- **Reason**: Systematic debugging when stuck is strictly-better default behavior that nobody would opt out of; analogous to the existing conditional-TDD guidance, which is likewise ungated.
- **User Evidence**: "不加 workflow.auto_debug 配置键"

### DEC-003: Attach surface = `implement-tasks` only

- **Status**: confirmed
- **Decision**: Attach the hook to `implement-tasks` only.
- **Alternatives Rejected**: (a) A separate hook or recommendation inside `review-code` — unnecessary, because `review-code` is review-only and `implement-tasks` already owns the repair of its findings; (b) attaching the hook to further commands.
- **Reason**: `implement-tasks` is the single locus of all fixing (TDD + review-defect repair). For the standalone review-then-user-fix path, the user invokes `/codexspec:debug` themselves.
- **User Evidence**: "本质其实只要加在 implement-tasks 一个命令中即可"

## Out of Scope

### OUT-001: Debug is not a mandatory pipeline stage

- **Status**: confirmed
- **Statement**: No forced, dedicated `debug` step is inserted into the `specify → … → implement-tasks` chain. Debug is reached only conditionally (the `implement-tasks` hook) or on-demand (standalone).
- **Reason**: Debug is not a stage in the mandatory SDD chain. (This is unrelated to `auto_next`: `auto_next` only auto-advances between existing mandatory stages, and debug is not one.)
- **User Evidence**: "debug 不是一个必然调用的命令所以没有在流程中强制一个专门单独调用debug的环节"

## Open Questions

### OPEN-001: Exact `debug.md` template skeleton

- **Status**: open (non-blocking; a design detail resolved in spec/implementation)
- **Why It Matters**: Determines the final command file layout; does not block spec generation.
- **Owner**: Team
- **Suggested starting point** (sampled from existing templates): frontmatter `description` + `argument-hint` + `allowed-tools`; sections `## Language Preference` → `## User Input` → `## Role and Iron Law` → `## Symptom Intake` → `## Investigation Protocol` (Phase 1–4 + Architecture Gate as `###` subsections) → `## Completion`.

<!--
Resolved during discovery:
- The review-code hook wording (an earlier open question) was resolved by the single-hook simplification (DEC-003): its "correctness + non-trivial" narrowing became CON-003 (trip condition (b) limiter).
- Whether to leave a root-cause note / debug trace file (an earlier open question) was resolved as CON-005 (no persistent artifact).
-->

## Confirmation Log

### Session 2026-08-11

- **Summary Presented**: debug = one standalone command carrying a four-phase root-cause discipline + one reference-style hook in `implement-tasks` with two trip conditions (stuck TDD test; non-trivial correctness-defect repair). No config key, no persistent artifact; `review-code` unmodified.
- **User Confirmation**: "确认"
- **Entries Confirmed**: NEED-001..005, CON-001..005, DEC-001..003, OUT-001
- **Open (non-blocking)**: OPEN-001
- **Notable rejected alternatives**: a separate `review-code` hook (dropped — `implement-tasks` owns all repair); a debug trace file / root-cause note (dropped — non-automatic persistence is low value; reusable knowledge flows through `distill`); a `workflow.auto_debug` gate (dropped).
