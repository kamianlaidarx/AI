"""
测试豆包API连接
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# 加载环境变量
load_dotenv('config/.env')

# 测试OpenAI兼容接口
def test_openai_compatible():
    """测试使用OpenAI SDK调用豆包API"""
    try:
        from openai import OpenAI

        api_key = os.getenv('DOUBAO_API_KEY')
        base_url = os.getenv('DOUBAO_API_BASE', 'https://ark.cn-beijing.volces.com/api/v3')

        print(f"API Key: {api_key[:20]}...")
        print(f"Base URL: {base_url}")

        client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )

        print("\n发送测试消息...")
        response = client.chat.completions.create(
            model="ep-20251226192412-8kff2",
            messages=[
                {"role": "system", "content": "你是一个友好的AI助手。"},
                {"role": "user", "content": "你好，请简单介绍一下你自己。"}
            ],
            max_tokens=100,
            temperature=0.8
        )

        reply = response.choices[0].message.content
        print(f"\n✅ API调用成功！")
        print(f"回复: {reply}")
        return True

    except Exception as e:
        print(f"\n❌ API调用失败: {e}")
        return False

# 测试火山引擎SDK
def test_volcengine_sdk():
    """测试使用火山引擎官方SDK"""
    try:
        from volcenginesdkarkruntime import Ark

        api_key = os.getenv('DOUBAO_API_KEY')

        print(f"\n使用火山引擎SDK测试...")
        print(f"API Key: {api_key[:20]}...")

        client = Ark(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=api_key,
        )

        print("\n发送测试消息...")
        response = client.responses.create(
            model="ep-20251226192412-8kff2",
            input="你好，请简单介绍一下你自己。"
        )

        print(f"\n✅ 火山引擎SDK调用成功！")
        print(f"回复: {response}")
        return True

    except ImportError:
        print("\n⚠️ 未安装火山引擎SDK，跳过此测试")
        print("安装命令: pip install 'volcengine-python-sdk[ark]'")
        return None
    except Exception as e:
        print(f"\n❌ 火山引擎SDK调用失败: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("豆包API连接测试")
    print("=" * 60)

    # 测试1: OpenAI兼容接口
    print("\n【测试1】使用OpenAI SDK（兼容接口）")
    print("-" * 60)
    result1 = test_openai_compatible()

    # 测试2: 火山引擎官方SDK
    print("\n" + "=" * 60)
    print("【测试2】使用火山引擎官方SDK")
    print("-" * 60)
    result2 = test_volcengine_sdk()

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"OpenAI兼容接口: {'✅ 通过' if result1 else '❌ 失败'}")
    if result2 is not None:
        print(f"火山引擎SDK: {'✅ 通过' if result2 else '❌ 失败'}")
    else:
        print(f"火山引擎SDK: ⚠️ 未安装")

    if result1:
        print("\n✅ 推荐使用OpenAI兼容接口，当前项目已配置")
    elif result2:
        print("\n⚠️ OpenAI接口失败，但火山引擎SDK可用")
        print("建议修改代码使用火山引擎SDK")
