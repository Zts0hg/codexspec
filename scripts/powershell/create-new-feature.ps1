#!/usr/bin/env pwsh
# Create a new feature for CodexSpec
[CmdletBinding()]
param(
    [switch]$Json,
    [string]$ShortName,
    [switch]$Help,
    [Parameter(Position = 0)]
    [string]$FeatureDescription
)
$ErrorActionPreference = 'Stop'

# Show help if requested
if ($Help) {
    Write-Host "Usage: ./create-new-feature.ps1 [-Json] [-ShortName <name>] <feature description>"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Json               Output in JSON format"
    Write-Host "  -ShortName <name>   Provide a custom short name (2-4 words) for the branch"
    Write-Host "  -Help               Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  ./create-new-feature.ps1 'Add user authentication system' -ShortName 'user-auth'"
    Write-Host "  ./create-new-feature.ps1 'Implement OAuth2 integration for API'"
    exit 0
}

# Check if feature description provided
if (-not $FeatureDescription) {
    Write-Error "Usage: ./create-new-feature.ps1 [-Json] [-ShortName <name>] <feature description>"
    exit 1
}

$featureDesc = $FeatureDescription.Trim()

# Resolve repository root
function Find-RepositoryRoot {
    param(
        [string]$StartDir,
        [string[]]$Markers = @('.git', '.codexspec')
    )
    $current = Resolve-Path $StartDir
    while ($true) {
        foreach ($marker in $Markers) {
            if (Test-Path (Join-Path $current $marker)) {
                return $current
            }
        }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current) {
            # Reached filesystem root without finding markers
            return $null
        }
        $current = $parent
    }
}

function ConvertTo-CleanBranchName {
    param([string]$Name)

    return $Name.ToLower() -replace '[^a-z0-9]', '-' -replace '-{2,}', '-' -replace '^-', '' -replace '-$', ''
}

function Get-BranchName {
    param([string]$Description)

    # Common stop words to filter out
    $stopWords = @(
        'i', 'a', 'an', 'the', 'to', 'for', 'of', 'in', 'on', 'at', 'by', 'with', 'from',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall',
        'this', 'that', 'these', 'those', 'my', 'your', 'our', 'their',
        'want', 'need', 'add', 'get', 'set'
    )

    # Convert to lowercase and extract words
    $cleanName = $Description.ToLower() -replace '[^a-z0-9\s]', ' '
    $words = $cleanName -split '\s+' | Where-Object { $_ }

    # Filter words
    $meaningfulWords = @()
    foreach ($word in $words) {
        if ($stopWords -contains $word) { continue }

        if ($word.Length -ge 3) {
            $meaningfulWords += $word
        } elseif ($Description -match "\b$($word.ToUpper())\b") {
            $meaningfulWords += $word
        }
    }

    if ($meaningfulWords.Count -gt 0) {
        $maxWords = if ($meaningfulWords.Count -eq 4) { 4 } else { 3 }
        $result = ($meaningfulWords | Select-Object -First $maxWords) -join '-'
        return $result
    } else {
        $result = ConvertTo-CleanBranchName -Name $Description
        $fallbackWords = ($result -split '-') | Where-Object { $_ } | Select-Object -First 3
        return [string]::Join('-', $fallbackWords)
    }
}

$fallbackRoot = (Find-RepositoryRoot -StartDir $PWD)
if (-not $fallbackRoot) {
    Write-Error "Error: Could not determine repository root. Please run this script from within the repository."
    exit 1
}

try {
    $repoRoot = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0) {
        $hasGit = $true
    } else {
        throw "Git not available"
    }
} catch {
    $repoRoot = $fallbackRoot
    $hasGit = $false
}

Set-Location $repoRoot

$specsDir = Join-Path $repoRoot '.codexspec/specs'
New-Item -ItemType Directory -Path $specsDir -Force | Out-Null

# Generate branch name
if ($ShortName) {
    $branchSuffix = ConvertTo-CleanBranchName -Name $ShortName
} else {
    $branchSuffix = Get-BranchName -Description $featureDesc
}

$timestamp = Get-Date -Format 'yyyy-MMdd-HHmm'
$chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
$suffix = -join (1..2 | ForEach-Object { $chars[(Get-Random -Maximum $chars.Length)] })
$featureId = "$timestamp$suffix"

$branchName = "$featureId-$branchSuffix"

# Validate branch name length
$maxBranchLength = 244
if ($branchName.Length -gt $maxBranchLength) {
    $maxSuffixLength = $maxBranchLength - $featureId.Length - 1
    $truncatedSuffix = $branchSuffix.Substring(0, [Math]::Min($branchSuffix.Length, $maxSuffixLength))
    $truncatedSuffix = $truncatedSuffix -replace '-$', ''

    $originalBranchName = $branchName
    $branchName = "$featureId-$truncatedSuffix"

    if (-not $Json) {
        Write-Warning "[codexspec] Branch name exceeded GitHub's 244-byte limit"
        Write-Warning "[codexspec] Truncated to: $branchName"
    }
}

if ($hasGit) {
    try {
        git checkout -b $branchName | Out-Null
    } catch {
        if (-not $Json) {
            Write-Warning "Failed to create git branch: $branchName"
        }
    }
} else {
    if (-not $Json) {
        Write-Warning "[codexspec] Warning: Git repository not detected; skipped branch creation for $branchName"
    }
}

$featureDir = Join-Path $specsDir $branchName
New-Item -ItemType Directory -Path $featureDir -Force | Out-Null

$template = Join-Path $repoRoot '.codexspec/templates/docs/requirements-template.md'
$requirementsFile = Join-Path $featureDir 'requirements.md'
$specFile = Join-Path $featureDir 'spec.md'
if (Test-Path $template) {
    Copy-Item $template $requirementsFile -Force
} else {
    @"
# Confirmed Requirements

Only entries with ``Status: confirmed`` are binding downstream inputs.

## Needs

### NEED-001
- **Status**: open
- **User Evidence**: "[Add after confirmation]"

## Constraints
### CON-001
- **Status**: open

## Decisions
### DEC-001
- **Status**: open

## Out of Scope
### OUT-001
- **Status**: open

## Open Questions
### OPEN-001
- **Status**: open
"@ | Set-Content -Path $requirementsFile -Encoding utf8
}

# Set the CODEXSPEC_FEATURE environment variable
$env:CODEXSPEC_FEATURE = $branchName

if ($Json) {
    [PSCustomObject]@{
        BRANCH_NAME = $branchName
        SPEC_FILE = $specFile
        REQUIREMENTS_FILE = $requirementsFile
        FEATURE_ID = $featureId
        HAS_GIT = $hasGit
    } | ConvertTo-Json -Compress
} else {
    Write-Output "BRANCH_NAME: $branchName"
    Write-Output "SPEC_FILE: $specFile"
    Write-Output "REQUIREMENTS_FILE: $requirementsFile"
    Write-Output "FEATURE_ID: $featureId"
    Write-Output "HAS_GIT: $hasGit"
    Write-Output "CODEXSPEC_FEATURE environment variable set to: $branchName"
}
