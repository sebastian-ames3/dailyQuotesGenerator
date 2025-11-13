@echo off
REM Morning Motivation Quote Generator - Uninstall Scheduled Quotes
REM This removes all Task Scheduler entries for the quote generator

echo.
echo ============================================================
echo  Morning Motivation Quote Generator - Uninstall
echo ============================================================
echo.
echo This will remove the scheduled quote tasks.
echo.
pause

REM Delete scheduled task
echo.
echo Removing scheduled quote task...
schtasks /delete /tn "MorningQuoteScheduled" /f
if %ERRORLEVEL% EQU 0 (
    echo Task removed successfully.
) else (
    echo Task not found or already removed.
)

REM Delete tracker file
set "SCRIPT_DIR=%~dp0"
if exist "%SCRIPT_DIR%.quote_tracker.json" (
    echo Removing quote tracker file...
    del "%SCRIPT_DIR%.quote_tracker.json"
    echo Tracker file removed.
)

echo.
echo ============================================================
echo  Uninstall Complete!
echo ============================================================
echo.
echo Scheduled quotes have been removed.
echo You can still manually run LaunchQuote.bat to see a quote.
echo.
pause
