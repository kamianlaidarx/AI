"""
配置管理模块
负责加载和管理项目配置
"""
import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class Config:
    """配置管理类"""

    def __init__(self, config_path: str = "config/config.yaml"):
        """
        初始化配置管理器

        Args:
            config_path: 配置文件路径
        """
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._load_env()
        self._load_config()

    def _load_env(self):
        """加载环境变量"""
        env_path = Path("config/.env")
        if env_path.exists():
            load_dotenv(env_path)

    def _load_config(self):
        """加载YAML配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置项

        Args:
            key: 配置键，支持点号分隔的嵌套键，如 'ai.model'
            default: 默认值

        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def get_env(self, key: str, default: str = None) -> str:
        """
        获取环境变量

        Args:
            key: 环境变量名
            default: 默认值

        Returns:
            环境变量值
        """
        return os.getenv(key, default)

    def reload(self):
        """重新加载配置"""
        self._load_env()
        self._load_config()


# 全局配置实例
config = Config()
