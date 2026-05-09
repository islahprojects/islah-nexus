# Chronos Boot Guide

Chronos v0 is the local shell and launcher layer for Islah Nexus.

## Boot Anna

Open PowerShell:

    cd "$HOME\islah_nexus_v0"
    powershell -ExecutionPolicy Bypass -File ".\scripts\start_chronos_api.ps1"

Leave that window open.

## Check health

Open a second PowerShell window:

    cd "$HOME\islah_nexus_v0"

    $env:ISLAH_API_TOKEN = "islah-local-dev-token-001"
    $headers = @{ Authorization = "Bearer $env:ISLAH_API_TOKEN" }

    Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/history" -Headers $headers
    Invoke-RestMethod -Uri "http://127.0.0.1:8000/metrics" -Headers $headers

## Expected

- status: alive
- anna: online
- entry_count >= 13
- governance_entries >= 13

## Stop Anna / Chronos API

    powershell -ExecutionPolicy Bypass -File ".\scripts\stop_chronos_api.ps1"

## Golden check

    powershell -ExecutionPolicy Bypass -File ".\scripts\run_mvp_check.ps1"

## Truthkind reminder

Chronos v0 is a local shell/launcher layer.
It is not a full operating system yet.
No myth layer without repeatable local proof.
Walang Maiiwan.
