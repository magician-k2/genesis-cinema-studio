@echo off
chcp 65001 > nul
cls
echo ===============================================================================
echo   ⚡ GENESIS STANDALONE MICRO-CORE & LIVE XAI DEMO
echo   (Google x Devpost "All Things Agentic" Official Instant Judge Runner)
echo ===============================================================================
echo.
echo   [INFO] Zero-Setup Instant Verification:
echo   - No API Key Required
echo   - No Python / Pip Dependencies Required
echo   - In-Browser WebGPU 10,000 Neuromorphic SNN Active Inference
echo   - Real-time Reverse-Mindmap Causal Reasoning & Merkle Proof
echo.
echo   Launching standalone instant demo in your default browser...
echo.

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo   [INFO] Python detected. Starting local micro-server on port 8080...
    start "" /b python -m http.server 8080 >nul 2>nul
    timeout /t 1 >nul
    start "" "http://localhost:8080/web/genesis_standalone_instant_demo.html"
) else (
    echo   [INFO] Opening standalone HTML bundle directly...
    start "" "%~dp0web\genesis_standalone_instant_demo.html"
)

echo.
echo   ✅ DEMO LAUNCHED SUCCESSFULLY!
echo   Please enjoy the live WebGPU Neuromorphic SNN & XAI Reverse-Mindmap.
echo ===============================================================================
pause
