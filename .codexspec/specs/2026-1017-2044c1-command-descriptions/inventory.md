# Command Behavior Inventory

The approved compact descriptions summarize the current public command bodies.
Section labels below identify the relevant instructions; prerequisite details and
full option syntax remain in those bodies and argument hints.

| Command | Source and relevant sections | Purpose and important distinction |
| --- | --- | --- |
| constitution | [Source](../../../internal/command_templates/sources/constitution.md): Input Mode Detection; Execution Flow | Project principles and consistency checks; dependent templates are not silently rewritten. |
| specify | [Source](../../../internal/command_templates/sources/specify.md): Goal; Discussion Rules; Stage Summary Confirmation | Discuss goals, scope and constraints; persist confirmed requirements, not a specification. |
| blueprint | [Source](../../../internal/command_templates/sources/blueprint.md): Goal; Allowed Work; Completion | Maintain confirmed multi-feature requirements and pending order for auto-dev. |
| generate-spec | [Source](../../../internal/command_templates/sources/generate-spec.md): Role; Required Output; Pre-Save Validation | Specify behavior, error handling and acceptance from confirmed requirements. |
| spec-to-design | [Source](../../../internal/command_templates/sources/spec-to-design.md): Role; Design Rules; Required Output | Define components, interfaces and technical decisions. |
| design-to-plan | [Source](../../../internal/command_templates/sources/design-to-plan.md): Role; Planning Rules; Required Output | Translate design into implementation sequence and verification. |
| plan-to-tasks | [Source](../../../internal/command_templates/sources/plan-to-tasks.md): Task Rules; Required Output | Create executable tasks, dependencies and verification; scenarios for testable tasks. |
| review-spec | [Source](../../../internal/command_templates/sources/review-spec.md): Review Passes; Report | Check requirement fidelity and acceptance quality before design. |
| review-design | [Source](../../../internal/command_templates/sources/review-design.md): Review Passes; Report | Check fidelity and feasibility before implementation planning. |
| review-plan | [Source](../../../internal/command_templates/sources/review-plan.md): Review Passes; Report | Check steps, order and coverage before task decomposition. |
| review-tasks | [Source](../../../internal/command_templates/sources/review-tasks.md): Review Passes; Report | Check coverage, dependencies and verification before implementation. |
| implement-tasks | [Source](../../../internal/command_templates/sources/implement-tasks.md): Instructions; Pre-Review Baseline; Final Code Review Loop | Implement tasks, run tests and independent review, repair verified issues. |
| auto-dev | [Source](../../../internal/command_templates/sources/auto-dev.md): Goal; Select Work; Resume and Stage Resolution; Autonomous Decisions, Repair and Commits | Develop confirmed blueprint items in document order through verified implementation and commits. |
| clarify | [Source](../../../internal/command_templates/sources/clarify.md): Clarification Priorities; Question Loop; Persistence Order | Resolve gaps and contradictions; update requirements first, then specification. |
| analyze | [Source](../../../internal/command_templates/sources/analyze.md): Operating Model; End-to-End Traceability; Remediation | Check artifact consistency and repair deterministic downstream defects without changing requirements. |
| checklist | [Source](../../../internal/command_templates/sources/checklist.md): Checklist Purpose; Generate Checklist; Prohibited Patterns | Check requirement quality, not implementation correctness. |
| tasks-to-issues | [Source](../../../internal/command_templates/sources/tasks-to-issues.md): Goal; Parse Tasks; Create Issues; Safety Constraints | Create remote GitHub issues with task files, dependencies and available acceptance criteria. |
| distill | [Source](../../../internal/command_templates/sources/distill.md): Operating Model; What distill captures; Vetting candidates | Capture reusable knowledge and review or consolidate existing records. |
| evolve | [Source](../../../internal/command_templates/sources/evolve.md): Selecting what to promote; Compiling the draft; Contribution mechanics | Promote vetted general knowledge into commands/skills; approval precedes upstream contribution. |
| onboard | [Source](../../../internal/command_templates/sources/onboard.md): Role and Operating Model; What onboard Extracts; Safety Gate | Extract conventions and explicit constraints; save constraints after user review. |
| reverse-spec | [Source](../../../internal/command_templates/sources/reverse-spec.md): Role and Operating Model; Mode Resolution; Generate, Overview and Reconcile modes | Recover architecture or module specification/design; reconcile against an existing confirmed baseline. |
| debug | [Source](../../../internal/command_templates/sources/debug.md): Role and Iron Law; Investigation Protocol; Completion | Reproduce and trace root cause before a minimal verified repair. |
| commit-staged | [Source](../../../internal/command_templates/sources/commit-staged.md): Parameter Check and Input Identity; Staging Boundary; Analysis | Use only staged changes; execute an authorized commit or preview with -p. |
| pr | [Source](../../../internal/command_templates/sources/pr.md): Git Context Collection; PR Title Generation; Section Generation; Output Modes | Generate branch-based PR/MR content and verification guidance. |
| release-notes | [Source](../../../internal/command_templates/sources/release-notes.md): Role; Forbidden Operations; CHANGELOG.md Maintenance; Release Body Generation | Update changelog and draft release notes without publishing. |
| review-code | [Source](../../../internal/command_templates/sources/review-code.md): Usage Hints; Role and Non-Negotiable Boundary; Mode Dispatch | Judge changes for merge readiness; --audit assesses existing code quality. |
| config | [Source](../../../internal/command_templates/sources/config.md): Parameter Check; Instructions; Worktree Isolation Setting | Configure languages and workflow options interactively; --view is read-only. |
| quick | [Source](../../../internal/command_templates/sources/quick.md): Scope Check; Compact Requirement Confirmation; Automated Flow | Confirm a bounded requirement, then automate the remaining specification-to-review workflow. |

Scope: the 28 registered public commands. Repository-only maintenance skills are
excluded. The exact approved English and Chinese wording is recorded in
[description-proposals.md](description-proposals.md).
