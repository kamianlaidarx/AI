"""
消息处理器模块
处理微信消息并协调AI回复
"""
import time
import random
from typing import Optional
from ..utils import log, config, ContextManager
from .wechat_client import WeChatClient
from .ai_engine import AIEngine
from .proactive_chat import ProactiveChatManager


class MessageHandler:
    """消息处理器类"""

    def __init__(self, wechat_client: WeChatClient, ai_engine: AIEngine):
        """
        初始化消息处理器

        Args:
            wechat_client: 微信客户端
            ai_engine: AI引擎
        """
        self.wechat = wechat_client
        self.ai = ai_engine
        self.context_manager = ContextManager(
            max_messages=config.get('ai.max_context_messages', 20)
        )

        # 加载配置
        self.auto_reply = config.get('wechat.auto_reply', True)
        self.reply_delay = config.get('wechat.reply_delay', [1, 3])
        self.whitelist = config.get('filters.whitelist', [])
        self.blacklist = config.get('filters.blacklist', [])

        # 初始化主动对话管理器
        proactive_config = config.get('proactive_chat', {
            'enabled': True,
            'idle_time': 3600,  # 1小时
            'min_interval': 1800,  # 30分钟
            'max_daily_proactive': 3
        })
        self.proactive_chat = ProactiveChatManager(
            ai_engine=self.ai,
            context_manager=self.context_manager,
            config=proactive_config
        )

        log.info("消息处理器初始化成功")

    def should_reply(self, sender: str) -> bool:
        """
        判断是否应该回复该发送者

        Args:
            sender: 发送者名称

        Returns:
            是否应该回复
        """
        # 检查黑名单
        if sender in self.blacklist:
            log.info(f"发送者 {sender} 在黑名单中，忽略消息")
            return False

        # 检查白名单（如果白名单不为空）
        if self.whitelist and sender not in self.whitelist:
            log.info(f"发送者 {sender} 不在白名单中，忽略消息")
            return False

        return True

    def process_message(self, sender: str, content: str) -> Optional[str]:
        """
        处理消息并生成回复

        Args:
            sender: 发送者
            content: 消息内容

        Returns:
            回复内容，如果不需要回复则返回None
        """
        # 检查是否应该回复
        if not self.should_reply(sender):
            return None

        # 消息预处理
        content = self._preprocess_message(content)

        if not content:
            return None

        # 添加用户消息到上下文
        self.context_manager.add_message(sender, "user", content)

        # 获取对话上下文
        context = self.context_manager.get_context(sender)

        # 生成AI回复
        try:
            reply = self.ai.generate_response(
                message=content,
                context=context[:-1],  # 不包含刚添加的消息
                user_id=sender
            )

            # 回复后处理
            reply = self._postprocess_reply(reply)

            # 添加AI回复到上下文
            self.context_manager.add_message(sender, "assistant", reply)

            return reply

        except Exception as e:
            log.error(f"处理消息失败: {e}")
            return None

    def _preprocess_message(self, content: str) -> str:
        """
        消息预处理

        Args:
            content: 原始消息内容

        Returns:
            处理后的消息内容
        """
        # 去除首尾空白
        content = content.strip()

        # 过滤空消息
        if not content:
            return ""

        # 这里可以添加更多预处理逻辑
        # 例如：敏感词过滤、特殊字符处理等

        return content

    def _postprocess_reply(self, reply: str) -> str:
        """
        回复后处理

        Args:
            reply: 原始回复内容

        Returns:
            处理后的回复内容
        """
        # 去除首尾空白
        reply = reply.strip()

        # 限制回复长度
        max_length = config.get('wechat.max_message_length', 500)
        if len(reply) > max_length:
            reply = reply[:max_length] + "..."

        return reply

    def send_reply(self, to_user: str, content: str) -> bool:
        """
        发送回复（带延迟）

        Args:
            to_user: 接收人
            content: 回复内容

        Returns:
            是否发送成功
        """
        # 随机延迟，模拟人类打字时间
        delay = random.uniform(self.reply_delay[0], self.reply_delay[1])

        return self.wechat.send_message(to_user, content, delay)

    def handle_message(self, sender: str, content: str):
        """
        完整处理消息流程：接收 -> 处理 -> 回复

        Args:
            sender: 发送者
            content: 消息内容
        """
        log.info(f"收到来自 {sender} 的消息: {content[:50]}...")

        # 更新最后消息时间（用于主动对话判断）
        self.proactive_chat.update_last_message_time(sender)

        # 处理消息
        reply = self.process_message(sender, content)

        if reply and self.auto_reply:
            # 发送回复
            success = self.send_reply(sender, reply)

            if success:
                log.info(f"已回复 {sender}: {reply[:50]}...")
            else:
                log.error(f"回复 {sender} 失败")

    def clear_context(self, user_id: str):
        """
        清除用户的对话上下文

        Args:
            user_id: 用户ID
        """
        self.context_manager.clear_context(user_id)
        log.info(f"已清除 {user_id} 的对话上下文")

    def save_conversation(self, user_id: str):
        """
        保存对话历史

        Args:
            user_id: 用户ID
        """
        self.context_manager.save_conversation(user_id)
        log.info(f"已保存 {user_id} 的对话历史")

    def check_and_send_proactive_messages(self):
        """
        检查并发送主动消息
        应该在主循环中定期调用
        """
        # 获取所有有对话历史的用户
        for user_id in list(self.proactive_chat.last_message_time.keys()):
            # 检查是否应该主动聊天
            if self.proactive_chat.should_initiate_chat(user_id):
                # 生成主动消息
                message = self.proactive_chat.generate_proactive_message(user_id)

                if message:
                    # 发送主动消息
                    success = self.send_reply(user_id, message)

                    if success:
                        # 记录主动聊天
                        self.proactive_chat.record_proactive_chat(user_id)

                        # 添加到上下文
                        self.context_manager.add_message(user_id, "assistant", message)

                        log.info(f"已向 {user_id} 主动发送消息: {message[:50]}...")
                    else:
                        log.error(f"向 {user_id} 发送主动消息失败")
