@echo off
chcp 65001 >nul
echo ========================================
echo AILive - 微信AI女友机器人
echo 快速配置脚本
echo ========================================
echo.

REM 检查虚拟环境
if not exist "venv\" (
    echo [1/4] 创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo 错误：创建虚拟环境失败
        pause
        exit /b 1
    )
    echo ✓ 虚拟环境创建成功
) else (
    echo [1/4] 虚拟环境已存在
)
echo.

REM 激活虚拟环境
echo [2/4] 激活虚拟环境...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo 错误：激活虚拟环境失败
    pause
    exit /b 1
)
echo ✓ 虚拟环境已激活
echo.

REM 升级pip
echo [3/4] 升级pip...
python -m pip install --upgrade pip -q
echo ✓ pip已升级
echo.

REM 安装依赖
echo [4/4] 安装依赖包...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo 错误：安装依赖失败
    pause
    exit /b 1
)
echo ✓ 依赖包安装成功
echo.

REM 检查配置文件
if not exist "config\.env" (
    echo ========================================
    echo 配置环境变量
    echo ========================================
    echo.
    echo 正在复制环境变量模板...
    copy config\.env.example config\.env >nul
    echo ✓ 已创建 config\.env 文件
    echo.
    echo ⚠️  请编辑 config\.env 文件，填入你的API密钥：
    echo    - DOUBAO_API_KEY=你的豆包API密钥
    echo.
    echo 然后运行以下命令测试：
    echo    python src\main.py --mode interactive
    echo.
) else (
    echo ========================================
    echo 配置完成！
    echo ========================================
    echo.
    echo 你可以运行以下命令：
    echo.
    echo 1. 交互测试模式（不需要微信）：
    echo    python src\main.py --mode interactive
    echo.
    echo 2. 正常模式（需要微信登录）：
    echo    python src\main.py
    echo.
)

echo 查看配置说明：
echo    - README.md - 使用说明
echo    - DOUBAO_SETUP.md - 豆包API配置指南
echo.

pause
