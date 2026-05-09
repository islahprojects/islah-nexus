$ErrorActionPreference = "Stop"

Write-Host "============================================================"
Write-Host "DUCK SECURITY CHECK: START"
Write-Host "============================================================"

if (-not (Test-Path ".\islah_nexus\security\secret_scan.py")) {
    Write-Error "Missing .\islah_nexus\security\secret_scan.py"
    exit 1
}

if (-not (Test-Path ".\tests\test_secret_scan.py")) {
    Write-Error "Missing .\tests\test_secret_scan.py"
    exit 1
}

Write-Host "[1/3] Compile secret_scan.py"
python -m py_compile .\islah_nexus\security\secret_scan.py

Write-Host "[2/3] Compile test_secret_scan.py"
python -m py_compile .\tests\test_secret_scan.py

Write-Host "[3/3] Run tests.test_secret_scan"
python -m unittest tests.test_secret_scan

if ($LASTEXITCODE -ne 0) {
    Write-Error "DUCK SECURITY CHECK: FAIL"
    exit 1
}

Write-Host "============================================================"
Write-Host "DUCK SECURITY CHECK: PASS"
Write-Host "Law VI / Duck Security smoke test clean."
Write-Host "============================================================"
exit 0
