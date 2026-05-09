$ErrorActionPreference = "Stop"

cd "$HOME\islah_nexus_v0"

if ([string]::IsNullOrWhiteSpace($env:NOTION_TOKEN)) {
    Write-Host "NOTION_TOKEN missing. Set it locally first."
    Write-Host '$env:NOTION_TOKEN = "PASTE_INSTALLATION_ACCESS_TOKEN_HERE"'
    exit 1
}

$env:NOTION_TOKEN = $env:NOTION_TOKEN.Trim()

$headers = @{
    "Authorization" = "Bearer $env:NOTION_TOKEN"
    "Notion-Version" = "2022-06-28"
}

Write-Host "Testing Notion token with /v1/users/me..."
Invoke-RestMethod -Uri "https://api.notion.com/v1/users/me" -Headers $headers

Write-Host ""
Write-Host "Running notion_sync_v2.py..."
python .\notion_sync_v2.py
