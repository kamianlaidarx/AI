"""
修复wxauto的Python 3.8兼容性问题
"""
import sys
from pathlib import Path

# 找到wxauto安装路径
wxauto_path = None
for path in sys.path:
    component_file = Path(path) / 'wxauto' / 'ui' / 'component.py'
    if component_file.exists():
        wxauto_path = component_file
        break

if not wxauto_path:
    print("❌ 找不到wxauto安装路径")
    sys.exit(1)

print(f"找到wxauto文件: {wxauto_path}")

# 读取文件
with open(wxauto_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 修复类型注解
# 将 List[Path] 改为 'List[Path]'（字符串形式）
original = "def save_all(self, dir_path: Path) -> WxResponse[List[Path]]:"
fixed = "def save_all(self, dir_path: Path) -> 'WxResponse[List[Path]]':"

if original in content:
    content = content.replace(original, fixed)

    # 写回文件
    with open(wxauto_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("✅ 修复成功！")
    print("现在可以运行: python src/main.py --mode interactive")
else:
    print("⚠️ 未找到需要修复的代码，可能已经修复或版本不同")
    print("尝试直接运行程序看看")
