"""
AILive Web管理面板
提供配置管理的Web界面
"""
import os
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import Config
from src.web.api.config_api import config_bp

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 注册蓝图
app.register_blueprint(config_bp, url_prefix='/api')

# 配置
app.config['SECRET_KEY'] = 'ailive-secret-key-change-in-production'
app.config['JSON_AS_ASCII'] = False  # 支持中文


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'message': 'AILive Web Panel is running'})


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("AILive Web管理面板启动中...")
    print("访问地址: http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)
