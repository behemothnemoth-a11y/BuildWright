$ErrorActionPreference='Stop'
python "$PSScriptRoot/validate_repo.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
