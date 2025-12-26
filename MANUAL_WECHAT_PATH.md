# 手动配置微信路径

## 问题

如果 WeChatFerry 无法自动找到微信安装路径，可以手动指定。

## 解决方案

### 步骤1：找到你的微信安装路径

常见路径：
- `C:\Program Files\Tencent\WeChat`
- `C:\Program Files (x86)\Tencent\WeChat`
- `C:\Users\你的用户名\AppData\Local\Programs\Tencent\WeChat`

或者：
1. 右键点击桌面上的微信图标
2. 选择"打开文件所在位置"
3. 复制路径

### 步骤2：编辑配置文件

打开 `config/config.yaml`，添加微信路径：

```yaml
# 微信配置
wechat:
  path: "C:\\Program Files\\Tencent\\WeChat"  # 你的微信安装路径
  auto_reply: true
  reply_delay: [1, 3]
  max_message_length: 500
```

**注意**：
- 路径中的反斜杠 `\` 要写成双反斜杠 `\\`
- 或者使用正斜杠 `/`：`C:/Program Files/Tencent/WeChat`

### 步骤3：运行程序

```bash
python src/main.py
```

## 示例配置

### 示例1：标准安装路径
```yaml
wechat:
  path: "C:\\Program Files\\Tencent\\WeChat"
```

### 示例2：用户目录安装
```yaml
wechat:
  path: "C:\\Users\\lenovo\\AppData\\Local\\Programs\\Tencent\\WeChat"
```

### 示例3：使用正斜杠
```yaml
wechat:
  path: "C:/Program Files/Tencent/WeChat"
```

## 验证

配置后，程序启动时会显示：

```
使用配置的微信路径: C:\Program Files\Tencent\WeChat
微信客户端初始化成功（使用 wcferry）
```

## 如果还是失败

### 方案1：检查路径是否正确

确保路径中包含 `WeChat.exe` 文件。

### 方案2：使用诊断脚本

```bash
python diagnose_wcferry.py
```

这个脚本会自动查找微信路径。

### 方案3：使用交互模式

如果微信功能无法使用，可以先用交互模式测试AI功能：

```bash
python src/main.py --mode interactive
```

或：

```bash
python simple_test.py
```

---

## 完整配置示例

`config/config.yaml`：

```yaml
# 微信配置
wechat:
  path: "C:\\Program Files\\Tencent\\WeChat"  # 手动指定微信路径
  auto_reply: true
  reply_delay: [1, 3]
  max_message_length: 500

# AI配置
ai:
  provider: "doubao"
  model: "ep-20251226192412-8kff2"
  max_tokens: 1000
  temperature: 0.8
  max_context_messages: 20

# 人格配置
personality:
  config_file: "config/persona.yaml"

# 过滤器配置
filters:
  whitelist: []
  blacklist: []
  keywords_filter: []

# 日志配置
logging:
  level: "INFO"
  file: "logs/ailive.log"
  rotation: "100 MB"
  retention: "30 days"

# 数据存储
storage:
  conversations_dir: "data/conversations"
  cache_dir: "data/cache"
```

---

**找到你的微信路径后，编辑 `config/config.yaml` 添加 `path` 配置即可！** 🚀
