# AILive - 微信群聊机器人

一个基于Python的微信群聊AI机器人，支持多种AI模型（豆包/Claude/OpenAI）。

## 核心特性

- **智能对话** - 支持豆包、Claude、OpenAI等多种AI模型
- **群聊@回复** - 只有@机器人才会回复，不会打扰群聊
- **Web管理面板** - 可视化配置界面，支持在线获取模型列表
- **上下文记忆** - 持久化对话历史，重启后保持记忆
- **黑白名单** - 支持群聊过滤

## 环境要求

- **操作系统**：Windows（微信自动化仅支持Windows）
- **Python版本**：3.8+
- **微信版本**：3.9.10（推荐）

## 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装wxauto
pip install git+https://github.com/cluic/wxauto.git
```

### 2. 配置机器人

启动Web管理面板：

```bash
python src\web\app.py
```

访问 http://127.0.0.1:5000 进行配置：

1. **AI配置页面**：
   - 选择AI提供商（豆包/Claude/OpenAI）
   - 填写API Key和Base URL
   - 点击"获取模型"加载可用模型列表
   - 从下拉框选择模型
   - 点击"保存配置"

2. **微信配置页面**（可选）：
   - 配置黑白名单
   - 设置回复延迟

### 3. 安装微信3.9.10

下载地址：https://dldir1.qq.com/weixin/Windows/WeChatSetup_3.9.10.19.exe

### 4. 启动机器人

```bash
# 方式一：使用启动脚本
start_bot.bat

# 方式二：命令行启动
python src\main.py
```

## 使用说明

### 群聊使用

- **@机器人** 才会回复
- 未@的消息会被忽略
- 支持多群同时使用

### 命令

在群里@机器人后发送：
- `/modellist` - 查看可用模型列表
- `/model <模型名>` - 切换模型（仅管理员）

### 结束会话

@机器人 + "结束本次会话" 可清空当前群的对话上下文。

## 项目结构

```
AILive/
├── src/
│   ├── core/
│   │   ├── wechat_client.py   # 微信客户端
│   │   ├── ai_engine.py       # AI引擎
│   │   └── message_handler.py # 消息处理
│   ├── utils/
│   │   ├── config.py          # 配置管理
│   │   ├── logger.py          # 日志系统
│   │   └── context_manager.py # 上下文管理
│   ├── web/                   # Web管理面板
│   └── main.py                # 主程序
├── config/
│   ├── config.yaml            # 主配置
│   └── .env                   # API密钥
├── data/conversations/        # 对话历史
├── logs/                      # 日志
├── start_bot.bat              # 启动脚本
└── requirements.txt           # 依赖
```

## 配置说明

### config/config.yaml

```yaml
wechat:
  auto_reply: true
  reply_delay: [1, 3]
  max_message_length: 500

ai:
  provider: "openai"           # doubao/claude/openai
  model: "gpt-4o-mini"
  max_tokens: 1000
  temperature: 0.8

filters:
  whitelist: []                # 白名单群（空则接受所有）
  blacklist: []                # 黑名单群

group_chat:
  enabled: true
  end_session_keyword: "结束本次会话"
```

### config/.env

```env
# OpenAI兼容API
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=https://api.openai.com/v1

# 豆包API
DOUBAO_API_KEY=your_api_key
DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3

# Claude API
CLAUDE_API_KEY=your_api_key
```

## 常见问题

### Q: 机器人不回复消息？
A: 确保消息中@了机器人，未@的消息会被忽略。

### Q: 提示"未获取到微信昵称"？
A: 确保微信已登录且使用3.9.10版本。

### Q: 如何切换模型？
A: 在Web管理面板中点击"获取模型"，从下拉框选择后保存。

## 注意事项

1. **微信版本**：推荐使用3.9.10版本
2. **封号风险**：建议使用小号测试
3. **API费用**：按使用量计费，注意控制
4. **隐私安全**：不要将 `.env` 文件提交到Git

## 许可证

MIT License

---

**免责声明**：本项目仅供学习和研究使用，使用者需自行承担风险。
