# AILive - 微信AI女友机器人

一个基于Python的微信AI女友机器人，使用豆包（Doubao）API实现智能对话。

## ✨ 核心特性

- 🤖 **智能对话** - 基于豆包（Doubao）API的高质量AI对话
- 💬 **自动回复** - 支持微信消息自动回复，只回复新消息
- 🎭 **人格定制** - 可自定义AI女友的性格、说话风格和行为特征
- 💾 **记忆功能** - 持久化上下文记忆，自动保存和加载对话历史
- 💌 **主动聊天** - AI会在你长时间没发消息时主动找你聊天
- 🌐 **Web管理面板** - 可视化配置界面，无需手动编辑配置文件
- 🛡️ **智能过滤** - 支持黑白名单和关键词过滤
- 📝 **完善日志** - 详细的运行日志，方便调试和监控

## 📋 环境要求

- **操作系统**：Windows（微信自动化仅支持Windows）
- **Python版本**：3.8+
- **微信版本**：3.9.10（推荐）
- **API密钥**：豆包（Doubao）API密钥

## 🚀 快速开始

### 第一步：安装Python环境

1. 下载并安装 Python 3.8+：https://www.python.org/downloads/
2. 安装时勾选 "Add Python to PATH"

### 第二步：下载项目

```bash
git clone <repository_url>
cd AILive
```

### 第三步：安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 升级pip
python -m pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt

# 安装wxauto（从GitHub）
pip install git+https://github.com/cluic/wxauto.git
```

### 第四步：获取豆包API密钥

1. 访问火山引擎控制台：https://console.volcengine.com/ark
2. 注册/登录账号
3. 创建推理接入点（Endpoint）
4. 选择合适的模型（推荐：豆包视觉理解模型）
5. 获取 **Endpoint ID**（格式：`ep-xxxxxx`）
6. 创建 **API Key**
7. 保存这两个信息，后面配置时需要用到

### 第五步：配置机器人

**方式一：使用Web管理面板（推荐，适合小白）**

1. 启动Web管理面板：
   ```bash
   python src\web\app.py
   ```

2. 在浏览器中打开：http://127.0.0.1:5000

3. 在"AI配置"页面填写：
   - **AI提供商**：选择"豆包 (Doubao)"
   - **模型/Endpoint ID**：填写你的Endpoint ID（如：`ep-20251226192412-8kff2`）
   - **豆包 API Key**：填写你的API密钥
   - **Temperature**：0.8（默认值，控制回复的随机性）
   - 点击"测试连接"验证配置
   - 点击"保存配置"

4. 在"人格配置"页面设置AI女友的性格（可选）：
   - 姓名、年龄、性别、职业
   - 性格特点（如：温柔体贴、善解人意）
   - 说话风格（语气词、常用表达）
   - 点击"保存配置"

5. 在"微信配置"页面设置（可选）：
   - 微信路径：`C:\Program Files\Tencent\Weixin`
   - 其他保持默认即可
   - 点击"保存配置"

6. 关闭Web管理面板（Ctrl+C）

**方式二：手动编辑配置文件（适合技术用户）**

1. 复制环境变量模板：
   ```bash
   copy config\.env.example config\.env
   ```

2. 编辑 `config/.env` 文件：
   ```env
   DOUBAO_API_KEY=你的API密钥
   DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3
   ```

3. 编辑 `config/config.yaml` 文件：
   ```yaml
   ai:
     provider: "doubao"
     model: "你的Endpoint-ID"  # 如：ep-20251226192412-8kff2
     temperature: 0.8
   ```

4. （可选）编辑 `config/persona.yaml` 自定义人格

### 第六步：安装微信3.9.10

1. 下载微信3.9.10：https://dldir1.qq.com/weixin/Windows/WeChatSetup_3.9.10.19.exe
2. 安装并登录微信账号
3. **重要**：不要升级微信版本

### 第七步：启动机器人

1. 确保微信已登录
2. 双击运行 `start_bot.bat`
3. 看到"机器人已启动，开始监听消息..."表示成功
4. 打开要监听的聊天窗口
5. 开始对话！

## 📖 使用说明

### 基本使用

1. **启动机器人**：双击 `start_bot.bat`
2. **打开聊天窗口**：打开要监听的微信聊天窗口
3. **发送消息**：对方发消息后，机器人会自动回复
4. **停止机器人**：在命令行窗口按 `Ctrl+C`

### 重要提示

**wxauto的限制：**
- ✅ 只能监听**当前打开的聊天窗口**
- ✅ 需要保持聊天窗口打开（可以最小化微信）
- ❌ 无法同时监听多个聊天
- ❌ 切换到其他聊天会停止监听

**使用建议：**
1. 启动机器人后，打开要监听的聊天窗口
2. 保持该窗口打开（不要切换到其他聊天）
3. 可以最小化微信，但不要关闭

### 核心功能

#### 1. 持久化记忆

机器人会记住你们的对话：
- 自动保存对话历史（每5条消息）
- 重启后自动加载历史对话
- 从上次对话的地方继续

**示例：**
```
第一天:
你: 我叫小明，喜欢打篮球
AI: 小明你好！打篮球很酷呀~

第二天（重启后）:
你: 今天打球了
AI: 打篮球了吗？玩得开心吗？小明~
```

#### 2. 主动对话

AI会在你长时间没发消息时主动找你：
- 默认1小时没消息就主动
- 每天最多主动3次
- 基于之前的对话内容生成问候

**示例：**
```
10:00 你: 我今天要去打篮球
10:01 AI: 哇，打篮球很酷呀！

[1小时后]

11:30 AI: 打完篮球了吗？累不累呀~
```

**配置主动对话：**

在 `config/config.yaml` 中：
```yaml
proactive_chat:
  enabled: true              # 是否启用
  idle_time: 3600            # 闲置1小时后主动（秒）
  min_interval: 1800         # 最小间隔30分钟（秒）
  max_daily_proactive: 3     # 每天最多3次
```

#### 3. 黑白名单

在 `config/config.yaml` 中配置：
```yaml
filters:
  whitelist: ["张三", "李四"]  # 只回复这些人（为空则接受所有）
  blacklist: ["王五"]          # 不回复这些人
  keywords_filter: ["广告", "推广"]  # 包含这些关键词的消息不回复
```

## 🌐 Web管理面板

### 启动面板

```bash
# 方式一：直接运行
python src\web\app.py

# 方式二：使用启动脚本
start_web_panel.bat
```

访问地址：http://127.0.0.1:5000

### 功能说明

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

### 使用流程

1. 启动Web管理面板
2. 在浏览器中配置各项参数
3. 点击"保存配置"
4. 关闭Web管理面板
5. 启动机器人

## 📁 项目结构

```
AILive/
├── src/
│   ├── core/                  # 核心模块
│   │   ├── wechat_client.py   # 微信客户端（支持wxauto和WeChatFerry）
│   │   ├── ai_engine.py       # AI对话引擎（支持豆包/Claude/OpenAI）
│   │   ├── message_handler.py # 消息处理器
│   │   └── proactive_chat.py  # 主动对话管理器
│   ├── personality/           # 人格系统
│   │   ├── persona.py         # 人格管理
│   │   └── prompts.py         # 提示词模板
│   ├── utils/                 # 工具模块
│   │   ├── config.py          # 配置管理
│   │   ├── logger.py          # 日志系统
│   │   └── context_manager.py # 上下文管理（持久化记忆）
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
│   └── conversations/         # 对话历史（自动创建）
├── logs/                      # 日志目录（自动创建）
├── start_bot.bat              # 启动机器人脚本
├── start_web_panel.bat        # 启动Web面板脚本
├── requirements.txt           # Python依赖
├── README.md                  # 本文件
├── 快速启动.txt               # 快速启动指南
├── 上下文记忆说明.txt         # 记忆功能说明
└── 主动对话功能说明.txt       # 主动对话说明
```

## ⚙️ 配置说明

### 主配置文件 (config/config.yaml)

```yaml
# 微信配置
wechat:
  path: "C:\\Program Files\\Tencent\\Weixin"  # 微信安装目录
  auto_reply: true           # 是否自动回复
  reply_delay: [1, 3]        # 回复延迟范围（秒）
  max_message_length: 500    # 最大消息长度

# AI配置
ai:
  provider: "doubao"         # AI提供商：doubao/claude/openai
  model: "ep-xxxxxx"         # 豆包模型的Endpoint ID
  max_tokens: 1000           # 最大生成token数
  temperature: 0.8           # 温度参数（0-1，越高越随机）
  max_context_messages: 20   # 最大上下文消息数

# 人格配置
personality:
  config_file: "config/persona.yaml"

# 过滤器配置
filters:
  whitelist: []              # 白名单（为空则接受所有）
  blacklist: []              # 黑名单
  keywords_filter: []        # 关键词过滤

# 主动对话配置
proactive_chat:
  enabled: true              # 是否启用主动对话
  idle_time: 3600            # 闲置多久后主动（秒）
  min_interval: 1800         # 最小间隔时间（秒）
  max_daily_proactive: 3     # 每天最多主动几次

# 日志配置
logging:
  level: "INFO"              # 日志级别：DEBUG/INFO/WARNING/ERROR
  file: "logs/ailive.log"    # 日志文件
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
# 豆包API配置
DOUBAO_API_KEY=你的API密钥
DOUBAO_API_BASE=https://ark.cn-beijing.volces.com/api/v3

# Claude API配置（可选）
# CLAUDE_API_KEY=your_claude_api_key_here

# OpenAI API配置（可选）
# OPENAI_API_KEY=your_openai_api_key_here
```

## 🐛 常见问题

### Q: 启动后微信被关闭？
**A:** 已修复此问题。确保使用微信3.9.10版本，机器人会自动使用wxauto库。

### Q: 提示"微信未登录或未运行"？
**A:**
1. 确保微信客户端已打开
2. 确保已登录账号
3. 检查微信路径配置是否正确

### Q: 提示"未设置DOUBAO_API_KEY"？
**A:**
1. 检查 `config/.env` 文件是否存在
2. 检查API密钥是否正确填写
3. 可以使用Web管理面板重新配置

### Q: 无法获取微信消息？
**A:**
1. 确保使用微信3.9.10版本
2. 确保已打开要监听的聊天窗口
3. wxauto只能读取当前打开的聊天窗口

### Q: 机器人回复了历史消息？
**A:** 已修复此问题。启动时会自动清空历史消息，只回复新消息。

### Q: wxauto安装失败？
**A:**
```bash
# 如果有代理，使用代理安装
pip install git+https://github.com/cluic/wxauto.git

# 或者先克隆再安装
git clone https://github.com/cluic/wxauto.git
cd wxauto
pip install -e .
```

### Q: AI回复质量不好？
**A:**
1. 调整 `config/persona.yaml` 中的人格设置
2. 修改 `config/config.yaml` 中的 `temperature` 参数（0-1）
3. 调整 `max_context_messages` 增加上下文记忆

### Q: 如何查看日志？
**A:** 日志文件保存在 `logs/ailive.log`，可以设置日志级别为DEBUG查看详细信息。

### Q: Web管理面板无法访问？
**A:**
1. 确保Flask已安装：`pip install flask flask-cors`
2. 检查端口5000是否被占用
3. 查看启动日志中的错误信息

### Q: 如何切换AI提供商？
**A:**
- **使用Web管理面板**：访问 http://127.0.0.1:5000，在AI配置页面选择提供商
- **手动编辑**：编辑 `config/config.yaml`，修改 `ai.provider`

## ⚠️ 注意事项

1. **微信版本**：推荐使用微信3.9.10版本，兼容性最好
2. **封号风险**：虽然使用官方客户端，但仍有一定风险，建议使用小号测试
3. **API费用**：豆包API按使用量计费，建议设置每日上限
4. **隐私安全**：
   - 对话历史保存在本地
   - 不要将 `.env` 文件提交到Git仓库
   - 注意保护 `data/conversations/` 目录
5. **合规性**：仅用于个人学习和研究，不要用于商业用途
6. **消息获取**：wxauto只能读取当前打开的聊天窗口

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📮 联系方式

如有问题，请提交Issue。

---

**⚠️ 免责声明**：本项目仅供学习和研究使用，使用者需自行承担使用本项目可能带来的风险。作者不对使用本项目造成的任何后果负责。
