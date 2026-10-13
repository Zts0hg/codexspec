# Spanish and French README Translation Review

Date: 2026-10-13. Scope: root README pairs for `es,fr`, full synchronization.
Strict semantic result: **PASS for Spanish; PASS for French** after the repairs
recorded below. No selected pair remains unassessed or has an unresolved finding.

## Invocation, workspace and authority

The delegated real task invoked `$codexspec:translate-docs --readme --lang es,fr`
followed by `$codexspec:check-i18n-semantics --readme --lang es,fr --strict`.
These are agent skills, not shell commands. I explicitly loaded and followed the
selected worktree's native entries:

- `.agents/skills/codexspec-translate-docs/SKILL.md`
- `.agents/skills/codexspec-check-i18n-semantics/SKILL.md`
- `internal/references/doc-translation.md`

The selected source and output workspace was
`/Users/xiaoming/code/codexspec-codexspec-worktrees/2026-1013-1133ii-codex-docs-maintenance`.
Every executable check ran there. The existing-feature resolver returned `ready`
with that same workspace and branch `2026-1013-1133ii-codex-docs-maintenance`:

```text
.venv/bin/python -B .venv/bin/codexspec _worktree-helper resolve --feature 2026-1013-1133ii-codex-docs-maintenance
```

Before translation, I read its AGENTS.md, CLAUDE.md, constitution, configuration,
repository layout, workspace-routing reference, all profile constraints, matching
profile records, current confirmed requirements, and the preceding English README
audit's requirements. The current feature explicitly authorizes the previously
reserved translation work while preserving English and the maintainer-only
boundary. `language.interaction` is `zh-CN`; `language.document` is `en`.

I read the complete actual English README and `docs/i18n/glossary.yml`. Inventory
selected exactly `README.md → README.es.md` and `README.md → README.fr.md`, with
no site selection. Existing targets were preflighted before writes. The inspected
external restoration/writer helpers enforce the explicit worktree, reject escaped
paths, symlinks and non-regular/hard-linked destinations, and require the existing
target's SHA-256 before writing. They were used solely to restore protected source
bytes, localize the active-language header, regenerate self-links and write these
two assigned translations. They did not supply translated prose or semantic verdicts.

## Reviewed baselines

| Language | Source | Target | Result |
|----------|--------|--------|--------|
| es | `README.md` | `README.es.md` | Strict PASS |
| fr | `README.md` | `README.fr.md` | Strict PASS |

Source SHA-256 before inventory, before/after translation, and at final review:

```text
200a4224d7dfd6519fdeecad3a83328e788b8635e696b86edb021286f3f66363
```

Final assessed target SHA-256 values:

```text
README.es.md 282698a07bbe3c63008bf4243e06b53b9af5b94f0a00866acb88a394512ae715
README.fr.md 712081a02de063803778f742627c6bdadbbc597b0ac84bdfb31917a60a110541
```

The reviewer stage read both complete generated files from disk, including all
prose, headings, tables, lists, summaries, navigation and protected examples.
It compared meaning with the already read complete source, section by section;
it did not treat generation intent or mechanical agreement as semantic proof.
After sending the concrete wording repairs back to the translator stage, I read
the changed passages again and repeated verification. Translation and review were
performed sequentially by this forward-test worker; this report does not claim a
separate human reviewer or a separate reviewer subagent.

## Semantic assessment of the actual pairs

The references below identify source sections and actual translated sections.
Quoted clauses are evidence of the specific proposition being assessed; they do
not replace the full-section review. Both translations preserve actors,
conditions, defaults, ordering, prohibitions and consequences.

| Assessed proposition and source evidence | Actual Spanish evidence | Actual French evidence |
|-----------------------------------------|-------------------------|------------------------|
| Introduction and requirements authority: source says “You decide **what** to build and **why**” and confirmed requirements are the “highest-priority feature authority.” | Introduction: “Tú decides **qué** construir y **por qué**”; Requirements-First section: “los requisitos confirmados como la autoridad de mayor prioridad para una funcionalidad.” | Introduction: “Vous décidez **quoi** construire et **pourquoi**”; Requirements-First section: “exigences confirmées l'autorité la plus haute pour une fonctionnalité.” |
| Setup: source offers both assistant integrations, defaults to `claude`, and distinguishes one-time initialization from workflows still needing the CLI. | Installation: “La selección del asistente es `claude` de forma predeterminada”; one-time setup: “siguen invocando la CLI de CodexSpec.” | Installation: “L'assistant sélectionné par défaut est `claude`”; one-time setup: “continuent d'invoquer la CLI CodexSpec.” |
| Upgrade: source retains existing requirements/principles, context bodies and unspecified configuration; `spec-to-plan` is retired “without an alias.” | Upgrade: “se conservan las claves de configuración que no hayas establecido explícitamente”; “sin dejar un alias.” | Upgrade: “les clés de configuration que vous n'avez pas explicitement définies sont conservées”; “sans alias.” |
| Plugin boundary: source says plugin installation “does not initialize a project”; some operations retain CLI requirements, and guidance “does not intercept manual Git commands.” | Plugin: “La instalación del plugin no inicializa un proyecto”; “mantienen sus requisitos de CLI”; “no intercepta comandos Git manuales.” | Plugin: “L'installation du plugin n'initialise pas de projet”; “conservent leurs exigences de CLI”; “il n'intercepte pas les commandes Git manuelles.” |
| Discovery and clarification: source says only explicit confirmation binds the requirements summary; clarify updates requirements first, then the specification. | Core workflow: “Solo la confirmación explícita hace vinculante el resumen”; “Actualiza primero `requirements.md` y después sincroniza `spec.md`.” | Core workflow: “Seule une confirmation explicite rend le résumé des exigences contraignant”; “Il met d'abord à jour `requirements.md`, puis synchronise `spec.md`.” |
| Analysis: source permits downstream deterministic corrections, never edits requirements, and is informational rather than an implementation gate. | Core workflow: “nunca edita `requirements.md`”; “es informativo, no un control que bloquee la implementación.” | Core workflow: “il ne modifie jamais `requirements.md`”; “informatif, sans constituer un contrôle bloquant pour l'implémentation.” |
| Quick: source uses a compact confirmed/persistent requirement summary; broad or unresolved choices need the standard workflow, and Quick pauses for a new decision. | Quick: “confirma y guarda un resumen compacto”; “Quick se detiene cuando necesita una nueva decisión.” | Quick: “confirme et enregistre un résumé compact”; “Quick s'arrête lorsqu'une nouvelle décision est nécessaire.” |
| Stage automation: source defaults auto-next to false, advances on PASS/PASS_WITH_WARNINGS, stops on NEEDS_REVISION/BLOCKED, ends at implement-tasks; artifact repair allows at most two rounds. | Automation: “es **false** de forma predeterminada”; “`NEEDS_REVISION` o `BLOCKED` detiene la cadena”; “un máximo de dos rondas.” All four status tokens remain exact. | Automation: “vaut **false** par défaut”; “`NEEDS_REVISION` ou `BLOCKED` arrête la chaîne”; “au maximum deux cycles.” All four status tokens remain exact. |
| Blueprint: source makes active/completed entries read-only, resumes in-progress work before new work, rereads the queue, and enables auto-dev independently of auto-next. | Blueprint: “las entradas activas y completadas son de solo lectura”; “retoma una funcionalidad en curso antes de empezar otra”; “vuelve a leer la cola”; “no modifica ese ajuste.” | Blueprint: “les entrées actives et terminées sont en lecture seule”; “reprend une fonctionnalité en cours avant d'en commencer une autre”; “relit la file”; “ne modifie pas ce paramètre.” |
| Autonomous execution: source develops requirements sequentially in a fixed shared worktree and stops for unresolved product decisions with evidence instead of normal interactive questioning. | Blueprint: “se desarrollan secuencialmente”; “detienen la ejecución con evidencia, en lugar de solicitar respuestas.” Both fixed worktree/branch identifiers are intact. | Blueprint: “développées séquentiellement”; “arrêtent l'exécution avec des preuves plutôt que de poser des questions.” Both fixed identifiers are intact. |
| Worktrees: source creates before the first requirement write; settings are checkout-local; main-history divergence merges in the new workspace; creation failure never falls back to main writes. | Worktrees: “antes de escribir el primer requisito”; “local a cada checkout”; “Los historiales divergentes se fusionan dentro del nuevo worktree”; “no hacen que se escriba en el checkout principal como alternativa.” | Worktrees: “avant la première écriture des exigences”; “locale à chaque checkout”; “historiques divergents sont fusionnés dans le nouveau worktree”; “ne se rabattent pas sur des écritures dans le checkout principal.” |
| Isolation: source defaults worktrees to true; only literal YAML false disables ordinary isolation; blueprint remains fixed, initialization uses the selected checkout, and completed worktrees are retained. | Worktrees: “solo el valor YAML literal `false`”; “conservan su worktree compartido fijo”; “no los fusiona ni elimina automáticamente.” Initialization exception is explicitly translated. | Worktrees: “seul le booléen YAML littéral `false`”; “conservent leur worktree partagé fixe”; “ne les fusionne ni ne les supprime automatiquement.” Initialization exception is explicitly translated. |
| Existing code: source's onboard writes candidate knowledge, requires a session decision for constraints, preserves existing knowledge, and does not invent past rationale/pitfalls. | Existing code: “requieren una decisión en la sesión para guardarlas, editarlas o descartarlas”; “no inventa justificaciones de decisiones pasadas.” | Existing code: “nécessitent une décision dans la session : conserver, modifier ou abandonner”; “n'invente ni la justification de décisions passées.” |
| Reverse-spec: source has overview/generate/reconcile modes, distinguishes inferred from confirmed baselines, reports three drift types, and never automatically applies reconciliation directions. | Three mode bullets remain complete; “Los borradores inferidos requieren confirmación humana”; “no la aplica automáticamente.” | Three mode bullets remain complete; “Les brouillons inférés nécessitent une confirmation humaine”; “sans l'appliquer automatiquement.” |
| Code review: source includes committed/staged/unstaged/untracked non-ignored changes; feature context does not narrow Git scope; audit returns an advisory rather than acceptance. | Review: “registrados en commits, preparados, no preparados y no rastreados”; “sin reducir el alcance de Git”; “en lugar de un veredicto de finalización.” | Review: “committés, indexés, non indexés et non suivis”; “sans restreindre le périmètre Git”; “plutôt qu'un verdict d'achèvement.” Both retain the non-ignored condition. |
| Acceptance and maintenance: source requires a fresh complete-feature PASS, completed coverage/verification and zero admitted P0–P3 defects; disabling maintenance does not waive defects/checks. | Review: “un `PASS` nuevo de la funcionalidad completa”; “ningún defecto P0–P3 admitido”; “no exime de corregir defectos ni de realizar las comprobaciones obligatorias.” | Review: “un nouveau `PASS` sur la fonctionnalité complète”; “aucun défaut P0–P3 admis”; “ne dispense ni de corriger les défauts ni d'effectuer les vérifications obligatoires.” |
| Debug: source preserves investigation → pattern analysis → single hypothesis → failing-test-first fix and requires architectural reassessment after three failed fixes. | Debug: “verificación de una sola hipótesis → corrección precedida de una prueba que falla”; “Tres correcciones fallidas provocan una reevaluación arquitectónica.” | Debug: “vérification d'une hypothèse unique → correction précédée d'un test en échec”; “Trois corrections échouées déclenchent une réévaluation architecturale.” |
| Project knowledge: source distinguishes reusable from feature-specific intent, candidates from vetted records, and manual recoverable drafts from automatic non-blocking capture. | Knowledge: “la intención específica ... permanece en sus requisitos, diseño y plan”; “verificación de los resultados y respaldo humano”; “nunca abre la revisión manual, ni espera a una persona ni bloquea.” | Knowledge: “l'intention propre ... reste dans ses exigences, sa conception et son plan”; “vérification des résultats et une approbation humaine”; “n'attend jamais un humain et ne bloque jamais.” |
| Capture and contribution: source has three wrap-up hooks, excludes commit preview, keeps ambient capture independent of the wrap-up setting, and requires approval before evolve push/PR. | Knowledge: all three hooks listed; “La vista previa de commits no activa la captura”; “independiente del ajuste de cierre”; “aprobación explícita antes de hacer push o abrir una PR.” | Knowledge: all three hooks listed; “L'aperçu d'un commit ne déclenche pas la capture”; “indépendamment du paramètre de fin”; “approbation explicite avant un push ou l'ouverture d'une PR.” |
| Historical requirements: source keeps older unchanged requirements applicable, gives latest explicit user decisions precedence, and excludes open proposals as confirmation. | History: “Los requisitos antiguos que no hayan cambiado siguen siendo aplicables”; “La última decisión explícita ... siempre tiene prioridad”; “no se consideran intención confirmada.” | History: “Les anciennes exigences inchangées restent applicables”; “La dernière décision explicite ... prévaut toujours”; “pas considérées comme une intention confirmée.” |
| Git permissions: source makes staged analysis depend on exact staging, separates caller staging and preview, and says availability alone neither invokes nor authorizes commit. | Git: “El flujo de trabajo que lo invoca elige y prepara los archivos”; “contenido del commit coincide con el análisis”; “no lo invoca ni autoriza un commit.” | Git: “Le flux appelant choisit et indexe les fichiers”; “contenu committé correspond à l'analyse”; “ne l'invoque pas et n'autorise pas de commit.” |
| Delivery boundaries: source preserves release-notes exclusions, authenticated matching-remote issue creation, contentful/history-only merge distinctions and no-commit fast-forwards. | Git: “ni hace commits, ni incrementa versiones, ni crea tags, ni publica ni crea una release”; “coincida con el remoto configurado”; “los avances rápidos no crean commits.” | Git: “ne crée pas de commit, n'incrémente pas les versions ... ne crée pas de release”; “correspond au distant configuré”; “les avances rapides ne créent aucun commit.” |
| Commands: source lists six public CLI commands and 28 agent commands, with equivalent Claude/Codex invocation forms. | Commands: “seis comandos públicos”; “28 comandos”; every named command, category, purpose and inline invocation retained. | Commands: “six commandes publiques”; “28 commandes”; every named command, category, purpose and inline invocation retained. |
| Languages: source's 13 runtime codes are separate from Portuguese documentation's pt-BR; language dimensions independently fall back to output then en; templates stay English. | Configuration: “El código de portugués de la CLI es `pt` ... usan `pt-BR`”; “de forma independiente a `language.output` ... a `en`.” | Configuration: “Le code portugais de la CLI est `pt` ... utilisent `pt-BR`”; “indépendamment sur `language.output`, puis sur `en`.” Both preserve all four dimensions and setters. |
| Initialization: source's TTY language prompt is bypassed only by lang/all three options, not force; non-TTY defaults English; unspecified language keys survive reinitialization. | Configuration: “`--lang` o las tres opciones”; “no omite esta selección de idioma”; “La inicialización sin TTY usa inglés.” | Configuration: “`--lang` ou les trois options”; “il ne supprime pas cette sélection de langue”; “hors TTY utilise l'anglais.” Preservation clause retained in both. |
| Review decisions/config writes: source's boolean switches support aliases/whitespace/case, bare toggle uses destination value; ask decisions are pending, block completion and persist; writes route locally. | Configuration: “invierte el valor actual del checkout de destino”; “Las decisiones pendientes bloquean la finalización”; “no cambia inmediatamente el ajuste efectivo del principal.” | Configuration: “inverse la valeur actuelle du checkout de destination”; “Les décisions en attente bloquent l'achèvement”; “ne modifie pas immédiatement le paramètre effectif du principal.” |
| Structure and extensions: source keeps blueprint in auto-dev, excludes manual drafts from Git, provides authoring materials without extension loading/management CLI, and preserves resource edits unless replacement is requested. | Structure/extensions: “Los borradores ... se excluyen de Git”; “no carga automáticamente los comandos o hooks de `extension.yml`”; “salvo que se solicite su sustitución.” | Structure/extensions: “brouillons ... exclus de Git”; “ne charge pas automatiquement les commandes ou hooks de `extension.yml`”; “sauf si leur remplacement est demandé.” |
| Development and contribution: source requires upstream-source edits/regeneration and preserving confirmed requirements, traceability and the user/maintainer boundary. MIT and both assistant acknowledgements remain present. | Development: “edita sus fuentes autorizadas y vuelve a generarlos”; contribution: “el límite de empaquetado entre usuarios y mantenedores”; License/Acknowledgements complete. | Development: “modifiez leurs sources faisant autorité et régénérez-les”; contribution: “la frontière du packaging entre utilisateurs et mainteneurs”; Licence/Remerciements complete. |

All default values in the settings table were independently compared by meaning:
auto-next false; auto-distill, auto-maintenance and worktrees true; decided-by
reviewer. The corresponding effects and CLI controls remain accurate. Initialization
and configuration option tables, prerequisites, installation methods, detailed
English-guide links, source-linked workflow table, knowledge categories and all
list entries are translated without omission or reordered propositions.

## Naturalness, terminology and navigation

Spanish uses consistent direct instructions, normal technical prose and the
established glossary terms Especificación, Tarea, Flujo de trabajo, Repositorio,
Rama, Plantilla, Comando, Configuración and Internacionalización where their
concepts occur. French uses the corresponding Spécification, Tâche, Flux de
travail, Dépôt, Branche, Modèle, Commande, Configuration and Internationalisation.
Both retain technical/product identifiers and the glossary's keep-English terms.
Worktree, checkout, blueprint, commit and plugin remain recognizable technical
terms; surrounding explanations communicate their behavior. These are not
untranslated English prose sections. English prompts, comments and labels inside
protected code examples deliberately remain source-identical.

The reviewer checked prose, translated table labels, summary labels and heading
text for fluency as well as meaning. Spanish now distinguishes Git commits from
requirement confirmation and makes compound prohibitions explicit. French uses
native phrasing for correctness defects and distinguishes index state clearly.
No substantive readability or glossary finding remains. Optional personal wording
preferences were not converted into defects.

All eight language destinations remain accessible. English links to README.md;
Español is the only active/bold Spanish language and Français is the only
active/bold French language. All 17 source TOC entries keep their order and point
to actual translated headings. The desktop-installation self-link is translated
and rebuilt. Spanish Unicode slugs and French apostrophe/punctuation handling
were checked against their headings; the French question heading's trailing
hyphen reflects the preserved space before its question mark. External links,
branding, badges and intentionally English detailed-guide references are retained.

## Findings repaired through the translator stage

1. Spanish coordinated prohibitions could be read ambiguously: the first version
   said “No prepara archivos, hace commits, incrementa versiones ...” and
   “nunca abre la revisión manual, espera a una persona ...”. The source prohibits
   every action. Repeated `ni` now states that scope explicitly. Source evidence:
   Git Workflow release-notes exclusions and Project Knowledge automatic-capture
   restrictions. Final target evidence appears in the semantic table above.
2. Spanish Git contexts initially used “confirmados” for committed changes/history.
   Requirement confirmation is a different concept in this README. Source evidence:
   “committed local ... history”, default review's “committed” changes, and
   “committed content matches the analysis”. Repairs use “registrado en commits”
   and “contenido del commit”, preserving technical meaning without conflating it
   with product confirmation.
3. Both command-table audit descriptions initially referred literally to quality
   “of paths”. Source Review and Debugging establishes that audit assesses code
   at named paths. Final Spanish says “calidad del código en las rutas indicadas”;
   final French says “qualité du code dans les chemins indiqués”.
4. Literal correctness-defect wording was smoothed in both debug paragraphs.
   Source says “a non-trivial correctness defect needs tracing”. Final Spanish
   uses “un defecto de funcionamiento no trivial requiere rastreo”; final French
   uses “un défaut non trivial affectant le bon fonctionnement nécessite un traçage”.
   The non-trivial condition, tracing requirement and escalation logic are retained.

5. The parent workflow's broader test run exposed two established-terminology
   contract failures in `tests/test_review_code_docs.py`: Spanish's table row had
   “control de defectos” instead of “puerta de defectos”; French had
   “contrôle des défauts” instead of “contrôle de défauts”. The earlier wording
   preserved meaning but failed the repository's explicit continuity requirement.
   I inspected the actual test and the existing Spanish/French command guides,
   which use those established terms, then aligned each translation's benefits,
   review prose and command row consistently. No tests or site docs were edited.

The first four were translation-output repairs identified by actual reading,
not mechanical failures. The fifth was an actual existing documentation-contract
failure found by the parent workflow, and remains recorded even though repaired. They were applied in translator scope; the reviewer role did not expand
writes to English, other languages or site documents. No unresolved finding or
strict-mode advisory remains.

## Actual mechanical outcomes

All commands below ran from the selected output workspace with the local Python
3.11.13 environment where applicable. Their final individual exit codes were zero.

```text
.venv/bin/python -B -m internal.doc_translation inventory --readme --lang es,fr
.venv/bin/python -B -m internal.doc_translation verify --readme --lang es,fr
npx --offline --yes markdownlint-cli@0.42.0 README.es.md README.fr.md
git diff --check -- README.es.md README.fr.md
```

Inventory and verification each reported exactly the two requested pairs, the
pinned source hash, `errors: []` and `dry_run: false`. Markdownlint produced no
findings under the repository's declared configuration. Scoped diff-check
produced no findings. Verification passed both before and after wording repairs.
Each target retains 40 source heading positions and all 25 protected code blocks.
The existing documentation contract was also executed:

```text
.venv/bin/python -B -m pytest tests/test_review_code_docs.py -k 'es or fr' -q
```

Actual result: `16 passed`. The expression matched all 16 collected tests, not
only four locale cases, so this records the actual scope rather than claiming
locale-exclusive execution. This was repeated against the frozen final README
bytes after terminology was aligned consistently. The report records the initial
failure separately from this passing result.

Protected examples, inline technical tokens, structure and navigation passed;
these outcomes support preservation but do not establish semantic equivalence.
The actual prose comparison above establishes the semantic judgment.

The report itself is also included in the final scoped Markdownlint invocation:

```text
npx --offline --yes markdownlint-cli@0.42.0 README.es.md README.fr.md .codexspec/specs/2026-1013-1133ii-codex-docs-maintenance/translation-review-es-fr.md
```

## Forward-test observations and limits

The selected native skills were sufficient to carry the real full README task
through source selection, preflight, complete translation, actual semantic review,
repairs and mechanical verification. Root README mapping, native-entry loading,
source protection and semantic repair routing behaved as documented. The broader
suite did expose a terminology-continuity gap in the initial translation/review:
defect-gate terms are absent from the loaded glossary, and neither the helper's
mechanical checks nor the initial semantic review surfaced the existing localized
documentation contract. The shared rules require established translations, but
the execution checklist did not explicitly direct the worker to relevant existing
documentation-contract tests. Future executions should consult those contracts
and corresponding locale terminology as well as the glossary. This actual failure
and repair are recorded above; the final output passes the contract. An initial operator attempt to invoke `python -m codexspec`
failed because the package has no `__main__`; the existing CLI script invocation
shown above corrected it and resolved the workspace. That attempt was not an
instruction in either skill and is not reported as a skill defect.

This report claims only the two actual full README pairs. It does not claim that
this forward test exercised site mode, dry-run, incremental selection, unsupported
language handling or every helper safety failure. The parent workflow owns broader
implementation checks and final feature acceptance. This worker wrote only
README.es.md, README.fr.md and this feature-local evidence report in the checkout;
it did not stage, commit, merge, push, publish, alter the English source, add a
language, change public commands or perform site-wide translation.
