# 豆包API配置指南

## 1. 获取豆包API密钥和Endpoint ID

### 步骤：
1. 访问火山引擎控制台：https://console.volcengine.com/ark
2. 注册/登录账号
3. 进入"豆包大模型"服务
4. 创建推理接入点（Inference Endpoint）
5. 选择你想使用的模型（如 doubao-pro-32k）
6. 获取以下信息：
   - **API Key**（API密钥）
   - **Endpoint ID**（推理接入点ID，格式如 `ep-20250101-xxxxx`）

⚠️ **重要**：豆包API使用 Endpoint ID 而不是模型名称！

## 2. 可用模型

豆包提供多个模型，推荐使用：

| 模型名称 | 说明 | 上下文长度 | 适用场景 |
|---------|------|-----------|---------|
| `doubao-pro-32k` | 专业版 | 32K | 推荐使用，对话质量高 |
| `doubao-lite-32k` | 轻量版 | 32K | 成本较低，速度快 |
| `doubao-pro-128k` | 专业版 | 128K | 需要超长上下文时使用 |
| `doubao-vision-pro-32k` | 视觉理解版 | 32K | 支持图片理解 |

## 3. 配置步骤

### 3.1 复制环境变量模板
```bash
copy config\.env.example config\.env
```

### 3.2 编辑 config\.env 文件

```env
# 填入你的豆包API密钥
DOUBAO_API_KEY=你的API密钥

# API Base URL（一般不需要修改）
DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

### 3.3 编辑 config\config.yaml 文件

```yaml
ai:
  provider: "doubao"         # 使用豆包
  model: "ep-20250101-xxxxx" # 填入你的Endpoint ID
  max_tokens: 1000
  temperature: 0.8
```

⚠️ **关键**：`model` 字段必须填写你在火山引擎控制台创建的 **Endpoint ID**，而不是模型名称！

### 示例配置

假设你在火山引擎控制台：
- 创建了一个推理接入点
- 选择了 `doubao-pro-32k` 模型
- 获得的 Endpoint ID 是 `ep-20250126-abcde`
- 获得的 API Key 是 `546f43b8-c915-4587-b7e8-074ee9b1757d`

那么配置应该是：

**config/.env**:
```env
DOUBAO_API_KEY=546f43b8-c915-4587-b7e8-074ee9b1757d
DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

**config/config.yaml**:
```yaml
ai:
  provider: "doubao"
  model: "ep-20250126-abcde"  # 你的实际Endpoint ID
  max_tokens: 1000
  temperature: 0.8
```

## 4. 测试配置

### 4.1 安装依赖
```bash
pip install -r requirements.txt
```

### 4.2 交互测试模式
```bash
python src/main.py --mode interactive
```

如果配置正确，你应该能看到：
```
AI引擎初始化成功，使用提供商: doubao, 模型: doubao-pro-32k
```

然后可以输入消息测试AI回复。

## 5. 常见问题

### Q1: 提示"未设置DOUBAO_API_KEY环境变量"
**A**: 检查 `config\.env` 文件是否存在，且正确填写了API密钥。

### Q2: API调用失败
**A**: 检查以下几点：
- API密钥是否正确
- 账户余额是否充足
- endpoint ID是否正确
- 网络连接是否正常

### Q3: 如何切换回Claude或其他模型？
**A**: 修改 `config\config.yaml`：
```yaml
ai:
  provider: "claude"  # 或 "openai"
  model: "claude-3-5-sonnet-20241022"
```

然后在 `config\.env` 中配置对应的API密钥。

## 6. 费用说明

豆包API按token计费，具体价格请查看火山引擎官网。

建议：
- 设置每日调用上限
- 监控API使用量
- 使用lite版本降低成本

## 7. 获取帮助

- 火山引擎文档：https://www.volcengine.com/docs/82379
- 豆包大模型文档：https://www.volcengine.com/docs/82379/1099475

---

配置完成后，运行 `python src/main.py --mode interactive` 测试！
