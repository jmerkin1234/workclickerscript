@echo off
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    start "" pyw click.pyw
    exit /b 0
)

where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw click.pyw
    exit /b 0
)

echo Python is not installed or not on PATH.
echo Install Python for Windows, then run this file again.
pause
