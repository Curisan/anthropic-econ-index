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
from app.models.EconIndex import EconIndex, EconIndexStats, get_title_percentage, search_titles_by_keyword, record_occupation_search, get_popular_occupation_searches, add_feedback, get_feedbacks, occupation_stats
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
async def search_occupations(keyword: str = "", language: str = "cn", limit: int = 100, request: Request = None, db: None = Depends(get_db)):
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
        
        # 这里不记录搜索关键词，只记录用户最终选择的职业
        
        return {"occupations": occupations}
    
    except Exception as e:
        logger.error(f"搜索职业失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"搜索失败: {str(e)}")

@router.get("/occupation/tasks")
async def get_occupation_tasks(title: str = "", language: str = "cn", request: Request = None, db: None = Depends(get_db)):
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
        # 记录职业查询
        client_ip = get_client_ip(request) if request else None
        record_occupation_search(title, language, client_ip)
        
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

@router.get("/occupation/popular")
async def get_popular_occupations(days: int = 30, limit: int = 10, db: None = Depends(get_db)):
    """
    获取热门搜索的职业
    
    参数:
        days: 最近几天的数据
        limit: 返回的结果数量
        
    返回:
        热门职业列表，包含职业名称和搜索次数
    """
    logger.info(f"获取热门职业，天数: {days}, 限制: {limit}")
    
    try:
        popular_occupations = get_popular_occupation_searches(limit, days)
        
        logger.info(f"获取热门职业成功: {len(popular_occupations)} 个职业")
        return {"occupations": popular_occupations}
    
    except Exception as e:
        logger.error(f"获取热门职业失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取热门职业失败: {str(e)}")

# 反馈相关API
@router.post("/feedback")
async def submit_feedback(
    feedback_type: str = Form(...),
    feedback_content: str = Form(...),
    request: Request = None,
    db: None = Depends(get_db)
):
    """
    提交用户反馈
    
    参数:
        feedback_type: 反馈类型('建议', '问题', '其他')
        feedback_content: 反馈内容
        
    返回:
        反馈提交状态
    """
    logger.info(f"提交反馈, 类型: {feedback_type}")
    
    try:
        # 获取客户端IP
        client_ip = get_client_ip(request) if request else None
        
        # 添加反馈
        feedback_id = add_feedback(
            feedback_type=feedback_type,
            feedback_content=feedback_content,
            client_ip=client_ip
        )
        
        if feedback_id:
            logger.info(f"反馈提交成功，ID: {feedback_id}")
            return {"success": True, "feedback_id": feedback_id}
        else:
            logger.warning("反馈提交失败")
            return {"success": False, "error": "反馈提交失败"}
    
    except Exception as e:
        logger.error(f"提交反馈失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"提交反馈失败: {str(e)}")

@router.get("/feedback")
async def get_feedback_list(
    days: int = 30,
    limit: int = 50,
    db: None = Depends(get_db)
):
    """
    获取反馈列表
    
    参数:
        days: 最近几天的数据，默认30天
        limit: 返回的结果数量，默认50条
        
    返回:
        反馈列表
    """
    logger.info(f"获取反馈列表, 天数: {days}")
    
    try:
        feedbacks = get_feedbacks(
            days=days,
            limit=limit
        )
        
        logger.info(f"获取反馈列表成功: {len(feedbacks)} 条")
        return {"feedbacks": feedbacks}
    
    except Exception as e:
        logger.error(f"获取反馈列表失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取反馈列表失败: {str(e)}")
    
@router.get("/occupation/stats")
async def get_occupation_stats(type: str = "percentage_sum", limit: int = 20, db: None = Depends(get_db)):
    """
    获取所有职业的统计数据
    
    返回:
        职业统计数据列表，包含每个职业的总对话占比、非零任务平均占比和自动化分数
    """
    logger.info("获取职业统计数据")
    
    try:
        stats = occupation_stats(type, limit)
        logger.info(f"获取职业统计数据成功: {len(stats)} 个职业")
        return {"stats": stats}
    except Exception as e:
        logger.error(f"获取职业统计数据失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"获取职业统计数据失败: {str(e)}") 