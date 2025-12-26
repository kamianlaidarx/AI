# 豆包API配置指南

## 1. 获取豆包API密钥

### 步骤：
1. 访问火山引擎控制台：https://console.volcengine.com/ark
2. 注册/登录账号
3. 进入"豆包大模型"服务
4. 创建API密钥
5. 选择模型并获取endpoint ID

## 2. 可用模型

豆包提供多个模型，推荐使用：

| 模型名称 | 说明 | 适用场景 |
|---------|------|---------|
| `doubao-pro-32k` | 专业版，32K上下文 | 推荐使用，对话质量高 |
| `doubao-lite-32k` | 轻量版，32K上下文 | 成本较低，速度快 |
| `doubao-pro-128k` | 专业版，128K上下文 | 需要超长上下文时使用 |

## 3. 配置步骤

### 3.1 复制环境变量模板
```bash
copy config\.env.example config\.env
```

### 3.2 编辑 config\.env 文件

```env
# 填入你的豆包API密钥
DOUBAO_API_KEY=your_actual_api_key_here

# API Base URL（一般不需要修改）
DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

### 3.3 确认 config\config.yaml 配置

```yaml
ai:
  provider: "doubao"         # 使用豆包
  model: "doubao-pro-32k"    # 模型名称（使用你的endpoint ID）
  max_tokens: 1000
  temperature: 0.8
```

**重要**：`model` 字段应该填写你在火山引擎控制台获取的 **endpoint ID**，而不是模型名称。

例如：
```yaml
model: "ep-20231201-xxxxx"  # 你的实际endpoint ID
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
