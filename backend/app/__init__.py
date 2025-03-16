"""
应用包初始化文件 - 创建和配置FastAPI应用
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import setup_logging, DEBUG, ENVIRONMENT, DB_TYPE, DB_CONFIG
from app.models import setup_database, is_db_initialized
from app.api.routes import router

# 应用实例缓存
_app_instance = None

def create_app():
    """
    创建并配置FastAPI应用
    
    返回:
        配置好的FastAPI应用实例
    """
    global _app_instance
    
    # 如果应用已经初始化，直接返回缓存的实例
    if _app_instance is not None:
        return _app_instance
    
    # 设置日志
    logger = setup_logging()
    logger.info("正在初始化应用...")
    
    # 创建FastAPI应用
    app = FastAPI(
        title="EasyIDPhoto API",
        description="证件照处理服务API",
        version="1.0.0",
        debug=DEBUG
    )
    
    # 启用CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS已配置")
    
    # 初始化数据库
    logger.info("正在初始化数据库...")
    try:
        db = setup_database(DB_TYPE, DB_CONFIG)
        
        # 验证数据库是否正确初始化
        if not is_db_initialized():
            logger.error("数据库初始化后，验证失败")
            if ENVIRONMENT == 'production':
                raise RuntimeError("数据库初始化失败")
            logger.warning("在非生产环境中继续启动应用，但数据库功能可能不可用")
        else:
            # 验证ImageRecord类型
            from app.models.EconIndex import EconIndex
            if EconIndex is not None:
                logger.info(f"EconIndex类型: {type(EconIndex)}")
            else:
                logger.error("EconIndex仍为None，数据库初始化可能不完整")
            logger.info("数据库初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}", exc_info=True)
        # 在非生产环境中，我们可能希望应用继续启动，即使数据库初始化失败
        if ENVIRONMENT == 'production':
            raise
        logger.warning("在非生产环境中继续启动应用，但数据库功能可能不可用")
    
    # 存储数据库初始化状态
    app.state.db_initialized = is_db_initialized()
    
    # 注册路由
    app.include_router(router)
    logger.info("API路由已注册")
    
    # 存储处理后的图片
    app.state.processed_images = {}
    
    logger.info("应用初始化完成")
    
    # 缓存应用实例
    _app_instance = app
    
    return app