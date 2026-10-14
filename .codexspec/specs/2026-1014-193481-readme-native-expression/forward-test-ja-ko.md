# Independent Forward Test: Japanese and Korean README Translation

The full Japanese and Korean READMEs were retranslated from the selected English source using the mirror's actual `$codexspec:translate-docs --readme --lang ja,ko` instructions. A separate read-only pass followed the actual `$codexspec:check-i18n-semantics --readme --lang ja,ko --strict` instructions. Both pairs pass this agent's final fidelity and natural-expression assessment after repairs. All applicable mechanical, Markdown lint, source-derived skill, distribution, and existing documentation-contract checks passed.

This is an agent evaluation in an isolated mirror, not a native-human review. The evaluator is independent of the caller's drafting session, but the same evaluator translated and then reviewed these two documents. The strict semantic assessment therefore does not claim a second independent reviewer or native-speaker certification. The caller must inspect the actual output before adoption.

## Selection, source, and isolation

- Physical source and output root: `/private/tmp/codexspec-native-forward-ja-ko-bgwp6_jd`.
- Source: `README.md`.
- Selected targets: `README.ja.md` and `README.ko.md` only.
- English source SHA-256 before translation, before and after each target write/repair, and at final verification: `200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363`.
- Final Japanese SHA-256: `a404b95a68ab2717d39e166429d25c25910ae6297cbf077e5094fe7bbf954525`.
- Final Korean SHA-256: `97e77ad5b00e8e68223c5035743a94029a146e44a696e18a30f7c53eb1fc5277`.
- The English source was never edited. The mirror's intentional `workflow.worktrees: false` remained unchanged, making SOURCE_ROOT and OUTPUT_ROOT the same physical mirror.
- Before the first target write, both destinations and the requested report path were checked. Immediately before every later output write, the output ancestry was inspected with `lstat`, links were refused, existing destinations had to be regular files with exactly one hard link, and physical parent containment was checked. Target writes also used `O_NOFOLLOW` and checked the opened file with `fstat`. The report destination was absent, its physical ancestry was checked, and its creation used exclusive/no-follow flags.
- No work occurred in the original repository or a sibling feature worktree. No staging, commits, pushes, merges, or publication occurred. Only the two targets and this report were written by the evaluator, apart from ignored environment/test setup. The caller supplied the mirror's existing raw extension-guide dependency so the original relative link could be verified; no README source or skill content changed.

The environment was built independently with `uv sync --frozen --extra dev --extra docs --python 3.11.13`. Runtime provenance was checked: `sys.executable` and `sys.prefix` resolve to the mirror's `.venv`, and `codexspec.__file__` resolves to its own `src/codexspec/__init__.py`. Tests used external fixture directories, not directories inside the mirror. This mirror has no `.git`; the read-only distribution check nevertheless completed successfully.

## Actual skill use and reading

The selected mirror's `.agents/skills/codexspec-translate-docs/SKILL.md` and `.agents/skills/codexspec-check-i18n-semantics/SKILL.md` were loaded directly. Their shared `internal/references/doc-translation.md` and the workspace-routing fragment were read. The two skill invocations were carried out by executing their agent workflows; no hypothetical translation CLI was substituted for them.

Raw project context included AGENTS.md, CLAUDE.md, the project constitution, repository layout, configuration, all constraints, profile headings/conditions and applicable environment/path records, the two relevant confirmed documentation requirements records, the complete glossary, existing localized workflow/review-command terminology, Markdown lint configuration, and relevant documentation-contract tests. The complete English source and both original localized READMEs were read. Complete new target documents were then reread from the actual files in sequential chunks; the final repaired passages were reread and the complete files were rechecked mechanically. The rewrite covered every prose section, heading, list, table, notice, and summary label, rather than an opening-paragraph edit.

Glossary translations and keep-English rules were retained, including Japanese プロジェクト憲法 / 仕様書 / タスク and Korean 프로젝트 헌법 / 명세서 / 태스크 / 워크플로우 / 리포지토리. The established documentation-contract terms 欠陥ゲート and 결함 게이트 remain. Korean confirmation terminology was aligned with the existing guide's 확정된 요구사항. No glossary decision or skill change was invented.

## Full-document coverage and fidelity

Every row below was assessed for both languages. The review compared actors, source authority, inputs, conditions, defaults, ordering, exclusions, and consequences, then read the target independently for expression.

| Source section | Propositions assessed in both targets |
|---|---|
| Branding, introduction, and language navigation | Claude/Codex integration; user decides what/why; agent works within confirmed requirements; review checkpoints and persistent knowledge; default worktrees; optional blueprint; eight language destinations with the selected language active and English linked |
| Table of Contents | All original TOC entries in source order; translated heading text and valid self-links |
| Why Choose CodexSpec? | All seven need/benefit rows; Requirements-First authority; goals, constraints, decisions, exclusions, open questions, confirmation evidence; human control of intent and limits on automatic advancement |
| 30-Second Quick Start | Assistant-specific initialization; both invocation forms; optional constitution customization; final confirmation; returned feature/workspace; desktop link |
| Installation | Desktop installation's three steps and protected prompt; Chinese-language substitution; prerequisites; CLI verification; assistant default; one-time CLI limitations; development versions; Windows/PATH guidance; separate upgrade/refresh; exact force behavior and retained data; retired entry without alias; plugin guidance and scaffold boundary; runtime/CLI/hook requirements and manual-Git boundary |
| Core Workflow | Entire requirements/spec/design/plan/tasks/code chain; all seven step rows and outputs; host prefixes; explicit feature continuity; specify's explicit confirmation; clarify's five-question/four-category limit and requirements-first update; analyze's deterministic downstream fixes, untouched requirements, unresolved reports, automatic but informational role; Quick's scope/pause conditions; false auto-next default, passing/stopping statuses, terminal implementation, two artifact-repair rounds |
| Shared Blueprint and Autonomous Development | Discovery before queue entry; three states; four pending mutations; active/completed read-only boundary; document order and resume-first behavior; reread after completion; newly appended work; independence from auto-next; fixed workspace/branch; concurrency protections and sequential development; evidence-backed stop on unresolved product decisions; read-only inspection |
| Worktree Development | Worktree definition; one per ordinary feature before first write; related work kept together; stable reuse; maintenance routing; checkout-local configuration and Git propagation; returned workspace for checks; ancestry baselines, verified divergence merge, failed-fetch warning, no fallback to main; literal-false rule; blueprint exception; initialization/update exception; retained worktrees and no automatic merge/delete |
| Work with Existing Code | Distinct onboard/reverse-spec goals and read-only code; candidate conventions versus narrowly evidenced constraints; immediate convention effect versus constraint decision; preserved existing knowledge and no invented rationale/pitfalls; overview, generate, reconcile triggers and outputs; human confirmation before baseline; three drift kinds; requirements govern intent; report-only proposed direction |
| Review and Debugging | Four artifact reviewers and compatibility scores; defects separated from advisories; whole-feature default Git delta; explicit evidence selectors; feature context does not narrow scope; path audit is advisory; shared standards; concrete/reachable/attributed/impact evidence; reviewer read-only and caller verification; code test-first; final fresh complete-feature PASS, completed coverage and zero admitted P0–P3 defects; maintenance defaults and exemptions; debug phases, three escalation triggers and three-failure reassessment; checklist scope |
| Project Knowledge | All six categories; cross-feature capture versus feature intent; installed context guidance and no reinitialization requirement; candidate caution and vetted verification/human endorsement; manual offline browser review, six actions, final preview/apply, recoverable draft, conflict protection and text fallback; three default-on wrap-up hooks; preview exclusion; independent near-moment guidance; within/across-session deduplication; no-write exit and non-blocking auto capture; vetted upstream contribution and explicit approval |
| Reusing Historical Decisions | Substantive recall in ordinary chat and SDD; reconstruct unchanged decisions/additions/replacements before questions; older unchanged requirements remain; latest user decision prevails; open proposals not confirmed; task-scoped retrieval and background reuse; refresh installations |
| Git Workflow | Exact staged input and caller staging ownership; preview/authorized guarded execution; availability is not invocation/authority; PR context path/name/prefix and text default; changelog default/label and all excluded Git/release actions; issues' authentication/remote/dependencies/acceptance; standalone runtime prerequisites; contentful/history-only/fast-forward merge distinctions |
| Available Commands | Six public CLI commands and all 28 integrated commands; seven command groups; faithful purpose of every row; defect-gate and audit distinction |
| Configuration and Internationalization | English templates; 13 runtime codes versus Portuguese docs/catalog code; all four language dimensions and configuration options; independent fallback; TTY exemption only for base/all-three options; force does not skip language choice; non-TTY English; reinitialization preservation; five workflow/review settings with exact defaults and controls; boolean accepted values/whitespace/toggle destination; out-of-context decision mode and blocking; one-run override; routed writes; both option tables and YAML example |
| Project Structure | Complete protected tree; shared resources and assistant integration; blueprint location without per-checkout editable copies; Git-excluded review drafts |
| Extension Materials | Manifest/example/guide are authoring material; absent CLI extension install/list/remove support and absent automatic loading; project additions to shared reviews; preservation unless replacement requested |
| Development | Complete protected setup/check/build example; required context/layout reading; generated installation artifacts and authoritative-source regeneration |
| Contributing | Local contribution guide; confirmed requirements, traceability, user/maintainer packaging boundary |
| License and Acknowledgements | MIT/LICENSE link; spec-kit inspiration and both assistant integrations |

## Separate per-language assessment

| Pair | Fidelity | Natural expression | Strict final outcome |
|---|---|---|---|
| `README.md` → `README.ja.md` | PASS: no remaining identified omitted/added capability or changed condition, default, ordering, obligation, or exclusion | PASS by agent assessment: coherent Japanese technical prose, normal clause order, appropriate particles/register, readable headings and table descriptions; observed ambiguities and source calques repaired | PASS |
| `README.md` → `README.ko.md` | PASS: no remaining identified omitted/added capability or changed condition, default, ordering, obligation, or exclusion | PASS by agent assessment: natural Korean syntax and collocations, consistent technical register and terminology, explicit subjects/actions where needed; observed modifier/terminology issues repaired | PASS |

These judgments come from source/target reading. Neither matching structure nor passing tests was used as proof of fidelity or natural expression.

## Specific before/after expression examples

The “before” text below comes from the original mirror targets read before the complete rewrite. Examples span the document, including later review and configuration sections.

| Language and location | Before | After | Assessment |
|---|---|---|---|
| Japanese, introduction | レビューの確認点と永続的なプロジェクト知識を使い | レビューの節目と蓄積したプロジェクト知識を活用しながら | Replaces the awkward literal checkpoint phrase with ordinary Japanese; retains review checkpoints and persistent project knowledge. |
| Japanese, benefits | セッションとチームでの継続性 | セッションや担当者が変わっても作業を引き継ぐ | States the continuity benefit as a concrete action rather than a translated abstract noun phrase. |
| Japanese, review evidence | 選択した変更への帰属 | 選択した変更に起因すること | Expresses attribution naturally while retaining the requirement that the finding arise from the selected change. |
| Japanese, debugging | 単純ではない正しさの欠陥を追跡する必要がある場合 | 単純ではない動作上の欠陥について原因を追う必要がある場合 | Repairs an unnatural correctness-defect collocation without changing the non-trivial defect trigger. |
| Japanese, command table | 端から端までの追跡可能性を確認し、下位成果物を判断基準に適合 | 一連の成果物の追跡可能性を確認し、下位成果物を上位の判断基準に合わせて修正 | Avoids a literal end-to-end calque and names the actual downstream correction. |
| Japanese, workflow guide link | 詳細な契約 | 詳しい動作と条件 | Uses the ordinary documentation description appropriate to these behavior contracts. |
| Korean, introduction | 리뷰 점검 단계와 지속적으로 보존되는 프로젝트 지식을 활용해 | 단계별 리뷰와 축적된 프로젝트 지식을 활용해 | Removes a cumbersome calque and reads naturally while retaining reviews and persistent accumulated knowledge. |
| Korean, benefits | 세션과 팀 간 연속성 | 세션이나 담당자가 바뀌어도 작업 이어가기 | Makes continuity understandable as the ability to continue the work across sessions/team members. |
| Korean, review evidence | 선택된 변경에 대한 귀속 | 선택한 변경에서 비롯되었다는 설명 | Replaces an unnatural nominal phrase with the actual selected-change attribution requirement. |
| Korean, debugging | 단순하지 않은 정확성 결함을 추적해야 하거나 | 단순하지 않은 동작상 결함의 원인을 추적해야 하거나 | Repairs the literal correctness-defect phrase without omitting non-triviality or tracing. |
| Korean, workflow guide link | 자세한 계약 | 자세한 동작과 조건 | Makes the referenced behavior contracts readable as technical documentation. |
| Korean, configuration decision | 맥락 밖의 발생 조건이 보류 중인 시나리오 결정이 됩니다 | 운영 범위 밖의 발생 조건을 사용자 판단을 기다리는 시나리오로 처리합니다 | Uses natural syntax and makes the user-decision state explicit; later sentences retain one decision, persistence, blocking, and override. |

One equally natural phrase may still have another valid formulation. No unresolved grammatical error, unnatural collocation, or clear calque was intentionally treated as an optional preference.

## Review findings and actual repairs

The first mechanical verification and lint passed before the semantic reread. The reread still found issues, showing why mechanical agreement cannot establish prose quality:

1. Both compact `--auto-maintenance` option descriptions had lost the source's incremental qualification. The translator restored 段階的な保守改善 and 점진적 유지보수 개선. Japanese's setting row was also changed from “sequentially” to “in stages” to preserve incremental behavior. This was a fidelity repair, not a stylistic advisory.
2. Onboard's narrow-evidence description could read as weak/limited evidence: 限定的な根拠 / 좁은 범위의 근거. It now says 根拠に基づいて範囲を絞った制約 / 근거에 따라 범위를 한정한 제약. The following paragraph still limits constraints to explicit prohibitions. This repairs both expression and an avoidable fidelity ambiguity.
3. Authorized in-place commit descriptions had an awkward modifier attachment that could appear to authorize the checkout instead of the commit. The prose was restructured to say that an authorized commit is executed in the current checkout. Python/Git/runtime and persistent-CLI distinctions were retained.
4. Japanese's tagline was aligned to the same 要件優先 term used in the definition, keeping the named Requirements-First concept explicit. The repeated “intent” phrasing in both definitions was simplified without removing the human-authorization or automation limitation.
5. Korean uses the existing localized guide's 확정된 terminology consistently for confirmed requirements/baselines/intent/decisions. This avoids conflating an explicitly settled requirement with one merely checked. Blueprint command-table modifier order was also repaired in both targets.

The semantic reviewer phase remained read-only. These findings were returned to the translator role in the calling workflow; target writes were then preflighted again, followed by checks and rereading of the repaired passages. Final review has no unresolved fidelity or natural-expression finding.

## Actual verification outcomes

All commands ran in the mirror against its own environment and actual final files.

| Check | Actual outcome |
|---|---|
| `.venv/bin/python -B -m internal.doc_translation inventory --readme --lang ja,ko` | Exit 0; exactly the two selected pairs; expected source SHA-256; no selection errors |
| `.venv/bin/python -B -m internal.doc_translation verify --readme --lang ja,ko` | Exit 0; `errors: []` before and after prose repairs |
| `npx --yes markdownlint-cli@0.42.0 --config .markdownlint.json README.ja.md README.ko.md` | Exit 0, no diagnostics; run without `--fix` before and after repairs |
| `.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_maintainer_doc_tools.py tests/test_review_code_docs.py --basetemp=/private/tmp/codexspec-native-forward-ja-ko-fixtures-final-bgwp6_jd` | Exit 0; 112 passed, 5 skipped in 0.66 seconds; first pre-repair run also 112 passed, 5 skipped |
| `.venv/bin/python -B -m internal.maintainer_doc_skills --check` | Exit 0; `{"mode": "check", "changed": []}` |
| `.venv/bin/python -B internal/command_template_fragments.py --check-distribution` | Exit 0, no diagnostics |
| Additional exact-byte/parsed-structure probe | Every target preserves all 25 fenced code blocks exactly, including comments; equal parsed inline-token multisets (180 distinct tokens), 40 heading levels in order, and all 16 table structures |
| Final source hash/configuration check | Expected SHA-256 retained; `worktrees: false` retained |

The five skips are filesystem-dependent cases in the existing helper tests on this macOS environment. No native Windows or Linux execution is claimed. The 16 review-document contracts include all locales; their success does not imply that the evaluator reviewed unselected translations or changed site documentation. These checks verify the relevant existing contract and protected structure, not native expression.

The English source has 892 lines; each target has 827 after sentence/paragraph restructuring. This difference is not an omission claim or a completeness proof: complete section-by-section reading supplies the coverage evidence, while matching protected content and structure provide separate mechanical support.

## Instruction weaknesses and remaining limits

The updated skills explicitly required the necessary complete reading, proposition preservation, natural-language rewriting, separate assessments, repairs, source pinning, and mechanical verification. They were sufficient to complete this realistic request without changing skill instructions.

The glossary is intentionally sparse for newer feature concepts such as confirmed state, profiles, review attribution, and worktree routing. Consulting established guides and their tests, as the shared rules require, was necessary. Some older guide prose is itself awkward or reflects an older workflow; it was used for established terminology only, while the selected README remained the authority for behavior. This is an evidence-quality limitation worth retaining, not a reason to copy old wording or change the English source.

The current reviewer instructions permit the translator agent to perform its own separate read-only review; they do not establish a second independent reviewer. That limitation remains explicit here. A native-human review may find nuances this agent missed. No such review was performed, no native-human endorsement is claimed, and the caller's inspection of these exact targets remains the adoption step.
