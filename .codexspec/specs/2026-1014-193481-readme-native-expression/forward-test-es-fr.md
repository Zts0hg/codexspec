# Independent native-expression forward-test: Spanish and French

Date: 2026-10-14. Selection: `--readme --lang es,fr`; semantic review: `--readme --lang es,fr --strict`.

Both complete translations pass the final agent assessment for fidelity and natural expression. Initial strict-review defects were returned to the translator role and repaired before final acceptance. This is an assessment by an agent, not native-human review. Mechanical tests do not prove idiomatic prose; the prose judgments below come from reading the actual complete documents and comparing their propositions with the source.

## Isolation, entrypoints, and evidence

- Physical selected mirror, `SOURCE_ROOT` and `OUTPUT_ROOT`: `/private/tmp/codexspec-native-forward-es-fr-mg5yl043`. This independent test did not write to the caller's source checkout or sibling feature worktrees.
- The mirror intentionally has no Git repository. Its existing literal `workflow.worktrees: false` was preserved. This selects in-place work in the mirror; no worktree was created and no staging, commit, push, merge or publication was attempted.
- Own environment created with `uv sync --frozen --extra dev --extra docs --python 3.11.13`. No other checkout's environment was reused. Verified `sys.executable` and `sys.prefix` under this mirror's `.venv`, and `codexspec.__file__` under this mirror's `src/codexspec/`.
- Loaded the mirror's actual `.agents/skills/codexspec-translate-docs/SKILL.md`, `.agents/skills/codexspec-check-i18n-semantics/SKILL.md`, and complete `internal/references/doc-translation.md`. The caller supplied a later conditional approved-wording rule; those actual files were reread. No approved Spanish or French sample was supplied, so that conditional did not constrain either translation.
- Loaded selected context/configuration, constitution, workspace-routing rules, all hard-constraint records, applicable environment/path/text-handling profile knowledge and the profile scope/trigger inventory. Relevant confirmed history: `2026-1012-2306uu-readme-feature-audit`, `2026-1013-1133ii-codex-docs-maintenance`, and `2026-1014-193481-readme-native-expression` requirements. The later records authorize these full translations while retaining the English-source and maintainer-only boundaries.
- Read the complete English source and both complete old targets. Loaded the raw `docs/i18n/glossary.yml`, inspected actual Spanish/French command guides and their review-code sections, and read `tests/test_review_code_docs.py` for established terms. Retained `puerta de defectos`, `contrôle de défauts`, blueprint/worktree naming and each locale's existing requirements/specification vocabulary. No glossary or skill files were modified by this agent.
- Before each content write, checked physical containment and each path ancestor, rejecting symlinks, escaped paths, non-regular file destinations and file destinations with multiple hard links. Rechecked the pinned source hash before and after translation writes. Intended persistent outputs are only the two selected READMEs and this report; ignored environment setup is separate.

## Actual hashes

| Artifact | SHA-256 |
|---|---|
| `README.md` | `200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363` |
| `README.es.md` | `53bbd19f379513586bc0da98e11a6d962bd872134162629393aa47b6137478c9` |
| `README.fr.md` | `2206cacb79b3fecbf6d368a4456562dbbe3c23f8e2d2a7d639a672705a172a1a` |

Old Spanish target: `282698a07bbe3c63008bf4243e06b53b9af5b94f0a00866acb88a394512ae715`.
Old French target: `712081a02de063803778f742627c6bdadbbc597b0ac84bdfb31917a60a110541`.
The final English source hash is the required unchanged baseline.

## Complete coverage and fidelity

Each translation was reconstructed from the entire English source, with 150 translated content blocks and all 25 protected fenced examples restored unchanged. This was not an introductory edit or a selective synchronization. Complete actual outputs were then read in three contiguous ranges per language; changed passages were read again after repairs.

The following propositions were checked independently of structural counts in both languages:

| Source area | Propositions checked in Spanish and French |
|---|---|
| Preamble, value proposition, Requirements-First definition | Human owns what/why; agent develops how within confirmed requirements; confirmation has the highest feature authority; reviews and persistent knowledge; optional blueprint and default feature isolation; logos, badges and all language/documentation destinations. |
| Quick start and installation | Claude/Codex invocation forms; explicit confirmation and returned feature identity; desktop instructions and conditional dependency permission; uv/pip/uvx alternatives; Python/Git requirements; default Claude selection; persistent CLI requirements; update versus project refresh; force preserves authored data and unspecified settings; retired spec-to-plan has no alias; plugin does not initialize projects or intercept manual Git. |
| Core workflow and automation | Full requirements→spec→design→plan→tasks chain; clarify asks up to five questions across four categories and updates requirements first; analyze never edits requirements and is informational; Quick pauses for decisions; auto_next defaults false, advances on PASS/PASS_WITH_WARNINGS and stops on NEEDS_REVISION/BLOCKED; terminal implementation; maximum two artifact repair/review rounds. |
| Blueprint and auto-dev | Confirm user-owned direction before queue entry; pending/in_progress/completed states; only pending entries mutable; document order and resume-first; reread queue after completion; automation independent of and does not modify auto_next; fixed shared branch/workspace; concurrent command access protected, requirement development sequential; unresolved product direction stops with evidence. |
| Worktree development | One workspace per ordinary feature; first write occurs after creation; stable reuse; standalone maintenance versus active feature; checkout-local configuration and Git propagation; committed local/fetched remote ancestry; verify divergent merges; failed fetch permits local refs; creation failure never falls back to main; literal YAML false only; blueprint exception; init/update explicit checkout; retention without automatic merge/deletion. |
| Existing code | Both commands read code without editing it; onboard conventions inferred and locally immediate, constraints only from explicit prohibitions and require persist/edit/drop; no invented rationale or experiential pitfalls; reverse-spec overview/generate/reconcile inputs and artifacts; confirmed requirements govern intent; drafts need human confirmation; reconciliation does not automatically apply direction. |
| Review and debugging | Four artifact reviews and compatibility scores; gate versus advisory path audit; complete feature delta includes committed/staged/unstaged/nonignored untracked files; feature context does not narrow Git scope; concrete reachable triggers and attribution; reviewer does not edit, repair caller verifies independently; test-first versus direct document/config work; fresh whole-feature PASS and zero admitted P0–P3; maintenance default true, no waived defects/checks; ordered root-cause process and three-failure reassessment. |
| Project knowledge and historical recall | All six categories and constraint-first reading; candidate versus vetted status; human endorsement; offline browser review, recoverable draft and all-or-nothing conflict checks; text fallback; auto_distill default true and three successful wrap-up hooks; preview excluded; ordinary-chat capture remains independent; deduplication/no-new-material early exit; automatic capture does not await people or block; evolve approval; unchanged historical decisions remain applicable and latest explicit user decision prevails. |
| Git workflow and command catalog | Exact staged-area ownership and authorization; Conventional Commits preview versus guarded execution; PR/MR and optional spec path/name/prefix; changelog section/version label and every exclusion; authenticated issue repository check; in-place runtime prerequisites; contentful/history-only/fast-forward distinctions; six CLI and all 28 distributed commands represented in source order. |
| Language and workflow configuration | All 13 runtime codes and pt versus pt-BR distinction; independent interaction/document/commit fallbacks to output then en; English templates; init and config switches; TTY/base-language prompt exceptions; force does not suppress language selection; non-TTY English and preservation on reinit; all five defaults; valued/bare booleans; reviewer/ask admission and once-only pending decisions; routed settings do not immediately affect main. |
| Structure, extensions, development, contribution, legal closing | Selected assistant resources and common scaffolding; blueprint's sole shared-worktree home; review drafts excluded from Git; extension authoring materials are not install/list/remove or auto-load capabilities; resource edits preserved unless replacement requested; developer extra and checks; authoritative source editing/regeneration; user/maintainer packaging boundary; MIT, acknowledgements and integrations. |

All source headings and subordinate sections are mapped below in the same order. The preamble is additionally covered above.

| Source heading | Spanish target heading | French target heading |
|---|---|---|
| Table of Contents | Índice | Table des matières |
| Why Choose CodexSpec? | ¿Por qué elegir CodexSpec? | Pourquoi choisir CodexSpec ? |
| What is Requirements-First SDD? | ¿En qué consiste SDD con prioridad en los requisitos? | Que signifie SDD avec priorité aux exigences ? |
| 30-Second Quick Start | Inicio rápido en 30 segundos | Démarrage rapide en 30 secondes |
| Installation | Instalación | Installation |
| Install with the Codex Desktop App | Instalar desde la aplicación de escritorio de Codex | Installer depuis l'application de bureau Codex |
| Prerequisites | Requisitos previos | Prérequis |
| CLI Installation | Instalación de la CLI | Installation de la CLI |
| One-time initialization | Inicialización puntual | Initialisation ponctuelle |
| Development versions | Versiones de desarrollo | Versions de développement |
| Upgrade and Refresh a Project | Actualizar CodexSpec y los archivos del proyecto | Mettre à jour CodexSpec et les fichiers du projet |
| Plugin Marketplace Installation | Instalación desde el marketplace de plugins | Installation depuis le marketplace de plugins |
| Core Workflow | Flujo de trabajo principal | Flux de travail principal |
| specify, clarify, and analyze | specify, clarify y analyze | specify, clarify et analyze |
| Small Changes with Quick | Cambios pequeños con Quick | Petits changements avec Quick |
| Workflow Automation | Automatización del flujo de trabajo | Automatisation du flux de travail |
| Shared Blueprint and Autonomous Development | Blueprint compartido y desarrollo autónomo | Blueprint partagé et développement autonome |
| Worktree Development | Desarrollo con worktrees | Développement avec les worktrees |
| Work with Existing Code | Trabajar con código existente | Travailler avec du code existant |
| Review and Debugging | Revisión y depuración | Revue et débogage |
| Project Knowledge | Conocimiento del proyecto | Connaissances du projet |
| Reusing Historical Decisions | Reutilizar decisiones históricas | Réutiliser les décisions historiques |
| Git Workflow | Flujo de trabajo con Git | Flux de travail Git |
| Available Commands | Comandos disponibles | Commandes disponibles |
| CLI Commands | Comandos CLI | Commandes CLI |
| Core Workflow Commands | Comandos del flujo de trabajo principal | Commandes du flux de travail principal |
| Artifact Review Commands | Comandos de revisión de artefactos | Commandes de revue des artefacts |
| Requirements, Existing Code, and Debugging | Requisitos, código existente y depuración | Exigences, code existant et débogage |
| Project Knowledge Commands | Comandos de conocimiento del proyecto | Commandes de gestion des connaissances du projet |
| Git and Code Review Commands | Comandos de Git y revisión de código | Commandes Git et de revue du code |
| Utility Commands | Comandos de utilidad | Commandes utilitaires |
| Configuration and Internationalization | Configuración e internacionalización | Configuration et internationalisation |
| Language Dimensions | Idiomas de interacción, documentos y commits | Langues des échanges, des documents et des commits |
| Workflow and Review Settings | Ajustes del flujo de trabajo y la revisión | Paramètres du flux de travail et des revues |
| Project Structure | Estructura del proyecto | Structure du projet |
| Extension Materials | Materiales para extensiones | Ressources pour les extensions |
| Development | Desarrollo | Développement |
| Contributing | Contribuir | Contribuer |
| License | Licencia | Licence |
| Acknowledgements | Agradecimientos | Remerciements |

## Separate per-language assessment

| Pair | Fidelity | Natural expression | Mechanical/navigation | Strict result |
|---|---|---|---|---|
| `README.md` → `README.es.md` | PASS: no missing or added capability, changed default, weakened exclusion or reordered requirement found after repairs. | PASS by agent judgment: coherent developer register, direct instructions, idiomatic clause structure and collocations; initial ownership calque and ambiguous negative coordination repaired. | PASS: protected content, structures, navigation and anchors. | PASS |
| `README.md` → `README.fr.md` | PASS: all source conditions, authority relationships, ordering, defaults and boundaries retained after repairs. | PASS by agent judgment: consistent formal address, normal French clause structure and punctuation; ownership calque and bare artifact noun calques repaired; strongest-priority wording made explicit. | PASS: protected content, structures, navigation and anchors. | PASS |

Final unresolved fidelity or natural-expression defects: none identified in either pair. No defect was downgraded to an optional wording preference merely because the intended meaning could be recovered.

## Before/after prose evidence

These are excerpts from actual old and final files. Line wrapping is normalized in this table; omissions use an ellipsis.

| Language and passage | Before | After | Assessment |
|---|---|---|---|
| Spanish introduction | “el agente desarrolla **cómo** hacerlo dentro de esos requisitos confirmados” | “el agente se encarga de definir **cómo** hacerlo, siempre dentro de los requisitos que hayas confirmado” | Replaces a literal mapping of develops/how with normal Spanish verbal structure; actor and requirement constraint retained. |
| Spanish assistant default | “La selección del asistente es `claude` de forma predeterminada; elige el valor explícitamente para Codex o ambos.” | “El asistente predeterminado es `claude`: si quieres Codex o ambos, debes indicarlo explícitamente.” | Clear default and condition expressed directly. |
| Spanish baseline ancestry | “Las bases de nuevas funcionalidades comparan, mediante la ascendencia de Git, el historial…” | “Para establecer la base de una nueva funcionalidad, se comparan los historiales de commits…” | Makes the operation the subject of the explanation instead of attributing comparison to an abstract base; committed local/fetched remote and ancestry remain explicit. |
| Spanish language fallback | “Cada idioma específico recurre de forma independiente a `language.output` y, después, a `en`.” | “Si no se define el idioma de una dimensión, se utiliza `language.output` y, en su defecto, `en`. Esta regla se aplica de forma independiente a cada dimensión.” | Explains fallback using an explicit condition instead of personifying a language. |
| French opening artifacts | “spécifications, conceptions, plans, tâches et implémentations traçables” | “spécifications, documents de conception, plans, tâches et implémentations dont la traçabilité est assurée” | Uses the normal artifact noun phrase and an explicit traceability clause. |
| French feature reuse | “Poursuivre une fonctionnalité réutilise son espace de travail.” | “Lorsque vous reprenez une fonctionnalité, son espace de travail est réutilisé.” | Removes an unnatural infinitive-as-actor construction; same reuse behavior. |
| French language fallback | “Chaque langue spécifique se replie indépendamment sur `language.output`, puis sur `en`.” | “Si la langue d'une dimension n'est pas définie, `language.output` est utilisée, puis `en` à défaut.” | Removes the literal “se replie” calque while retaining fallback order and independent dimensions in the next sentence. |
| French governing authority | “fait des **exigences confirmées l'autorité la plus haute pour une fonctionnalité**” | “**les exigences confirmées priment sur toute autre référence pour la fonctionnalité**” | Expresses the source's highest-priority feature authority naturally and explicitly. |

Strict review also rejected wording introduced by the first full translation, even though mechanical verification already passed:

- Spanish/French shared ownership was initially “protecciones compartidas de propiedad y escritura” / “protections communes de propriété et d'écriture”. Legal-property wording is a source-language calque in this context. The translator repaired it to “mecanismos compartidos que controlan quién ocupa el espacio de trabajo y protegen las escrituras” / “mécanismes communs qui contrôlent l'attribution de l'espace de travail et protègent les écritures”. Both retain shared ownership control, write protection and concurrent-command/sequential-requirement distinctions.
- Spanish release-notes initially said “No prepara archivos, crea commits, incrementa versiones…”; the negative scope was too easy to misread. It now says “No prepara archivos, ni crea commits, ni incrementa versiones, ni crea tags, ni publica, ni crea una release.” Every excluded action is unambiguously negative.
- French first repair used “constituent la référence prioritaire”; on rereading, “priment sur toute autre référence” was selected to keep the highest-priority relationship explicit rather than merely call the requirements an important reference.

## Actual verification outcomes

All executable checks used the mirror's own Python 3.11.13 environment. Final reruns followed the actual repairs.

| Check | Actual outcome |
|---|---|
| `.venv/bin/python -B -m internal.doc_translation inventory --readme --lang es,fr` | Exit 0; exactly README.md→README.es.md and README.md→README.fr.md; pinned source hash; no errors. |
| `.venv/bin/python -B -m internal.doc_translation verify --readme --lang es,fr` | Exit 0; both selected pairs; `errors: []` after final repairs. |
| `npx --yes markdownlint-cli@0.42.0 README.es.md README.fr.md` | Exit 0 with repository `.markdownlint.json`; read-only, no `--fix`. Version matches the declared pre-commit hook. |
| `.venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_review_code_docs.py` | Exit 0; 16 passed. Both locale README gate terms and related guide contracts retained. |
| `.venv/bin/python -B -m internal.maintainer_doc_skills --check` | Exit 0; `changed: []`; actual loaded native entries match their authored sources. |
| `.venv/bin/python -B internal/command_template_fragments.py --check-distribution` | Exit 0; no stale or unknown distribution artifacts reported. |
| Additional direct comparison of actual files | Per file: 40 Markdown headings, 25 identical fenced examples, 229 identical protected inline-token occurrences, 16 identical table structures and 119 table-row widths. External HTTP(S) URL multisets exactly equal the source. |
| Actual navigation inspection | All eight language choices retained; target self-language active and English linked. TOC/self-links regenerated from actual translated headings; protected English detailed-guide links and anchors retained. French punctuation creates the expected trailing-hyphen slug for “Pourquoi choisir CodexSpec ?”. |

The semantic skill's `--strict` is an agent review mode, not an option passed to the mechanical helper. Its actual final judgment is documented separately above; helper success was not substituted for that review.

## Weaknesses and remaining limits

There is no native-human linguistic sign-off. The same independent forward-test agent performed translation and subsequent read-only semantic review as separate workflow roles; this is independent of the caller's implementation work, not a second independent human translator. No rendered GitHub browser session or full site build was performed: README Markdown, file references and heading anchors were validated locally. The existing contract-mandated names “puerta de defectos” and “contrôle de défauts” are retained as established project terminology, even though a fresh terminology project might choose different names. They are not treated as permission to retain awkward syntax elsewhere.

No unresolved translation defect is known after the reported repairs. The caller still needs to inspect these actual artifacts before adoption, as required by the independent forward-test procedure. Tests and counts support preservation and navigation; they do not independently establish fidelity or natural expression.
