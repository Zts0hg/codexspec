---
description: Reverse-derive spec/design from existing code, then reconcile code against the confirmed baseline
argument-hint: "[path]"
allowed-tools: Read, Grep, Glob, Bash(git:*), Bash(ls/cat/find:*), Edit, Write
---

# Reverse Specification

## Language Preference

Read `.codexspec/config.yml`. Two independent language controls apply (each falls back to `language.output`, then English):

- **Interaction language** (`language.interaction`): language for all conversation with the user — questions, explanations, status messages, and `codexspec` CLI terminal output.
- **Document language** (`language.document`): language for generated artifact files (the reverse-derived spec/design and the reconcile report).

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language.

## User Input

`$ARGUMENTS`

## Role and Operating Model

You bring an existing codebase into Requirements-First SDD, and you keep it there.
The command runs in exactly one of three mutually exclusive modes, chosen before
any output is written:

- **Overview** — no path given. Survey the architecture and produce a map plus a
  list of candidate slices worth specifying.
- **Generate** — a path is given and no confirmed baseline exists for it. Read the
  code and draft the slice's specification and design, all marked as inferred.
- **Reconcile** — a path is given and a confirmed baseline exists. Compare the
  current code against that baseline and report drift.

The lifecycle is generate, then human confirmation, then reconcile — repeatedly.
Generation alone cannot detect deviation, because a specification derived from
code is a mirror of that code and the two agree by construction. Confirmation is
the step that injects human intent and turns a description of what the code is
into a specification of what it ought to be. Reconciliation is only meaningful
against that confirmed baseline.

Two principles govern everything below:

- **Two axes.** Authority runs requirements over spec over design over plan over
  tasks, and decides which artifact wins a conflict. Reconcilability runs the
  other way — design and spec can be compared to code, requirements cannot — and
  decides what may serve as a comparison baseline. Compare against spec and
  design; adjudicate with requirements.
- **Report, never repair.** When code and a confirmed specification disagree, the
  code may carry a defect or the specification may be stale. The direction is not
  derivable by this command, so it is always surfaced and never applied.

## Mode Resolution

Resolve the mode first, in this order. Do not write anything until the mode is settled.

1. **No path supplied.** Enter overview mode. The command performs the
   architectural survey and never reconciles, whatever the state of any existing
   workspace. Do not perform a baseline lookup at all in this case. If an
   `<id>-overview` workspace already exists, continue it rather than creating a
   second one, so an interrupted survey resumes instead of leaving orphans.
2. **The argument is not a path.** If it is a diff or pull-request range such as
   `main..feature`, `HEAD~3..HEAD`, or `#42`, report the path-only contract from
   the next section and stop. Test this before testing path existence, so such an
   argument is never misreported as a merely invalid path.
3. **The path does not exist.** Report the invalid path and stop. Create no
   workspace.
4. **The path exists.** Resolve it to a slice and search `.codexspec/specs/*/`
   for a workspace whose recorded `Slice:` value matches that path. A workspace
   containing `slices.md` is an overview workspace, never a baseline: skip it
   during this search. Identify it by that positive marker, not by the absence of
   a `spec.md` — a slice workspace left incomplete by an interrupted run may not
   have written its `spec.md` yet, and must not be mistaken for an overview.
5. **No matching workspace.** Enter generate mode — but first check that the slice
   contains analyzable code. If it does not, report that there is nothing to
   reverse-derive and stop, creating no workspace and no artifacts. This check
   belongs to generate mode alone. Never apply it in reconcile mode: a slice whose
   implementation has been emptied is the maximal `unimplemented-spec` case, and
   reporting it as drift is exactly what this command exists to do.
6. **Several matching workspaces.** Ask the user to select one. Never silently
   pick the most recent workspace.
7. **One matching workspace whose artifacts are confirmed.** Enter reconcile mode.
8. **One matching workspace whose artifacts are still open.** Do not reconcile:
   comparing code against a draft derived from that same code would compare the
   code with itself and report no drift by construction. Instead **resume generate
   mode into that existing workspace**, continuing an interrupted or incomplete
   draft rather than starting over. Never create a second workspace for a slice
   that already has one. Report that you are continuing the draft rather than
   reconciling, and state the exact confirmation action from the section below so
   the user knows how to promote it once it is complete.

Report the resolved mode before proceeding, so the user can stop you if it is not
the mode they wanted.

## Slice and Workspace

A slice is a directory, module, or package path, or a file set within one. The
`[path]` argument is the slice boundary. Do not attempt to partition the codebase
automatically, and do not merge several unrelated directories into one slice.

A diff or pull-request range is not a slice source. If the user supplies one,
report the path-only contract and stop; reverse-deriving a specification for a
single change is a different workflow.

A workspace is the directory `.codexspec/specs/<id>-<slice>/`. Reuse the project's
existing `{YYYY-MMDD-HHMM}{rr}` identifier convention exactly — a timestamp plus
two random lowercase alphanumeric characters — and derive the slice segment from
the slice's final path segment, normalized to kebab-case (`overview` for a bare
run). Never implement a separate identifier generator and never fall back to
sequential numbering. If `.codexspec/specs/` does not exist, report the missing
prerequisite and stop rather than scaffolding an SDD workspace root yourself.

Create the directory only. Do not run `.codexspec/scripts/create-new-feature.sh`
or its PowerShell counterpart: those scripts create and switch a git branch, which
this command must never do. Creating a workspace changes no git state, so the
command is safe to run on whatever branch the user is already working on.

Every generated `spec.md` and `design.md` carries a `Slice:` header holding the
repo-relative path its content describes. This field is the whole baseline-lookup
mechanism: there is no index file and the directory name does not encode the path.
State the recorded value in the closing summary so a later mismatch is diagnosable.

## Generate Mode

Scan the slice per the scan discipline below, writing as you go rather than
holding everything until the scan completes. Create the workspace as soon as the
slice is confirmed to have analyzable code, and append to the artifacts
incrementally so an interrupted run leaves usable partial output that a re-run can
continue from. Three artifacts are produced:

- `spec.md` — the behavior and contracts the code exhibits: public surface,
  inputs and outputs, observable behavior, error and boundary handling.
- `design.md` — the structure the code has: components, responsibilities,
  interfaces, and relationships. Scale it to the slice's real complexity. A
  structurally trivial slice gets a thin design, not padded sections.
- `requirements.md` — a thin stub whose entries are all open.

Attribute every derived statement to something you observed in the code. Intent is
not present in code: do not reverse-derive why a feature exists, and never present
an inferred purpose as confirmed requirement. Where behavior is genuinely unclear
from the code, say so in the artifact rather than filling the gap with a plausible
story.

## Overview Mode

Survey the repository high-signal-first, writing incrementally as the survey
proceeds so an interrupted run leaves usable partial output. Produce an
`<id>-overview` workspace containing exactly two artifacts:

- `design.md` — a thin architecture-level map: components, their responsibilities,
  and how they relate. Marked as inferred, scaled to complexity.
- `slices.md` — the candidate slice list. One row per slice: path, a one-line
  description, and a rough size or priority.

Overview mode writes no `spec.md` and no `reconcile.md`. It is a map and a
deepening plan, not a specification. A single repository-wide detailed
specification is unreadable and unmaintainable, which would defeat the reason this
command exists.

## Inference Marking and Confirmation

Everything this command derives is inference, not confirmed intent.

Generated `spec.md` and `design.md` carry a file-level `Status: inferred/open`
header, mark their principal entries `[inferred]`, and state in the file that they
are not a reconciliation baseline until confirmed. The `requirements.md` stub is
likewise entirely open.

Promotion to baseline is done by the user, reusing the convention `requirements.md`
already uses: change the file-level status from open to confirmed and append a
Confirmation Log entry recording what was reviewed and that it was confirmed. This
command adds no separate confirmation command, no flag, and no state file.

End generate mode by stating the exact confirmation action, including the file
paths and the status line to change. Confirmation is a manual step, and a user who
never takes it never gets the drift checking this command exists to provide.

## Reconcile Mode

The baseline is the slice's confirmed `spec.md` and `design.md`. When the confirmed
baseline has a spec but no design — the design was legitimately scaled away, or the
workspace predates it — reconcile against the spec alone.

Never use `requirements.md`, `plan.md`, or `tasks.md` as a comparison baseline.
Requirements deliberately withhold verifiable contracts, so they cannot mechanically
adjudicate code: a requirement to resist brute force is equally satisfied by locking
after three attempts, after five, or by rate limiting. Plan and tasks are build
scaffolding and say nothing about whether the code conforms to its design.

Re-read the slice's current code and classify each finding as exactly one of:

- `undocumented-behavior` — the code does something the baseline never describes.
- `unimplemented-spec` — the baseline states something the code does not do.
- `semantic-mismatch` — both sides address the same thing and disagree about it.

Assign each item a severity of Critical, Warning, or Minor from the item's actual
impact against confirmed intent. Severity is not fixed by its kind: an
undocumented behavior can be a security-grade finding such as a hidden endpoint,
and a semantic mismatch can be trivial.

For a `semantic-mismatch`, quote both sides as evidence — the code observation and
the baseline text. An item you cannot evidence on both sides is not reported as a
mismatch.

Propose a direction for each item, reasoning from the confirmed `requirements.md`
intent where it exists, since requirements adjudicate which side should change even
though they are never the comparison baseline. When no confirmed intent settles the
item, set the direction to `needs-your-judgment`. Never guess a direction, and never
suppress a drift item merely because its direction cannot be derived — reporting the
drift is the point.

The suggested direction is never applied. Reconciliation modifies no code, no
baseline artifact, and nothing else in the repository.

## Reconcile Report

Write `reconcile.md` into the resolved slice workspace, and additionally give a
short briefing in the conversation.

```text
# Reconcile Report — <slice>
## Summary
- Baseline: <the spec.md / design.md compared against, and their confirmed status>
- Code scope: <path/slice>
- Status: IN_SYNC | DRIFT_DETECTED
- Counts: undocumented N1 / unimplemented N2 / mismatch N3, plus the severity spread
## Drift Items
- id: <stable identifier>
- kind: undocumented-behavior | unimplemented-spec | semantic-mismatch
- severity: Critical | Warning | Minor
- location: <code path:line> and the corresponding baseline reference
- evidence: the code observation and the baseline text, side by side
- direction: fix-code | update-spec | needs-your-judgment, with reasoning
- status: open
## Notes
```

`reconcile.md` is this command's own output, not a pre-existing artifact in the
sense of the boundary below, so a later reconcile of the same slice regenerates
it. Regeneration replaces the previous report: any adjudication the user recorded
by editing item statuses in it is not carried over. Say so before overwriting, so
the user can resolve or copy out an earlier report's open items first.

The report status and the item severities exist to help the user prioritize. They
are not a gate: this command emits no pass/fail verdict, and no other command
consumes the report's status. Zero drift items with status IN_SYNC is a valid and
common outcome, not a failure.

## Scan Discipline

Scanning follows the discipline defined in `/codexspec:onboard` — read that
command's scan section rather than a restatement here, so the two cannot drift
apart. In short: high-signal-first, deep-read the structural and configuration
surface while shallow-sampling bulk business code, respect `.gitignore` with a
documented fallback when there is no git, stream output so an interrupted run is
resumable, and never claim full coverage when you sampled.

Two parts of that section do not carry over, and the referenced text must be read
subject to these overrides:

- Where `onboard` streams findings into the profile store and writes each
  convention as it is confirmed, this command writes nothing to
  `.codexspec/profile/`. Its incremental output goes to its own workspace
  artifacts instead. Importing that write directive would breach the boundary
  below and create a second writer for a store this command does not own.
- In `onboard` the `[path]` argument narrows a profile scan, whereas here it is
  the slice boundary itself and therefore also determines what the generated
  artifacts describe.

## Boundaries

- Read-only on the codebase. This command never modifies source, tests, git state,
  or the constitution.
- Writes are confined to the feature workspace it creates or resolves.
- Never writes to `.codexspec/profile/`. That store belongs to `/codexspec:distill`
  and `/codexspec:onboard`.
- Never edits an artifact it did not produce — source, tests, and above all the
  baseline it reconciles against. Regenerating its own `reconcile.md` on a repeat
  run is the one exception, and is covered by the notice rule above.
- Never applies a drift resolution, in either direction.

## Output Summary

Report the resolved mode and why, the slice and the workspace path, the recorded
`Slice:` value, the artifacts written, and what remains for the user to do. In
generate mode that is the confirmation action; in reconcile mode it is adjudicating
each open drift item. Distinguish deep-read areas from sampled ones, and never
claim coverage you did not achieve.
