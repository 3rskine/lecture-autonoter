@echo off
title Course Automation - Starting...

REM Start Docker Desktop if not running
tasklist /FI "IMAGENAME eq Docker Desktop.exe" 2>NUL | find /I "Docker Desktop.exe" >NUL
if errorlevel 1 (
    echo Starting Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    timeout /t 30 /nobreak >nul
)

REM Open browser
start "" "http://localhost:5678"

REM Run startup script in WSL
wsl bash /mnt/c/Course_Automation/start_automation.sh
