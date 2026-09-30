param(
    [Parameter(Mandatory=$true)][string]$DropName,
    [string]$Destination = (Join-Path (Get-Location) $DropName)
)

$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $Destination | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $Destination 'payload') | Out-Null
@"
# $DropName

## Intent

## Changes

## Validation

## Rollback notes
"@ | Set-Content -Encoding UTF8 (Join-Path $Destination 'DROP_NOTES.md')
Write-Host "Created drop workspace: $Destination"
