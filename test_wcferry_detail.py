"""
详细测试 WeChatFerry 初始化
"""
import os
import sys

print("=" * 60)
print("WeChatFerry 详细测试")
print("=" * 60)

# 设置环境变量
wechat_path = r"C:\Program Files\Tencent\Weixin"
os.environ['WECHAT_DIR'] = wechat_path
os.environ['WECHAT_PATH'] = wechat_path

print(f"\n[1] 设置环境变量")
print(f"WECHAT_DIR: {os.environ.get('WECHAT_DIR')}")
print(f"WECHAT_PATH: {os.environ.get('WECHAT_PATH')}")

# 检查微信是否运行
print(f"\n[2] 检查微信进程")
import psutil
wechat_running = False
for proc in psutil.process_iter(['name', 'pid']):
    try:
        if proc.info['name'] and 'Weixin.exe' in proc.info['name']:
            wechat_running = True
            print(f"✅ 微信正在运行 (PID: {proc.info['pid']})")
            break
    except:
        pass

if not wechat_running:
    print("❌ 微信未运行，请先启动微信")
    input("\n按回车键退出...")
    sys.exit(1)

# 尝试导入 WeChatFerry
print(f"\n[3] 导入 WeChatFerry")
try:
    from wcferry import Wcf
    print("✅ WeChatFerry 导入成功")
except ImportError as e:
    print(f"❌ WeChatFerry 导入失败: {e}")
    input("\n按回车键退出...")
    sys.exit(1)

# 尝试初始化
print(f"\n[4] 初始化 WeChatFerry")
try:
    print("正在初始化...")
    wcf = Wcf()
    print("✅ WeChatFerry 初始化成功")

    # 检查登录状态
    print(f"\n[5] 检查登录状态")
    try:
        is_login = wcf.is_login()
        if is_login:
            print("✅ 微信已登录")

            # 获取自己的 wxid
            try:
                self_wxid = wcf.get_self_wxid()
                print(f"✅ 当前账号 wxid: {self_wxid}")
            except Exception as e:
                print(f"⚠️ 无法获取 wxid: {e}")

        else:
            print("❌ 微信未登录")

    except Exception as e:
        print(f"❌ 检查登录状态失败: {e}")

    # 清理
    print(f"\n[6] 清理资源")
    try:
        wcf.cleanup()
        print("✅ 清理成功")
    except Exception as e:
        print(f"⚠️ 清理失败: {e}")

    print("\n" + "=" * 60)
    print("✅ 测试完成！WeChatFerry 可以正常使用")
    print("=" * 60)
    print("\n现在可以运行: python src/main.py")

except Exception as e:
    print(f"❌ 初始化失败: {e}")
    print(f"\n错误类型: {type(e).__name__}")
    print(f"错误详情: {str(e)}")

    import traceback
    print("\n完整错误堆栈:")
    traceback.print_exc()

    print("\n" + "=" * 60)
    print("可能的原因:")
    print("1. 微信版本不兼容（需要微信4.0+）")
    print("2. WeChatFerry 版本问题")
    print("3. 微信未完全启动")
    print("4. 权限问题")
    print("\n建议:")
    print("1. 确保微信已完全启动并登录")
    print("2. 尝试重启微信")
    print("3. 更新 WeChatFerry: pip install --upgrade wcferry")
    print("4. 或使用交互模式: python src/main.py --mode interactive")
    print("=" * 60)

input("\n按回车键退出...")
