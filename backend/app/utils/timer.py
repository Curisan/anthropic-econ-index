"""
通用工具模块 - 提供通用功能
"""
import time
from functools import wraps
from app.core.config import logger

def timer(func):
    """
    计时装饰器,用于测量函数执行时间
    
    参数:
        func: 需要计时的函数
        
    返回:
        包装后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        logger.info(f"函数 {func.__name__} 执行时间: {duration:.3f} 秒")
        return result
    return wrapper

class TimerContext:
    """
    计时上下文管理器,用于测量代码块执行时间
    
    用法:
        with TimerContext("操作名称"):
            # 需要计时的代码
    """
    def __init__(self, name):
        """
        初始化计时器
        
        参数:
            name: 计时操作的名称标识
        """
        self.name = name
        self.start_time = None
        
    def __enter__(self):
        """进入上下文时开始计时"""
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时结束计时并记录"""
        duration = time.time() - self.start_time
        logger.info(f"{self.name} 执行时间: {duration:.3f} 秒")

