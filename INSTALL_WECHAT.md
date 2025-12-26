# wxauto 安装指南

## 问题说明

`wxauto` 包在某些镜像源（如阿里云）中不可用，需要单独安装。

## 安装方法

### 方法1：从PyPI官方源安装（推荐）

```bash
pip install wxauto -i https://pypi.org/simple
```

### 方法2：从GitHub安装

```bash
pip install git+https://github.com/cluic/wxauto.git
```

### 方法3：使用国内镜像（清华源）

```bash
pip install wxauto -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方法4：临时切换到官方源

```bash
pip install wxauto --index-url https://pypi.python.org/simple/
```

## 验证安装

安装完成后，运行以下命令验证：

```bash
python -c "import wxauto; print('wxauto安装成功')"
```

## 如果不需要微信功能

如果你只想测试AI对话功能，可以暂时不安装wxauto：

1. **先安装其他依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **使用交互测试模式**（不需要微信）：
   ```bash
   python src/main.py --mode interactive
   ```

3. **等需要微信功能时再安装wxauto**

## 完整安装步骤

```bash
# 1. 安装基础依赖
pip install -r requirements.txt

# 2. 单独安装wxauto
pip install wxauto -i https://pypi.org/simple

# 3. 验证安装
python -c "import wxauto; print('所有依赖安装完成')"
```

## 常见问题

### Q: 为什么找不到wxauto？
A: 某些国内镜像源没有收录wxauto包，需要使用官方源或GitHub安装。

### Q: 可以不安装wxauto吗？
A: 可以！如果只用交互测试模式，不需要wxauto。只有连接微信时才需要。

### Q: wxauto支持哪些系统？
A: 仅支持Windows系统，需要安装微信客户端。

## 下一步

安装完成后：

1. **测试API连接**：
   ```bash
   python test_doubao_api.py
   ```

2. **交互测试模式**：
   ```bash
   python src/main.py --mode interactive
   ```

3. **连接微信**（需要wxauto）：
   ```bash
   python src/main.py
   ```

---

**提示**：建议先用交互模式测试AI功能，确认正常后再安装wxauto连接微信。
