@echo off
REM Morning Motivation Quote Generator - Install Scheduled Quotes
REM This creates Task Scheduler entries to show quotes at specific times on login

echo.
echo ============================================================
echo  Morning Motivation Quote Generator - Installation
echo ============================================================
echo.
echo This will set up quotes to appear when you log in during these times:
echo   - 5:00 AM - 11:00 AM (morning window)
echo   - 12:00 PM - 5:00 PM (midday window)
echo.
echo How it works:
echo   - When you log in, the system checks if you're in a time window
echo   - If yes, and you haven't seen a quote in that window today, it shows
echo   - Only shows once per window per day
echo   - No background process runs
echo.
pause

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Create login task that uses the scheduler
echo.
echo Creating scheduled quote task (triggers on login)...
schtasks /create /tn "MorningQuoteScheduled" /tr "python \"%SCRIPT_DIR%quote_scheduler.py\"" /sc onlogon /rl limited /f
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
echo Quote windows:
echo   Morning:  5:00 AM - 11:00 AM (shows once per day in this window)
echo   Midday:   12:00 PM - 5:00 PM (shows once per day in this window)
echo.
echo How it works:
echo   1. When you log in, the scheduler checks the current time
echo   2. If you're in a window and haven't seen that quote today, it shows
echo   3. Quote displays for 15 seconds, then closes
echo   4. No background process runs - only checks on login
echo.
echo Examples:
echo   - Log in at 7am: Morning quote shows
echo   - Log in again at 9am: No quote (already shown today)
echo   - Log in at 1pm: Midday quote shows
echo   - Log in at 10pm: No quote (outside time windows)
echo.
echo To uninstall: Run uninstall_scheduled_quotes.bat
echo.
pause
