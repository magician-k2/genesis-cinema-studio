@echo off
title GENESIS 24/7 Sentinel Orchestrator Daemon
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================================
echo   🏛️ GENESIS 24/7 Autonomous Sentinel Watchdog
echo   Antigravity 2.0 (Conductor) ^<==^> SDK ^<==^> IDE (LSP)
echo ========================================================
echo.
echo [INFO] Starting Autonomous Sentinel Daemon in background...
echo [INFO] Monitoring file changes and enforcing Triple-Shield All-Green...
echo.

python scripts\genesis_sentinel_daemon.py

pause
