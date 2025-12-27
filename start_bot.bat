@echo off
chcp 65001 >nul
echo ========================================
echo AILive WeChat Bot Startup
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [Error] Virtual environment not found
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Checking WeChat status...
echo Please make sure WeChat is running and logged in
echo.

echo [3/3] Starting AILive bot...
echo.
echo Bot is running. Press Ctrl+C to stop
echo.
python src\main.py

pause
