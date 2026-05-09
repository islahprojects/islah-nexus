$ErrorActionPreference = "Stop"

cd "$HOME\islah_nexus_v0"

if ([string]::IsNullOrWhiteSpace($env:ISLAH_API_TOKEN)) {
    $env:ISLAH_API_TOKEN = "islah-local-dev-token-001"
}

Write-Host "Starting Islah Nexus / Chronos API..."
Write-Host "Host: 127.0.0.1"
Write-Host "Port: 8000"
Write-Host "Anna should report online at /health"

python -m uvicorn islah_nexus.main:app --host 127.0.0.1 --port 8000
