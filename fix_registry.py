"""
修复微信注册表信息
需要管理员权限运行
"""
import winreg
import os
import sys

def fix_wechat_registry():
    """修复微信注册表"""
    wechat_path = r"C:\Program Files\Tencent\Weixin"

    print("=" * 60)
    print("微信注册表修复工具")
    print("=" * 60)
    print(f"\n将要写入的路径: {wechat_path}")

    # 检查路径是否存在
    if not os.path.exists(wechat_path):
        print(f"\n❌ 错误：路径不存在: {wechat_path}")
        print("请确认微信安装路径是否正确")
        return False

    # 检查 WeChat.exe 或 Weixin.exe
    exe_files = ["WeChat.exe", "Weixin.exe"]
    exe_found = None
    for exe in exe_files:
        exe_path = os.path.join(wechat_path, exe)
        if os.path.exists(exe_path):
            exe_found = exe
            print(f"✅ 找到微信程序: {exe}")
            break

    if not exe_found:
        print(f"\n❌ 错误：在 {wechat_path} 中未找到微信程序")
        return False

    # 尝试写入注册表
    registry_keys = [
        (winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Tencent\WeChat"),
    ]

    success_count = 0

    for hkey, subkey in registry_keys:
        try:
            # 尝试创建或打开键
            key = winreg.CreateKey(hkey, subkey)

            # 写入 InstallPath
            winreg.SetValueEx(key, "InstallPath", 0, winreg.REG_SZ, wechat_path)

            # 关闭键
            winreg.CloseKey(key)

            hkey_name = "HKEY_CURRENT_USER" if hkey == winreg.HKEY_CURRENT_USER else "HKEY_LOCAL_MACHINE"
            print(f"✅ 成功写入: {hkey_name}\\{subkey}")
            success_count += 1

        except PermissionError:
            hkey_name = "HKEY_CURRENT_USER" if hkey == winreg.HKEY_CURRENT_USER else "HKEY_LOCAL_MACHINE"
            print(f"⚠️ 权限不足，无法写入: {hkey_name}\\{subkey}")
            print("   请以管理员权限运行此脚本")
        except Exception as e:
            print(f"❌ 写入失败: {e}")

    if success_count > 0:
        print(f"\n✅ 成功写入 {success_count} 个注册表项")
        print("\n现在可以运行: python src/main.py")
        return True
    else:
        print("\n❌ 所有注册表写入都失败了")
        print("\n解决方案：")
        print("1. 右键点击此脚本，选择'以管理员身份运行'")
        print("2. 或者使用管理员权限的命令行运行:")
        print("   python fix_registry.py")
        return False

if __name__ == "__main__":
    print("\n⚠️ 注意：此脚本需要管理员权限才能修改注册表")
    print("如果失败，请右键选择'以管理员身份运行'\n")

    input("按回车键继续...")

    result = fix_wechat_registry()

    print("\n" + "=" * 60)
    if result:
        print("修复完成！")
    else:
        print("修复失败，请查看上面的错误信息")
    print("=" * 60)

    input("\n按回车键退出...")
