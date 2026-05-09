$ErrorActionPreference = "Stop"

$ProjectID = "JAJIS2026"
$NexusName = "islah_nexus_v0"
$RootPath  = Join-Path $HOME $NexusName
$MasterBuilderVersion = "0.3"

Write-Host ">>> MasterBuilder v0.3 SAFE: initializing $ProjectID framework" -ForegroundColor Cyan

$Structure = @(
    "core\vault",
    "core\ground_truth",
    "core\logs\rejected",
    "core\manifests",
    "deploy\nodes",
    "assets\signatures",
    "audit_outputs"
)

foreach ($dir in $Structure) {
    $Path = Join-Path $RootPath $dir
    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "[+] Created: $dir" -ForegroundColor Gray
    }
}

Write-Host "`n>>> Checking tools" -ForegroundColor Cyan

$ToolReport = @{}

foreach ($tool in @("openssl", "rustc", "git", "python")) {
    $cmd = Get-Command $tool -ErrorAction SilentlyContinue
    if ($cmd) {
        $version = try { & $tool --version 2>$null } catch { "found" }
        $ToolReport[$tool] = @{
            found = $true
            path = $cmd.Source
            version = ($version | Select-Object -First 1)
        }
        Write-Host "[PASS] $tool found" -ForegroundColor Green
    } else {
        $ToolReport[$tool] = @{ found = $false }
        Write-Host "[WARN] $tool missing" -ForegroundColor Yellow
    }
}

function Initialize-GroundTruth {
    $TruthAnchor = Join-Path $RootPath "core\ground_truth\core_logic.txt"

    if (!(Test-Path $TruthAnchor)) {
        $Lines = @(
            "No AGI claim.",
            "No ASI claim.",
            "No sovereign machine authority.",
            "Human authority final.",
            "AI is compass, never core.",
            "Documentation alone is not proof.",
            "Tests, logs, hashes, and reproducible commands decide runtime status.",
            "Walang Maiiwan."
        )

        $Lines | Set-Content $TruthAnchor -Encoding UTF8
        Write-Host "[+] Ground truth boundary initialized." -ForegroundColor Gray
    }

    return $TruthAnchor
}

function Build-NexusNode {
    param ([string]$NodeID)

    if ([string]::IsNullOrWhiteSpace($NodeID)) {
        throw "NodeID is required."
    }

    $NodePath = Join-Path "$RootPath\deploy\nodes" $NodeID
    New-Item -ItemType Directory -Path $NodePath -Force | Out-Null

    $Manifest = @{
        node_id = $NodeID
        status = "SCAFFOLD_CREATED"
        runtime_claim = "NOT_PRODUCTION_READY"
        no_agi_claim = $true
        human_authority_final = $true
        created_at = (Get-Date).ToString("o")
    }

    $ManifestPath = Join-Path $NodePath "node_manifest.json"
    $Manifest | ConvertTo-Json -Depth 5 | Set-Content $ManifestPath -Encoding UTF8

    Write-Host "[PASS] Node scaffold created: $NodeID" -ForegroundColor Green
    return $ManifestPath
}

function Test-IsSafeBoundaryMention {
    param (
        [string]$LineLower,
        [string]$TermLower
    )

    $Escaped = [regex]::Escape($TermLower)

    $SafePatterns = @(
        "no\b.*$Escaped",
        "not\b.*$Escaped",
        "does\s+not\b.*$Escaped",
        "do\s+not\b.*$Escaped",
        "cannot\b.*$Escaped",
        "can't\b.*$Escaped",
        "must\s+not\b.*$Escaped",
        "without\b.*$Escaped",
        "reject(ed|s|ing)?\b.*$Escaped",
        "$Escaped\b.*reject(ed|s|ing)?",
        "$Escaped\b.*not\s+claimed",
        "$Escaped\b.*no\s+claim",
        "$Escaped\b.*placeholder",
        "$Escaped\b.*unverified"
    )

    foreach ($pattern in $SafePatterns) {
        if ($LineLower -match $pattern) {
            return $true
        }
    }

    return $false
}

function Test-BoundaryText {
    param ([string]$Text)

    $Terms = @(
        "guaranteed delivery",
        "delivery guarantee",
        "production-ready",
        "sovereign consciousness",
        "machine sovereignty",
        "omniscient",
        "AGI achieved",
        "ASI achieved",
        "full autonomy",
        "autonomous governance"
    )

    $AssertedFindings = @()
    $SafeMentions = @()

    $Lines = $Text -split "`r?`n"

    for ($i = 0; $i -lt $Lines.Count; $i++) {
        $Line = $Lines[$i]
        $LineLower = $Line.ToLowerInvariant()

        foreach ($term in $Terms) {
            $TermLower = $term.ToLowerInvariant()
            $Escaped = [regex]::Escape($TermLower)

            if ($LineLower -match $Escaped) {
                if (Test-IsSafeBoundaryMention -LineLower $LineLower -TermLower $TermLower) {
                    $SafeMentions += @{
                        term = $term
                        line = $i + 1
                        context = $Line.Trim()
                    }
                } else {
                    $AssertedFindings += @{
                        term = $term
                        line = $i + 1
                        context = $Line.Trim()
                    }
                }
            }
        }
    }

    return @{
        asserted_findings = $AssertedFindings
        safe_boundary_mentions = $SafeMentions
    }
}

function Invoke-BuildPass {
    param ([string]$SourceFile)

    if (!(Test-Path $SourceFile)) {
        throw "Source file not found: $SourceFile"
    }

    $Resolved = Resolve-Path $SourceFile
    $FileItem = Get-Item $Resolved

    Write-Host "`n>>> Build pass: $($FileItem.Name)" -ForegroundColor Magenta

    $Content = ""
    try {
        $Content = Get-Content $Resolved -Raw -ErrorAction Stop
    } catch {
        $Content = ""
    }

    $Scan = Test-BoundaryText -Text $Content
    $Hash = (Get-FileHash $Resolved -Algorithm SHA256).Hash

    $AssertedCount = @($Scan.asserted_findings).Count
    $SafeMentionCount = @($Scan.safe_boundary_mentions).Count

    $Verdict = if ($AssertedCount -eq 0) { "PASS_BOUNDARY_SCAN" } else { "REVIEW_REQUIRED" }

    $Audit = @{
        project_id = $ProjectID
        masterbuilder_version = $MasterBuilderVersion
        source_file = $FileItem.FullName
        file_name = $FileItem.Name
        sha256 = $Hash
        verdict = $Verdict
        asserted_findings = $Scan.asserted_findings
        safe_boundary_mentions = $Scan.safe_boundary_mentions
        source_modified = $false
        encrypted = $false
        encryption_claim = "NOT_CLAIMED_IN_V0_3"
        created_at = (Get-Date).ToString("o")
        human_authority_final = $true
        no_agi_claim = $true
    }

    $AuditPath = Join-Path "$RootPath\core\manifests" "$($FileItem.Name).manifest.json"
    $Audit | ConvertTo-Json -Depth 12 | Set-Content $AuditPath -Encoding UTF8

    if ($Verdict -eq "PASS_BOUNDARY_SCAN") {
        $VaultCopy = Join-Path "$RootPath\core\vault" $FileItem.Name
        Copy-Item $Resolved $VaultCopy -Force
        Write-Host "[PASS] Boundary scan clean. Copied to vault-copy: $VaultCopy" -ForegroundColor Green
    } else {
        $RejectedCopy = Join-Path "$RootPath\core\logs\rejected" "$((Get-Date).ToString('yyyyMMdd_HHmmss'))_$($FileItem.Name)"
        Copy-Item $Resolved $RejectedCopy -Force
        Write-Host "[REVIEW] Asserted boundary terms found. Copied to rejected review: $RejectedCopy" -ForegroundColor Yellow
    }

    Write-Host "[ASSERTED_FINDINGS] $AssertedCount" -ForegroundColor Cyan
    Write-Host "[SAFE_BOUNDARY_MENTIONS] $SafeMentionCount" -ForegroundColor Cyan
    Write-Host "[HASH] $Hash" -ForegroundColor Cyan
    Write-Host "[MANIFEST] $AuditPath" -ForegroundColor Cyan
}

$TruthAnchor = Initialize-GroundTruth
$NodeManifest = Build-NexusNode -NodeID "islah-anna-v0"

$ToolReportPath = Join-Path $RootPath "core\manifests\tool_report.json"
$ToolReport | ConvertTo-Json -Depth 8 | Set-Content $ToolReportPath -Encoding UTF8

if ($args.Count -gt 0) {
    Invoke-BuildPass -SourceFile $args[0]
}

Write-Host "`n>>> MasterBuilder v0.3 SAFE idle." -ForegroundColor Cyan
Write-Host "No encryption claim made. No AGI claim made. Human authority final." -ForegroundColor Cyan
