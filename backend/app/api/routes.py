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
from app.models.EconIndex import EconIndex, EconIndexStats, get_title_percentage
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

async def handle_image_processing(
    image: UploadFile, 
    size: str, 
    background_color: str, 
    compression: int,
    request_id: str
) -> tuple:
    """
    处理图片并返回结果
    
    返回:
        (processed_image, status, error_message)
    """
    try:
        # 读取上传的文件内容
        contents = await image.read()
        file_obj = io.BytesIO(contents)
        file_obj.filename = image.filename
        
        # 处理图片
        logger.debug(f"[{request_id}] 开始处理图片")
        processed_image = process_image(file_obj, size, background_color, compression, request_id)
        logger.debug(f"[{request_id}] 图片处理成功")
        
        return processed_image, "success", None
    except Exception as e:
        logger.error(f"[{request_id}] 处理图片时出错: {str(e)}", exc_info=True)
        return None, "error", str(e)

@router.post("/process")
async def process_route(
    request: Request,
    image: UploadFile = File(...),
    size: str = Form("1"),
    background_color: str = Form("#FFFFFF"),
    compression: str = Form("20"),
    db: None = Depends(get_db)
):
    """
    处理图片API
    
    参数:
        image: 上传的图片文件
        size: 照片尺寸（1寸/2寸）
        background_color: 背景颜色，如 #FFFFFF
        compression: 压缩率 (0-100)
    
    返回:
        处理后的图片
    """
    # 生成唯一请求ID
    request_id = generate_request_id()
    logger.info(f"[{request_id}] 收到处理图片请求: {image.filename}")
    logger.info(f"[{request_id}] 处理参数：size={size}, background_color={background_color}, compression={compression}")
    
    # 验证输入参数
    if not image.filename:
        raise HTTPException(status_code=400, detail="无效的文件名")
    
    if not allowed_file(image.filename):
        raise HTTPException(status_code=400, detail="不支持的文件类型")
    
    try:
        compression_int = int(compression)
        if compression_int < 0 or compression_int > 100:
            raise HTTPException(status_code=400, detail="压缩率必须在0-100之间")
    except ValueError:
        raise HTTPException(status_code=400, detail="无效的压缩率")
    
    error_message = None
    # 处理图片
    processed_image, status, error_message = await handle_image_processing(
        image, size, background_color, compression_int, request_id
    )
    
    # 如果处理失败，抛出异常
    if status == "error":
        # 记录错误到数据库
        create_image_record(
            original_filename=image.filename,
            size=size,
            background_color=background_color,
            compression=compression_int,
            ip_address=get_client_ip(request),
            user_agent=request.headers.get("user-agent", ""),
            status="error",
            error_message=error_message
        )
        raise HTTPException(status_code=500, detail=error_message)
    
    # 记录成功处理到数据库
    create_image_record(
        original_filename=image.filename,
        size=size,
        background_color=background_color,
        compression=compression_int,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("user-agent", ""),
        status="success",
        error_message=error_message
    )
    
    # 创建响应
    logger.info(f"[{request_id}] 返回处理后的图片")
    response = Response(content=processed_image.getvalue(), media_type="image/jpeg")
    response.headers["Content-Disposition"] = f"attachment; filename=processed_{image.filename}"
    
    return response

@router.get("/download/{order_id}")
async def download(order_id: str, request: Request):
    """
    下载处理后的图片
    
    参数:
        order_id: 订单ID
    
    返回:
        图片文件
    """
    # 检查订单是否存在
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 检查订单状态
    order = orders[order_id]
    if order["status"] != "paid":
        raise HTTPException(status_code=403, detail="订单未支付")
    
    # 获取图片路径
    image_path = order["image_path"]
    
    # 返回图片文件
    return FileResponse(
        image_path, 
        filename=f"photo_{order_id}.jpg",
        media_type="image/jpeg"
    )

@router.get("/stats")
async def stats_route(db: None = Depends(get_db)):
    """
    获取处理统计信息
    
    返回:
        处理统计信息
    """
    stats = get_stats()
    return JSONResponse(content=stats)

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