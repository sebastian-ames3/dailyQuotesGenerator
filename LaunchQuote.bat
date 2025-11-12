@echo off
REM Morning Motivation Quote Generator - Auto-Launch Batch File
REM This batch file opens the quote as a frameless window (no browser UI)
REM Place a shortcut to this file in your Windows Startup folder

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Convert path to file:/// URL format (replace backslashes and spaces)
set "HTML_PATH=%SCRIPT_DIR%index.html"
set "HTML_PATH=%HTML_PATH:\=/%"

REM Try Chrome first (best --app mode support)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app="file:///%HTML_PATH%" --no-first-run --no-default-browser-check
    exit /b
)

REM Try Edge (built into Windows 10/11)
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app="file:///%HTML_PATH%"
    exit /b
)

REM Try Edge (alternative location for ARM/newer versions)
if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files\Microsoft\Edge\Application\msedge.exe" --app="file:///%HTML_PATH%"
    exit /b
)

REM Fallback to default browser (will show browser UI as a tab)
REM This is not ideal but ensures the quote displays even without Chrome/Edge
start "" "%SCRIPT_DIR%index.html"
