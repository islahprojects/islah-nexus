$ErrorActionPreference = "Stop"

Write-Host "============================================================"
Write-Host "ISLAH NEXUS MIRROR APP: START"
Write-Host "============================================================"

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Error "Ollama not found."
    exit 1
}

$tags = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method Get
$modelNames = @($tags.models | ForEach-Object { $_.name })

if (-not ($modelNames -match "^islah-anna-v0(:latest)?$")) {
    Write-Error "islah-anna-v0 not found. Create the model first."
    exit 1
}

python -m py_compile ".\mirror_app\app.py"

Write-Host "Open this in browser:"
Write-Host "http://127.0.0.1:8787"
Write-Host "============================================================"

python ".\mirror_app\app.py"
