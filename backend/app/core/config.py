"""
核心配置模块 - 集中管理应用配置
"""
import os
import logging
import sys
from pathlib import Path
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 尝试加载.env文件
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print(f"已加载环境变量配置文件: {env_path}")
else:
    print(f"警告: 环境变量配置文件不存在: {env_path}，将使用默认值或系统环境变量")

# 应用基本配置
APP_NAME = "Anthropic Economic Index"
VERSION = "0.0.1"
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')  # 'development', 'testing', 'production'

# 数据库配置
DB_TYPE = os.environ.get('DB_TYPE', 'sqlite').lower()
DB_CONFIG = {
    'sqlite': {
        'filename': os.environ.get('DATABASE_PATH', str(BASE_DIR / 'data' / 'database.sqlite')),
        'create_db': True
    },
    'mysql': {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': int(os.environ.get('DB_PORT', '3306')),
        'user': os.environ.get('DB_USER', 'root'),
        'passwd': os.environ.get('DB_PASSWORD', ''),
        'db': os.environ.get('DB_NAME', 'easy_id_photo'),
        'charset': 'utf8mb4'
    }
}

# 日志配置
LOG_DIR = os.environ.get('LOG_DIR', str(BASE_DIR / 'logs'))
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_MAX_BYTES = int(os.environ.get('LOG_MAX_BYTES', 10 * 1024 * 1024))  # 10MB
LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', 5))

# 服务器配置
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', '5000'))

# Uvicorn配置
WORKERS = int(os.environ.get('WORKERS', '1'))
RELOAD = DEBUG

# 初始化标志，用于防止重复初始化
_is_app_initialized = False

def setup_logging():
    """
    配置日志系统
    
    返回:
        根日志记录器
    """
    global _is_app_initialized
    
    # 确保日志目录存在
    log_dir = Path(LOG_DIR)
    if not log_dir.exists():
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # 设置日志级别
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    # 配置日志
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout),
            RotatingFileHandler(
                str(log_dir / 'app.log'),
                maxBytes=LOG_MAX_BYTES,
                backupCount=LOG_BACKUP_COUNT,
                encoding='utf-8'
            )
        ]
    )
    
    # 获取根日志记录器
    logger = logging.getLogger()
    
    # 只在首次初始化时记录详细信息
    if not _is_app_initialized:
        logger.info(f"日志系统初始化完成，级别: {LOG_LEVEL}, 目录: {LOG_DIR}")
        
        # 记录环境变量加载情况
        if env_path.exists():
            logger.info(f"已加载环境变量配置文件: {env_path}")
        else:
            logger.warning(f"环境变量配置文件不存在: {env_path}，使用默认值或系统环境变量")
        
        # 记录应用环境
        logger.info(f"应用环境: {ENVIRONMENT}, 调试模式: {DEBUG}")
        
        # 设置初始化标志
        _is_app_initialized = True
    else:
        logger.debug("日志系统已初始化，跳过详细日志")
    
    return logger

# 创建默认日志记录器
logger = setup_logging()
