[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$BuildRoot,
    [Parameter(Mandatory=$true)]
    [string]$Output
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Resolve-NewOutputPath {
    param([Parameter(Mandatory=$true)][string]$LiteralOutput)
    $fullOutput = [System.IO.Path]::GetFullPath($LiteralOutput)
    $parent = Split-Path -LiteralPath $fullOutput -Parent
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    $resolvedParent = (Resolve-Path -LiteralPath $parent).Path
    Join-Path $resolvedParent ([System.IO.Path]::GetFileName($fullOutput))
}

function Write-NativeBuildEvidence {
    param(
        [Parameter(Mandatory=$true)][string]$NativeBuildRoot,
        [Parameter(Mandatory=$true)][string]$OutputPath
    )
    if (-not (Test-Path -LiteralPath $NativeBuildRoot -PathType Container)) {
        throw "FAIL-CLOSED: native build root not found: $NativeBuildRoot"
    }
    $resolvedBuildRoot = (Resolve-Path -LiteralPath $NativeBuildRoot).Path
    $resolvedOutput = Resolve-NewOutputPath -LiteralOutput $OutputPath
    $dll = Join-Path $resolvedBuildRoot 'libswe.dll'
    if (-not (Test-Path -LiteralPath $dll -PathType Leaf)) {
        throw "FAIL-CLOSED: native DLL not found: $dll"
    }
    $dllHash = (Get-FileHash -LiteralPath $dll -Algorithm SHA256).Hash.ToLowerInvariant()
    $record = [ordered]@{
        capture_status = 'MACHINE_GENERATED'
        captured_at_utc = (Get-Date).ToUniversalTime().ToString('o')
        build_root = $resolvedBuildRoot
        dll_path = $dll
        dll_sha256 = $dllHash
        output_path = $resolvedOutput
        fresh_output_parent_created = $true
    }
    $record | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $resolvedOutput -Encoding utf8NoBOM
    if (-not (Test-Path -LiteralPath $resolvedOutput -PathType Leaf)) {
        throw "FAIL-CLOSED: evidence output was not created: $resolvedOutput"
    }
    $resolvedOutput
}

Write-NativeBuildEvidence -NativeBuildRoot $BuildRoot -OutputPath $Output
