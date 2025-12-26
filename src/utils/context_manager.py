"""
上下文管理模块
管理对话历史和上下文
"""
from typing import List, Dict, Any
from collections import deque
from datetime import datetime
import json
from pathlib import Path


class ContextManager:
    """上下文管理类"""

    def __init__(self, max_messages: int = 20, storage_dir: str = "data/conversations"):
        """
        初始化上下文管理器

        Args:
            max_messages: 最大保留消息数
            storage_dir: 对话存储目录
        """
        self.max_messages = max_messages
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # 使用deque实现滑动窗口
        self.contexts: Dict[str, deque] = {}

    def add_message(self, user_id: str, role: str, content: str):
        """
        添加消息到上下文

        Args:
            user_id: 用户ID
            role: 角色（user/assistant）
            content: 消息内容
        """
        if user_id not in self.contexts:
            self.contexts[user_id] = deque(maxlen=self.max_messages)

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }

        self.contexts[user_id].append(message)

    def get_context(self, user_id: str) -> List[Dict[str, Any]]:
        """
        获取用户的对话上下文

        Args:
            user_id: 用户ID

        Returns:
            消息列表
        """
        if user_id not in self.contexts:
            return []

        return list(self.contexts[user_id])

    def clear_context(self, user_id: str):
        """
        清除用户的对话上下文

        Args:
            user_id: 用户ID
        """
        if user_id in self.contexts:
            self.contexts[user_id].clear()

    def save_conversation(self, user_id: str):
        """
        保存对话历史到文件

        Args:
            user_id: 用户ID
        """
        if user_id not in self.contexts or len(self.contexts[user_id]) == 0:
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.storage_dir / f"{user_id}_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(list(self.contexts[user_id]), f, ensure_ascii=False, indent=2)

    def load_conversation(self, user_id: str, filename: str):
        """
        从文件加载对话历史

        Args:
            user_id: 用户ID
            filename: 文件名
        """
        filepath = self.storage_dir / filename

        if not filepath.exists():
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            messages = json.load(f)

        self.contexts[user_id] = deque(messages, maxlen=self.max_messages)

    def get_context_summary(self, user_id: str) -> str:
        """
        获取上下文摘要（用于token优化）

        Args:
            user_id: 用户ID

        Returns:
            上下文摘要
        """
        context = self.get_context(user_id)

        if not context:
            return ""

        # 简单的摘要：保留最近的几条消息
        recent_messages = context[-5:] if len(context) > 5 else context

        summary = []
        for msg in recent_messages:
            summary.append(f"{msg['role']}: {msg['content'][:50]}...")

        return "\n".join(summary)
