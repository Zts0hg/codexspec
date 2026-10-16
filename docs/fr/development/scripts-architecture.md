# Architecture des scripts et de l’installation

## Exécution et sources des commandes

La CLI Python de `src/codexspec/` installe les modèles complets de commandes de `templates/commands/`, les modèles de documents et les critères de revue partagés. Claude Code reçoit des commandes slash ; Codex reçoit des skills natives générées à partir des mêmes sources. Les 28 commandes publiques suivent les mêmes règles de workflow dans les deux environnements.

## Installation et contexte du projet

`codexspec init` sélectionne les scripts auxiliaires adaptés à la plateforme et l’intégration demandée. Les ressources partagées résident dans `.codexspec/`, les commandes Claude dans `.claude/commands/codexspec/` et les skills Codex dans `.agents/skills/`. La CLI installée assure également le routage des espaces de travail et les opérations auxiliaires soumises à des contrôles de protection utilisées par les workflows.

L’initialisation met à jour les blocs gérés par CodexSpec dans les fichiers `AGENTS.md` et `CLAUDE.md` existants, tout en conservant le contenu propre au projet situé en dehors de ces blocs. `--force` actualise les artefacts installés et confirme les demandes de mise à jour ; il ne remplace pas tout le fichier de contexte et ne supprime pas les réglages sans rapport. Installer la CLI ne suffit pas à initialiser un projet.

## Scripts auxiliaires par plateforme

Les projets Unix reçoivent les scripts Bash de `scripts/bash/` ; ceux sous Windows, les scripts PowerShell de `scripts/powershell/`. La création de fonctionnalités et les contrôles des prérequis identifient la fonctionnalité sélectionnée et renvoient un contexte lisible par machine. `common.sh` et `common.ps1` regroupent les utilitaires communs à chaque plateforme ; `review-context` aide à recueillir les informations sur la cible de revue. Sur les deux plateformes, le runtime autonome de commit est copié de `src/codexspec/commit_runtime.py` vers `.codexspec/scripts/commit-staged-helper.py`.

## Identité des fonctionnalités et compatibilité des artefacts

Les noms suivent le format `YYYY-MMDD-HHMMss-name` : un horodatage à la minute, un suffixe de deux caractères alphanumériques minuscules et un nom ASCII. Le nom complet identifie un espace de travail ; utilisez son chemin explicite ou sa branche pour poursuivre. Les identifiants séquentiels `NNN-name` ne sont pas pris en charge. La compatibilité avec les anciennes fonctionnalités porte sur les artefacts : en l’absence de `requirements.md` ou de `design.md`, les commandes signalent les limites de traçabilité au lieu d’inventer une confirmation initiale.

## Maintenance pour les contributeurs

Modifiez les sources de référence, régénérez les copies dérivées et vérifiez la distribution. Les commandes qui utilisent des fragments sont rédigées dans `internal/command_templates/sources/` ; leurs fichiers complets dans `templates/commands/` sont générés. Les autres modèles de commandes restent édités directement. Ne modifiez pas à la main les copies installées pour Claude ou Codex.

Le paquet contient les modèles publics et les deux répertoires de scripts propres aux plateformes. Les outils de maintenance de `internal/`, les sources du site dans `docs/`, les tests ainsi que les sources et images des diagrammes restent hors du paquet installé. N’élargissez pas l’inclusion des scripts à tout `scripts/`.

<a id="extension-materials"></a>

## Ressources pour les extensions

Le dépôt comprend un modèle de manifeste d'extension, un exemple de commande
et un [Guide de développement des extensions](https://github.com/Zts0hg/codexspec/blob/main/extensions/EXTENSION-DEVELOPMENT-GUIDE.md).
Ces ressources servent à créer des extensions. La CLI actuelle ne propose
aucune commande pour installer, lister ou supprimer des extensions et ne charge
pas automatiquement les commandes ou hooks de `extension.yml`. Les ressources
de revue partagées permettent des ajouts propres au projet dans
`.codexspec/review-code/`. L'initialisation conserve les ressources déjà modifiées
et les fichiers supplémentaires, sauf si leur remplacement est demandé.
