# WeChatFerry 安装和使用指南

## 支持微信4.0+版本

WeChatFerry 是一个支持微信4.0及以上版本的Python库。

## 安装步骤

### 1. 安装 WeChatFerry

```bash
pip install wcferry
```

### 2. 确保微信已登录

- 打开微信客户端
- 登录你的账号
- 保持微信运行

### 3. 运行程序

```bash
# 交互测试模式
python src/main.py --mode interactive

# 微信自动回复模式
python src/main.py
```

## 特性

### WeChatFerry vs wxauto

| 特性 | WeChatFerry | wxauto |
|------|-------------|--------|
| 支持微信版本 | 4.0+ | 仅3.9 |
| 稳定性 | ✅ 高 | ⚠️ 中等 |
| 功能完整性 | ✅ 完整 | ✅ 完整 |
| 安装难度 | ✅ 简单 | ⚠️ 需要代理 |

## 自动检测

程序会自动检测可用的微信库：

1. **优先使用 WeChatFerry**（如果已安装）
2. **其次使用 wxauto**（如果已安装）
3. **如果都没有**，提示安装

## 使用说明

### 基本使用

```bash
# 安装
pip install wcferry

# 运行
python src/main.py
```

### 配置黑白名单

编辑 `config/config.yaml`：

```yaml
filters:
  whitelist: []              # 只回复这些人
  blacklist: ["群聊", "广告"] # 不回复这些人
```

### 调整回复延迟

```yaml
wechat:
  reply_delay: [1, 3]  # 1-3秒随机延迟
```

## 常见问题

### Q: 提示"微信未登录"？
A: 确保微信客户端已打开并登录。

### Q: 无法接收消息？
A: WeChatFerry 需要微信保持运行状态。

### Q: 如何切换回wxauto？
A: 卸载 WeChatFerry：`pip uninstall wcferry`，程序会自动使用 wxauto。

### Q: 两个库可以同时安装吗？
A: 可以，程序会优先使用 WeChatFerry。

## 测试

### 测试连接

```bash
python -c "from wcferry import Wcf; wcf = Wcf(); print('✅ WeChatFerry可用' if wcf.is_login() else '❌ 微信未登录')"
```

### 测试程序

```bash
# 交互模式（不连接微信）
python src/main.py --mode interactive

# 微信模式
python src/main.py
```

## 注意事项

1. **封号风险**
   - 建议使用小号测试
   - 不要频繁发送消息
   - 已设置随机延迟

2. **性能**
   - WeChatFerry 性能优于 wxauto
   - 支持更多消息类型

3. **兼容性**
   - 支持微信4.0+所有版本
   - 包括你的4.1.6.14版本

---

**现在运行 `pip install wcferry` 开始使用！** 🚀
