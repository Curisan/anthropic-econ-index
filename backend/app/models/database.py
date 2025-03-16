"""
数据库连接管理模块 - 处理数据库连接和初始化
"""
import os
import logging
from pony.orm import *
from pathlib import Path
from datetime import datetime

# 获取日志记录器
logger = logging.getLogger(__name__)

# 创建数据库实例
db = Database()

# 数据库初始化状态
_is_initialized = False

def setup_database(db_type, db_config):
    """
    设置数据库连接并初始化表结构
    
    参数:
        db_type: 数据库类型 ('sqlite' 或 'mysql')
        db_config: 数据库配置字典
    
    返回:
        数据库实例
    """
    global _is_initialized
    
    # 如果数据库已经初始化，则直接返回
    if _is_initialized:
        logger.info("数据库已经初始化，跳过重复初始化")
        return db
    
    logger.info(f"正在初始化数据库连接，数据库类型: {db_type}")
    
    try:
        # 根据数据库类型连接到不同的数据库
        if db_type == 'mysql':
            _connect_mysql(db_config)
        else:
            _connect_sqlite(db_config)
        
        # 创建表
        logger.info("开始创建数据库表")
        db.generate_mapping(create_tables=True)
        logger.info("数据库表创建成功")
        
        # 标记为已初始化
        _is_initialized = True
        
        return db
    except Exception as e:
        # 初始化失败时，重置状态
        _is_initialized = False
        logger.error(f"数据库初始化失败: {str(e)}", exc_info=True)
        raise

def _connect_mysql(db_config):
    """连接到MySQL数据库"""
    config = db_config['mysql']
    logger.info(f"连接到MySQL数据库: {config['user']}@{config['host']}:{config['port']}/{config['db']}")
    
    # 连接MySQL
    db.bind(provider='mysql', **config)
    logger.info("MySQL数据库连接成功")

def _connect_sqlite(db_config):
    """连接到SQLite数据库"""
    config = db_config['sqlite']
    db_path = config['filename']
    
    # 确保目录存在
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        logger.info(f"创建数据库目录: {db_dir}")
        os.makedirs(db_dir)
    
    logger.info(f"连接到SQLite数据库: {db_path}")
    
    # 连接SQLite
    db.bind(provider='sqlite', **config)
    logger.info("SQLite数据库连接成功")

def is_db_initialized():
    """检查数据库是否已初始化"""
    return _is_initialized