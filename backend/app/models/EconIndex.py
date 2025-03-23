"""
图片记录实体模块 - 定义图片处理记录的数据模型
"""
from datetime import datetime
from pony.orm import PrimaryKey, Required, db_session, select, Optional

from app.models.database import db
from app.models.database import is_db_initialized
from app.core.config import logger
from app.utils.timer import timer, TimerContext

class EconIndex(db.Entity):
    id = PrimaryKey(int, auto=True)
    onet_soc_code = Required(str)
    title = Required(str) # 职业名称
    task_id = Required(int)
    task = Required(str, max_len=1024)  # 任务描述,可能较长
    task_type = Required(str)
    incumbents_responding = Required(int)
    date = Required(str) 
    domain_source = Required(str)
    percentage = Required(float)  # 该任务占所有对话的百分比
    title_cn = Required(str)
    task_cn = Required(str, max_len=1024)  # 任务描述,可能较长
    automated_score = Required(int)
    automated_score_reason = Required(str, max_len=4096)

    def to_dict(self):
        """将实体转换为字典，用于API响应"""
        result = dict(self._vals_)
        return result
    
class EconIndexStats(db.Entity):
    id = PrimaryKey(int, auto=True)
    title = Required(str)
    title_cn = Required(str)
    percentage_sum = Required(float) # 职业所有对话的百分比
    percentage_non_zero = Required(float) # 职业非零对话的百分比
    automated_score_avg = Required(float) # 职业自动化平均分

    def to_dict(self):
        """将实体转换为字典，用于API响应"""
        result = dict(self._vals_)
        return result

class OccupationSearchRecord(db.Entity):
    """职业搜索记录模型，用于记录用户查询的职业"""
    id = PrimaryKey(int, auto=True)
    title = Required(str)  # 查询的职业名称
    language = Required(str)  # 查询使用的语言(en/cn)
    search_time = Required(datetime, default=datetime.now)  # 查询时间
    client_ip = Optional(str)  # 客户端IP地址
    
    def to_dict(self):
        """将实体转换为字典，用于API响应"""
        return {
            "id": self.id,
            "title": self.title,
            "language": self.language,
            "search_time": self.search_time.isoformat(),
            "client_ip": self.client_ip
        }

@timer
@db_session
def get_title_percentage(title: str, language: str) -> dict:
    """
    获取职业各任务的百分比
    """
    try:
        # 获取职业信息
        if language == 'en':
            task_info = EconIndex.select(lambda s: s.title == title)
        else:
            task_info = EconIndex.select(lambda s: s.title_cn == title)

        # 返回任务对应的百分比
        task_percentage_dict = {}
        for task in task_info:
            if language == 'en':
                task_percentage_dict[task.task] = task.percentage
            else:
                task_percentage_dict[task.task_cn] = task.percentage

        return task_percentage_dict
    except Exception as e:
        logger.error(f"获取职业: {title} 的统计信息失败: {str(e)}", exc_info=True)
        return {}

@timer
@db_session
def search_titles_by_keyword(keyword: str, language: str) -> list:
    """
    根据关键字搜索职业标题
    
    参数:
        keyword: 搜索关键字
        language: 语言选择 ('en' 或 'cn')
        
    返回:
        匹配的职业标题列表
    """
    try:
        with TimerContext("搜索职业标题"):
            if language == 'en':
                # 英文标题搜索
                titles = select(e.title for e in EconIndex 
                            if keyword in e.title)
            else:
                # 中文标题搜索
                titles = select(e.title_cn for e in EconIndex 
                            if keyword in e.title_cn)
            
        return list(titles)
    except Exception as e:
        logger.error(f"搜索职业标题失败,关键字:{keyword}, 错误:{str(e)}", exc_info=True)
        return []

@db_session
def record_occupation_search(title: str, language: str, client_ip: str = None):
    """
    记录职业搜索
    
    参数:
        title: 搜索的职业名称
        language: 使用的语言
        client_ip: 客户端IP地址
    """
    try:
        OccupationSearchRecord(
            title=title, 
            language=language, 
            client_ip=client_ip
        )
        # 因为使用了@db_session装饰器，提交是自动的
        return True
    except Exception as e:
        logger.error(f"记录职业搜索失败, 职业: {title}, 错误: {str(e)}", exc_info=True)
        return False

@db_session
def get_popular_occupation_searches(limit: int = 10, days: int = 30):
    """
    获取最近一段时间内热门搜索的职业
    
    参数:
        limit: 返回的结果数量
        days: 最近几天的数据
        
    返回:
        包含职业名称和搜索次数的列表
    """
    try:
        from_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        from_date = from_date.replace(day=from_date.day - days)
        
        # 查询最近days天内搜索次数最多的职业
        query = select((r.title, count(r)) for r in OccupationSearchRecord 
                      if r.search_time >= from_date)
        query = query.order_by(lambda t: t[1], desc=True)
        query = query.limit(limit)
        
        # 构建结果
        results = [{
            "title": title,
            "count": count
        } for title, count in query]
        
        return results
    except Exception as e:
        logger.error(f"获取热门职业搜索失败: {str(e)}", exc_info=True)
        return []
