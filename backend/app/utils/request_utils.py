"""
请求工具模块 - 提供请求处理相关功能
"""
import time
import logging

# 获取日志记录器
logger = logging.getLogger(__name__)

def generate_request_id():
    """
    生成唯一的请求ID
    
    返回:
        字符串，格式为 'req-{timestamp}'
    """
    return f"req-{int(time.time() * 1000)}" 