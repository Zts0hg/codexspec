# Repository Documentation Translation and Semantic Review

These rules serve CodexSpec maintainers in both Claude Code and Codex. They are
repository-internal, depend on this repository's layout/glossary, and are never
public commands installed into user projects.

## Workspace, language and selection

Read the selected checkout's AGENTS.md/CLAUDE.md, constitution and configuration.
Interaction uses language.interaction, then language.output, then English.
Translation prose uses the selected target language; report artifacts use
language.document, then language.output, then English.

Before writes, read internal/command_templates/fragments/workspace-routing.md
and honor its existing workspace routing. Capture SOURCE_ROOT before routing and
use the returned ready OUTPUT_ROOT for every write and executable check. An
explicit feature workspace stays selected. Preserve the source's provenance;
do not assume a session launched from main reloads another checkout's commands.
For a new worktree, make its CodexSpec CLI available if routing requires it.
Read-only review/preview keeps its selected input without creating a worktree.
Reject symbolic links, non-regular files, hard-linked destinations and escaped
paths before writing. Never alter the English source to make a translation pass.

Parse the supplied arguments:

- --readme selects the selected checkout's root README.md and existing root
  variants. --source README.md also selects this mode. No root directory scan.
- Site mode defaults to docs/en/. A relative page argument such as
  user-guide/installation.md selects that English page. --source may select an
  explicit documentation file/directory inside the checkout. Files beneath
  docs/en retain their path relative to docs/en; custom directories retain their
  own relative paths; a custom single file maps by its filename.
- --lang/-l accepts all (default) or comma-separated target languages.
- --incremental/-i retains the site's missing/newer-target timestamp selection.
  It is a selection hint, not evidence of semantic correctness. A requested full
  README synchronization uses full selection rather than timestamps.
- --dry-run/-d is a read-only preview. List selected source/target pairs and stop
  before generating or writing translations.
- Semantic review accepts --strict: report any semantic drift as a failing
  review. Without it, minor optional prose improvements can remain advisories;
  omissions, changed behavior, broken navigation and clear unnatural expression
  remain defects in either mode.

| Resource language | Accepted aliases | Root README | Site directory |
|-------------------|------------------|-------------|----------------|
| zh | zh, zh-CN | README.zh-CN.md | docs/zh/ |
| ja | ja | README.ja.md | docs/ja/ |
| ko | ko | README.ko.md | docs/ko/ |
| es | es | README.es.md | docs/es/ |
| fr | fr | README.fr.md | docs/fr/ |
| de | de | README.de.md | docs/de/ |
| pt-BR | pt-BR, pt | README.pt-BR.md | docs/pt-BR/ |

Only these seven existing translation resources are supported. They are
distinct from the runtime's 13 CLI language identifiers. Reject unsupported
languages, duplicate normalized targets, unavailable sources or invalid
selection before any translation write. Do not infer new output filenames.

Use the selected checkout's interpreter from OUTPUT_ROOT to run the read-only
inventory (omit --readme for site mode, and add the selected --source when used):

```bash
python -B -m internal.doc_translation inventory --readme --lang all
```

The JSON inventory carries exact relative source/target pairs and source hashes.
Read every selected source; pin hashes and preflight every output before writes.
For --dry-run, pass the flag to inventory and return the pairs without writing.

## Shared translation rules

Load docs/i18n/glossary.yml. Apply keep_english, established translations and
rules by meaning. If unavailable, disclose it and use established technical
terminology; never invent glossary decisions. Before a complete rewrite, inspect
relevant existing localized guides and documentation-contract tests for established
terms not recorded in the glossary; retain those terms while preserving meaning.
Use an explicitly approved target-language sample as a style reference, and retain
approved wording for its corresponding passage unless the user requests a change.
Existing localized prose and glossary defaults do not override that explicit choice.

Translate propositions, not individual words. Preserve actors, conditions,
ordering, must/may/never distinctions, defaults, exclusions and consequences.
Write as if the document were originally authored in the target language for
software developers. Use its normal syntax, idiomatic collocations, technical
register and punctuation; do not mirror English word order or map phrases
word-for-word. Split or join sentences and reorder clauses when that reads
naturally, while preserving every proposition and technical constraint. Use a
consistent established term for each concept. Keep English names when they are
the established searchable term. Natural expression is required, not a preference.

Preserve fenced and indented code examples, command names/arguments, inline
technical spans, environment-variable spellings, paths, external URLs and YAML
frontmatter. Translate prose, headings, table text, notices and summary labels.
Code comments inside protected examples remain unchanged.

Preserve heading hierarchy, source section order, the complete meaning of each
paragraph, table rows and lists. Sentence boundaries and clause order need not
match the source. Do not copy an older target's missing/stale sections or
add capabilities absent from the English source.

Preserve logos and branding. In root READMEs, keep all eight language destinations,
mark the target's own language as active, and make English a link to README.md.
Regenerate TOC and self-links from translated headings using GitHub heading slugs,
including Unicode and duplicate suffixes. Retain external URLs and references
that intentionally point to the English detailed guide. For translated site
references, resolve anchors against their actual destination document.

## Translator execution

1. Establish selected source/target pairs and hashes from inventory; --dry-run
   stops here. Verify all destinations before writing any target.
2. Read each complete source, including its setup, workflow, command, configuration
   and boundary descriptions. Translate the full selected document using the
   shared rules; write only the listed targets in OUTPUT_ROOT. Reread each
   complete target on its own as technical documentation, correcting awkward
   syntax, unnatural collocations and unnecessary translationese before checking
   it against the source again for lost or added meaning.
3. Recheck the source hash before and after writing. If source bytes changed,
   stop and establish a new selected baseline rather than blending revisions.
4. Run the read-only mechanical verification and declared Markdown lint for the
   selected target files and relevant existing documentation-contract tests; fix
   translation, terminology and anchor problems supported by the source/contracts.
5. Invoke the host's check-i18n-semantics entry for the same selection. Retain
   actual per-language review outcomes, repair substantiated issues and verify
   again. Translation generation alone does not establish semantic acceptance.

A translation error identifies the file/language and remains visible. Continue
only independent safe pairs when useful; never report failed pairs as success.
Do not stage, commit, merge, push or publish as part of these commands.

## Semantic reviewer execution

1. Build the selection and read both complete documents for every pair. Review
   the actual output, not a previous translator report or intended result.
2. Compare section-by-section source propositions: purpose, actors, inputs,
   conditions, defaults, ordering, state transitions, exclusions and consequences.
   Check source capabilities and command/options examples are all represented.
3. Assess fidelity and natural expression separately. Read the complete target
   as a target-language document, checking syntax, collocations, register,
   headings and punctuation, then compare its meaning with the source. Changed
   or omitted meaning, clear grammatical errors, non-idiomatic phrasing and
   obvious source-language calques are defects even when mechanically valid
   and semantically recoverable. Only a preference between equally natural,
   accurate phrasings is an optional advisory; do not downgrade translationese
   to a wording preference.
4. Check heading hierarchy, tables/lists, warnings, examples, language navigation
   and links. Run the selected mechanical verification:

   ```bash
   python -B -m internal.doc_translation verify --readme --lang all
   ```

5. Report each language with source/target paths and source hash, assessed
   sections/propositions, separate fidelity and natural-expression outcomes,
   actual mechanical outcomes, findings with source/target evidence, repairs
   where applicable, and optional advisories. When a report file is requested, write it
   only to the authorized feature/report destination; otherwise print the report.
6. Semantic review is read-only. Return repairs to the translator/calling workflow.
   A strict passing result needs all selected pairs assessed, no semantic drift,
   no unresolved fidelity or natural-expression defect and passing applicable
   mechanical checks.

Mechanical checks cover examples, inline tokens, structure and navigation. They
cannot determine whether translated prose has the same meaning; numeric agreement
is never semantic proof. Do not claim installed instructions or test counts
alone demonstrate actual translation quality.

## Maintained entrypoints

The two authored Claude entries select translator/reviewer behavior and load this
reference. Codex entries are generated from those sources by the existing native
renderer. Run these maintainer-only operations from the selected worktree:

```bash
python -B -m internal.maintainer_doc_skills --write
python -B -m internal.maintainer_doc_skills --check
python -B internal/command_template_fragments.py --check-distribution
```

Never hand-edit derived Codex SKILL.md files. A --check operation reports missing
or stale output without repairing it. Generation is explicitly separate from
codexspec init and public template installation.
