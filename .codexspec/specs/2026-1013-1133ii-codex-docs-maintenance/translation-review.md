# Seven-language README Translation and Semantic Review

## Scope and execution

The English source is README.md at commit
bdab1f3705daf5df6d5b11efdf17651f2b9efc94, SHA-256
`200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363`.
It remains byte-identical. All seven existing root variants were completely
translated; the documentation site and historical features were outside this run.

The selected ready workspace is
`/Users/xiaoming/code/codexspec-codexspec-worktrees/2026-1013-1133ii-codex-docs-maintenance`.
The newly generated native skill files in that checkout were explicitly loaded.
A session started from the main checkout was not assumed to refresh its skills.

The actual agent workflow invocations were:

```text
$codexspec:translate-docs --readme --lang all
$codexspec:check-i18n-semantics --readme --lang all --strict
```

These are skill workflows, not executable translation-engine commands. The
coordinator handled Chinese. Independent forward-use workers, applying
skill-creator's complex-skill testing procedure, executed both new entries
for ja,ko; es,fr; and de,pt-BR. Each read the complete English source, glossary
and its complete actual written targets, compared propositions and native prose,
returned repairs to translation, and rechecked the repaired output. Translation
and semantic review were separate phases; no human native-speaker review is claimed.

## Per-language outcomes

Every row is a strict semantic PASS after actual complete-pair assessment.
No unresolved omission, changed behavior, terminology or navigation defect remains.
The linked reports retain the detailed assessment and repairs for each pair.

| Language | Source → target | Final target SHA-256 | Semantic evidence |
|----------|-----------------|----------------------|-------------------|
| zh | README.md → README.zh-CN.md | `0a36f1bf37b3a50b4b5ffc7e51d5b94658a5ecd1046585e3e81a1423e1c1b7fa` | Complete Chinese assessment below |
| ja | README.md → README.ja.md | `d0238755b1a851e0ea135b6d84f2d41946e571018e98e94ea877b66a2da43290` | [Japanese/Korean assessment](translation-review-ja-ko.md) |
| ko | README.md → README.ko.md | `9f373c9d6663d11bed18750109873864ab5e42673f9efbe0cc96ea5a787cac70` | [Japanese/Korean assessment](translation-review-ja-ko.md) |
| es | README.md → README.es.md | `282698a07bbe3c63008bf4243e06b53b9af5b94f0a00866acb88a394512ae715` | [Spanish/French assessment](translation-review-es-fr.md) |
| fr | README.md → README.fr.md | `712081a02de063803778f742627c6bdadbbc597b0ac84bdfb31917a60a110541` | [Spanish/French assessment](translation-review-es-fr.md) |
| de | README.md → README.de.md | `b31a67037f9f54996078160e1fe904ba6a800454708886803ced60f5aa64c8fb` | [German/Portuguese assessment](translation-review-de-pt.md) |
| pt-BR | README.md → README.pt-BR.md | `4009086fa4e715a993967ba170016949ff6719f77a75ef9419eb6bdf28748a86` | [German/Portuguese assessment](translation-review-de-pt.md) |

## Complete Chinese assessment

The coordinator read the actual complete translated prose, headings, HTML summaries,
tables, lists and navigation from disk. Protected source examples were separately
compared with the actual target. The following covers all source sections and
their conditions, ordering, defaults, exclusions and consequences.

| Source section | Chinese section start | Meaning assessed and actual target evidence |
|----------------|-----------------------|--------------------------------------------|
| Introduction, README.md:22 | README.zh-CN.md:22 | User decides what/why; agent develops how within confirmed intent. “你决定**做什么**以及**为什么做**”；“在这些已确认需求的范围内”. Both hosts, default separate worktrees and optional blueprint retained. |
| Contents, README.md:36 | README.zh-CN.md:31 | All 17 entries translated and retained in order; each self-link resolves to its actual translated heading. |
| Why Choose / Requirements-First, README.md:56 | README.zh-CN.md:51 | All seven need/provision rows retained. “已确认的需求作为功能的最高优先级依据”; goals, constraints, decisions, exclusions, questions and confirmation evidence precede derivation. Automation cannot replace intent. |
| Quick Start, README.md:83 | README.zh-CN.md:73 | Chosen-host initialization, both invocation forms, optional principles, final summary confirmation and returned feature/workspace continuation. Desktop installation link points to its translated heading. |
| Installation and all subsections, README.md:114 | README.zh-CN.md:101 | Complete desktop steps/prompt/language advice, prerequisites, Claude default, both integrations, alternatives and Windows guidance. One-time setup installs commands/runtime; other workflows still need CLI. Update and refresh are separate; force preserves authored content/unset keys and does not leave an old planning alias. Plugin does not initialize/intercept Git; startup and persistent-CLI prerequisites retained. |
| Core Workflow and all subsections, README.md:266 | README.zh-CN.md:233 | All stages/files/purposes and prefix substitution retained. Clarify: “先更新” requirements, then spec, at most five questions/four categories. Analyze: deterministic downstream correction only, “绝不修改” requirements, informational after passing tasks review. Quick confirms/persists compact intent and pauses for new decisions. Auto-next false, statuses and terminal implementation retained; artifact repairs limited to two rounds. |
| Shared Blueprint, README.md:342 | README.zh-CN.md:289 | User decisions before queue entry, all three states, pending-only edits, active/completed read-only, resume before new work, reread queue after each completion. “独立于” auto-next and “不修改该设置”; fixed workspace/branch, concurrent command protection and sequential requirements, evidence-based stop for unresolved product decisions. |
| Worktree Development, README.md:376 | README.zh-CN.md:310 | Definition and one per ordinary feature before first write, reuse/maintenance routing, checkout-local configuration and Git integration, ancestry/divergence verification, fetch warning/local refs and no main fallback. “只有字面 YAML” false disables ordinary isolation; fixed blueprint and selected-init exceptions, retained worktrees without automatic merge/delete. |
| Existing Code, README.md:413 | README.zh-CN.md:332 | Onboard/read-only code, observed conventions and explicit-prohibition constraints, immediate conventions versus in-session constraint decision, preserved knowledge/no invented rationale. Three reverse-spec modes, their conditions/files and all three drift classes; inferred drafts need human confirmation, proposed reconciliation never auto-applied. |
| Review and Debugging, README.md:448 | README.zh-CN.md:357 | Four artifact reviewers, automatic/manual use and separate advisories/score. Complete code delta, explicit selectors, feature does not narrow Git, advisory audit, concrete evidence/trigger/attribution/impact and independent repair verification. Test-first code versus directly checked docs/config. “全新完整功能审查” PASS, coverage/verification and zero admitted P0–P3. Independent maintenance control, all debug stages/escalations/three-failure architectural reassessment, checklist/reference retained. |
| Project Knowledge / History, README.md:508 | README.zh-CN.md:393 | Six categories and complete contents; reusable versus feature intent, read-first guidance, candidate caution and vetted verification/human endorsement. Offline manual actions, recoverable drafts/conflict protection/text fallback. Three hooks with preview exclusion; independent ambient capture, new-material/session dedup, no-write exit and no wait/block. Vetted-only evolve approval. Old unchanged requirements remain, “用户最新的明确决定始终优先”, proposals unconfirmed and retrieval bounded. |
| Git Workflow, README.md:574 | README.zh-CN.md:432 | Exact staged analysis, caller staging, preview/authorized guarded execution; availability gives no invocation/permission. PR/MR text/context resolution; release defaults and all six excluded actions; authenticated matching-remote issues. Runtime prerequisites and contentful/history-only/fast-forward distinctions retained. |
| Available Commands and every category, README.md:606 | README.zh-CN.md:448 | Six public CLI and all 28 agent commands with complete purposes, category order and dual-host prefixes. Tasks table says “覆盖上游产物”, preserving upstream artifacts rather than narrowing to requirements alone. |
| Configuration/i18n and subsections, README.md:681 | README.zh-CN.md:521 | All 13 codes, pt/pt-BR distinction, four dimensions/flags/independent fallback, English templates. TTY prompt conditions and force exception, non-TTY English, retained unset keys. Five exact defaults/effects/controls, all boolean aliases/case/whitespace/destination toggle rules. Reviewer/ask choice, one retained user decision, “待定决策会阻止完成”, override and routed writes. All init/config options and disclosure summaries retained. |
| Project Structure, README.md:809 | README.zh-CN.md:629 | Common and selected integration resources, full protected tree, one dedicated blueprint rather than editable ordinary copies, manual drafts excluded from Git. |
| Extension Materials, README.md:848 | README.zh-CN.md:666 | Authoring materials and guide; no extension-management CLI or automatic manifest hooks/commands; existing review additions/edits retained unless replacement requested. |
| Development, README.md:858 | README.zh-CN.md:670 | Complete protected tooling examples; context/layout before template/package/init changes; authoritative-source edits and regeneration of installed derivatives. |
| Contributing, License, Acknowledgements, README.md:879 | README.zh-CN.md:688 | Local setup/contribution reference, confirmed requirements/traceability/packaging boundary, MIT/license link, spec-kit inspiration and both integrations retained. |

Chinese uses normal technical prose and consistent established terminology.
CLI, Git, Markdown, YAML, PR/MR, product names and protected technical identifiers
remain searchable. Preserved English comments/prompts inside examples do not
indicate untranslated prose. All disclosures and table/heading labels are localized.

## Repairs and command improvements

Actual reading found and repaired narrowed upstream-coverage wording in Chinese,
Japanese and Korean; an ambiguous deterministic-correction phrase in Korean;
literal upstream wording; Spanish coordinated negatives and conflation of
commit history with confirmed requirements; and unnatural correctness-defect
phrases in several languages. The paired reports cite the initial and final
evidence. Repairs preserve source intent rather than add behavior.

The first complete-suite run also exposed established German/Spanish/French
defect-gate term assertions in tests/test_review_code_docs.py. The Portuguese
worker searched the sibling locale and retained its corresponding term as well.
The current translations preserve the established localized terms without
changing those tests. Initial failures remain recorded in verification.md.

This forward-use evidence led to a narrow shared-guide improvement: a full
rewrite now explicitly consults relevant localized guides and existing
documentation-contract tests for terms outside the glossary, and runs those
checks alongside mechanics/lint. Both hosts load that same reference.

## Deterministic outcomes and limits

The all-language command below exited 0 with seven exact pinned pairs and
`errors: []`:

```text
.venv/bin/python -B -m internal.doc_translation verify --readme --lang all
```

Every target retains the 40 heading levels, 25 protected examples, 229 inline
technical spans and 16 tables. Independent external-URL comparisons also pass.
Local files, translated Unicode/self anchors and eight-language navigation pass;
the current language alone is active and English remains a README.md link.
The individual language reports record their actual Markdown lint outcomes.

These checks establish structural/technical preservation. Semantic PASS is
based on the complete actual-pair proposition/native-prose assessment recorded
above and in the paired reports. It is separate from full implementation
acceptance; verification.md and the mandatory isolated code gate cover that work.
