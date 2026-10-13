---
name: codexspec:check-i18n-semantics
description: Review semantic fidelity and navigation of CodexSpec repository README or site translations
---

# Repository Translation Semantic Reviewer

This is CodexSpec maintainer tooling, not a command distributed to user projects.

## User Input

the text after the $codexspec:check-i18n-semantics skill mention

## Workflow

Read `internal/references/doc-translation.md` in the selected checkout. Follow
its workspace/language/selection rules, shared translation rules, and Semantic
reviewer execution section. Read every complete source/target pair and independently
assess meaning; mechanical agreement is not semantic evidence.

Use --readme or an explicit README.md source for root README variants. Default
selection remains site documentation. Report missing content, changed meaning,
terminology, readability and navigation findings with concrete evidence.
Review is read-only; send repairs to the translator/calling workflow.

```text
$codexspec:check-i18n-semantics --readme --lang all --strict
$codexspec:check-i18n-semantics user-guide/installation.md --lang ja
$codexspec:check-i18n-semantics --lang zh --strict
```
