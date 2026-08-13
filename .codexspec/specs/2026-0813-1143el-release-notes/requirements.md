# Confirmed Requirements: release-notes

<!--
Language: Maintain this document in the language specified in .codexspec/config.yml (document: en).
This file is the authoritative, persistent record of user-confirmed intent.
Do not copy the full conversation. Keep only confirmed decisions and short evidence
quotes needed to resolve later interpretation disputes.
-->

**Feature ID**: `2026-0813-1143el`
**Status**: Confirmed — ready for `/codexspec:generate-spec`
**Last Confirmed**: 2026-08-13

## Authority Rules

- Only entries with `Status: confirmed` are binding downstream inputs.
- `open` entries MUST NOT be converted into confirmed product requirements.
- Replaced entries remain in this file with `Status: superseded` and a link to the replacement.
- AI inferences must be labeled as assumptions and require user confirmation before becoming binding.

## Summary

A new **distributed** slash command `/codexspec:release-notes` for **end-user projects** that
summarizes "what changed since the last release" straight from git, producing two layered
outputs: a developer-facing **CHANGELOG.md** entry (Keep a Changelog format) and a derived
**user-facing Release body**. It is a standalone, immediate-use git-family command (sibling of
`commit-staged` / `pr`), **agnostic to how the user releases** (no assumption of a version
scheme, CI, platform, or a `publish.sh`).

## Needs

### NEED-001: Distributed release-notes command for user projects

- **Status**: confirmed
- **Statement**: Provide `/codexspec:release-notes`, installed into end-user projects by
  `codexspec init`, that reads git history and summarizes "what changed since the last release."
  It fills the gap where projects have no CHANGELOG and release notes are written manually and
  inconsistently.
- **Rationale**: Low-risk, high-frequency quick win that fits the existing git-family commands;
  borrowed from the roadmap's gstack "Release Manager".
- **User Evidence**: "codexspec这个命令不是给自身使用，而是给用户使用的，用户的项目里可没有
  publish.sh脚本，我们并不知道用户如何发布版本"
- **Confirmed At**: 2026-08-13

### NEED-002: Double-layer output (changelog then user-facing notes)

- **Status**: confirmed
- **Statement**: Generate two layers. (a) A developer **CHANGELOG entry** organized into Keep a
  Changelog categories (`Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security`).
  (b) A **user-facing Release body** derived from it, benefit-oriented ("You can now…", plain
  language, not implementation detail). Internal / contributor-only changes are placed in a
  separate `### For contributors` subsection rather than the user-facing list.
- **Rationale**: Industry best practice and the gstack pattern both write the changelog first and
  extract user-facing release notes from it; one command serves both audiences.
- **User Evidence**: "双层:先changelog后提炼"
- **Confirmed At**: 2026-08-13

### NEED-003: Maintain CHANGELOG.md safely (never clobber)

- **Status**: confirmed
- **Statement**: Maintain a `CHANGELOG.md` in the user's repo. If absent, create it with the
  standard Keep a Changelog header. Insert a new version / `Unreleased` section. **Never** rewrite,
  reorder, or delete existing entries — only precise insertion via `Edit`, never a `Write` that
  overwrites the file.
- **Rationale**: gstack recorded a real incident where an agent clobbered existing CHANGELOG
  entries; this is a hard safety rule. Aligns with the project's forbidden-operations discipline in
  `commit-staged`.
- **User Evidence**: "维护CHANGELOG.md+输出Release正文"
- **Confirmed At**: 2026-08-13

### NEED-004: Emit the Release body as platform-agnostic text

- **Status**: confirmed
- **Statement**: Output the user-facing Release body as plain markdown to the terminal by default,
  or to a file via `--output <file>`. It is platform-agnostic text the user pastes wherever they
  release (GitHub / GitLab / other). The command does not itself publish it.
- **Rationale**: We cannot assume the user's release platform; text output keeps the command
  universal and safe.
- **Confirmed At**: 2026-08-13

### NEED-005: Input = git range by default, opt-in `--spec` enrichment

- **Status**: confirmed
- **Statement**: Default input is the commits + diff over a git range (see NEED-007). Opt-in
  `--spec <feature>` pulls the feature's `tasks.md` / `spec.md` to enrich the "why", mirroring
  `pr.md`'s opt-in `--spec` pattern.
- **User Evidence**: "默认 git 范围 + 可选 --spec"
- **Confirmed At**: 2026-08-13

### NEED-006: Version handling — Unreleased default, `--version` override, guarded advisory

- **Status**: confirmed
- **Statement**:
  - Default the changelog section to `## [Unreleased]` (Keep a Changelog convention for
    accumulating changes before a version is assigned).
  - `--version X.Y.Z` is a first-class explicit override: when given, stamp that version (with an
    ISO `YYYY-MM-DD` date) and **short-circuit any inference** — print no suggestion.
  - When `--version` is not given, apply a **guarded advisory**: only when the project is detected
    to use semver **and** conventional commits, print a console-only "suggested next version" with
    its reasoning and an explicit "override with `--version`" note; otherwise stay silent.
  - The command **never** writes a version number into the file on its own (only `Unreleased`, or a
    user-provided `--version`).
- **Rationale**: The command is release-process-agnostic; a confidently-wrong bump on a non-semver
  project is worse than none. The guard captures the friendliness of a suggestion without
  re-crossing the "do not own versioning" boundary.
- **User Evidence**: "守卫式 advisory 是否也可以支持 --version来支持用户直接自己指定版本号，省去
  我们推断的麻烦"; challenge that prompted the guard: "明明额外给出一个仅提示的推荐版本号看起来更
  智能更友好？"
- **Confirmed At**: 2026-08-13

### NEED-007: Range selection — tag-first with fallback chain and explicit override

- **Status**: confirmed
- **Statement**: Default range is `latest tag..HEAD`. If the repo has no reachable tag, fall back
  to "after the last version recorded in CHANGELOG.md"; if that is unavailable (e.g. first run with
  no CHANGELOG), take the full history. `--from <ref>` / `--to <ref>` always override. Use
  `--no-merges`. Handle an empty range and detached HEAD gracefully (inform, do not hard-error),
  mirroring `pr.md`.
- **Rationale**: Tags are the closest thing to a universal, release-process-agnostic "last release"
  marker; the fallback chain covers no-tag projects; explicit override covers everything else.
- **User Evidence**: "tag 优先 + 回退链 + 显式覆盖"
- **Confirmed At**: 2026-08-13

### NEED-008: Completeness cross-check; do not hard-require conventional commits

- **Status**: confirmed
- **Statement**: Every commit in the selected range must map to at least one changelog bullet
  (cross-check the written entry against the commit list, per the gstack pattern). Conventional
  commits are used when present, but are **not** required — when absent, infer categories and
  wording from the diff and commit subjects (the `commit-staged` / `pr` "diff is the source of
  truth" approach).
- **Rationale**: User projects may not follow conventional commits; the command must degrade
  gracefully instead of producing an empty or partial changelog.
- **Confirmed At**: 2026-08-13

## Constraints

### CON-001: Self-bootstrap and lockstep distribution updates

- **Status**: confirmed
- **Statement**: Author the command in `templates/commands/release-notes.md` only. The derived
  `.claude/commands/codexspec/` and `.agents/skills/` forms are regenerated via publish → init and
  are never hand-edited. Registering the command requires lockstep updates: a
  `get_commands_metadata()` entry in `installer.py`, its docstring total, the inline category count
  comment, the command-count assertions in both `tests/commands/test_installer.py` and
  `tests/test_cli.py`, and a row in all 8 `README*.md` files.
- **User Evidence**: Project profile record `Con-2026-0811-1418yq-1`.

### CON-002: House conventions for command templates

- **Status**: confirmed
- **Statement**: Template is written in English with a `## Language Preference` section and a
  `## Constitution Compliance` section; `allowed-tools` are read-only git operations (plus the file
  edits needed to maintain CHANGELOG.md). Generated content language follows `language.commit`,
  falling back to `language.output`, then English — as in `pr.md`.

### CON-003: No AI attribution in generated content

- **Status**: confirmed
- **Statement**: Generated CHANGELOG entries and Release bodies must never contain AI attribution
  (no `Co-Authored-By`, "Generated with", robot emoji, or tool references).

### CON-004: Generator semantics — never mutate git state

- **Status**: confirmed
- **Statement**: The command is a generator. It must never modify the git staging area and never
  create a commit (same discipline as `commit-staged` / `pr`). Its only file mutation is the
  safe insertion into `CHANGELOG.md` per NEED-003.

### CON-005: Release-process-agnostic

- **Status**: confirmed
- **Statement**: Assume nothing about how the user releases — no `publish.sh`, no specific CI, no
  specific hosting platform, no specific versioning scheme (semver / CalVer / date tags all
  possible). Every behavior degrades gracefully when an assumption does not hold.
- **User Evidence**: "用户的项目里可没有publish.sh脚本，我们并不知道用户如何发布版本"

### CON-006: New command needs no translation-catalog entry

- **Status**: confirmed
- **Statement**: A brand-new distributed command does not need an entry in
  `templates/translations/*.json`; it installs with English frontmatter, matching the
  `debug` / `distill` / `evolve` / `config` precedent.
- **User Evidence**: Project profile record `Con-2026-0812-2114vj-1`.

## Decisions

### DEC-001: Command name is `release-notes`

- **Status**: confirmed
- **Decision**: Name the command `release-notes`.
- **Alternatives Rejected**: `changelog` (accurately names only the file layer, undersells the
  user-facing Release body, and users who do not keep a CHANGELOG might skip it); `release`
  (misleadingly implies performing the release, contradicting OUT-001).
- **Reason**: `release-notes` is the superset/umbrella term covering both layers, binds to the
  "release" event as the most intuitive trigger, has no false-negative discovery, and matches the
  codexspec "name = deliverable" family (`pr`, `tasks-to-issues`).
- **User Evidence**: "我更顾虑如何让用户直观知道命令的用途，以及命令名能够准确直观表达命令的用途";
  selected "release-notes".

### DEC-002: Guarded advisory for version suggestion

- **Status**: confirmed
- **Decision**: Use a guarded advisory (NEED-006) rather than pure `Unreleased` (no suggestion) or
  an unconditional advisory (always suggest).
- **Alternatives Rejected**: Unconditional advisory — would emit misleading bumps on
  CalVer / non-conventional projects. Pure Unreleased — foregoes a friendly, safe suggestion where
  it is well-founded.
- **Reason**: Captures friendliness where the signal is trustworthy without owning versioning or
  misleading non-semver projects.

### DEC-003: Standalone git-family command, not an SDD pipeline stage

- **Status**: confirmed
- **Decision**: `release-notes` is a standalone, immediate-use command; it does not occupy a
  position in the `auto_next` SDD chain.
- **Reason**: It is a delivery-time generator (like `pr`), not a requirements-traceable pipeline
  stage. Matches the roadmap's "独立命令" recommendation for release-notes.

### DEC-004: tag-first range with fallback chain

- **Status**: confirmed
- **Decision**: Resolve the default range tag-first, then CHANGELOG-last-version, then full history
  (NEED-007).
- **Alternatives Rejected**: CHANGELOG-last-version first — more self-consistent with the file we
  append to, but the version-string → commit mapping is more fragile (an `Unreleased`-only prior
  entry has no commit anchor).
- **Reason**: Tags are the most universal release marker; the mapping is more robust.

### DEC-005: `--version` is a first-class override that short-circuits inference

- **Status**: confirmed
- **Decision**: When `--version X.Y.Z` is provided, stamp it and skip all inference / suggestion.
- **Reason**: Lets users who know their version bypass detection entirely.
- **User Evidence**: "支持 --version来支持用户直接自己指定版本号，省去我们推断的麻烦"

### DEC-006: No Automatic Distillation hook

- **Status**: confirmed (AI assumption, not vetoed)
- **Decision**: Do not add a `## Automatic Distillation` section to this command.
- **Reason**: It is a formatting/generation command, not an interaction that produces reusable
  cross-feature knowledge; unlike `implement-tasks` / `commit-staged` / `pr` it has no knowledge to
  distill.

### DEC-007: `For contributors` split heuristic

- **Status**: confirmed (AI assumption, not vetoed)
- **Decision**: Classify user-facing vs contributor changes by: user-facing = `feat` / `fix` /
  `perf` and any user-visible change; contributors = `chore` / `refactor` / `test` / `ci` /
  `build` / internal-only docs. When conventional-commit types are absent, infer visibility from
  the diff.
- **Reason**: A deterministic default the spec can refine; keeps the user-facing list free of
  internal noise.

### DEC-008: Single generic markdown Release body

- **Status**: confirmed (AI assumption, not vetoed)
- **Decision**: Produce one generic markdown Release body; do not build per-platform
  (GitHub / GitLab) variants the way `pr.md` does.
- **Reason**: Platform-agnostic text is sufficient and simpler; the user pastes it anywhere.

## Out of Scope

### OUT-001: Does not decide/own versioning or publish

- **Status**: confirmed
- **Statement**: The command does not decide or own version bumps, does not auto-write a version
  into any file, and does not tag, publish, or create a GitHub/GitLab release via `gh` or an API.
- **Reason**: Release-process-agnostic (CON-005); versioning and publishing belong to whatever
  mechanism the user's project already uses.
- **User Evidence**: "我们并不知道用户如何发布版本"

### OUT-002: Does not mutate git staging or create commits

- **Status**: confirmed
- **Statement**: No `git add`, `git commit`, or any staging/history mutation.
- **Reason**: Generator semantics (CON-004).

### OUT-003: No monorepo / path-scoping in this iteration

- **Status**: confirmed
- **Statement**: Scoping the changelog to a subdirectory / package within a monorepo is not
  included.
- **Reason**: Keep the first iteration small; avoid over-design.

### OUT-004: Not an SDD pipeline stage

- **Status**: confirmed
- **Statement**: `release-notes` does not read `requirements.md` as an authority and is not part of
  the auto_next chain. `--spec` is enrichment only.
- **Reason**: DEC-003.

## Open Questions

None remaining. All discovery questions raised this session (command name, auto-distill hook,
contributor split heuristic, single vs per-platform Release body, version handling, range fallback)
were resolved and folded into the entries above. Nothing blocks specification generation.

## Confirmation Log

### Session 2026-08-13

- **Summary Presented**: Grounded design briefing (gstack `document-release` + `ship/changelog`;
  git-cliff / release-please / semantic-release; Keep a Changelog; developer-vs-user audience
  split) plus codexspec's own gap (no CHANGELOG, GitHub Releases stale at v0.6.0, `publish.sh`
  emits no notes). Four framing axes decided (output = double-layer; persistence = maintain
  CHANGELOG.md + emit Release body; input = git range + opt-in `--spec`; versioning boundary
  reframed to release-process-agnostic). Follow-ups resolved: guarded advisory + first-class
  `--version`; tag-first range with fallback chain; command name `release-notes`.
- **User Confirmation**: "确认 + auto_next 直接全链开建" (final stage summary confirmed; auto_next to
  proceed).
- **Entries Confirmed**: NEED-001..008, CON-001..006, DEC-001..008, OUT-001..004.
