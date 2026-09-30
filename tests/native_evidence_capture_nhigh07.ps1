# N-HIGH-07 final Windows verification trigger: current OutputPath implementation.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$root = Join-Path $env:RUNNER_TEMP ('ce-native-evidence-nhigh07-' + [guid]::NewGuid().ToString('N'))
$build = Join-Path $root 'build'
$out = Join-Path $root 'new\nested\evidence.json'
$script = Join-Path $PSScriptRoot '..\tools\capture_native_build_evidence_v2.ps1'
New-Item -ItemType Directory -Path $build -Force | Out-Null
Set-Content -LiteralPath (Join-Path $build 'libswe.dll') -Value 'synthetic-native-artifact' -NoNewline
try {
    $resolved = & $script $build $out
    if (-not (Test-Path -LiteralPath $out -PathType Leaf)) { throw 'N-HIGH-07 FAIL: fresh output file was not created' }
    if (-not (Test-Path -LiteralPath (Split-Path -LiteralPath $out -Parent) -PathType Container)) { throw 'N-HIGH-07 FAIL: output parent directory was not created' }
    if ($resolved -ne (Resolve-Path -LiteralPath $out).Path) { throw 'N-HIGH-07 FAIL: returned output path is not the created file' }
    $payload = Get-Content -LiteralPath $out -Raw | ConvertFrom-Json
    if ($payload.fresh_output_parent_created -ne $true) { throw 'N-HIGH-07 FAIL: fresh-parent flag missing' }
    if ([string]::IsNullOrWhiteSpace($payload.dll_sha256)) { throw 'N-HIGH-07 FAIL: DLL SHA-256 missing' }
    Write-Host 'N-HIGH-07_SELF_TEST=PASS'
} finally {
    if (Test-Path -LiteralPath $root) { Remove-Item -LiteralPath $root -Recurse -Force }
}
