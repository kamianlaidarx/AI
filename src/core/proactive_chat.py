"""
主动对话管理器
管理机器人的主动聊天行为
"""
import time
import random
from typing import Dict, Optional
from datetime import datetime, timedelta
from ..utils import log


class ProactiveChatManager:
    """主动对话管理器"""

    def __init__(self, ai_engine, context_manager, config: dict):
        """
        初始化主动对话管理器

        Args:
            ai_engine: AI引擎
            context_manager: 上下文管理器
            config: 配置字典
        """
        self.ai = ai_engine
        self.context_manager = context_manager

        # 配置参数
        self.enabled = config.get('enabled', True)
        self.idle_time = config.get('idle_time', 3600)  # 默认1小时无消息后主动聊天
        self.min_interval = config.get('min_interval', 1800)  # 最小间隔30分钟
        self.max_daily_proactive = config.get('max_daily_proactive', 3)  # 每天最多主动3次

        # 跟踪每个用户的最后消息时间
        self.last_message_time: Dict[str, datetime] = {}

        # 跟踪每个用户今天的主动次数
        self.daily_proactive_count: Dict[str, int] = {}
        self.last_reset_date: Optional[str] = None

        log.info(f"主动对话管理器初始化完成 (闲置时间: {self.idle_time}秒)")

    def update_last_message_time(self, user_id: str):
        """
        更新用户的最后消息时间

        Args:
            user_id: 用户ID
        """
        self.last_message_time[user_id] = datetime.now()

    def should_initiate_chat(self, user_id: str) -> bool:
        """
        判断是否应该主动发起对话

        Args:
            user_id: 用户ID

        Returns:
            是否应该主动聊天
        """
        if not self.enabled:
            return False

        # 重置每日计数（如果是新的一天）
        self._reset_daily_count_if_needed()

        # 检查今天是否已达到主动次数上限
        if self.daily_proactive_count.get(user_id, 0) >= self.max_daily_proactive:
            return False

        # 检查是否有历史消息（没有历史就不主动）
        context = self.context_manager.get_context(user_id)
        if not context or len(context) < 2:
            return False

        # 检查最后消息时间
        if user_id not in self.last_message_time:
            return False

        time_since_last = datetime.now() - self.last_message_time[user_id]

        # 检查是否超过闲置时间
        if time_since_last.total_seconds() < self.idle_time:
            return False

        # 检查是否满足最小间隔（避免频繁主动）
        if time_since_last.total_seconds() < self.min_interval:
            return False

        # 随机性：不是每次都主动（30%概率）
        if random.random() > 0.3:
            return False

        return True

    def generate_proactive_message(self, user_id: str) -> Optional[str]:
        """
        生成主动聊天的消息

        Args:
            user_id: 用户ID

        Returns:
            主动消息内容
        """
        try:
            # 获取对话上下文
            context = self.context_manager.get_context(user_id)

            if not context:
                return None

            # 构建主动聊天的提示词
            proactive_prompts = [
                "好久没聊天了，想你了呀~",
                "在干嘛呢？",
                "突然想起你了~",
                "有没有想我呀？",
                "最近怎么样？",
            ]

            # 基于上下文生成更自然的主动消息
            last_topic = self._extract_last_topic(context)

            if last_topic:
                # 基于上次话题生成
                prompt = f"基于我们上次聊到的'{last_topic}'，生成一条自然的、关心对方的主动问候消息。要求：1)简短自然 2)体现关心 3)可以延续话题或询问近况 4)不要太正式"

                response = self.ai.generate_response(
                    message=prompt,
                    context=context[-5:],  # 只用最近5条
                    user_id=user_id
                )

                if response:
                    return response

            # 如果生成失败，使用预设消息
            return random.choice(proactive_prompts)

        except Exception as e:
            log.error(f"生成主动消息失败: {e}")
            return None

    def record_proactive_chat(self, user_id: str):
        """
        记录一次主动聊天

        Args:
            user_id: 用户ID
        """
        if user_id not in self.daily_proactive_count:
            self.daily_proactive_count[user_id] = 0

        self.daily_proactive_count[user_id] += 1
        self.update_last_message_time(user_id)

        log.info(f"已向 {user_id} 主动发起对话 (今日第{self.daily_proactive_count[user_id]}次)")

    def _reset_daily_count_if_needed(self):
        """重置每日计数（如果是新的一天）"""
        today = datetime.now().strftime("%Y-%m-%d")

        if self.last_reset_date != today:
            self.daily_proactive_count.clear()
            self.last_reset_date = today
            log.info("已重置每日主动对话计数")

    def _extract_last_topic(self, context: list) -> Optional[str]:
        """
        从上下文中提取最后的话题

        Args:
            context: 对话上下文

        Returns:
            话题关键词
        """
        if not context:
            return None

        # 获取最近的用户消息
        recent_user_messages = [
            msg['content'] for msg in context[-5:]
            if msg['role'] == 'user'
        ]

        if recent_user_messages:
            # 返回最后一条用户消息的前20个字符作为话题
            last_message = recent_user_messages[-1]
            return last_message[:20] if len(last_message) > 20 else last_message

        return None
