"""
模型包初始化文件
"""
# 直接导入所有需要的组件
from app.models.database import (
    db, 
    setup_database, 
    is_db_initialized
)

from app.models.EconIndex import EconIndex, EconIndexStats, get_title_percentage

# 导出公共API
__all__ = [
    'db', 
    'setup_database', 
    'get_title_percentage', 
    'is_db_initialized', 
    'EconIndex',
    'EconIndexStats',
] 