@echo off
REM Morning Motivation Quote Generator - Install Auto-Launch
REM This creates a Task Scheduler entry to show quotes on every login

echo.
echo ============================================================
echo  Morning Motivation Quote Generator - Installation
echo ============================================================
echo.
echo This will set up quotes to appear on login AND unlock.
echo.
echo How it works:
echo   - When you log in OR unlock, a motivational quote appears
echo   - Quote displays for 25 seconds, then closes
echo   - No background process runs
echo.
pause

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Remove trailing backslash if present
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Create temporary XML file with both triggers
echo.
echo Creating task configuration...
set "TEMP_XML=%TEMP%\MorningQuoteTask.xml"
powershell -Command "(Get-Content '%SCRIPT_DIR%\task_template.xml') -replace 'SCRIPT_DIR_PLACEHOLDER', '%SCRIPT_DIR%' | Set-Content '%TEMP_XML%'"

REM Create the task with both login and unlock triggers
echo Creating auto-launch quote task (triggers on login AND unlock)...
schtasks /create /tn "MorningQuoteOnLogin" /xml "%TEMP_XML%" /f
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to create task. You may need to run as Administrator.
    del "%TEMP_XML%" 2>nul
    pause
    exit /b 1
)

REM Clean up temporary file
del "%TEMP_XML%" 2>nul

echo.
echo ============================================================
echo  Installation Complete!
echo ============================================================
echo.
echo A motivational quote will now appear on login AND unlock.
echo.
echo How it works:
echo   1. When you log in OR unlock, a quote appears automatically
echo   2. Quote displays for 25 seconds in the bottom-right corner
echo   3. No background process runs - only shows on login/unlock
echo.
echo To uninstall: Run uninstall_scheduled_quotes.bat
echo To test now: Double-click LaunchQuote.bat or lock/unlock your PC
echo.
pause
