"""
测试 WeChatFerry 并诊断问题
"""
import os
import sys

print("=" * 60)
print("WeChatFerry 诊断工具")
print("=" * 60)

# 1. 检查是否安装
print("\n[1] 检查 WeChatFerry 安装...")
try:
    import wcferry
    print(f"✅ WeChatFerry 已安装，版本: {wcferry.__version__ if hasattr(wcferry, '__version__') else '未知'}")
except ImportError:
    print("❌ WeChatFerry 未安装")
    print("安装命令: pip install wcferry")
    sys.exit(1)

# 2. 检查微信安装路径
print("\n[2] 检查微信安装路径...")
import winreg

def find_wechat_path():
    """从注册表查找微信路径"""
    paths_to_check = [
        (winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent\WeChat"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Tencent\WeChat"),
    ]

    for hkey, subkey in paths_to_check:
        try:
            key = winreg.OpenKey(hkey, subkey)
            install_path, _ = winreg.QueryValueEx(key, "InstallPath")
            winreg.CloseKey(key)
            if install_path and os.path.exists(install_path):
                return install_path
        except:
            continue

    return None

wechat_path = find_wechat_path()
if wechat_path:
    print(f"✅ 找到微信安装路径: {wechat_path}")
    wechat_exe = os.path.join(wechat_path, "WeChat.exe")
    if os.path.exists(wechat_exe):
        print(f"✅ 微信程序存在: {wechat_exe}")
    else:
        print(f"⚠️ 微信程序不存在: {wechat_exe}")
else:
    print("❌ 未找到微信安装路径")
    print("\n可能的原因：")
    print("1. 微信未安装")
    print("2. 微信安装在非标准位置")
    print("3. 注册表信息缺失")

    # 尝试常见路径
    print("\n尝试查找常见安装路径...")
    common_paths = [
        r"C:\Program Files\Tencent\WeChat\WeChat.exe",
        r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Tencent\WeChat\WeChat.exe"),
    ]

    for path in common_paths:
        if os.path.exists(path):
            print(f"✅ 找到微信: {path}")
            wechat_path = os.path.dirname(path)
            break
    else:
        print("❌ 未在常见路径找到微信")

# 3. 检查微信是否运行
print("\n[3] 检查微信是否运行...")
import psutil

wechat_running = False
for proc in psutil.process_iter(['name']):
    try:
        if proc.info['name'] and 'WeChat.exe' in proc.info['name']:
            wechat_running = True
            print(f"✅ 微信正在运行 (PID: {proc.pid})")
            break
    except:
        pass

if not wechat_running:
    print("❌ 微信未运行")
    print("请先启动并登录微信客户端")

# 4. 尝试初始化 WeChatFerry
print("\n[4] 尝试初始化 WeChatFerry...")
if wechat_running:
    try:
        from wcferry import Wcf
        wcf = Wcf()

        if wcf.is_login():
            print("✅ WeChatFerry 初始化成功，微信已登录")

            # 获取一些信息
            try:
                self_wxid = wcf.get_self_wxid()
                print(f"✅ 当前登录账号 wxid: {self_wxid}")
            except:
                pass

            wcf.cleanup()
        else:
            print("⚠️ WeChatFerry 初始化成功，但微信未登录")

    except Exception as e:
        print(f"❌ WeChatFerry 初始化失败: {e}")
        print("\n可能的解决方案：")
        print("1. 确保微信已完全启动并登录")
        print("2. 尝试重启微信")
        print("3. 以管理员权限运行此脚本")
        print("4. 检查防火墙/杀毒软件是否拦截")
else:
    print("⏭️ 跳过初始化测试（微信未运行）")

# 5. 总结
print("\n" + "=" * 60)
print("诊断总结")
print("=" * 60)

if wechat_path and wechat_running:
    print("✅ 环境正常，可以使用 WeChatFerry")
    print("\n运行程序: python src/main.py")
else:
    print("❌ 环境存在问题，需要修复")
    if not wechat_path:
        print("- 未找到微信安装路径")
    if not wechat_running:
        print("- 微信未运行")

    print("\n建议：")
    print("1. 确保微信已安装并登录")
    print("2. 尝试重启微信")
    print("3. 或使用交互模式测试: python src/main.py --mode interactive")
