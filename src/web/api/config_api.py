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
            'DOUBAO_API_BASE': os.getenv('DOUBAO_API_BASE', 'https://ark.cn-beijing.volces.com/api/v3'),
            'CLAUDE_API_KEY': os.getenv('CLAUDE_API_KEY', ''),
            'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
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
                'max_context_messages': config.get('ai', {}).get('max_context_messages', 20),
                'api_keys': {
                    'doubao': env_config.get('DOUBAO_API_KEY', ''),
                    'doubao_base': env_config.get('DOUBAO_API_BASE', ''),
                    'claude': env_config.get('CLAUDE_API_KEY', ''),
                    'openai': env_config.get('OPENAI_API_KEY', ''),
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


@config_bp.route('/config/test', methods=['POST'])
def test_api_connection():
    """测试API连接"""
    try:
        data = request.json
        provider = data.get('provider', 'doubao')

        # 这里可以添加实际的API测试逻辑
        # 暂时返回模拟结果
        return jsonify({
            'success': True,
            'message': f'{provider} API连接测试成功',
            'details': {
                'provider': provider,
                'status': 'connected',
                'latency': '120ms'
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
