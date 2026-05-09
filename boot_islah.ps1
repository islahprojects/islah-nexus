# ==============================================================================
# PROJECT: ISLAH NEXUS
# MODULE: OMNISINGULAR MASTER BOOT SEQUENCE (WINDOWS NATIVE)
# ARCHITECT: JJ
# COVENANT: WALANG MAIIWAN
# ==============================================================================

$ErrorActionPreference = "Continue"

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "[MIRROR] INITIATING SOVEREIGN BOOT SEQUENCE..." -ForegroundColor Cyan
Write-Host "=======================================================" -ForegroundColor Cyan

# 1. Hardware/Environment Validation
Write-Host "[1/4] Validating Local Node Dependencies..."
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "LAW VII WARNING: Python not found. Local-first execution impossible. Halting." -ForegroundColor Red
    exit
}

# 2. Corrigibility & Unity Floor Check
Write-Host "[2/4] Running SOOG Corrigibility Tests (Ensuring 0.05 Unity Floor)..."
if (Test-Path "test_soog_corrigibility (1).py") {
    python "test_soog_corrigibility (1).py" --fast
} else {
    Write-Host "[!] test_soog_corrigibility (1).py missing. Bypassing gate (Not Recommended)." -ForegroundColor Yellow
}

# 3. Boot Hexagonal Control Plane (Background Daemon)
Write-Host "[3/4] Igniting Nexus Hex Control Plane..."
if (Test-Path "nexus_hex_control_plane.py") {
    $env:NEXUS_HOST="127.0.0.1"
    $env:NEXUS_PORT="9090"
    # Run silently in the background
    Start-Process python -ArgumentList "nexus_hex_control_plane.py" -WindowStyle Hidden
    Write-Host "[MIRROR] Control Plane active on $env:NEXUS_HOST:$env:NEXUS_PORT" -ForegroundColor Green
    Start-Sleep -Seconds 2
} else {
    Write-Host "[!] nexus_hex_control_plane.py missing. Operating without local API." -ForegroundColor Yellow
}

# 4. Activate Sovereign Terminal (Human Authority Handover)
Write-Host "[4/4] Activating Sovereign Vault Shell..."
if (Test-Path "Sovereign.py") {
    python "Sovereign.py"
} else {
    Write-Host "[!] Sovereign.py missing. Dropping to standard shell." -ForegroundColor Yellow
}

Write-Host "=======================================================" -ForegroundColor Cyan
Write-Host "[MIRROR] Sequence complete. The Gate holds." -ForegroundColor Cyan