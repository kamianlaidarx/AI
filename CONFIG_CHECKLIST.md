# 豆包API配置检查清单

在运行程序之前，请确认以下配置都已完成：

## ✅ 配置检查清单

### 1. 环境变量配置 (config/.env)

- [ ] 文件已创建（从 .env.example 复制）
- [ ] `DOUBAO_API_KEY` 已填写你的实际API密钥
- [ ] `DOUBAO_API_BASE` 保持默认值 `https://ark.cn-beijing.volces.com/api/v3`

**示例**：
```env
DOUBAO_API_KEY=546f43b8-c915-4587-b7e8-074ee9b1757d
DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

### 2. 主配置文件 (config/config.yaml)

- [ ] `ai.provider` 设置为 `"doubao"`
- [ ] `ai.model` 填写你的 **Endpoint ID**（格式：`ep-xxxxxxxx-xxxx`）
- [ ] 其他参数根据需要调整

**示例**：
```yaml
ai:
  provider: "doubao"
  model: "ep-20250126-xxxxx"  # 你的实际Endpoint ID
  max_tokens: 1000
  temperature: 0.8
```

### 3. 依赖安装

- [ ] 已创建虚拟环境
- [ ] 已激活虚拟环境
- [ ] 已安装所有依赖包

**命令**：
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 4. 获取Endpoint ID

⚠️ **最重要的一步**：

1. 登录火山引擎控制台：https://console.volcengine.com/ark
2. 进入"豆包大模型" → "推理"
3. 点击"创建推理接入点"
4. 选择模型（如 doubao-pro-32k）
5. 创建后，复制 **Endpoint ID**（格式：`ep-xxxxxxxx-xxxx`）
6. 将这个 Endpoint ID 填入 `config/config.yaml` 的 `ai.model` 字段

## 🧪 测试配置

配置完成后，运行测试：

```bash
python src/main.py --mode interactive
```

### 预期输出

如果配置正确，你应该看到：

```
==================================================
AILive - 微信AI女友机器人
==================================================
正在初始化微信客户端...
正在初始化AI引擎...
豆包API初始化成功
AI引擎初始化成功，使用提供商: doubao, 模型: ep-20250126-xxxxx
正在初始化消息处理器...
消息处理器初始化成功！
==================================================
交互式测试模式
输入消息测试AI回复，输入 'quit' 退出
==================================================

你:
```

### 常见错误

#### 错误1：未设置DOUBAO_API_KEY环境变量
```
ValueError: 未设置DOUBAO_API_KEY环境变量
```
**解决**：检查 `config/.env` 文件是否存在且正确填写了API密钥

#### 错误2：API调用失败
```
AI生成回复失败: ...
```
**可能原因**：
- Endpoint ID 填写错误
- API密钥无效
- 账户余额不足
- 网络连接问题

**解决**：
1. 确认 Endpoint ID 格式正确（`ep-xxxxxxxx-xxxx`）
2. 在火山引擎控制台检查API密钥是否有效
3. 检查账户余额
4. 测试网络连接

#### 错误3：模型不存在
```
Model not found
```
**解决**：确认你填写的是 **Endpoint ID** 而不是模型名称

## 📝 配置示例

### 完整的配置示例

**config/.env**:
```env
DOUBAO_API_KEY=546f43b8-c915-4587-b7e8-074ee9b1757d
DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3
DEBUG=false
LOG_LEVEL=INFO
```

**config/config.yaml**:
```yaml
# 微信配置
wechat:
  auto_reply: true
  reply_delay: [1, 3]
  max_message_length: 500

# AI配置
ai:
  provider: "doubao"
  model: "ep-20250126-abcde"  # 你的实际Endpoint ID
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
```

## 🎯 下一步

配置完成并测试通过后：

1. **交互测试模式**：
   ```bash
   python src/main.py --mode interactive
   ```
   在命令行中测试AI对话

2. **正常模式**（需要微信登录）：
   ```bash
   python src/main.py
   ```
   连接微信，自动回复消息

3. **自定义人格**：
   编辑 `config/persona.yaml` 调整AI女友的性格和说话风格

## 📚 相关文档

- [README.md](README.md) - 完整使用说明
- [DOUBAO_SETUP.md](DOUBAO_SETUP.md) - 豆包API详细配置指南
- [PROJECT_PLAN.md](PROJECT_PLAN.md) - 项目技术方案

---

**祝你配置顺利！有问题随时查看文档或提issue。** 🚀
