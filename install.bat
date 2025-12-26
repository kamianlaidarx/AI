@echo off
chcp 65001 >nul
echo ========================================
echo AILive - 依赖安装脚本
echo ========================================
echo.

echo [1/3] 安装基础依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 基础依赖安装失败
    pause
    exit /b 1
)
echo ✅ 基础依赖安装成功
echo.

echo [2/3] 安装wxauto（微信集成）...
echo 提示：如果只测试AI功能，可以跳过此步骤
echo.
choice /C YN /M "是否安装wxauto（需要连接微信时才需要）"
if errorlevel 2 (
    echo ⏭️  跳过wxauto安装
    echo 提示：使用交互模式测试：python src/main.py --mode interactive
    goto test
)

echo 正在从PyPI官方源安装wxauto...
pip install wxauto -i https://pypi.org/simple
if errorlevel 1 (
    echo.
    echo ⚠️  从官方源安装失败，尝试从清华源安装...
    pip install wxauto -i https://pypi.tuna.tsinghua.edu.cn/simple
    if errorlevel 1 (
        echo ❌ wxauto安装失败
        echo 请查看 INSTALL_WECHAT.md 获取更多安装方法
        echo.
        echo 提示：可以先不安装wxauto，使用交互模式测试AI功能
        goto test
    )
)
echo ✅ wxauto安装成功
echo.

:test
echo [3/3] 测试安装...
python -c "import openai, yaml, loguru; print('✅ 核心依赖检查通过')"
if errorlevel 1 (
    echo ❌ 依赖检查失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 下一步：
echo.
echo 1. 测试API连接：
echo    python test_doubao_api.py
echo.
echo 2. 交互测试模式（不需要微信）：
echo    python src/main.py --mode interactive
echo.
echo 3. 连接微信（需要wxauto）：
echo    python src/main.py
echo.
echo 查看文档：
echo    - READY_TO_RUN.md - 配置完成指南
echo    - INSTALL_WECHAT.md - wxauto安装指南
echo.

pause
