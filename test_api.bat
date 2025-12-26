@echo off
chcp 65001 >nul
echo ========================================
echo 豆包API配置测试
echo ========================================
echo.

echo 当前配置信息：
echo - API Key: 12d8f57f-9ac5-4988-8d82-87e9bdd47d0e
echo - Endpoint ID: ep-20251226192412-8kff2
echo - Base URL: https://ark.cn-beijing.volces.com/api/v3
echo.

echo 开始测试API连接...
echo.

python test_doubao_api.py

echo.
echo ========================================
echo 测试完成
echo ========================================
echo.

if errorlevel 1 (
    echo ❌ 测试失败，请检查：
    echo    1. 是否已安装依赖：pip install openai python-dotenv
    echo    2. API密钥是否正确
    echo    3. Endpoint ID是否正确
    echo    4. 网络连接是否正常
) else (
    echo ✅ 测试通过！可以运行主程序了：
    echo    python src/main.py --mode interactive
)

echo.
pause
