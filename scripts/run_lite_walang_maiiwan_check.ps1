$ErrorActionPreference = "Stop"

Write-Host "============================================================"
Write-Host "WALANG MAIIWAN LITE RUNTIME CHECK: START"
Write-Host "============================================================"

Write-Host "[1/3] Compile lite_runtime.py"
python -m py_compile ".\islah_nexus\lite_runtime.py"

Write-Host "[2/3] Compile test_lite_runtime.py"
python -m py_compile ".\tests\test_lite_runtime.py"

Write-Host "[3/3] Run tests.test_lite_runtime"
python -m unittest tests.test_lite_runtime

Write-Host "============================================================"
Write-Host "WALANG MAIIWAN LITE RUNTIME CHECK: PASS"
Write-Host "Filipino-first labels, veto, Truth Gap, Deepworlds boundary, and RF no-guarantee guard clean."
Write-Host "============================================================"
