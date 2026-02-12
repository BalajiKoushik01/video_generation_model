@echo off
echo Launching Hollywood Studio...
cd /d "%~dp0"
py gui.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Failed to launch with 'py'. Trying 'python'...
    python gui.py
)
if %errorlevel% neq 0 (
    echo.
    echo ❌ Launch Failed. Please check if Python is installed.
    pause
    exit /b 1
)
exit /b 0
