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

Converse in the interaction language and author artifacts in the document language. Apply the project's translation standard to both: translate by meaning (not word-for-word), keep English for terms with no good native equivalent, and write as if originally in that language. **Exception**: in `reconcile.md`, `location` and `evidence` quote the code and the baseline verbatim — path, line, and the quoted spans on both sides — and MUST NOT be translated. A translated quote can no longer be checked against its source, which is exactly what the both-side evidence rule exists to make possible.

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

1. **No path supplied, or a path that resolves to the repository root.** Enter
   overview mode. A bare `reverse-spec` and `reverse-spec .` are the same run: the
   repository as a whole is never a slice, because no output of this command may
   aggregate the whole repository into a single detailed specification. The command
   performs the architectural survey and never reconciles, whatever the state of
   any existing workspace. Do not perform a baseline lookup at all in this case. To
   find an earlier survey to continue, look for a workspace holding `slices.md` —
   the same positive marker step 5 uses — and never go by the directory name. A
   generate run on a slice whose final path segment is `overview` produces an
   identically named directory, so identifying the survey workspace by name would
   let a bare run write the repository map over that slice's draft and then, once
   `slices.md` is in it, hide that slice's baseline from every later lookup. If
   exactly one workspace holds `slices.md`, continue it rather than creating a
   second one, so an interrupted survey resumes instead of leaving orphans. If
   several do, ask which to continue.
2. **The argument is not a path.** If it is a diff or pull-request range such as
   `main..feature`, `HEAD~3..HEAD`, or `#42`, report the path-only contract from
   the next section and stop. Test this before testing path existence, so such an
   argument is never misreported as a merely invalid path.
3. **The path does not exist.** Report the invalid path and stop. Create no
   workspace.
4. **The path exists but lies outside the repository.** A path such as `..`,
   `../sibling`, or `/` exists and still resolves outside. Report that a slice must
   be inside the repository and stop, creating no workspace. A slice is a subtree of
   the repository this command runs in: its `Slice:` header is defined as a
   repo-relative path carrying no `..` segment and never absolute, so an outside
   path could not be recorded in that form at all, and scanning a tree that strictly
   contains the repository would produce exactly the repository-wide specification
   step 1 exists to prevent.
5. **The path exists inside the repository.** Normalize it before comparing anything: make it
   repo-relative, resolve `.`, `..`, and absolute forms, and drop any trailing
   slash, so `src/auth`, `./src/auth`, `src/auth/`, and an absolute path to that
   same directory are one slice rather than four. Record every `Slice:` header in
   exactly this normalized form and compare in it too — an unnormalized comparison
   silently misses the workspace a slice already has and creates a duplicate.
   Then search `.codexspec/specs/*/` for workspaces whose recorded `Slice:` value
   matches the normalized path. Every workspace writes its identifying artifact as
   the act that creates it, so both the lookup key and the mode marker are present
   even in a workspace an interrupted run left half-written. A workspace containing
   `slices.md` is an overview workspace, never a baseline: skip it during this
   search. Identify it by that positive marker, not by the absence of a `spec.md`.
6. **Sort what the search found into exact and covering matches.** A workspace
   matches **exactly** when its normalized `Slice:` equals the normalized path. It
   **covers** the path when its `Slice:` is a proper ancestor of it — a workspace
   recorded as `src/auth` covers `src/auth/tokens` without being it. Only an exact
   match selects a mode on its own. A covering match never does, because its
   baseline describes a wider boundary than the slice you were given: reconciling
   against it would report everything else under that boundary as
   `unimplemented-spec`, and its `reconcile.md` belongs to that wider slice.
7. **No workspace matches, exactly or by covering.** Enter generate mode — but
   first check that the slice contains analyzable code. If it does not, report
   that there is nothing to
   reverse-derive and stop, creating no workspace and no artifacts. This check
   belongs to generate mode alone. Never apply it in reconcile mode: a slice whose
   implementation has been emptied is the maximal `unimplemented-spec` case, and
   reporting it as drift is exactly what this command exists to do.
8. **Several workspaces match exactly.** Ask the user to select one. Never silently
   pick the most recent workspace.
9. **No exact match, but one or more workspaces cover the slice.** Never pick one
   silently and never quietly start a nested workspace. Report each covering
   workspace with the slice it records, and ask the user which they want: reconcile
   or continue that workspace at its own wider boundary, or create a new workspace
   for the narrower path you were given. Proceed only on their answer.
10. **One exact match whose artifacts are confirmed.** Enter reconcile mode.
11. **One exact match whose artifacts are still open.** Do not reconcile:
    comparing code against a draft derived from that same code would compare the
    code with itself and report no drift by construction. Instead resume generate
    mode into that existing workspace. Never create a second workspace for a slice
    that already has one. Resuming means completing only what is missing: read what
    the workspace already holds, append the parts that were never written, and
    leave everything already written exactly as it stands. If the draft is already
    complete, write nothing at all and simply report the unconfirmed baseline.
    Report that you are continuing the draft rather than reconciling, say which
    parts you added and which you left untouched, and state the exact confirmation
    action from the section below so the user knows how to promote it once it is
    complete.

Whichever mode you resolved, if any existing workspace records a slice nested
inside the one you were given, say so before proceeding — the two overlap — but do
not stop for it. This disclosure is not confined to generate mode. It matters most
in reconcile: a baseline for `src/auth` compared against code that includes
`src/auth/tokens` reports that subtree's behavior as `undocumented-behavior` even
though the user holds a narrower confirmed baseline for it, and without the
disclosure the report gives no clue where those items came from.

Report the resolved mode before proceeding, so the user can stop you if it is not
the mode they wanted.

## Slice and Workspace

A slice is a directory, module, or package path, or a file set within one. The
`[path]` argument is the slice boundary. Do not attempt to partition the codebase
automatically, and do not merge several unrelated directories into one slice. The
repository root is not a slice: a path that resolves to it is the bare run and gets
the architectural survey, so no run of this command ever produces one detailed
specification covering the whole repository.

A diff or pull-request range is not a slice source. If the user supplies one,
report the path-only contract and stop; reverse-deriving a specification for a
single change is a different workflow.

A workspace is the directory `.codexspec/specs/<id>-<slice>/`. Reuse the project's
existing `{YYYY-MMDD-HHMM}{rr}` identifier convention exactly — a timestamp plus
two random lowercase alphanumeric characters — and derive the slice segment from
the slice's final path segment, normalized to kebab-case (`overview` for a bare
run). Never implement a separate identifier generator and never fall back to
sequential numbering. The directory name is a convenience for humans reading
`.codexspec/specs/`, never how a workspace is identified: a slice can legitimately
end in `overview` and produce the same name as the survey workspace, so identity
always comes from the artifacts inside — `slices.md` for a survey, the `Slice:`
header for a slice. If `.codexspec/specs/` does not exist, report the missing
prerequisite and stop rather than scaffolding an SDD workspace root yourself.

Create the directory only. Do not run `.codexspec/scripts/create-new-feature.sh`
or its PowerShell counterpart: those scripts create and switch a git branch, which
this command must never do. Creating a workspace changes no git state, so the
command is safe to run on whatever branch the user is already working on. That
restriction is about git side effects, not about writing: what the new directory
must contain from its first moment is set out below.

Every generated `spec.md` and `design.md` carries a `Slice:` header holding the
repo-relative path its content describes, written in the normalized form mode
resolution defines — no trailing slash, no `.` or `..` segment, never absolute.
This field is the whole baseline-lookup mechanism: there is no index file and the
directory name does not encode the path. Writing it unnormalized breaks the lookup
for a path the user spells differently next time, so normalize on the way in as
well as on the way out. State the recorded value in the closing summary so a later
mismatch is diagnosable.

Creating a workspace is one indivisible act: create the directory and immediately
write the artifact that identifies it — in generate mode a `spec.md` carrying the
`Slice:` header, in overview mode a `slices.md` — before scanning anything and
before writing any derived content. The lookup key and the mode marker therefore
exist from the workspace's first moment. Do not create the directory and defer
the header until the scan has something to say: that ordering opens a window in
which the workspace is invisible to the lookup above, so an interruption inside it
would leave the next run creating a second workspace for the same slice and
orphaning the first.

## Generate Mode

Scan the slice per the scan discipline below, writing as you go rather than
holding everything until the scan completes. Create the workspace as soon as the
slice is confirmed to have analyzable code, writing its `spec.md` with the `Slice:`
header as the creating act described above, then append to the artifacts
incrementally so an interrupted run leaves usable partial output that a re-run can
continue from. Append; never rewrite. Content already in an artifact stays as it
is, and the run continues after it. Three artifacts are produced:

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
proceeds so an interrupted run leaves usable partial output. Create the
`<id>-overview` workspace by writing its `slices.md` as the creating act described
above, so the workspace is identifiable as an overview from its first moment and
an interrupted survey can never be mistaken for a slice workspace. The workspace
contains exactly two artifacts:

- `design.md` — a thin architecture-level map: components, their responsibilities,
  and how they relate. Marked as inferred, scaled to complexity.
- `slices.md` — the candidate slice list. One row per slice: path, a one-line
  description, and a rough size or priority.

When the `<id>-overview` workspace already exists from an interrupted survey,
continue it under the resume rule mode resolution states: complete only what is
missing, and leave what is already written untouched.

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

`reconcile.md` is this command's own output and the one artifact the boundary
below allows it to rewrite wholesale, so a later reconcile of the same slice
regenerates it rather than appending to it. Regeneration replaces the previous
report: any adjudication the user recorded
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
- Never edits source, tests, or the baseline it reconciles against.
- Rewrites only what it wrote during the current run, and never without notice.
  Whatever a workspace already held when the run began belongs to the maintainer,
  whether it came from an interrupted earlier run or from corrections they made to
  that run's draft — you cannot tell the two apart, so treat both as theirs. A
  resumed draft is therefore appended to, never overwritten. Where existing content
  looks wrong or contradicts what the code now shows, report the discrepancy and
  leave the decision to the user rather than correcting it yourself. The one
  artifact this command regenerates wholesale is its own `reconcile.md`, and only
  behind the notice the report section above requires.
- Never applies a drift resolution, in either direction.

## Output Summary

Report the resolved mode and why, the slice and the workspace path, the recorded
`Slice:` value, the artifacts written, and what remains for the user to do. In
generate mode that is the confirmation action; in reconcile mode it is adjudicating
each open drift item. Distinguish deep-read areas from sampled ones, and never
claim coverage you did not achieve.
