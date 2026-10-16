# Dépannage sous Windows

## Vérifier l’installation

Utilisez PowerShell pour identifier l’exécutable utilisé et vérifier que la CLI démarre. La commande de version est `codexspec version`.

```powershell
Get-Command codexspec -All
codexspec version
codexspec check
```

## Commande introuvable

Si uv est absent, suivez son guide d’installation. Si CodexSpec a été installé avec uv mais ne figure pas dans `PATH`, vérifiez le répertoire des exécutables, mettez à jour la configuration du shell, puis ouvrez un nouveau terminal. Redémarrez aussi l’assistant s’il a hérité de l’ancien environnement. Le répertoire peut différer de celui par défaut ; utilisez le chemin indiqué par uv.

```powershell
uv tool list
uv tool dir --bin
uv tool update-shell
```

[uv](https://docs.astral.sh/uv/getting-started/installation/) · [uv tool update-shell](https://docs.astral.sh/uv/reference/cli/#uv-tool-update-shell)

## Accès refusé ou échec au démarrage

Un message d’accès refusé ne suffit pas à identifier la cause. Notez la commande exacte, le chemin de l’exécutable, l’erreur et les versions. Vérifiez que le fichier existe, qu’une autre installation n’est pas sélectionnée à sa place et que les permissions ou un logiciel de sécurité n’ont pas bloqué son exécution. Sur un appareil administré, suivez la procédure d’assistance approuvée. Comparez PowerShell et CMD pour isoler les différences d’environnement, sans supposer qu’un changement de shell résout la cause.

Une fois la CLI opérationnelle, initialisez le projet choisi avec l’intégration souhaitée. Le guide d’installation décrit les prérequis et le comportement de mise à jour des projets.

[CodexSpec](getting-started/installation.md)
