---
description: Translate CodexSpec repository READMEs or site documentation with shared terminology and fidelity checks
argument-hint: "[source] [--readme] [--lang all|zh,ja,ko,es,fr,de,pt-BR] [--incremental] [--dry-run]"
---

# Repository Document Translator

This is CodexSpec maintainer tooling, not a command distributed to user projects.

## User Input

$ARGUMENTS

## Workflow

Read `internal/references/doc-translation.md` in the selected checkout. Follow
its workspace/language/selection rules, shared translation rules, and Translator
execution section. Retain existing site support and select root READMEs with
--readme or an explicit README.md source.

Translate the complete selected content and verify actual outputs. Then invoke
`/codexspec:check-i18n-semantics` for the same selection; report every failed pair.
A preview does not write translations.

```text
/codexspec:translate-docs --readme --lang all
/codexspec:translate-docs user-guide/installation.md --lang ja
/codexspec:translate-docs --lang zh --incremental --dry-run
```
