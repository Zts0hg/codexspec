# Confirmed Requirements: Natural README Translations

Status: Confirmed by the explicit user request on 2026-10-14.
Baseline: e35e6be295cf42a931df4b3d8dc405aa3b9f7f93.

## Authority

The user approved the Chinese sample and requested: "效果确实比之前的翻译结果好。 接下来按照你的建议更新 translate-docs 技能，并且重新使用技能将7种语言的文档重新翻译".
This confirms the proposed stronger native-expression requirements without a
second approval question. Earlier requirements in
../2026-1013-1133ii-codex-docs-maintenance/requirements.md remain applicable
except that native expression is now an explicit acceptance requirement.

## Requirements

1. Update the authored translator and shared rules, and regenerate the native
   Codex skill. Write natural technical documentation in the target language:
   use idiomatic syntax, collocations, register and punctuation. Sentence
   splitting, joining and clause reordering may change while preserving every
   source proposition, condition, default, obligation and technical example.
2. Update the corresponding reviewer rules so fidelity and natural expression
   receive separate explicit assessments. Clear translationese, grammatical
   problems and unnatural source-language syntax are defects even when meaning
   survives; only equally idiomatic wording preferences remain optional.
3. Actually use the updated translator and reviewer on all seven existing root
   README variants: zh, ja, ko, es, fr, de and pt-BR. Read complete source and
   outputs, repair observed problems and retain actual assessment evidence.
4. Preserve README.md with SHA-256
   200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363.
   Preserve protected technical content, full content coverage, section order,
   branding, language navigation, examples and valid translated heading links.
5. Keep the repository-only authoring/generation boundary. No public command
   registration, runtime, packaging, version, new language, site-wide rewrite or
   historical-artifact change is required. Translation itself does not stage,
   commit, merge, push or publish.

## Verification

Read-only source-derived skill and distribution checks must pass. Verify all
seven actual target documents mechanically and with Markdown lint and existing
documentation contracts. Assess natural expression by reading the prose;
mechanical agreement, CI status and a previous PASS are not proof of naturalness.
Independent skill forward-tests run only in isolated temporary mirrors; their
actual outputs are inspected before adopting them in the feature workspace.

## 2026-10-14: Approved Chinese introduction

The user explicitly requested the previously approved two-paragraph Chinese
introduction, quoting it in full: "为什么不是翻译成你之前给我看的那段中文".
Use that text verbatim for the corresponding Chinese introduction. The sample
is the style reference for natural expression; glossary defaults and inherited
formatting must not silently replace the user's approved wording. This does not
change protected technical content or authorize modifying the English source.

Approved text:

> CodexSpec 将已确认的需求逐步转化为可追溯的规格说明、设计、计划、任务和具体实现。你来决定做什么、为什么做；智能体则在这些需求的约束下制定实现方案，通过阶段审查把关，并结合长期保存的项目知识推进开发。
>
> 你可以通过 Claude Code 的斜杠命令或 Codex 技能使用 CodexSpec，也可以将两种方式配合使用。常规功能开发默认在各自独立的 Git worktree 中进行。如果需要，还可以使用共享蓝图，让智能体按顺序自主推进已确认需求的开发。
