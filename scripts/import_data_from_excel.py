import pandas as pd
from pony.orm import db_session
from datetime import datetime

from app.models import setup_database, is_db_initialized
from app.models.EconIndex import EconIndex, update_occupation_stats
from app.core.config import DB_TYPE, DB_CONFIG

# 读取Excel文件
csv_file = 'assets/onet_tasks_with_mapping_pct_CN.csv'
df = pd.read_csv(csv_file, encoding='gbk')

# 初始化数据库
db = setup_database(DB_TYPE, DB_CONFIG)

"""
O*NET-SOC Code,Title,Task ID,Task,Task Type,Incumbents Responding,Date,Domain Source,pct,Task_CN,Title_CN,Automated_Score,Automated_Score_Reason
"""

@db_session
def import_data_from_excel():
    for index, row in df.iterrows():
        try:
            print(row)
            print(type(row['Task Type']))
                
            # 创建新记录
            EconIndex(
                onet_soc_code=row['O*NET-SOC Code'],
                title=row['Title'],
                task_id=int(row['Task ID']),
                task=row['Task'],
                task_type=row['Task Type'] if not pd.isna(row['Task Type']) else "未知",
                incumbents_responding=int(row['Incumbents Responding']) if not pd.isna(row['Incumbents Responding']) else 0,
                date=row['Date'],
                domain_source=row['Domain Source'],
                percentage=float(row['pct']),
                title_cn=row['Title_CN'],
                task_cn=row['Task_CN'],
                automated_score=int(row['Automated_Score']),
                automated_score_reason=row['Automated_Score_Reason']
            )
        except Exception as e:
            print(f"导入第{index}行数据时出错: {str(e)}")
            break

if __name__ == "__main__":
    # import_data_from_excel()
    # 更新职业统计数据
    if update_occupation_stats():
        print("职业统计数据更新成功")
    else:
        print("职业统计数据更新失败")