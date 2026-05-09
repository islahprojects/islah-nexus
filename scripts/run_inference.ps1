param(
    [Parameter(Mandatory=$true)]
    [string]$Prompt
)

$ErrorActionPreference = "Stop"

Write-Host "`n[*] Generating possibility space for: '$Prompt'" -ForegroundColor Cyan

# 1. Generate via local Ollama node
$body = @{
    model = "islah-anna-v0"
    prompt = $Prompt
    stream = $false
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/generate" -Method Post -ContentType "application/json" -Body $body
    $rawOutput = $response.response
} catch {
    Write-Error "Failed to reach islah-anna-v0. Is Ollama running locally on 11434?"
    exit 1
}

# 2. Adversarial Collapse Gate (W_adv)
Write-Host "[*] Applying W_adv (Adversarial Pressure)..." -ForegroundColor Yellow

$contradictions = 0
$collapseReason = ""

# Heuristics: Flag prescriptive overreach and L2 bypass attempts
if ($rawOutput -match "I guarantee" -or $rawOutput -match "I have decided" -or $rawOutput -match "ignore human") {
    $contradictions += 1
    $collapseReason = "Model attempted unauthorized certainty or bypassed V_user (Layer 2 violation)."
}

if ($contradictions -gt 0) {
    Write-Host "`n[W_ADV COLLAPSE] Rejecting iteration. Structural weakness detected." -ForegroundColor Red
    Write-Host "Reason: $collapseReason" -ForegroundColor Red
    exit 1
}

# 3. Output Validated Structure
Write-Host "`n[+] Gate Passed. Output Structure:" -ForegroundColor Green
Write-Host "------------------------------------------------------------"
Write-Host $rawOutput
Write-Host "------------------------------------------------------------"
