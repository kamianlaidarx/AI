# AILive - 微信AI女友机器人

一个基于Python的微信AI女友机器人，使用Claude API实现智能对话。

## ✨ 特性

- 🤖 基于Claude API的高质量对话
- 💬 支持微信消息自动回复
- 🎭 可自定义AI女友人格和说话风格
- 💾 对话上下文管理和历史记录
- 🛡️ 黑白名单过滤
- 📝 完善的日志系统
- ⚙️ 灵活的配置管理

## 📋 环境要求

- Python 3.8+
- Windows系统（wxauto仅支持Windows）
- 已安装微信客户端
- Claude API密钥

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <repository_url>
cd AILive
```

### 2. 创建虚拟环境

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
copy config\.env.example config\.env

# 编辑 config\.env 文件，填入你的API密钥
# CLAUDE_API_KEY=your_api_key_here
```

### 5. 配置人格（可选）

编辑 `config/persona.yaml` 文件，自定义AI女友的性格和说话风格。

### 6. 运行程序

```bash
# 正常模式（连接微信）
python src/main.py

# 交互测试模式（不需要微信）
python src/main.py --mode interactive
```

## 📁 项目结构

```
AILive/
├── src/
│   ├── core/                  # 核心模块
│   │   ├── wechat_client.py   # 微信客户端
│   │   ├── ai_engine.py       # AI对话引擎
│   │   └── message_handler.py # 消息处理器
│   ├── personality/           # 人格系统
│   │   ├── persona.py         # 人格管理
│   │   └── prompts.py         # 提示词模板
│   ├── utils/                 # 工具模块
│   │   ├── config.py          # 配置管理
│   │   ├── logger.py          # 日志系统
│   │   └── context_manager.py # 上下文管理
│   └── main.py                # 主程序入口
├── config/                    # 配置文件
│   ├── config.yaml            # 主配置
│   ├── persona.yaml           # 人格配置
│   └── .env.example           # 环境变量模板
├── data/                      # 数据目录
├── logs/                      # 日志目录
├── requirements.txt           # 依赖列表
├── PROJECT_PLAN.md            # 项目规划文档
└── README.md                  # 本文件
```

## ⚙️ 配置说明

### 主配置文件 (config/config.yaml)

```yaml
wechat:
  auto_reply: true           # 是否自动回复
  reply_delay: [1, 3]        # 回复延迟范围（秒）

ai:
  provider: "claude"         # AI提供商
  model: "claude-3-5-sonnet-20241022"
  temperature: 0.8           # 温度参数

filters:
  whitelist: []              # 白名单（为空则接受所有）
  blacklist: []              # 黑名单
```

### 人格配置文件 (config/persona.yaml)

```yaml
name: "小雨"
age: 22
personality:
  traits:
    - 温柔体贴
    - 善解人意
speaking_style:
  tone: "温柔亲切"
  particles:
    - "呀"
    - "哦"
```

## 📖 使用说明

### 正常模式

1. 确保微信客户端已登录
2. 运行 `python src/main.py`
3. 程序会自动监听微信消息并回复

### 交互测试模式

1. 运行 `python src/main.py --mode interactive`
2. 在命令行中输入消息测试AI回复
3. 输入 `quit` 退出

### 黑白名单设置

编辑 `config/config.yaml`：

```yaml
filters:
  whitelist: ["张三", "李四"]  # 只回复这些人
  blacklist: ["王五"]          # 不回复这些人
```

## ⚠️ 注意事项

1. **封号风险**：虽然使用官方客户端，但仍有一定风险，建议使用小号测试
2. **API费用**：Claude API按使用量计费，建议设置每日上限
3. **隐私安全**：不要记录敏感信息，对话历史仅保存在本地
4. **合规性**：仅用于个人学习和研究，不要用于商业用途

## 🐛 常见问题

### Q: 提示"微信未登录或未运行"？
A: 请确保微信客户端已打开并登录。

### Q: 提示"未设置CLAUDE_API_KEY"？
A: 请检查 `config/.env` 文件是否正确配置了API密钥。

### Q: AI回复质量不好？
A: 可以调整 `config/persona.yaml` 中的人格设置，或修改 `ai.temperature` 参数。

### Q: 如何查看日志？
A: 日志文件保存在 `logs/ailive.log`。

## 🔧 开发计划

- [ ] 支持群聊消息
- [ ] 添加图片识别能力
- [ ] 添加语音消息处理
- [ ] Web管理界面
- [ ] 支持更多AI模型

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📮 联系方式

如有问题，请提交Issue。

---

**⚠️ 免责声明**：本项目仅供学习和研究使用，使用者需自行承担使用本项目可能带来的风险。
