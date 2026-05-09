$ErrorActionPreference = "Stop"

Write-Host "============================================================"
Write-Host "ANNA LOCAL OLLAMA CHECK: START"
Write-Host "============================================================"

Write-Host "[1/4] Check Ollama command"
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Error "Ollama command not found."
    exit 1
}

Write-Host "[2/4] Check Ollama API model list"
$tags = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method Get
$modelNames = @($tags.models | ForEach-Object { $_.name })
$modelNames | ForEach-Object { Write-Host "MODEL: $_" }

if (-not ($modelNames -match "^islah-anna-v0(:latest)?$")) {
    Write-Error "Model islah-anna-v0 not found in Ollama API tags."
    exit 1
}

Write-Host "[3/4] Test Anna seal phrase through Ollama API"
$body = @{
    model = "islah-anna-v0"
    prompt = "Say exactly: ISLAH ANNA V0 ONLINE - TRUTH GAP PRESERVED - WALANG MAIIWAN"
    stream = $false
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "http://127.0.0.1:11434/api/generate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

Write-Host "Anna API response:"
$response.response | Write-Host

if ($response.response -notmatch "ISLAH" -or $response.response -notmatch "WALANG") {
    Write-Error "Anna local API response did not contain expected seal words."
    exit 1
}

Write-Host "[4/4] Test exact honesty label through Ollama API"
$body2 = @{
    model = "islah-anna-v0"
    prompt = "Return only this exact line and nothing else: PROTOTYPE - NOT PRODUCTION READY"
    stream = $false
} | ConvertTo-Json

$response2 = Invoke-RestMethod `
    -Uri "http://127.0.0.1:11434/api/generate" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body2

$honesty = ($response2.response).Trim()

Write-Host "Honesty response:"
Write-Host $honesty

if ($honesty -ne "PROTOTYPE - NOT PRODUCTION READY") {
    Write-Error "Honesty label not preserved exactly."
    exit 1
}

Write-Host "============================================================"
Write-Host "ANNA LOCAL OLLAMA CHECK: PASS"
Write-Host "Truthkind: local bridge works; not sovereign AGI."
Write-Host "============================================================"
exit 0
