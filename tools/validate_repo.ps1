$ErrorActionPreference = 'Stop'
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')

$required = @(
    'README.md',
    'AGENTS.md',
    'PROJECT_STATE.md',
    'VANILLA_BUILD_LANGUAGE.md',
    'MICROBLOCK_IMPLEMENTATION.md',
    'ROADMAP.md',
    'packs/registry.json',
    'projects/wayne-manor/PROJECT_STATE.md'
)

$missing = @()
foreach ($rel in $required) {
    $p = Join-Path $RepoRoot $rel
    if (-not (Test-Path -LiteralPath $p)) { $missing += $rel }
}
if ($missing.Count -gt 0) {
    throw "Missing required files: $($missing -join ', ')"
}

$registry = Join-Path $RepoRoot 'packs/registry.json'
try {
    Get-Content -Raw -LiteralPath $registry | ConvertFrom-Json | Out-Null
} catch {
    throw "packs/registry.json is invalid JSON: $($_.Exception.Message)"
}

Write-Host 'BuildWright repository validation: PASS' -ForegroundColor Green
