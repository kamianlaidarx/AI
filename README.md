# AILive - 微信AI女友机器人

一个基于Python的微信AI女友机器人，使用豆包（Doubao）API实现智能对话。

## ✨ 特性

- 🤖 基于豆包（Doubao）API的高质量对话
- 💬 支持微信消息自动回复
- 🎭 可自定义AI女友人格和说话风格
- 💾 **持久化上下文记忆** - 自动保存和加载对话历史，从上次对话继续
- 💌 **主动对话功能** - AI会在你长时间没发消息时主动找你聊天
- 🛡️ 黑白名单过滤
- 📝 完善的日志系统
- ⚙️ 灵活的配置管理
- 🔄 支持多种微信版本（wxauto for 3.9 / WeChatFerry for 4.0+）
- 🌐 **Web管理面板** - 可视化配置管理界面

## 📋 环境要求

- Python 3.8+
- Windows系统（微信自动化仅支持Windows）
- 已安装微信客户端（推荐版本 3.9.10）
- 豆包（Doubao）API密钥

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
# 升级 pip
python -m pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 安装 wxauto（从GitHub）
pip install git+https://github.com/cluic/wxauto.git
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
copy config\.env.example config\.env

# 编辑 config\.env 文件，填入你的豆包API密钥
# DOUBAO_API_KEY=your_api_key_here
# DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3
```

### 5. 配置主配置文件

编辑 `config/config.yaml`：

```yaml
# 微信配置
wechat:
  path: "C:\\Program Files\\Tencent\\Weixin"  # 微信安装目录
  auto_reply: true
  reply_delay: [1, 3]

# AI配置
ai:
  provider: "doubao"
  model: "your-endpoint-id"  # 豆包模型的 Endpoint ID
  temperature: 0.8
```

### 6. 配置人格（可选）

编辑 `config/persona.yaml` 文件，自定义AI女友的性格和说话风格。

### 7. 运行程序

**方式一：使用Web管理面板（推荐）**

```bash
# 启动Web管理面板
python src/web/app.py

# 或使用启动脚本
start_web_panel.bat
```

访问 http://127.0.0.1:5000 打开管理面板，在界面中配置所有参数。

**方式二：命令行模式**

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
│   │   ├── wechat_client.py   # 微信客户端（支持 wxauto 和 WeChatFerry）
│   │   ├── ai_engine.py       # AI对话引擎（支持豆包/Claude/OpenAI）
│   │   └── message_handler.py # 消息处理器
│   ├── personality/           # 人格系统
│   │   ├── persona.py         # 人格管理
│   │   └── prompts.py         # 提示词模板
│   ├── utils/                 # 工具模块
│   │   ├── config.py          # 配置管理
│   │   ├── logger.py          # 日志系统
│   │   └── context_manager.py # 上下文管理
│   ├── web/                   # Web管理面板
│   │   ├── app.py             # Flask应用
│   │   ├── api/               # API路由
│   │   ├── static/            # 静态文件（CSS/JS）
│   │   └── templates/         # HTML模板
│   └── main.py                # 主程序入口
├── config/                    # 配置文件
│   ├── config.yaml            # 主配置
│   ├── persona.yaml           # 人格配置
│   ├── .env                   # 环境变量（需自行创建）
│   └── .env.example           # 环境变量模板
├── data/                      # 数据目录
│   ├── conversations/         # 对话历史
│   └── cache/                 # 缓存文件
├── logs/                      # 日志目录
├── requirements.txt           # 依赖列表
├── .gitignore                 # Git忽略文件
├── PROJECT_PLAN.md            # 项目规划文档
└── README.md                  # 本文件
```

## ⚙️ 配置说明

### 主配置文件 (config/config.yaml)

```yaml
# 微信配置
wechat:
  path: "C:\\Program Files\\Tencent\\Weixin"  # 微信安装目录（不是exe文件）
  auto_reply: true           # 是否自动回复
  reply_delay: [1, 3]        # 回复延迟范围（秒）
  max_message_length: 500    # 最大消息长度

# AI配置
ai:
  provider: "doubao"         # AI提供商：doubao/claude/openai
  model: "ep-20251226192412-8kff2"  # 豆包模型的 Endpoint ID
  max_tokens: 1000           # 最大生成token数
  temperature: 0.8           # 温度参数（0-1）
  max_context_messages: 20   # 最大上下文消息数

# 人格配置
personality:
  config_file: "config/persona.yaml"

# 过滤器配置
filters:
  whitelist: []              # 白名单（为空则接受所有）
  blacklist: []              # 黑名单
  keywords_filter: []        # 关键词过滤

# 日志配置
logging:
  level: "INFO"              # 日志级别：DEBUG/INFO/WARNING/ERROR
  file: "logs/ailive.log"    # 日志文件
  rotation: "100 MB"         # 日志轮转大小
  retention: "30 days"       # 日志保留时间
```

### 人格配置文件 (config/persona.yaml)

```yaml
name: "小雨"
age: 22
gender: "女"
occupation: "大学生"

personality:
  traits:
    - 温柔体贴
    - 善解人意
    - 活泼开朗
    - 有点小调皮

  interests:
    - 看电影
    - 听音乐
    - 旅游
    - 美食

speaking_style:
  tone: "温柔亲切"
  length: "适中"
  emoji_frequency: "适度"

  particles:
    - "呀"
    - "哦"
    - "呢"
    - "啦"

  expressions:
    - "嘻嘻"
    - "哈哈"
    - "嗯嗯"

relationship:
  role: "女朋友"
  intimacy_level: "亲密"

  behaviors:
    - 关心对方的日常
    - 分享自己的生活
    - 偶尔撒娇
    - 给予情感支持
```

### 环境变量文件 (config/.env)

```env
# 豆包 API 配置
DOUBAO_API_KEY=your_api_key_here
DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3

# Claude API 配置（可选）
# CLAUDE_API_KEY=your_claude_api_key_here

# OpenAI API 配置（可选）
# OPENAI_API_KEY=your_openai_api_key_here
```

## 📖 使用说明

### 正常模式

1. 确保微信客户端已登录
2. 运行 `python src/main.py`
3. 程序会自动监听微信消息并回复
4. 按 `Ctrl+C` 停止程序

### 交互测试模式

1. 运行 `python src/main.py --mode interactive`
2. 在命令行中输入消息测试AI回复
3. 输入 `quit` 退出

### 黑白名单设置

编辑 `config/config.yaml`：

```yaml
filters:
  whitelist: ["张三", "李四"]  # 只回复这些人（为空则接受所有）
  blacklist: ["王五"]          # 不回复这些人
  keywords_filter: ["广告", "推广"]  # 包含这些关键词的消息不回复
```

## 🌐 Web管理面板

### 启动管理面板

```bash
# 方式一：直接运行
python src/web/app.py

# 方式二：使用启动脚本
start_web_panel.bat
```

访问地址：http://127.0.0.1:5000

### 功能特性

**1. AI配置页面**
- 选择AI提供商（豆包/Claude/OpenAI）
- 配置模型参数（Temperature、Max Tokens等）
- 管理API密钥
- 测试API连接

**2. 人格配置页面**
- 设置基本信息（姓名、年龄、性别、职业）
- 配置性格特征和兴趣爱好
- 自定义说话风格（语气、语气词、常用表达）
- 设置关系角色和行为特征

**3. 微信配置页面**
- 设置微信路径
- 配置自动回复参数
- 管理黑白名单
- 设置关键词过滤

### 使用说明

1. **首次使用**：启动面板后，依次配置AI、人格和微信设置
2. **修改配置**：在对应页面修改后点击"保存配置"
3. **测试连接**：在AI配置页面可以测试API连接是否正常
4. **实时生效**：配置保存后，重启主程序即可生效

### API端点

管理面板提供以下RESTful API：

- `GET /api/config/ai` - 获取AI配置
- `POST /api/config/ai` - 保存AI配置
- `GET /api/config/persona` - 获取人格配置
- `POST /api/config/persona` - 保存人格配置
- `GET /api/config/wechat` - 获取微信配置
- `POST /api/config/wechat` - 保存微信配置
- `POST /api/config/test` - 测试API连接
- `GET /health` - 健康检查

## 🔧 微信版本兼容性

本项目支持两种微信自动化库：

### wxauto（推荐）
- **支持版本**：微信 3.9.x
- **推荐版本**：3.9.10
- **下载地址**：https://dldir1.qq.com/weixin/Windows/WeChatSetup_3.9.10.19.exe
- **安装方式**：`pip install git+https://github.com/cluic/wxauto.git`
- **优点**：稳定可靠，经过充分测试

### WeChatFerry
- **支持版本**：微信 4.0+
- **安装方式**：`pip install wcferry`
- **注意**：可能存在兼容性问题，建议使用 wxauto

程序会自动检测微信版本并选择合适的库。

## ⚠️ 注意事项

1. **微信版本**：推荐使用微信 3.9.10 版本，兼容性最好
2. **封号风险**：虽然使用官方客户端，但仍有一定风险，建议使用小号测试
3. **API费用**：豆包API按使用量计费，建议设置每日上限
4. **隐私安全**：
   - 不要记录敏感信息
   - 对话历史仅保存在本地
   - 不要将 `.env` 文件提交到Git仓库
5. **合规性**：仅用于个人学习和研究，不要用于商业用途
6. **消息获取**：wxauto 只能读取当前打开的聊天窗口的消息

## 🐛 常见问题

### Q: 提示"微信未登录或未运行"？
A: 请确保微信客户端已打开并登录。

### Q: 提示"未设置DOUBAO_API_KEY"？
A: 请检查 `config/.env` 文件是否正确配置了API密钥。

### Q: 无法获取微信消息？
A:
- 确保使用的是微信 3.9.10 版本
- 确保已打开要监听的聊天窗口
- wxauto 只能读取当前打开的聊天窗口

### Q: wxauto 安装失败？
A:
```bash
# 如果有代理，使用代理安装
pip install git+https://github.com/cluic/wxauto.git

# 或者先克隆再安装
git clone https://github.com/cluic/wxauto.git
cd wxauto
pip install -e .
```

### Q: Python 3.8 类型注解错误？
A: 这是 wxauto 的已知问题，已在项目中修复。如果仍有问题，请检查 wxauto 的 component.py 文件。

### Q: AI回复质量不好？
A:
- 调整 `config/persona.yaml` 中的人格设置
- 修改 `config/config.yaml` 中的 `ai.temperature` 参数（0-1，越高越随机）
- 调整 `ai.max_context_messages` 增加上下文记忆

### Q: 如何查看日志？
A: 日志文件保存在 `logs/ailive.log`，可以设置日志级别为 DEBUG 查看详细信息。

### Q: 如何切换AI提供商？
A:
- **使用Web管理面板**：访问 http://127.0.0.1:5000，在AI配置页面选择提供商并保存
- **手动编辑**：编辑 `config/config.yaml`，修改 `ai.provider` 为 `doubao`、`claude` 或 `openai`，并在 `.env` 中配置相应的API密钥

### Q: Web管理面板无法访问？
A:
- 确保Flask已安装：`pip install flask flask-cors`
- 检查端口5000是否被占用
- 查看启动日志中的错误信息

## 🎯 获取豆包API密钥

1. 访问火山引擎控制台：https://console.volcengine.com/ark
2. 创建推理接入点（Endpoint）
3. 选择合适的模型（如：豆包视觉理解模型）
4. 获取 Endpoint ID（格式：ep-xxxxxx）
5. 创建 API Key
6. 将 Endpoint ID 填入 `config/config.yaml` 的 `ai.model`
7. 将 API Key 填入 `config/.env` 的 `DOUBAO_API_KEY`

## 🔧 开发计划

- [x] 支持豆包API
- [x] 支持微信 3.9 和 4.0+
- [x] 人格系统
- [x] 上下文管理
- [x] **Web管理界面**
- [ ] 支持群聊消息
- [ ] 添加图片识别能力
- [ ] 添加语音消息处理
- [ ] 支持更多AI模型
- [ ] 对话历史查看和导出

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📮 联系方式

如有问题，请提交Issue。

---

**⚠️ 免责声明**：本项目仅供学习和研究使用，使用者需自行承担使用本项目可能带来的风险。作者不对使用本项目造成的任何后果负责。
