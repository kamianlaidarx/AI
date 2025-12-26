"""
日志系统模块
基于loguru实现的日志管理
"""
import sys
from pathlib import Path
from loguru import logger


class Logger:
    """日志管理类"""

    def __init__(self, log_file: str = "logs/ailive.log", level: str = "INFO"):
        """
        初始化日志系统

        Args:
            log_file: 日志文件路径
            level: 日志级别
        """
        self.log_file = Path(log_file)
        self.level = level
        self._setup_logger()

    def _setup_logger(self):
        """配置日志系统"""
        # 移除默认的handler
        logger.remove()

        # 添加控制台输出
        logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=self.level,
            colorize=True
        )

        # 确保日志目录存在
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # 添加文件输出
        logger.add(
            self.log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            level=self.level,
            rotation="100 MB",  # 文件大小达到100MB时轮转
            retention="30 days",  # 保留30天
            compression="zip",  # 压缩旧日志
            encoding="utf-8"
        )

    def get_logger(self):
        """获取logger实例"""
        return logger


# 全局logger实例
log = Logger().get_logger()
