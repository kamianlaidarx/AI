// AILive 管理面板 JavaScript

const API_BASE = '/api';

// Toast通知
function showToast(message, type = 'info') {
    const toast = document.getElementById('notification-toast');
    const toastBody = toast.querySelector('.toast-body');
    const toastHeader = toast.querySelector('.toast-header');
    const icon = toastHeader.querySelector('i');

    // 设置图标和颜色
    if (type === 'success') {
        icon.className = 'bi bi-check-circle me-2';
        toastHeader.style.backgroundColor = '#198754';
    } else if (type === 'error') {
        icon.className = 'bi bi-exclamation-circle me-2';
        toastHeader.style.backgroundColor = '#dc3545';
    } else {
        icon.className = 'bi bi-info-circle me-2';
        toastHeader.style.backgroundColor = '#0d6efd';
    }

    toastBody.textContent = message;
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// 加载AI配置
async function loadAIConfig() {
    try {
        const response = await axios.get(`${API_BASE}/config/ai`);
        if (response.data.success) {
            const data = response.data.data;
            document.getElementById('ai-provider').value = data.provider || 'doubao';
            document.getElementById('ai-model').value = data.model || '';
            document.getElementById('ai-temperature').value = data.temperature || 0.8;
            document.getElementById('temperature-value').textContent = data.temperature || 0.8;
            document.getElementById('ai-max-tokens').value = data.max_tokens || 1000;
            document.getElementById('ai-max-context').value = data.max_context_messages || 20;

            // API密钥（显示为占位符）
            if (data.api_keys) {
                if (data.api_keys.doubao) {
                    document.getElementById('doubao-api-key').placeholder = '已设置（点击修改）';
                }
                document.getElementById('doubao-api-base').value = data.api_keys.doubao_base || '';
                if (data.api_keys.claude) {
                    document.getElementById('claude-api-key').placeholder = '已设置（点击修改）';
                }
                if (data.api_keys.openai) {
                    document.getElementById('openai-api-key').placeholder = '已设置（点击修改）';
                }
                document.getElementById('openai-api-base').value = data.api_keys.openai_base || '';
            }
        }
    } catch (error) {
        showToast('加载AI配置失败: ' + error.message, 'error');
    }
}

// 保存AI配置
async function saveAIConfig(event) {
    event.preventDefault();
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>保存中...';

    try {
        const data = {
            provider: document.getElementById('ai-provider').value,
            model: document.getElementById('ai-model').value,
            temperature: parseFloat(document.getElementById('ai-temperature').value),
            max_tokens: parseInt(document.getElementById('ai-max-tokens').value),
            max_context_messages: parseInt(document.getElementById('ai-max-context').value),
            api_keys: {}
        };

        // 只保存非空的API密钥
        const doubaoKey = document.getElementById('doubao-api-key').value;
        const doubaoBase = document.getElementById('doubao-api-base').value;
        const claudeKey = document.getElementById('claude-api-key').value;
        const openaiKey = document.getElementById('openai-api-key').value;
        const openaiBase = document.getElementById('openai-api-base').value;

        if (doubaoKey) data.api_keys.doubao = doubaoKey;
        if (doubaoBase) data.api_keys.doubao_base = doubaoBase;
        if (claudeKey) data.api_keys.claude = claudeKey;
        if (openaiKey) data.api_keys.openai = openaiKey;
        if (openaiBase) data.api_keys.openai_base = openaiBase;

        const response = await axios.post(`${API_BASE}/config/ai`, data);
        if (response.data.success) {
            showToast('AI配置保存成功', 'success');
            // 清空密码输入框
            document.getElementById('doubao-api-key').value = '';
            document.getElementById('claude-api-key').value = '';
            document.getElementById('openai-api-key').value = '';
        } else {
            showToast('保存失败: ' + response.data.error, 'error');
        }
    } catch (error) {
        showToast('保存失败: ' + error.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-save"></i> 保存配置';
    }
}

// 测试API连接 - 打开对话窗口
async function testAPIConnection() {
    const provider = document.getElementById('ai-provider').value;
    const model = document.getElementById('ai-model').value;

    // 更新对话窗口信息
    document.getElementById('test-chat-provider').textContent = provider;
    document.getElementById('test-chat-model').textContent = model || '默认模型';

    // 清空对话记录
    clearTestChat();

    // 清空测试会话上下文
    testChatContext = [];

    // 打开对话窗口
    const modal = new bootstrap.Modal(document.getElementById('test-chat-modal'));
    modal.show();
}

// 测试会话上下文
let testChatContext = [];

// 发送测试消息
async function sendTestMessage() {
    const input = document.getElementById('test-chat-input');
    const message = input.value.trim();

    if (!message) return;

    const messagesContainer = document.getElementById('test-chat-messages');
    const sendBtn = document.getElementById('test-chat-send');

    // 禁用发送按钮
    sendBtn.disabled = true;
    sendBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';

    // 显示用户消息
    appendMessage(messagesContainer, message, 'user');
    input.value = '';

    try {
        const provider = document.getElementById('ai-provider').value;
        const model = document.getElementById('ai-model').value;

        // 获取当前配置的 API 信息
        const doubaoBase = document.getElementById('doubao-api-base').value;
        const openaiBase = document.getElementById('openai-api-base').value;

        const response = await axios.post(`${API_BASE}/config/test/chat`, {
            provider: provider,
            model: model,
            message: message,
            context: testChatContext,
            api_keys: {
                doubao_base: doubaoBase,
                openai_base: openaiBase
            }
        });

        if (response.data.success) {
            const reply = response.data.data.reply;
            appendMessage(messagesContainer, reply, 'assistant');

            // 更新上下文
            testChatContext.push({ role: 'user', content: message });
            testChatContext.push({ role: 'assistant', content: reply });

            // 保持上下文在合理范围内
            if (testChatContext.length > 20) {
                testChatContext = testChatContext.slice(-20);
            }
        } else {
            appendMessage(messagesContainer, '❌ 错误: ' + response.data.error, 'error');
        }
    } catch (error) {
        appendMessage(messagesContainer, '❌ 请求失败: ' + error.message, 'error');
    } finally {
        sendBtn.disabled = false;
        sendBtn.innerHTML = '<i class="bi bi-send"></i> 发送';
    }
}

// 添加消息到对话窗口
function appendMessage(container, message, role) {
    // 移除初始提示
    const placeholder = container.querySelector('.text-muted');
    if (placeholder) {
        placeholder.remove();
    }

    const div = document.createElement('div');
    div.className = `mb-2 ${role === 'user' ? 'text-end' : ''}`;

    const badge = document.createElement('span');
    if (role === 'user') {
        badge.className = 'badge bg-primary';
        badge.textContent = '你';
    } else if (role === 'assistant') {
        badge.className = 'badge bg-success';
        badge.textContent = 'AI';
    } else {
        badge.className = 'badge bg-danger';
        badge.textContent = '系统';
    }

    const content = document.createElement('div');
    content.className = `d-inline-block p-2 rounded ${role === 'user' ? 'bg-primary text-white' : role === 'assistant' ? 'bg-white border' : 'bg-danger text-white'}`;
    content.style.maxWidth = '80%';
    content.style.textAlign = 'left';
    content.textContent = message;

    div.appendChild(badge);
    div.appendChild(document.createElement('br'));
    div.appendChild(content);

    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

// 清空测试对话
function clearTestChat() {
    const container = document.getElementById('test-chat-messages');
    container.innerHTML = `
        <div class="text-center text-muted">
            <i class="bi bi-chat-left-text"></i> 发送消息开始测试对话
        </div>
    `;
    testChatContext = [];
}

// 加载人格配置
async function loadPersonaConfig() {
    try {
        const response = await axios.get(`${API_BASE}/config/persona`);
        if (response.data.success) {
            const data = response.data.data;
            document.getElementById('persona-name').value = data.name || '';
            document.getElementById('persona-age').value = data.age || 22;
            document.getElementById('persona-gender').value = data.gender || '女';
            document.getElementById('persona-occupation').value = data.occupation || '';

            // 性格特征
            if (data.personality) {
                if (data.personality.traits) {
                    document.getElementById('persona-traits').value = data.personality.traits.join('\n');
                }
                if (data.personality.interests) {
                    document.getElementById('persona-interests').value = data.personality.interests.join('\n');
                }
            }

            // 说话风格
            if (data.speaking_style) {
                document.getElementById('persona-tone').value = data.speaking_style.tone || '';
                if (data.speaking_style.particles) {
                    document.getElementById('persona-particles').value = data.speaking_style.particles.join(',');
                }
                if (data.speaking_style.expressions) {
                    document.getElementById('persona-expressions').value = data.speaking_style.expressions.join(',');
                }
            }

            // 关系设定
            if (data.relationship) {
                document.getElementById('persona-role').value = data.relationship.role || '女朋友';
                document.getElementById('persona-intimacy').value = data.relationship.intimacy_level || '亲密';
                if (data.relationship.behaviors) {
                    document.getElementById('persona-behaviors').value = data.relationship.behaviors.join('\n');
                }
            }
        }
    } catch (error) {
        showToast('加载人格配置失败: ' + error.message, 'error');
    }
}

// 保存人格配置
async function savePersonaConfig(event) {
    event.preventDefault();
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>保存中...';

    try {
        const data = {
            name: document.getElementById('persona-name').value,
            age: parseInt(document.getElementById('persona-age').value),
            gender: document.getElementById('persona-gender').value,
            occupation: document.getElementById('persona-occupation').value,
            personality: {
                traits: document.getElementById('persona-traits').value.split('\n').filter(t => t.trim()),
                interests: document.getElementById('persona-interests').value.split('\n').filter(i => i.trim())
            },
            speaking_style: {
                tone: document.getElementById('persona-tone').value,
                length: "适中",
                emoji_frequency: "适度",
                particles: document.getElementById('persona-particles').value.split(',').map(p => p.trim()).filter(p => p),
                expressions: document.getElementById('persona-expressions').value.split(',').map(e => e.trim()).filter(e => e)
            },
            relationship: {
                role: document.getElementById('persona-role').value,
                intimacy_level: document.getElementById('persona-intimacy').value,
                behaviors: document.getElementById('persona-behaviors').value.split('\n').filter(b => b.trim())
            }
        };

        const response = await axios.post(`${API_BASE}/config/persona`, data);
        if (response.data.success) {
            showToast('人格配置保存成功', 'success');
        } else {
            showToast('保存失败: ' + response.data.error, 'error');
        }
    } catch (error) {
        showToast('保存失败: ' + error.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-save"></i> 保存配置';
    }
}

// 加载微信配置
async function loadWeChatConfig() {
    try {
        const response = await axios.get(`${API_BASE}/config/wechat`);
        if (response.data.success) {
            const data = response.data.data;
            document.getElementById('wechat-path').value = data.path || '';
            document.getElementById('wechat-auto-reply').checked = data.auto_reply !== false;

            if (data.reply_delay && Array.isArray(data.reply_delay)) {
                document.getElementById('wechat-delay-min').value = data.reply_delay[0] || 1;
                document.getElementById('wechat-delay-max').value = data.reply_delay[1] || 3;
            }

            document.getElementById('wechat-max-length').value = data.max_message_length || 500;

            if (data.whitelist) {
                document.getElementById('wechat-whitelist').value = data.whitelist.join('\n');
            }
            if (data.blacklist) {
                document.getElementById('wechat-blacklist').value = data.blacklist.join('\n');
            }
            if (data.keywords_filter) {
                document.getElementById('wechat-keywords').value = data.keywords_filter.join('\n');
            }
        }
    } catch (error) {
        showToast('加载微信配置失败: ' + error.message, 'error');
    }
}

// 保存微信配置
async function saveWeChatConfig(event) {
    event.preventDefault();
    const form = event.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>保存中...';

    try {
        const data = {
            path: document.getElementById('wechat-path').value,
            auto_reply: document.getElementById('wechat-auto-reply').checked,
            reply_delay: [
                parseInt(document.getElementById('wechat-delay-min').value),
                parseInt(document.getElementById('wechat-delay-max').value)
            ],
            max_message_length: parseInt(document.getElementById('wechat-max-length').value),
            whitelist: document.getElementById('wechat-whitelist').value.split('\n').filter(w => w.trim()),
            blacklist: document.getElementById('wechat-blacklist').value.split('\n').filter(b => b.trim()),
            keywords_filter: document.getElementById('wechat-keywords').value.split('\n').filter(k => k.trim())
        };

        const response = await axios.post(`${API_BASE}/config/wechat`, data);
        if (response.data.success) {
            showToast('微信配置保存成功', 'success');
        } else {
            showToast('保存失败: ' + response.data.error, 'error');
        }
    } catch (error) {
        showToast('保存失败: ' + error.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="bi bi-save"></i> 保存配置';
    }
}

// Temperature滑块更新
document.addEventListener('DOMContentLoaded', function() {
    const temperatureSlider = document.getElementById('ai-temperature');
    const temperatureValue = document.getElementById('temperature-value');

    temperatureSlider.addEventListener('input', function() {
        temperatureValue.textContent = this.value;
    });

    // 加载所有配置
    loadAIConfig();
    loadPersonaConfig();
    loadWeChatConfig();

    // 绑定表单提交事件
    document.getElementById('ai-config-form').addEventListener('submit', saveAIConfig);
    document.getElementById('persona-config-form').addEventListener('submit', savePersonaConfig);
    document.getElementById('wechat-config-form').addEventListener('submit', saveWeChatConfig);

    // 绑定测试按钮
    document.getElementById('test-api-btn').addEventListener('click', testAPIConnection);

    // 绑定测试会话按钮
    document.getElementById('test-chat-send').addEventListener('click', sendTestMessage);
    document.getElementById('test-chat-clear').addEventListener('click', clearTestChat);
    document.getElementById('test-chat-input').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendTestMessage();
        }
    });
});
