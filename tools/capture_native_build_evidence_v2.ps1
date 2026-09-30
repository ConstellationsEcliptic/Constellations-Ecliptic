param(
    [string]$BuildRoot,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Resolve-NewOutputPath {
    param([string]$LiteralOutput)

    if ([string]::IsNullOrWhiteSpace($LiteralOutput)) {
        throw 'FAIL-CLOSED: output path is empty'
    }

    $fullOutput = [System.IO.Path]::GetFullPath($LiteralOutput)
    $parent = [System.IO.Path]::GetDirectoryName($fullOutput)

    # N-HIGH-07 fix: create and resolve the parent directory, never the future output file.
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    $resolvedParent = (Resolve-Path -LiteralPath $parent).Path
    return (Join-Path $resolvedParent ([System.IO.Path]::GetFileName($fullOutput)))
}

function Write-NativeBuildEvidence {
    param(
        [string]$NativeBuildRoot,
        [string]$OutputPath
    )

    if ([string]::IsNullOrWhiteSpace($NativeBuildRoot)) {
        throw 'FAIL-CLOSED: native build root is empty'
    }
    if ([string]::IsNullOrWhiteSpace($OutputPath)) {
        throw 'FAIL-CLOSED: output path is empty'
    }

    if (-not (Test-Path -LiteralPath $NativeBuildRoot -PathType Container)) {
        throw "FAIL-CLOSED: native build root not found: $NativeBuildRoot"
    }

    $resolvedBuildRoot = (Resolve-Path -LiteralPath $NativeBuildRoot).Path
    $resolvedOutput = Resolve-NewOutputPath $OutputPath

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

    $record | ConvertTo-Json -Depth 5 |
        Set-Content -LiteralPath $resolvedOutput -Encoding utf8NoBOM

    if (-not (Test-Path -LiteralPath $resolvedOutput -PathType Leaf)) {
        throw "FAIL-CLOSED: evidence output was not created: $resolvedOutput"
    }

    return $resolvedOutput
}

Write-NativeBuildEvidence $BuildRoot $OutputPath
