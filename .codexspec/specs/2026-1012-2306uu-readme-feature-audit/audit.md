# English README Capability Audit

**Status**: All inventory items assessed; README repairs and coverage checks complete.
**Baseline**: `a0ab7fa52e1a3c68b5a7a3e66915a17b65a1039e`
**Scope**: English README.md only; current functionality, including missing descriptions.
**Authority**: [requirements.md](requirements.md), NEED-001 through NEED-004 and CON-001.

## Method and Evidence

The inventory starts from [CLI implementation](../../../src/codexspec/__init__.py) public registrations,
[src/codexspec/commands/installer.py](../../../src/codexspec/commands/installer.py) command metadata,
[templates/commands/](../../../templates/commands/) command contracts, and shared runtime source.
The baseline README is the committed file at the hash above. Assessments check
purpose, suitable use, entry point, important defaults, and reference links,
rather than treating any mention of a name as complete documentation.

Relevant confirmed history establishes the design stage
(`2026-0812-2114vj`), blueprint/auto-dev (`2026-0829-2159yg`),
HTML distill review (`2026-0927-2310d6`), worktrees (`2026-1003-204985`),
review convergence (`2026-1008-1952ti`), planning rename
(`2026-1009-2352qc`), staged commits (`2026-1010-21225w`),
maintenance/review standards (`2026-1011-105126`), and historical recall
(`2026-1011-1611mh`). Newer requirements supplement or explicitly revise
earlier decisions. Current source verifies the implemented behavior.

## Public CLI Inventory

Each row's source is the public command registration and implementation in
[CLI implementation](../../../src/codexspec/__init__.py).

| Command | Baseline Coverage | Evidence of Coverage or Issue | README Resolution |
|---------|-------------------|-------------------------------|---------------------------|
| `codexspec init` | Incomplete | Options present; force description too broad and generated tree outdated | [Installation](../../../README.md#installation) |
| `codexspec check` | Accurate | Public table states tool checking | [Available Commands](../../../README.md#available-commands) |
| `codexspec version` | Incorrect | Public subcommand exists, but baseline examples use unsupported codexspec --version | [Available Commands](../../../README.md#available-commands) |
| `codexspec config` | Incomplete | Missing --decided-by; switches/defaults incompletely explained | [Configuration and Internationalization](../../../README.md#configuration-and-internationalization) |
| `codexspec list-commands` | Absent | Missing from CLI table | [Available Commands](../../../README.md#available-commands) |
| `codexspec show-blueprint` | Absent | Missing from CLI table | [Shared Blueprint and Autonomous Development](../../../README.md#shared-blueprint-and-autonomous-development) |

## Distributed Command Inventory

All 28 registered commands are accounted for. The linked command template is
the current behavior evidence for that row.

| Command / Source | Baseline Coverage | Evidence of Coverage or Issue | README Resolution |
|------------------|-------------------|-------------------------------|---------------------------|
| [constitution](../../../templates/commands/constitution.md) | Accurate | Project principles and confirmation | [Core Workflow](../../../README.md#core-workflow) |
| [specify](../../../templates/commands/specify.md) | Accurate | Persistent confirmed requirements and final summary gate | [Core Workflow](../../../README.md#core-workflow) |
| [blueprint](../../../templates/commands/blueprint.md) | Insufficient | Only a command-table row; shared queue and editing rules absent | [Shared Blueprint and Autonomous Development](../../../README.md#shared-blueprint-and-autonomous-development) |
| [generate-spec](../../../templates/commands/generate-spec.md) | Accurate | Requirements compilation and auto-review described | [Core Workflow](../../../README.md#core-workflow) |
| [spec-to-design](../../../templates/commands/spec-to-design.md) | Inconsistent | Workflow includes it; opening feature summaries omit design | [Core Workflow](../../../README.md#core-workflow) |
| [design-to-plan](../../../templates/commands/design-to-plan.md) | Accurate | Renamed planning entry present; responsibility retained | [Core Workflow](../../../README.md#core-workflow) |
| [plan-to-tasks](../../../templates/commands/plan-to-tasks.md) | Insufficient | Automatic analyze invocation and design traceability underexplained | [Core Workflow](../../../README.md#core-workflow) |
| [review-spec](../../../templates/commands/review-spec.md) | Accurate | Available manually and in automatic generation reviews | [Review and Debugging](../../../README.md#review-and-debugging) |
| [review-design](../../../templates/commands/review-design.md) | Inconsistent | Present in workflow; comparison still claims only three reviews | [Review and Debugging](../../../README.md#review-and-debugging) |
| [review-plan](../../../templates/commands/review-plan.md) | Accurate | Available manually and in automatic generation reviews | [Review and Debugging](../../../README.md#review-and-debugging) |
| [review-tasks](../../../templates/commands/review-tasks.md) | Accurate | Available manually and in automatic generation reviews | [Review and Debugging](../../../README.md#review-and-debugging) |
| [implement-tasks](../../../templates/commands/implement-tasks.md) | Insufficient | Full final review and conditional maintenance underexplained | [Review and Debugging](../../../README.md#review-and-debugging) |
| [auto-dev](../../../templates/commands/auto-dev.md) | Insufficient | Only name/short purpose; invocation and independence from auto_next absent | [Shared Blueprint and Autonomous Development](../../../README.md#shared-blueprint-and-autonomous-development) |
| [clarify](../../../templates/commands/clarify.md) | Accurate | Four categories, at most five questions, requirements-first persistence | [Core Workflow](../../../README.md#core-workflow) |
| [analyze](../../../templates/commands/analyze.md) | Insufficient | Describes detection; omits design, directed fixes and automatic invocation | [Core Workflow](../../../README.md#core-workflow) |
| [checklist](../../../templates/commands/checklist.md) | Insufficient | Row exists; requirements-quality purpose and usage entry absent | [Review and Debugging](../../../README.md#review-and-debugging) |
| [tasks-to-issues](../../../templates/commands/tasks-to-issues.md) | Insufficient | Row exists; tasks prerequisite and target-repository boundary absent | [Git Workflow](../../../README.md#git-workflow) |
| [distill](../../../templates/commands/distill.md) | Insufficient | Row exists; local knowledge use, manual review and automation absent | [Project Knowledge](../../../README.md#project-knowledge) |
| [evolve](../../../templates/commands/evolve.md) | Insufficient | Row exists; vetted-only gate and contribution approval absent | [Project Knowledge](../../../README.md#project-knowledge) |
| [onboard](../../../templates/commands/onboard.md) | Insufficient | Row exists; code-read-only, candidate and narrow constraints behavior absent | [Work with Existing Code](../../../README.md#work-with-existing-code) |
| [reverse-spec](../../../templates/commands/reverse-spec.md) | Insufficient | Row exists; overview/generate/reconcile and confirmation boundary absent | [Work with Existing Code](../../../README.md#work-with-existing-code) |
| [debug](../../../templates/commands/debug.md) | Insufficient | Row exists; practical invocation and repeated-fix escalation absent | [Review and Debugging](../../../README.md#review-and-debugging) |
| [commit-staged](../../../templates/commands/commit-staged.md) | Misplaced | Accurate staged-only guidance; CLI-free runtime paragraph under License | [Git Workflow](../../../README.md#git-workflow) |
| [pr](../../../templates/commands/pr.md) | Insufficient | Row exists; GitHub/GitLab description generation and optional spec use absent | [Git Workflow](../../../README.md#git-workflow) uses a spec file path or feature-name/prefix lookup |
| [release-notes](../../../templates/commands/release-notes.md) | Insufficient | Row exists; Unreleased default and no tagging/publishing boundary absent | [Git Workflow](../../../README.md#git-workflow) |
| [review-code](../../../templates/commands/review-code.md) | Insufficient | Mode row exists; review applicability, incremental/final acceptance and decision mode absent | [Review and Debugging](../../../README.md#review-and-debugging) |
| [config](../../../templates/commands/config.md) | Incomplete | Plugin guide describes only two language settings; newer settings omitted | [Configuration and Internationalization](../../../README.md#configuration-and-internationalization) |
| [quick](../../../templates/commands/quick.md) | Absent | No command entry anywhere in README | [Small Changes with Quick](../../../README.md#small-changes-with-quick) |

## Shared Mechanisms and Whole-Document Issues

| Capability / Source | Baseline Coverage | Evidence of Coverage or Issue | README Resolution |
|---------------------|-------------------|-------------------------------|---------------------------|
| Claude/Codex integration — [AI integration selection](../../../src/codexspec/integrations/__init__.py) | Inconsistent | Opening and comparison describe Claude only despite both integrations | [30-Second Quick Start](../../../README.md#30-second-quick-start) |
| Installation and refresh — [CLI implementation](../../../src/codexspec/__init__.py) | Incomplete | Upgrade updates CLI without explaining project command/resource refresh | [Installation](../../../README.md#installation) |
| Requirements authority and design — [templates/commands/spec-to-design.md](../../../templates/commands/spec-to-design.md) | Inconsistent | Opening pipeline and initialized tree omit design/requirements | [Core Workflow](../../../README.md#core-workflow) |
| Ordinary and maintenance worktrees — [src/codexspec/worktrees.py](../../../src/codexspec/worktrees.py) | Misplaced/incomplete | Late Acknowledgements paragraph; defaults, checkout-local effects and retention underexplained | [Worktree Development](../../../README.md#worktree-development) |
| Language dimensions, standard CLI codes and plugin configuration — [templates/commands/config.md](../../../templates/commands/config.md), `src/codexspec/i18n.py` | Incorrect/incomplete | Standard-code list uses pt-BR instead of pt; plugin instructions mention only output and commit despite four controls | [Configuration and Internationalization](../../../README.md#configuration-and-internationalization) |
| Automatic stage advancement — [templates/commands/specify.md](../../../templates/commands/specify.md) | Insufficient | Switch listed without default, pass gates, terminal stage or effect on manual confirmation | [Workflow Automation](../../../README.md#workflow-automation) |
| Automatic knowledge capture — [templates/commands/distill.md](../../../templates/commands/distill.md) | Insufficient | Switch listed without ambient/mid-task/wrap-up paths, default, de-duplication or no-write early exit | [Project Knowledge](../../../README.md#project-knowledge) |
| Review standards and repair convergence — [templates/review-code/change-review.md](../../../templates/review-code/change-review.md) | Insufficient | Mode row lacks applicable shared standards and complete final acceptance | [Review and Debugging](../../../README.md#review-and-debugging) |
| Maintenance and scenario decision policies — [CLI implementation](../../../src/codexspec/__init__.py) | Incomplete | Maintenance paragraph exists; review.decided_by/--decided-by absent | [Configuration and Internationalization](../../../README.md#configuration-and-internationalization) |
| Profile local consumption and categories — [src/codexspec/profile.py](../../../src/codexspec/profile.py) | Absent | No explanation of ambient reads, six categories or candidate/vetted distinction | [Project Knowledge](../../../README.md#project-knowledge) |
| Local manual knowledge review — [src/codexspec/distill_review/server.py](../../../src/codexspec/distill_review/server.py) | Absent | No browser review, staged Apply all, recoverable draft, or text fallback introduction | [Project Knowledge](../../../README.md#project-knowledge) |
| Historical requirements recall — [src/codexspec/specs_context.py](../../../src/codexspec/specs_context.py) | Absent | No reuse of confirmed earlier decisions or latest-user-decision precedence | [Reusing Historical Decisions](../../../README.md#reusing-historical-decisions) |
| Plugin startup and runtime prerequisites — [src/codexspec/commit_guidance.py](../../../src/codexspec/commit_guidance.py) | Misplaced/incomplete | Startup guidance appended under Acknowledgements; CLI-free limits under License | [Plugin Marketplace Installation](../../../README.md#plugin-marketplace-installation) |
| Extension materials versus runtime support — [CLI implementation](../../../src/codexspec/__init__.py) | Incorrect | Claims implemented plugin architecture; source has no extension loader or management CLI | [Extension Materials](../../../README.md#extension-materials) |
| Development dependency extra — [pyproject.toml](../../../pyproject.toml) | Incorrect | uv sync --dev does not request the dev optional-dependency extra | [Development](../../../README.md#development) |
| Version-check syntax — [CLI implementation](../../../src/codexspec/__init__.py) | Incorrect | Baseline examples use unsupported `codexspec --version`; actual CLI rejects it | [CLI Installation](../../../README.md#cli-installation) uses `codexspec version` |
| Windows troubleshooting link — [docs/en/WINDOWS-TROUBLESHOOTING.md](../../../docs/en/WINDOWS-TROUBLESHOOTING.md) | Broken | README links missing docs/WINDOWS-TROUBLESHOOTING.md | [Installation](../../../README.md#installation) |
| Comparison and navigation — [src/codexspec/commands/installer.py](../../../src/codexspec/commands/installer.py) | Inconsistent | Three-review count and Claude-only claims; feature paragraphs under License/Acknowledgements | [Why Choose CodexSpec](../../../README.md#why-choose-codexspec) |

## Evidence Boundaries

- The desktop installation guide added on 2026-10-12 is useful setup material;
  it is not evidence that descriptions of project capabilities are current.
- The extension guide and manifest examples exist, but the shipped CLI/package
  has no extension-manifest discovery, hook dispatcher, or extension management
  commands. The README must describe these as materials, not automatic loading.
- Quick's current command contract invokes generate-spec → design-to-plan →
  plan-to-tasks → implement-tasks. This audit does not change that implementation
  or assert a separate Quick design invocation.
- Existing detailed guides have their own stale tables. They are navigational
  references; source and confirmed history remain the evidence for this audit.
- First-time TTY language selection depends on explicit language options and
  existing configuration, not `--force`. Current init control flow and confirmed
  language-init decisions distinguish this selection from migration, update,
  and constitution-compliance confirmations.
- Installed capture guidance covers ordinary conversations, non-SDD fixes and
  mid-task knowledge events independently of the wrap-up toggle. Overlapping
  triggers process new material only, with existing-profile de-duplication and
  no-write early exit when nothing reusable remains.
- The standard Portuguese CLI identifier is `pt`; `pt-BR` identifies localized
  documentation and translation resources. The two surfaces are distinct.
- `pr --spec` resolves a feature directory name or prefix to spec.md. A supplied
  path names the specification file directly, so examples using a returned
  feature-directory path include `/spec.md`.
- Other-language READMEs and reference-site repairs are separate work.

## Completion

All 6 public CLI commands, 28 distributed commands, and 18 shared mechanisms or
whole-document issues have an assessment and a current README resolution.
Previously accurate descriptions are retained or restated consistently;
incorrect, absent, insufficient, and misplaced descriptions are repaired.
The desktop installation guide is preserved verbatim.

The unsupported third-party comparison table is replaced by a table of
CodexSpec's own verified capabilities; the spec-kit acknowledgement is retained.
No third-party product-support claims are inferred from this repository.

Coverage, local-link/anchor, option, rendering, and product-scope checks are
performed with a temporary checker outside the repository. See
[verification.md](verification.md) for final commands/results. The final
complete-feature review result is kept in the external review state store.
