"""
配置管理API
"""
import os
import yaml
from pathlib import Path
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv, set_key

config_bp = Blueprint('config', __name__)

# 配置文件路径
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / 'config'
CONFIG_YAML = CONFIG_DIR / 'config.yaml'
PERSONA_YAML = CONFIG_DIR / 'persona.yaml'
ENV_FILE = CONFIG_DIR / '.env'


def load_yaml_file(file_path):
    """加载YAML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {'error': str(e)}


def save_yaml_file(file_path, data):
    """保存YAML文件"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        return True
    except Exception as e:
        return {'error': str(e)}


def load_env_file():
    """加载.env文件"""
    try:
        load_dotenv(ENV_FILE)
        return {
            'DOUBAO_API_KEY': os.getenv('DOUBAO_API_KEY', ''),
            'DOUBAO_API_BASE': os.getenv('DOUBAO_API_BASE', ''),
            'CLAUDE_API_KEY': os.getenv('CLAUDE_API_KEY', ''),
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
            'OPENAI_API_BASE': os.getenv('OPENAI_API_BASE', ''),
        }
    except Exception as e:
        return {'error': str(e)}


def save_env_file(data):
    """保存.env文件"""
    try:
        for key, value in data.items():
            if value:  # 只保存非空值
                set_key(ENV_FILE, key, value)
        return True
    except Exception as e:
        return {'error': str(e)}


@config_bp.route('/config/ai', methods=['GET'])
def get_ai_config():
    """获取AI配置"""
    try:
        config = load_yaml_file(CONFIG_YAML)
        env_config = load_env_file()

        if 'error' in config:
            return jsonify({'success': False, 'error': config['error']}), 500
        if 'error' in env_config:
            return jsonify({'success': False, 'error': env_config['error']}), 500

        return jsonify({
            'success': True,
            'data': {
                'provider': config.get('ai', {}).get('provider', 'doubao'),
                'model': config.get('ai', {}).get('model', ''),
                'temperature': config.get('ai', {}).get('temperature', 0.8),
                'max_tokens': config.get('ai', {}).get('max_tokens', 1000),
                'max_context_messages': config.get('ai', {}).get('max_context_messages', 500),
                'api_keys': {
                    'doubao': env_config.get('DOUBAO_API_KEY', ''),
                    'doubao_base': env_config.get('DOUBAO_API_BASE', ''),
                    'claude': env_config.get('CLAUDE_API_KEY', ''),
                    'openai': env_config.get('OPENAI_API_KEY', ''),
                    'openai_base': env_config.get('OPENAI_API_BASE', ''),
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@config_bp.route('/config/ai', methods=['POST'])
def save_ai_config():
    """保存AI配置"""
    try:
        data = request.json

        # 更新config.yaml
        config = load_yaml_file(CONFIG_YAML)
        if 'error' in config:
            return jsonify({'success': False, 'error': config['error']}), 500

        if 'ai' not in config:
            config['ai'] = {}

        config['ai']['provider'] = data.get('provider', 'doubao')
        config['ai']['model'] = data.get('model', '')
        config['ai']['temperature'] = float(data.get('temperature', 0.8))
        config['ai']['max_tokens'] = int(data.get('max_tokens', 1000))
        config['ai']['max_context_messages'] = int(data.get('max_context_messages', 20))

        result = save_yaml_file(CONFIG_YAML, config)
        if isinstance(result, dict) and 'error' in result:
            return jsonify({'success': False, 'error': result['error']}), 500

        # 更新.env文件
        api_keys = data.get('api_keys', {})
        env_data = {}
        if api_keys.get('doubao'):
            env_data['DOUBAO_API_KEY'] = api_keys['doubao']
        if api_keys.get('doubao_base'):
            env_data['DOUBAO_API_BASE'] = api_keys['doubao_base']
        if api_keys.get('claude'):
            env_data['CLAUDE_API_KEY'] = api_keys['claude']
        if api_keys.get('openai'):
            env_data['OPENAI_API_KEY'] = api_keys['openai']
        if api_keys.get('openai_base'):
            env_data['OPENAI_API_BASE'] = api_keys['openai_base']

        if env_data:
            result = save_env_file(env_data)
            if isinstance(result, dict) and 'error' in result:
                return jsonify({'success': False, 'error': result['error']}), 500

        return jsonify({'success': True, 'message': 'AI配置保存成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@config_bp.route('/config/persona', methods=['GET'])
def get_persona_config():
    """获取人格配置"""
    try:
        persona = load_yaml_file(PERSONA_YAML)
        if 'error' in persona:
            return jsonify({'success': False, 'error': persona['error']}), 500

        return jsonify({'success': True, 'data': persona})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@config_bp.route('/config/persona', methods=['POST'])
def save_persona_config():
    """保存人格配置"""
    try:
        data = request.json
        result = save_yaml_file(PERSONA_YAML, data)

        if isinstance(result, dict) and 'error' in result:
            return jsonify({'success': False, 'error': result['error']}), 500

        return jsonify({'success': True, 'message': '人格配置保存成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@config_bp.route('/config/wechat', methods=['GET'])
def get_wechat_config():
    """获取微信配置"""
    try:
        config = load_yaml_file(CONFIG_YAML)
        if 'error' in config:
            return jsonify({'success': False, 'error': config['error']}), 500

        return jsonify({
            'success': True,
            'data': {
                'path': config.get('wechat', {}).get('path', ''),
                'auto_reply': config.get('wechat', {}).get('auto_reply', True),
                'reply_delay': config.get('wechat', {}).get('reply_delay', [1, 3]),
                'max_message_length': config.get('wechat', {}).get('max_message_length', 500),
                'whitelist': config.get('filters', {}).get('whitelist', []),
                'blacklist': config.get('filters', {}).get('blacklist', []),
                'keywords_filter': config.get('filters', {}).get('keywords_filter', []),
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@config_bp.route('/config/wechat', methods=['POST'])
def save_wechat_config():
    """保存微信配置"""
    try:
        data = request.json
        config = load_yaml_file(CONFIG_YAML)

        if 'error' in config:
            return jsonify({'success': False, 'error': config['error']}), 500

        if 'wechat' not in config:
            config['wechat'] = {}
        if 'filters' not in config:
            config['filters'] = {}

        config['wechat']['path'] = data.get('path', '')
        config['wechat']['auto_reply'] = data.get('auto_reply', True)
        config['wechat']['reply_delay'] = data.get('reply_delay', [1, 3])
        config['wechat']['max_message_length'] = int(data.get('max_message_length', 500))

        config['filters']['whitelist'] = data.get('whitelist', [])
        config['filters']['blacklist'] = data.get('blacklist', [])
        config['filters']['keywords_filter'] = data.get('keywords_filter', [])

        result = save_yaml_file(CONFIG_YAML, config)
        if isinstance(result, dict) and 'error' in result:
            return jsonify({'success': False, 'error': result['error']}), 500

        return jsonify({'success': True, 'message': '微信配置保存成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@config_bp.route('/config/models', methods=['POST'])
def fetch_models():
    """获取模型列表"""
    try:
        data = request.json or {}
        provider = data.get('provider', 'openai')
        api_key = data.get('api_key', '')
        base_url = data.get('base_url', '')

        if not api_key:
            return jsonify({'success': False, 'error': 'API Key 未提供'}), 400

        models = []

        if provider == 'doubao':
            if not base_url:
                return jsonify({'success': False, 'error': 'API Base URL 未配置'}), 400
            try:
                from volcenginesdkarkruntime import Ark
            except ImportError:
                return jsonify({'success': False, 'error': '未安装 volcenginesdkarkruntime 库'}), 500

            client = Ark(api_key=api_key, base_url=base_url)
            response = client.models.list()
            models = [model.id for model in response.data]

        elif provider == 'claude':
            # Claude 没有官方模型列表API，返回常用模型
            models = [
                'claude-3-5-sonnet-20241022',
                'claude-3-5-haiku-20241022',
                'claude-3-opus-20240229',
                'claude-3-sonnet-20240229',
                'claude-3-haiku-20240307'
            ]

        elif provider == 'openai':
            if not base_url:
                return jsonify({'success': False, 'error': 'API Base URL 未配置'}), 400
            try:
                from openai import OpenAI
            except ImportError:
                return jsonify({'success': False, 'error': '未安装 openai 库'}), 500

            client = OpenAI(api_key=api_key, base_url=base_url)
            response = client.models.list()
            models = [model.id for model in response.data]

        else:
            return jsonify({'success': False, 'error': f'不支持的提供商: {provider}'}), 400

        return jsonify({
            'success': True,
            'data': {
                'models': models
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'error_type': e.__class__.__name__
        }), 500


@config_bp.route('/config/test', methods=['POST'])
def test_api_connection():
    """测试API连接"""
    provider = None
    try:
        data = request.json or {}
        provider = data.get('provider', 'doubao')

        env_config = load_env_file()
        if 'error' in env_config:
            return jsonify({'success': False, 'error': env_config['error']}), 500

        config_data = load_yaml_file(CONFIG_YAML)
        if 'error' in config_data:
            return jsonify({'success': False, 'error': config_data['error']}), 500

        ai_config = config_data.get('ai', {}) if isinstance(config_data, dict) else {}
        model = data.get('model') or ai_config.get('model', '')

        try:
            temperature = float(data.get('temperature', ai_config.get('temperature', 0.8)))
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'temperature 参数必须是数字'}), 400

        try:
            max_tokens = int(data.get('max_tokens', 200))
            max_tokens = max(10, min(max_tokens, 500))
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'max_tokens 参数必须是整数'}), 400

        test_message = data.get('test_message', '你好，这是一条测试消息。请简短回复确认收到。')
        api_keys = data.get('api_keys', {})

        if provider == 'doubao':
            api_key = api_keys.get('doubao') or env_config.get('DOUBAO_API_KEY', '')
            base_url = api_keys.get('doubao_base') or env_config.get('DOUBAO_API_BASE', '')
            if not api_key:
                return jsonify({'success': False, 'error': '豆包 API Key 未提供'}), 400
            if not base_url:
                return jsonify({'success': False, 'error': '豆包 API Base URL 未配置'}), 400
            if not model:
                model = 'doubao-pro-32k'

            try:
                from volcenginesdkarkruntime import Ark
            except ImportError:
                return jsonify({'success': False, 'error': '未安装 volcenginesdkarkruntime 库，请运行: pip install volcengine-python-sdk'}), 500

            client = Ark(api_key=api_key, base_url=base_url)
            messages = [
                {"role": "user", "content": test_message}
            ]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            if not response.choices or not response.choices[0].message.content:
                return jsonify({'success': False, 'error': '豆包 API 返回了空响应'}), 500
            reply = response.choices[0].message.content

        elif provider == 'claude':
            api_key = api_keys.get('claude') or env_config.get('CLAUDE_API_KEY', '')
            if not api_key:
                return jsonify({'success': False, 'error': 'Claude API Key 未提供'}), 400
            if not model:
                model = 'claude-3-haiku-20240307'

            try:
                from anthropic import Anthropic
            except ImportError:
                return jsonify({'success': False, 'error': '未安装 anthropic 库，请运行: pip install anthropic'}), 500

            client = Anthropic(api_key=api_key)
            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": test_message}]
            )
            if not response.content or not response.content[0].text:
                return jsonify({'success': False, 'error': 'Claude API 返回了空响应'}), 500
            reply = response.content[0].text

        elif provider == 'openai':
            api_key = api_keys.get('openai') or env_config.get('OPENAI_API_KEY', '')
            base_url = api_keys.get('openai_base') or env_config.get('OPENAI_API_BASE', '')
            if not api_key:
                return jsonify({'success': False, 'error': 'OpenAI API Key 未提供'}), 400
            if not base_url:
                return jsonify({'success': False, 'error': 'OpenAI API Base URL 未配置'}), 400
            if not model:
                model = 'gpt-3.5-turbo'

            try:
                from openai import OpenAI
            except ImportError:
                return jsonify({'success': False, 'error': '未安装 openai 库，请运行: pip install openai'}), 500

            client = OpenAI(api_key=api_key, base_url=base_url)
            messages = [
                {"role": "user", "content": test_message}
            ]
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            if not response.choices or not response.choices[0].message.content:
                return jsonify({'success': False, 'error': 'OpenAI API 返回了空响应'}), 500
            reply = response.choices[0].message.content

        else:
            return jsonify({'success': False, 'error': f'不支持的 AI 提供商: {provider}'}), 400

        return jsonify({
            'success': True,
            'message': f'{provider} API 连接测试成功',
            'data': {
                'provider': provider,
                'model': model,
                'test_message': test_message,
                'reply': reply[:200] if len(reply) > 200 else reply
            }
        })

    except Exception as e:
        error_info = {
            'success': False,
            'error': str(e),
            'error_type': e.__class__.__name__
        }
        if provider:
            error_info['provider'] = provider
        return jsonify(error_info), 500


@config_bp.route('/config/test/chat', methods=['POST'])
def test_chat():
    """测试会话聊天接口"""
    provider = None
    try:
        data = request.json or {}
        provider = data.get('provider', 'doubao')
        message = data.get('message', '')
        context = data.get('context', [])

        if not message:
            return jsonify({'success': False, 'error': '消息不能为空'}), 400

        env_config = load_env_file()
        if 'error' in env_config:
            return jsonify({'success': False, 'error': env_config['error']}), 500

        config_data = load_yaml_file(CONFIG_YAML)
        if 'error' in config_data:
            return jsonify({'success': False, 'error': config_data['error']}), 500

        ai_config = config_data.get('ai', {}) if isinstance(config_data, dict) else {}
        model = data.get('model') or ai_config.get('model', '')
        temperature = float(ai_config.get('temperature', 0.8))
        max_tokens = int(ai_config.get('max_tokens', 1000))
        api_keys = data.get('api_keys', {})

        if provider == 'doubao':
            api_key = env_config.get('DOUBAO_API_KEY', '')
            base_url = api_keys.get('doubao_base') or env_config.get('DOUBAO_API_BASE', '')
            if not api_key:
                return jsonify({'success': False, 'error': '豆包 API Key 未配置'}), 400
            if not base_url:
                return jsonify({'success': False, 'error': '豆包 API Base URL 未配置'}), 400
            if not model:
                model = 'doubao-pro-32k'

            try:
                from volcenginesdkarkruntime import Ark
            except ImportError:
                return jsonify({'success': False, 'error': '未安装 volcenginesdkarkruntime 库'}), 500

            client = Ark(api_key=api_key, base_url=base_url)
            messages = []
            for ctx in context:
                messages.append({"role": ctx["role"], "content": ctx["content"]})
            messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            if not response.choices or not response.choices[0].message.content:
                return jsonify({'success': False, 'error': 'AI 返回了空响应'}), 500
            reply = response.choices[0].message.content

        elif provider == 'claude':
            api_key = env_config.get('CLAUDE_API_KEY', '')
            if not api_key:
                return jsonify({'success': False, 'error': 'Claude API Key 未配置'}), 400
            if not model:
                model = 'claude-3-haiku-20240307'

            try:
                from anthropic import Anthropic
            except ImportError:
                return jsonify({'success': False, 'error': '未安装 anthropic 库'}), 500

            client = Anthropic(api_key=api_key)
            messages = []
            for ctx in context:
                messages.append({"role": ctx["role"], "content": ctx["content"]})
            messages.append({"role": "user", "content": message})

            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=messages
            )
            if not response.content or not response.content[0].text:
                return jsonify({'success': False, 'error': 'AI 返回了空响应'}), 500
            reply = response.content[0].text

        elif provider == 'openai':
            api_key = api_keys.get('openai') or env_config.get('OPENAI_API_KEY', '')
            base_url = api_keys.get('openai_base') or env_config.get('OPENAI_API_BASE', '')
            if not api_key:
                return jsonify({'success': False, 'error': 'OpenAI API Key 未配置'}), 400
            if not base_url:
                return jsonify({'success': False, 'error': 'OpenAI API Base URL 未配置'}), 400
            if not model:
                model = 'gpt-3.5-turbo'

            try:
                from openai import OpenAI
            except ImportError:
                return jsonify({'success': False, 'error': '未安装 openai 库'}), 500

            client = OpenAI(api_key=api_key, base_url=base_url)
            messages = []
            for ctx in context:
                messages.append({"role": ctx["role"], "content": ctx["content"]})
            messages.append({"role": "user", "content": message})

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            if not response.choices or not response.choices[0].message.content:
                return jsonify({'success': False, 'error': 'AI 返回了空响应'}), 500
            reply = response.choices[0].message.content

        else:
            return jsonify({'success': False, 'error': f'不支持的 AI 提供商: {provider}'}), 400

        return jsonify({
            'success': True,
            'data': {
                'provider': provider,
                'model': model,
                'reply': reply
            }
        })

    except Exception as e:
        error_info = {
            'success': False,
            'error': str(e),
            'error_type': e.__class__.__name__
        }
        if provider:
            error_info['provider'] = provider
        return jsonify(error_info), 500
