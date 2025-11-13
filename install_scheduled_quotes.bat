@echo off
REM Morning Motivation Quote Generator - Install Auto-Launch
REM This creates a Task Scheduler entry to show quotes on every login

echo.
echo ============================================================
echo  Morning Motivation Quote Generator - Installation
echo ============================================================
echo.
echo This will set up quotes to appear EVERY TIME you log in.
echo.
echo How it works:
echo   - When you log in, a motivational quote appears
echo   - Quote displays for 15 seconds, then closes
echo   - No background process runs
echo.
pause

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Create login task
echo.
echo Creating auto-launch quote task (triggers on login)...
schtasks /create /tn "MorningQuoteOnLogin" /tr "python \"%SCRIPT_DIR%quote_overlay.py\"" /sc onlogon /rl limited /f
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create task. You may need to run as Administrator.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  Installation Complete!
echo ============================================================
echo.
echo A motivational quote will now appear every time you log in.
echo.
echo How it works:
echo   1. When you log in, a quote appears automatically
echo   2. Quote displays for 15 seconds in the bottom-right corner
echo   3. No background process runs - only shows on login
echo.
echo To uninstall: Run uninstall_scheduled_quotes.bat
echo To test now: Double-click LaunchQuote.bat
echo.
pause
