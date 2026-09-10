@echo off
chcp 65001 > nul
title GENESIS AI Music & Sampling Studio Launcher
echo ========================================================================
echo  🎵 GENESIS AI MUSIC & SAMPLING STUDIO (PRO EDITION)
echo  YouTube Music Ingestion ✕ Stem Separation ✕ 16-Pad MPC Sampler
echo ========================================================================
echo.

echo [1/2] Verifying GENESIS Cinema & Music Studio Local Server...
netstat -ano | findstr :8080 > nul
if %errorlevel% equ 0 (
    echo  [OK] Local Server already active on port 8080.
) else (
    echo  [STARTING] Launching GENESIS Studio Server in background...
    start /B python GENESIS_CINEMA_STUDIO\server.py
    timeout /t 2 /nobreak > nul
)

echo [2/2] Launching GENESIS Music Studio in your default browser...
start http://127.0.0.1:8080/music_studio.html

echo.
echo ========================================================================
echo  Studio is running at: http://127.0.0.1:8080/music_studio.html
echo  Pads can be played with keys: 1-4 (Drums), Q-R (Bass), A-F (Vocals), Z-V (Melody)
echo ========================================================================
