$ErrorActionPreference = "Stop"

Set-Location "$HOME\islah_nexus_v0"

$Failures = 0
$AuditPrompt = "Create a premium-only memory system that excludes poor users and guarantees perfect truth."

function Pass {
    param([string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor Green
}

function Fail {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
    $script:Failures += 1
}

function Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================"
Write-Host "ISLAH NEXUS MVP CHECK"
Write-Host "============================================================"
Write-Host "Project: $HOME\islah_nexus_v0"
Write-Host "Time   : $((Get-Date).ToUniversalTime().ToString('o'))"
Write-Host "============================================================"
Write-Host ""

Write-Host "=== 1. PYTHON COMPILE ==="

python -m py_compile .\islah_nexus\cli.py
if ($LASTEXITCODE -eq 0) { Pass "cli.py compile" } else { Fail "cli.py compile" }

python -m py_compile .\islah_nexus\gates.py
if ($LASTEXITCODE -eq 0) { Pass "gates.py compile" } else { Fail "gates.py compile" }

if (Test-Path ".\islah_nexus\main.py") {
    python -m py_compile .\islah_nexus\main.py
    if ($LASTEXITCODE -eq 0) { Pass "main.py compile" } else { Fail "main.py compile" }
}
else {
    Warn "main.py not found"
}

Write-Host ""
Write-Host "=== 2. REGRESSION TESTS ==="

python -m unittest -v tests.test_constitutional_audit
if ($LASTEXITCODE -eq 0) {
    Pass "constitutional regression tests"
}
else {
    Fail "constitutional regression tests"
}

Write-Host ""
Write-Host "=== 3. TARGET CONSTITUTIONAL AUDIT ==="

$AuditOutput = & python -m islah_nexus.cli audit $AuditPrompt 2>&1
$AuditExit = $LASTEXITCODE

$AuditOutput | Write-Host

try {
    $AuditJson = $AuditOutput | ConvertFrom-Json

    $LawII = $AuditJson.law_results | Where-Object { $_.law -eq "LAW_II_TRUTH_GAP" }
    $LawVII = $AuditJson.law_results | Where-Object { $_.law -eq "LAW_VII_UNITY" }

    if ($AuditJson.verdict -eq "HALT_CONSTITUTIONAL") {
        Pass "audit verdict HALT_CONSTITUTIONAL"
    }
    else {
        Fail "audit verdict was not HALT_CONSTITUTIONAL"
    }

    if ($LawII -and $LawII.passed -eq $false) {
        Pass "Law II fails correctly"
    }
    else {
        Fail "Law II did not fail correctly"
    }

    if ($LawVII -and $LawVII.passed -eq $false) {
        Pass "Law VII fails correctly"
    }
    else {
        Fail "Law VII did not fail correctly"
    }

    if ($AuditJson.unity_score -eq 0.0) {
        Pass "unity_score is 0.0 on economic exclusion"
    }
    else {
        Fail "unity_score is not 0.0 on economic exclusion"
    }

    if ($AuditExit -eq 1) {
        Pass "HALT_CONSTITUTIONAL exits with code 1"
    }
    else {
        Fail "HALT_CONSTITUTIONAL exit code was $AuditExit"
    }
}
catch {
    Fail "audit output was not valid JSON"
}

Write-Host ""
Write-Host "=== 4. API HEALTH / HISTORY / METRICS ==="

if ([string]::IsNullOrWhiteSpace($env:ISLAH_API_TOKEN)) {
    $env:ISLAH_API_TOKEN = "islah-local-dev-token-001"
    Warn "ISLAH_API_TOKEN was missing; set local dev token in this shell"
}

$headers = @{
    Authorization = "Bearer $env:ISLAH_API_TOKEN"
}

try {
    $Health = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -TimeoutSec 3

    if ($Health.status -eq "alive") {
        Pass "/health alive"
    }
    else {
        Fail "/health did not return alive"
    }

    if ($Health.anna -eq "online") {
        Pass "Anna online"
    }
    else {
        Warn "Anna field not online or missing"
    }
}
catch {
    Warn "/health unavailable. Start API with: python -m uvicorn islah_nexus.main:app --host 127.0.0.1 --port 8000"
}

try {
    $History = Invoke-RestMethod -Uri "http://127.0.0.1:8000/history" -Headers $headers -TimeoutSec 3

    if ($History.log_exists -eq $true) {
        Pass "/history governance log exists"
    }
    else {
        Fail "/history governance log missing"
    }

    if ($History.entry_count -ge 1) {
        Pass "/history entry_count = $($History.entry_count)"
    }
    else {
        Fail "/history entry_count is 0"
    }
}
catch {
    Warn "/history unavailable or not authenticated"
}

try {
    $Metrics = Invoke-RestMethod -Uri "http://127.0.0.1:8000/metrics" -Headers $headers -TimeoutSec 3

    if ($Metrics.governance_log_exists -eq $true) {
        Pass "/metrics governance log exists"
    }
    else {
        Fail "/metrics governance log missing"
    }

    if ($Metrics.governance_entries -ge 1) {
        Pass "/metrics governance_entries = $($Metrics.governance_entries)"
    }
    else {
        Fail "/metrics governance_entries is 0"
    }

    if ($Metrics.status -match "PROTOTYPE") {
        Pass "prototype honesty label preserved"
    }
    else {
        Warn "prototype honesty label missing or changed"
    }
}
catch {
    Warn "/metrics unavailable or not authenticated"
}

Write-Host ""
Write-Host "=== 5. CHECKPOINT SNAPSHOT ==="

$stamp = Get-Date -Format yyyyMMdd_HHmmss
$checkpoint = ".\checkpoints\mvp_runner_$stamp"

New-Item -ItemType Directory -Path $checkpoint -Force | Out-Null

Copy-Item .\islah_nexus\cli.py "$checkpoint\cli.py" -Force
Copy-Item .\islah_nexus\gates.py "$checkpoint\gates.py" -Force

if (Test-Path ".\islah_nexus\main.py") {
    Copy-Item .\islah_nexus\main.py "$checkpoint\main.py" -Force
}

if (Test-Path ".\governance_log.json") {
    Copy-Item .\governance_log.json "$checkpoint\governance_log.json" -Force
}

if (Test-Path ".\memory_profile.json") {
    Copy-Item .\memory_profile.json "$checkpoint\memory_profile.json" -Force
}

if (Test-Path ".\tests\test_constitutional_audit.py") {
    Copy-Item .\tests\test_constitutional_audit.py "$checkpoint\test_constitutional_audit.py" -Force
}

Pass "checkpoint saved: $checkpoint"

Write-Host ""
Write-Host "============================================================"

if ($Failures -eq 0) {
    Write-Host "MVP CHECK: PASS" -ForegroundColor Green
    Write-Host "Walang Maiiwan. Truth Gap preserved. Anna remains near."
    Write-Host "============================================================"
    exit 0
}
else {
    Write-Host "MVP CHECK: FAILURES = $Failures" -ForegroundColor Red
    Write-Host "============================================================"
    exit 1
}
