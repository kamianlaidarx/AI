"""
消息处理器模块
处理微信消息并协调AI回复
"""
import time
import random
import json
from pathlib import Path
from typing import Optional, Dict
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
            max_messages=config.get('ai.max_context_messages', 500)
        )

        # 加载配置
        self.auto_reply = config.get('wechat.auto_reply', True)
        self.reply_delay = config.get('wechat.reply_delay', [1, 3])
        self.whitelist = config.get('filters.whitelist', [])
        self.blacklist = config.get('filters.blacklist', [])

        # 群聊唤醒配置
        self.group_chat_enabled = config.get('group_chat.enabled', True)
        self.end_session_keyword = config.get('group_chat.end_session_keyword', '结束本次会话')
        self.end_session_reply = config.get('group_chat.end_session_reply', '会话已结束，如需唤醒请艾特我。')
        self.test_group = config.get('group_chat.test_group', '')

        # 群聊活跃状态 {群名: bool}
        self.group_active_sessions: Dict[str, bool] = {}

        # 群管理员 {群名: 管理员ID}
        self.group_admins: Dict[str, str] = {}
        self.admins_file = Path(config.get('group_chat.admins_file', 'data/group_admins.json'))
        self._load_admins()

        # 从 persona 获取机器人名字
        self.bot_name = self.ai.persona.config.get('name', '')

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

        log.info(f"消息处理器初始化成功，机器人名字: {self.bot_name}")

    def _load_admins(self):
        """从文件加载群管理员信息"""
        try:
            if self.admins_file.exists():
                with open(self.admins_file, 'r', encoding='utf-8') as f:
                    self.group_admins = json.load(f)
                log.info(f"已加载 {len(self.group_admins)} 个群的管理员信息")
        except Exception as e:
            log.error(f"加载管理员信息失败: {e}")
            self.group_admins = {}

    def _save_admins(self):
        """保存群管理员信息到文件"""
        try:
            self.admins_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.admins_file, 'w', encoding='utf-8') as f:
                json.dump(self.group_admins, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log.error(f"保存管理员信息失败: {e}")

    def _is_admin(self, group: str, user: str) -> bool:
        """检查用户是否是群管理员"""
        return self.group_admins.get(group) == user

    def _set_admin(self, group: str, user: str):
        """设置群管理员（首个唤醒者）"""
        if group not in self.group_admins:
            self.group_admins[group] = user
            self._save_admins()
            log.info(f"群 {group} 的管理员已设为: {user}")

    def _is_group_message(self, sender: str) -> bool:
        """
        判断是否是群聊消息
        wxauto 中群聊的 sender 通常包含群名

        Args:
            sender: 发送者/来源

        Returns:
            是否是群聊消息
        """
        # 如果设置了测试群，只对该群启用唤醒功能
        if self.test_group:
            return sender == self.test_group
        # 未设置测试群时，禁用群聊唤醒功能（所有消息正常响应）
        return False

    def _is_wake_up_message(self, content: str) -> bool:
        """
        检测是否是唤醒消息（@机器人名字）

        Args:
            content: 消息内容

        Returns:
            是否是唤醒消息
        """
        if not self.bot_name:
            return False
        wake_pattern = f"@{self.bot_name}"
        return wake_pattern in content

    def _is_end_session_message(self, content: str) -> bool:
        """
        检测是否是结束会话消息

        Args:
            content: 消息内容

        Returns:
            是否是结束会话消息
        """
        return self._is_wake_up_message(content) and self.end_session_keyword in content

    def _strip_at_prefix(self, content: str) -> str:
        """
        去除消息中的@前缀

        Args:
            content: 原始消息内容

        Returns:
            去除@前缀后的消息
        """
        if self.bot_name:
            wake_pattern = f"@{self.bot_name}"
            content = content.replace(wake_pattern, '').strip()
        return content

    def should_reply(self, sender: str, content: str) -> bool:
        """
        判断是否应该回复该发送者

        Args:
            sender: 发送者名称
            content: 消息内容

        Returns:
            是否应该回复
        """
        # 检查黑名单
        if sender in self.blacklist:
            log.info(f"发送者 {sender} 在黑名单中，忽略消息")
            return False

        # 检查白名单（如果白名单不为空，私聊直接响应）
        if self.whitelist and sender in self.whitelist:
            return True

        # 群聊唤醒逻辑
        if self.group_chat_enabled and self._is_group_message(sender):
            # 检查是否是结束会话消息
            if self._is_end_session_message(content):
                return True  # 需要响应结束消息

            # 检查是否是唤醒消息
            if self._is_wake_up_message(content):
                self.group_active_sessions[sender] = True
                log.info(f"群 {sender} 被唤醒，进入活跃状态")
                return True

            # 检查群是否处于活跃状态
            if self.group_active_sessions.get(sender, False):
                return True

            # 群未被唤醒，不响应
            log.debug(f"群 {sender} 未被唤醒，忽略消息")
            return False

        # 白名单为空时的默认行为
        if self.whitelist and sender not in self.whitelist:
            log.info(f"发送者 {sender} 不在白名单中，忽略消息")
            return False

        return True

    def _handle_command(self, sender: str, content: str, real_sender: str = None) -> Optional[str]:
        """
        处理命令消息

        Args:
            sender: 发送者/群名
            content: 消息内容
            real_sender: 实际发送者

        Returns:
            命令响应，如果不是命令则返回None
        """
        content_stripped = content.strip()

        # /modellist - 查询可用模型（所有人可用）
        if content_stripped == '/modellist':
            models = self.ai.get_available_models()
            if models:
                model_list = '\n'.join([f"• {m}" for m in models[:20]])  # 最多显示20个
                current = self.ai.model
                return f"当前模型: {current}\n\n可用模型:\n{model_list}"
            return "获取模型列表失败"

        # /model <model_name> - 切换模型（仅管理员）
        if content_stripped.startswith('/model '):
            new_model = content_stripped[7:].strip()
            if not new_model:
                return "用法: /model <模型名称>"

            # 检查权限
            user = real_sender or sender
            if self._is_group_message(sender):
                if not self._is_admin(sender, user):
                    admin = self.group_admins.get(sender, '未知')
                    return f"仅管理员可切换模型（当前管理员: {admin}）"

            # 切换模型
            old_model = self.ai.model
            self.ai.set_model(new_model)
            return f"模型已切换: {old_model} → {new_model}"

        return None

    def process_message(self, sender: str, content: str, real_sender: str = None) -> Optional[str]:
        """
        处理消息并生成回复

        Args:
            sender: 发送者/群名
            content: 消息内容
            real_sender: 实际发送者（群聊中的用户名，私聊时为None）

        Returns:
            回复内容，如果不需要回复则返回None
        """
        # 检查是否应该回复
        if not self.should_reply(sender, content):
            return None

        # 群聊时，记录首个唤醒者为管理员
        if self._is_group_message(sender) and self._is_wake_up_message(content):
            if real_sender:
                self._set_admin(sender, real_sender)

        # 处理命令
        cmd_result = self._handle_command(sender, content, real_sender)
        if cmd_result is not None:
            return cmd_result

        # 检查是否是结束会话消息
        if self._is_end_session_message(content):
            self.group_active_sessions[sender] = False
            self.context_manager.clear_context(sender)
            log.info(f"群 {sender} 会话结束，进入休眠状态")
            return self.end_session_reply

        # 消息预处理（去除@前缀）
        processed_content = self._preprocess_message(content)
        processed_content = self._strip_at_prefix(processed_content)

        if not processed_content:
            return None

        # 添加用户消息到上下文
        self.context_manager.add_message(sender, "user", processed_content)

        # 获取对话上下文
        context = self.context_manager.get_context(sender)

        # 生成AI回复
        try:
            reply = self.ai.generate_response(
                message=processed_content,
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

    def handle_message(self, sender: str, content: str, real_sender: str = None):
        """
        完整处理消息流程：接收 -> 处理 -> 回复

        Args:
            sender: 发送者/群名
            content: 消息内容
            real_sender: 实际发送者（群聊中的用户名）
        """
        log.info(f"收到来自 {sender} 的消息: {content[:50]}...")

        # 更新最后消息时间（用于主动对话判断）
        self.proactive_chat.update_last_message_time(sender)

        # 处理消息
        reply = self.process_message(sender, content, real_sender)

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
