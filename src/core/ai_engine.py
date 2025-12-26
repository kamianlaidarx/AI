"""
AI对话引擎模块
集成Claude API实现智能对话
"""
import os
from typing import List, Dict, Optional
from anthropic import Anthropic
from ..utils import log, config
from ..personality import Persona


class AIEngine:
    """AI对话引擎类"""

    def __init__(self):
        """初始化AI引擎"""
        self.api_key = config.get_env('CLAUDE_API_KEY')
        self.model = config.get('ai.model', 'claude-3-5-sonnet-20241022')
        self.max_tokens = config.get('ai.max_tokens', 1000)
        self.temperature = config.get('ai.temperature', 0.8)

        if not self.api_key:
            raise ValueError("未设置CLAUDE_API_KEY环境变量")

        self.client = Anthropic(api_key=self.api_key)
        self.persona = Persona()

        log.info(f"AI引擎初始化成功，使用模型: {self.model}")

    def generate_response(
        self,
        message: str,
        context: List[Dict[str, str]] = None,
        user_id: str = None
    ) -> str:
        """
        生成AI回复

        Args:
            message: 用户消息
            context: 对话上下文
            user_id: 用户ID

        Returns:
            AI回复内容
        """
        try:
            # 构建消息列表
            messages = []

            # 添加历史上下文
            if context:
                for ctx in context:
                    messages.append({
                        "role": ctx["role"],
                        "content": ctx["content"]
                    })

            # 添加当前消息
            messages.append({
                "role": "user",
                "content": message
            })

            # 获取系统提示词
            system_prompt = self.persona.get_system_prompt()

            # 调用Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=messages
            )

            # 提取回复内容
            reply = response.content[0].text

            log.info(f"AI生成回复: {reply[:50]}...")
            return reply

        except Exception as e:
            log.error(f"AI生成回复失败: {e}")
            return "抱歉，我现在有点累了，稍后再聊好吗？"

    def generate_response_stream(
        self,
        message: str,
        context: List[Dict[str, str]] = None
    ):
        """
        流式生成AI回复

        Args:
            message: 用户消息
            context: 对话上下文

        Yields:
            回复内容片段
        """
        try:
            # 构建消息列表
            messages = []

            if context:
                for ctx in context:
                    messages.append({
                        "role": ctx["role"],
                        "content": ctx["content"]
                    })

            messages.append({
                "role": "user",
                "content": message
            })

            system_prompt = self.persona.get_system_prompt()

            # 流式调用
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=messages
            ) as stream:
                for text in stream.text_stream:
                    yield text

        except Exception as e:
            log.error(f"流式生成失败: {e}")
            yield "抱歉，我现在有点累了，稍后再聊好吗？"

    def reload_persona(self):
        """重新加载人格配置"""
        self.persona.reload()
        log.info("人格配置已重新加载")
