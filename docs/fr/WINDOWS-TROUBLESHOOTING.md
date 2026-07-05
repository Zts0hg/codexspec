# Guide de dépannage Windows

Ce guide aide les utilisateurs Windows à résoudre les problèmes courants lors de l'installation et de l'exécution de CodexSpec.

## Problème : « spawn codexspec access denied » (OSError 5) dans CMD

### Symptômes

- L'exécution de `codexspec --version` ou `codexspec init` dans CMD échoue avec « Access denied » ou « spawn codexspec access denied (OSError 5) »
- Les mêmes commandes fonctionnent correctement dans PowerShell

### Cause racine

Ce problème provient des différences de gestion des variables d'environnement utilisateur entre Windows CMD et PowerShell :

1. **Rafraîchissement de la variable d'environnement PATH** : lorsque uv installe codexspec, il ajoute `%USERPROFILE%\.local\bin` au PATH utilisateur. PowerShell le reconnaît généralement immédiatement, tandis que CMD peut ne pas rafraîchir les variables d'environnement avant le redémarrage du terminal.

2. **Différences de création de processus** : CMD utilise l'API Windows CreateProcess, tandis que PowerShell emploie un mécanisme différent, potentiellement plus tolérant aux problèmes de résolution de chemin.

### Solutions

#### Solution 1 : utiliser PowerShell (recommandé)

La solution la plus simple consiste à utiliser PowerShell au lieu de CMD :

```powershell
# Installer et exécuter codexspec dans PowerShell
uv tool install codexspec
codexspec --version
```

#### Solution 2 : redémarrer CMD

Fermez toutes les fenêtres CMD et ouvrez-en une nouvelle. Cela force CMD à recharger ses variables d'environnement.

#### Solution 3 : rafraîchir manuellement le PATH dans CMD

```cmd
# Ajouter le répertoire bin de uv au PATH pour la session courante
set PATH=%PATH%;%USERPROFILE%\.local\bin

# Vérifier
codexspec --version
```

#### Solution 4 : utiliser le chemin complet

```cmd
# Exécuter codexspec via son chemin complet
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### Solution 5 : ajouter au PATH système de façon permanente

1. Ouvrir **Propriétés système** → **Variables d'environnement**
2. Trouver `Path` dans les **Variables utilisateur** ou les **Variables système**
3. Ajouter : `%USERPROFILE%\.local\bin`
4. Cliquer OK et redémarrer tous les terminaux

#### Solution 6 : utiliser pipx au lieu de uv tool

Si uv continue de poser problème, utilisez pipx comme alternative :

```cmd
# Installer pipx
pip install pipx
pipx ensurepath

# Redémarrer CMD, puis installer codexspec
pipx install codexspec

# Vérifier
codexspec --version
```

## Étapes de vérification

Pour diagnostiquer le problème, exécutez ces commandes dans CMD :

```cmd
# Vérifier si le répertoire bin de uv est dans le PATH
echo %PATH% | findstr ".local\bin"

# Vérifier si l'exécutable codexspec existe
dir %USERPROFILE%\.local\bin\codexspec.*

# Tenter l'exécution avec le chemin complet
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## Problèmes courants

### Problème : « uv is not recognized »

**Cause** : uv n'est pas installé ou n'est pas dans le PATH.

**Solution** :

```powershell
# Installer uv avec PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Redémarrer le terminal et vérifier
uv --version
```

### Problème : « python is not recognized »

**Cause** : Python n'est pas installé ou n'est pas dans le PATH.

**Solution** :

1. Installer Python 3.11+ depuis [python.org](https://www.python.org/downloads/)
2. Lors de l'installation, cocher « Add Python to PATH »
3. Redémarrer le terminal

### Problème : antivirus bloquant l'exécution

**Symptômes** : codexspec fonctionne brièvement puis s'arrête, ou affiche des erreurs intermittentes.

**Solution** : ajoutez codexspec à la liste blanche de votre antivirus :

- **Windows Defender** : Paramètres → Mise à jour et sécurité → Sécurité Windows → Protection contre les virus et menaces → Gérer les paramètres → Exclusions
- Ajouter le chemin : `%USERPROFILE%\.local\bin\codexspec.exe`

## Ressources connexes

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) — problèmes connus de permission Windows avec uv
- [Guide d'installation uv pour Windows](https://docs.astral.sh/uv/getting-started/installation/)
- [Documentation pipx](https://pypa.github.io/pipx/) — installeur alternatif d'applications Python
