"""
微信客户端模块
支持 wxauto (微信3.9) 和 WeChatFerry (微信4.0+)
"""
import time
from typing import List, Dict, Optional
from ..utils import log, config

# 尝试导入不同的微信库
WECHAT_BACKEND = None
WeChat = None
Wcf = None

# 检查微信版本，决定使用哪个库
def get_wechat_version():
    """获取微信版本"""
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat")
        version, _ = winreg.QueryValueEx(key, "Version")
        winreg.CloseKey(key)
        # 转换为字符串
        return str(version) if version else None
    except:
        return None

wechat_version = get_wechat_version()

# 优先尝试 wxauto（适用于微信3.9）
try:
    import sys
    if sys.version_info < (3, 9):
        from typing import List as _List
        import typing
        if not hasattr(typing, 'get_origin'):
            pass

    from wxauto import WeChat as WxAutoWeChat
    WeChat = WxAutoWeChat
    WECHAT_BACKEND = 'wxauto'
    if wechat_version:
        log.info(f"检测到微信版本 {wechat_version}，使用 wxauto")
    else:
        log.info("使用 wxauto（推荐用于微信3.9）")
except (ImportError, TypeError) as e:
    log.warning(f"wxauto未安装或版本不兼容: {e}")
    # 如果wxauto失败，再尝试 WeChatFerry（仅用于微信4.0+）
    if wechat_version and wechat_version.startswith("4."):
        try:
            from wcferry import Wcf as WcfClient, WxMsg
            Wcf = WcfClient
            WECHAT_BACKEND = 'wcferry'
            log.info("检测到 WeChatFerry，将使用此库（支持微信4.0+）")
        except ImportError:
            pass

if WECHAT_BACKEND is None:
    log.error("未找到可用的微信库！请安装 wxauto: pip install git+https://github.com/cluic/wxauto.git")


class WeChatClient:
    """微信客户端类（支持多种后端）"""

    def __init__(self):
        """初始化微信客户端"""
        if WECHAT_BACKEND is None:
            raise ImportError(
                "未找到可用的微信库！\n"
                "请安装以下之一：\n"
                "1. WeChatFerry (支持微信4.0+): pip install wcferry\n"
                "2. wxauto (仅支持微信3.9): pip install git+https://github.com/cluic/wxauto.git\n"
                "或使用交互模式测试：python src/main.py --mode interactive"
            )

        self.backend = WECHAT_BACKEND
        self.client = None
        self.last_messages = {}  # 用于消息去重
        self.initialized = False  # 标记是否已初始化（清空历史消息）
        self._init_client()

    def _init_client(self):
        """初始化微信客户端"""
        try:
            if self.backend == 'wcferry':
                try:
                    self._init_wcferry()
                except Exception as e:
                    log.warning(f"WeChatFerry 初始化失败: {e}")
                    log.info("尝试使用 wxauto...")
                    # 切换到 wxauto
                    if WeChat is not None:
                        self.backend = 'wxauto'
                        self._init_wxauto()
                    else:
                        raise Exception("WeChatFerry 和 wxauto 都不可用")
            elif self.backend == 'wxauto':
                self._init_wxauto()
            else:
                raise ValueError(f"不支持的后端: {self.backend}")

            log.info(f"微信客户端初始化成功（使用 {self.backend}）")

        except Exception as e:
            log.error(f"微信客户端初始化失败: {e}")
            raise

    def _init_wcferry(self):
        """初始化 WeChatFerry"""
        import os

        # 从配置文件读取微信路径（如果有）
        wechat_path = config.get('wechat.path', None)

        # 如果配置了路径，设置环境变量（WeChatFerry会读取这个环境变量）
        if wechat_path and os.path.exists(wechat_path):
            log.info(f"使用配置的微信路径: {wechat_path}")
            # 设置环境变量，WeChatFerry会从这里读取
            os.environ['WECHAT_DIR'] = wechat_path
            # 也尝试设置这个
            os.environ['WECHAT_PATH'] = wechat_path

        # 初始化 WeChatFerry（不传参数）
        self.client = Wcf()

        # 检查是否登录
        if not self.client.is_login():
            raise Exception("微信未登录，请先登录微信客户端")

    def _init_wxauto(self):
        """初始化 wxauto"""
        self.client = WeChat()

    def get_latest_messages(self, who: str = None) -> List[Dict[str, str]]:
        """
        获取最新消息

        Args:
            who: 联系人名称，None表示获取所有消息

        Returns:
            消息列表，每条消息包含 sender, content, time
        """
        try:
            # 第一次调用时，清空所有历史消息（不返回）
            if not self.initialized:
                log.info("首次启动，正在清空历史消息...")
                if self.backend == 'wcferry':
                    self._get_messages_wcferry()
                elif self.backend == 'wxauto':
                    self._get_messages_wxauto(who)
                self.initialized = True
                log.info("历史消息已清空，开始监听新消息")
                return []  # 第一次不返回任何消息

            # 正常获取消息
            if self.backend == 'wcferry':
                return self._get_messages_wcferry()
            elif self.backend == 'wxauto':
                return self._get_messages_wxauto(who)
            return []

        except Exception as e:
            log.error(f"获取消息失败: {e}")
            return []

    def _get_messages_wcferry(self) -> List[Dict[str, str]]:
        """使用 WeChatFerry 获取消息"""
        new_messages = []

        # WeChatFerry 使用回调方式接收消息
        # 这里我们需要轮询获取消息
        while self.client.is_receiving_msg():
            msg = self.client.get_msg()
            if msg:
                # 转换为统一格式
                msg_dict = {
                    'sender': msg.sender,
                    'content': msg.content,
                    'time': str(msg.ts),
                    'type': msg.type
                }

                # 消息去重
                msg_id = f"{msg.sender}_{msg.ts}_{msg.content}"
                if msg_id not in self.last_messages:
                    self.last_messages[msg_id] = True
                    # 只处理文本消息
                    if msg.type == 1:  # 文本消息
                        new_messages.append(msg_dict)

        return new_messages

    def _get_messages_wxauto(self, who: str = None) -> List[Dict[str, str]]:
        """使用 wxauto 获取消息"""
        if who:
            messages = self.client.GetAllMessage(who=who)
        else:
            messages = self.client.GetAllMessage()

        # 消息去重
        new_messages = []
        for msg in messages:
            # 跳过时间消息
            if 'TimeMessage' in str(type(msg)):
                continue

            # 跳过自己发送的消息
            if 'SelfTextMessage' in str(type(msg)) or 'SelfFileMessage' in str(type(msg)):
                continue

            # 处理好友文本消息
            if 'FriendTextMessage' in str(type(msg)):
                try:
                    # 从消息对象中提取信息
                    content = str(msg.content) if hasattr(msg, 'content') else str(msg)
                    time_str = str(msg.time) if hasattr(msg, 'time') else ''

                    # 获取聊天窗口名（群名或好友名）和实际发送者
                    # wxauto 的 sender 是消息发送者，对于群聊就是群成员名
                    # 需要从 info 或 chat 属性获取群名
                    chat_name = None
                    real_sender = None

                    # 尝试获取聊天窗口名称
                    if hasattr(msg, 'chat'):
                        chat_name = str(msg.chat)
                    elif hasattr(msg, 'chatroom'):
                        chat_name = str(msg.chatroom)
                    elif hasattr(msg, 'info') and msg.info:
                        # info 可能包含群名信息
                        chat_name = str(msg.info)

                    # 获取实际发送者
                    sender_name = str(msg.sender) if hasattr(msg, 'sender') else 'Unknown'

                    # 如果没有 chat_name，说明是私聊，sender 就是聊天窗口
                    if chat_name:
                        real_sender = sender_name
                    else:
                        chat_name = sender_name

                    # 构建消息字典
                    msg_dict = {
                        'sender': chat_name,
                        'content': content,
                        'time': time_str,
                        'real_sender': real_sender
                    }

                    # 消息去重
                    msg_id = f"{chat_name}_{time_str}_{content}"
                    if msg_id not in self.last_messages:
                        self.last_messages[msg_id] = True
                        new_messages.append(msg_dict)
                        log.debug(f"收到新消息: {chat_name} - {content}")

                except Exception as e:
                    log.error(f"解析消息失败: {e}, 消息对象: {msg}")
                    continue

        return new_messages

    def send_message(self, to_user: str, content: str, delay: float = 0) -> bool:
        """
        发送消息

        Args:
            to_user: 接收人（聊天窗口名称：群名或好友昵称）
            content: 消息内容
            delay: 发送延迟（秒）

        Returns:
            是否发送成功
        """
        try:
            if delay > 0:
                time.sleep(delay)

            if self.backend == 'wcferry':
                # WeChatFerry 需要 wxid
                self.client.send_text(content, to_user)
            elif self.backend == 'wxauto':
                # wxauto 需要先切换到聊天窗口再发送
                self.client.ChatWith(to_user)
                self.client.SendMsg(msg=content)

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
            if self.backend == 'wcferry':
                contacts = self.client.get_contacts()
                return [c['name'] for c in contacts]
            elif self.backend == 'wxauto':
                return self.client.GetAllContacts()
            return []

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
            if self.backend == 'wcferry':
                return self.client.is_login()
            elif self.backend == 'wxauto':
                # wxauto 如果初始化成功就说明在线
                return self.client is not None
            return False

        except:
            return False

    def clear_message_cache(self):
        """清除消息缓存"""
        self.last_messages.clear()
        log.info("消息缓存已清除")

    def __del__(self):
        """清理资源"""
        if self.backend == 'wcferry' and self.client:
            try:
                self.client.cleanup()
            except:
                pass
