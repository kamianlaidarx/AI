"""
调试 wxauto 消息获取
"""
from wxauto import WeChat
import time

print("=" * 60)
print("wxauto 消息获取调试")
print("=" * 60)

# 初始化微信
wx = WeChat()
print(f"\n✅ 微信初始化成功")

print("\n请用另一个微信给当前微信发送消息...")
print("然后打开那个聊天窗口（必须打开聊天窗口！）")
print("\n等待10秒后开始获取消息...\n")

time.sleep(10)

# 获取消息
print("正在获取消息...")
messages = wx.GetAllMessage()

print(f"\n获取到 {len(messages)} 条消息\n")

# 显示所有消息
for i, msg in enumerate(messages, 1):
    print(f"消息 {i}:")
    print(f"  类型: {type(msg)}")
    if isinstance(msg, dict):
        print(f"  发送者: {msg.get('sender', 'N/A')}")
        print(f"  内容: {msg.get('content', 'N/A')}")
        print(f"  时间: {msg.get('time', 'N/A')}")
    else:
        print(f"  对象: {msg}")
    print()

print("=" * 60)
print("调试完成")
print("=" * 60)
print("\n重要提示：")
print("1. wxauto 只能读取当前打开的聊天窗口的消息")
print("2. 必须先打开聊天窗口，然后程序才能读取消息")
print("3. 如果没有打开聊天窗口，将无法获取消息")

input("\n按回车键退出...")
