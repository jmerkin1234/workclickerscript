@echo off
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
    py -m pip install pyinstaller
    if errorlevel 1 goto :error
    py -m PyInstaller --noconfirm --clean --onefile --windowed --name click click.pyw
    goto :done
)

where python >nul 2>nul
if %errorlevel%==0 (
    python -m pip install pyinstaller
    if errorlevel 1 goto :error
    python -m PyInstaller --noconfirm --clean --onefile --windowed --name click click.pyw
    goto :done
)

echo Python is not installed or not on PATH.
goto :end

:error
echo Build failed.
goto :end

:done
echo EXE created in the dist folder.

:end
pause
