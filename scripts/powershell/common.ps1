#!/usr/bin/env pwsh
# Common PowerShell functions for CodexSpec scripts

function Get-RepoRoot {
    try {
        $result = git rev-parse --show-toplevel 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $result
        }
    } catch {
        # Git command failed
    }

    # For non-git repos, walk upward from the current directory.
    $current = (Resolve-Path ".").Path
    while ($true) {
        if (Test-Path (Join-Path $current ".codexspec") -PathType Container) {
            return $current
        }
        $parent = Split-Path $current -Parent
        if (-not $parent -or $parent -eq $current) {
            break
        }
        $current = $parent
    }

    # Last-resort fallback for callers outside a project.
    return (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
}

function Get-CurrentBranch {
    if ($env:CODEXSPEC_FEATURE) {
        if (Test-FeatureName -Name $env:CODEXSPEC_FEATURE) {
            return $env:CODEXSPEC_FEATURE
        }
        return ""
    }

    # Then check git if available
    try {
        $result = git rev-parse --abbrev-ref HEAD 2>$null
        if ($LASTEXITCODE -eq 0) {
            return $result
        }
    } catch {
        # Git command failed
    }

    # For non-git repos, resolve only when exactly one feature exists.
    $repoRoot = Get-RepoRoot
    $specsDir = Join-Path $repoRoot ".codexspec/specs"

    if (Test-Path $specsDir) {
        $features = @(
            Get-ChildItem -Path $specsDir -Directory |
                Where-Object { Test-FeatureName -Name $_.Name }
        )
        if ($features.Count -eq 1) {
            return $features[0].Name
        }
    }

    return ""
}

function Test-FeatureId {
    param([string]$Id)
    return $Id -match '^[0-9]{4}-[0-9]{4}-[0-9]{4}[a-z0-9]{2}$'
}

function Test-FeatureName {
    param([string]$Name)
    # Timestamp names are the only supported feature naming contract.
    # Artifact-level legacy mode does not permit sequential NNN-name directories.
    return $Name -match '^[0-9]{4}-[0-9]{4}-[0-9]{4}[a-z0-9]{2}-[a-z0-9][a-z0-9-]*$'
}

function Test-HasGit {
    try {
        git rev-parse --show-toplevel 2>$null | Out-Null
        return ($LASTEXITCODE -eq 0)
    } catch {
        return $false
    }
}

function Test-FeatureBranch {
    param(
        [string]$Branch,
        [bool]$HasGit = $true
    )

    # For non-git repos, we can't enforce branch naming but still provide output
    if (-not $HasGit) {
        Write-Warning "[codexspec] Warning: Git repository not detected; skipped branch validation"
        return $true
    }

    if (-not (Test-FeatureName -Name $Branch)) {
        Write-Output "ERROR: Not on a feature branch. Current branch: $Branch"
        Write-Output "Feature branches must use YYYY-MMDD-HHMMxx-name"
        return $false
    }
    return $true
}

function Get-FeatureDir {
    param([string]$RepoRoot, [string]$Branch)
    Join-Path $RepoRoot ".codexspec/specs/$Branch"
}

function Get-FeaturePathsEnv {
    param([string]$Feature)

    $repoRoot = Get-RepoRoot
    $currentBranch = Get-CurrentBranch
    $hasGit = Test-HasGit
    if ($Feature) {
        if (Test-Path $Feature -PathType Container) {
            $featureDir = (Resolve-Path $Feature).Path
            if (-not (Test-FeatureName -Name (Split-Path $featureDir -Leaf))) {
                throw "Invalid feature directory name: $Feature"
            }
        } elseif (Test-Path $Feature -PathType Leaf) {
            $featureDir = (Resolve-Path (Split-Path $Feature -Parent)).Path
            if (-not (Test-FeatureName -Name (Split-Path $featureDir -Leaf))) {
                throw "Invalid feature directory name: $featureDir"
            }
        } else {
            $candidate = Join-Path $repoRoot ".codexspec/specs/$Feature"
            if (Test-Path $candidate -PathType Container) {
                if (-not (Test-FeatureName -Name $Feature)) {
                    throw "Invalid feature directory name: $Feature"
                }
                $featureDir = (Resolve-Path $candidate).Path
            } else {
                if (-not (Test-FeatureId -Id $Feature)) {
                    throw "Invalid feature ID: $Feature"
                }
                $specsDir = Join-Path $repoRoot ".codexspec/specs"
                # A short ID is only a local lookup convenience. The full
                # directory name identifies the workspace.
                $matches = @(
                    Get-ChildItem -Path $specsDir -Directory -ErrorAction SilentlyContinue |
                        Where-Object {
                            (Test-FeatureName -Name $_.Name) -and
                            $_.Name.StartsWith("$Feature-", [System.StringComparison]::Ordinal)
                        }
                )
                if ($matches.Count -eq 1) {
                    $featureDir = $matches[0].FullName
                } elseif ($matches.Count -gt 1) {
                    throw "Multiple feature directories match ID '$Feature'. Pass a full directory or artifact path."
                } else {
                    throw "Feature directory not found: $Feature"
                }
            }
        }
    } else {
        if (-not (Test-FeatureName -Name $currentBranch)) {
            throw "No timestamp feature could be resolved."
        }
        $featureDir = Get-FeatureDir -RepoRoot $repoRoot -Branch $currentBranch
    }

    [PSCustomObject]@{
        REPO_ROOT     = $repoRoot
        CURRENT_BRANCH = $currentBranch
        HAS_GIT       = $hasGit
        FEATURE_DIR   = $featureDir
        FEATURE_SPEC  = Join-Path $featureDir 'spec.md'
        IMPL_PLAN     = Join-Path $featureDir 'plan.md'
        TASKS         = Join-Path $featureDir 'tasks.md'
        REQUIREMENTS  = Join-Path $featureDir 'requirements.md'
        RESEARCH      = Join-Path $featureDir 'research.md'
        DATA_MODEL    = Join-Path $featureDir 'data-model.md'
        QUICKSTART    = Join-Path $featureDir 'quickstart.md'
        CONTRACTS_DIR = Join-Path $featureDir 'contracts'
    }
}

function Test-FileExists {
    param([string]$Path, [string]$Description)
    if (Test-Path -Path $Path -PathType Leaf) {
        Write-Output "  [OK] $Description"
        return $true
    } else {
        Write-Output "  [MISSING] $Description"
        return $false
    }
}

function Test-DirHasFiles {
    param([string]$Path, [string]$Description)
    if ((Test-Path -Path $Path -PathType Container) -and (Get-ChildItem -Path $Path -ErrorAction SilentlyContinue | Where-Object { -not $_.PSIsContainer } | Select-Object -First 1)) {
        Write-Output "  [OK] $Description"
        return $true
    } else {
        Write-Output "  [MISSING] $Description"
        return $false
    }
}

function Write-LogInfo {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-LogSuccess {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-LogWarning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-LogError {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}
