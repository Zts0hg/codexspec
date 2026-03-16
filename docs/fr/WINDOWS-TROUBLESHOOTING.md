# Guide de Resolution des Problemes Windows

Ce guide aide les utilisateurs Windows a resoudre les problemes courants lors de l'installation et de l'execution de CodexSpec.

## Probleme : "spawn codexspec access denied" (OSError 5) dans CMD

### Symptomes

- L'execution de `codexspec --version` ou `codexspec init` dans CMD echoue avec "Access denied" ou "spawn codexspec access denied (OSError 5)"
- Les memes commandes fonctionnent correctement dans PowerShell

### Cause Racine

Ceci est cause par des differences dans la facon dont Windows CMD et PowerShell gerent les variables d'environnement utilisateur :

1. **Rafraichissement de la variable d'environnement PATH** : Lorsque uv installe codexspec, il ajoute `%USERPROFILE%\.local\bin` au PATH utilisateur. PowerShell reconnait generalement cela immediatement, tandis que CMD peut ne pas rafraichir les variables d'environnement jusqu'a ce que le terminal soit redemarre.

2. **Differences de creation de processus** : CMD utilise l'API Windows CreateProcess, tandis que PowerShell utilise un mecanisme different qui peut etre plus tolerant aux problemes de resolution de chemin.

### Solutions

#### Solution 1 : Utiliser PowerShell (Recommande)

La solution la plus simple est d'utiliser PowerShell au lieu de CMD :

```powershell
# Installer et executer codexspec dans PowerShell
uv tool install codexspec
codexspec --version
```

#### Solution 2 : Redemarrer CMD

Fermez toutes les fenetres CMD et ouvrez-en une nouvelle. Cela force CMD a recharger les variables d'environnement.

#### Solution 3 : Rafraichir Manuellement le PATH dans CMD

```cmd
# Ajouter le repertoire bin de uv au PATH pour la session courante
set PATH=%PATH%;%USERPROFILE%\.local\bin

# Verifier
codexspec --version
```

#### Solution 4 : Utiliser le Chemin Complet

```cmd
# Executer codexspec en utilisant son chemin complet
%USERPROFILE%\.local\bin\codexspec.exe --version
```

#### Solution 5 : Ajouter au PATH Systeme Permanemment

1. Ouvrir **Proprietes systeme** -> **Variables d'environnement**
2. Trouver `Path` dans les **Variables utilisateur** ou **Variables systeme**
3. Ajouter : `%USERPROFILE%\.local\bin`
4. Cliquer OK et redemarrer tous les terminaux

#### Solution 6 : Utiliser pipx au lieu de uv tool

Si uv continue a avoir des problemes, utilisez pipx comme alternative :

```cmd
# Installer pipx
pip install pipx
pipx ensurepath

# Redemarrer CMD, puis installer codexspec
pipx install codexspec

# Verifier
codexspec --version
```

## Etapes de Verification

Pour diagnostiquer le probleme, executez ces commandes dans CMD :

```cmd
# Verifier si le repertoire bin de uv est dans le PATH
echo %PATH% | findstr ".local\bin"

# Verifier si l'executable codexspec existe
dir %USERPROFILE%\.local\bin\codexspec.*

# Essayer d'executer avec le chemin complet
%USERPROFILE%\.local\bin\codexspec.exe --version
```

## Problemes Courants

### Probleme : "uv is not recognized"

**Cause** : uv n'est pas installe ou n'est pas dans le PATH.

**Solution** :

```powershell
# Installer uv en utilisant PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Redemarrer le terminal et verifier
uv --version
```

### Probleme : "python is not recognized"

**Cause** : Python n'est pas installe ou n'est pas dans le PATH.

**Solution** :

1. Installer Python 3.11+ depuis [python.org](https://www.python.org/downloads/)
2. Pendant l'installation, cocher "Add Python to PATH"
3. Redemarrer le terminal

### Probleme : Antivirus Bloquant l'Execution

**Symptomes** : Codexspec fonctionne brievement puis s'arrete, ou affiche des erreurs intermittentes.

**Solution** : Ajouter codexspec a la liste blanche de votre antivirus :

- **Windows Defender** : Parametres -> Mise a jour et securite -> Securite Windows -> Protection contre les virus et menaces -> Gerer les parametres -> Exclusions
- Ajouter le chemin : `%USERPROFILE%\.local\bin\codexspec.exe`

## Ressources Connexes

- [uv GitHub Issue #16747](https://github.com/astral-sh/uv/issues/16747) - Problemes connus de permission Windows avec uv
- [Guide d'Installation uv Windows](https://docs.astral.sh/uv/getting-started/installation/)
- [Documentation pipx](https://pypa.github.io/pipx/) - Installeur d'application Python alternatif
