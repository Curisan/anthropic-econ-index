"""
API路由模块 - 定义API端点和处理函数
"""
import io
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile, Request, Depends, HTTPException, Response
from fastapi.responses import FileResponse, JSONResponse
from pony.orm import db_session

from app.models.database import is_db_initialized
from app.models.EconIndex import EconIndex, EconIndexStats, get_title_percentage, search_titles_by_keyword
from app.utils.request_utils import generate_request_id

# 获取日志记录器
logger = logging.getLogger(__name__)

# 创建路由器
router = APIRouter()

# 订单信息存储
orders = {}

def get_db():
    """获取数据库会话，用于依赖注入"""
    if not is_db_initialized():
        logger.warning("数据库未完全初始化，某些功能可能不可用")
    yield None  # 使用Pony ORM的db_session装饰器，不需要实际传递会话

def get_client_ip(request: Request) -> str:
    """获取客户端真实IP地址"""
    # 首先检查常见的代理头
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # 取第一个IP（最原始的客户端）
        return forwarded_for.split(",")[0].strip()
    
    # 然后检查其他可能的头
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # 最后使用直接客户端IP，如果可用
    if request.client and request.client.host:
        return request.client.host
    
    # 默认值
    return "127.0.0.1"


@router.get("/health")
async def health_check():
    """
    健康检查API
    
    返回:
        应用健康状态
    """
    # 检查数据库是否已初始化
    db_status = "ok" if is_db_initialized() else "error"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
        "components": {
            "database": db_status,
            "api": "ok"
        }
    } 


# 添加经济指数相关API路由

@router.get("/occupation/search")
async def search_occupations(keyword: str = "", language: str = "cn", limit: int = 100, db: None = Depends(get_db)):
    """
    根据关键词搜索职业
    
    参数:
        keyword: 搜索关键词
        language: 语言选择 ('en' 或 'cn')
        limit: 返回结果数量限制
        
    返回:
        匹配的职业列表
    """
    logger.info(f"搜索职业，关键词: {keyword}, 语言: {language}")
    
    if not keyword:
        return {"occupations": []}
    
    try:
        # 使用已有的search_titles_by_keyword函数进行搜索
        titles = search_titles_by_keyword(keyword, language)

        print("titles", titles)
        
        # 限制结果数量
        titles = titles[:limit]

        occupations = titles
        
        logger.info(f"搜索结果: 找到 {len(occupations)} 个匹配的职业")
        return {"occupations": occupations}
    
    except Exception as e:
        logger.error(f"搜索职业失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@router.get("/occupation/tasks")
async def get_occupation_tasks(title: str = "", language: str = "cn", db: None = Depends(get_db)):
    """
    获取指定职业的任务分布百分比
    
    参数:
        title: 职业名称
        language: 语言选择 ('en' 或 'cn')
        
    返回:
        任务分布百分比列表
    """
    logger.info(f"获取职业任务分布，职业: {title}, 语言: {language}")
    
    if not title:
        return {"tasks": []}
    
    try:
        # 使用get_title_percentage函数获取任务分布
        tasks_data = get_title_percentage(title, language)
        
        # 转换数据格式
        tasks = [
            {
                "task": task,
                "percentage": percentage
            }
            for task, percentage in tasks_data.items()
        ]
        
        # 按百分比降序排序
        tasks.sort(key=lambda x: x["percentage"], reverse=True)
        
        logger.info(f"获取任务分布成功: {len(tasks)} 个任务")
        return {"tasks": tasks}
    
    except Exception as e:
        logger.error(f"获取职业任务分布失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取任务分布失败: {str(e)}")