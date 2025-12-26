"""
AI对话引擎模块
支持多种AI模型：Claude、豆包、OpenAI等
"""
import os
from typing import List, Dict, Optional
from ..utils import log, config
from ..personality import Persona


class AIEngine:
    """AI对话引擎类"""

    def __init__(self):
        """初始化AI引擎"""
        self.provider = config.get('ai.provider', 'doubao')
        self.model = config.get('ai.model', 'doubao-pro-32k')
        self.max_tokens = config.get('ai.max_tokens', 1000)
        self.temperature = config.get('ai.temperature', 0.8)

        self.persona = Persona()

        # 根据provider初始化不同的客户端
        if self.provider == 'doubao':
            self._init_doubao()
        elif self.provider == 'claude':
            self._init_claude()
        elif self.provider == 'openai':
            self._init_openai()
        else:
            raise ValueError(f"不支持的AI提供商: {self.provider}")

        log.info(f"AI引擎初始化成功，使用提供商: {self.provider}, 模型: {self.model}")

    def _init_doubao(self):
        """初始化豆包API（使用火山引擎SDK）"""
        from volcenginesdkarkruntime import Ark

        self.api_key = config.get_env('DOUBAO_API_KEY')
        if not self.api_key:
            raise ValueError("未设置DOUBAO_API_KEY环境变量")

        base_url = config.get_env('DOUBAO_API_BASE', 'https://ark.cn-beijing.volces.com/api/v3')

        self.client = Ark(
            api_key=self.api_key,
            base_url=base_url
        )
        log.info("豆包API初始化成功（火山引擎SDK）")

    def _init_claude(self):
        """初始化Claude API"""
        from anthropic import Anthropic

        self.api_key = config.get_env('CLAUDE_API_KEY')
        if not self.api_key:
            raise ValueError("未设置CLAUDE_API_KEY环境变量")

        self.client = Anthropic(api_key=self.api_key)
        log.info("Claude API初始化成功")

    def _init_openai(self):
        """初始化OpenAI API"""
        from openai import OpenAI

        self.api_key = config.get_env('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("未设置OPENAI_API_KEY环境变量")

        base_url = config.get_env('OPENAI_API_BASE', 'https://api.openai.com/v1')

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=base_url
        )
        log.info("OpenAI API初始化成功")

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
            if self.provider == 'doubao':
                return self._generate_doubao(message, context)
            elif self.provider == 'claude':
                return self._generate_claude(message, context)
            else:
                # OpenAI使用兼容接口
                return self._generate_openai_compatible(message, context)

        except Exception as e:
            log.error(f"AI生成回复失败: {e}")
            return "抱歉，我现在有点累了，稍后再聊好吗？"

    def _generate_doubao(self, message: str, context: List[Dict[str, str]] = None) -> str:
        """使用火山引擎SDK生成回复"""
        # 构建输入
        input_messages = []

        # 添加历史上下文
        if context:
            for ctx in context:
                input_messages.append({
                    "role": ctx["role"],
                    "content": ctx["content"]
                })

        # 添加当前消息
        input_messages.append({
            "role": "user",
            "content": message
        })

        # 获取系统提示词
        system_prompt = self.persona.get_system_prompt()

        # 构建完整输入（将系统提示词和对话历史合并）
        if input_messages:
            # 将系统提示词添加到第一条用户消息前
            full_input = f"{system_prompt}\n\n{message}"
        else:
            full_input = message

        # 调用火山引擎API
        response = self.client.responses.create(
            model=self.model,
            input=full_input
        )

        # 提取回复内容
        # 根据API返回格式提取文本
        if hasattr(response, 'output') and response.output:
            for item in response.output:
                if hasattr(item, 'type') and item.type == 'message':
                    if hasattr(item, 'content') and item.content:
                        for content_item in item.content:
                            if hasattr(content_item, 'type') and content_item.type == 'output_text':
                                reply = content_item.text
                                log.info(f"AI生成回复: {reply[:50]}...")
                                return reply

        # 如果无法提取，返回默认消息
        log.warning("无法从响应中提取回复内容")
        return "抱歉，我现在有点累了，稍后再聊好吗？"

    def _generate_claude(self, message: str, context: List[Dict[str, str]] = None) -> str:
        """使用Claude API生成回复"""
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

    def _generate_openai_compatible(self, message: str, context: List[Dict[str, str]] = None) -> str:
        """使用OpenAI兼容API生成回复（豆包、OpenAI等）"""
        # 构建消息列表
        messages = []

        # 添加系统提示词
        system_prompt = self.persona.get_system_prompt()
        messages.append({
            "role": "system",
            "content": system_prompt
        })

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

        # 调用API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )

        # 提取回复内容
        reply = response.choices[0].message.content
        log.info(f"AI生成回复: {reply[:50]}...")
        return reply


    def reload_persona(self):
        """重新加载人格配置"""
        self.persona.reload()
        log.info("人格配置已重新加载")

