# Code Review Report — blueprint / auto-dev (complete feature, defect gate)

## Meta

- **Target selector**: `default` (complete merge-base-to-worktree delta)
- **Base**: `origin/main` @ `4cb40cb2e6b29b0a4d27050aa27953c60906aad6` (HEAD == merge base; all work uncommitted: 56 modified + 27 untracked = 83 entries incl. this report)
- **Feature context**: `.codexspec/specs/2026-0829-2159yg-blueprint-auto-dev/` (requirements/spec/design/plan/tasks all readable)
- **Resolver**: `.codexspec/scripts/review-context.sh` (schema 1, status ok)
- **Review date**: 2026-08-30/31

## Review rounds

| Round | Context | Target fingerprint | Result |
|---|---|---|---|
| 1 | Primary (isolated) + command-execution/filesystem specialist (isolated) | `sha256:d9c3256a…d97638` (81 entries) | FAIL — 10 admitted findings (P2×2, P3×8) |
| 2 | Fresh isolated reviewer (no prior findings supplied) | `sha256:200aff01…1747` (82 entries, post-repair) | FAIL — 3 newly admitted findings (P2×1, P3×2); all round-1 repairs independently confirmed effective |
| 3 (final) | Coordinator repair verification + full deterministic gates | `sha256:21bd698d…281c` (83 entries, includes this report) | **PASS** — round-3 detail below |

Round 3 (coordinator verification of the round-2 repairs) found and fixed one additional defect in
the repair itself: the first non-blocking `acquire` implementation called
`fcntl.flock(fd, LOCK_NB)` without `LOCK_EX`, which macOS rejects with `EBADF` (a lock type is
required). Corrected to `LOCK_EX | LOCK_NB`, with busy classification limited to
`EAGAIN`/`EWOULDBLOCK`/`EACCES` (any other errno fails closed with the raw error instead of being
misreported as `already_running`). The guard-contention test was updated to pin the new
immediate-failure semantics required by REQ-018. Diagnostic probes that had repeated the same
`LOCK_NB`-alone mistake briefly suggested an environment problem; probes using correct flags
(`LOCK_EX | LOCK_NB`) show the host behaves normally, and no environment condition remains.

## Round 1 findings (all repaired, regression tests added)

| ID | P | Location | Defect | Repair |
|---|---|---|---|---|
| F1-1 | P2 | `automation.py _conflict_paths` | `git diff --name-only` C-quotes non-ASCII paths (`core.quotePath`) → resolution staging gate could never match | `-c core.quotePath=false … -z`, split on NUL; test with `需求文档.md` |
| F1-2 | P2 | `automation.py prepare_sync_verification` | `git diff --check` conflated leftover markers with `core.whitespace` errors → legitimate resolutions permanently rejected | disable whitespace classes, keep marker detection (empirically verified); tests both directions |
| F1-3 | P3 | `_rollback_sync` / `_recover_merge_state` | rollback completion judged by porcelain incl. untracked → `merge-owner.json` wedge; recovery dead-ended at `needs_resolution` with empty conflict list | tracked-only dirty predicate (`--untracked-files=no`); deterministic rollback + record clear; recovery returns `none` |
| F1-4 | P3 | `_atomic_bytes` | mkstemp 0600 leaked onto replaced blueprint | preserve existing mode, default 0644 (`os.fchmod`); test |
| F1-5 | P3 | `GitRunner` | no subprocess timeout; git-write lock held across fetch → hung remote wedged repo | shared `_run_git_with_timeout` (600 s) incl. env-discovery site → `git_command_timeout`; test |
| F1-6 | P3 | `apply_and_commit` | byte-identical "applied" op failed at `git commit` (nothing to commit) as transport error | content-equality short-circuit → applied, no commit; test |
| F1-7 | P3 | `sync_default` | fetch stderr (may embed remote-URL credentials) copied verbatim into `fetch_warning` | `_redact_url_credentials`; test with hostile URL |
| F1-8 | P3 | temp lifecycle | orphaned `.codexspec/.blueprint.md.*` temp permanently tripped `workspace_not_clean` | `_sweep_stale_blueprint_temporaries` in apply + sync; test |
| F1-9 | P3 | `blueprint.py _apply` move | self-reference branch unreachable (pop before lookup) → wrong code `reference_not_found` | self-reference checked before pop; test asserts `rejected/self_reference` |
| F1-10 | P3 | CLAUDE.md | command tables stale (11 core) vs shipped 13 core / 27 total | tables updated (13 core, both rows), feature section added |

Round-1 non-admitted observations (recorded, no repair): coordination dir name divergence from design Decision 3; `GIT_CONFIG_KEY_n` not stripped (outside stated threat model); repo hooks run on blueprint commits (fail closed); activity-based PID-free ownership is a documented design trade-off (design C7 / Decision 3).

## Round 2 findings (all repaired, regression tests added)

| ID | P | Location | Defect | Repair |
|---|---|---|---|---|
| F2-1 | P2 | `FileLock.__enter__` (Windows branch) | `msvcrt.LK_LOCK` retries only ~10×1 s then raises → Windows lost the documented wait-and-retry contract while a fetch/merge (≤600 s) holds the lock | blocking Windows branch now retries indefinitely (0.1 s), matching POSIX flock; POSIX non-blocking branch classifies only EAGAIN/EWOULDBLOCK/EACCES as busy (see round 3) |
| F2-2 | P3 | `AutoDevOwnership.acquire` + CLI | busy check ran AFTER two blocking lock acquisitions → a second auto-dev could block for the whole mutation instead of "exit immediately" (REQ-018) | `acquire` now takes the ownership lock non-blocking (`FileLockBusyError` → `already_running` immediately); CLI acquires ownership BEFORE `ensure_dedicated_workspace`; test asserts immediate busy failure under a held `guard()` |
| F2-3 | P3 | `blueprint.py _insert_feature_id` / `parse` | `str.splitlines()` splits on U+2028/U+2029/U+0085/\\v/\\f while every validation regex is `\n`-only → confirmed requirements bodies containing those characters were silently rewritten | tokenize on `"\n"` only; test asserts U+2028 survives append + parse round-trip |

Round-2 confirmed-good (fresh reviewer, independent): lock order (git-write → blueprint-modification → ownership, no inversion), protocol classification order and exact response shapes, `show-blueprint` read-only byte-exactness, env sanitization + redaction coverage, recovery state machine, path validation (`--literal-pathspecs`, blueprint-path exclusion, pathspec magic), registration counts 13 core / 27 total in installer + tests + CLAUDE.md + AGENTS.md + 8 READMEs + 16 docs files, 8×113 translation key parity, derived-copy body equality for all 7 commands (both `.claude` and `.agents`, modulo the documented generator substitutions).

## Findings

None outstanding after repair (round-3 coordinator verification).

## Requirements Coverage

- **complete** — feature target with all confirmed artifacts readable; REQ-001…REQ-024 and DEC-001…DEC-018 assessed against the implementation with no unauthorized intent drift; all scenarios T001-S01…T012 verified by mapped tests (see tasks.md T013 evidence).

## Verification Summary

| Command | Outcome |
|---|---|
| `uv run ruff check src/ tests/` | all checks passed (final state) |
| `uv run pytest` (full suite) | 1325 passed / 50 skipped at round-1→2 boundary; final-state full-suite run recorded in the T013 evidence block below |
| `git diff --check` | clean |
| Focused suites T001–T012 (`tests/test_blueprint*.py`, `tests/test_automation_git.py`, `tests/test_auto_dev_*.py`, `tests/test_sdd_workflow_templates.py`, `tests/commands/test_installer.py`, `tests/test_cli*.py`, `tests/test_codex_integration.py`, `tests/test_init_compliance.py`) | all pass |
| Translation completeness | 19 new keys × 8 languages, zero missing/extra (full catalogs 113 keys × 8) |
| Documentation sweep | `blueprint` present in 8/8 READMEs, 8/8 `docs/*/user-guide/commands.md`, 8/8 `docs/*/reference/cli.md`; fixed branch `codexspec/auto-dev` and worktree basename match `automation.py` constants in all 8 reference docs |
| Package inspection (`uv build` + wheel/sdist member check) | wheel ships only `scripts/bash` + `scripts/powershell` under `scripts/`; `templates/commands/blueprint.md` + `auto-dev.md` included; sdist contains no `docs/`, `tests/`, `internal/`, `scripts/python` |
| Derived-copy sync | byte-equal bodies for `.claude/commands/codexspec/*.md` (7/7); `.agents/skills/*/SKILL.md` differ only by the generator's documented substitutions — now pinned by `TestDerivedCopySyncInvariant` |
| Empirical git probes | `-c core.whitespace=…` keeps marker detection while accepting trailing whitespace; `quotePath=false -z` returns raw bytes; both fixed behaviors pinned by tests |

Final-state gate evidence: `uv run ruff check src/ tests/` all checks passed; `uv run pytest`
**1327 passed / 50 skipped (exit 0)**; `git diff --check` clean; all focused T001–T012 suites green.

## Coverage Gaps

Non-blocking, recorded for future rounds:

- CG-1: Windows `msvcrt` branch is `# pragma: no cover`; no Windows CI exercises `FileLock` contention semantics (F2-1's fix is untestable on POSIX CI).
- CG-2: `show-blueprint` fallback diagnostics for unmapped codes and missing git binary are untranslated by design (English `unknown` fallback) and unpinned by tests.
- CG-3: auto-dev ownership with a silent period longer than `AUTO_DEV_STALE_AFTER_SECONDS` mid-stage is a documented trade-off without a boundary test.
- CG-4: packaging regression guard asserts resolvers and `review-code.md` only (env-gated `CODEXSPEC_DIST_DIR`); the two new templates are covered by the manual boundary inspection and `force-include` semantics but not by an automated archive assertion.
- CG-5: `_blueprint-helper apply --ensure`, invalid-UTF-8 blueprint inspect, and `_recover` at a root-commit HEAD are traced fail-closed by hand but unpinned.

<review-code-result>
{
  "schema_version": "2",
  "mode": "defect",
  "verdict": "PASS",
  "target": {
    "selector": "default",
    "fingerprint": "sha256:21bd698d7ecd20d641b8bacdc4df92fb502e2aaf0f78d9e2b8e9010ac2b8281c",
    "complete_feature": true,
    "empty": false,
    "base_ref": "origin/main",
    "merge_base_sha": "4cb40cb2e6b29b0a4d27050aa27953c60906aad6",
    "commit_sha": null,
    "parent_sha": null,
    "inventory_count": 83
  },
  "requirements_coverage": {
    "status": "complete",
    "feature": ".codexspec/specs/2026-0829-2159yg-blueprint-auto-dev"
  },
  "verification": {
    "status": "complete",
    "commands": [
      "uv run ruff check src/ tests/",
      "uv run pytest",
      "git diff --check",
      "uv run pytest tests/test_blueprint.py tests/test_blueprint_store.py tests/test_blueprint_cli.py tests/test_blueprint_template.py tests/test_automation_git.py tests/test_auto_dev_ownership.py tests/test_auto_dev_git.py tests/test_auto_dev_template.py tests/test_sdd_workflow_templates.py tests/commands/test_installer.py tests/test_cli.py tests/test_cli_i18n.py tests/test_codex_integration.py tests/test_init_compliance.py",
      "uv build + wheel/sdist member inspection",
      "translation completeness 8x113",
      "derived-copy sync invariant"
    ]
  },
  "findings": [],
  "finding_counts": {"P0": 0, "P1": 0, "P2": 0, "P3": 0},
  "review_coverage": {
    "contracts": [
      {"id": "C-001", "statement": "Blueprint mutations persist as one atomic file replacement plus one blueprint-only commit under git-write -> blueprint-modification lock order, journaled for deterministic or fail-closed recovery of every interrupt window; byte-identical operations apply without a commit.", "sources": ["REQ-011", "NFR-001", "design C4"], "producers": ["BlueprintStore.apply_and_commit", "_recover", "_restore_old", "_atomic_bytes"], "propagation": ["recovery journal -> every later helper call"], "consumers": ["_blueprint-helper apply", "_auto-dev-helper acquire/sync-default"], "entry_surfaces": ["codexspec _blueprint-helper apply"], "scenarios": ["applied", "conflict", "crash windows", "unknown record fail-closed", "no-op applied without commit", "mode preservation"], "evidence": ["automation.py store paths read in full", "tests/test_blueprint_store.py incl. mode/no-op regression tests"], "status": "complete"},
      {"id": "C-002", "statement": "A second auto-dev acquire reports busy immediately without waiting behind any lock; ownership is a random fencing token with renewal, stale reclaim, and fail-closed old tokens.", "sources": ["REQ-018", "design C7/Decision 3"], "producers": ["AutoDevOwnership.acquire/_acquire_locked", "auto_dev_helper CLI ordering"], "propagation": ["token -> every mutation"], "consumers": ["_auto-dev-helper *"], "entry_surfaces": ["codexspec _auto-dev-helper acquire"], "scenarios": ["busy under held guard", "stale reclaim", "concurrent CLI acquire exactly one owner", "wrong token lost_ownership"], "evidence": ["non-blocking acquire + CLI reorder", "test_acquire_reports_busy_immediately_while_owner_lock_is_held", "tests/test_auto_dev_ownership.py", "tests/test_blueprint_cli.py"], "status": "complete"},
      {"id": "C-003", "statement": "Cross-process locks block indefinitely on POSIX and Windows alike; non-blocking acquisition raises a dedicated busy error.", "sources": ["design C8 wait-and-retry", "REQ-018"], "producers": ["FileLock"], "propagation": ["FileLockBusyError -> already_running"], "consumers": ["all lock users"], "entry_surfaces": ["all helper commands"], "scenarios": ["POSIX flock blocking + EBADF-tolerant", "Windows LK_LOCK retry loop", "LK_NBLCK/flock NB busy"], "evidence": ["FileLock implementation reviewed on both branches", "POSIX paths exercised by suite", "Windows branch code-reviewed (no Windows CI - see CG-1)"], "status": "complete"},
      {"id": "C-004", "statement": "Protocol responses classify strictly invalid_request -> conflict -> rejected -> applied with exact key sets; the requirements body is preserved byte-exactly apart from CRLF normalization and the inserted Feature ID line.", "sources": ["REQ-004", "REQ-006", "REQ-007", "REQ-008", "REQ-009", "REQ-010", "NFR-002"], "producers": ["blueprint.py protocol"], "propagation": ["one JSON response per request"], "consumers": ["blueprint/auto-dev templates"], "entry_surfaces": ["codexspec _blueprint-helper apply"], "scenarios": ["invalid shapes", "conflict precedence", "protected targets", "self_reference", "unicode line separators preserved"], "evidence": ["tests/test_blueprint.py 36 tests incl. self_reference and U+2028 regressions"], "status": "complete"},
      {"id": "C-005", "statement": "Synchronization merges are fenced, gated on the exact complete conflict-path list (quotePath-safe) and a marker-only check (whitespace classes disabled), and always end verified-merged or restored to pre-merge HEAD with tracked-state verification.", "sources": ["REQ-019", "REQ-020", "REQ-021", "REQ-022", "design C8"], "producers": ["AutoDevGit sync/prepare/continue/abort/recover/rollback", "_conflict_paths", "_tracked_changes_present"], "propagation": ["merge-owner.json -> blocked blueprint writes and feature commits"], "consumers": ["auto-dev template", "BlueprintStore"], "entry_surfaces": ["codexspec _auto-dev-helper sync-*"], "scenarios": ["conflict/verify/abort/recover", "non-ASCII paths", "trailing whitespace accepted, markers rejected", "untracked preserved, wedge impossible"], "evidence": ["tests/test_auto_dev_git.py incl. five regression tests", "empirical git flag probes"], "status": "complete"},
      {"id": "C-006", "statement": "All git subprocesses run through one environment-sanitizing, timeout-bounded runner; fetch failures are redacted non-blocking warnings; hung subprocesses raise git_command_timeout.", "sources": ["REQ-003", "REQ-020", "REQ-021", "NFR-001"], "producers": ["GitRunner", "_run_git_with_timeout", "_redact_url_credentials"], "propagation": ["fetch_warning in sync responses", "AutomationError codes"], "consumers": ["ensure/store/AutoDevGit"], "entry_surfaces": ["all helpers + show-blueprint"], "scenarios": ["hostile env vars", "600s timeout", "credential redaction", "fetch retry"], "evidence": ["tests/test_automation_git.py incl. timeout + hostile-env regression tests", "tests/test_auto_dev_git.py redaction test"], "status": "complete"},
      {"id": "C-007", "statement": "show-blueprint is read-only and lock-free, byte-exact on stdout, with translated per-check stderr diagnostics and non-zero exit on failure.", "sources": ["REQ-023", "REQ-024", "NFR-004", "design C11/Decision 7"], "producers": ["show_blueprint CLI"], "propagation": ["bytes -> stdout", "diagnostics -> stderr"], "consumers": ["users/scripts"], "entry_surfaces": ["codexspec show-blueprint"], "scenarios": ["exact bytes", "missing branch/worktree/file/not-a-repo", "no mutation"], "evidence": ["tests/test_blueprint_cli.py show-blueprint suite", "translator keys 8/8 languages"], "status": "complete"},
      {"id": "C-008", "statement": "Registration and every catalog surface move in lockstep (13 core / 27 total); derived copies stay in sync with templates; hidden helpers stay undocumented; docs in 8 languages describe the same public surface.", "sources": ["REQ-001", "REQ-002", "REQ-023", "NFR-004", "design C12", "constitution Self-bootstrap rule"], "producers": ["installer metadata", "codex.py skill renderer", "translator"], "propagation": ["templates -> .claude/.agents -> README/docs/CLAUDE.md/AGENTS.md"], "consumers": ["init/list-commands", "Claude/Codex sessions"], "entry_surfaces": ["codexspec init", "codexspec list-commands"], "scenarios": ["counts asserted in tests", "CLAUDE.md tables updated to 13 core", "derived-copy invariant test", "8x8 doc sweeps", "hidden helpers absent from docs"], "evidence": ["TestDerivedCopySyncInvariant", "installer/cli/codex-integration suites", "rg sweeps per language"], "status": "complete"},
      {"id": "C-009", "statement": "Run-local delegation: under the delegation marker each chain stage skips only its Auto-Next section and returns its result to auto-dev; direct invocations are unchanged.", "sources": ["REQ-013", "REQ-014", "NFR-003", "design C10/Decision 6"], "producers": ["five stage templates", "auto-dev template"], "propagation": ["invocation context -> stage behavior"], "consumers": ["auto-dev run", "direct users"], "entry_surfaces": ["the five chain commands"], "scenarios": ["uniform delegation clause", "direct behavior preserved", "implement-tasks terminal semantics intact"], "evidence": ["test_every_stage_has_uniform_delegation_and_direct_compatibility", "test_sdd_workflow_templates.py"], "status": "complete"}
    ],
    "partitions": [
      {"id": "P-001", "scope": "blueprint.py document model + protocol", "owner": "primary", "contract_ids": ["C-004"], "evidence": ["full module read across rounds 1-2", "protocol suite green"], "status": "complete"},
      {"id": "P-002", "scope": "automation.py runner/locks/store/ownership/sync", "owner": "primary", "contract_ids": ["C-001", "C-002", "C-003", "C-005", "C-006"], "evidence": ["full module read across rounds 1-2", "13 repair-round tests green", "specialist call-site enumeration"], "status": "complete"},
      {"id": "P-003", "scope": "CLI adapters (hidden helpers, show-blueprint, translator)", "owner": "primary", "contract_ids": ["C-002", "C-006", "C-007"], "evidence": ["delta read", "CLI suites green incl. reordering"], "status": "complete"},
      {"id": "P-004", "scope": "distribution, registration, translations, docs", "owner": "primary", "contract_ids": ["C-008"], "evidence": ["installer/codex/translator suites green", "8-language sweeps", "CLAUDE.md updated"], "status": "complete"},
      {"id": "P-005", "scope": "templates + stage delegation", "owner": "primary", "contract_ids": ["C-009"], "evidence": ["template contract tests green", "derived-copy invariant green"], "status": "complete"},
      {"id": "P-006", "scope": "confirmed artifacts + tasks coverage", "owner": "primary", "contract_ids": ["C-001", "C-009"], "evidence": ["artifacts read; T001-T012 [x]; scenario-to-test mapping recorded", "no intent drift found by either round"], "status": "complete"}
    ],
    "variant_searches": [
      {"root_cause_id": "RC-QUOTE", "finding_ids": ["F1-1"], "cause": "parsing git path output without quotePath/-z controls", "scope": "all git-output-to-path consumers in the change", "methods": ["grep + consumer classification"], "checked_locations": ["worktree list porcelain", "rev-parse", "diff-tree", "status porcelain", "diff --name-only"], "evidence": ["exactly one affected producer"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-CHECK", "finding_ids": ["F1-2"], "cause": "single content gate conflating markers with whitespace errors", "scope": "all content-validation gates in the change", "methods": ["grep for diff/--check call sites"], "checked_locations": ["prepare_sync_verification", "feature-commit validation"], "evidence": ["single gate"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-DIRTY", "finding_ids": ["F1-3"], "cause": "rollback completion judged by full porcelain incl. untracked", "scope": "every status --porcelain consumer and merge-owner record consumer", "methods": ["call-site enumeration"], "checked_locations": ["sync gate", "recover_merge_state", "rollback", "tests"], "evidence": ["two same-root-cause sites fixed together"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-ATOMIC", "finding_ids": ["F1-4", "F1-8"], "cause": "temp-file lifecycle ignoring mode and orphan recovery", "scope": "every file-writing site in the change", "methods": ["grep mkstemp/write_text + recovery-path enumeration"], "checked_locations": ["_atomic_bytes sole writer", "coordination records", "recovery records"], "evidence": ["single write primitive; sweep covers the one unrecovered artifact class"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-TIMEOUT", "finding_ids": ["F1-5"], "cause": "no subprocess duration bound anywhere", "scope": "all subprocess sites in the change", "methods": ["grep subprocess.run/Popen"], "checked_locations": ["GitRunner.run", "env discovery", "pre-existing unrelated CLI sites (out of scope)"], "evidence": ["both in-scope sites wrapped by one helper"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-NOOP", "finding_ids": ["F1-6"], "cause": "unguarded applied-to-commit transition", "scope": "all apply_operation persistence callers", "methods": ["caller enumeration"], "checked_locations": ["apply_and_commit", "commit_feature (caller-controlled paths)"], "evidence": ["single blueprint commit site fixed"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-REDACT", "finding_ids": ["F1-7"], "cause": "verbatim stderr passthrough for the one credential-capable command (fetch)", "scope": "all stderr/stdout passthrough into messages", "methods": ["grep .stderr/.stdout in exception paths"], "checked_locations": ["check=True raises (not credential-bearing)", "fetch_warning"], "evidence": ["single leaking channel fixed"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-SELFREF", "finding_ids": ["F1-9"], "cause": "pop-before-lookup ordering in move", "scope": "all move validation branches", "methods": ["control-flow read"], "checked_locations": ["blueprint.py move path", "_validate_payload move branch"], "evidence": ["single-site defect"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-LOCKWIN", "finding_ids": ["F2-1"], "cause": "cross-platform lock abstraction with non-equivalent blocking semantics", "scope": "every lock acquisition and every >10s critical section", "methods": ["grep msvcrt/fcntl/FileLock/_git_write_lock + critical-section timing"], "checked_locations": ["single lock primitive", "7 git-write holders", "5 ownership holders"], "evidence": ["one fix location covers all callers"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-BUSY", "finding_ids": ["F2-2"], "cause": "busy-state detection placed after blocking acquisition", "scope": "all entry points whose contract requires immediate failure", "methods": ["contract classification of every FileLock acquisition"], "checked_locations": ["acquire (fixed)", "ensure-before-acquire (reordered)", "blueprint paths (documented to wait, correct)", "show-blueprint (no locks, correct)"], "evidence": ["one defective entry surface"], "reason": null, "status": "complete"},
      {"root_cause_id": "RC-SPLITLINES", "finding_ids": ["F2-3"], "cause": "str.splitlines() unicode line-boundary set vs the \\n-only document model", "scope": "all line splitting and line-anchored matching in the protocol", "methods": ["grep splitlines/re.MULTILINE"], "checked_locations": ["parse", "_insert_feature_id (fixed)", "regex guards (already \\n-only)"], "evidence": ["single reachable defect site"], "reason": null, "status": "complete"}
    ]
  },
  "follow_up": {
    "received": [],
    "required": [
      {"id": "FU-1", "origin_fingerprint": "sha256:21bd698d7ecd20d641b8bacdc4df92fb502e2aaf0f78d9e2b8e9010ac2b8281c", "source_ids": ["CG-1"], "statement": "When Windows CI exists, exercise FileLock contention semantics (blocking wait and non-blocking busy) on the msvcrt branch.", "status": "open", "evidence": "recorded as non-blocking coverage gap CG-1"},
      {"id": "FU-2", "origin_fingerprint": "sha256:21bd698d7ecd20d641b8bacdc4df92fb502e2aaf0f78d9e2b8e9010ac2b8281c", "source_ids": ["CG-4"], "statement": "Extend the archive-contents test to assert the blueprint and auto-dev templates ship in wheel/sdist when CODEXSPEC_DIST_DIR is provided.", "status": "open", "evidence": "recorded as non-blocking coverage gap CG-4"}
    ]
  },
  "coverage_gaps": [
    {"id": "CG-1", "scope": "Windows FileLock branch untested (no Windows CI)", "impact": "msvcrt semantics cannot regress-detect on POSIX CI", "blocking": false},
    {"id": "CG-2", "scope": "show-blueprint fallback diagnostics unpinned", "impact": "fallback path traced fail-closed but untested", "blocking": false},
    {"id": "CG-3", "scope": ">stale_after ownership boundary untested", "impact": "documented trade-off, untested boundary", "blocking": false},
    {"id": "CG-4", "scope": "new templates absent from automated archive assertions", "impact": "manual inspection + force-include semantics cover current state", "blocking": false},
    {"id": "CG-5", "scope": "helper edge inputs (--ensure+apply, invalid UTF-8 inspect, root-commit recover) unpinned", "impact": "hand-traced fail-closed", "blocking": false}
  ],
  "coverage_gap_count": 5,
  "review_context": "isolated",
  "reviewers": {
    "primary": "complete",
    "specialists": [
      {"profile": "command/process execution + filesystem/path handling + secrets/injection (round 1)", "state": "complete"},
      {"profile": "full-profile fresh reviewer (round 2, isolated)", "state": "complete"}
    ]
  }
}
</review-code-result>
