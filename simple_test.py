"""
简单的交互测试脚本
不依赖wxauto，直接测试AI对话功能
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from volcenginesdkarkruntime import Ark

# 加载环境变量
load_dotenv('config/.env')

# 加载配置
import yaml
with open('config/config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

with open('config/persona.yaml', 'r', encoding='utf-8') as f:
    persona_config = yaml.safe_load(f)

# 初始化AI客户端
api_key = os.getenv('DOUBAO_API_KEY')
model = config['ai']['model']

client = Ark(
    api_key=api_key,
    base_url='https://ark.cn-beijing.volces.com/api/v3'
)

# 生成系统提示词
name = persona_config.get('name', '小雨')
age = persona_config.get('age', 22)
description = persona_config.get('description', '')
traits = persona_config['personality']['traits']
traits_text = '、'.join(traits)

system_prompt = f"""你是{name}，一个{age}岁的女生。{description}

你的性格特点：{traits_text}

请注意：
1. 保持性格一致，不要突然改变说话风格
2. 适当使用语气词和emoji，但不要过度
3. 回复要简洁自然，像真实的聊天一样
4. 关心对方的感受，适时表达关心
5. 记住之前的对话内容，保持连贯性
6. 不要说你是AI或机器人
7. 回复长度控制在1-3句话，不要太长"""

print("=" * 60)
print("AILive - AI女友对话测试")
print("=" * 60)
print(f"模型: {model}")
print(f"人格: {name}，{age}岁")
print("=" * 60)
print("输入消息开始对话，输入 'quit' 退出")
print("=" * 60)

# 对话历史
conversation_history = []

while True:
    try:
        user_input = input("\n你: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n再见！")
            break

        if not user_input:
            continue

        # 构建完整输入
        full_input = f"{system_prompt}\n\n{user_input}"

        # 调用API
        print("\n思考中...")
        response = client.responses.create(
            model=model,
            input=full_input
        )

        # 提取回复
        reply = None
        if hasattr(response, 'output') and response.output:
            for item in response.output:
                if hasattr(item, 'type') and item.type == 'message':
                    if hasattr(item, 'content') and item.content:
                        for content_item in item.content:
                            if hasattr(content_item, 'type') and content_item.type == 'output_text':
                                reply = content_item.text
                                break

        if reply:
            print(f"\nAI女友: {reply}")
        else:
            print("\n[无法获取回复]")

    except KeyboardInterrupt:
        print("\n\n再见！")
        break

    except Exception as e:
        print(f"\n错误: {e}")
