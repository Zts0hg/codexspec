# Independent Native Skill Forward-Test: German and Brazilian Portuguese

Date: 2026-10-14. Selected languages: `de,pt-BR`.

The complete German and Brazilian Portuguese READMEs were retranslated from the
current English README, then read as complete target-language technical documents
and compared with the source. The strict semantic workflow found passages requiring
repair; those repairs were returned to the translator workflow. After repair,
there are no unresolved fidelity or natural-expression defects in either pair.
Selected mechanical verification, Markdown lint, documentation contracts, and
native skill/distribution checks pass. Target bytes are stable for caller inspection.

This is an agent assessment of actual text. It is not native-human certification,
and the mechanical tests do not prove meaning or natural expression.

## Scope, isolation, and authority

`SOURCE_ROOT` and `OUTPUT_ROOT` were both
`/private/tmp/codexspec-native-forward-de-pt-sl7s6e5v`. The supplied mirror's literal
`workflow.worktrees: false` selects in-place work. No worktree was created.
The persistent task outputs are only `README.de.md`, `README.pt-BR.md`, and this
report. English, other translations, skills, shared rules, glossary, configuration,
code, tests, and existing historical artifacts were not changed. No staging,
commit, merge, push, publication, or child-agent delegation occurred.

The report was initially absent. The caller initialized it as an empty regular
single-link file after I reported the literal existing-file preflight requirement.
Every target write, repair, lint operation with `--fix`, and report write was
preceded by physical containment, full ancestry, regular-file, and one-hard-link
checks. Translator writes additionally used `O_NOFOLLOW`, compared the open file's
identity with preflight, and pinned the English hash before and after writing.
All three output paths are physically contained in the mirror and have no symlink
ancestor. The mirror retained its own environment and editable source installation.

The following actual mirror entrypoints were loaded, not inferred from the calling
session's registered copies:

- `.agents/skills/codexspec-translate-docs/SKILL.md`
- `.agents/skills/codexspec-check-i18n-semantics/SKILL.md`
- `internal/references/doc-translation.md`
- `internal/command_templates/fragments/workspace-routing.md`

I read the mirror's `AGENTS.md`, `CLAUDE.md`, project constitution, repository-layout
reference, configuration, and every profile constraint. I scanned profile headings
and applicability conditions and read the relevant environment, source-path,
filesystem, newline, and external-fixture records. Confirmed requirements from
`2026-1012-2306uu-readme-feature-audit`,
`2026-1013-1133ii-codex-docs-maintenance`, and
`2026-1014-193481-readme-native-expression` establish the English baseline,
root-README mapping, actual translation/review execution, the maintainer-only
boundary, and natural expression as a separate required acceptance condition.
The newest request extends the earlier translation work rather than replacing
its source-preservation and coverage constraints.

I loaded `docs/i18n/glossary.yml` and inspected the existing German and Portuguese
workflow and configuration guides and `tests/test_review_code_docs.py` before
rewriting. Established terms retained include Projektverfassung, Spezifikation,
Workflow, Repository, Branch, and German Defekt-Gate; Brazilian Portuguese uses
Constituição do Projeto, especificação, projeto técnico, fluxo de trabalho,
repositório, branch, and gate de defeitos. The two gate terms are explained in prose
and retained in the command-table rows required by the existing contracts.
No approved target-language passage or expected answer was supplied for these pairs.

## Workflow execution

The actual request executed was:

```text
$codexspec:translate-docs --readme --lang de,pt-BR
$codexspec:check-i18n-semantics --readme --lang de,pt-BR --strict
```

These are instruction-driven agent workflows, not translation-generating Python
commands. `internal.doc_translation` was used for read-only inventory and
mechanical verification. The full English README and both complete old targets
were read. The translator then authored the complete new prose, headings, table
cells, notices, and summary labels, using the English section order. An external
scratch renderer inserted the exact 25 source fence blocks and branding scaffold
so that examples and their comments remained byte-identical. English navigation
became a link, and each target's own language became active. Translated TOC and
self-links follow the actual translated headings.

After writing, I explicitly applied the reviewer entry's strict workflow to the
actual files. Both complete targets were reread from disk in consecutive full-file
chunks, first as German/Brazilian Portuguese technical documentation, then against
the source propositions. This read was not replaced by the translator's intent or
by a test result. The reviewer returned the supported repairs listed below without
editing during its read-only assessment. The translator/calling phase applied them,
pinned the source again, and reread the repaired passages in their actual surrounding
sections. Final verification assessed the resulting bytes. The full review of
unchanged paragraphs plus that repair review covers the final complete documents.

## Source and output identity

All hashes are SHA-256 over the actual file bytes.

| File | Hash | Final size |
|---|---|---|
| `README.md` | `200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363` | Unchanged source |
| `README.de.md` | `027a56eec7331bede806b3bad244c6be7a0b34584d2677722ae2144bf9d99c3a` | 48,224 bytes; 965 lines |
| `README.pt-BR.md` | `703a790413ab0d291790461e1fa7845de109ebfe6c809b17b5312efa31c99779` | 47,376 bytes; 950 lines |

The English hash matches the confirmed native-expression requirement and the
inventory baseline. Full-source hashes were checked before/after translator writes
and after validation. Final lint left both target hashes unchanged.

## Complete section and proposition coverage

Both source/target pairs were examined across the entire document, including the
installation prompt, all later workflow boundaries, all command-table rows,
configuration details, and the final contribution/license/acknowledgement sections.
The following table records the source propositions assessed, in source order;
`Covered` means a prose comparison was performed for both German and Portuguese,
not merely that a heading or token count matched.

| English source section | Propositions compared in both target documents | Result |
|---|---|---|
| Branding, introduction, language/site navigation | Product identity; confirmed requirements become traceable artifacts; human what/why versus agent how; review and persistent knowledge; two integrations; default separate worktrees; optional autonomous confirmed queue; all eight language destinations | Covered |
| Table of Contents | All 17 original TOC entries, order, translated labels and actual self-anchors | Covered |
| Why Choose CodexSpec?; What is Requirements-First SDD? | All seven needs/benefits; confirmed feature authority; goals, constraints, decisions, exclusions, open questions and confirmation evidence; human intent changes; automatic checks; automation cannot silently replace requirements | Covered |
| 30-Second Quick Start | Installation and selected assistant initialization; both invocation forms; optional principles; final confirmation; returned feature directory/workspace; links to continuation and desktop setup | Covered |
| Installation; Install with the Codex Desktop App | Three setup steps; permission conditional; complete English prompt unchanged; latest stable release, prerequisites, user-directory installation, preserve existing state, verify CLI/skills and refresh guidance; Chinese-language substitution | Covered |
| Prerequisites; CLI Installation | Python, uv/pip, assistant and Git requirements; verification commands; new/current project; both integrations; default claude and explicit Codex selection | Covered |
| Alternative installation methods; One-time initialization; Development versions; Windows installation | uvx examples; standalone commit runtime versus CLI requirements for routing/blueprint/profile review; all development install forms; PowerShell example and PATH troubleshooting | Covered |
| Upgrade and Refresh a Project | CLI update versus installed-project refresh; selected integrations; exact force behavior; migration/update/compliance confirmation; preservation of requirements, principles, context bodies and unrelated settings; design-to-plan replacement without alias | Covered |
| Plugin Marketplace Installation | Complete marketplace example; session and resumed-session guidance; no project initialization; config versus full scaffold; direct commit runtime requirements; remaining CLI requirements; Git/PATH and hook args conditions; agent guidance does not intercept manual Git | Covered |
| Core Workflow | Exact chain and invocation prefixes; all seven phase purposes/outputs; explicit feature directory/worktree identity across sessions | Covered |
| specify, clarify, and analyze | Explicit confirmation authority; maximum five questions across four categories; requirements before spec synchronization; full five-artifact chain; deterministic downstream repairs from upstream authority; never edit requirements; unresolved findings; automatic post-task-review and informational boundary | Covered |
| Small Changes with Quick; Workflow Automation | Bounded-change use; compact confirmed persistent summary; orchestrated stages and reviews; pause for unresolved decisions; auto_next false default; active-workspace setting; final confirmation; PASS/PASS_WITH_WARNINGS advances; NEEDS_REVISION/BLOCKED stops; terminal implementation; maximum two artifact repair rounds; separate advisories and implementation loop | Covered |
| Shared Blueprint and Autonomous Development | User-owned choices before queue entry; pending/in_progress/completed; allowed pending edits versus read-only active/completed entries; document order; resume active first; reread queue and include additions; complete confirmed development cycle; automation independent of and does not change auto_next; shared fixed workspace/branch; concurrent protected maintenance with sequential development; evidence-backed stop for unresolved product decisions; read-only display | Covered |
| Worktree Development | Worktree meaning; one per ordinary feature by default before first requirements write; stable reuse; maintenance routing versus active-feature locality; checkout-local config and Git integration; execute checks in returned workspace; committed local versus fetched remote main history by ancestry; divergent merge/verification; fetch warning/local refs; no fallback on creation failure; literal false exception; fixed autonomous worktree; explicit init checkout; keep completed worktrees without automatic merge/delete | Covered |
| Work with Existing Code | Distinct onboard/reverse goals and read-only code boundaries; convention inference and explicit-prohibition-only constraints; immediate candidate conventions versus session persist/edit/drop for constraints; preserve existing knowledge and do not invent experiential rationale; all overview/generate/reconcile triggers, outputs and drift kinds; requirements govern intent; inferred drafts need confirmation; reconciliation reports direction without applying it | Covered |
| Review and Debugging | All four automatic/manual artifact reviewers, dimensions, distinction between defects and non-gating advice/opportunities and compatibility score; change gate versus whole-code audit; all default Git change kinds and explicit selectors; feature context does not narrow Git scope; shared standards and evidence/trigger/attribution/impact requirements; read-only reviewer and independent repair verification; code test-first versus doc/config direct checks; incremental reuse; fresh full-feature PASS, coverage, verification, zero P0–P3; separate maintenance; auto_maintenance default and disabled obligations; no implement-tasks argument; debug sequence, escalation triggers and three-failed-fix reassessment; requirements checklist | Covered |
| Project Knowledge; Reusing Historical Decisions | All six categories; feature-specific intent stays in owning artifacts; installed constraints/relevant-knowledge guidance; immediate later knowledge; candidate caution and vetted verification/human endorsement; local offline browser and all actions; recoverable draft/conflict protection/text fallback; three auto-distill hooks and preview exclusion; ambient capture independent of wrap-up; session/new-material and cross-session deduplication; early exit/no blocking manual review; vetted-only evolve and explicit contribution approval; scoped history with unchanged decisions, additions, replacements, latest-user precedence, open-proposal exclusion and installation refresh | Covered |
| Git Workflow | Exact examples; staging-only analysis, preview, caller stages, authorization and content recheck; ordinary/SDD/blueprint/auto-dev guidance; availability neither invokes nor authorizes; PR/MR generation and spec file/name/prefix selection; text default; changelog/history/default Unreleased/version label and all six exclusions; tasks-to-issues dependencies/acceptance/authenticated matching remote; runtime placement; contentful versus history-only merges, parent/tree checks and fast-forward boundary | Covered |
| Available Commands and all seven subsections | Six public CLI rows; all 28 distributed agent command rows; two invocation forms; each command purpose, auto-review/analysis, read-only/audit and authorization boundaries | Covered |
| Configuration and Internationalization; Language Dimensions | Config path; English templates; all 13 codes; CLI pt versus docs pt-BR; all four language dimensions, keys, init and later switches, responsibilities; independent fallback to output then English; templates en; exact example; first-time TTY exceptions, force does not suppress choice, non-TTY English, re-init preserves unset keys | Covered |
| Workflow and Review Settings; CLI initialization/configuration options; Configuration example | All five settings, defaults and controls; all accepted boolean spellings/case/whitespace, bare destination-value toggle, YAML booleans; reviewer versus ask, one retained user scenario decision and blocking pending decisions, per-run override; routed config locality; all ten init option rows and ten config option rows; complete YAML unchanged | Covered |
| Project Structure | Common plus selected integration; complete protected tree; shared blueprint only in dedicated autonomous worktree; manual review drafts excluded from Git | Covered |
| Extension Materials | Three authoring materials; no extension CLI install/list/remove; no automatic extension command/hook loading; project-specific shared review resources; preserve edits/additions unless replacement requested | Covered |
| Development | Complete developer example, optional dev/docs extras; required context/layout reading before template/packaging/init changes; generated copies and authoritative-source regeneration | Covered |
| Contributing; License; Acknowledgements | Local setup/contribution link; confirmed requirements, traceability and user/maintainer boundary; MIT/LICENSE; spec-kit inspiration; both integrations | Covered |

The source parser and both actual outputs have 40 Markdown headings with identical
hierarchy, 25 identical fenced examples, 16 tables with matching structures and
raw row widths, and 229 inline-code occurrences covering 180 distinct tokens.
The check compares exact examples and inline-token multisets, not just these counts.
All source sections, lists and table rows remain in order. External URLs and links
to intentionally English detailed guides remain unchanged. All eight root-language
navigation destinations remain present, with each target active and English linked.
These structural facts support coverage verification but do not establish meaning.

## Separate per-language outcomes

| Language and pair | Fidelity after repair | Natural expression after repair | Mechanical result | Strict result |
|---|---|---|---|---|
| German: `README.md` → `README.de.md` | PASS: no omitted/added source proposition, actor, condition, default, obligation, exclusion or changed technical example identified | PASS: the complete German prose was assessed for syntax, idiomatic collocations, consistent Sie register, headings and punctuation; no unresolved clear translationese or grammatical defect identified | PASS, zero errors | PASS |
| Brazilian Portuguese: `README.md` → `README.pt-BR.md` | PASS: no omitted/added source proposition, actor, condition, default, obligation, exclusion or changed technical example identified | PASS: the complete Brazilian Portuguese prose was assessed for syntax, natural clause order, collocations, consistent você register, headings and punctuation; no unresolved clear translationese or grammatical defect identified | PASS, zero errors | PASS |

No equal-naturalness preference was promoted into a mandatory fidelity finding.
Conversely, ambiguous file ownership or awkward non-idiomatic expression was not
excused merely because its general meaning could be recovered.

## Actual findings and translator repairs

The strict review of the first new outputs required the following repairs. They
were made only in the two allowed targets. Each final passage was reread in its
section and checked against the corresponding English meaning.

| Finding | Actual first-output evidence | Source meaning and repair |
|---|---|---|
| DE/PT overview file ownership ambiguity | German: “ein knapper Architekturentwurf in `design.md` und `slices.md`”; Portuguese: “um projeto de arquitetura conciso em `design.md` e `slices.md`” | Source overview produces the architecture design and a slices file for module selection. German now distinguishes an architecture draft in `design.md` “sowie `slices.md` zur Auswahl”; Portuguese uses “em `design.md`, além de `slices.md` para escolher”. Both outputs and the selection purpose remain explicit. |
| DE onboarding candidate phrasing and agency | “Konventionen als Kandidaten”; passive “Aus einer erstmaligen Untersuchung werden … erfunden” | Candidate conventions take effect immediately; constraints require a session choice; onboard preserves knowledge and never invents rationale/pitfalls from a cold scan. Now “Konventionseinträge mit Kandidatenstatus” and direct “Onboard bewahrt … und erfindet … weder … noch …”. Corresponding table rows were repaired consistently. |
| DE/PT fallback condition ambiguity | German “`language.output` und danach `en`”; Portuguese “e, em seguida, `en`” | Each dimension falls back independently, with English only if the base is also unset. Final prose states the two absence conditions explicitly in both languages, retaining all four protected technical spans. |
| PT substantive-work scope narrowed in prose | “antes de trabalhos que envolvam decisões substanciais” | Source requires knowledge before substantive work, not only work involving decisions. Changed to “antes de realizar trabalho substancial”. Historical recall now mentions “análises e decisões relevantes” to preserve both judgment types. |
| PT actionable issue described as executable object | “issues do GitHub que possam ser executadas” | Source converts tasks to actionable GitHub issues. Changed to “issues do GitHub que orientem sua execução”, making the tasks' execution the purpose rather than treating an issue as executable software. |
| DE final-body collocation/fragments | “die Nachvollziehbarkeit zu den Quellen”; “Mit Claude Code und OpenAI Codex integriert.” | Source requires traceability and states integrations. Changed to “die Rückverfolgbarkeit zu den Quellen” and “Bietet Integrationen für Claude Code und OpenAI Codex.” |

## Old/new prose examples across the body

These examples compare the supplied old targets with the final outputs, not just
the introduction. Line wrapping is collapsed in short quotations. The changes
illustrate a full translation rewrite, including clauses that now state actors
and conditions directly; they are not a test-based certification of prose quality.

| Language / passage | Supplied old prose | Final prose / retained meaning |
|---|---|---|
| DE / introduction | “der Agent entwickelt das **Wie** innerhalb dieser bestätigten Anforderungen” | “Der Agent erarbeitet innerhalb dieser bestätigten Anforderungen das **Wie**”; same division of responsibility with natural German verb choice |
| DE / plugin analysis | “Analyse bereitgestellter Commits” | “Analyse von Änderungen im Staging-Bereich”; avoids implying already-created commits and states the selected input |
| DE / automation | “führt die abschließende Anforderungsbestätigung zur Spezifikation weiter” | “folgt auf die abschließende Bestätigung der Anforderungen automatisch die Spezifikation”; direct transition wording |
| DE / blueprint protections | “gemeinsamen Besitz- und Schreibschutzregeln” | “gemeinsamen Regeln zur Zuständigkeit und zum Schreibschutz”; preserves ownership/write protections without property-like phrasing |
| DE / worktree baseline | “Die Ausgangsbasis neuer Features vergleicht den lokalen Verlauf …” | “Für die Ausgangsbasis neuer Features wird der bereits in Commits gespeicherte Verlauf des lokalen Hauptbranches … verglichen”; preserves committed local main versus fetched remote main and avoids assigning an action to a baseline |
| DE / reverse-spec | “eine knappe Architektur-`design.md` und `slices.md`” | “einen knappen Architekturentwurf in `design.md` sowie `slices.md` zur Auswahl”; explicit document roles |
| DE / code review | “die aufrufende Korrekturinstanz prüft sie unabhängig” | “Die Stelle, die die Korrektur ausführt, prüft diese Befunde unabhängig”; direct actor description |
| DE / configuration | “Jede spezifische Sprache fällt unabhängig auf `language.output` und anschließend auf `en` zurück” | “Ist für eine Dimension keine spezifische Sprache gesetzt … Ist auch dieser Wert nicht gesetzt, gilt `en`”; preserves independent fallback with explicit conditions |
| PT / introduction | “o agente desenvolve **como** dentro desses requisitos confirmados” | “O agente define **como** fazer isso dentro dos requisitos confirmados”; natural verbal construction |
| PT / project refresh | “os corpos dos arquivos de contexto existentes são preservados” | “Nos arquivos de contexto existentes, as orientações gerenciadas são atualizadas e o restante do conteúdo é preservado”; removes literal body terminology while preserving the edit boundary |
| PT / plugin CLI requirement | “mantêm seus requisitos de CLI” | “continuam exigindo a CLI”; direct dependency statement |
| PT / blueprint protections | “proteções compartilhadas de titularidade e escrita” | “proteções compartilhadas de controle do espaço de trabalho e de escrita”; expresses operational ownership, not legal title |
| PT / worktree baseline | “As bases de novas funcionalidades comparam o histórico local com commits …” | “Para definir a base de uma nova funcionalidade, o histórico já registrado em commits do branch principal local é comparado …”; preserves the local/remote main-branch condition |
| PT / review evidence | “gatilhos alcançáveis” | “condições que possam ocorrer”; retains reachable triggers in ordinary technical prose |
| PT / debug trigger | “um defeito não trivial que afeta a correção do comportamento precisa ser rastreado” | “um defeito não trivial no comportamento do código precisa ser rastreado”; clearer statement of a correctness defect |
| PT / configuration fallback | “Cada idioma específico usa como fallback …” | “Quando uma dimensão não tem um idioma próprio configurado … Se esse valor também não estiver definido, usa `en`”; independent conditional fallback retained |
| PT / extension boundary | “São materiais de autoria” | “Esses materiais servem para criar extensões”; concrete authoring purpose without a literal abstract label |

## Executed checks and outcomes

Every executable project check ran from the mirror with its own `.venv/bin/python -B`.
The interpreter, prefix and imported `codexspec.__file__` were verified inside this
mirror: Python 3.11.13, mirror `.venv`, and mirror `src/codexspec/__init__.py`.
Tests used external fixture/cache directories under physical `/private/tmp`.

| Command / operation | Actual outcome |
|---|---|
| `UV_CACHE_DIR=/private/tmp/codexspec-forward-de-pt-uv-cache uv sync --frozen --extra dev --extra docs --python 3.11.13` | Fresh virtual environment created; dependency fetch timed out for `pyyaml==6.0.3`; exit 1 |
| Same frozen sync with `UV_HTTP_TIMEOUT=90` | Network retry timed out for `mkdocs-material-extensions==1.3.1`; exit 1 |
| `UV_CACHE_DIR=/Users/xiaoming/.cache/uv UV_LINK_MODE=copy uv sync --offline --frozen --extra dev --extra docs --python 3.11.13` | Caller explicitly authorized this shared distribution cache; fresh mirror-owned environment successfully installed 61 pinned packages, including an editable install from this mirror; exit 0 |
| `.venv/bin/python -B -m internal.doc_translation inventory --readme --lang de,pt-BR` | Exactly the two expected root pairs with the confirmed English hash; exit 0 |
| `.venv/bin/python -B -m internal.doc_translation verify --readme --lang de,pt-BR` | Passed immediately after full writes and after repairs; final zero errors; exit 0 |
| `npm_config_cache=/private/tmp/codexspec-forward-de-pt-fixtures/npm-cache npx --yes --package markdownlint-cli@0.42.0 markdownlint --fix README.de.md README.pt-BR.md` | Repository-declared version/configuration/arguments; exit 0. npm emitted a transitive `ini@7.0.0` engine warning on Node 25.6.1, but lint itself succeeded. |
| Cached pinned lint using `npx --offline --yes --package markdownlint-cli@0.42.0 markdownlint --fix README.de.md README.pt-BR.md` | Final lint after repair: exit 0 and both hashes unchanged |
| `.venv/bin/python -B -m pytest tests/test_maintainer_doc_tools.py tests/test_command_template_fragments.py tests/test_review_code_docs.py -q --basetemp=/private/tmp/codexspec-forward-de-pt-fixtures/pytest-tmp -o cache_dir=/private/tmp/codexspec-forward-de-pt-fixtures/pytest-cache` | 231 passed, 6 skipped; exit 0. This includes the existing documentation contract's two selected language terms, not a semantic or native-language test. |
| `.venv/bin/python -B -m pytest tests/test_review_code_docs.py -q --basetemp=/private/tmp/codexspec-forward-de-pt-fixtures/pytest-docs-final -o cache_dir=/private/tmp/codexspec-forward-de-pt-fixtures/pytest-cache` | Final documentation contracts after repair: 16 passed; exit 0 |
| `.venv/bin/python -B -m internal.maintainer_doc_skills --check` | Source-derived native entries current; `changed: []`; exit 0 |
| `.venv/bin/python -B internal/command_template_fragments.py --check-distribution` | Distribution/self-bootstrap/native maintainer parity passed; exit 0 |
| Baseline SHA-256 manifest comparison | Only the two selected README files changed; report is the sole added persistent task file. No bytecode outside `.venv`; English and all other supplied file hashes unchanged. |

The full helper/fragment/documentation check set was run once; after prose repairs,
only the affected documentation contracts and selected mechanical/lint checks were
repeated. No broad product test suite or site-wide rewrite was necessary for these
translation-only outputs. Six existing platform/filesystem-specific test cases
were skipped by the selected suite; they are not counted as passes.

## Instruction weaknesses and remaining limits

The updated instructions successfully require whole-document coverage and separate
fidelity/natural-expression outcomes, and they make clear that helpers only inspect
mechanical properties. Their main residual limitation is that idiomatic expression
remains agent judgment: the glossary gives noun-level terminology, not a complete
locale style guide or native-reviewed examples for difficult workflow prose.
Technical abstracts such as caller, ownership, authority, and baseline can still
produce calques unless the translator reads the actual full output carefully.
The reverse-spec file-role and fallback examples show that a mechanically valid
translation can still benefit from clause restructuring and explicit condition
handling. No instruction, glossary, test, skill, or source rule was edited here.

The strict-review instructions do not prescribe a particular proposition ledger
schema. This report supplies the complete section/condition/actor coverage table
so the reader can assess what was actually compared, rather than relying on a
single unexplained PASS or on matching counts. The read-only reviewer boundary
and separate translator repair phase were honored.

No native human has certified either translation. No claim is made about semantic
acceptance of the five unselected languages or the documentation site. External
URLs were preserved; their live contents and availability were not audited.
Examples intentionally remain in English because the protected-content rules
require exact source examples and comments. The caller should inspect the actual
stable target artifacts and these hashes before adoption. The agent's prose
assessment is additional review evidence, not a substitute for that inspection.
