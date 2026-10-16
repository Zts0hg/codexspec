---
name: codexspec:update-workflow-diagrams
description: Update CodexSpec README workflow diagrams and synchronize eight languages and light/dark assets
---

# Repository Workflow Diagram Maintenance

This is repository-maintainer tooling, not a command installed into user projects.
Use it for changes to this repository's workflow diagrams and their README assets.

## User Input

the text after the $codexspec:update-workflow-diagrams skill mention

## Workflow

Read the selected checkout's AGENTS.md/CLAUDE.md, constitution and configuration.
Before writes, load `internal/command_templates/fragments/workspace-routing.md`
and use its ready output workspace throughout. Read the selected workspace's
`internal/workflow_diagrams/README.md` and follow its complete update procedure;
it is the shared authority for source files, regeneration, inspection and recovery.
Use the configured interaction language when reporting results.

Translate catalog text using the Shared translation rules section of
`internal/references/doc-translation.md` and `docs/i18n/glossary.yml`. The Markdown
translation selectors are not catalog inputs. Preserve approved wording where its
meaning is unchanged; review every affected locale for fidelity and natural usage.

Map the requested change to the canonical template, catalog or layout overrides.
Keep generated locale files as outputs. Rebuild all eight editable diagrams and
sixteen themed images, validate freshness and README references, and inspect actual
renders. Adjust language-specific geometry or wrapping when needed; do not omit
meaning or blindly shrink text to fit. Follow existing authorization for visual
acceptance, and do not treat command success as proof of semantic/readability checks.

Report changed concepts/locales, actual checks and visual outcomes, outstanding
limitations, and absolute paths to the requested previews. This command does not
stage, commit, merge, push or release; an enclosing authorized workflow owns those
steps after the update is complete.
