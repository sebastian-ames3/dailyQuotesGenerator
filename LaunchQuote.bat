@echo off
REM Morning Motivation Quote Generator - Auto-Launch Batch File
REM This batch file launches a true frameless overlay window using Python
REM Place a shortcut to this file in your Windows Startup folder

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Try to run the Python overlay script (frameless window - no console, no browser UI)
pythonw "%SCRIPT_DIR%quote_overlay.py"
if %ERRORLEVEL% EQU 0 (
    exit /b
)

REM If pythonw fails, try python3w command
python3w "%SCRIPT_DIR%quote_overlay.py"
if %ERRORLEVEL% EQU 0 (
    exit /b
)

REM If Python not found, try pyw launcher
pyw "%SCRIPT_DIR%quote_overlay.py"
if %ERRORLEVEL% EQU 0 (
    exit /b
)

REM Fallback: Open in browser (less ideal, but ensures quote displays)
REM Convert path to file:/// URL format
set "HTML_PATH=%SCRIPT_DIR%index.html"
set "HTML_PATH=%HTML_PATH:\=/%"

REM Try Chrome in app mode
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app="file:///%HTML_PATH%" --no-first-run --no-default-browser-check
    exit /b
)

REM Try Edge in app mode
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app="file:///%HTML_PATH%"
    exit /b
)

if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files\Microsoft\Edge\Application\msedge.exe" --app="file:///%HTML_PATH%"
    exit /b
)

REM Final fallback: default browser
start "" "%SCRIPT_DIR%index.html"
