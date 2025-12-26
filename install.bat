@echo off
echo ========================================
echo AILive - Dependency Installation
echo ========================================
echo.

echo [1/3] Installing core dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install core dependencies
    pause
    exit /b 1
)
echo SUCCESS: Core dependencies installed
echo.

echo [2/3] Installing wxauto (WeChat integration)...
echo Note: You can skip this if you only want to test AI features
echo.
set /p INSTALL_WXAUTO="Install wxauto? (Y/N): "
if /i "%INSTALL_WXAUTO%"=="N" goto test
if /i "%INSTALL_WXAUTO%"=="n" goto test

echo Installing wxauto from PyPI official source...
pip install wxauto -i https://pypi.org/simple
if errorlevel 1 (
    echo.
    echo WARNING: Failed from official source, trying Tsinghua mirror...
    pip install wxauto -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo ERROR: wxauto installation failed
        echo See INSTALL_WECHAT.md for more installation methods
        echo.
        echo TIP: You can test AI features without wxauto using interactive mode
        goto test
    )
)
echo SUCCESS: wxauto installed
echo.

:test
echo [3/3] Testing installation...
python -c "import openai, yaml, loguru; print('SUCCESS: Core dependencies verified')"
if errorlevel 1 (
    echo ERROR: Dependency check failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Test API connection:
echo    python test_doubao_api.py
echo.
echo 2. Interactive test mode (no WeChat needed):
echo    python src/main.py --mode interactive
echo.
echo 3. Connect to WeChat (requires wxauto):
echo    python src/main.py
echo.
echo Documentation:
echo    - READY_TO_RUN.md - Setup complete guide
echo    - INSTALL_WECHAT.md - wxauto installation guide
echo.

pause
