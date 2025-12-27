@echo off
chcp 65001 >nul
echo ========================================
echo AILive Web Panel Startup
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [Error] Virtual environment not found
    pause
    exit /b 1
)

echo [1/2] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/2] Starting web panel...
echo.
echo Access URL: http://127.0.0.1:5000
echo Press Ctrl+C to stop
echo.
python src\web\app.py

pause
