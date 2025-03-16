"""
核心包初始化文件
"""
from app.core.config import logger, DEBUG, ENVIRONMENT, DB_TYPE, DB_CONFIG, setup_logging

__all__ = ['logger', 'DEBUG', 'ENVIRONMENT', 'DB_TYPE', 'DB_CONFIG', 'setup_logging'] 