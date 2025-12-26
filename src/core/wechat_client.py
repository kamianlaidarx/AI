"""
微信客户端模块
基于wxauto实现微信消息收发
"""
import time
from typing import List, Dict, Optional
from ..utils import log

# 尝试导入wxauto，如果失败则设为None
try:
    # 添加类型注解兼容性支持
    import sys
    if sys.version_info < (3, 9):
        # Python 3.8及以下版本需要这个
        from typing import List as _List
        import typing
        if not hasattr(typing, 'get_origin'):
            # 为旧版本Python添加兼容性
            pass

    from wxauto import WeChat
    WXAUTO_AVAILABLE = True
except (ImportError, TypeError) as e:
    WeChat = None
    WXAUTO_AVAILABLE = False
    log.warning(f"wxauto未安装或版本不兼容: {e}")
    log.warning("使用交互模式测试：python src/main.py --mode interactive")


class WeChatClient:
    """微信客户端类"""

    def __init__(self):
        """初始化微信客户端"""
        if not WXAUTO_AVAILABLE:
            raise ImportError(
                "wxauto未安装或版本不兼容，无法使用微信功能。\n"
                "解决方案：\n"
                "1. 运行修复脚本: python fix_wxauto.py\n"
                "2. 或使用交互模式测试：python src/main.py --mode interactive"
            )

        self.wx = None
        self.last_messages = {}  # 用于消息去重
        self._init_client()

    def _init_client(self):
        """初始化微信客户端"""
        try:
            self.wx = WeChat()
            log.info("微信客户端初始化成功")
        except Exception as e:
            log.error(f"微信客户端初始化失败: {e}")
            raise

    def get_latest_messages(self, who: str = None) -> List[Dict[str, str]]:
        """
        获取最新消息

        Args:
            who: 联系人名称，None表示获取所有消息

        Returns:
            消息列表，每条消息包含 sender, content, time
        """
        try:
            if who:
                # 获取指定联系人的消息
                messages = self.wx.GetAllMessage(who=who)
            else:
                # 获取所有消息
                messages = self.wx.GetAllMessage()

            # 消息去重
            new_messages = []
            for msg in messages:
                msg_id = f"{msg.get('sender', '')}_{msg.get('time', '')}_{msg.get('content', '')}"

                if msg_id not in self.last_messages:
                    self.last_messages[msg_id] = True
                    new_messages.append(msg)

            return new_messages

        except Exception as e:
            log.error(f"获取消息失败: {e}")
            return []

    def send_message(self, to_user: str, content: str, delay: float = 0) -> bool:
        """
        发送消息

        Args:
            to_user: 接收人
            content: 消息内容
            delay: 发送延迟（秒）

        Returns:
            是否发送成功
        """
        try:
            if delay > 0:
                time.sleep(delay)

            self.wx.SendMsg(msg=content, who=to_user)
            log.info(f"发送消息给 {to_user}: {content[:50]}...")
            return True

        except Exception as e:
            log.error(f"发送消息失败: {e}")
            return False

    def get_contacts(self) -> List[str]:
        """
        获取联系人列表

        Returns:
            联系人名称列表
        """
        try:
            contacts = self.wx.GetAllContacts()
            return contacts
        except Exception as e:
            log.error(f"获取联系人列表失败: {e}")
            return []

    def is_online(self) -> bool:
        """
        检查微信是否在线

        Returns:
            是否在线
        """
        try:
            # 尝试获取联系人列表来判断是否在线
            self.wx.GetAllContacts()
            return True
        except:
            return False

    def clear_message_cache(self):
        """清除消息缓存"""
        self.last_messages.clear()
        log.info("消息缓存已清除")
