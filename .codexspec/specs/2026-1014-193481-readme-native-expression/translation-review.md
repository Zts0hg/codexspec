# Native README Translation Review

Status: PASS by agent assessment. All seven complete actual targets were inspected for fidelity and natural expression, observed defects repaired, and final document checks passed. No native-human certification is claimed.

## Selection and authority

Baseline: `e35e6be295cf42a931df4b3d8dc405aa3b9f7f93`.
English source SHA-256: `200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363`.

Selected workflow: `$codexspec:translate-docs --readme --lang all`, followed by `$codexspec:check-i18n-semantics --readme --lang all --strict`. These are agent workflows; inventory and verification helpers provide separate mechanical evidence.

The complete English source and all selected target prose were read. Protected examples were read in the source and compared byte for byte in the targets. All seven existing root variants were fully selected; no timestamp selection or introduction-only rewrite was used. The [confirmed requirements](requirements.md) retain the exact user-approved Chinese introduction, which matches the actual Chinese file verbatim.

## Instructions and both hosts

The authored Claude translator/reviewer and shared rules require native technical prose, permit sentence restructuring without meaning loss, treat clear translationese as a defect, and assess fidelity and natural expression separately. Approved wording governs its corresponding passage. Codex entries were generated from the authored sources; source-derived parity and distribution checks pass. The later approved-wording rule was read by the caller and the Spanish/French and German/Portuguese evaluators; no approved passage exists for the Japanese/Korean pair, whose actual targets the caller also inspected.

## Actual final target assessment

These are agent judgments based on source/target reading. Matching structure and test success were not used as evidence of natural expression.

| Target | Fidelity | Natural expression | Final SHA-256 |
|---|---|---|---|
| `README.zh-CN.md` | PASS after inspection/repairs | PASS after inspection/repairs | `a0f535a79a6db70b78ac6bd39197cafd1d05492b594de4573acb81e88dcc3269` |
| `README.ja.md` | PASS after inspection/repairs | PASS after inspection/repairs | `37d52635242851302173422cdf79b4cf4f56e1b6121c6f55e335d637738c51cc` |
| `README.ko.md` | PASS after inspection/repairs | PASS after inspection/repairs | `0ad786458a1b89b71c9294f57f2c61274af3fd42d975407a5d8e330aca57d598` |
| `README.es.md` | PASS after inspection/repairs | PASS after inspection/repairs | `91e3e5087978330bab9e9965cc194f77c633d3c6db9b166c7f17eccdbae3796c` |
| `README.fr.md` | PASS after inspection/repairs | PASS after inspection/repairs | `71819c22fc805867e0bc55f60aefb7db8eda6947a106e2036ee6ad70c23bde4d` |
| `README.de.md` | PASS after inspection/repairs | PASS after inspection/repairs | `8882aebd9dc6560a5b94aa948b87db611445d18cadac22058fbb796edbe05b7f` |
| `README.pt-BR.md` | PASS after inspection/repairs | PASS after inspection/repairs | `d5bfc24272a20efc5672eef8e5d990689de7076935d2fcce932a1c825759cc52` |

## Complete-source coverage

Every row below was assessed in all seven final targets. The complete prose reads and rereading of repaired passages cover the final bytes.

| Source area | Propositions assessed |
|---|---|
| Preamble and language navigation | User owns what/why; agent develops how within confirmed requirements; reviews and persistent knowledge; optional blueprint, default worktrees and all eight language choices. |
| Table of Contents | Source entry order, translated headings and valid destination slugs. |
| Why Choose CodexSpec? | All seven needs/benefits; confirmation authority, constraints, exclusions, open questions and confirmation evidence; human control of intent and limits on automation. |
| 30-Second Quick Start | Both assistant invocation forms, explicit requirements confirmation and returned feature/workspace; optional project principles; desktop installation link. |
| Installation | Complete desktop setup and protected prompt, alternatives and prerequisites; default assistant, one-time CLI limits, Windows guidance, CLI upgrade versus project refresh, exact force preservation, retired entry without alias, plugin boundary and runtime/hook prerequisites. |
| Core Workflow | Entire artifact chain and all step outputs; continuity, specify/clarify/analyze authority and question limits; Quick boundaries; exact automation defaults/statuses, terminal implementation and two artifact-repair rounds. |
| Shared Blueprint and Autonomous Development | Confirmation before queue entry, three states, pending-only mutations, document order, resume first, reread queue, independent automation, fixed shared workspace/branch, protected concurrency and sequential development, evidence-backed stopping. |
| Worktree Development | Create before first write, one workspace per ordinary feature, stable reuse, maintenance routing, checkout-local settings and Git propagation, ancestry baseline and verified divergence merge, failed-fetch warning, no fallback, literal-false rule, initialization/blueprint exceptions and retention. |
| Work with Existing Code | Distinct onboard/reverse-spec goals and code read-only boundary; constrained evidence, candidate effects/decisions, no invented history, three reverse-spec modes and drift types, human baseline confirmation and report-only proposed direction. |
| Review and Debugging | Four artifact reviews, defects/advisories, full-feature Git scope and selectors, audit-only scorecard, relevant standards and concrete evidence/attribution, read-only reviewer, caller verification, tests first, fresh final whole-feature PASS and zero admitted defects, independent maintenance, debug sequence/escalation and checklist. |
| Project Knowledge, including Reusing Historical Decisions | All six categories, feature/profile boundary, candidate/vetted distinction, offline manual review/draft/conflict protection, text fallback, three default-on capture hooks and preview exclusion, ambient capture, deduplication, no-write exit, non-blocking automatic capture, evolve approval and continuing historical decisions with latest user authority. |
| Git Workflow | Exact staged scope/ownership and authorization, preview versus guarded execution, PR/MR context resolution, changelog labels and all release-action exclusions, authenticated issue destination, standalone runtime and all merge distinctions. |
| Available Commands | Six public CLI commands, all 28 distributed agent commands and all seven groups, with source-backed command descriptions. |
| Configuration and Internationalization | 13 runtime languages versus pt-BR resource code, independent language fallbacks, English templates, TTY exceptions and force behavior, retained unspecified settings, all five defaults, boolean parsing/toggle destination, out-of-context review decisions and checkout-routed updates, complete options and YAML. |
| Project Structure | Complete protected tree and selected assistant integration, blueprint's sole editable home and excluded manual-review drafts. |
| Extension Materials | Authoring resources, absent CLI install/list/remove and automatic loading, additions to shared review resources, preservation unless replacement requested. |
| Development | Complete protected development example, required context/layout reading and authoritative source regeneration. |
| Contributing | Local contribution guide, confirmed requirements, traceability and user/maintainer packaging boundary. |
| License | MIT and LICENSE link. |
| Acknowledgements | spec-kit inspiration and both assistant integrations. |

## Concrete findings and repairs

- **Chinese:** Adopted the exact two-paragraph introduction explicitly approved by the user; requirements retain that full text. The complete document was reworked, including tables and later sections. Restored incremental maintenance and upstream coverage qualifications; replaced the remaining ownership calque with coordinated workspace use and protected writes.
- **Japanese:** Independent complete rewrite and separate fidelity/natural-expression review; caller read all actual prose. The caller made persistent storage explicit in the opening: プロジェクトに保存した知識. The original evaluation report retains its own pre-caller-repair hashes.
- **Korean:** Independent complete rewrite, confirmed-state terminology and source-supported modifier repairs; caller read all actual prose. The caller made persistent storage explicit in the opening: 프로젝트에 저장된 지식. The original evaluation report retains its own pre-caller-repair hashes.
- **Spanish:** Independent complete rewrite and strict review repaired legal-property wording for ownership, ambiguous release-action negatives and fallback explanations. Caller read the entire actual target and made automatic-capture negative coordination explicit before adoption checks.
- **French:** Independent complete rewrite and strict review repaired design artifact names, ownership wording and highest requirements authority. Caller read the entire actual target and corrected the grammatical elision before effectuer; no forward-test PASS was used to excuse that defect.
- **German:** Complete source and both draft/stable target prose were read. Independent review repaired onboarding candidate phrasing, document roles and conditional fallback. Caller made runtime terminology explicit as Laufzeitumgebung and narrowed constraints by their evidence-backed scope rather than describing evidence as weak.
- **Brazilian Portuguese:** Complete source and both draft/stable target prose were read. Independent review repaired document roles, substantive-work scope, actionable-issue wording and fallback conditions. Caller clarified evidence-backed constraint scope and repeated negative coordination for automatic capture and all release-action exclusions.
- **Language configuration in all locales:** Caller replaced literal Git-delivery phrasing with each language’s normal description of commit messages and texts produced by Git workflows. This preserves the language.commit scope while avoiding wording that could suggest deployment.

Original independent evaluations and body-wide old/new examples are retained in [Japanese/Korean](forward-test-ja-ko.md), [Spanish/French](forward-test-es-fr.md) and [German/Portuguese](forward-test-de-pt.md). Their hashes describe the original mirror outputs; the table above describes current caller-repaired files. The evaluator for each pair translated and then performed a separate read-only review; the caller additionally inspected complete actual prose and subsequent changes before acceptance.

The Chinese rewrite also spans the complete document. Examples include replacing 编译为带来源引用的规格 with 根据已确认需求编写规格并标明来源, 规划就绪度 with 能否据此制定计划, and the ownership abstraction with coordinating workspace use and protected writes. These prose changes retain the source behavior; the approved opening is preserved exactly.

## Actual final verification

The source has 25 fenced examples, 180 distinct inline technical tokens (229 occurrences), 40 heading levels, 16 tables and 119 raw table rows. Raw example blocks, inline-token multisets, heading-level order, table structures and raw row widths match in every final target. External HTTP(S) URL multisets also match. English source bytes equal HEAD and the pinned hash.

| Check | Actual result |
|---|---|
| `.venv/bin/python -B -m internal.doc_translation verify --readme --lang all` | Exit 0; all seven final pairs selected; no errors |
| `.venv/bin/python -B -m internal.maintainer_doc_skills --check` | Exit 0; `changed: []`; both native entries match authored sources |
| `.venv/bin/python -B internal/command_template_fragments.py --check-distribution` | Exit 0; distribution remains current |
| `.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_maintainer_doc_tools.py tests/test_command_template_fragments.py tests/test_review_code_docs.py tests/test_translation_files.py --basetemp=/private/tmp/codexspec-native-193481-final-fixtures` | 308 passed, 6 skipped; 314 collected. Helper/fragment content was final; the last two README rewrites had not yet been adopted |
| `.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_review_code_docs.py tests/test_translation_files.py --basetemp=/private/tmp/codexspec-native-193481-final-readme-fixtures` | 93 passed, no skips, after all seven final caller-repaired targets were present |

The six earlier skips are filesystem/platform-dependent existing cases; they do not establish native Windows/Linux results. Python 3.11.13 and the feature workspace's own editable environment were used. Independent environments/check outcomes are detailed in their reports. Final Markdown lint and path/state results are recorded below.

## Validation compatibility and isolation

The generic skill-creator validator rejects the unchanged `codexspec:translate-docs` namespace as non-hyphenated. The same rejection was reproduced on the baseline skill; the project renderer intentionally uses this namespace. Project skill/distribution checks pass. The limitation is recorded as a candidate [pitfall](../../profile/pitfalls/P-2026-1014-193481-1-generic-skill-validator-rejects-namespaces.md); no command identity was changed to satisfy that generic check.

All persistent project writes use the isolated feature workspace. Independent forward tests use physical temporary mirrors with their own environments; original artifacts were inspected before adoption. The caller's final small repairs are identified above rather than attributed to an earlier evaluator PASS. No staging, commit, merge, push, publication or version change is part of this translation work.

## Final file checks

- `npx --offline --yes markdownlint-cli@0.42.0` on all seven READMEs, both authored Claude entries, both generated Codex entries, the shared guide, five feature artifacts and the candidate profile record: exit 0, no diagnostics; no `--fix` used by the caller.
- `git diff --check`: exit 0, no diagnostics.
- Final destination/state inspection: exactly 12 tracked modified files and 6 new authorized artifacts; all are contained regular single-link files with no symlink ancestor. The index is empty. English README, version files, runtime, public templates and packaging remain unchanged; main is clean at the recorded baseline.
- Feature branch: `2026-1014-193481-readme-native-expression`. Project output root: `/Users/xiaoming/code/codexspec-codexspec-worktrees/2026-1014-193481-readme-native-expression`.
