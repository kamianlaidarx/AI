# 快速开始指南

## 📋 当前配置状态

✅ **API密钥已配置**：
- DOUBAO_API_KEY: `546f43b8-c915-4587-b7e8-074ee9b1757d`
- DOUBAO_API_BASE: `https://ark.cn-beijing.volces.com/api/v3`

✅ **配置文件已就绪**：
- `config/.env` - 环境变量配置
- `config/config.yaml` - 主配置文件
- `config/persona.yaml` - AI女友人格配置

## 🚀 安装和运行步骤

### 步骤1：安装依赖

在项目根目录下运行：

```bash
# 方法1：使用requirements.txt（推荐）
pip install -r requirements.txt

# 方法2：手动安装核心依赖
pip install pyyaml python-dotenv loguru openai wxauto
```

### 步骤2：配置对话模型Endpoint

⚠️ **重要**：你提供的 `ep-20251226191856-ns4lj` 是图生视频模型，不能用于对话。

你需要：
1. 访问：https://console.volcengine.com/ark
2. 进入"推理" → "创建推理接入点"
3. 选择**对话模型**（如 `doubao-pro-32k`）
4. 获取对话模型的 Endpoint ID
5. 更新 `config/config.yaml` 中的 `model` 字段

**临时方案**：当前配置使用 `doubao-pro-32k` 模型名称，某些情况下也可能工作。

### 步骤3：测试运行

```bash
# 交互测试模式（不需要微信）
python src/main.py --mode interactive
```

**预期输出**：
```
==================================================
AILive - 微信AI女友机器人
==================================================
正在初始化微信客户端...
正在初始化AI引擎...
豆包API初始化成功
AI引擎初始化成功，使用提供商: doubao, 模型: doubao-pro-32k
正在初始化消息处理器...
消息处理器初始化成功！
==================================================
交互式测试模式
输入消息测试AI回复，输入 'quit' 退出
==================================================

你: 你好
AI女友: 你好呀~ 有什么想聊的吗？
```

### 步骤4：连接微信（可选）

如果测试通过，可以连接微信：

```bash
# 确保微信客户端已登录
python src/main.py
```

## 🔧 常见问题

### Q1: 提示"未设置DOUBAO_API_KEY环境变量"
**解决**：检查 `config/.env` 文件是否存在

### Q2: 提示"pip: command not found"
**解决**：
```bash
# 使用python -m pip
python -m pip install -r requirements.txt
```

### Q3: API调用失败
**可能原因**：
- 使用了错误的endpoint（图生视频而非对话模型）
- API密钥无效
- 账户余额不足

**解决**：
1. 确认使用的是**对话模型**的endpoint
2. 在火山引擎控制台检查API密钥和余额

### Q4: 模块导入错误
**解决**：
```bash
# 确保在项目根目录运行
cd F:\项目\AILive
python src/main.py --mode interactive
```

## 📝 配置文件说明

### config/.env
```env
DOUBAO_API_KEY=546f43b8-c915-4587-b7e8-074ee9b1757d
DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

### config/config.yaml
```yaml
ai:
  provider: "doubao"
  model: "doubao-pro-32k"  # 或你的对话模型Endpoint ID
  max_tokens: 1000
  temperature: 0.8
```

### config/persona.yaml
AI女友的性格配置，可以自定义：
- 名字、年龄
- 性格特征
- 说话风格
- 兴趣爱好

## 🎯 下一步

1. **安装依赖**：`pip install -r requirements.txt`
2. **测试运行**：`python src/main.py --mode interactive`
3. **获取对话模型endpoint**（如果当前配置不工作）
4. **自定义人格**：编辑 `config/persona.yaml`
5. **连接微信**：`python src/main.py`

## 📚 相关文档

- [README.md](README.md) - 完整使用说明
- [DOUBAO_SETUP.md](DOUBAO_SETUP.md) - 豆包API详细配置
- [CONFIG_CHECKLIST.md](CONFIG_CHECKLIST.md) - 配置检查清单
- [PROJECT_PLAN.md](PROJECT_PLAN.md) - 项目技术方案

---

**准备好了吗？运行 `pip install -r requirements.txt` 开始吧！** 🚀
