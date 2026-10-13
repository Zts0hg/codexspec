# Japanese and Korean README Translation Evidence

## Result and invocation

Final strict semantic result: **PASS for ja; PASS for ko**. No unresolved
omission, changed behavior, terminology defect, or navigation finding remains
in the reviewed pairs. The result follows complete source/target reading and
the proposition assessment below; matching counts alone do not establish it.

Executed native Codex workflows in this agent:

```text
$codexspec:translate-docs --readme --lang ja,ko
$codexspec:check-i18n-semantics --readme --lang ja,ko --strict
```

These are agent skills, not executable CLI translation programs. I loaded the
selected checkout's actual `.agents/skills/codexspec-translate-docs/SKILL.md`
and `.agents/skills/codexspec-check-i18n-semantics/SKILL.md`, read their shared
`internal/references/doc-translation.md`, and executed those workflows against
the actual files. The checker assessed outputs independently of generation
intent, returned repairs to the translator, and assessed the repaired spans
again. No previous translator report or supplied correctness conclusion was
used as semantic evidence.

`SOURCE_ROOT` and `OUTPUT_ROOT` both remained the caller's explicitly selected,
ready feature workspace:

```text
/Users/xiaoming/code/codexspec-codexspec-worktrees/2026-1013-1133ii-codex-docs-maintenance
```

Only `README.ja.md`, `README.ko.md`, and this feature-local evidence report were
written by this agent inside that checkout. English was not edited. No staging,
commit, push, new feature, site translation, or nested agent work occurred.
Temporary translation drafts and restoration requests stayed under
`/private/tmp/`, outside Git.

## Inputs and provenance

| Role | File | SHA-256 |
|------|------|---------|
| Complete English baseline | `README.md` | `200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363` |
| Original Japanese target, pinned before writes | `README.ja.md` | `445a57f62c2270fe01034e731b6a9a5ad6a02fce54939f397b3dd93ba5611e99` |
| Original Korean target, pinned before writes | `README.ko.md` | `2b08caf73dd1ba7f974812930f062bbab4ef7d6bbf4e5028c9c0632e41508ad9` |
| Final Japanese output | `README.ja.md` | `d0238755b1a851e0ea135b6d84f2d41946e571018e98e94ea877b66a2da43290` |
| Final Korean output | `README.ko.md` | `9f373c9d6663d11bed18750109873864ab5e42673f9efbe0cc96ea5a787cac70` |

The source was read completely, including its installation prompt, all 25
examples, configuration options, command tables, and final acknowledgements.
Both complete actual targets were then read. The glossary was loaded from
`docs/i18n/glossary.yml` rather than the deprecated path. Technical names and
searchable terms such as CLI, API, Markdown, YAML, GitHub, uv, and SDD remain
English where appropriate. Japanese uses 仕様書, タスク, ワークフロー,
リポジトリ, コミット, 設定, 国際化, and プロジェクト憲法; Korean uses 명세서,
태스크, 워크플로우, 리포지토리, 커밋, 설정, 국제화, and 프로젝트 헌법 consistently
by meaning. Native inflection and particles were assessed as prose, not merely
matched against a word list.

Before substantive assessment, the selected AGENTS.md, CLAUDE.md, repository
layout, constitution, configuration, workspace-routing fragment, all profile
constraints, and relevant profile records were read. Historical applicability
was prepared from the current feature's confirmed requirements and the
preceding English README audit's confirmed requirements. The current feature
authorizes complete translations while retaining the English baseline and the
28-command maintainer/public boundary; it does not authorize expanding scope
into site translations or historical edits.

Existing target files were regular, single-linked files, with no symbolic link
in their ancestry. The scoped writer rechecked path containment and expected
target hashes before each write. Restoration rechecked the pinned English hash
before and after each target publication.

## Complete section and proposition assessment

The line keys in the table refer to the final files listed above. `EN` means
`README.md`, `JA` means `README.ja.md`, and `KO` means `README.ko.md`. Each row
was assessed in both languages; all rows passed after the recorded repairs.
Rows identify the actual corresponding section and the propositions checked,
rather than treating heading presence as semantic proof.

| Section and source key | Japanese key | Korean key | Assessed propositions preserved in both outputs |
|------------------------|--------------|------------|-----------------------------------------------|
| Branding, introduction, documentation navigation; EN:1 | JA:1 | KO:1 | Logos and badges retained; confirmed requirements become traceable spec/design/plan/tasks/implementation; user owns what/why and agent develops how within intent; Claude/Codex/both; separate ordinary worktrees and optional autonomous queue. |
| Table of Contents; EN:36 | JA:35 | KO:35 | All 17 source entries retain order, use translated labels, and resolve to their actual translated headings. |
| Why Choose CodexSpec; EN:56 | JA:55 | KO:55 | All seven need/provision rows preserve confirmation before specification, source-linked stages, four artifact reviewers plus analysis and code gate, continuity, one ordinary worktree per feature, optional automation, and independent languages. |
| What is Requirements-First SDD; EN:68 | JA:67 | KO:67 | Confirmed requirements are highest feature authority; all recorded intent categories and confirmation evidence precede derivation; humans change intent; automatic review/advancement cannot silently replace requirements. |
| 30-Second Quick Start; EN:83 | JA:79 | KO:79 | Install and initialize for the chosen assistant; both invocation forms; optional constitution customization; final summary confirmation; returned directory/workspace continuation; working self-links to workflow and desktop setup. |
| Installation; EN:114 | JA:108 | KO:108 | All installation subsections, ordered instructions, alternatives, refresh rules, and plugin boundaries retained. |
| Install with the Codex Desktop App; EN:116 | JA:110 | KO:110 | Add/select local project, start chat/paste prompt, approve requested dependency installation if prompted; full source prompt is protected verbatim; Chinese language replacement, same CLI/skills, example invocation and official guide link preserved. |
| Prerequisites; EN:151 | JA:147 | KO:147 | Python 3.11+, recommended uv or pip, intended assistant, Git for worktrees/Git workflows; no new dependency or softened version requirement. |
| CLI Installation; EN:158 | JA:154 | KO:154 | CLI install/verification examples; new/current project distinction; both integration option; Claude default requires explicit Codex/both selection. |
| Alternative installation summary and One-time initialization; EN:178 | JA:173 | KO:173 | Translated disclosure label; uvx examples unchanged; project commands and standalone commit runtime installed; worktree, blueprint/auto-dev, manual review retain CLI requirement. |
| Development versions; EN:191 | JA:186 | KO:186 | Development/repository, main, and tag examples remain unchanged and in order; heading translated. |
| Windows installation disclosure; EN:206 | JA:201 | KO:201 | PowerShell requirement, restart/install/version example, and intentionally English PATH/install troubleshooting destination retained. |
| Upgrade and Refresh a Project; EN:220 | JA:214 | KO:214 | CLI update and project refresh are separate; single/both integration choices; force regeneration and resource refresh; automatic migration/update/compliance confirmation; retain requirements/principles/context bodies/unset keys; retire old planning entry without alias. |
| Plugin Marketplace Installation; EN:241 | JA:234 | KO:234 | Claude plugin commands and startup/resumed-session guidance; plugin does not initialize; config and full scaffold alternatives; bundled direct commit runtime versus workflows requiring persistent CLI; Git PATH and exec args support; no interception of manual Git. |
| Core Workflow; EN:266 | JA:257 | KO:256 | Complete protected stage chain, both prefixes, all seven purpose/output table rows, independent review-findings verification, feature directory substitution and stable identity across commands/sessions. |
| specify, clarify, and analyze; EN:296 | JA:286 | KO:285 | Explicit confirmation binds; four categories/up to five questions; update requirements before spec; whole chain analysis; deterministic downstream repair; requirements never edited; unresolved findings reported; automatic after task review and informational rather than implementation gate. |
| Small Changes with Quick; EN:314 | JA:301 | KO:300 | Small bounded changes; compact confirmed persistent summary; reviewed generation/planning/tasks/implementation; standard workflow for broad/unresolved choices; pause for new decision. |
| Workflow Automation; EN:327 | JA:313 | KO:312 | auto_next defaults false; active workspace true and final requirement confirmation start specification; PASS/warnings advance, revision/blocked stop; implementation terminal; verified upstream-grounded repair only, maximum two rounds; separate advisories and implementation loop rules. |
| Shared Blueprint and Autonomous Development; EN:342 | JA:324 | KO:323 | Queue preparation/development distinction; user-owned decisions resolved before queue; three states and pending-only edits; document order and in-progress resume; reread queue after completion; all SDD/review/repair stages; independence from auto_next; fixed worktree/branch; concurrent protection with sequential development; evidence-based stop for unresolved intent; read-only CLI inspection. |
| Worktree Development; EN:376 | JA:352 | KO:351 | Separate directory/branch definition; default one per ordinary feature before first write; colocated artifacts/code/tests/repairs; reuse and maintenance routing; checkout-local settings via Git integration; checks in returned workspace; ancestry baseline, divergent merge verification, fetch warning/local refs, no main fallback; literal-false isolation control; fixed auto-dev, init exception, retained completion without auto-merge/delete. |
| Work with Existing Code; EN:413 | JA:384 | KO:382 | Both purpose/output table rows and read-only code boundary; conventions inferred from observed code; explicit-prohibition constraints only; immediate conventions versus human constraint decision; preserve knowledge and never invent rationale/pitfalls; overview/generate/reconcile conditions, artifacts and three drift kinds; drafts require confirmation, reports do not automatically repair. |
| Review and Debugging; EN:448 | JA:413 | KO:411 | All four artifact reviewers, automatic/manual operation, quality dimensions and score; code defect gate versus audit; complete delta and explicit selectors; feature context does not narrow Git; standards and concrete evidence/trigger/attribution/impact; read-only reviewer and independent verification; code test-first versus docs/config checks; incremental reuse but fresh complete PASS and zero admitted P0–P3; maintenance defaults/control; all debug stages/escalation triggers/three failed fixes; checklist and reference. |
| Project Knowledge; EN:508 | JA:463 | KO:461 | All six categories and contents; distill versus feature intent; installed read-first guidance; no reinit requirement; cautious candidates versus verified/human-endorsed vetted records; offline manual review actions/final preview/apply-all; recoverable draft and conflict/all-or-nothing protection; text fallback; three hooks and preview exclusion; independent near-moment capture; per-session/new-material and cross-session dedup; no-write empty result, no human waiting/blocking; vetted-only evolve and approval before push/PR. |
| Reusing Historical Decisions; EN:562 | JA:507 | KO:503 | Recall before substantive judgments in ordinary and SDD work; unchanged/additional/replaced timeline before questions; old unchanged requirements still apply; latest explicit decision wins; open proposals unconfirmed; bounded retrieval/reuse and refresh instruction. |
| Git Workflow; EN:574 | JA:517 | KO:511 | All four examples; exact staged analysis, preview versus authorized guarded execution, caller stages, availability is not invocation/permission; PR/MR diff and optional file/name/prefix context, text default; release entry/body, Unreleased/default version label and all six excluded mutations; authenticated matching-repo issues with dependencies/acceptance; Python/Git runtime and merge distinctions. |
| Available Commands; EN:606 | JA:545 | KO:538 | Six public CLI and 28 distributed agent commands, both invocation spellings, Claude table convention; no maintainer command added to public count. |
| CLI Commands; EN:612 | JA:551 | KO:544 | All six names and respective init/check/version/config/list/show-blueprint effects, including read-only blueprint. |
| Core Workflow Commands; EN:623 | JA:562 | KO:555 | All nine names and purposes; cross-artifact principles, confirmation, pending queue, source-traceable specification/design/planning, upstream-covered tasks with review/analyze, verified implementation, ordered autonomous development. |
| Artifact Review Commands; EN:637 | JA:576 | KO:569 | All four names and fidelity/quality/feasibility/readiness/dependency/execution/verification distinctions. |
| Requirements, Existing Code, and Debugging; EN:646 | JA:585 | KO:578 | All six commands preserve requirements-first synchronization, authority conformity, checklist, issue conversion, cause-first debugging, architecture/draft/drift alternatives. |
| Project Knowledge Commands; EN:657 | JA:596 | KO:589 | All three commands retain capture/review, vetted upstream draft, candidate conventions/evidenced constraints distinctions. |
| Git and Code Review Commands; EN:665 | JA:604 | KO:597 | All four names preserve staged preview/authorized commit, PR/MR generation, history-derived entry/body, defect gate versus path audit. |
| Utility Commands; EN:674 | JA:613 | KO:606 | Config create/view/modify/reset and small-change compact requirements-first workflow retained. |
| Configuration and Internationalization; EN:681 | JA:620 | KO:613 | Config location, English templates with configured output, all 13 codes unchanged, Portuguese CLI pt versus resources pt-BR preserved. |
| Language Dimensions; EN:690 | JA:626 | KO:619 | All four rows with exact config/init/later flags and scopes; independent output-then-en fallback, templates en; examples; TTY conditional prompt, force does not skip language, non-TTY English, preserve unset reinit keys. |
| Workflow and Review Settings; EN:717 | JA:650 | KO:643 | All five exact keys/defaults/controls; case-insensitive whitespace-tolerant boolean aliases, bare switch uses destination value, YAML booleans; reviewer versus once-confirmed ask decision, blocking pending state and override; routed settings; all 10 init and 10 config options and translated disclosure labels; full YAML example; detailed English destinations. |
| Project Structure; EN:809 | JA:737 | KO:730 | Common and selected integration resources; complete protected tree; blueprint lives only in fixed auto-dev workspace, manual drafts excluded from Git. |
| Extension Materials; EN:848 | JA:775 | KO:768 | Manifest/example/guide are authoring materials; no CLI extension install/list/remove and no automatic commands/hooks loading; project-specific review additions and existing edits/additional files preserved unless replacement requested. |
| Development; EN:858 | JA:783 | KO:776 | Exact clone/dev extra/docs extra/CLI/test/lint/build example; read context/layout before template/package/init changes; derived install artifacts edited through authoritative source and regeneration. |
| Contributing; EN:879 | JA:803 | KO:796 | Local setup/guide link; preserve confirmed requirements, source traceability, packaging boundary. |
| License; EN:885 | JA:808 | KO:801 | MIT and LICENSE destination retained. |
| Acknowledgements; EN:889 | JA:812 | KO:805 | spec-kit inspiration and both assistant integrations retained. |

## Concrete source/target semantic evidence

These examples document the actual meaning-bearing correspondence assessed,
including actors, conditions, defaults, ordering, exclusions, and consequences.
The complete section table above additionally records the other propositions.

| Source evidence | Japanese evidence | Korean evidence | Judgment |
|-----------------|-------------------|-----------------|----------|
| EN:299–307: only explicit confirmation binds; requirements updated first; analyze never edits requirements | JA:288–294: 「明示的に確認された場合だけ」, 「最初に」/「次に」, 「一切編集しません」 | KO:287–293: 「명시적으로 확인한 경우에만」, 「먼저」/「뒤」, 「절대 편집하지 않습니다」 | Confirmation authority, order, absolute prohibition and informational boundary preserved. |
| EN:335–336: verified upstream-grounded repair with at most two rounds | JA:319: 「検証済みの欠陥に限定され」, 「最大 2 ラウンド」 | KO:318: 「검증된 결함으로 제한」, 「최대 두 라운드」 | Conditional automatic repair and upper bound remain mandatory boundaries. |
| EN:358–369: in-progress resume, reread queue, auto-next independence, fixed shared workspace, sequential requirements, unresolved decisions stop with evidence | JA:337–344: resume, reread, 「その設定を変更しません」, shared worktree/branch, 「順番」, evidence/stop | KO:336–343: resume, reread, 「그 설정을 변경하지 않습니다」, shared worktree/branch, 「순차적으로」, evidence/stop | Actors, processing order, configuration non-mutation and stop condition preserved. |
| EN:389–407: checkout-local configuration and literal false disabling ordinary isolation; fixed shared worktree and init exception | JA:367–380: 「チェックアウトごと」, Git integration, literal false, fixed worktree and selected checkout | KO:366–378: 「체크아웃별」, Git integration, literal false, fixed worktree and selected checkout | No implication that routed writes immediately alter main; fixed blueprint isolation remains. |
| EN:428–446: convention/constraint safety distinction; confirmation before baseline; report does not apply direction | JA:399–411: immediate conventions, in-session constraint decision, human confirmation, 「自動適用はしません」 | KO:397–409: immediate conventions, in-session constraint decision, human confirmation, 「자동으로 적용하지 않습니다」 | Human decision gate and read-only report boundary preserved. |
| EN:465–486: feature does not narrow Git; audit advisory; final fresh complete PASS with zero admitted P0–P3; disabling maintenance does not waive defects | JA:428–442: scope unchanged, advisory evaluation, 「新たに行う機能全体」/「ゼロ」, no waiver | KO:427–441: scope unchanged, advisory evaluation, 「새로 수행하는 기능 전체」/「0개」, no waiver | Defect acceptance and advisory/repair separation preserved without weakening the gate. |
| EN:534–557: draft/conflict protection; preview excluded; automatic capture never waits/blocks; evolve needs approval before push or contribution PR | JA:485–503: recoverable drafts, conflict checks, preview exclusion, no wait/block, 「前に、明示的な承認」 | KO:484–499: recoverable drafts, conflict checks, preview exclusion, no wait/block, 「전에 명시적인 승인」 | Transaction effect, trigger exclusion, non-blocking capture and external-action approval preserved. |
| EN:569–572: unchanged old requirements applicable, latest explicit decision wins, open proposals unconfirmed | JA:513–515: 「引き続き適用」, 「最新の明示的な判断が常に優先」, proposals unconfirmed | KO:508–509: 「계속 적용」, 「최신 명시적 결정이 항상 우선」, proposals unconfirmed | No invented expiry or historical override. |
| EN:581–604: caller stages, preview does not commit, availability grants no authorization; release has no mutations; three merge behaviors | JA:526–543: caller stages, preview, no permission, six excluded actions, content/history/fast-forward distinctions | KO:520–536: caller stages, preview, no permission, six excluded actions, content/history/fast-forward distinctions | Execution permissions and release/merge boundaries preserved. |
| EN:710–715 and 731–735: force does not skip language prompt; ask decision confirmed once; pending blocks completion | JA:646–648 and 663–666: prompt exception, preserved unset keys, once-confirmed decision and 「完了できません」 | KO:639–641 and 656–659: prompt exception, preserved unset keys, once-confirmed decision and 「완료를 막습니다」 | Initialization exception and unresolved-state consequences preserved. |
| EN:850–855: authoring materials, no extension CLI commands or automatic loading, preserve review edits unless replacement requested | JA:777–781: authoring status, explicit absent commands/loading, conditional retention | KO:770–774: authoring status, explicit absent commands/loading, conditional retention | No extension runtime capability added. |

## Findings and repairs from the actual strict review

The first semantic pass identified these issues despite passing initial
mechanical checks. They were handed back to translation and repaired before
the final passing assessment.

| Pair | Source and initial output evidence | Repair and final evidence |
|------|------------------------------------|---------------------------|
| JA and KO | EN:633 says tasks have “upstream coverage”. Initial JA:572 「上位要件」 and KO:565 「상위 요구사항」 narrowed coverage to requirements alone. | JA:572 now says 「上位成果物の内容を網羅」; KO:565 says 「상위 산출물의 내용을 포괄」, covering upstream artifacts without that narrowing. |
| KO | EN:304 describes deterministic downstream fixes grounded in authority. Initial KO:291 「결정적인 수정을」 could read as decisive or important fixes rather than uniquely determined ones. | KO:291 now states 「수정 내용이 하나로 결정되면」 and applies that determined correction; KO:292 retains the prohibition on editing requirements. |
| KO | EN:663 describes an upstream contribution draft. Initial KO:594 「상류」 was a literal stream-direction rendering rather than normal software terminology. | KO:594 uses 「업스트림」. KO:794 was also smoothed to 「기준이 되는 원본」 for authoritative sources without altering its instruction. |

An additional exact-order probe found that the shared-worktree sentence initially
placed the branch token before the worktree token for native grammar. Both
protected strings were already byte-identical and their meaning was unchanged.
JA:342 and KO:341 were rephrased naturally to retain the source token order as
well. All 229 inline spans now match the complete source sequence.

Japanese final prose is complete and reads as technical Japanese rather than
untranslated English paragraphs. Korean final prose is complete and uses normal
technical Korean with the glossary's established terms. Remaining English in
examples, inline spans, names, language navigation labels, and protected badge
attributes is required preservation, not an omitted prose translation.

## Mechanical results and reproducible checks

All executable checks used the selected checkout's `.venv/bin/python`, verified
as Python **3.11.13**, from `OUTPUT_ROOT`.

```bash
.venv/bin/python -B -m internal.doc_translation inventory --readme --lang ja,ko
.venv/bin/python -B -m internal.doc_translation verify --readme --lang ja,ko
npx --offline --yes markdownlint-cli@0.42.0 README.ja.md README.ko.md .codexspec/specs/2026-1013-1133ii-codex-docs-maintenance/translation-review-ja-ko.md
```

| Check | Actual result |
|-------|---------------|
| Initial inventory | Exit 0; exactly two readme pairs, ja and ko; pinned source hash above; `errors: []`, `dry_run: false`. |
| Initial target verify | Exit 0; same pairs and hash; `errors: []`. |
| Initial declared target Markdown lint | Exit 0; no output. |
| Verify after semantic repairs and after inline-order repair | Exit 0 on both reruns; same two pairs/source hash; `errors: []`. |
| Final declared Markdown lint including this report | Exit 0; no output. |
| Complete code-block byte comparison | 25 blocks in each; every full source block equals its corresponding target block. |
| Inline span content/order comparison | 229 in each; all content and the complete sequence equal the source after final repair. |
| Source preservation | Source hash remains `200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363` before and after each publication and final check. |
| Language navigation | JA:12 bold 日本語, KO:12 bold 한국어; seven remaining language links including README.md for English; all eight destinations represented. |
| Heading/table/list/link verification | Mechanical helper passed for both; 40 heading levels and source section order retained, same table/list structures, intact external and intentional English-guide links, translated TOC/self-links resolved. |

The additional byte/order probe is reproducible with the same interpreter:

```python
from pathlib import Path
from markdown_it import MarkdownIt

parser = MarkdownIt("commonmark")

def protected(name):
    text = Path(name).read_bytes().decode("utf-8")
    lines = text.splitlines(keepends=True)
    tokens = parser.parse(text)
    blocks = ["".join(lines[t.map[0]:t.map[1]]) for t in tokens
              if t.type in ("fence", "code_block")]
    spans = [c.content for t in tokens if t.type == "inline"
             for c in t.children or [] if c.type == "code_inline"]
    return blocks, spans

source = protected("README.md")
for target in ("README.ja.md", "README.ko.md"):
    assert protected(target) == source
```

No native skill behavior failure was encountered. One auxiliary discovery
search included a nonexistent `package.json` and returned a missing-file error;
the declared lint configuration was obtained from `.markdownlint.json` and
`.pre-commit-config.yaml` and the cached repository-declared version executed
successfully. This discovery error did not write files or skip a required check.
The translation, scoped publication, inventory, verification, and lint commands
had no failed execution. Repository-wide distribution and test gates remain
the parent workflow's responsibility; this report does not claim they ran here.
