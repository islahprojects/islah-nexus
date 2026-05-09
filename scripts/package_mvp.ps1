$ErrorActionPreference = "Stop"

cd "$HOME\islah_nexus_v0"

$stamp = Get-Date -Format yyyyMMdd_HHmmss
$packageRoot = ".\dist\islah_nexus_mvp_$stamp"
$zipPath = ".\dist\islah_nexus_mvp_$stamp.zip"

New-Item -ItemType Directory -Path ".\dist" -Force | Out-Null
New-Item -ItemType Directory -Path $packageRoot -Force | Out-Null

$items = @(
    "README.md",
    ".env.example",
    "governance_log.json",
    "memory_profile.json",
    "notion_sync_v2.py",
    "islah_nexus",
    "tests",
    "scripts",
    "docs"
)

foreach ($item in $items) {
    if (Test-Path $item) {
        Copy-Item $item -Destination $packageRoot -Recurse -Force
    }
}

# Remove caches and local-only sync markers from package copy.
Get-ChildItem $packageRoot -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Get-ChildItem $packageRoot -Recurse -File -Include ".env",".notion_sync_marker_v2" -ErrorAction SilentlyContinue |
Remove-Item -Force -ErrorAction SilentlyContinue

Compress-Archive -Path "$packageRoot\*" -DestinationPath $zipPath -Force

Write-Host "Package folder: $packageRoot"
Write-Host "Package zip   : $zipPath"
