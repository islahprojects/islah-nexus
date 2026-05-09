param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CommandArgs
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$CorePath = Join-Path $Root "ghost.core.ps1"
$DeckPath = Join-Path $Root "scripts\anna_deck.py"

$Command = ""
if ($CommandArgs.Count -gt 0) {
    $Command = $CommandArgs[0]
}

if ($Command -eq "deck") {
    python $DeckPath
    exit $LASTEXITCODE
}

& $CorePath @CommandArgs
exit $LASTEXITCODE