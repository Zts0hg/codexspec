# Verification: Codex Documentation Maintenance

## Selected baseline and scope

All checks used the ready feature workspace
`/Users/xiaoming/code/codexspec-codexspec-worktrees/2026-1013-1133ii-codex-docs-maintenance`,
branch `2026-1013-1133ii-codex-docs-maintenance`, based on
bdab1f3705daf5df6d5b11efdf17651f2b9efc94. The interpreter is the worktree's
uv-managed CPython 3.11.13 with frozen dev/docs extras. Editable imports resolve
to this checkout rather than another checkout or Conda.

The change covers both repo-only host entries, shared instructions, maintainer
generation/inventory/verification helpers, paired self-bootstrap checks, focused
tests, maintainer guidance and seven root translations. Public registrations,
templates, init behavior and package allowlists are unchanged. English README.md
retains SHA-256 `200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363`.
The main checkout is clean; no historical feature or site translation was edited.

This records the green implementation baseline before the separate mandatory
isolated complete-feature review. Gate records and the caller loop ledger remain
outside Git in the shared review cache; this baseline does not claim a gate verdict.

## Actual checks

| Check | Outcome |
|-------|---------|
| New helper behavior tests | 87 passed, 4 skipped; 91 collected |
| New and directly related fragment tests | 206 passed, 5 skipped; including README contracts: 222 passed, 5 skipped |
| Complete suite, every one of 86 test files | 2,434 passed, 58 skipped; 2,492 collected/accounted; all three groups exit 0 |
| Ruff over src, tests and affected internal Python | Passed; project-pinned Ruff 0.9.10 format --check passes all five selected Python files |
| Native maintainer --check | Exit 0; changed [] |
| Legacy direct --check-distribution | Exit 0 |
| Seven-language README mechanics | Exit 0; seven selected pairs, pinned English source, errors [] |
| Complete semantic review | Strict PASS for every pair; [actual assessments and repairs](translation-review.md) |
| Declared Markdownlint 0.42.0 | Passed over all 31 changed Markdown files, including this report and the candidate profile record |
| Whitespace and selected output containment | Passed |
| Package build and archive exclusion | Build exit 0; no internal/.agents/.claude/.codexspec files or either maintainer command in wheel/sdist |
| Source/scope check | English unchanged, seven existing target resources, permitted file scope, main checkout clean |
| Enumerated scenario self-check | TS-001–TS-012 have real tests asserting their expected behavior; no uncovered scenario |

Executable checks, from the selected workspace:

```text
.venv/bin/python -B -m pytest tests/test_maintainer_doc_tools.py tests/test_command_template_fragments.py -q -p no:cacheprovider --basetemp <physical-external-fixtures>
.venv/bin/ruff check src tests internal/doc_translation.py internal/maintainer_doc_skills.py internal/command_template_fragments.py
.venv/bin/python -B -m internal.maintainer_doc_skills --check
.venv/bin/python -B internal/command_template_fragments.py --check-distribution
.venv/bin/python -B -m internal.doc_translation verify --readme --lang all
npx --offline --yes markdownlint-cli@0.42.0 <all-changed-Markdown-paths>
git diff --check
uv build --out-dir <physical-external-build-directory>
```

The variable arguments above describe destination roles; the exact executed
paths/commands for longer runs are retained in the external manifests below.
Markdown paths are the union of HEAD-different and non-ignored untracked files,
filtered only for this formatting check. Final defect review uses the complete
unfiltered target.

## Complete-suite evidence and repaired failures

The full-suite runner collected the entire tests tree, then partitioned its 86
files into three disjoint groups. Their union equals the complete file set;
all 2,492 collected tests are accounted for. Pytest caches were disabled and
all fixtures/logs were placed under physical /private/tmp directories outside
Git. No group was skipped or stopped early.

Final manifest:
`/private/tmp/codexspec-docs-maintenance-suite-71bp4l49/manifest.json`.

| Group | Passed | Skipped | Exit |
|-------|--------|---------|------|
| 0 | 947 | 14 | 0 |
| 1 | 610 | 13 | 0 |
| 2 | 877 | 31 | 0 |
| Total | 2,434 | 58 | 0 |

An earlier complete run yielded 2,374 passed, 54 skipped and three failures.
Its manifest remains at
`/private/tmp/codexspec-docs-maintenance-suite-5h_14syt/manifest.json`.
The failures were de/es/fr cases in
tests/test_review_code_docs.py::test_readme_summary_describes_gate_not_default_scorecard:
their translated review-code rows used synonyms instead of the established
Defekt-Gate, puerta de defectos and contrôle de défauts terms. The outputs were
aligned with existing localized guide terminology; the Portuguese sibling's
gate de defeitos was preserved as well. Existing tests were not weakened.
Focused documentation contracts then passed all 16 cases, and the complete
86-file suite was rerun to the green result above.

Actual prose assessment also repaired upstream-coverage narrowing and
deterministic-correction/commit/negative-clause wording. Those documentation
repairs used source comparison, mechanics and lint; no artificial code test was
created for a prose defect. Both host workflows share the instruction improvement
to consult relevant existing documentation contracts in addition to the glossary.

## Scenario coverage independently checked

The implementer read the test bodies and their outcome assertions; test names
or an AST assertion count alone were not accepted as evidence. The following
functions are in tests/test_maintainer_doc_tools.py; initial parametrization gave
30 cases, and verified-gate regressions below bring the current total to 91.

| Scenario | Covering test(s) | Expected outcome actually asserted |
|----------|------------------|------------------------------------|
| TS-001 | test_ts001_native_entries_use_existing_renderer_and_source_changes | Two valid named frontmatters, Codex prefix/argument conversion, source edit makes output stale, check preserves bytes, write regenerates only changed output |
| TS-002 | test_ts002_missing_check_does_not_create_output | Missing check raises without creating a skill tree; generation then passes check with no changes |
| TS-003 | test_ts003_writer_preflights_all_outputs_before_any_mutation | Five unsafe-output/parent variants raise before a stale first output or outside destination is altered |
| TS-004 | test_ts004_public_install_stays_public_only; test_ts004_self_bootstrap_verifies_maintainer_pair | Fresh installed set is 28 without either internal skill; missing/stale native pair and unknown extra each raise; current pair passes |
| TS-005 | test_ts005_readme_all_and_alias_mapping | Exactly seven root outputs, correct zh-CN/pt-BR normalization and root source detection, source hashes present |
| TS-006 | test_ts006_site_relative_mapping_and_incremental | Site file/directory relative mapping, docs/zh versus README naming, explicit timestamps skip current and include newer/missing pairs |
| TS-007 | test_ts007_invalid_and_duplicate_languages_are_read_only | Five invalid/duplicate selectors raise and preserve every source/target byte |
| TS-008 | test_ts008_invalid_selected_paths_preserve_bytes | Missing, source/target redirect and parent-escape variants refuse and preserve selected/outside bytes |
| TS-009 | test_ts009_valid_translated_structure_and_tokens | Valid translated Unicode headings/anchors, examples, inline tokens, tables and links produce no mechanics error |
| TS-010 | test_ts010_technical_and_structure_drift_is_detected | Changed fence, missing inline token, heading removal and malformed table each produce their corresponding diagnostic |
| TS-011 | test_ts011_missing_links_and_duplicate_anchors_fail; test_ts011_unicode_duplicate_anchor_passes | Missing file/Unicode anchor/wrong duplicate suffix fail; valid duplicate -1 succeeds |
| TS-012 | test_ts012_cli_inventory_verify_and_dry_run_do_not_write | Both CLI main paths return valid selected JSON and preserve all fixture files without persistent output |

Initial tests were written before the modules. Running them first produced the
expected import failures for the absent inventory module and then the absent
maintainer renderer. After implementation all 30 passed. A root self-bootstrap
failure then demonstrated the paired entry requirement before T004 generated
the two derived skills; generation resolved it without relaxing the check.

## Package and output evidence

Build output:
`/private/tmp/codexspec-docs-maintenance-package-c2hjryjg/`.

| Archive | Entries | Maintainer files found |
|---------|---------|-----------------------|
| codexspec-0.7.24-py3-none-any.whl | 133 | None |
| codexspec-0.7.24.tar.gz | 136 | None |

Archive members were inspected directly, not inferred from allowlists.
Both maintainer skills are generated from the two authored Claude entries using
the existing Codex renderer; check mode does not repair stale/missing output.
The distribution gate rejects unknown additions rather than loosely allowing
all Codex skill extras. Shared instructions remain maintainer-only.

All seven actual translation pairs retain complete source sections, 25 examples,
229 inline technical spans and 16 tables, localized self-anchors and eight-language
navigation; external URLs and intentional English guide references are preserved.
Those mechanics complement, rather than replace, the per-language semantic evidence.

## Verified gate repairs and current baseline

The first isolated complete review is preserved externally at
sha256:1b293b5f0e2c7ea9b7fd8ae19aec3fe280e0ae2899e1b0381931ad3631df91fa.
Its validated schema-3 result was FAIL with F-FS-001–003, all P2, complete
coverage and no maintenance advice. The implementer independently reproduced
all three before changing code. The seven translated README bytes were not
implicated and remain frozen at translation-review.md's final hashes.

Root-cause debugging compared rejected absolute/--readme controls with the
accepted relative fallback and traced inventory to its checked-path and target
consumers. Regressions then observed 15 failures and one positive-control pass,
with the expected missing-error/path-serialization assertions. Repairs recognize
explicit README selection before fallback, validate source/parent identity before
site shorthand, require a regular root README, and validate all selected sources
before constructing targets. Targets overlapping source file identities, including
case aliases, or sharing a generated destination are rejected before writes.
Source/target JSON paths use portable forward slashes; a Windows relative-path
representation regression exposed the previous backslash output.

The added actual asserting tests cover TS-006 and TS-008 without inventing a new
product requirement:

| Scenario | Additional covering functions | Verified outcome |
|----------|-------------------------------|------------------|
| TS-008 | test_ts008_explicit_source_identity_is_checked_before_fallback | Six missing/dangling/parent/explicit-path cases refuse through API and CLI with unchanged bytes; valid existing shorthand remains covered by original TS-006 |
| TS-008 | test_ts008_readme_directory_is_never_a_readme_source | Flag/relative/absolute forms reject a directory source as non-regular without outputs |
| TS-008 | test_ts008_targets_cannot_overlap_any_selected_source | File/directory/cross-pair/case-alias collisions fail, including incremental selection and CLI; case-alias case skips only on case-sensitive filesystems |
| TS-006 | test_ts006_custom_directory_cannot_map_multiple_sources_to_one_target | Duplicate target mappings refuse with all input bytes preserved |
| TS-006 | test_ts006_disjoint_custom_source_remains_supported | Supported custom English input with another-language target remains correctly mapped and read-only |
| TS-006 | test_ts006_inventory_paths_are_portable_across_path_representations | Windows relative-path representation yields canonical source/target resource strings while fixture I/O remains physical/local |

After the first repair set, targeted tests passed 181 cases with one skip and
all 86 files passed 2,393 cases with 54 skips. That manifest remains archived
under suite-sm6ubovx. The initial green baseline (2,377/54) remains archived
under suite-q0dfcqkr. Neither substitutes for the current full baseline.

## Filesystem identity and compatibility regression evidence

The next isolated incremental result, preserved externally at
sha256:e95dd7558a8775b99a721eb0ac9723c3a2f8a797792dea1d675b5eae9aa8d76e,
was a validated FAIL with one P2 source-classification defect. Current macOS
samefile probes independently confirmed that case aliases of the root README
selected site targets, and English-directory aliases lost nested paths.
Missing-source and root-directory aliases also bypassed canonical-form refusal.

The implementer traced accepted aliases and their working canonical controls
to lexical source classification and prefix comparisons. New physical-fixture
regressions produced 14 failures, two control passes and two platform skips;
three additional English-directory-entry-case regressions failed as expected.
The repair recovers actual source-entry spellings after path safety checks,
classifies the root README by physical file identity, and recognizes the English
parent by device/inode identity before generating its full relative target.
Existing source-target identity checks remain ahead of incremental omission.

A compatibility check also observed two expected failures when a case-sensitive
namespace was modeled: folded reserved names suppressed valid English-page
shorthand. The final repair reserves those aliases only when a real docs/DOCS
identity comparison establishes case folding. Canonical README/docs forms remain
reserved. Real source/target I/O verifies the modeled shorthand outcomes; no Linux
execution is claimed. Two actual distinct-name controls remain platform-skipped
on this case-insensitive macOS volume. Full-site/custom-source compatibility and
read-only byte assertions remain covered.

| Scenario | Additional covering functions | Expected outcome asserted |
|----------|-------------------------------|---------------------------|
| TS-005 | test_ts005_filesystem_equivalent_readme_sources_keep_root_mapping | Relative/absolute/mixed-case root aliases retain identical pinned root pairs through API/CLI |
| TS-006 | test_ts006_filesystem_equivalent_english_sources_keep_relative_hierarchy; test_ts006_english_directory_entry_case_retains_identity_mapping | Equivalent explicit files/directories and physical directory-entry casing retain the complete guide/page destination hierarchy |
| TS-008 | test_ts008_missing_reserved_source_spellings_never_select_alternate_inputs; test_ts008_filesystem_equivalent_readme_directory_is_rejected | Missing reserved aliases cannot select another input; root directory aliases are rejected before outputs, with unchanged bytes |
| TS-006 | test_ts006_case_sensitive_distinct_readme_file_keeps_custom_mapping; test_ts006_case_sensitive_distinct_english_directory_keeps_custom_mapping | Genuinely distinct files/directories retain custom mapping and documented shorthand; these two controls skip on this volume |
| TS-006 | test_ts006_case_sensitive_namespace_preserves_english_page_shorthand | A modeled case-sensitive namespace retains real English-page shorthand inputs, hashes and relative targets; fixture bytes stay unchanged |

After the namespace repair, targeted tests passed 202 cases with 3 skips, and
the complete 86-file suite passed 2,414 cases with 56 skips (2,470 accounted).
That manifest remains archived under suite-lqlclfts; it does not substitute for
the current baseline below. Ruff, native/distribution,
all seven README mechanics, Markdown lint and whitespace checks pass. Seven
translation hashes remain frozen. Package-included bytes remain unchanged.

A completed intermediate 2,412/56 run is archived under suite-x1k9vifn before
the final shorthand compatibility cases. A preceding run under suite-a4xcglbg
was explicitly withdrawn with SIGINT while checking a newly reproduced sibling;
it is incomplete and never used as a success baseline or code-failure claim.

The transferable filesystem-identity lesson is recorded as candidate knowledge
in .codexspec/profile/pitfalls/P-2026-1013-1133ii-1-filesystem-identity-before-source-classification.md.
It carries actual outcome evidence and explicit platform limits, without human
endorsement or a new hard policy. All retained neutral gate obligations require
fresh independent verification. This document records the current green baseline;
it does not declare the subsequent mandatory complete-review verdict.

## Absolute checkout-prefix admission and pinned formatting

The next isolated incremental review at
sha256:18b69994fe0bd513a16ee9fbc6c7008c24178eca1e7cd0d581a0342f25b38cfc
was a validated FAIL with one P2 valid-source rejection and one P3 formatting
failure. All seven actual translations were independently assessed with no
admitted fidelity defect. Actual project CLI controls confirmed that a
physically identical, link-free absolute checkout-prefix alias was rejected by
lexical containment before source spelling recovery. The project-pinned Ruff
0.9.10 formatter also rejected the new paired self-bootstrap assignment;
the unchanged base and other four selected Python files passed.

The implementer independently reproduced both. Root-cause debugging traced the
alias input through shared checked_path into translator/reviewer selection and
native/read-only consumers. Six real prefix regressions failed; two redirect and
different-checkout controls passed. The uniform path validator now inspects all
raw ancestors, including those above an alias of the selected root, before using
root-directory device/inode identity to establish containment and rebasing to
the selected root. Redirects, invalid parents, parent traversal, nonregular or
hard-linked files and genuinely different checkouts remain refused. Root alias
normalization cannot remove an unchecked link from the original path.

| Scenario | Additional covering function | Expected outcome asserted |
|----------|------------------------------|---------------------------|
| TS-008 | test_ts008_physical_checkout_prefix_alias_keeps_selected_source | Six checkout/parent-prefix alias forms retain exact README/site-file/site-directory pairs, hashes and CLI success with unchanged bytes |
| TS-008 | test_ts008_prefix_identity_never_launders_redirects_or_other_checkouts | A symlinked ancestor leading to the same physical source and a different checkout with identical source bytes both refuse through API/CLI without changing either input |

Formatting used the existing pinned binary on stdin, with scoped writes only
through the contained writer. Python ASTs before and after formatting are equal;
no artificial functional test was added for a formatting defect. The fixed
format --check --no-cache now passes all five selected Python files; source-derived
native/distribution behavior and the regression suite remain green.

After the prefix repair, targeted tests passed 210 cases with 3 skips and the
complete suite passed 2,422 cases with 56 skips (2,478 accounted). The archived
manifest is /private/tmp/codexspec-docs-maintenance-suite-emby99wh/manifest.json.
It does not substitute for the current complete baseline above.
The source, translation hashes and package-included bytes remain preserved.
Pinned formatting, Ruff lint, native/distribution, seven-pair mechanics,
Markdownlint and whitespace checks pass. Mandatory fresh incremental and complete
review acceptance remains separate. Those four neutral obligations were
subsequently independently verified against their selected frozen target, as
recorded in the next section.

## Prospective destination uniqueness

The next isolated incremental result at
sha256:fcfed4edb422c7d0b528952b10a77a61a7a0020883e78428482513477a17e69c
was validated with one P2, FS-CUR-F001. Both independent reviewers verified the
four incoming source-selection and pinned-format obligations. A new real
filesystem witness showed distinct custom source files producing two absent
case-equivalent targets; sequential writes addressed one eventual inode and
replaced the first translation. This output-cardinality defect is separate
from source-object admission and existing source-target overlap, both of which
remain verified. The current obligation is to retain one source per prospective
physical destination before incremental omission, while preserving disjoint
and case-sensitive destination compatibility.

Root-cause debugging traced the complete source set through English/custom
relative mapping to the target set comparison. That comparison used POSIX path
spelling. Real fixture witnesses outside the selected fixture checkout establish
leaf, parent, empty-parent and Unicode-normalization aliases; eight regression
cases first failed in ordinary/incremental modes, four compatibility controls
passed and two native distinct-destination controls skipped. The uniform target
key applies normalized folded names only when a real namespace alias establishes
case folding; a namespace that preserves spelling retains distinct target names.
The complete output set is checked before any timestamp omission. Target source
inode overlap, path/type/link refusal and original resource path spelling remain
covered by the existing tests.

| Scenario | Additional covering function | Expected outcome asserted |
|----------|------------------------------|---------------------------|
| TS-006 | test_ts006_prospective_destination_aliases_are_rejected_before_any_write | Eight real alias cases refuse through API/CLI before output creation, preserve all source bytes and cover ordinary/incremental selection |
| TS-006 | test_ts006_case_sensitive_prospective_destinations_remain_distinct | Distinct leaf/Unicode names retain two mappings and separate eventual output inodes where the native namespace supports them; both skip on this volume |
| TS-006 | test_ts006_case_sensitive_destination_namespace_policy_preserves_spelling | Modeled namespace policy retains exact target spellings using real source I/O without claiming native case-sensitive platform execution |
| TS-006 | test_ts006_disjoint_prospective_destinations_remain_supported | Ordinary and incremental selection retain separate supported outputs with unchanged bytes |

Targeted evidence: /private/tmp/codexspec-docs-output-red.log (8 failed, 4 passed,
2 skipped) and /private/tmp/codexspec-docs-output-green.log (222 passed, 5 skipped).
The helper has 91 collected cases: 87 pass and four native distinct-name controls
skip on this case-insensitive volume. All earlier tests remain green. Pinned
formatting preserves Python ASTs; evidence is
/private/tmp/codexspec-docs-output-format-evidence.json. The current complete
86-file baseline is 2,434 passed and 58 skipped, all 2,492 collected tests
accounted for with three successful groups. The final manifest above retains
exact commands, group membership and raw outcomes. No package-included bytes or
README source/translation hashes changed. The new neutral output-uniqueness
obligation remains subject to fresh independent verification; this document does
not claim the mandatory subsequent complete-review verdict.
