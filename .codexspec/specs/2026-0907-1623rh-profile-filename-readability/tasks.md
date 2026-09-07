# Tasks: profile-filename-readability

<!--
Language: en (.codexspec/config.yml language.document)
Expands plan.md of feature 2026-0907-1623rh. Slug strings come from plan Decision 4.
-->

## 1. Author the convention in the maintainer sources

- [x] 1.1 Rewrite the naming rule in `internal/command_templates/sources/distill.md`: in the `id` bullet, replace the "heading and filename" unity wording with heading=id / filename=`<id>-<slug>.md`; state the slug rules (derived from the title, `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤50 chars, English rendering for non-ASCII titles, bare-`<id>.md` fallback when no meaningful slug is derivable); state the id-lookup boundary rule (a record's file is exactly `<id>.md` or `<id>-<slug>.md`; no other filename begins with `<id>` followed by `-` or `.`; uniqueness never depends on the slug); update the store-layout sentence ("one record per file") and the `add` operation's path pattern to the same form. — **Covers**: REQ-001, REQ-002, REQ-003, REQ-004; Plan: Phase 1 step 1 (Filename convention definition). *Verify deterministically: the stale-wording sweep in 3.1 step 3 returns only intended mentions.*
- [x] 1.2 Update the four worked examples in `internal/command_templates/sources/distill.md` to the Decision-4 filenames (heading and ids unchanged): `conventions/Con-2026-0809-2219gg-1-prefer-absolute-imports.md`, `pitfalls/P-2026-0810-1330ab-1-re-sub-string-replacement-corruption.md`, `strategies/S-2026-0813-1606fz-1-suspect-markdown-emphasis-first.md`, `runbooks/R-2026-0813-1143el-1-release-a-new-codexspec-version.md`. — **Covers**: REQ-001, REQ-005; Plan: Phase 1 step 2 (Worked examples). *Verified by 1.4's assertions after 2.1 renders.*
- [x] 1.3 Update the onboard format cross-note in `internal/command_templates/sources/onboard.md` (the sentence citing `conventions/<id>.md`, `constraints/<id>.md`) to the `<id>-<slug>.md` form. — **Covers**: REQ-005; Plan: Phase 1 step 3 (onboard.md format cross-note). *Verify deterministically: same sweep as 1.1.*
- [x] 1.4 [P] Strengthen the four example assertions in `tests/test_distill_template.py` (currently lines 49–50 and 142–143) from bare ids to the full new example filenames listed in 1.2. — **Covers**: REQ-005; Plan: Phase 1 step 4 (Worked examples pin, plan Decision 2).

  **Test Scenarios** (each maps one-to-one to a strengthened assertion in the existing pytest functions, validating 1.1–1.3's content):
  - TS-1: the distill template contains `conventions/Con-2026-0809-2219gg-1-prefer-absolute-imports.md`
  - TS-2: the distill template contains `pitfalls/P-2026-0810-1330ab-1-re-sub-string-replacement-corruption.md`
  - TS-3: the distill template contains `strategies/S-2026-0813-1606fz-1-suspect-markdown-emphasis-first.md`
  - TS-4: the distill template contains `runbooks/R-2026-0813-1143el-1-release-a-new-codexspec-version.md`

## 2. Propagate and document

- [x] 2.1 Render the opted-in sources: `uv run python internal/command_template_fragments.py --write`, then `uv run python internal/command_template_fragments.py --check-distribution` must exit 0. — **Covers**: REQ-005; Plan: Phase 1 step 5 (Distribution propagation).
- [x] 2.2 Sync the self-bootstrap artifacts: `uv tool install --force .` then `codexspec init --here --force --ai both`; inspect `git diff` and keep only the four expected derived copies (`.claude/commands/codexspec/distill.md`, `.claude/commands/codexspec/onboard.md`, `.agents/skills/codexspec-distill/SKILL.md`, `.agents/skills/codexspec-onboard/SKILL.md`), reverting anything else. — **Covers**: REQ-005; Plan: Phase 1 step 6 (Distribution propagation).
- [x] 2.3 [P] Update `CLAUDE.md` (Profile Consumption section, "the id also being the filename") to the id-plus-slug filename form. — **Covers**: REQ-001; Plan: Phase 2 step 1 (Repo CLAUDE.md store documentation). *Non-testable doc change; deterministic verification: the phrase no longer appears (`grep`), the new form does.*

## 3. Verify and commit

- [x] 3.1 Run the verification battery and commit the feature's own outputs as one commit (English message, no split). Commit scope — exactly: `internal/command_templates/sources/distill.md`, `internal/command_templates/sources/onboard.md`, `templates/commands/distill.md`, `templates/commands/onboard.md`, the four derived copies from 2.2, `tests/test_distill_template.py`, `CLAUDE.md`, and `.codexspec/specs/2026-0907-1623rh-profile-filename-readability/` (spec artifacts ship with the feature per repository convention). Explicitly EXCLUDE the six pre-existing profile-record changes in the working tree (`M .codexspec/profile/constraints/C-2026-0902-054178-1.md` and the five untracked `P-`/`R-`/`S-` records) — they predate this feature and keep their separate disposition; stage by path, never `git add -A`. Battery: (a) `uv run pytest` full suite green including TS-1…TS-4; (b) `--check-distribution` exit 0 with `git status --porcelain` identical before/after; (c) stale-wording sweep `grep -n '<id>.md' internal/command_templates/sources/distill.md internal/command_templates/sources/onboard.md` returns only intended mentions (the fallback rule and legacy-form references); (d) init idempotence: a second `codexspec init --here --force --ai both` produces no diff. — **Covers**: REQ-001…REQ-005; Plan: Phase 2 step 2 (Verification battery, plan Decision 3).

## Dependencies

```
1.1 -> 1.2 -> 2.1 -> 2.2 -> 3.1
      1.3 ----^            ^
1.4 [P] -------------------+  (edits tests; passes only after 2.1; validated in 3.1)
2.3 [P] -------------------+
```

1.4 depends on 1.2 for content agreement (the asserted strings must be the ones 1.2 writes) and is validated after 2.1. 2.3 is independent of group 1 and joins at 3.1.

## Coverage

| Plan Component / Requirement | Task(s) | Scenarios |
|---|---|---|
| Filename convention definition (REQ-001…004) | 1.1 | deterministic sweep in 3.1(c) |
| Worked examples (REQ-001, REQ-005) | 1.2, 1.4 | TS-1…TS-4 |
| onboard.md cross-note (REQ-005) | 1.3 | deterministic sweep in 3.1(c) |
| Distribution propagation (REQ-005) | 2.1, 2.2 | 3.1(b), 3.1(d) |
| Repo CLAUDE.md doc (REQ-001) | 2.3 | grep check in 2.3 |
| Verification battery + single commit (REQ-001…005) | 3.1 | (a)–(d) |

No unmapped tasks.
