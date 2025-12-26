"""
检查 WeChatFerry 和微信版本兼容性
"""
import sys

print("=" * 60)
print("版本兼容性检查")
print("=" * 60)

# 1. 检查 WeChatFerry 版本
print("\n[1] WeChatFerry 版本")
try:
    import wcferry
    version = getattr(wcferry, '__version__', '未知')
    print(f"✅ WeChatFerry 版本: {version}")
except ImportError:
    print("❌ WeChatFerry 未安装")
    sys.exit(1)

# 2. 检查微信版本
print("\n[2] 微信版本")
import os
import winreg

def get_wechat_version():
    """从注册表获取微信版本"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat")
        version, _ = winreg.QueryValueEx(key, "Version")
        winreg.CloseKey(key)
        return version
    except:
        pass

    # 尝试从文件获取
    wechat_exe = r"C:\Program Files\Tencent\Weixin\Weixin.exe"
    if os.path.exists(wechat_exe):
        try:
            import win32api
            info = win32api.GetFileVersionInfo(wechat_exe, "\\")
            version = "%d.%d.%d.%d" % (
                info['FileVersionMS'] >> 16,
                info['FileVersionMS'] & 0xFFFF,
                info['FileVersionLS'] >> 16,
                info['FileVersionLS'] & 0xFFFF
            )
            return version
        except:
            pass

    return "未知"

wechat_version = get_wechat_version()
print(f"微信版本: {wechat_version}")

# 3. 兼容性检查
print("\n[3] 兼容性分析")
print(f"你的微信版本: {wechat_version}")
print(f"WeChatFerry 版本: {version}")

if wechat_version.startswith("4."):
    print("✅ 微信版本 4.x，理论上支持 WeChatFerry")
elif wechat_version.startswith("3.9"):
    print("⚠️ 微信版本 3.9.x，建议使用 wxauto")
else:
    print(f"⚠️ 微信版本 {wechat_version}，兼容性未知")

# 4. 建议
print("\n" + "=" * 60)
print("建议方案")
print("=" * 60)

print("\n由于 WeChatFerry 初始化失败，建议：")
print("\n方案1：使用交互模式（不需要微信）")
print("  python src/main.py --mode interactive")
print("  或")
print("  python simple_test.py")

print("\n方案2：尝试更新 WeChatFerry")
print("  pip install --upgrade wcferry")

print("\n方案3：降级微信到 3.9.10")
print("  下载：https://dldir1.qq.com/weixin/Windows/WeChatSetup_3.9.10.19.exe")
print("  然后使用 wxauto")

print("\n方案4：等待 WeChatFerry 更新")
print("  关注：https://github.com/lich0821/WeChatFerry")

print("\n" + "=" * 60)
print("推荐：先使用方案1（交互模式）测试AI功能")
print("=" * 60)

input("\n按回车键退出...")
