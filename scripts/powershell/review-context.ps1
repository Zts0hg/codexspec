#!/usr/bin/env pwsh
# Resolve a deterministic, read-only review target for review-code.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$SchemaVersion = "1"
$ReviewArgs = @($args)

function ConvertTo-CompactJson {
    param([Parameter(Mandatory = $true)] $Value)
    return ($Value | ConvertTo-Json -Depth 20 -Compress)
}

function Exit-ReviewError {
    param(
        [Parameter(Mandatory = $true)] [string] $Code,
        [Parameter(Mandatory = $true)] [string] $Message,
        [Parameter(Mandatory = $true)] [string] $Hint
    )
    $payload = [ordered]@{
        schema_version = $SchemaVersion
        status = "error"
        error = [ordered]@{
            code = $Code
            message = $Message
            hint = $Hint
        }
    }
    [Console]::Out.WriteLine((ConvertTo-CompactJson -Value $payload))
    exit 2
}

function Invoke-GitRaw {
    param(
        [Parameter(Mandatory = $true)] [string[]] $Arguments,
        [AllowNull()] [string] $InputText = $null
    )
    $startInfo = [System.Diagnostics.ProcessStartInfo]::new()
    $startInfo.FileName = "git"
    $startInfo.UseShellExecute = $false
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $startInfo.RedirectStandardInput = $true
    $startInfo.CreateNoWindow = $true
    $startInfo.WorkingDirectory = (Get-Location).Path
    foreach ($argument in $Arguments) {
        [void] $startInfo.ArgumentList.Add($argument)
    }

    $process = [System.Diagnostics.Process]::new()
    $process.StartInfo = $startInfo
    [void] $process.Start()
    if ($null -ne $InputText) {
        $process.StandardInput.Write($InputText)
    }
    $process.StandardInput.Close()
    $stdout = $process.StandardOutput.ReadToEnd()
    $stderr = $process.StandardError.ReadToEnd()
    $process.WaitForExit()
    return [PSCustomObject]@{
        ExitCode = $process.ExitCode
        StdOut = $stdout
        StdErr = $stderr
    }
}

function Resolve-GitCommit {
    param([Parameter(Mandatory = $true)] [string] $Ref)
    $result = Invoke-GitRaw -Arguments @("rev-parse", "--verify", "$Ref^{commit}")
    if ($result.ExitCode -ne 0) {
        return ""
    }
    return $result.StdOut.Trim()
}

$Selector = "default"
$BaseOverride = ""
$CommitInput = ""
$ParentOverride = ""
$FeatureOverride = ""
$FocusValues = [System.Collections.Generic.List[string]]::new()

function Set-ReviewSelector {
    param([Parameter(Mandatory = $true)] [string] $Requested)
    if ($script:Selector -ne "default") {
        Exit-ReviewError -Code "conflicting_selectors" `
            -Message "Review target selectors are mutually exclusive." `
            -Hint "Choose exactly one of --committed, --uncommitted, or --commit <sha>."
    }
    $script:Selector = $Requested
}

function Require-OptionValue {
    param([int] $Index, [string] $Option)
    if ($Index + 1 -ge $ReviewArgs.Count) {
        Exit-ReviewError -Code "missing_option_value" -Message "Missing value for $Option." `
            -Hint "Pass a value immediately after $Option."
    }
}

$argumentIndex = 0
while ($argumentIndex -lt $ReviewArgs.Count) {
    $argument = $ReviewArgs[$argumentIndex]
    switch ($argument) {
        "--committed" {
            Set-ReviewSelector -Requested "committed"
            $argumentIndex += 1
        }
        "--uncommitted" {
            Set-ReviewSelector -Requested "uncommitted"
            $argumentIndex += 1
        }
        "--commit" {
            Require-OptionValue -Index $argumentIndex -Option $argument
            Set-ReviewSelector -Requested "commit"
            $CommitInput = $ReviewArgs[$argumentIndex + 1]
            $argumentIndex += 2
        }
        "--base" {
            Require-OptionValue -Index $argumentIndex -Option $argument
            if ($BaseOverride) {
                Exit-ReviewError -Code "duplicate_base" -Message "--base may be supplied only once." `
                    -Hint "Remove the duplicate --base argument."
            }
            $BaseOverride = $ReviewArgs[$argumentIndex + 1]
            $argumentIndex += 2
        }
        "--parent" {
            Require-OptionValue -Index $argumentIndex -Option $argument
            if ($ParentOverride) {
                Exit-ReviewError -Code "duplicate_parent" -Message "--parent may be supplied only once." `
                    -Hint "Remove the duplicate --parent argument."
            }
            $ParentOverride = $ReviewArgs[$argumentIndex + 1]
            $argumentIndex += 2
        }
        "--feature" {
            Require-OptionValue -Index $argumentIndex -Option $argument
            if ($FeatureOverride) {
                Exit-ReviewError -Code "duplicate_feature" -Message "--feature may be supplied only once." `
                    -Hint "Remove the duplicate --feature argument."
            }
            $FeatureOverride = $ReviewArgs[$argumentIndex + 1]
            $argumentIndex += 2
        }
        "--focus" {
            Require-OptionValue -Index $argumentIndex -Option $argument
            $FocusValues.Add($ReviewArgs[$argumentIndex + 1])
            $argumentIndex += 2
        }
        default {
            if ($argument.StartsWith("--", [System.StringComparison]::Ordinal)) {
                Exit-ReviewError -Code "unknown_argument" -Message "Unknown review-code argument: $argument" `
                    -Hint "Use a documented defect target, --feature, --focus, or explicit --audit mode."
            }
            Exit-ReviewError -Code "bare_path_argument" `
                -Message "Bare path arguments are not valid defect-review targets: $argument" `
                -Hint "Use review-code --audit $argument for a whole-path quality audit."
        }
    }
}

if ($BaseOverride -and $Selector -notin @("default", "committed")) {
    Exit-ReviewError -Code "invalid_base_modifier" `
        -Message "--base is valid only for the default or --committed target." `
        -Hint "Remove --base or select the default/--committed target."
}
if ($ParentOverride -and $Selector -ne "commit") {
    Exit-ReviewError -Code "parent_requires_commit" -Message "--parent is valid only with --commit <sha>." `
        -Hint "Add --commit <sha> or remove --parent."
}
if ($ParentOverride -and $ParentOverride -notmatch '^[1-9][0-9]*$') {
    Exit-ReviewError -Code "invalid_parent" -Message "--parent must be a positive integer." `
        -Hint "Pass a valid merge-parent index such as --parent 2."
}

$repoResult = Invoke-GitRaw -Arguments @("rev-parse", "--show-toplevel")
if ($repoResult.ExitCode -ne 0) {
    Exit-ReviewError -Code "not_a_git_repository" -Message "review-code defect mode requires a Git repository." `
        -Hint "Run the command inside a Git repository or use --audit for a path audit."
}
$RepoRoot = $repoResult.StdOut.Trim()
Set-Location -LiteralPath $RepoRoot

$branchResult = Invoke-GitRaw -Arguments @("branch", "--show-current")
$CurrentBranch = if ($branchResult.ExitCode -eq 0) { $branchResult.StdOut.Trim() } else { "" }
$HeadSha = Resolve-GitCommit -Ref "HEAD"
if (-not $HeadSha) {
    Exit-ReviewError -Code "head_not_found" -Message "The repository has no resolvable HEAD commit." `
        -Hint "Create an initial commit before defect review."
}

function Get-SelectedRemote {
    $upstream = Invoke-GitRaw -Arguments @("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    if ($upstream.ExitCode -eq 0 -and $upstream.StdOut.Trim().Contains("/")) {
        return $upstream.StdOut.Trim().Split('/')[0]
    }
    $origin = Invoke-GitRaw -Arguments @("remote", "get-url", "origin")
    if ($origin.ExitCode -eq 0) {
        return "origin"
    }
    $remotes = Invoke-GitRaw -Arguments @("remote")
    if ($remotes.ExitCode -eq 0) {
        $names = @($remotes.StdOut -split "`r?`n" | Where-Object { $_ })
        if ($names.Count -eq 1) {
            return $names[0]
        }
    }
    return ""
}

function Resolve-ReviewBase {
    param([string] $Override)
    $resolvedRef = $Override
    if (-not $resolvedRef) {
        $remote = Get-SelectedRemote
        if ($remote) {
            $symbolic = Invoke-GitRaw -Arguments @("symbolic-ref", "--quiet", "--short", "refs/remotes/$remote/HEAD")
            if ($symbolic.ExitCode -eq 0) {
                $candidate = $symbolic.StdOut.Trim()
                if (Resolve-GitCommit -Ref $candidate) {
                    $resolvedRef = $candidate
                }
            }
            if (-not $resolvedRef) {
                $remoteHead = Invoke-GitRaw -Arguments @("ls-remote", "--symref", $remote, "HEAD")
                if ($remoteHead.ExitCode -eq 0) {
                    foreach ($line in ($remoteHead.StdOut -split "`r?`n")) {
                        if ($line -match '^ref:\s+(refs/heads/\S+)\s+HEAD$') {
                            $candidate = "$remote/$($Matches[1].Substring('refs/heads/'.Length))"
                            if (Resolve-GitCommit -Ref $candidate) {
                                $resolvedRef = $candidate
                            }
                            break
                        }
                    }
                }
            }
        }
        if (-not $resolvedRef) {
            foreach ($fallback in @("origin/main", "origin/master", "main", "master")) {
                if (Resolve-GitCommit -Ref $fallback) {
                    $resolvedRef = $fallback
                    break
                }
            }
        }
    }
    if (-not $resolvedRef) {
        Exit-ReviewError -Code "base_not_found" -Message "Could not determine the repository base branch." `
            -Hint "Pass --base <branch> explicitly or configure the remote default HEAD."
    }
    $resolvedSha = Resolve-GitCommit -Ref $resolvedRef
    if (-not $resolvedSha) {
        Exit-ReviewError -Code "base_not_found" -Message "Base ref cannot be resolved: $resolvedRef" `
            -Hint "Pass an existing local or remote-tracking ref."
    }
    $mergeBase = Invoke-GitRaw -Arguments @("merge-base", $HeadSha, $resolvedSha)
    if ($mergeBase.ExitCode -ne 0 -or -not $mergeBase.StdOut.Trim()) {
        Exit-ReviewError -Code "merge_base_not_found" `
            -Message "No merge base exists between HEAD and $resolvedRef." `
            -Hint "Pass the correct --base ref or reconcile unrelated histories."
    }
    return [PSCustomObject]@{
        Ref = $resolvedRef
        Sha = $resolvedSha
        MergeBase = $mergeBase.StdOut.Trim()
    }
}

$Inventory = [System.Collections.Generic.Dictionary[string, object]]::new([System.StringComparer]::Ordinal)
$InventoryOrder = [System.Collections.Generic.List[string]]::new()
$TargetSegments = [System.Collections.Generic.List[object]]::new()

function Add-InventoryRecord {
    param([string] $Status, [string] $Path, [AllowNull()] [string] $OldPath, [string] $Segment)
    $normalizedStatus = $Status.Substring(0, 1)
    if (-not $Inventory.ContainsKey($Path)) {
        $entry = [PSCustomObject][ordered]@{
            path = $Path
            old_path = if ($OldPath) { $OldPath } else { $null }
            status = $normalizedStatus
            segments = [System.Collections.Generic.List[string]]::new()
            object_mode = $null
            kind = "file"
        }
        $entry.segments.Add($Segment)
        $Inventory.Add($Path, $entry)
        $InventoryOrder.Add($Path)
    } else {
        $entry = $Inventory[$Path]
        $entry.status = $normalizedStatus
        if (-not $entry.segments.Contains($Segment)) {
            $entry.segments.Add($Segment)
        }
        if ($OldPath) {
            $entry.old_path = $OldPath
        }
    }
}

function Add-TargetSegment {
    param([string] $Name, [string] $From, [string] $To)
    $TargetSegments.Add([PSCustomObject][ordered]@{ name = $Name; from = $From; to = $To })
}

function Add-DiffInventory {
    param([string] $Segment, [string[]] $GitArguments)
    $result = Invoke-GitRaw -Arguments $GitArguments
    if ($result.ExitCode -ne 0) {
        Exit-ReviewError -Code "inventory_failed" -Message "Git failed while inventorying $Segment changes." `
            -Hint "Verify repository objects and permissions, then retry."
    }
    $tokens = $result.StdOut.Split([char] 0)
    $index = 0
    while ($index -lt $tokens.Count -and $tokens[$index]) {
        $status = $tokens[$index]
        $index += 1
        $oldPath = $null
        if ($status.StartsWith("R") -or $status.StartsWith("C")) {
            $oldPath = $tokens[$index]
            $index += 1
        }
        $path = $tokens[$index]
        $index += 1
        Add-InventoryRecord -Status $status -Path $path -OldPath $oldPath -Segment $Segment
    }
}

function Add-UntrackedInventory {
    $result = Invoke-GitRaw -Arguments @("ls-files", "--others", "--exclude-standard", "-z")
    if ($result.ExitCode -ne 0) {
        Exit-ReviewError -Code "inventory_failed" -Message "Git failed while inventorying untracked files." `
            -Hint "Verify repository permissions, then retry."
    }
    foreach ($path in $result.StdOut.Split([char] 0)) {
        if ($path) {
            Add-InventoryRecord -Status "A" -Path $path -OldPath $null -Segment "untracked"
        }
    }
}

function Test-HasUncommittedWork {
    $unstaged = Invoke-GitRaw -Arguments @("diff", "--quiet", "--ignore-submodules=none", "--")
    if ($unstaged.ExitCode -eq 1) { return $true }
    $staged = Invoke-GitRaw -Arguments @("diff", "--cached", "--quiet", "--ignore-submodules=none", "--")
    if ($staged.ExitCode -eq 1) { return $true }
    $untracked = Invoke-GitRaw -Arguments @("ls-files", "--others", "--exclude-standard")
    return [bool] $untracked.StdOut.Trim()
}

function Add-UncommittedSegments {
    Add-TargetSegment -Name "staged" -From $HeadSha -To "index"
    Add-DiffInventory -Segment "staged" -GitArguments @("diff", "--cached", "--name-status", "-z", "--find-renames", "--")
    Add-TargetSegment -Name "unstaged" -From "index" -To "worktree"
    Add-DiffInventory -Segment "unstaged" -GitArguments @("diff", "--name-status", "-z", "--find-renames", "--")
    Add-TargetSegment -Name "untracked" -From "none" -To "worktree"
    Add-UntrackedInventory
}

$BaseRef = ""
$BaseSha = ""
$MergeBaseSha = ""
$CommitSha = ""
$ParentSha = ""
$ParentNumber = $null
$CompleteFeature = $false

switch ($Selector) {
    "default" {
        $base = Resolve-ReviewBase -Override $BaseOverride
        $BaseRef = $base.Ref
        $BaseSha = $base.Sha
        $MergeBaseSha = $base.MergeBase
        $baseBranchName = ($BaseRef -replace '^refs/(heads|remotes)/', '').Split('/')[-1]
        if ($CurrentBranch -and $CurrentBranch -eq $baseBranchName) {
            Add-UncommittedSegments
        } else {
            Add-TargetSegment -Name "committed" -From $MergeBaseSha -To $HeadSha
            Add-DiffInventory -Segment "committed" `
                -GitArguments @("diff", "--name-status", "-z", "--find-renames", $MergeBaseSha, $HeadSha, "--")
            Add-UncommittedSegments
            $CompleteFeature = $true
        }
    }
    "committed" {
        $base = Resolve-ReviewBase -Override $BaseOverride
        $BaseRef = $base.Ref
        $BaseSha = $base.Sha
        $MergeBaseSha = $base.MergeBase
        Add-TargetSegment -Name "committed" -From $MergeBaseSha -To $HeadSha
        Add-DiffInventory -Segment "committed" `
            -GitArguments @("diff", "--name-status", "-z", "--find-renames", $MergeBaseSha, $HeadSha, "--")
        $CompleteFeature = -not (Test-HasUncommittedWork)
    }
    "uncommitted" {
        Add-UncommittedSegments
    }
    "commit" {
        $CommitSha = Resolve-GitCommit -Ref $CommitInput
        if (-not $CommitSha) {
            Exit-ReviewError -Code "commit_not_found" -Message "Commit cannot be resolved: $CommitInput" `
                -Hint "Pass an existing commit SHA or ref."
        }
        $parentsResult = Invoke-GitRaw -Arguments @("rev-list", "--parents", "-n", "1", $CommitSha)
        $parts = @($parentsResult.StdOut.Trim() -split '\s+' | Where-Object { $_ })
        $parentCount = $parts.Count - 1
        if ($parentCount -eq 0) {
            if ($ParentOverride) {
                Exit-ReviewError -Code "invalid_parent" -Message "Root commits have no selectable parent." `
                    -Hint "Remove --parent for a root commit."
            }
            $emptyTree = Invoke-GitRaw -Arguments @("hash-object", "-t", "tree", "--stdin") -InputText ""
            $ParentSha = $emptyTree.StdOut.Trim()
            $ParentNumber = 0
            Add-TargetSegment -Name "commit" -From $ParentSha -To $CommitSha
            Add-DiffInventory -Segment "commit" `
                -GitArguments @("diff-tree", "--root", "--no-commit-id", "-r", "--name-status", "-z", "--find-renames", $CommitSha, "--")
        } else {
            $ParentNumber = if ($ParentOverride) { [int] $ParentOverride } else { 1 }
            if ($ParentNumber -gt $parentCount) {
                Exit-ReviewError -Code "invalid_parent" -Message "Commit has no parent $ParentNumber." `
                    -Hint "Choose a parent index from 1 through $parentCount."
            }
            $ParentSha = $parts[$ParentNumber]
            Add-TargetSegment -Name "commit" -From $ParentSha -To $CommitSha
            Add-DiffInventory -Segment "commit" `
                -GitArguments @("diff", "--name-status", "-z", "--find-renames", $ParentSha, $CommitSha, "--")
        }
    }
}

function Test-BinaryFile {
    param([string] $Path)
    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $buffer = [byte[]]::new(8192)
        $count = $stream.Read($buffer, 0, $buffer.Length)
        for ($index = 0; $index -lt $count; $index += 1) {
            if ($buffer[$index] -eq 0) { return $true }
        }
        return $false
    } finally {
        $stream.Dispose()
    }
}

foreach ($path in $InventoryOrder) {
    $entry = $Inventory[$path]
    $modeResult = Invoke-GitRaw -Arguments @("ls-files", "-s", "--", $path)
    if ($modeResult.ExitCode -eq 0 -and $modeResult.StdOut -match '^(\d+)\s') {
        $entry.object_mode = $Matches[1]
    }
    $fullPath = Join-Path $RepoRoot ($path -replace '/', [System.IO.Path]::DirectorySeparatorChar)
    if ($entry.object_mode -eq "160000") {
        $entry.kind = "submodule"
    } elseif ($entry.object_mode -eq "120000") {
        $entry.kind = "symlink"
    } elseif ($entry.status -eq "D" -and -not (Test-Path -LiteralPath $fullPath)) {
        $entry.kind = "missing"
    } elseif (Test-Path -LiteralPath $fullPath -PathType Leaf) {
        $item = Get-Item -LiteralPath $fullPath -Force
        if ($item.LinkType) {
            $entry.kind = "symlink"
        } elseif (Test-BinaryFile -Path $fullPath) {
            $entry.kind = "binary"
        }
    }
}

$FeatureStatus = "not_resolved"
$FeatureSource = "none"
$FeaturePath = $null
if ($FeatureOverride) {
    if (-not (Test-Path -LiteralPath $FeatureOverride -PathType Container)) {
        Exit-ReviewError -Code "feature_not_found" -Message "Feature directory does not exist: $FeatureOverride" `
            -Hint "Pass an existing CodexSpec feature directory."
    }
    $FeaturePath = (Resolve-Path -LiteralPath $FeatureOverride).Path
    $FeatureStatus = "resolved"
    $FeatureSource = "explicit"
} elseif ($CurrentBranch) {
    $candidate = Join-Path $RepoRoot ".codexspec/specs/$CurrentBranch"
    if (Test-Path -LiteralPath $candidate -PathType Container) {
        $FeaturePath = (Resolve-Path -LiteralPath $candidate).Path
        $FeatureStatus = "resolved"
        $FeatureSource = "branch"
    }
}

$Artifacts = @()
if ($FeaturePath) {
    $Artifacts = @("requirements.md", "spec.md", "plan.md", "tasks.md") | ForEach-Object {
        [PSCustomObject][ordered]@{
            name = $_
            readable = Test-Path -LiteralPath (Join-Path $FeaturePath $_) -PathType Leaf
        }
    }
}

$InventoryOutput = @($InventoryOrder | ForEach-Object {
    $entry = $Inventory[$_]
    [PSCustomObject][ordered]@{
        path = $entry.path
        old_path = $entry.old_path
        status = $entry.status
        segments = @($entry.segments)
        object_mode = $entry.object_mode
        kind = $entry.kind
    }
})

$CommittedCount = 0
$StagedCount = 0
$UnstagedCount = 0
$UntrackedCount = 0
foreach ($entry in $InventoryOutput) {
    foreach ($segment in $entry.segments) {
        switch ($segment) {
            { $_ -in @("committed", "commit") } { $CommittedCount += 1 }
            "staged" { $StagedCount += 1 }
            "unstaged" { $UnstagedCount += 1 }
            "untracked" { $UntrackedCount += 1 }
        }
    }
}

$payload = [ordered]@{
    schema_version = $SchemaVersion
    status = "ok"
    mode = "defect"
    selector = $Selector
    arguments = [ordered]@{
        base_override = if ($BaseOverride) { $BaseOverride } else { $null }
        commit = if ($CommitInput) { $CommitInput } else { $null }
        parent = if ($ParentOverride) { [int] $ParentOverride } else { $null }
        feature_override = if ($FeatureOverride) { $FeatureOverride } else { $null }
        focus = @($FocusValues)
    }
    repository = [ordered]@{
        root = $RepoRoot
        current_branch = if ($CurrentBranch) { $CurrentBranch } else { $null }
        head_sha = $HeadSha
    }
    target = [ordered]@{
        complete_feature = $CompleteFeature
        empty = $InventoryOutput.Count -eq 0
        base_ref = if ($BaseRef) { $BaseRef } else { $null }
        base_sha = if ($BaseSha) { $BaseSha } else { $null }
        merge_base_sha = if ($MergeBaseSha) { $MergeBaseSha } else { $null }
        commit_sha = if ($CommitSha) { $CommitSha } else { $null }
        parent_sha = if ($ParentSha) { $ParentSha } else { $null }
        parent_number = $ParentNumber
        segments = @($TargetSegments)
    }
    feature = [ordered]@{
        status = $FeatureStatus
        source = $FeatureSource
        path = $FeaturePath
        artifacts = @($Artifacts)
    }
    inventory = @($InventoryOutput)
    counts = [ordered]@{
        total = $InventoryOutput.Count
        committed = $CommittedCount
        staged = $StagedCount
        unstaged = $UnstagedCount
        untracked = $UntrackedCount
    }
}

[Console]::Out.WriteLine((ConvertTo-CompactJson -Value $payload))
exit 0
