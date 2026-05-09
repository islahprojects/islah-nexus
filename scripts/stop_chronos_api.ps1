$ErrorActionPreference = "Stop"

Write-Host "Stopping any process listening on port 8000..."

Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue |
ForEach-Object {
    Write-Host "Stopping process:" $_.OwningProcess
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
}

Write-Host "Done."
