---
name: codexspec:translate-docs
description: Translate CodexSpec repository READMEs or site documentation with shared terminology and fidelity checks
---

# Repository Document Translator

This is CodexSpec maintainer tooling, not a command distributed to user projects.

## User Input

the text after the $codexspec:translate-docs skill mention

## Workflow

Read `internal/references/doc-translation.md` in the selected checkout. Follow
its workspace/language/selection rules, shared translation rules, and Translator
execution section. Retain existing site support and select root READMEs with
--readme or an explicit README.md source.

Write the complete selected content as natural target-language technical
documentation. Reorganize sentence structure when useful while preserving all
meaning and protected technical content; obvious translationese requires repair.
Honor explicitly approved wording for its corresponding passage.
Verify the actual outputs for both fidelity and natural expression. Then invoke
`$codexspec:check-i18n-semantics` for the same selection; report every failed pair.
A preview does not write translations.

```text
$codexspec:translate-docs --readme --lang all
$codexspec:translate-docs user-guide/installation.md --lang ja
$codexspec:translate-docs --lang zh --incremental --dry-run
```
