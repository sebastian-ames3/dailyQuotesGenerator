@echo off
REM Morning Motivation Quote Generator - Uninstall Auto-Launch
REM This removes the Task Scheduler entry for the quote generator

echo.
echo ============================================================
echo  Morning Motivation Quote Generator - Uninstall
echo ============================================================
echo.
echo This will remove the auto-launch quote task.
echo.
pause

REM Delete login task
echo.
echo Removing auto-launch quote task...
schtasks /delete /tn "MorningQuoteOnLogin" /f
if %ERRORLEVEL% EQU 0 (
    echo Task removed successfully.
) else (
    echo Task not found or already removed.
)

echo.
echo ============================================================
echo  Uninstall Complete!
echo ============================================================
echo.
echo Auto-launch quotes have been removed.
echo You can still manually run LaunchQuote.bat to see a quote.
echo.
pause
