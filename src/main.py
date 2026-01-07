"""
AILive - 微信AI女友机器人
主程序入口
"""
import time
import signal
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import WeChatClient, AIEngine, MessageHandler
from src.utils import log, config


class AILive:
    """AI女友机器人主类"""

    def __init__(self):
        """初始化机器人"""
        self.running = False
        self.wechat = None
        self.ai_engine = None
        self.message_handler = None

        # 注册信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """信号处理器"""
        log.info("收到退出信号，正在关闭...")
        self.stop()
        sys.exit(0)

    def initialize(self):
        """初始化各个模块"""
        try:
            log.info("=" * 50)
            log.info("AILive - 微信AI女友机器人")
            log.info("=" * 50)

            # 初始化微信客户端
            log.info("正在初始化微信客户端...")
            self.wechat = WeChatClient()

            # 检查微信是否在线
            if not self.wechat.is_online():
                log.error("微信未登录或未运行，请先登录微信")
                return False

            # 初始化AI引擎
            log.info("正在初始化AI引擎...")
            self.ai_engine = AIEngine()

            # 初始化消息处理器
            log.info("正在初始化消息处理器...")
            self.message_handler = MessageHandler(self.wechat, self.ai_engine)

            log.info("所有模块初始化成功！")
            return True

        except Exception as e:
            log.error(f"初始化失败: {e}")
            return False

    def start(self):
        """启动机器人"""
        if not self.initialize():
            log.error("初始化失败，程序退出")
            return

        self.running = True
        log.info("机器人已启动，开始监听消息...")
        log.info("按 Ctrl+C 退出程序")

        # 主循环
        check_interval = 2  # 检查消息的间隔（秒）
        proactive_check_counter = 0  # 主动消息检查计数器
        proactive_check_interval = 300  # 每5分钟检查一次主动消息（300秒）

        while self.running:
            try:
                # 获取最新消息
                messages = self.wechat.get_latest_messages()

                # 处理每条消息
                for msg in messages:
                    sender = msg.get('sender', '')
                    content = msg.get('content', '')
                    real_sender = msg.get('real_sender')

                    # 过滤系统消息和自己发送的消息
                    if sender and content:
                        self.message_handler.handle_message(sender, content, real_sender)

                # 定期检查是否需要主动发送消息
                proactive_check_counter += check_interval
                if proactive_check_counter >= proactive_check_interval:
                    self.message_handler.check_and_send_proactive_messages()
                    proactive_check_counter = 0

                # 等待一段时间再检查
                time.sleep(check_interval)

            except KeyboardInterrupt:
                log.info("收到键盘中断信号")
                break

            except Exception as e:
                log.error(f"运行时错误: {e}")
                time.sleep(5)  # 出错后等待5秒再继续

        self.stop()

    def stop(self):
        """停止机器人"""
        self.running = False
        log.info("机器人已停止")

    def run_interactive(self):
        """交互式运行模式（用于测试）"""
        try:
            log.info("=" * 50)
            log.info("AILive - 微信AI女友机器人")
            log.info("=" * 50)

            # 交互模式不需要微信客户端，只初始化AI引擎
            log.info("正在初始化AI引擎...")
            self.ai_engine = AIEngine()

            # 创建一个简化的消息处理器（不需要微信客户端）
            log.info("正在初始化消息处理器...")
            from src.utils import ContextManager, config
            self.context_manager = ContextManager(
                max_messages=config.get('ai.max_context_messages', 20)
            )

            log.info("初始化成功！")
            log.info("=" * 50)
            log.info("交互式测试模式")
            log.info("输入消息测试AI回复，输入 'quit' 退出")
            log.info("=" * 50)

            test_user = "测试用户"

            while True:
                try:
                    user_input = input("\n你: ").strip()

                    if user_input.lower() in ['quit', 'exit', 'q']:
                        log.info("退出交互模式")
                        break

                    if not user_input:
                        continue

                    # 添加用户消息到上下文
                    self.context_manager.add_message(test_user, "user", user_input)

                    # 获取对话上下文
                    context = self.context_manager.get_context(test_user)

                    # 生成AI回复
                    reply = self.ai_engine.generate_response(
                        message=user_input,
                        context=context[:-1],  # 不包含刚添加的消息
                        user_id=test_user
                    )

                    # 添加AI回复到上下文
                    self.context_manager.add_message(test_user, "assistant", reply)

                    if reply:
                        print(f"\nAI女友: {reply}")
                    else:
                        print("\n[无回复]")

                except KeyboardInterrupt:
                    log.info("\n退出交互模式")
                    break

                except Exception as e:
                    log.error(f"错误: {e}")

        except Exception as e:
            log.error(f"初始化失败: {e}")
            return


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='AILive - 微信AI女友机器人')
    parser.add_argument(
        '--mode',
        choices=['normal', 'interactive'],
        default='normal',
        help='运行模式：normal(正常模式) 或 interactive(交互测试模式)'
    )

    args = parser.parse_args()

    # 创建机器人实例
    bot = AILive()

    # 根据模式运行
    if args.mode == 'interactive':
        bot.run_interactive()
    else:
        bot.start()


if __name__ == '__main__':
    main()
