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
                document.getElementById('doubao-api-base').value = data.api_keys.doubao_base || 'https://ark.cn-beijing.volces.com/api/v3';
                if (data.api_keys.claude) {
                    document.getElementById('claude-api-key').placeholder = '已设置（点击修改）';
                }
                if (data.api_keys.openai) {
                    document.getElementById('openai-api-key').placeholder = '已设置（点击修改）';
                }
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

        if (doubaoKey) data.api_keys.doubao = doubaoKey;
        if (doubaoBase) data.api_keys.doubao_base = doubaoBase;
        if (claudeKey) data.api_keys.claude = claudeKey;
        if (openaiKey) data.api_keys.openai = openaiKey;

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

// 测试API连接
async function testAPIConnection() {
    const btn = document.getElementById('test-api-btn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>测试中...';

    try {
        const provider = document.getElementById('ai-provider').value;
        const response = await axios.post(`${API_BASE}/config/test`, { provider });
        if (response.data.success) {
            showToast(`${provider} API连接成功`, 'success');
        } else {
            showToast('连接失败: ' + response.data.error, 'error');
        }
    } catch (error) {
        showToast('连接失败: ' + error.message, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-plug"></i> 测试连接';
    }
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
});
