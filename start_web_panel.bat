@echo off
chcp 65001 >nul
echo ========================================
echo AILive Web管理面板启动脚本
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [错误] 未找到虚拟环境，请先运行安装脚本
    pause
    exit /b 1
)

echo [1/2] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [2/2] 启动Web管理面板...
echo.
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务器
echo.
python src\web\app.py

pause
