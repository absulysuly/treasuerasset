<#
============================================================
🧠 IRAQ ELECTION MEGA SYSTEM LAUNCHER
Purpose: Safely run all local AI agents (research, assemble, verify)
Location: E:\HamletUnified\IraqElectinMegaMVP
============================================================
#>

Write-Host "🚀 Launching Mega System..." -ForegroundColor Cyan

# --- Setup directories
$root = "E:\HamletUnified\IraqElectinMegaMVP"
$reports = "$root\reports"
$logs = "$root\logs"
if (!(Test-Path $reports)) { New-Item -ItemType Directory -Path $reports | Out-Null }
if (!(Test-Path $logs)) { New-Item -ItemType Directory -Path $logs | Out-Null }

# --- Run Agent Researcher
Write-Host "🔍 Running Agent Researcher (scanning repos)..."
python "$root\agent_researcher.py" | Tee-Object "$logs\research.log"

# --- Run Agent Assembler
Write-Host "🧠 Running Agent Assembler (building assembly plan)..."
python "$root\agent_assembler.py" | Tee-Object "$logs\assembly.log"

# --- Run Agent Verifier
Write-Host "✅ Running Agent Verifier (checking data & backend)..."
python "$root\agent_verifier.py" | Tee-Object "$logs\verify.log"

Write-Host "🎯 All agents completed. Check the 'reports' folder for results." -ForegroundColor Green
